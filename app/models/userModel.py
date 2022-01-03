from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    nama_user = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.Text)
    no_hp = db.Column(db.String(16))
    gender = db.Column(db.Enum('male', 'female'),
                       name='gender_type')
    role = db.Column(db.Enum('user', 'admin', 'adminMitra'),
                     nullable=False, server_default='user', name='role_type')

    def __init__(self, nama_user, username, email, no_hp, gender, role):
        self.nama_user = nama_user
        self.username = username
        self.email = email
        self.no_hp = no_hp
        self.gender = gender
        self.role = role

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)
