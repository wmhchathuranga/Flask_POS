def create_cashier(connection, cashier):
    cursor = connection.cursor()
    sql = "INSERT INTO cashier (name,nic,dob,profile_pic,address) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(sql, (cashier['name'], cashier['nic'], cashier['dob'], cashier['profile_pic'], cashier['address']))
    connection.commit()
    return cursor.lastrowid


def get_all_cashiers(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM cashier"
    cursor.execute(sql)
    response = []
    for (id, name, email) in cursor:
        response.append({
            'id': id,
            'name': name,
            'email': email
        })
    return response


def get_cashier(connection, cashier_id):
    cursor = connection.cursor()
    sql = "SELECT * FROM cashier WHERE id = %s"
    cursor.execute(sql, (cashier_id,))
    response = []
    for (id, name, email) in cursor:
        response.append({
            'id': id,
            'name': name,
            'email': email
        })
    return response


def update_cashier(connection, cashier):
    cursor = connection.cursor()
    sql = "UPDATE cashier SET name = %s, nic = %s, dob = %s, profile_pic = %s, address = %s WHERE id = %s"
    cursor.execute(sql, (
        cashier['name'], cashier['nic'], cashier['dob'], cashier['profile_pic'], cashier['address'], cashier['id']))
    connection.commit()
    return cursor.rowcount


def soft_delete_cashier(connection, cashier_id):
    cursor = connection.cursor()
    sql = "UPDATE cashier SET is_deleted = 1, deleted_at = NOW() WHERE id = %s"
    cursor.execute(sql, (cashier_id,))
    connection.commit()
    return cursor.rowcount
