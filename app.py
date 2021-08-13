import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import redirect
import re

# create class as part of flask requirements


class User(object):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


# create tables in sqlite
class CreateTable:

    def __init__(self):
        self.conn = sqlite3.connect('shoprite.db')
        self.cursor = self.conn.cursor()
        self.conn.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "username TEXT NOT NULL, "
                          "first_name TEXT NOT NULL,"
                          "last_name TEXT NOT NULL,"
                          "email TEXT NOT NULL,"
                          "password TEXT NOT NULL,"
                          "address TEXT NOT NULL)")
        print("users table created successfully")

        self.conn.execute("CREATE TABLE IF NOT EXISTS products(prod_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "name TEXT NOT NULL,"
                          "price TEXT NOT NULL,"
                          "description TEXT NOT NULL,"
                          "prod_type TEXT NOT NULL,"
                          "quantity TEXT NOT NULL)")
        print("product table created successfully")
        self.conn.close()


CreateTable()


def fetch_users():
    conn = sqlite3.connect('shoprite.db')
    cursor = conn.cursor()
    with sqlite3.connect('shoprite.db') as conn:
        cursor.execute("SELECT * FROM users")
        user = cursor.fetchall()

        new_data = []

        for data in user:
            new_data.append(User(data[0], data[1], data[5]))
    return new_data


users = fetch_users()


app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

# email tings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cody01101101@gmail.com'
app.config['MAIL_PASSWORD'] = 'Polonykop100'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# @app.route('/user-registration/', methods=["POST"])
# def user_registration():
#     response = {}
#
#     if request.method == "POST":
#
#         username = request.form['username']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         email = request.form['email']
#         password = request.form['password']
#         address = request.form['address']
#
#         with sqlite3.connect('shoprite.db') as conn:
#             cursor = conn.cursor()
#             cursor.execute("INSERT INTO users("
#                            "username,"
#                            "first_name,"
#                            "last_name,"
#                            "email,"
#                            "password,"
#                            "address) VALUES(?, ?, ?, ?, ?, ?)",
#                            (username, first_name, last_name, email, password, address))
#             conn.commit()
#             response["message"] = "success"
#             response["status_code"] = 201
#
#             msg = Message('Yo Bro', sender='cody01101101@gmail.com', recipients=[email])
#             msg.body = "Welcome " + first_name + ". You have Successfully registered."
#             mail.send(msg)
#
#         # return redirect("/emailsent/%s" % email)
#         return redirect('https://murmuring-everglades-76424.herokuapp.com/show-users/')
#     else:
#         return "Email not valid. Please enter a valid email address"


# a route with a function to register the users
@app.route('/user-registration/', methods=["POST"])
def user_registration():
    response = {}

    if request.method == "POST":
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'         # code to validate email entered
        #
        # # entry will only be accepted if email address and ID Number is valid
        # if re.search(regex, email):

        with sqlite3.connect('shoprite.db') as conn:

            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # code to validate email entered

            # entry will only be accepted if email address and ID Number is valid
            if re.search(regex, email):
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users("
                               "username,"
                               "first_name,"
                               "last_name,"
                               "email,"
                               "password,"
                               "address) VALUES(?, ?, ?, ?, ?, ?)",
                               (username, first_name, last_name, email, password, address))
                conn.commit()

            else:
                redirect('shorturl.at/ehrAQ')

        msg = Message('Welcome', sender='cody01101101@gmail.com', recipients=[email])
        msg.body = first_name + ' you have successfully registered.'
        mail.send(msg)

        response["message"] = "Success, Check Email"
        response["status_code"] = 201
        return redirect('https://murmuring-everglades-76424.herokuapp.com/show-users/')

        # else:
        #     response['message'] = "Invalid Email Address"
        #     return redirect('https://www.google.com/search?q=google&oq=GOOGLE&aqs=chrome.0.0i131i433i512l3j0i433i512l2j0i131i433i512l2j0i512.2563j0j15&sourceid=chrome&ie=UTF-8')


@app.route('/show-users/')
def show_users():
    response = {}

    with sqlite3.connect("shoprite.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")

        response["status_code"] = 200
        response["description"] = "Displaying all products successfully"
        response["data"] = cursor.fetchall()
    return jsonify(response)


@app.route('/delete-users/<int:user_id>')
def delete_users(user_id):
    response = {}
    with sqlite3.connect("shoprite.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=" + str(user_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Product successfully deleted"

    return response


@app.route('/prod-registration/', methods=["POST"])
def prod_registration():
    response = {}

    try:
        if request.method == "POST":

            name = request.json['name']
            price = request.json['price']
            description = request.json['description']
            prod_type = request.json['prod_type']
            quantity = request.json['quantity']

            with sqlite3.connect('shoprite.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO products("
                               "name,"
                               "price,"
                               "description,"
                               "prod_type,"
                               "quantity) VALUES(?, ?, ?, ?, ?)",
                               (name, price, description, prod_type, quantity))
                conn.commit()
                response["message"] = "success"
                response["status_code"] = 201
            return response

    except ConnectionError as e:
        return e
    except Exception as e:
        return e


@app.route('/show-products/')
def show_products():
    response = {}

    with sqlite3.connect("shoprite.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")

        response["status_code"] = 200
        response["description"] = "Displaying all products successfully"
        response["data"] = cursor.fetchall()
    return jsonify(response)


@app.route('/delete-products/<int:prod_id>')
def delete_products(prod_id):
    response = {}
    with sqlite3.connect("shoprite.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE prod_id=" + str(prod_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Product successfully deleted"

    return response


@app.route('/edit-prod/<int:prod_id>', methods=["PUT"])
def edit_products(prod_id):
    response = {}
    if request.method == "PUT":
        with sqlite3.connect("shoprite.db") as conn:
            incoming_data = dict(request.json)
            put_data = {}

            if incoming_data.get("price") is not None:
                put_data["price"] = incoming_data.get("price")
                with sqlite3.connect("shoprite.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE products SET price=? WHERE prod_id=?", (put_data["price"], prod_id))
                    conn.commit()
                    response['message'] = "Update was successful"
                    response['status_code'] = 200
                return response

            if incoming_data.get("quantity") is not None:
                put_data["quantity"] = incoming_data.get("quantity")
                with sqlite3.connect("shoprite.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE products SET quantity=? WHERE prod_id=?", (put_data["quantity"], prod_id))
                    conn.commit()
                    response['message'] = "Update was successful"
                    response['status_code'] = 200
                return response


if __name__ == '__main__':
    app.run()
