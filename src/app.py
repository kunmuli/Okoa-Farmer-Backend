from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_jwt import JWT, JWTError
from src import google_auth
import json
from security import authenticate, identity
from src.resources.user import UserRegister
from src.google_auth import logout

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Masaki2017$$@localhost/okoafarmer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = '#^#%^%&#BgdvttkkgyDDT&*%$'
api = Api(app)
# api_bp = Blueprint('api', __name__)
# api = Api(api_bp)
# app.register_blueprint(google_auth.app)

jwt = JWT(app, authenticate, identity)  # /auth


@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization header?'}), 401


# Route
api.add_resource(UserRegister, '/register')


@app.route('/')
def home():
    return 'I am coming home'


# app.register_blueprint(google_auth.app)
@app.route('/google/login')
def google_login():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return jsonify({'user_info': json.dumps(user_info, indent=4), 'message': 'You have logged in successfully'})

    return jsonify({'message': 'You are not currently logged in.'})


@app.route('/google/logout')
def signOutUser():
    if google_auth.is_logged_in():
        logout()
    return jsonify({'message': 'You are not currently logged in.'})


@app.route('/end')
def end_():
    return 'it is finally done'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
