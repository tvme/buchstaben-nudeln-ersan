from nuudel_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    score = db.Column(db.Integer, default=0)
    
    def __init__(self, email, name, password, score=0):
        self.email = email
        self.name = name
        self.password = password
        self.score = score

    def __repr__(self):
        return f'User({self.name}, {self.email}, {self.score})'
    
class Word(db.Model):
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category_ref = db.relationship('Category', back_populates='words')

    def __init__(self, word, category_ref):
        self.word = word
        self.category_ref = category_ref

    def __repr__(self):
        return f'Word({self.word}, {self.category})'

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, category):
        self.category = category

    words = db.relationship('Word', back_populates='category_ref', cascade="all, delete-orphan")