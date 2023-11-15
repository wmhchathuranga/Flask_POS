def create_order(connection, order):
    cursor = connection.cursor()
    sql = "INSERT INTO orders (items, cashier_id, total) VALUES (%s, %s, %s)"
    items = []
    for item in order['items']:
        items.append({
            'product_id': item['product_id'],
            'uint_price': item['unit_price'],
            'quantity': item['quantity']
        })
    cursor.execute(sql, (items, order['cashier_id'], order['total']))
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
            'items': items,
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
            'items': items,
            'cashier_id': cashier_id,
            'total': total,
            'created_at': created_at
        })
    return response
