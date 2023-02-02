from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)

session = db.session()

cursor_user = session.execute("SELECT * from `offer`").cursor
mytable = prettytable.from_db_cursor(cursor_user)

if __name__ == '__main__':
    print(mytable)
