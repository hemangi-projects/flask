from flask import Flask, request, jsonify, make_response, Blueprint
import jwt
from functools import wraps
from models.users import UserModel
import json
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash
from db import db
from datetime import datetime, timedelta
auth = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = UserModel.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated

@auth.route('/add_user', methods=["POST"])
def add_user():
    values = json.loads(request.data)
    if values.get('username', False) and values.get('password', False):
        user = UserModel(
            public_id=str(uuid.uuid4()),
            username=values.get('username', False),
            password=generate_password_hash(values.get('password', False)),
            type=values['type'] if values.get('type',False) else 'student'
        )
        db.session.add(user)
        db.session.commit()
        return json.dumps({'status_code': 200, 'message': 'User Added Successfully'})
    else:
        return json.dumps({'status_code': 404, 'error': 'UserName and Password can not be blank'})

@auth.route('/login', methods=["POST"])
def login_todo():
    values = json.loads(request.data)
    if values.get('username', False) and values.get('password', False):
        user = UserModel.query.filter_by(username=values.get('username', False)).first()
        if check_password_hash(user.password, values['password']):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'])

            return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    return make_response(jsonify({'error': 'Wrong UserName or Password'}), 404)