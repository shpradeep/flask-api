from app import app
from model.user_model import user_model
from flask import request, make_response

obj = user_model()

@app.route('/api/getall')
def user_getall_controller():
    return obj.user_getall_model()

@app.route('/api/getplan/<user_id>')
def user_getplan_controller(user_id):
    return obj.user_getplan_model(user_id)

@app.route('/api/adduser', methods=["POST"])
def user_addone_controller():
    return obj.user_addone_model(request.json)

@app.route('/api/update', methods=["PUT"])
def user_update_controller():
    return obj.user_update_model(request.json)

