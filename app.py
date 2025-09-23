from flask import render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask_mail import Mail, Message
from nuudel_app import create_app
from nuudel_app.models import User, Category
from nuudel_app import db
from nuudel_app.nuudel_game import Nuudel_game
from nuudel_app.game_logger import logger


app = create_app()
game = Nuudel_game()
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def send_confirmation_email(user_email):
    token = serializer.dumps(user_email, salt='email-confirm-salt')
    confirm_url = url_for('confirm_email', token=token, _external=True)
    mail_html = render_template('email_confirmation.html', confirm_url=confirm_url)
    msg = Message("Подтердите Email в Nuuel Game",
                  recipients=[user_email],
                  html=mail_html)
    try:
        mail.send(msg)
        logger.info(f"Письмо с подтверждением отправлено на {user_email}.")
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}", exc_info=True)

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id:
        try:
            g.user = User.query.get(user_id)
        except:
            g.user = None
    else:
        g.user = None

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        elif g.user.email_confirmed:
            return view(**kwargs)
        else:
            return render_template("home.html", feedback="Вам отправлен email, перейдите по ссылке для активации аккаунта.")
    return wrapped_view

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        category = request.form.get("category")
        return redirect(url_for("play", category=category))
    try:
        category_for_tabel = Category.query.all()
    except:
        return render_template("login.html", error="Ошибка базы данных")
    logger.debug(f"Доступные категории: {category_for_tabel}")
    return render_template("home.html", category_for_tabel=category_for_tabel, feedback="Добро пожаловать!")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mode = request.form.get("mode")
        logger.debug(f"Login mode: {mode}")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if mode == "register":
            name = request.form.get("name", "")
            confirm_password = request.form.get("confirm", "")
            try:
                user_in_db = User.query.filter_by(email=email).first()
                if user_in_db:
                    return render_template("login.html", feedback=f"Ползователь с {email} уже существует!")
            except:
                return render_template("login.html", error="Ошибка базы данных")
            if password != confirm_password:
                return render_template("login.html", error="Пароли не совпадают")
            hashed_password = generate_password_hash(password)
            user_data = User(email=email, name=name, password=hashed_password)
            try:
                db.session.add(user_data)
                db.session.commit()
            except:
                return render_template("login.html", error="Ошибка базы данных")
            session.clear()
            session["user_id"] = user_data.id
            session["user_email"] = user_data.email
            session["user_name"] = user_data.name
            session["email_confirmed"] = False
            send_confirmation_email(session["user_email"])
            return render_template("home.html", feedback="Вам отправлен email, перейдите по ссылке для активации аккаунта.")
        if mode == "login":
            try:
                user_login = User.query.filter_by(email=email).first()
            except:
                return render_template("login.html", error="Неверный email")
            if not user_login:
                return render_template("login.html", error="Пользователь не найден")
            if check_password_hash(user_login.password, password):
                session.clear()
                session["user_id"] = user_login.id
                session["user_email"] = user_login.email
                session["user_name"] = user_login.name
                return redirect(url_for("user_page"))
            else:
                return render_template("login.html", error="Неверный пароль")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/delete_account")
@login_required
def delete_account():
    user = User.query.get(session["user_id"])
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            session.clear()
            flash('Аккаунт успешно удален.', 'alert alert-success mt-3')
            logger.info(f"Пользователь {user.email} удалил свой аккаунт.")
            return redirect(url_for('home'))
        except Exception as e:
            logger.error(f"Ошибка при удалении аккаунта пользователя {user.email}: {e}.", exc_info=True)
            return render_template("home.html", error="Ошибка базы данных")
    else:
        return render_template("home.html", error="Пользователь не найден")

