import os

import pymysql
from flask import jsonify
from pymysql import DatabaseError

# save db login vars to variables
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_DATABASE_NAME")


# define the database connection function

def connect_to_db():
    try:
        connection = pymysql.connect(host=db_host,
                                     user=db_user,
                                     password=db_pass,
                                     database=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.err.InternalError as e:
        return jsonify({'code': 500, 'message': 'MySQL Internal Error: ' + e.args[1]})
    except DatabaseError as e:
        # if e.args[1] == '#42000Unknown database \'{0}\''.format(db_name):
        return jsonify({'code': 500, 'message': 'Databse Error: ' + e.args[1]})
    except Exception as e:
        return jsonify({'code': 500, 'message': 'MySQL Exception: ' + str(e)})


def check_db():
    con = connect_to_db()
    if con.open:
        return True
    else:
        return False


def check_admin(email, uid):
    con = connect_to_db()
    if con.open:
        with con:
            with con.cursor() as cursor:
                sql = "select * from admin_emails where uid = %s"
                cursor.execute(sql, uid)
                result = cursor.fetchone()

                if result['email'] == str(email):
                    return True
                else:
                    return False
    else:
        return False
