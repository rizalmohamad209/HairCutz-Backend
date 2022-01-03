import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    HOST = "localhost"
    DATABASE = "bigproject"
    USERNAME = "root"
    PASSWORD = "Rizalmohamad123"
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    SQLALCHEMY_DATABASE_URI = 'mysql://'+USERNAME+':'+PASSWORD+'@'+HOST+'/'+DATABASE
    #SQLALCHEMY_DATABASE_URI = 'postgresql://tnapfpqvoynmwg:554a1ee3d9e138f45a4f91a69828bc30e4a43ae2cf26f036f45bd72847f40228@ec2-3-95-130-249.compute-1.amazonaws.com:5432/d2sgqnt1p1t3lp'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