@app.route("/user_update", methods=["POST", "GET"])
@login_required
def user_update():
    if request.method == "POST":
        email = request.form.get("email", "")
        name = request.form.get("name", "")
        password = request.form.get("password", "")
        old_password = request.form.get("old_password", "")
        confirm = request.form.get("confirm", "")
        if confirm == password:
            try:
                user = User.query.get(session["user_id"])

                if not user:
                    return render_template("user_update.html", error="Пользователь не найден")
                
                if not check_password_hash(user.password, old_password):
                    return render_template("user_update.html", error="Старый пароль неверный", email=session["user_email"], name=session["user_name"])
                
                user.email = email
                user.name = name
                user.password = generate_password_hash(password)

                db.session.commit()
                
                session["user_email"] = email
                session["user_name"] = name
            except Exception as er:
                logger.error(f"Ошибка при обновлении данных пользователя {session['user_email']} {er}.", exc_info=True)
                return render_template("user_update.html", error="Ошибка базы данных", email=session["user_email"], name=session["user_name"])
        else:
            return render_template("user_update.html", error="Пароли не совпадают")
        return redirect(url_for('user_page'))
    return render_template("user_update.html", email=session["user_email"], name=session["user_name"])

@app.route("/user")
@login_required
def user_page():
    user_obj = User.query.filter_by(name=session["user_name"]).first()
    masked_password = "•••••"
    score = user_obj.score
    user = {"email": session["user_email"], "name": session["user_name"], "password": masked_password, "score": score}
    return render_template("user_page.html", user=user, feedback=f"Добро пожаловать, {session["user_name"]}!")

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(
            token,
            salt='email-confirm-salt',
            max_age=app.config['TOKEN_MAX_AGE_SECONDS']
        )

    except SignatureExpired: 
        return render_template("login.html", error='Срок действия ссылки истек. Пожалуйста, запросите новую.')
    except (BadTimeSignature, Exception):
        flash('Неверная или поврежденная ссылка для подтверждения.', 'danger')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Аккаунт уже подтвержден.', 'info')
    else:
        user.email_confirmed = True
        db.session.commit()
        session["email_confirmed"] = True
    return render_template('home.html', success = "Аккаунт подтвержден")

@app.route("/rating")
@login_required
def user_table_page():
    try:
        players = User.query.order_by(User.score.desc()).all()
    except:
        return render_template("login.html", error="Ошибка базы данных")
    logger.debug(f"Пользователи для таблицы рейтинга: {players}")
    return render_template("user_table_page.html", players=players)

@app.route("/play", methods=["POST"])
@login_required
def play():
    category = request.form.get("category", "animals")
    logger.info(f"Пользователь {session['user_name']} начал игру в категории {category}.")  
    try:
        scrambled_word = game.get_nuudel_word(category)

        if scrambled_word == "error: Not_category":
            return render_template("nuudel_play.html", error="Нет слов в этой категории.")
        
        if scrambled_word == "error: Not_word":
            return render_template("nuudel_play.html", error="Нет слов в этой категории.")
        
        return render_template("nuudel_play.html", scrambled_word=scrambled_word, word=game.word)
    
    except Exception as er:
        logger.error(f"Ошибка при получении слова для категории {category}.", exc_info=True)    
        return render_template("nuudel_play.html", error="Ошибка базы данных")

@app.route("/submit_answer", methods=["POST"])
@login_required
def submit_answer():
    logger.info("🚀 Hello Vercel, logging works!")
    logger.debug("This DEBUG log may not appear on Vercel")
    logger.error("❌ This is an ERROR log")
    guess = request.form.get("guess", "")
    logger.debug(f"Пользователь {session['user_name']} сделал попытку: {guess}")
    logger.debug(f"Правильный ответ: {game.word} | Категория: {game.category} | nuudel_word: {game.nuudel_word}")
    hinweis_anzal = request.form.get("hinweis_anzal", "")

    if game.check_answer(guess.lower()) == 10:
        difficulty = Category.query.filter_by(category=game.category).first()
        score = 10 - 5 * int(hinweis_anzal or 0)
        if difficulty.difficulty == "medium":
            score += 10
        if difficulty.difficulty == "hard":
            score += 20
        if score <= 0:
            score = 0
            success = "Правильно! но слишком много подсказек"
        else:
            try:
                success = f"Правильно! +{score}"
                user = User.query.filter_by(name=session["user_name"]).first()
                user.score += score
                db.session.commit()
            except Exception as e:
                logger.error(f"Ошибка при обновлении счета пользователя {session['user_name']}.", exc_info=True)
                return render_template("nuudel_play_success.html", error="Ошибка базы данных", category=game.category)
        return render_template("nuudel_play_success.html", success=success, category=game.category)
    else:
        feedback = "Попробуй ещё раз"
        return render_template("nuudel_play.html", scrambled_word=game.nuudel_word, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)