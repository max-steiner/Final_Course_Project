from flask import Flask, request, jsonify, render_template
from db_management.db_repo import DbRepo
from db_management.db_config import local_session
from tables.users import Users
from tables.customers import Customers
from flask_cors import CORS, cross_origin

repo = DbRepo(local_session)
app = Flask(__name__)
CORS(app)


def convert_to_json(_list): #cleaning & jsoning data recieved from SQLACLCHEMY
    json_list = []
    for i in _list:
        _dict = i.__dict__
        _dict.pop('_sa_instance_state', None)
        json_list.append(_dict)
    return json_list


def add_customer_user(_input):
    repo.add(Users(username=_input['username'],
                   password= _input['password'],
                   email=_input['email'],
                   user_role=3))
    user = repo.get_by_column_value(Users, Users.username, _input['username'])
    customer = repo.add(Customers(first_name=_input['first_name'],
                                  last_name=_input['last_name'],
                                  address=_input['address'],
                                  phone_number=_input['phone_number'],
                                  credit_card_number=_input['credit_card_number'],
                                  user_id=user[0].id))
    return jsonify(customer)


def update_customer(_input, id_):
    customers_json = convert_to_json(repo.get_all(Customers))
    for c in customers_json:
        if c["id"] == id_:
            c["id"] = _input["id"] if "id" in _input.keys() else None
            c["first_name"] = _input["first_name"] if "first_name" in _input.keys() else None
            c["last_name"] = _input["last_name"] if "last_name" in _input.keys() else None
            c["address"] = _input["address"] if "address" in _input.keys() else None
            c["phone_number"] = _input["phone_number"] if "phone_number" in _input.keys() else None
            c["credit_card_number"] = _input["credit_card_number"] if "credit_card_number" in _input.keys() else None
            repo.update_by_id(Customers, Customers.id, id, c)
    return jsonify(c)


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customer():
    customers = convert_to_json(repo.get_all(Customers))
    if request.method == 'GET':
        print(request.args.to_dict())
        search_args = request.args.to_dict()
        if len(search_args) == 0: jsonify(customers)
        results = []
        for c in customers:
            if "first_name" in search_args.keys() and c["first_name"].find(search_args["first_name"]) < 0: continue
            if "last_name" in search_args.keys() and c["last_name"].find(search_args["last_name"]) < 0: continue
            if "address" in search_args.keys() and c["address"].find(search_args["address"]) < 0: continue
            if "phone_number" in search_args.keys() and c["phone_number"].find(search_args["phone_number"]) < 0: continue
            if "credit_card_number" in search_args.keys() and c["credit_card_number"].find(search_args["credit_card_number"]) < 0: continue
            results.append(c)
        if len(results) == 0: return '{}'
        return jsonify(results)
    if request.method == 'POST':
        new_customer = request.get_json()
        print(new_customer)
        return add_customer_user(new_customer)


@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@cross_origin()
def get_customer_by_id(id):
    customers = convert_to_json(repo.get_all(Customers))
    if request.method == 'GET':
        for c in customers:
            if c["id"] == id: return jsonify(c)
        return "{}"
    if request.method == 'PUT':
        updated_new_customer = request.get_json()
        if repo.get_by_id(Customers, id) != None: return update_customer(updated_new_customer, id)
        return add_customer_user(updated_new_customer)
    if request.method == 'PATCH':
        updated_customer = request.get_json()
        if repo.get_by_id(Customers, id) != None: return update_customer(updated_customer, id)
        return '{}'
    if request.method == 'DELETE':
        deleted_customer = request.get_json()
        for c in customers:
            if c["id"] == id:
                repo.delete_by_id(Customers, Customers.id, id)
                repo.delete_by_id(Users, Users.id, c["user_id"])
                return f'{jsonify(deleted_customer)} deleted'
        return '{}'


if __name__ == "__main__":
    app.run(debug=True, port=5003)
