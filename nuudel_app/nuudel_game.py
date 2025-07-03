from nuudel_app import db, create_app
from nuudel_app.models import Word, Category
import random

class Nuudel_game():
    def __init__(self):
        self.db = db
        self.word = None
        self.category = "animals"

    def get_nuudel_word(self, category):
        """
        input:
            category: str категория для nuudel_word

        output:
            nuudel_word: str
        """
        self.category = category
        try:
            category_id = Category.query.filter_by(category=self.category).first()
        except:
            return "error: Not_category"
        word = Word.query.filter_by(category_id=category_id.id).order_by(db.func.random()).first()
        if not word:
            return "error: Not_word"
        self.word = word.word
        print(self.word)
        nuudel_word = ''.join(random.sample(self.word, len(self.word)))
        return nuudel_word

    def check_answer(self, answer_str):
        """
        input:
            answer_str: str, ответ пользователя

        output:
            score: int/None
        """
        if answer_str == self.word:
            return 10
        return self.word

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        def update_category(category_input):    
            existing = Category.query.filter_by(category=category_input).first()
            if existing:
                return "update_category status: Категория уже существует"
            category = Category(category=category_input)
            db.session.add(category)
            db.session.commit()
            return "update_category status: success"

        def update_word(wors, category_save):
            category = Category.query.filter_by(category=category_save).first()
            if not category:
                return f"Категория {category_save} не найдена"

            update_wors = 0

            for w in wors:
                existing_word = Word.query.filter_by(word=w, category_id=category.id).first()
                if not existing_word:
                    word_data = Word(word=w, category_ref=category)
                    db.session.add(word_data)
                    update_wors += 1
            db.session.commit()
            return f"update_word status: success  update_wors: {update_wors}"

        wors = [
            "тигр", "лев", "слон", "зебра", "волк",
            "медведь", "лисица", "кенгуру", "жираф", "панда", 
            "олень", "кошка",
        ]
        print(update_category("kitchen"))
        print(update_word(wors, "animals"))
        # game = Nuudel_game()
        # print(game.get_nuudel_word("animals"))