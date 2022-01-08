from app import app
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from app.models.mitraModel import db, Mitra
import cloudinary.uploader

ma = Marshmallow(app)


class MitraSchema(ma.Schema):
    class Meta:
        fields = ('id_mitra', 'nama_mitra', 'alamat_mitra', 'image',
                  'lat', 'long', 'jmlh_tukangCukur', 'user_id')


# init schema
mitraSchema = MitraSchema()
mitrasSchema = MitraSchema(many=True)


def postMitra():
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    nama_mitra = request.form['nama_mitra']
    alamat_mitra = request.form['alamat_mitra']
    lat = request.form['lat']
    long = request.form['long']
    user_id = request.form['user_id']
    jmlh_tukangCukur = request.form['jmlh_tukangCukur']

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

    newMitra = Mitra(nama_mitra, lat, long, alamat_mitra, image,
                     jmlh_tukangCukur, user_id)
    db.session.add(newMitra)
    db.session.commit()
    new = mitraSchema.dump(newMitra)
    return jsonify({"msg": "Success Get all mitra", "status": 200, "data": new})


def updateMitra(decodeToken):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    decode = decodeToken
    print(decode.get('id_user'))

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    mitra = Mitra.query.filter(Mitra.user_id == decode.get('id_user'))
    print(mitra)
    nama_mitra = request.form['nama_mitra']
    alamat_mitra = request.form['alamat_mitra']
    lat = request.form['lat']
    long = request.form['long']
    jmlh_tukangCukur = request.form['jmlh_tukangCukur']

    if 'image' not in request.files:
        resp = jsonify({"msg": "No body image attached in request"})
        resp.status_code = 501
        return resp
    fileImage = request.files['image']
    print(fileImage.filename)
    if fileImage.filename == '':
        resp = jsonify({'msg': "No file fileImage selected"})
        resp.status_code = 505
        return resp

    error = {}

    if fileImage and allowed_file(fileImage.filename):
        upload_result = cloudinary.uploader.upload(fileImage)
        print(upload_result["secure_url"])
        image = upload_result["secure_url"]
    else:
        error[fileImage.filename] = 'File type is not allowed'

    mitra.nama_mitra = nama_mitra
    mitra.alamat_mitra = alamat_mitra
    mitra.image = image
    mitra.jmlh_tukangCukur = jmlh_tukangCukur
    mitra.lat = lat
    mitra.long = long

    db.session.commit()
    mitraUpdate = mitraSchema.dump(mitra)
    return jsonify({"msg": "Success update mitra", "status": 200, "data": mitraUpdate})


def getAllMitra():
    mitra = Mitra.query.all()
    result = mitrasSchema.dump(mitra)
    return jsonify({"msg": "Success get all mitra", "status": 200, "data": result})


def getMitraById(id):
    mitra = Mitra.query.get(id)
    mitraDetails = mitraSchema.dump(mitra)
    return jsonify({"msg": "Success get mitra by id", "status": 200, "data": mitraDetails})


def getMitraDetails(decode):
    print(decode.get("id_mitra"))
    mitra = Mitra.query.get(decode.get("id_mitra"))
    print(mitra)
    mitraDetails = mitraSchema.dump(mitra)
    return jsonify({"msg": "Success get mitra by id", "status": 200, "data": mitraDetails})


def deleteMitra(id):
    mitra = Mitra.query.get(id)
    db.session.delete(mitra)
    db.session.commit()
    mitraDelete = mitraSchema.dump(mitra)
    return jsonify({"msg": "Success Delete mitra", "status": 200, "data": mitraDelete})
