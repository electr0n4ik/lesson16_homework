from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import prettytable
from create_update_tables import User
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db: SQLAlchemy = SQLAlchemy(app)

@app.route("/users")
def get_all_users():
    import sqlite3

    result = []
    con = sqlite3.connect("lesson16.db")
    cur = con.cursor()
    sqlite_query = ("""SELECT *
                    FROM user""")
    cur.execute(sqlite_query)
    users = cur.fetchall()
    con.close()

    return jsonify(users)

# session = db.session()
# cursor_user = session.execute("SELECT * from `user`").cursor
# mytable = prettytable.from_db_cursor(cursor_user)
#
# if __name__ == '__main__':
#     print(mytable)

if __name__ == '__main__':
    app.run()
