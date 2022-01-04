from app import app
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from app.models.modelHair import db, Hair
import cloudinary.uploader


ma = Marshmallow(app)


class HairSchema(ma.Schema):
    class Meta:
        fields = ('id_model', 'image', 'nama_model')


# init schema
hairSchema = HairSchema()
hairsSchema = HairSchema(many=True)


def postHairModel():
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    nama_model = request.form['nama_model']

    if 'image' not in request.files:
        resp = jsonify({"msg": "No body image attached in request"})
        resp.status_code = 501
        return resp
    fileImage = request.files['image']
    if fileImage.filename == '':
        resp = jsonify({'msg': "No file fileImage selected"})
        resp.status_code = 505
        return resp

    print(fileImage.filename)
    error = {}

    if fileImage and allowed_file(fileImage.filename):
        upload_result = cloudinary.uploader.upload(fileImage)
        print(upload_result["secure_url"])
        image = upload_result["secure_url"]
    else:
        error[fileImage.filename] = 'File type is not allowed'
    newHairModel = Hair(image, nama_model)
    db.session.add(newHairModel)
    db.session.commit()
    new = hairSchema.dump(newHairModel)
    return jsonify({"msg": "Success post new hair model", "status": 200, "data": new})


def getAllHairModel():
    allHairModel = Hair.query.all()
    result = hairsSchema.dump(allHairModel)
    return jsonify({"msg": "Success Get all Hair Model", "status": 200, "data": result})
