import datetime
import os
import jwt
import re
from api import secret_key
from validate_email import validate_email
from flask import jsonify, request, json, Response, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from api.model.orders import Orders
from api import conn

def check_empty_list(check_list, order_id):
    """
    function to check whether a list is empty
    """
    if not check_list:
        return jsonify({'message':'No Order Found with specified Id ' + str(order_id)}),200
    return jsonify({'order':check_list[0]}),200

def  check_if_no_user_orders(order_list, user_id):
    """
    function to check whether there are orders for a specific user
    """
    if not order_list:
        message = 'No User Orders Found with specified User Id  ' + str(user_id)
        return jsonify({'message':message}),200
    return jsonify({'specific_user_orders':[order for order in order_list]}),200

def check_if_there_no_orders(all_orders_list):
    """
    function to check if there are no orders
    """
    
    if not all_orders_list:
        return jsonify({'message':'No Orders Found!!!'}),200
    return jsonify({'all_orders':[order.__dict__ for order in all_orders_list]}),200

def check_order_object_keys(order_object):
    """
    function to check for keys in users posted order object
    """
    if ('order_name' in order_object and 'parcel_weight' in order_object and 'parcel_destination_address' 
    in order_object and 'receivers_names' in order_object and 'receivers_contact'):
        return True
    return False

def check_user_object_keys(user_object):
    """
    function to check for keys in users posted order object
    """
    if ('first_name' in user_object
    and 'last_name' in user_object and 'email' in user_object
    and 'phone_contact' in user_object and 'username' 
    in user_object and 'user_password' in user_object):
        return True
    return False


# def check_if_posted_user_data_are_not_empty_strings():
#     """
#     function to check whether posted object has got no empty strings
#     """
#     return (request.json['first_name'] != '' and request.json['last_name'] != ''
#     and request.json['email'] != '' and request.json['contact'] != ''
#     and request.json['username'] != '' and  
#     request.json['password'] != '' and request.json['user_type'] != '' )


def validating_email(user_email):
    """
    function to validate email of the user
    """
    return (validate_email(user_email))

def check_if_posted_user_data_are_strings(new_user_data):
    """
    function to check whether posted object string properties strings
    """
    if(isinstance(new_user_data['first_name'], str) and isinstance(new_user_data['last_name'], str)
    and isinstance(new_user_data['email'], str)  and 
    isinstance(new_user_data['phone_contact'],str) 
    and isinstance(new_user_data['username'], str) 
    and isinstance(new_user_data['user_password'], str)):
        return True
    return False

def check_if_posted_data_are_not_empty_strings():
    """
    function to check whether posted object has got no empty strings
    """
    return (request.json['order_name'] != '' and request.json['senders_names'] != ''
    and request.json['senders_contact'] != '' and request.json['parcel_pickup_address'] != ''
    and request.json['parcel_destination_address'] != '' and  
    request.json['receivers_names'] != '' and request.json['receivers_contact'] != '' )

def check_if_posted_data_are_strings(*args):
    """
    function to check whether posted object string properties strings
    """
    return (isinstance(request.json[args[0]], str) and isinstance(request.json[args[1]], str)
    and isinstance(request.json[args[2]], str)  and isinstance(request.json[args[3]],str) 
    and isinstance(request.json[args[4]], str) and isinstance(request.json[args[5]], str) 
    and isinstance(request.json[args[6]], str))

def check_if_posted_order_status_is_string():
    """
    function to check whether update order status object is a string
    """
    return (isinstance(request.json['order_status'], str))

def check_if_posted_order_status_is_not_empty_string():
    """
    function to check whether a user status string is empty
    """
    return (request.json['order_status'] != '')


def check_if_parcel_weight_is_an_integer():
    """
    function to check whether the parcel_weight and user_id are integers
    """
    return (isinstance(request.json['parcel_weight'], int) )

def check_for_empty_strings_in_reg_object(*args):
    """
    function to check whether posted object has got no empty strings
    """
    if (request.json[args[0]] != '' and request.json[args[1]] != ''
    and request.json[args[2]] != '' and request.json[args[3]] != ''
    and request.json[args[4]] != '' and  
    request.json[args[5]] != ''):
        return True
    return False


# def validate_posted_data(posted_order, orders_list, user_id):
#     """
#     function to validate user posted order object
#     """
#     if (check_order_object_keys(posted_order) and check_if_posted_data_are_not_empty_strings() 
#     and check_if_parcel_weight_is_an_integer() and check_if_posted_data_are_strings('order_name', 'senders_names', 
#     'senders_contact', 'parcel_pickup_address', 'parcel_destination_address', 'receivers_names', 'receivers_contact'
#     )):
#         get_todays_date = datetime.datetime.now()
#         order_status = 'pending'
#         price_to_be_paid = request.json['parcel_weight'] * 30000
#         order = Orders(
#             user_id, len(orders_list) + 1, request.json['order_name'],
#             request.json['senders_names'], request.json['senders_contact'], 
#             request.json['parcel_pickup_address'], request.json['parcel_destination_address'], 
#             request.json['receivers_names'], request.json['receivers_contact'], 
#             request.json['parcel_weight'], price_to_be_paid, get_todays_date, order_status
#         )
#         orders_list.append(order)
#         return jsonify(order.__dict__),201
#     parcel_order_object = "{'order_name': 'phones','parcel_destination_address': 'Mpigi','parcel_pickup_address': 'Kamwokya','parcel_weight': 6,\
#     'receivers_contact': '070786543','receivers_names': 'Bagzie','senders_contact': '0700978789','senders_names': 'Namyalo Agnes','user_id': 4}"
#     bad_order_object = {
#     "error": "Bad Order Object",
#     "help of the correct order object format":parcel_order_object
#     }
#     response = Response(
#         json.dumps(bad_order_object),
#         status=400, mimetype="application/json"
#         )
#     return response

# def validate_posted_user_data(register_user_object):
#     """
#     function to validate create new user object
#     """
#     if (check_for_keys_in_an_object('first_name', 'last_name', 'email', 
#     'phone_contact', 'username', 'user_password') 
#     and check_if_posted_user_data_are_strings() and 
#     check_user_object_keys(register_user_object)):
#         if (validating_email(request.json['email'])):
#             return True      
#         return jsonify({'message':'Invalid email'}),400
#     user_posted_object = "{'first_name': 'julius','last_name': 'kasagala','email': 'jk@gmail.com',\
#     'contact': '070786543','username': 'kas1234','password': 'kas@123','user_type': 'user'}"
#     bad_order_object = {
#     "error": "Bad Order Object",
#     "help of the correct order object format":user_posted_object
#     }
#     response = Response(
#         json.dumps(bad_order_object),
#         status=400, mimetype="application/json"
#         )
#     return response

def user_auth_logic(user_list, error_message):
        user_password = request.json['password']
        user_username = request.json['username']
        return refactor_auth_logic(user_list, user_password, user_username)
        

def refactor_auth_logic(user_list, user_password, user_username):
    for user in user_list:
        if user_username == user.__dict__['username']:
            return generate_token_logic(user, user_password, user_username)
    return jsonify({"message":"Wrong Username or Password!!"}),401

def generate_token_logic(user, user_password, user_username):
    if check_password_hash(user.__dict__['password'], user_password):
        token = jwt.encode({'username':user_username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},secret_key,  algorithm='HS256')
        return jsonify({'token_generated':token.decode('UTF-8')}),200
    return jsonify({"message":"Wrong Username or Password!!"}),401