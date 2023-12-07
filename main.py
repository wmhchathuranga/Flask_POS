import hashlib

from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dao.cashier_dao import *
from dao.order_dao import *
from dao.products_dao import *
from dao.quentity_dao import *
from db_connector.mysql_connector import mysql_connection

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = hashlib.sha256('chathuranga'.encode()).hexdigest()
jwt = JWTManager(app)
app.config['UPLOAD_FOLDER'] = './uploads'
CORS(app, origins="*", supports_credentials=True)
connection = mysql_connection()


def check_admin(current_user):
    cursor = connection.cursor()
    sql = "SELECT is_admin FROM cashier WHERE nic = %s and is_deleted = 0"
    cursor.execute(sql, (current_user,))
    is_admin = cursor.fetchone()[0]
    return is_admin


# login route
@app.route('/login', methods=['POST'])
def login():
    print(request.json)
    cursor = connection.cursor()
    username = request.json.get('nic')
    password = request.json.get('password')
    slq = "SELECT * FROM cashier WHERE nic = %s AND password = %s"
    cursor.execute(slq, (username, hashlib.sha256(password.encode('utf-8')).hexdigest()))
    if cursor.fetchone():
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    else:
        return {'message': 'Invalid username or password'}, 401


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
    if product_id > 0:
        return jsonify({'product_id': product_id}), 201
    else:
        return jsonify({'message': 'Product already exists'}), 409


@app.route('/api/update_product', methods=['PUT'])
@jwt_required()
def update_product_route():
    current_user = get_jwt_identity()
    is_admin = check_admin(current_user)
    if not is_admin:
        return jsonify({'message': 'Unauthorized'}), 401
    product = request.json
    row_count = update_product(connection, product)
    if row_count > 0:
        return jsonify({'message': 'Product updated successfully'}), 200
    elif row_count == 0:
        return jsonify({'message': 'Product Not Found or Already Updated'}), 404
    else:
        return jsonify({'message': 'Product Already Exists'}), 409


@app.route('/api/delete_product/<int:product_id>', methods=['PUT'])
@jwt_required()
def soft_delete_product_route(product_id):
    current_user = get_jwt_identity()
    is_admin = check_admin(current_user)
    if not is_admin:
        return jsonify({'message': 'Unauthorized'}), 401
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
    if quantity_id > 0:
        return jsonify({'quantity_id': quantity_id}), 201
    else:
        return jsonify({'message': 'Quantity Already Exists'}), 403


@app.route('/api/update_quantity', methods=['PUT'])
def update_quantity_route():
    quantity = request.json
    row_count = update_quantity(connection, quantity)
    if row_count > 0:
        return jsonify({'message': 'Quantity updated successfully'}), 200
    elif row_count == 0:
        return jsonify({'message': 'Quantity Not Found or Already Updated'}), 404
    else:
        return jsonify({'message': 'Quantity Already Exists'}), 403


@app.route('/api/delete_quantity/<int:quantity_id>', methods=['PUT'])
@jwt_required()
def delete_quantity_route(quantity_id):
    current_user = get_jwt_identity()
    is_admin = check_admin(current_user)
    if not is_admin:
        return jsonify({'message': 'Unauthorized'}), 401
    quantity = get_quantity(connection, quantity_id)
    if not quantity:
        return jsonify({'message': 'Quantity not found'}), 404
    row_count = soft_delete_quantity(connection, quantity_id)
    if row_count > 0:
        return jsonify({'message': 'Quantity deleted successfully'}), 200
    else:
        return jsonify({'message': 'Quantity not found'}), 404


@app.route('/api/all_orders', methods=['GET'])
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


@app.route('/api/add_order', methods=['POST'])
def create_order_route():
    order = request.json
    order_id = create_order(connection, order)
    return jsonify({'order_id': order_id}), 201


@app.route('/api/add_cashier', methods=['POST'])
def create_cashier_route():
    # cashier = request.file
    cashier_id = create_cashier(connection, request)
    return jsonify({'cashier_id': cashier_id}), 201


@app.route('/api/all_cashiers', methods=['GET'])
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


@app.route('/api/update_cashier', methods=['PUT'])
@jwt_required()
def update_cashier_route():
    current_user = get_jwt_identity()
    is_admin = check_admin(current_user)
    if not is_admin:
        return jsonify({'message': 'Unauthorized'}), 401
    cashier = request
    row_count = update_cashier(connection, cashier)
    if row_count > 0:
        return jsonify({'message': 'Cashier updated successfully'}), 200
    elif row_count == 0:
        return jsonify({'message': 'Cashier Not Found or Already Updated'}), 404
    else:
        return jsonify({'message': 'NIC already exists'}), 403


@app.route('/api/delete_cashier/<int:cashier_id>', methods=['PUT'])
@jwt_required()
def delete_cashier_route(cashier_id):
    current_user = get_jwt_identity()
    is_admin = check_admin(current_user)
    if not is_admin:
        return jsonify({'message': 'Unauthorized'}), 401
    cashier = get_cashier(connection, cashier_id)
    if not cashier:
        return jsonify({'message': 'Cashier not found'}), 404
    row_count = soft_delete_cashier(connection, cashier_id)
    if row_count > 0:
        return jsonify({'message': 'Cashier deleted successfully'}), 200
    else:
        return jsonify({'message': 'Cashier not found'}), 404


# route to get images in uploads folder
@app.route('/api/uploads/<path:filename>', methods=['GET'])
def get_uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
