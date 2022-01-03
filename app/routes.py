from app import app
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import bookingController, mitraController, userController, chatbotController, recomendationsController


@app.route('/user', methods=['GET', 'PUT'])
@jwt_required()
def userDetails():
    current_user = get_jwt_identity()
    if(request.method == 'GET'):
        return userController.getDetailUser(current_user)
    if(request.method == 'PUT'):
        return userController.updateUser(current_user)


@app.route('/signup', methods=['POST'])
def signUp():
    return userController.signUp()


@app.route('/signin', methods=['POST'])
def signIn():
    return userController.signIn()


@app.route('/mitra', methods=['POST', 'GET', 'PUT'])
@jwt_required()
def mitra():
    payload_user = get_jwt_identity()
    if(request.method == 'POST'):
        return mitraController.postMitra()
    elif(request.method == 'PUT'):
        return mitraController.updateMitra(payload_user)
    elif (request.method == 'GET'):
        return mitraController.getAllMitra()


@app.route('/mitra/<id>', methods=['GET', 'DELETE'])
@jwt_required()
def mitraById(id):
    if(request.method == 'GET'):
        return mitraController.getMitraById(id)
    elif (request.method == 'DELETE'):
        return mitraController.deleteMitra(id)


@app.route('/bookUser', methods=['POST', 'GET'])
@jwt_required()
def booking():
    payload_user = get_jwt_identity()
    if(request.method == 'POST'):
        return bookingController.postBooking(payload_user)
    elif(request.method == 'GET'):
        return bookingController.getHistoryBooking(payload_user)


@app.route('/bookMitra/<id>', methods=['PUT', 'GET'])
@jwt_required()
def updateStatus(id):
    if(request.method == 'PUT'):
        return bookingController.updateBookingStatus(id)
    elif(request.method == 'GET'):
        return bookingController.getBookingByMitra(id)


@app.route('/predict', methods=['POST'])
def prediksi():
    return recomendationsController.predict()


@app.route('/recomendations', methods=['POST'])
def recomendations():
    return recomendationsController.postRecomendations()


# test

@app.route('/chatbot', methods=['POST', 'GET'])
@jwt_required()
def chatsbot():
    payload = get_jwt_identity()
    if(request.method == 'POST'):
        return chatbotController.chatbot(payload)
    elif(request.method == 'GET'):
        return chatbotController.getChat(payload)