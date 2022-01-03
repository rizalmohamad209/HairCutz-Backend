from flask import Flask  
from config import Config
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:Rizalmohamad123@localhost/rest_flask'
app.config.from_object(Config)
db = SQLAlchemy(app)
cloud=cloudinary.config(
    cloud_name = "dk4dgvu4w",
    api_key = "312482332544282",
    api_secret = "1oSO-d9c8he7Z7Lb9CjTNjPFMmk"
)
jwt = JWTManager(app)



from app.models import bookingModel,mitraModel,userModel, newsModel,chatbotModel, recomendationsModel
from app import routes