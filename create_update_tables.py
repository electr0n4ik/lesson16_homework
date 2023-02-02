from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable
from users import users
from orders import orders
from offers import offers
import datetime

def get_date(str):
    list_str = str.split("/")
    join_str = "-".join(list_str)
    # int_to_str = int(join_str)
    date_ = datetime.date(join_str)
    return date_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)

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
    print("id повторяются, поэтому таблица User не наполняется")


# try:
for i in orders:
    order_class = Order(
        id=int(i['id']),
        name=i['name'],
        description=i['description'],
        start_date=get_date(i['start_date']),
        end_date=i['end_date'],
        address=i['address'],
        price=int(i['price']),
        customer_id=int(i['customer_id']),
        executor_id=int(i['executor_id']))

    with db.session.begin():
        db.session.add(order_class)
    db.session.commit()
# except:
#     print("id повторяются, поэтому таблица Order не наполняется")


try:
    for i in offers:
        offer_class = Offer(
            id=i["id"],
            order_id=i["order_id"],
            executor_id=["executor_id"])

        with db.session.begin():
            db.session.add(offer_class)

        db.session.commit()
except:
    print("id повторяются, поэтому таблица Offer не наполняется")

