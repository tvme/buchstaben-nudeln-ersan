from flask import render_template, request, redirect, url_for
from nuudel_app import create_app

app = create_app()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        topic = request.form.get("topic")
        return redirect(url_for("play", topic=topic))
    return render_template("home.html", feedback="Добро пожаловать!")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email == "test@example.com" and password == "123":
            return redirect(url_for("user_page"))
        else:
            return render_template("login.html", error="Неверный email или пароль")
    return render_template("login.html")

@app.route("/user")
def user_page():
    user = {"email": "test@example.com", "name": "Саша", "password": "••••••", "score": 120}
    return render_template("user_page.html", user=user, feedback="Добро пожаловать, Саша!")

@app.route("/rating")
def user_table_page():
    players = [
        {"name": "Саша", "score": 120},
        {"name": "Аня", "score": 95},
        {"name": "Игорь", "score": 88},
        {"name": "Мария", "score": 75},
        {"name": "Nikolai", "score": 60}
    ]
    return render_template("user_table_page.html", players=players)

@app.route("/play")
def play():
    scrambled_word = "АРБКА"  # Например, "БАРКА"
    return render_template("nuudel_play.html", scrambled_word=scrambled_word)

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    guess = request.form.get("guess", "")
    feedback = "Правильно!" if guess.lower() == "барка" else "Попробуй ещё раз"
    return render_template("nuudel_play.html", scrambled_word="АРБКА", feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
