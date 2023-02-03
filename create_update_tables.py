from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable
import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)

def get_json_file(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    phone = db.Column(db.Text)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.Text)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.relationship("Order")
    executor = db.relationship("User")


db.create_all()
users = get_json_file("users.json")
try:
    for i in users:
        user_class = User(
        id=int(i['id']),
        first_name=i['first_name'],
        last_name=i['last_name'],
        age=int(i['age']),
        email=i['email'],
        role=i['role'],
        phone=i['phone'])

        with db.session.begin():
            db.session.add(user_class)
        db.session.commit()
except:
    print("Таблица уже создана, или ошибка!")

orders = get_json_file("orders.json")
try:
    for i in orders:
        start_date_list = i['start_date'].split("/")
        end_date_list = i['end_date'].split("/")
        order_class = Order(
            id=int(i['id']),
            name=i['name'],
            description=i['description'],
            start_date=datetime.date(int(start_date_list[2]), int(start_date_list[0]), int(start_date_list[1])),
            end_date=datetime.date(int(end_date_list[2]), int(end_date_list[0]), int(end_date_list[1])),
            address=" ".join(i['address'].split("\n")),
            price=int(i['price']),
            customer_id=int(i['customer_id']),
            executor_id=int(i['executor_id']))

        with db.session.begin():
            db.session.add(order_class)
        db.session.commit()
except:
    print("Таблица уже создана, или ошибка!")

offers = get_json_file("offers.json")
try:
    for i in offers:
        offer_class = Offer(
            id=i["id"],
            order_id=i["order_id"],
            executor_id=i["executor_id"])

        with db.session.begin():
            db.session.add(offer_class)

        db.session.commit()
except:
    print("Таблица уже создана, или ошибка!")

