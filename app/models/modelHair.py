from app import db


class Hair(db.Model):
    id_hair = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Integer)
    nama_model = db.Column(db.String(200))

    def __init__(self, image, nama_model):
        self.image = image
        self.nama_model = nama_model
