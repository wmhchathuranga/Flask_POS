import mysql.connector


def get_all_products(connection):
    cursor = connection.cursor()
    sql = ("SELECT products.id, products.name, products.unit_price, products.quantity_id, products.created_at, "
           "products.updated_at, products.deleted_at, products.is_deleted, quantity.unit FROM products "
           "inner join quantity on products.quantity_id = quantity.id where products.is_deleted = 0")
    cursor.execute(sql)
    response = []
    for (id, name, unit_price, quantity_id, created_at, updated_at, deleted_at, is_deleted, q_unit) in cursor:
        response.append({
            'id': id,
            'name': name,
            'unit_price': unit_price,
            'quantity_id': quantity_id,
            'quantity_unit': q_unit,
        })
    return response


def get_product(connection, product_id):
    cursor = connection.cursor()
    sql = ("SELECT products.id, products.name, products.unit_price, products.quantity_id, products.created_at, "
           "products.updated_at, products.deleted_at, products.is_deleted, quantity.name FROM products inner join "
           "quantity on products.quantity_id = quantity.id WHERE products.id = %s and products.is_deleted = 0")
    cursor.execute(sql, (product_id,))
    response = []
    for (id, p_name, unit_price, quantity_id, created_at, updated_at, deleted_at, is_deleted, q_name) in cursor:
        response.append({
            'id': id,
            'name': p_name,
            'unit_price': unit_price,
            'quantity_id': quantity_id,
            'quantity_name': q_name
        }
        )
    return response


def add_product(connection, product):
    cursor = connection.cursor()
    sql = "INSERT INTO products (name, unit_price, quantity_id) VALUES (%s, %s, %s)"
    try:
        cursor.execute(sql, (product['name'], product['unit_price'], product['quantity_id']))
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.errors.IntegrityError:
        return -1


def update_product(connection, product):
    cursor = connection.cursor()
    sql = "UPDATE products SET name = %s, unit_price = %s, quantity_id = %s, updated_at = NOW() WHERE id = %s"
    try:
        cursor.execute(sql, (product['name'], product['unit_price'], product['quantity_id'], product['id']))
        connection.commit()
        return cursor.rowcount
    except mysql.connector.errors.IntegrityError:
        return -1


def soft_delete_product(connection, product_id):
    cursor = connection.cursor()
    sql = "UPDATE products SET is_deleted = 1, deleted_at = NOW() WHERE id = %s"
    cursor.execute(sql, (product_id,))
    connection.commit()
    return cursor.rowcount
