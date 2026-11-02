from flask import Flask, render_template, request
import csv
import json

app = Flask(__name__)


def read_json_products():
    with open('products.json', 'r') as file:
        return json.load(file)


def read_csv_products():
    with open('products.csv', 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)


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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
