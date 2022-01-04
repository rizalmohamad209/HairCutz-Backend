from app import db
from sqlalchemy.sql import func

from app.models.userModel import Users


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_urut = db.Column(db.Integer)
    id_mitra = db.Column(db.Integer)
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id_user))
    date = db.Column(db.Date)
    status = db.Column(db.String(100))

    def __init__(self, no_urut, id_mitra, id_user, date, status):
        self.no_urut = no_urut
        self.id_user = id_user
        self.id_mitra = id_mitra
        self.date = date
        self.status = status
