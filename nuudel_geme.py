from nuudel_app import db
from nuudel_app.models import Word

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
    animals = [
        "тигр",
        "лев",
        "слон",
        "зебра",
        "волк",
        "медведь",
        "лисица",
        "кенгуру",
        "жираф",
        "панда"
        ]
    for w in animals:
        word_adata = Word(word=w, category="animals")
        db.session.add(word_adata)
        db.session.commit()