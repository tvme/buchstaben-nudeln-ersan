from nuudel_app import db, create_app
from nuudel_app.models import Word, Category

class Nuudel_game():
    def __init__(self):
        self.db = db

    def get_nuudel_word(self, category):
        """
        input:
            category: str категория для nuudel_word

        output:
            nuudel_word: str
        """
        pass

    def check_answer(self, answer_str):
        """
        input:
            answer_str: str, ответ пользователя

        output:
            score: int/None
        """
        pass

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        def update_category(category_input):    
            existing = Category.query.filter_by(category=category_input).first()
            if existing:
                return "Категория уже существует"
            category = Category(category=category_input)
            db.session.add(category)
            db.session.commit()
            return "update_category status: success"

        def update_word(wors, category_save):
            category = Category.query.filter_by(category=category_save).first()
            if not category:
                return f"Категория {category_save} не найдена"

            for w in wors:
                existing_word = Word.query.filter_by(word=w, category_id=category.id).first()
                if not existing_word:
                    word_data = Word(word=w, category_ref=category)
                    db.session.add(word_data)
            db.session.commit()
            return "update_word status: success"

    wors = [
        "тигр", "лев", "слон", "зебра", "волк",
        "медведь", "лисица", "кенгуру", "жираф", "панда"
    ]
    print(update_category("animals"))
    print(update_word(wors, "animals"))