from flask import Flask
from flask import render_template, request, redirect
import sqlite3

app = Flask(__name__)
PROD_DB = "productDB.db"


class ContextManagerForDBConnect:
    """Контекстний менеджер для відкриття та закриття бази даних SQL"""

    def __init__(self, name_db):
        self._name_db = name_db

    def __enter__(self):
        self._connect = sqlite3.connect(self._name_db)
        return self._connect

    def __exit__(self, *args):
        self._connect.close()


def read_query_list(query="", *args):
    """Функція для зчитування даних з бази"""
    with ContextManagerForDBConnect(PROD_DB) as connection:
        cursor = connection.cursor()
        result = []
        try:
            cursor.execute(query, list(args))
            result = cursor.fetchall()
        except sqlite3.OperationalError as e:
            print("Error while reading data: " + query)
            print(e)
        finally:
            return result


def update_query(params, query=""):
    """Функція для запису даних в базу"""
    with ContextManagerForDBConnect(PROD_DB) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
        except sqlite3.OperationalError as e:
            print("Error while downloading data: " + query)
            print(e)


@app.route('/')
def start():
    categories = read_query_list("SELECT * FROM categories_table")
    return render_template('index.html', categories=categories)


@app.route('/category/<int:id_of_category>')
def show_products(id_of_category):
    products = read_query_list("SELECT * FROM products "
                               "WHERE id_of_category = ? "
                               "AND num_in_store + num_in_stock > 0",
                               id_of_category)
    category_name = read_query_list("SELECT name_category FROM categories_table "
                                    "WHERE id = ?",
                                    id_of_category)
    return render_template("products.html", products=products, category_name=category_name)


@app.route('/product/<int:product_id>')
def show_product(product_id):
    product = read_query_list("SELECT products.*, categories_table.name_category FROM products "
                              "INNER JOIN categories_table on products.id_of_category = categories_table.id "
                              "WHERE products.id = ?",
                              product_id)[0]
    return render_template("product.html", product=product)


@app.route('/admin')
def admin_main_page():
    return render_template("admin.html")


@app.route('/add_category', methods=['POST', 'GET'])
def add_category():
    if request.method == 'GET':
        return render_template("add_category.html")
    elif request.method == 'POST':
        params = [request.form['add_category_name']]
        update_query(params, "INSERT INTO categories_table (name_category) VALUES (?)")
        return redirect('/admin')


@app.route('/add_product', methods=['POST', 'GET'])
def new_product():
    if request.method == 'GET':
        categories = read_query_list("SELECT * FROM categories_table")
        return render_template("add_product.html", categories=categories)
    elif request.method == 'POST':
        params: dict = request.form.to_dict()
        print("dict? = ", params, type(params))

        # validation
        if not ('name' and 'model' and 'specification' and 'id_of_category' and 'num_in_store'
                and 'num_in_stock' and 'price') in params:
            return "Ошибка. Надо вводить все данные!"
        try:
            params['id_of_category'] = int(params['id_of_category'])
            params['num_in_store'] = int(params['num_in_store'])
            params['num_in_stock'] = int(params['num_in_stock'])
            params['price'] = int(params['price'])
        except ValueError:
            return "Ошибка. В четырех последних полях должны быть целочисленные значения"
        # inserting
        params_list = [param for param in params.values()]
        print("params_list =", params_list)
        update_query(params_list, """INSERT INTO products 
                                (name, model, specification, id_of_category, num_in_store, num_in_stock, price)
                                VALUES (?, ?, ?, ?, ?, ?, ?)""")

        return redirect('/admin')
    return "Unknown method"


if __name__ == '__main__':
    app.run(debug=True)
