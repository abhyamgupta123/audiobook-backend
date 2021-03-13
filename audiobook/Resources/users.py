import os
import datetime
import uuid
from flask_restful import Resource, reqparse, request
from flask import Response, render_template
from flask_jwt_extended import (create_access_token, decode_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, jwt_optional)
from audiobook import db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from audiobook import limiter


class UserRegistration(Resource):
    # decorators = [limiter.limit("8/second")]
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'This field cannot be blank and must be unique', required = True)
        parser.add_argument('first_name', help = 'This field cannot be blank', required = True)
        parser.add_argument('last_name', help = 'This field cannot be blank', required = True)
        parser.add_argument('email', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        parser.add_argument('phone_number', help = 'This field can be blank', required = False)

        # parsing data
        data = parser.parse_args()
        username = data['username'].lower()
        email = data['email'].lower()
        password = data['password']
        fname = data['first_name']
        lname = data['last_name']
        phone_number = data.get('phone_number', None)

        # verifying credentials
        # checking username
        if ((username.isalnum() == False)) :
            return  Response("{'message': 'please enter unique valid username'}", status=402, mimetype='application/json')

        # checking valid phone number and present
        if (phone_number != None):
            if ((phone_number.isnumeric() == False) or int(phone_number) < 6000000000 or int(phone_number) > 9999999999):
                return  Response("{'message': 'please enter correct and valid phone number'}", status=402, mimetype='application/json')
            else:
                phone_number = int(phone_number)

        # checking if user is already present in database
        if(db.users.find_one({'email': email}) or db.users.find_one({'username' : username})):
            return Response("{'message': 'username or email already exists'}", status=402, mimetype='application/json')

        # checking if email is valid
        if ("@" not in email):
            return Response("{'message': 'please enter your valid email address'}", status=402, mimetype='application/json')

        User = {'username': username,
                'first_name': fname,
                'last_name': lname,
                'email': email,
                'password': password,
                'phone': phone_number,
                'isactive':false
                }

        try:
            db.Users.insert_one(User)
        except:
            return Response("{'message': 'Some error occured while registering the user'}", status=402, mimetype='application/json')
        else:
            return Response("{'message': 'User registered successfully'}", status=200, mimetype='application/json')


class UserLogin(Resource):
    # decorators = [limiter.limit("5/second")]
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)

        # parsing data
        data = parser.parse_args()
        try:
            if('@' in data['id']):
                user = db.Users.find_one({'email': data['id'].lower() })
            else:
                user = db.Users.find_one({'username': data['id'].lower() })
            # print(user)
        except:
            return Response("{'message': 'Some unexpected error occured while logging'}", status=403, mimetype='application/json')

        # chcking if user is present in database
        if(user):
            if(user['password'] == data['password'] and user.get('isactive', False)):
                access_token = create_access_token(identity = user['username'])
                refresh_token = create_refresh_token(identity = user['username'])
                return {'message': 'Logging in User {}'.format(user['username']),
                'name': user['first_name'],
                'username': user['username'],
                'access_token': access_token
                }
            else:
                if not (user.get('isactive', False)):
                    return Response("{'message': 'Please verify your account'}", status=402, mimetype='application/json')
                else:
                    return Response("{'message': 'Please enter valid password'}", status=402, mimetype='application/json')
        else:
            return Response("{'message': 'User does not exists'}", status=403, mimetype='application/json')
