import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
# allow cross-domain access to all the server routes from any other domain
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES

# public endpoint to handle GET requests for all available drinks
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    if not drinks:
        abort(404)
    drinks_short = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drinks_short
    })


# private endpoint to handle GET requests for all drinks details
@requires_auth('get:drinks-detail')
@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():
    drinks = Drink.query.all()
    if not drinks:
        abort(404)
    drinks_long = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drinks_long
    })


# private endpoint to handle POST requests to add a new drink
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    body = request.get_json()
    req_title = body.get('title')
    req_recipe = json.dumps(body['recipe'])
    try:
        drink = Drink(title=req_title, recipe=req_recipe)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# ERROR HANDLING


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
