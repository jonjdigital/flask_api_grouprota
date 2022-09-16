import random

import functions.api_core_functions as funcs1


def access_control(uuid):
    access = get_key(uuid)
    if restrict_to_api_user(access['api_key']):
        return True
    else:
        return False

def restrict_to_api_user(key):
    user = get_uuid_from_key(key)
    if user.count() == 1:
        return True
    else:
        return False


def signup_user(uuid, email):
    characters = "abcdefghijklmnopqrstuvwxyzABCEDFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_str = ''.join(random.choice(characters) for i in range(20))
    connection = funcs1.connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            # insert uuid and random string into api_key table
            sql = "insert into api_keys (uuid, api_key) values (%s, %s)"
            print(sql)
            cursor.execute(sql, (uuid, random_str))
            connection.commit()

            # insert uuid and email into users table
            sql = "insert into users (uuid,email) values (%s,%s)"
            print(sql)
            cursor.execute(sql, (uuid, email))
            connection.commit()

            # read back the users info back to the application
            sql = "select api_keys.uuid, api_keys.api_key, users.email from api_keys inner join users on api_keys.uuid=users.uuid where api_keys.uuid = %s"
            print(sql)
            cursor.execute(sql, uuid)
            result = cursor.fetchone()
            print(result)
            return result


def get_key(uuid):
    connection = funcs1.connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            sql = "select api_key from api_keys where uuid = %s"
            cursor.execute(sql, uuid)
            result = cursor.fetchone()
            # print(result)
            return result


def verify_key(uuid, key):
    connection = funcs1.connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            sql = "select api_key from api_keys where uuid = %s"
            cursor.execute(sql, uuid)
            result = cursor.fetchone()
            if (result['api_key'] != key):
                return False
            # print(result)
            return True


def get_uuid_from_key(key):
    connection = funcs1.connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            sql = "select uuid from api_keys where api_key = %s"
            cursor.execute(sql, key)
            connection.commit()
            result = cursor.fetchone()
            # print(result)
            return result


def check_if_exists(uuid):
    connection = funcs1.connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            sql = "select * from users where uuid = %s"
            cursor.execute(sql, uuid)
            connection.commit()
            result = cursor.fetchone()
            if result.count() == 0:
                return False
            # print(result)
            return True
