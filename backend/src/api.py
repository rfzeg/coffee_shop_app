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
    req_recipe = body.get('recipe', None)
    try:
        drink = Drink(title=req_title, recipe=json.dumps([req_recipe]))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(422)


# private endpoint to update an existing drink
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def modify_drinks(payload, drink_id):

    drink = Drink.query.get(drink_id)
    if drink is None:
        return json.dumps({
        'success': False,
        'error': 'Drink #' + drink_id + ' not found'
    }), 404

    body = request.get_json()
    title = body.get('title')
    recipe = body.get('recipe', None)

    if title:
        drink.title = title
    if recipe:
        drink.recipe = json.dumps([recipe])
    drink.update()

    return {'drinks': [drink.long()], 'success': True}, 200


# private endpoint to delete an existing drink
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):

    drink = Drink.query.get(drink_id)

    if drink is None:
        print('An error occured, drink with id: ' + str(drink_id) + ' could not be found!')
        abort(404)

    drink.delete()

    return jsonify({'success': True, 'deleted': drink_id})


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
