import sqlite3

from create_update_tables import User
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

def get_route_all(name_table):
    con = sqlite3.connect("lesson16.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT * FROM `{name_table}`"""
    cur.execute(sqlite_query)
    result = cur.fetchall()
    con.close()

    return result


def get_route_by_id(table_name, name_id):

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


# @app.route("/users")
# def get_all_users():
#
#     return render_template("users_main.html", text_main = get_route_all("user"))

@app.route("/users", methods=["GET", "POST"])
def manipulation_user():
    try:
        try:
            del_user = request.values["del_user"]
            if del_user > 0:
                user_del = User.query.get(int(del_user))
                db.session.delete(user_del)
                db.session.commit()
                return render_template("users_main.html", text_main=get_route_all("user"))
        except:
            return render_template("users_main.html", text_main=get_route_all("user"))
    except:
        list_rows = request.values["list_rows"].strip().split("\r\n")
        user_class = User(
            first_name=list_rows[0],
            last_name=list_rows[1],
            age=list_rows[2],
            email=list_rows[3],
            role=list_rows[4],
            phone=list_rows[5])
        with db.session.begin():
            db.session.add(user_class)
        db.session.commit()
        return render_template("users_main.html", text_main=get_route_all("user"))


@app.route("/users/<user_id>", methods=["GET"])#, "PUT"])
def get_user_by_id(user_id):
    # response_put = request.put(f"http://127.0.0.1:5000/users/{user_id}",
    #                            jsonify(get_route_by_id("user", user_id)))
    # try:
    #
    #     response_put = request.values["upd_user"].strip().split("\r\n")
    #     upd_user_class = User(
    #         first_name=response_put[0],
    #         last_name=response_put[1],
    #         age=response_put[2],
    #         email=response_put[3],
    #         role=response_put[4],
    #         phone=response_put[5])
    #     with db.session.begin():
    #         db.session.add(upd_user_class)
    #     db.session.commit()
    #     return render_template("upd_user.html",
    #                            user=get_route_by_id("user", user_id),
    #                            user_id=user_id)
    # except:
    return render_template("upd_user.html",
                           user=get_route_by_id("user", user_id),
                           user_id=user_id)


@app.route("/orders")
def get_all_orders():

    return get_route_all('order')


@app.route("/orders/<order_id>")
def get_order_by_id(order_id):

    return get_route_by_id("order", order_id)


@app.route("/offers")
def get_all_offers():

    return get_route_all("offer")


@app.route("/offers/<offer_id>")
def get_offer_by_id(offer_id):

    return get_route_by_id("offer", offer_id)


if __name__ == '__main__':
    app.run()
