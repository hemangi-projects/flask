from flask import Flask, request, jsonify, make_response
import json
from flask_sqlalchemy import SQLAlchemy
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'hemangi'

# ishan belly dancer

app.debug = True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # after /// will be database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)



# Models
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    public_id = db.Column(db.String(50), unique=True)
    
    # @classmethod
    # def find_by_username(cls, username):
    #     return cls.query.filter_by(username=username).first()
    #
    # @classmethod
    # def find_by_id(cls, _id):
    #     return cls.query.filter_by(id=_id).first()


class ToDo(db.Model):
    __tablename__ = "todo"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    items = db.Column(db.String(200), unique=False, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')


@app.before_first_request
def create_tables():
    db.create_all()


# def authenticate(username, password):
#     user = User.find_by_username(username)
#     print("FHFHFGHGHGHGFHGHGFHGHGHGH",user)
#     if user and safe_str_cmp(user.password, password):
#         return user
#
#
# def identity(payload):
#     user_id = payload['identity']
#     return User.find_by_id(user_id)
#
#
# jwt = JWT(app, authenticate, identity)
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
            current_user = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated
# decorator for verifying the JWT


@app.route('/add_user', methods=["POST"])
def add_todo_user():
    values = json.loads(request.data)
    if values.get('username', False) and values.get('password', False):
        user = User(
            public_id=str(uuid.uuid4()),
            username=values.get('username', False),
            password=generate_password_hash(values.get('password', False))
        )
        db.session.add(user)
        db.session.commit()
        return json.dumps({'status_code': 200, 'message': 'User Added Successfully'})
    else:
        return json.dumps({'status_code': 404, 'error': 'UserName and Password can not be blank'})


@app.route('/login', methods=["POST"])
def login_todo():
    values = json.loads(request.data)
    if values.get('username', False) and values.get('password', False):
        user = User.query.filter_by(username=values.get('username', False)).first()
        if check_password_hash(user.password, values['password']):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'])

            return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    return make_response(jsonify({'error': 'Wrong UserName or Password'}), 404)

@app.route('/get_user', methods=["POST"])
@token_required
def get_user_id(current_user):
    values = json.loads(request.data)
    if values.get('username', False):
        user = User.query.filter_by(username=values.get('username', False)).first()
        return jsonify({'user': {'id':user.id,'username':user.username,'public_id':user.public_id}})
    else:
        return json.dumps({'status_code': 404, 'error': 'Wrong UserName or Password'})


@app.route('/edit_user', methods=["POST"])
@token_required
def edit_user(current_user):
    values = json.loads(request.data)
    if values.get('username', False) and values.get('new_password', False):
        user = User.query.filter_by(username=values.get('username', False)).first()
        user.password = generate_password_hash(values['new_password'])
        db.session.commit()
        return json.dumps({'status_code': 200, 'message': 'Password updated successfully'})
    else:
        return json.dumps({'status_code': 404, 'error': 'Wrong UserName or Password'})


@app.route('/delete_user', methods=["POST"])
@token_required
def delete_user(current_user):
    values = json.loads(request.data)
    if values.get('username', False):
        user = User.query.filter_by(username=values.get('username', False)).first()
        db.session.delete(user)
        db.session.commit()
        return json.dumps({'status_code': 200, 'message': 'User Deleted'})
    else:
        return json.dumps({'status_code': 404, 'error': 'Wrong UserName'})


@app.route('/add_todo', methods=["POST"])
@token_required
def add_todo(current_user):
    values = json.loads(request.data)
    if values.get('name', False):
        t = ToDo(user_id=current_user.id, name=values.get('name', False), items=values.get('items', False))
        db.session.add(t)
        db.session.commit()
        return json.dumps({'status_code': 200, 'message': 'Todo Added Successfully'})
    else:
        return json.dumps({'status_code': 404, 'error': 'UserID and Name are manadatory fields'})


@app.route('/edit_todo', methods=["POST"])
@token_required
def edit_todo(current_user):
    values = json.loads(request.data)
    if values.get('name', False):
        todo = ToDo.query.filter_by(name=values.get('name', False), user_id=current_user.id).first()
        todo.items = values['items']
        db.session.commit()
        return json.dumps({'status_code': 200, 'message': 'Items updated successfully'})
    else:
        return json.dumps({'status_code': 404, 'error': 'Wrong name or UserID'})


@app.route('/delete_todo', methods=["POST"])
@token_required
def delete_todo(current_user):
    values = json.loads(request.data)
    if values.get('name', False):
        todo = ToDo.query.filter_by(name=values.get('name', False)).first()
        db.session.delete(todo)
        db.session.commit()
        return json.dumps({'status_code': 200, 'message': 'ToDo Deleted'})
    else:
        return json.dumps({'status_code': 404, 'error': 'Wrong name'})


@app.route('/get_todo', methods=["POST"])
@token_required
def get_todo(current_user):
    values = json.loads(request.data)
    if values.get('name', False):
        todo = ToDo.query.filter_by(name=values.get('name', False)).first()
        if todo:
            return json.dumps(
                {'status_code': 200, 'data': {'user_id': todo.user_id, 'name': todo.name, 'items': todo.items}})
        else:
        	return json.dumps({'status_code': 404, 'error': 'Todo Not Found'})
    else:
        return json.dumps({'status_code': 404, 'error': 'Wrong USerID or ToDoName'})


@app.route('/')
def check():
    return 'Flask is working'


if __name__ == '__main__':
    app.run()
