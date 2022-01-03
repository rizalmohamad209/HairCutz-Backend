from app import db


class News(db.Model):
    id_news = db.Column(db.Integer, primary_key=True)
    mitra_id = db.Column(db.Integer)
    image = db.Column(db.String(200))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)

    def __init__(self, mitra_id, title, image, content):
        self.mitra_id = mitra_id
        self.image = image
        self.title = title
        self.content = content
