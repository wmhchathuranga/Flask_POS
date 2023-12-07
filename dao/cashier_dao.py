import hashlib
import os

import mysql.connector
from flask import json
from werkzeug.utils import secure_filename

from main import app


def create_cashier(connection, req, filename=""):
    cursor = connection.cursor()
    if 'profile_pic' in req.files:
        profile_pic = req.files['profile_pic']
        filename = secure_filename(profile_pic.filename)
        profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cashier = req.form['cashier']
    cashier = json.loads(cashier)

    sql = "INSERT INTO cashier (name,nic,password,dob,profile_pic,address) VALUES (%s,%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql,
                       (cashier['name'], cashier['nic'], hashlib.sha256(cashier['password'].encode()).hexdigest(),
                        cashier['dob'], filename,
                        cashier['address']))
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.errors.IntegrityError:
        return -1


def get_all_cashiers(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM cashier WHERE is_deleted = 0"
    cursor.execute(sql)
    response = []
    for (id, is_admin, name, nic, password, dob, profile_pic, address, created_at, deleted_at, updated_at, is_deleted,
         ) in cursor:
        response.append({
            'id': id,
            'name': name,
            'dob': dob.strftime('%a, %d-%m-%Y'),
            'nic': nic,
            'profile_pic': profile_pic,
            'address': address,
        })
    return response


def get_cashier(connection, cashier_id):
    cursor = connection.cursor()
    sql = "SELECT * FROM cashier WHERE id = %s and is_deleted = 0"
    cursor.execute(sql, (cashier_id,))
    response = []
    for (id, is_admin, name, nic, password, dob, profile_pic, address, created_at, deleted_at, updated_at,
         is_deleted) in cursor:
        response.append({
            'id': id,
            'name': name,
            'nic': nic,
            'dob': dob.strftime('%a, %d-%m-%Y'),
            'profile_pic': profile_pic,
            'address': address,
        })
    return response


def update_cashier(connection, req, filename=""):
    cursor = connection.cursor()
    if 'profile_pic' in req.files:
        profile_pic = req.files['profile_pic']
        filename = secure_filename(profile_pic.filename)
        profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cashier = req.form['cashier']
    cashier = json.loads(cashier)

    sql = ("UPDATE cashier SET name = %s, nic = %s, dob = %s, profile_pic = %s, address = %s,updated_at = NOW() WHERE "
           "id = %s")
    try:
        cursor.execute(sql, (
            cashier['name'], cashier['nic'], cashier['dob'], filename, cashier['address'], cashier['id']))
        connection.commit()
        return cursor.rowcount
    except mysql.connector.errors.IntegrityError:
        return -1


def soft_delete_cashier(connection, cashier_id):
    cursor = connection.cursor()
    sql = "UPDATE cashier SET is_deleted = 1, deleted_at = NOW() WHERE id = %s"
    cursor.execute(sql, (cashier_id,))
    connection.commit()
    return cursor.rowcount


# password reset for cashier
def reset_cashier_password(connection, cashier_id, old_password, password):
    cursor = connection.cursor()
    old_password = hashlib.sha256(old_password)
    sql = "SELECT * FROM cashier WHERE id = %s and password = %s"
    cursor.execute(sql, (cashier_id, old_password))
    if cursor.rowcount == 0:
        return -1
    sql = "UPDATE cashier SET password = %s WHERE id = %s"
    cursor.execute(sql, (hashlib.sha256(password), cashier_id))
    connection.commit()
    return cursor.rowcount
