from app import db


class Recomendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bentuk = db.Column(db.String(100))
    image = db.Column(db.Text)
    gender = db.Column(db.String(100))
    panjangrambut = db.Column(db.String(50))

    def __init__(self, bentuk, image, gender, panjangrambut):
        self.bentuk = bentuk
        self.image = image
        self.gender = gender
        self.panjangrambut = panjangrambut
