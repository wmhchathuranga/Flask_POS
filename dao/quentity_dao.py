import mysql.connector


def get_quantity(connection, quantity_id):
    cursor = connection.cursor()
    sql = "SELECT * FROM quantity WHERE id = %s and is_deleted = 0"
    cursor.execute(sql, (quantity_id,))
    response = []
    for (id, name, unit, created_at, updated_at, deleted_at, is_deleted) in cursor:
        response.append({
            'id': id,
            'name': name,
            'unit': unit
        })
        return response


def get_all_quantities(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM quantity where is_deleted = 0"
    cursor.execute(sql)
    response = []
    for (id, name, unit, created_at, updated_at, deleted_at, is_deleted) in cursor:
        response.append({
            'id': id,
            'name': name,
            'unit': unit
        })
    return response


def add_quantity(connection, quantity):
    cursor = connection.cursor()
    sql = "INSERT INTO quantity (name, unit) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (quantity['name'], quantity['unit']))
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.errors.IntegrityError:
        return -1


def update_quantity(connection, quantity):
    cursor = connection.cursor()
    sql = "UPDATE quantity SET name = %s, unit = %s, updated_at = NOW() WHERE id = %s"
    try:
        cursor.execute(sql, (quantity['name'], quantity['unit'], quantity['id']))
        connection.commit()
        return cursor.rowcount
    except mysql.connector.errors.IntegrityError:
        return -1


def soft_delete_quantity(connection, quantity_id):
    cursor = connection.cursor()
    sql = "UPDATE quantity SET is_deleted = 1, deleted_at = NOW() WHERE id = %s"
    cursor.execute(sql, (quantity_id,))
    connection.commit()
    return cursor.rowcount
