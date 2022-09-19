from flask import Flask, request, jsonify
from dotenv import load_dotenv
from functions.api_core_functions import *
from functions.user_functions import *
from functions.company_functions import *
# from werkzeug.middleware.proxy_fix import ProxyFix

# load env variables from the .env file
load_dotenv()

# initiate the flask object
app = Flask(__name__)

# declare unauthorised access reponse


# # if app is hosted on prod server, run proxy check
# if os.environ.get('SERVER') == "PROD":
#     app.wsgi_app = ProxyFix(
#         app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
#     )
#

@app.route('/')
def hello_world():  # put application's code here
    return 'This is the api for GroupRota, Developed by Jon James - Freelance Developer'


if __name__ == '__main__':
    app.run(port=80)


# route to call when user is signing up to key
# generate API key and store it, along with uuid and email
@app.route('/user/signup', methods=['GET'])
def user_signup():
    # check if uuid and email are present in the uri
    args = request.args
    if 'uuid' in args:
        uuid = str(args['uuid'])
    else:
        # return "Error: No UUID field provided. Please specify a UUID."
        return jsonify({"code": 400, "message": 'Error: No UUID field provided. Please specify an UUID.'})
    if 'email' in request.args:
        email = str(args['email'])
    else:
        return jsonify({"code": 400, "message": 'Error: No Email field provided. Please specify an Email.'})
        # return "Error: No Email field provided. Please specify an Email."
    return signup_user(uuid, email)


# declare route to follow when user is requesting API key
@app.route('/user/get_key', methods=['GET'])
def user_get_key():
    # check if uuid is present in the uri
    args = request.args
    if 'uuid' in request.args:
        uuid = str(args['uuid'])
    else:
        return jsonify({"code": 400, "message": "Error: No UUID field provided. Please specify an UUID."})
    
    if check_if_exists(uuid):
        key = get_key(uuid)
        if key:
            return key
        else:
            return jsonify({"code": 401, "message": "No key is available for this UUID. Please try another UUID"})
    else:
        return jsonify({"code": 401, "message": "This user does not exist"})
    # return check_if_exists(uuid)


@app.route('/company/create', methods=['GET'])
def create_company():
    # check if uuid and name are present in the uri
    args = request.args
    if 'name' in args:
        name = str(args['name'])
    else:
        return jsonify({"code": 400, "message": "No company name provided. Please provide a company name"})
    if 'uuid' in request.args:
        uuid = str(args['uuid'])
    else:
        return jsonify({"code": 400, "message": "Error: No UUID field provided. Please specify an UUID."})
    if access_control(uuid):
        return make_company(uuid, name)
    else:
        return jsonify({'code': 401, 'message': 'You are not authorised to use this API. If you believe this to be in '
                                                 'error please contact the admin at admin@grouprota.com'})


@app.route('/company/get_all', methods=['GET'])
def read_companies():
    args = request.args
    # check if uuid is present in the uri
    if 'uuid' in request.args:
        uuid = str(args['uuid'])
    else:
        return jsonify({"code": 400, "message": "Error: No UUID field provided. Please specify an UUID."})
    if access_control(uuid) != False:
        return jsonify(get_companies_for_user(uuid))
    else:
        return jsonify({'code': 401, 'message': 'You are not authorised to use this API. If you believe this to be in '
                                                 'error please contact the admin at admin@grouprota.com'})


@app.route('/company/read', methods=['GET'])
def read_company():
    args = request.args
    # check if uuid is present in the uri
    if 'ucid' in request.args:
        ucid = str(args['ucid'])
        # print(ucid)
    else:
        return jsonify({"code": 400, "message": "Error: No UCID field provided. Please specify an UCID."})
    company = get_company_details(ucid)
    print(company)
    return company


@app.route('/company/update', methods=['GET'])
def update_company():
    args = request.args
    print(args)
    # check if uuid, ucid and name are present in the uri
    if 'key' in request.args:
        key = str(args['key'])
    else:
        return jsonify({"code": 400, "message": "Error: No KEY field provided. Please specify an KEY."})
    if 'ucid' in request.args:
        ucid = str(args['ucid'])
    else:
        return jsonify({"code": 400, "message": "Error: No UCID field provided. Please specify an UCID."})
    if 'name' in request.args:
        name = str(args['name'])
    else:
        return jsonify({"code": 400, "message": "Error: No Name provided. Please specify a Name."})

    #check if the key matches the user who owns the company
    company_owner = get_company_details(ucid)
    # return str(company_owner['owner_uuid'])
    if (verify_key(company_owner['owner_uuid'], key)):
        # send info to the company_update function to update the company details
        return company_update(ucid, name, key)
    else:
        return jsonify({'code': 401, 'message': 'You are not authorised to use this API. If you believe this to be in '
                                                 'error please contact the admin at admin@grouprota.com'})


@app.route('/system/read_environ', methods=['GET'])
def display_envs():
    return os.environ
