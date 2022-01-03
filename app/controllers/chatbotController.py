from sqlalchemy.sql.elements import and_, or_
from app import app
import random
from tensorflow.keras.models import load_model
import pickle
from flask import request, jsonify
import numpy as np
import json
import nltk
from nltk.stem import WordNetLemmatizer
from flask_marshmallow import Marshmallow
from app.models.chatbotModel import db, Chat


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

ma = Marshmallow(app)


class ChatSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sender', 'receiver', 'message')


# init schema
chatSchema = ChatSchema()
chatsSchema = ChatSchema(many=True)

model = load_model('model/chatbot_model.h5')
intents = json.loads(open('model/dataset.json').read())
words = pickle.load(open('model/words.pkl', 'rb'))
classes = pickle.load(open('model/classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['pengetahuan']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


def chatbot(payload):
    print(payload)
    receiver = 9
    message = request.form['chat']
    newchat = Chat(payload.get('id_user'), receiver, message)
    db.session.add(newchat)
    db.session.commit()
    res = chatbot_response(message)

    chatbot = Chat(receiver, payload.get('id_user'), res)
    db.session.add(chatbot)
    db.session.commit()
    return jsonify({
        'status': 200,
        'answers': message,
        'msg': "Success get predict face shape",
        'response': res
    })


def getChat(payload):
    allChat = Chat.query.filter(or_(Chat.sender == payload.get(
        'id_user'), Chat.receiver == payload.get('id_user'))).all()
    result = chatsSchema.dump(allChat)
    return jsonify({"msg": "Success Get all berita", "status": 200, "data": result})
