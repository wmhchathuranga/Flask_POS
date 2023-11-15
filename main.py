from flask import Flask, jsonify, request
from db_connector.mysql_connector import mysql_connection
from dao.products_dao import *
from dao.quentity_dao import *
from dao.order_dao import *
from dao.cashier_dao import *

app = Flask(__name__)
connection = mysql_connection()


@app.route('/api/all_products', methods=['GET'])
def get_products():
    products = get_all_products(connection)
    response = jsonify(products)
    return response


@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_one_product(product_id):
    product = get_product(connection, product_id)
    if product:
        response = jsonify(product)
        return response
    else:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/api/add_product', methods=['POST'])
def add_new_product():
    product = request.json
    product_id = add_product(connection, product)
    return jsonify({'product_id': product_id}), 201


# update product route
@app.route('/api/update_product', methods=['PUT'])
def update_product_route():
    product = request.json
    row_count = update_product(connection, product)
    if row_count > 0:
        return jsonify({'message': 'Product updated successfully'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/api/delete_product/<int:product_id>', methods=['PUT'])
def soft_delete_product_route(product_id):
    product = get_product(connection, product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    row_count = soft_delete_product(connection, product_id)
    if row_count > 0:
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/api/all_quantity', methods=['GET'])
def get_all_quantities_route():
    quantities = get_all_quantities(connection)
    return jsonify(quantities), 200


@app.route('/api/quantity/<int:quantity_id>', methods=['GET'])
def get_quantity_route(quantity_id):
    quantity = get_quantity(connection, quantity_id)
    if quantity:
        return jsonify(quantity), 200
    else:
        return jsonify({'message': 'Quantity not found'}), 404


@app.route('/api/add_quantity', methods=['POST'])
def add_quantity_route():
    quantity = request.json
    quantity_id = add_quantity(connection, quantity)
    return jsonify({'quantity_id': quantity_id}), 201


@app.route('/api/update_quantity', methods=['PUT'])
def update_quantity_route():
    quantity = request.json
    row_count = update_quantity(connection, quantity)
    if row_count > 0:
        return jsonify({'message': 'Quantity updated successfully'}), 200
    else:
        return jsonify({'message': 'Quantity not found'}), 404


@app.route('/api/delete_quantity/<int:quantity_id>', methods=['PUT'])
def delete_quantity_route(quantity_id):
    quantity = get_quantity(connection, quantity_id)
    if not quantity:
        return jsonify({'message': 'Quantity not found'}), 404
    row_count = soft_delete_quantity(connection, quantity_id)
    if row_count > 0:
        return jsonify({'message': 'Quantity deleted successfully'}), 200
    else:
        return jsonify({'message': 'Quantity not found'}), 404


@app.route('/api/orders', methods=['GET'])
def get_all_orders_route():
    orders = get_all_orders(connection)
    return jsonify(orders), 200


@app.route('/api/order/<int:order_id>', methods=['GET'])
def get_order_route(order_id):
    order = get_order(connection, order_id)
    if order:
        return jsonify(order), 200
    else:
        return jsonify({'message': 'Order not found'}), 404


@app.route('/api/order', methods=['POST'])
def create_order_route():
    order = request.json
    order_id = create_order(connection, order)
    return jsonify({'order_id': order_id}), 201


@app.route('/api/cashier', methods=['POST'])
def create_cashier_route():
    cashier = request.json
    cashier_id = create_cashier(connection, cashier)
    return jsonify({'cashier_id': cashier_id}), 201


@app.route('/api/cashiers', methods=['GET'])
def get_all_cashiers_route():
    cashiers = get_all_cashiers(connection)
    return jsonify(cashiers), 200


@app.route('/api/cashier/<int:cashier_id>', methods=['GET'])
def get_cashier_route(cashier_id):
    cashier = get_cashier(connection, cashier_id)
    if cashier:
        return jsonify(cashier), 200
    else:
        return jsonify({'message': 'Cashier not found'}), 404


@app.route('/api/cashier/<int:cashier_id>', methods=['PUT'])
def update_cashier_route(cashier_id):
    cashier = request.json
    row_count = update_cashier(connection, cashier)
    if row_count > 0:
        return jsonify({'message': 'Cashier updated successfully'}), 200
    else:
        return jsonify({'message': 'Cashier not found'}), 404


@app.route('/api/cashier/<int:cashier_id>', methods=['PUT'])
def delete_cashier_route(cashier_id):
    cashier = get_cashier(connection, cashier_id)
    if not cashier:
        return jsonify({'message': 'Cashier not found'}), 404
    row_count = soft_delete_cashier(connection, cashier_id)
    if row_count > 0:
        return jsonify({'message': 'Cashier deleted successfully'}), 200
    else:
        return jsonify({'message': 'Cashier not found'}), 404


if __name__ == '__main__':
    app.run(port=8000)
