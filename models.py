from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


class Tutor(db.Model):
    __tablename__ = 'tutors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, default='/static/default_picture.png', nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.String, nullable=False)
    free = db.Column(db.String, nullable=False)
    booked = db.relationship('Booking', back_populates='tutor')


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    name= db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)



class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'), nullable=False)
    tutor = db.relationship('Tutor', back_populates='booked')
    day = db.Column(db.String(3), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    name= db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)


# db.create_all()
# DATABASE INITIATION SCRIPT
#
# import json
# with open('data.json', 'r', encoding='utf-8') as file:
#     data = file.read()
#
#
#
# data = json.loads(data)
# tutors = data['tutors']
# for tutor in tutors:
#     db.session.add(Tutor(name=tutor['name'], about=tutor['about'], rating=tutor['rating'],
#                       picture=tutor['picture'], price=tutor['price'], goals=' '.join(tutor['goals']),
#                       free=json.dumps(tutor['free'])))
# db.session.commit()



