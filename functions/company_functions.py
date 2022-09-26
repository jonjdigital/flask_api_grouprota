import functions.api_core_functions as funcs1
import functions.user_functions as user_funcs
from flask import jsonify


def make_company(uuid, name):
    con = funcs1.connect_to_db()
    sql = "insert into company_backup (company_name, owner_uuid) VALUES (%s,%s)"
    with con:
        with con.cursor() as cursor:
            cursor.execute(sql, (name, uuid))
            con.commit()
            return jsonify({'code': 200, 'message': 'Company Successfully Saved'})


def get_companies_for_user(uuid):
    # return all companies that user is owner of
    con = funcs1.connect_to_db()
    sql = "select * from company_backup where owner_uuid = %s"
    with con:
        with con.cursor() as cursor:
            cursor.execute(sql, uuid)
            con.commit()
            result = cursor.fetchall()
            # return all records
            return result


def get_company_details(ucid):
    # return all companies that user is owner of
    con = funcs1.connect_to_db()
    sql = "select * from company_backup where ucid = %s"
    with con:
        with con.cursor() as cursor:
            cursor.execute(sql, ucid)
            con.commit()
            result = cursor.fetchall()
            # return all records
            return result[0]


def company_update(ucid, name, key):
    # update the details of the company but verify it is owner doing so
    con = funcs1.connect_to_db()

    # get current company record
    sql = "select owner_uuid from company_backup where ucid = %s"
    with con:
        with con.cursor() as cursor:
            cursor.execute(sql, ucid)
            con.commit()
            owner_id = int(cursor.fetchone()['owner_uuid'])
            # print(key)
            user = int(user_funcs.get_uuid_from_key(key))
            # return user
            if owner_id == user:
                sql = "update company_backup set company_name = %s where owner_uuid = %s and ucid = %s"
                cursor.execute(sql, (name, user, ucid))
                con.commit()

                # return new company record
                sql = "select * from company_backup where ucid = %s"
                cursor.execute(sql, ucid)
                return jsonify({'code': 200, 'message': 'Company details successfully updated'})
            else:
                # if user does not match the one who made the company, request is denied
                return jsonify({'code': 401, 'message': 'You are not authorised to make this change'})

