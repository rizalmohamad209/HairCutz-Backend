from datetime import date, datetime

from sqlalchemy.sql.expression import and_
from app import app
from flask import request, jsonify
from app.models.mitraModel import Mitra
from app.models.userModel import Users
from flask_marshmallow import Marshmallow
from app.models.bookingModel import db, Booking

ma = Marshmallow(app)


class BookingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'no_urut', 'id_mitra', 'id_user',
                  'date', 'status', 'nama_user', 'nama_mitra', 'alamat_mitra')


# init schema
bookingSchema = BookingSchema()
bookingsSchema = BookingSchema(many=True)


def postBooking(decodeToken):
    id_mitra = request.form['id_mitra']
    status = request.form['status']
    id_user = decodeToken.get('id_user')
    tgl = date.today()
    print(tgl)

    allBerita = Booking.query.filter(
        and_(Booking.id_mitra == id_mitra, Booking.date == tgl
             )).all()
    no_urut = len(allBerita) + 1
    newBooking = Booking(no_urut, id_mitra, id_user, tgl, status)
    db.session.add(newBooking)
    db.session.commit()
    new = bookingSchema.dump(newBooking)
    return jsonify({"msg": "Success post new berita", "status": 200, "data": new})


def updateBookingStatus(id):

    booking = Booking.query.get(id)
    status = request.form['status']
    booking.status = status
    db.session.commit()
    result = bookingSchema.dump(booking)
    return jsonify({"msg": "Success update status", "status": 200, "data": result})


def getBookingByMitra(token):
    print(token)
    # book = Booking.query.join(Users, Booking.id_user == Users.id_user).filter(
    #     Booking.id_mitra == token.get('id_mitra')).all()
    book = db.session.query(Booking.date, Booking.status, Booking.no_urut, Booking.id, Booking.id_mitra, Users.nama_user, Mitra.nama_mitra, Mitra.alamat_mitra).join(
        Users, Users.id_user == Booking.id_user).join(Mitra, Mitra.id_mitra == Booking.id_mitra).filter(
            Booking.id_mitra == token.get('id_mitra')).all()
    # print(book)
    result = bookingsSchema.dump(book)
    return jsonify({"msg": "Success get booking by mitra", "status": 200, "data": result})


def getHistoryBooking(decodeToken):
    book = db.session.query(Booking.date, Booking.no_urut, Booking.id, Booking.id_mitra, Users.nama_user, Mitra.nama_mitra, Mitra.alamat_mitra).join(
        Users, Users.id_user == Booking.id_user).join(Mitra, Mitra.id_mitra == Booking.id_mitra).filter(
        Booking.id_user == decodeToken.get('id_user')).all()
    result = bookingsSchema.dump(book)
    return jsonify({"msg": "Success get booking by user", "status": 200, "data": result})


def getBookingByMitraForUser(id):

    # book = Booking.query.join(Users, Booking.id_user == Users.id_user).filter(
    #     Booking.id_mitra == token.get('id_mitra')).all()
    book = db.session.query(Booking.date, Booking.status, Booking.id_user, Booking.no_urut, Booking.id, Booking.id_mitra, Users.nama_user, Mitra.nama_mitra, Mitra.alamat_mitra).join(
        Users, Users.id_user == Booking.id_user).join(Mitra, Mitra.id_mitra == Booking.id_mitra).filter(
            Booking.id_mitra == id).all()
    # print(book)
    result = bookingsSchema.dump(book)
    return jsonify({"msg": "Success get booking by mitra", "status": 200, "data": result})
