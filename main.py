from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import prettytable
import sqlite3
from create_update_tables import User, Order, Offer
import datetime


def get_route_all(name_table):
    """
    Запрос всех данных
    """
    result = []
    con = sqlite3.connect("lesson16.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT * FROM `{name_table}`"""
    cur.execute(sqlite_query)
    result = cur.fetchall()
    con.close()

    return result


def get_route_by_id(table_name, name_id):
    """
    Запрос данных из одной строки
    """
    result = []
    con = sqlite3.connect("lesson16.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT *
                        FROM `{table_name}`
                        WHERE id 
                        LIKE {int(name_id)}
                        """
    cur.execute(sqlite_query)
    cur_f = cur.fetchall()
    con.close()

    return cur_f


def del_row(name_table, name_id):
    """
    Запрос на удаление строки
    """
    with sqlite3.connect("lesson16.db") as con:
        cur = con.cursor()
        sqlite_query = f"""DELETE FROM `{name_table}`
        WHERE id 
        LIKE {int(name_id)}
        """
        cur.execute(sqlite_query)
        return f"{name_id} удален!"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db: SQLAlchemy = SQLAlchemy(app)

@app.errorhandler(400)
def error_404(error):
    """
    Представление для ошибки "Неверный запрос"
    """
    return "<h1>Неверный запрос!</h1>", 400


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


@app.route("/users", methods=["GET", "POST"])
def get_users():
    """
    Вывод всех пользователей и раздела добавить пользователя
    """
    if request.method == "GET":
        return render_template("users_main.html", text_main=get_route_all("user"))
    elif request.method == "POST":
        list_rows = request.values["list_rows"].strip().split("\r\n")
        user_class = User(
            first_name=list_rows[0],
            last_name=list_rows[1],
            age=list_rows[2],
            email=list_rows[3],
            role=list_rows[4],
            phone=list_rows[5])

        db.session.add(user_class)
        db.session.commit()

        return render_template("users_main.html", text_main=get_route_all("user"))


@app.route("/users/<int:user_id>", methods=["PUT", "DELETE"])
def update_user_page(user_id):
    """
    Обновление и удаление пользователей в необходимых строках по одной за раз.
    """
    user_upd = request.args.get("key")
    if request.method == "PUT":
        with sqlite3.connect("lesson16.db") as con:
            cur = con.cursor()
            sqlite_query = f"""UPDATE user
            SET first_name = '{user_upd[0]}',
            last_name = '{user_upd[1]}',
            age = '{user_upd[2]}',
            email = '{user_upd[3]}',
            role = '{user_upd[4]}',
            phone = '{user_upd[5]}'
            WHERE id
            LIKE {int(user_id)}
            """
            cur.execute(sqlite_query)

    elif request.method == "DELETE":
        return del_row("user", user_id)

    return jsonify(get_route_by_id("user", user_id))


@app.route("/orders", methods=["GET", "POST"])
def get_all_orders():
    """
    Вывод всех заказов и раздела добавить пользователя
    """
    if request.method == "GET":
        return render_template("orders_main.html", text_main=get_route_all("order"))
    elif request.method == "POST":
        list_rows = request.values["list_rows"].strip().split("\r\n")
        start_date_list = list_rows[2].split("-")
        end_date_list = list_rows[3].split("-")
        user_class = Order(
        name=list_rows[0],
        description=list_rows[1],
        start_date=datetime.date(int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2])),
        end_date=datetime.date(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2])),
        address=list_rows[4],
        price=list_rows[5],
        customer_id = list_rows[6],
        executor_id = list_rows[7])
        db.session.add(user_class)
        db.session.commit()

        return render_template("orders_main.html", text_main=get_route_all("order"))


@app.route("/orders/<order_id>", methods=["PUT", "DELETE"])
def update_order_page(order_id):
    """
    Обновление и удаление заказов в необходимых строках по одной за раз.
    """
    order_upd = request.args.get("key")

    if request.method == "PUT":
        with sqlite3.connect("lesson16.db") as con:
            cur = con.cursor()
            sqlite_query = f"""UPDATE "order"
            SET name = '{order_upd[0]}',
            description = '{order_upd[1]}',
            start_date = '{order_upd[2]}',
            end_date = '{order_upd[3]}',
            address = '{order_upd[4]}',
            price = '{order_upd[5]}',
            customer_id = '{order_upd[6]}',
            executor_id = '{order_upd[7]}'
            WHERE id
            LIKE {int(order_id)}
            """
            cur.execute(sqlite_query)

    elif request.method == "DELETE":
        return del_row("order", order_id)

    return jsonify(get_route_by_id("order", order_id))


@app.route("/offers", methods=["GET", "POST"])
def get_all_offers():
    """
    Вывод всех номеров заказов и номеров исполнителей
    """
    if request.method == "GET":
        return render_template("offers_main.html", text_main=get_route_all("offer"))
    elif request.method == "POST":
        list_rows = request.values["list_rows"].strip().split("\r\n")
        user_class = Offer(
        order_id=list_rows[0],
        executor_id=list_rows[1])

        db.session.add(user_class)
        db.session.commit()

        return render_template("offers_main.html", text_main=get_route_all("offer"))


@app.route("/offers/<offer_id>", methods=["PUT", "DELETE"])
def update_offer_page(offer_id):
    """
    Обновление и удаление номеров заказов и номеров исполнителей в необходимых строках по одной за раз.
    """
    offer_upd = request.args.get("key")

    if request.method == "PUT":
        with sqlite3.connect("lesson16.db") as con:
            cur = con.cursor()
            sqlite_query = f"""UPDATE offer
            SET order_id = '{offer_upd[0]}',
            executor_id = '{offer_upd[1]}'
            WHERE id
            LIKE {int(offer_id)}
            """
            cur.execute(sqlite_query)

    elif request.method == "DELETE":
        return del_row("offer", offer_id)

    return jsonify(get_route_by_id("offer", offer_id))


if __name__ == '__main__':
    app.run()
