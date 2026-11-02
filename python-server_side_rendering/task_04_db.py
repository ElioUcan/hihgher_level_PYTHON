import csv
import json
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


def create_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    try:
        cursor.execute('''
            INSERT INTO Products (id, name, category, price)
            VALUES
            (1, 'Laptop', 'Electronics', 799.99),
            (2, 'Coffee Mug', 'Home Goods', 15.99)
        ''')
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


def read_json_products():
    with open('products.json', 'r') as file:
        return json.load(file)


def read_csv_products():
    with open('products.csv', 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)


def read_sql_products():
    try:
        conn = sqlite3.connect('products.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, category, price FROM Products')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except sqlite3.Error:
        return None


read_sqlite_products = read_sql_products
read_sqlite = read_sql_products


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/items')
def items():
    try:
        with open('items.json', 'r') as file:
            data = json.load(file)
            items_list = data.get('items', [])
    except (FileNotFoundError, json.JSONDecodeError):
        items_list = []
    return render_template('items.html', items=items_list)


@app.route('/products')
def products():
    source = request.args.get('source')
    product_id = request.args.get('id')

    if source == 'json':
        products_list = read_json_products()
    elif source == 'csv':
        products_list = read_csv_products()
    elif source == 'sql':
        try:
            products_list = read_sql_products()
        except sqlite3.Error:
            products_list = None
        if products_list is None:
            return render_template('product_display.html', error='Database error')
    else:
        return render_template('product_display.html', error='Wrong source')

    if product_id:
        products_list = [
            p for p in products_list
            if str(p.get('id')) == str(product_id)
        ]
        if not products_list:
            return render_template('product_display.html', error='Product not found')

    return render_template('product_display.html', products=products_list)


if __name__ == '__main__':
    create_database()
    app.run(debug=True, port=5000)
