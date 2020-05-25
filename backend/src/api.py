import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


# DELETE TABLE AND CREATE NEW ONE
# db_drop_and_create_all()


# ROUTES


# GET DRINKS ENDPOINT
@app.route('/drinks')
def drinks():
    try:
        drinks = Drink.query.all()
        print(f' drinks = {len(drinks)}')
        drinks_shortter = [drink.short() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': drinks_shortter
        })
    except Exception as exp:
        print(f' Some error ocurred with get = {exp}')
        abort(400)


# GET DRINK DETAIL , PERMISSION: get:drinks:detail
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drink_details(jwt):
    try:
        drinks = Drink.query.all()
        format_drink = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': format_drink
        })
    except Exception as exp:
        print(f' Some error ocurred on drink details = {exp} ❌')
        abort(404)


# POST NEW DRINK, PERMISSIONS : POST:DRINKS
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    try:
        body = request.get_json()
        title = body.get('title', None)
        receipt = json.dumps(body.get("recipe"))
        drink = Drink(title=title, recipe=receipt)
        drink.insert()
        long_drink = drink.long()
        print(f' Got this token = {jwt} 🔦  ')
        return jsonify({
            'success': True,
            'drinks': long_drink
        }), 200
    except Exception as exp:
        print(f' Some error ocurred - {exp} ❌')
        abort(400)


# UPDATE DRINK, PERMISSION:PATCH:DRINKS
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):
    try:
        body = request.get_json()
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        # Get title
        drink.title = body.get('title', None)

        # Keep old data if user not update recipe
        recipe = body.get('recipe', None)
        if recipe is not None:
            drink.recipe = json.dumps(body.get('recipe', drink.recipe))

        drink.update()

        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 200
    except Exception as exp:
        print(f' Some error ocurred with patch = {exp} ')
        abort(400)


# DELETE DRINK BY ID, PERMISSION:DELETE:DRINKS
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, drink_id):

    try:

        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify({"success": True, "delete": drink_id}), 200
    except Exception as exp:
        print(f' Some error occurred in delete = {exp} ❌')


# UNPROCCESABLE ENTITY ERROR HANDLER
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# NOT FOUND ERROR HANDLER
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


# AUTHError handler
@app.errorhandler(AuthError)
def auth_error_handler(AuthError):
    return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": AuthError.get_error_message()
    }), 401
