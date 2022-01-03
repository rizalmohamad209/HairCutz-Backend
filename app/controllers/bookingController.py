from datetime import date, datetime

from sqlalchemy.sql.expression import and_
from app import app
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from app.models.bookingModel import db, Booking

ma = Marshmallow(app)


class BookingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'no_urut', 'id_mitra', 'id_user', 'date', 'status')


# init schema
bookingSchema = BookingSchema()
bookingsSchema = BookingSchema(many=True)


def postBooking(decodeToken):
    id_mitra = request.form['id_mitra']
    status = request.form['status']
    id_user = decodeToken.get('id_user')
    tgl = date.today()

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
    status = request.form['status']
    booking = Booking.query.get(id)
    booking.status = status
    db.session.commit()
    result = bookingSchema.dump(booking)
    return jsonify({"msg": "Success update status", "status": 200, "data": result})


def getBookingByMitra(id):
    book = Booking.query.filter(Booking.id_mitra == id).all()
    result = bookingsSchema.dump(book)
    return jsonify({"msg": "Success get booking by mitra", "status": 200, "data": result})


def getHistoryBooking(decodeToken):
    book = Booking.query.filter(
        Booking.id_user == decodeToken.get('id_user')).all()
    result = bookingsSchema.dump(book)
    return jsonify({"msg": "Success get booking by user", "status": 200, "data": result})
