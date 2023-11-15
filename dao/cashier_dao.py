def create_cashier(connection, cashier):
    cursor = connection.cursor()
    sql = "INSERT INTO cashier (name,nic,dob,profile_pic,address) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(sql, (cashier['name'], cashier['nic'], cashier['dob'], cashier['profile_pic'], cashier['address']))
    connection.commit()
    return cursor.lastrowid


def get_all_cashiers(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM cashier WHERE is_deleted = 0"
    cursor.execute(sql)
    response = []
    for (id, name, nic, dob, profile_pic, address, created_at, deleted_at, is_deleted) in cursor:
        response.append({
            'id': id,
            'name': name,
            'dob': dob,
            'nic': nic,
            'profile_pic': profile_pic,
            'address': address,
        })
    return response


def get_cashier(connection, cashier_id):
    cursor = connection.cursor()
    sql = "SELECT * FROM cashier WHERE id = %s"
    cursor.execute(sql, (cashier_id,))
    response = []
    for (id, name, nic, dob, profile_pic, address, created_at, deleted_at, is_deleted) in cursor:
        response.append({
            'id': id,
            'name': name,
            'nic': nic,
            'dob': dob,
            'profile_pic': profile_pic,
            'address': address,
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
