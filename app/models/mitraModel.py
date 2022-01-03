from app import db


class Mitra(db.Model):
    id_mitra = db.Column(db.Integer, primary_key=True)
    nama_mitra = db.Column(db.String(200))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    alamat_mitra = db.Column(db.Text)
    image = db.Column(db.String(200))
    jmlh_tukangCukur = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, nama_mitra, lat, long, alamat_mitra, image, jmlh_tukangCukur, user_id, ):
        self.nama_mitra = nama_mitra
        self.lat = lat
        self.long = long
        self.alamat_mitra = alamat_mitra
        self.image = image
        self.jmlh_tukangCukur = jmlh_tukangCukur
        self.user_id = user_id
