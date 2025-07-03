from flask import render_template, request, redirect, url_for, session, g
from nuudel_app import create_app
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from nuudel_app.models import User
from nuudel_app import db
from nuudel_app.nuudel_game import Nuudel_game


app = create_app()
game = Nuudel_game()

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
        return view(**kwargs)
    return wrapped_view

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        category = request.form.get("category")
        return redirect(url_for("play", category=category))
    return render_template("home.html", feedback="Добро пожаловать!")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mode = request.form.get("mode")
        print(f"Login mode: {mode}")
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
            return redirect(url_for("user_page"))
        if mode == "login":
            try:
                user_login = User.query.filter_by(email=email).first()
            except:
                return render_template("login.html", error="Неверный email")
            if check_password_hash(user_login.password, password):
                session.clear()
                session["user_id"] = user_login.id
                session["user_email"] = user_login.email
                session["user_name"] = user_login.name
                return redirect(url_for("user_page"))
            else:
                return render_template("login.html", error="Неверный пароль")
    return render_template("login.html")

@app.route("/user")
@login_required
def user_page():
    user = {"email": "test@example.com", "name": "Саша", "password": "••••••", "score": 120}
    return render_template("user_page.html", user=user, feedback="Добро пожаловать, Саша!")

@app.route("/rating")
@login_required
def user_table_page():
    try:
        players = User.query.order_by(User.score).all()
    except:
        return render_template("login.html", error="Ошибка базы данных")
    print(players)
    return render_template("user_table_page.html", players=players)

@app.route("/play", methods=["POST"])
@login_required
def play():
    category = request.form.get("category", "")

    try:
        scrambled_word = game.get_nuudel_word(category)

        if scrambled_word == "error: Not_category":
            return render_template("nuudel_play.html", error="Нет слов в этой категории.")
        
        if scrambled_word == "error: Not_word":
            return render_template("nuudel_play.html", error="Нет слов в этой категории.")
        
        return render_template("nuudel_play.html", scrambled_word=scrambled_word)
    
    except Exception as er:
        print(er)
        return render_template("nuudel_play.html", error="Ошибка базы данных")

@app.route("/submit_answer", methods=["POST"])
@login_required
def submit_answer():
    guess = request.form.get("guess", "")

    if game.check_answer(guess.lower()) == 10:
        success = "Правильно! +10"
        # return render_template("nuudel_play_success.html", success=success, category=game.category)
        return render_template("nuudel_play_success.html", success=success)
    else:
        feedback = "Попробуй ещё раз"
        return render_template("nuudel_play.html", scrambled_word=game.word, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)

# return render_template("nuudel_play_check.html", feedback=feedback, error="Ошибка базы данных", success=success)