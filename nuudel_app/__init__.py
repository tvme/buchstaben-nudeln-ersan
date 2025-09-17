import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    static_path = os.path.join(os.path.dirname(__file__), 'static')
    print(f"Template path: {template_path}")
    app = Flask(__name__, 
                template_folder=template_path, 
                static_folder=static_path,
                instance_relative_config=True)
    app.config.from_object(Config)
    print('SQLALCHEMY_DATABASE_URI:', Config.SQLALCHEMY_DATABASE_URI)
    db.init_app(app)

    with app.app_context():
        from . import models  # Import models to register them with the app
        from .nuudel_game import Nuudel_game

        db.create_all()  # Create database tables
        animals = [
            "собака", "кошка", "лошадь", "корова", "свинья",
            "овца", "коза", "курица", "утка", "гусь",
            "тигр", "лев", "волк", "медведь", "заяц",
            "лось", "белка", "слон", "жираф"
        ]
        tools = [
            "молоток", "отвёртка", "пила", "гвоздодёр", "пассатижи",
            "шуруповёрт", "дрель", "стаместка", "рубанок",
            "напильник", "штангенциркуль", "лом", "паяльник",
            "ножовка", "уровень", "рулетка"
        ]
        kitchen_items = [
            "кастрюля", "сковорода", "чайник", "тарелка", "чашка",
            "ложка", "вилка", "нож", "миска",
            "терка", "половник", "дуршлаг", "холодильник", "духовка",
            "плита", "микроволновка", "блендер"
        ]
        gm = Nuudel_game()

        print(gm.update_category("animals", "easy"))
        print(gm.update_category("kitchen", "medium"))
        print(gm.update_category("tools", "hard"))
        print(gm.update_word(animals, "animals"))
        print(gm.update_word(tools, "tools"))
        print(gm.update_word(kitchen_items, "kitchen"))
        print("DB created or already exists")

    return app
