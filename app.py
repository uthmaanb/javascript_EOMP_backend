import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import redirect
import re


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


# class for Database functions
class Database(object):
    # function to connect to Database and crete cursor
    def __init__(self):
        self.conn = sqlite3.connect('shoprite.db')
        self.cursor = self.conn.cursor()

    # function for INSERT AND UPDATE query
    def insert(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()

    # function to fetch data for SELECT query
    def fetch(self):
        return self.cursor.fetchall()

    # function for executing SELECT query
    def select(self, query):
        self.cursor.execute(query)
        self.conn.commit()


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
app.config['MAIL_PASSWORD'] = 'agdpojipysvvqmoa'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


# a route with a function to register the users
@app.route('/user-registration/', methods=["POST"])
def user_registration():
    response = {}
    db = Database()

    if request.method == "POST":
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email):

            query = ("INSERT INTO users("
                     "username,"
                     "first_name,"
                     "last_name, "
                     "email,"
                     "password,"
                     "address) VALUES(?, ?, ?, ?, ?, ?)")
            values = username, first_name, last_name, email, password, address
            db.insert(query, values)

            msg = Message('Welcome To MyPOS', sender='cody01101101@gmail.com', recipients=[email])
            msg.body = "Thank You for registering with us " + first_name
            mail.send(msg)

            response["message"] = "Success, Check Email"
            response["status_code"] = 201
            return redirect('https://distracted-meninsky-b86e1a.netlify.app/index.html')

        else:
            response['message'] = "aaakakakakaa"
            return redirect('https://youtu.be/cMTAUr3Nm6I?t=31')

        # return redirect


@app.route('/login/', methods=['POST'])
def login():
    response = {}
    # db = Database()

    # query = "SELECT * FROM  users"
    # db.select(query)
    # data = db.fetch()

    # for i in data:
    #     print(i)
    #     if request.form['username'] == i[1] and request.form['password'] == i[5]:
    #         response['message'] = "Login successful"
    #         response['status_code'] = 200
    #         # print(data)
    #         # and redirect('https://www.youtube.com/watch?v=o2weDmBXfik&ab_channel=MarkAngelComedy')
    #     else:
    #         response['message'] = 'unsuccessful'
    #         # redirect('https://youtu.be/cMTAUr3Nm6I?t=31')
    #     return response

    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        conn = sqlite3.connect("shoprite.db")
        c = conn.cursor()
        statement = (f"SELECT * FROM users WHERE username='{username}' and password ="
                     f"'{password}'")
        c.execute(statement)
        if not c.fetchone():
            response['message'] = "failed"
            response["status_code"] = 401
            return response
        else:
            response['message'] = "welcome admin user"
            response["status_code"] = 201
            return response
    else:
        return "wrong method"


# end-point to view all products
@app.route("/show-users/")
def show_users():
    response = {}
    db = Database()

    query = "SELECT * FROM  users"
    db.select(query)

    response['status_code'] = 200
    response['data'] = db.fetch()

    return jsonify(response)


# delete user from table
@app.route("/delete-users/<int:user_id>")
def delete_users(user_id):

    response = {}
    db = Database()

    query = "DELETE FROM users WHERE user_id=" + str(user_id)
    db.select(query)

    # check if the id exists
    if not id:
        return "user does not exist"

    else:
        response['status_code'] = 200
        response['message'] = "item deleted successfully."
        return response


@app.route('/prod-registration/', methods=["POST"])
def prod_registration():
    response = {}
    db = Database()

    try:
        if request.method == "POST":

            name = request.form['name']
            price = request.form['price']
            description = request.form['description']
            prod_type = request.form['prod_type']
            quantity = request.form['quantity']

            try:
                query = ("INSERT INTO products("
                         "name,"
                         "price,"
                         "description,"
                         "prod_type,"
                         "quantity) VALUES(?, ?, ?, ?, ?)")
                values = name, price, description, prod_type, quantity
                db.insert(query, values)
                response["message"] = "success"
                response["status_code"] = 201
                return jsonify(response)

            except ValueError:
                return {
                    "error": "failed to insert into DB"
                }

    except ConnectionError as e:
        return e
    except Exception as e:
        return e


# end-point to view all products
@app.route("/show-products/")
def show_products():
    response = {}
    db = Database()

    query = "SELECT * FROM  products"
    db.select(query)

    response['status_code'] = 200
    response['data'] = db.fetch()

    return jsonify(response)


# delete products from table
@app.route("/delete-products/<int:prod_id>")
def delete_products(prod_id):

    response = {}
    db = Database()

    query = "DELETE FROM products WHERE prod_id=" + str(prod_id)
    db.select(query)

    # check if the id exists
    if not id:
        return "product does not exist"

    else:
        response['status_code'] = 200
        response['message'] = "item deleted successfully."
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
