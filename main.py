from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import prettytable
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db: SQLAlchemy = SQLAlchemy(app)

@app.errorhandler(404)
def error_404(error):
    """
    Представление для ошибки "Страница не найдена"
    """
    return "<h1>Страница не найдена</h1>", 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Представление для ошибки "Внутренняя ошибка сервера"
    """
    return "<h1>Сервер не отвечает</h1>", 500


@app.route("/users")
def get_all_users():

    result = []
    con = sqlite3.connect("lesson16.db")
    cur = con.cursor()
    sqlite_query = ("""SELECT *
                    FROM user""")
    cur.execute(sqlite_query)
    users = cur.fetchall()
    con.close()

    return jsonify(users)


@app.route("/users/<user_id>")
def get_user_by_id(user_id):

    result = []
    con = sqlite3.connect("lesson16.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT *
                    FROM user
                    WHERE id 
                    LIKE {int(user_id)}
                    """
    cur.execute(sqlite_query)
    user = cur.fetchall()
    con.close()

    return jsonify(user)


if __name__ == '__main__':
    app.run()
