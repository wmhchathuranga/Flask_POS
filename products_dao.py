from mysql_connector import mysql_connection


def get_all_products(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM products"
    cursor.execute(sql)
    return cursor.fetchall()


def get_product(connection, product_id):
    cursor = connection.cursor()
    sql = "SELECT * FROM products WHERE id = %s"
    cursor.execute(sql, (product_id,))
    return cursor.fetchone()


def add_product(connection, product):
    cursor = connection.cursor()
    sql = "INSERT INTO products (name, unit_price, quantity_id) VALUES (%s, %s, %s)"
    cursor.execute(sql, (product['name'], product['unit_price'], product['quantity_id']))
    connection.commit()
    return cursor.lastrowid


def update_product(connection, product):
    cursor = connection.cursor()
    sql = "UPDATE products SET name = %s, unit_price = %s, quantity_id = %s, updated_at = NOW() WHERE id = %s"
    cursor.execute(sql, (product['name'], product['unit_price'], product['quantity_id'], product['id']))
    connection.commit()
    return cursor.rowcount


def soft_delete_product(connection, product):
    cursor = connection.cursor()
    sql = "UPDATE products SET is_deleted = 1, deleted_at = NOW() WHERE id = %s"
    cursor.execute(sql, (product['id'],))
    connection.commit()
    return cursor.rowcount


if __name__ == '__main__':
    connection_obj = mysql_connection()
    print(get_all_products(connection_obj))
