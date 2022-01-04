from app import app
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from app.models.newsModel import db, News
import cloudinary.uploader

ma = Marshmallow(app)


class BeritaSchema(ma.Schema):
    class Meta:
        fields = ('id_news', 'image', 'title', 'content', 'mitra_id')


# init schema
beritaSchema = BeritaSchema()
beritasSchema = BeritaSchema(many=True)


def postNews():
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    title = request.form['title']
    content = request.form['content']
    mitra_id = request.form['mitra_id']

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
    newNews = News(mitra_id, title, image, content)
    db.session.add(newNews)
    db.session.commit()
    new = beritaSchema.dump(newNews)
    return jsonify({"msg": "Success post new berita", "status": 200, "data": new})


def getAllNews():
    allNews = News.query.all()
    result = beritasSchema.dump(allNews)
    return jsonify({"msg": "Success Get all berita", "status": 200, "data": result})


def getNewsById(id):
    news = News.query.get(id)
    beritaDetails = beritaSchema.dump(news)
    return jsonify({"msg": "Success get berita by id", "status": 200, "data": beritaDetails})


def updateNews(id):
    berita = News.query.get(id)
    title = request.form['title']
    content = request.form['content']
    mitra_id = request.form['mitra_id']
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    berita.image = image
    berita.title = title
    berita.content = content
    berita.mitra_id = mitra_id

    db.session.commit()
    beritaUpdate = beritaSchema.dump(berita)
    return jsonify({"msg": "Success update berita", "status": 200, "data": beritaUpdate})


def deleteNews(id):
    berita = News.query.get(id)
    db.session.delete(berita)
    db.session.commit()
    beritaDelete = beritaSchema.dump(berita)
    return jsonify({"msg": "Success Delete Berita", "status": 200, "data": beritaDelete})
