import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from functions.api_core_functions import *
from functions.user_functions import *
from functions.company_functions import *

# init sentry for error handling
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://c5facdea19b74f9c9679ae196f08a204@o1318032.ingest.sentry.io/6774585",
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0
)
# load env variables from the .env file
load_dotenv()

# initiate the flask object
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'This is the api for GroupRota, Developed by Jon James - Freelance Developer'


if __name__ == '__main__':
    app.run(port=80)


# route to call when user is signing up to key
# generate API key and store it, along with uuid and email
@app.route('/user/signup', methods=['GET'])
def user_signup():
    return "user signup"


# declare route to follow when user is requesting API key
@app.route('/user/get_key', methods=['GET'])
def user_get_key():
    return "user get_key"


@app.route('/company/create', methods=['GET'])
def create_company():
    return "company create"

@app.route('/company/get_all', methods=['GET'])
def read_companies():
    return "company get_all"


@app.route('/company/read', methods=['GET'])
def read_company():
    return "company get"


@app.route('/company/update', methods=['GET'])
def update_company():
    return "company update"

@app.route('/system/test', methods=['GET'])
def test():
    args = request.args
    if 'uid' in args:
        uid = str(args['uid'])
    else:
        return jsonify({"code": 400, "message": 'Error: No UUID field provided. Please specify an UUID.'})
    if 'email' in request.args:
        email = str(args['email'])
    else:
        return jsonify({"code": 400, "message": 'Error: No Email field provided. Please specify an Email.'})
    if check_admin(email, uid):
        # test if api can connect to database
        if check_db():
            return jsonify({"code": 200, "message": "Api connected successfully"})
        else:
            return jsonify({"code": 500, "message": "MySQL Connection Error. Please check logs for more information"})
    else:
        return jsonify({"code": 500, "message": "You are not authorised to access this route. If you belive this to be in error please contact the admin @ admin@grouprota.com"})
