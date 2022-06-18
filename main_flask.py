import jwt
import uuid
import json
from flask import Flask, request, Response, jsonify, make_response
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from db_management.db_repo import DbRepo
from db_management.db_config import local_session
from tables.users import Users
from tables.customers import Customers

repo = DbRepo(local_session)
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'


def convert_to_json(_list): #cleaning & jsoning data recieved from SQLACLCHEMY
    json_list = []
    for i in _list:
        _dict = i.__dict__
        _dict.pop('_sa_instance_state', None)
        json_list.append(_dict)
    return json_list


def add_customer_user(_input):
    repo.add(Users(     id=_input['user_id'],
                        username=_input['username'],
                        password=_input['password'],
                        email=_input['email'],
                        user_role=3))
    repo.add(Customers( id=_input['id'],
                        first_name=_input['first_name'],
                        last_name=_input['last_name'],
                        address=_input['address'],
                        phone_number=_input['phone_number'],
                        credit_card_number=_input['credit_card_number'],
                        user_id=_input['user_id']))
    return Response(f'"new-item": "{request.url}"', status=201, mimetype='application/json')


def update_customer(_input, id):
    customers_json = convert_to_json(repo.get_all(Customers))
    for c in customers_json:
        if c["id"] == id:
            c["id"] = _input["id"] if "id" in _input.keys() else None
            c["first_name"] = _input["first_name"] if "first_name" in _input.keys() else None
            c["last_name"] = _input["last_name"] if "last_name" in _input.keys() else None
            c["address"] = _input["address"] if "address" in _input.keys() else None
            c["phone_number"] = _input["phone_number"] if "phone_number" in _input.keys() else None
            c["credit_card_number"] = _input["credit_card_number"] if "credit_card_number" in _input.keys() else None
            repo.update_by_id(Customers, Customers.id, id, c)
    return Response(f'"Updated-item": "{request.url}"', status=200, mimetype='application/json')


@app.route('/signup', methods=['POST'])
def signup():
    form_data = request.form
    # gets username, email and password
    username = form_data.get('username')
    password = form_data.get('password')
    email = form_data.get('email')
    # check if user exists
    user = repo.get_by_column_value(Users, Users.username, username)
    if user: return Response('User already exists. Please Log in.', status=202, mimetype='application/json')
    else:
        repo.add(Users(username=username, password=generate_password_hash(password), email=email, public_id=str(uuid.uuid4()), user_role=3 ))
        return Response('Successfully registered.', status=201, mimetype='application/json')


@app.route('/login', methods=['POST'])
def login():
    form_data = request.form
    # check that no field is missing
    if not form_data.get('username') or not form_data.get('email') or not form_data.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="Login required!"'})
    # check if user exists
    user = repo.get_by_column_value(Users, Users.username, form_data.get('username'))
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="User does not exist!"'})
    # check password
    if not check_password_hash(user[0].password, form_data.get('password')):
        return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm ="Wrong Password!"'})
    # generates the JWT Token
    token = jwt.encode({'public_id': user[0].public_id,
                        'exp': datetime.utcnow() + timedelta(minutes=30)},
                        app.config['SECRET_KEY'])
    return make_response(jsonify({'token': token.decode('UTF-8')}), 201)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer ')
        if not token: return jsonify({'message': 'Token is missing !!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = repo.get_by_column_value(Users, Users.public_id, data['public_id'])
        except: return jsonify({'message': 'Token is invalid !!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = repo.get_all(Users)
    print(current_user[0].username)
    print(current_user[0].email)
    print(current_user[0].password)
    # convert to json
    output = []
    for user in users: output.append({'public_id': user.public_id, 'username': user.username, 'email': user.email})
    return jsonify({'users': output})

# localhost:5000/
# static page
# dynamic page
@app.route("/")
def home():
    print('hi')
    return '''
        <html>
            Customers!
            Countries!
            Administrators!
            Airline Companies!
            Users!
            User-Roles!
            Flights!
            Tickets!
        </html>
    '''

@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customer():
    customers = convert_to_json(repo.get_all(Customers))
    if request.method == 'GET':
        print(request.args.to_dict())
        search_args = request.args.to_dict()
        if len(search_args) == 0: Response(json.dumps(customers), status=200, mimetype='application/json')
        results = []
        #query check
        for c in customers:
            if "first_name" in search_args.keys() and c["first_name"].find(search_args["first_name"]) < 0: continue
            if "last_name" in search_args.keys() and c["last_name"].find(search_args["last_name"]) < 0: continue
            if "address" in search_args.keys() and c["address"].find(search_args["address"]) < 0: continue
            if "phone_number" in search_args.keys() and c["phone_number"].find(search_args["phone_number"]) < 0: continue
            if "credit_card_number" in search_args.keys() and c["credit_card_number"].find(search_args["credit_card_number"]) < 0: continue
            results.append(c)
        if len(results) == 0: return Response("[]", status=404, mimetype='application/json')
        return Response(json.dumps(customers), status=200, mimetype='application/json')
    if request.method == 'POST':
        #  {"username": "1i1y", "password": "passw0rd", "email": "lily@jb.com", "id":4, "first_name":"lily", "last_name":"musnikov", "address":"narnia22", "phone_number":"0565452243", "credit_card_number":"65546765534", "user_id":8}
        new_customer = request.get_json()
        if repo.get_by_id(Users,new_customer['user_id']): return 'Input violates restrictions!'
    return add_customer_user(new_customer)

@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def get_customer_by_id(id):
    customers = convert_to_json(repo.get_all(Customers))
    if request.method == 'GET':
        for c in customers:
            if c["id"] == id: return Response(json.dumps(c), status=200, mimetype='application/json')
        return Response("[]", status=404, mimetype='application/json')
    if request.method == 'PUT':
        #  {"username": "1i1y", "password": "passw0rd", "email": "lily@jb.com", "id":4, "first_name":"lily", "last_name":"musnikov", "address":"narnia22", "phone_number":"0565452243", "credit_card_number":"65546765534", "user_id":8}
        updated_new_customer = request.get_json()
        if repo.get_by_id(Customers, id) != None: return update_customer(updated_new_customer, id)
        return add_customer_user(updated_new_customer)
    if request.method == 'PATCH':
        # {"username": "1i1y", "password": "passw0rd", "email": "lily@jb.com", "id":4, "first_name":"lily", "last_name":"musnikov", "address":"narnia22", "phone_number":"0565452243", "credit_card_number":"65546765534", "user_id":8}
        updated_customer = request.get_json()
        if repo.get_by_id(Customers, id) != None: return update_customer(updated_customer, id)
        return Response("[]", status=404, mimetype='application/json')
    if request.method == 'DELETE':
        deleted_customer = request.get_json()
        for c in customers:
            if c["id"] == id:
                repo.delete_by_id(Customers, Customers.id, id)
                repo.delete_by_id(Users, Users.id, c["user_id"])
                return f'{json.dumps(deleted_customer)} deleted'
        return Response("[]", status=404, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
