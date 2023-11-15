import json

from flask import jsonify

from dao.products_dao import get_product


def create_order(connection, order):
    cursor = connection.cursor()
    sql = "INSERT INTO orders (items, cashier_id, total) VALUES (%s, %s, %s)"
    items = {}
    item_list = []
    total = 0
    for item in order['items']:
        product = get_product(connection, item['product_id'])
        total += product[0]['unit_price'] * item['quantity']
        item_list.append({
            'product_id': item['product_id'],
            'unit_price': product[0]['unit_price'],
            'quantity': item['quantity']
        })
    items['items'] = item_list
    print(items)
    cursor.execute(sql, (json.dumps(items), order['cashier_id'], total))
    connection.commit()
    return cursor.lastrowid


def get_order(connection, order_id):
    cursor = connection.cursor()
    sql = "SELECT * FROM orders WHERE id = %s"
    cursor.execute(sql, (order_id,))
    response = []
    for (id, items, cashier_id, total, created_at) in cursor:
        response.append({
            'id': id,
            'order_info': json.loads(items),
            'cashier_id': cashier_id,
            'total': total,
            'created_at': created_at
        })
    return response


def get_all_orders(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM orders"
    cursor.execute(sql)
    response = []
    for (id, items, cashier_id, total, created_at) in cursor:
        response.append({
            'id': id,
            'order_info': json.loads(items),
            'cashier_id': cashier_id,
            'total': total,
            'created_at': created_at
        })
    return response
