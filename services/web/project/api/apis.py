from flask import Blueprint, render_template,request,flash,redirect,url_for,render_template_string,Response
from flask_login import current_user
from flask_login import login_required
from project import db,app
import datetime
from functools import wraps
from flask_login import login_user, login_required, logout_user
import json
from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from ..users.models import User 
from ..clients.models import Client,Orga
from ..parameters.models import Parameter
from ..accounts.models import Account
from ..movements.models import CashMovement
import pandas as pd
from datetime import timedelta



apis_bp = Blueprint('apis', __name__,template_folder='templates')

def dict_helper(objlist):
    result2 = [item.obj_to_dict() for item in objlist]
    return result2


@apis_bp.route('/api/users', methods=['GET', 'POST'])
@login_required
def get_users():
    listUsers = User.query.all()
    users = [user.__dict__ for user in listUsers]
    for user in users:
        del user['_sa_instance_state']
    return jsonify(users)


@apis_bp.route('/api/setusers', methods=['GET','POST'])
def set_users():
    if (request.method == 'POST'):
        listUsers = json.loads(request.get_json())
        for oneUser in listUsers:
            new_user = User(**oneUser)
            db.session.add(new_user)
            
        db.session.commit()
        response = app.response_class(status=200)
        return response

    return render_template_string('methode POST uniquement')



@apis_bp.route('/api/setclients', methods=['GET','POST'])
def set_clients():
    if (request.method == 'POST'):
        listClients = json.loads(request.get_json())
        res={}
        for oneClient in listClients:
            new_client = Client(**oneClient)
            db.session.add(new_client)
            
        db.session.commit()
        response = app.response_class(response=jsonify(res),
                                status=200,
                                mimetype='application/json')
        return response

    return render_template_string('methode POST uniquement')


@apis_bp.route('/api/setorgas', methods=['GET','POST'])
def set_orgas():
    if (request.method == 'POST'):
        listOrgas = json.loads(request.get_json())
        res={}
        for oneOrga in listOrgas:
            print('pfff',oneOrga)
            #try:
            new_orga = Orga(**oneOrga)
            db.session.add(new_orga)
            #except Exception as e:
                #res[str(oneOrga)] = str(e)
            
        db.session.commit()
        response = app.response_class(status=200)
        return response

    return render_template_string('Method POST only')




#API to add structured parameters
@apis_bp.route('/api/setparameters', methods=['POST'])
def set_parameters():
    if (request.method == 'POST'):
        Parameter.query.delete()
        listParameters = json.loads(request.get_json())
        for parameter in listParameters:
            print(parameter)
            new_parameter = Parameter(**parameter)
            print(new_parameter.label, new_parameter.typeLabel)
            db.session.add(new_parameter)  
        db.session.commit()
        response = app.response_class(status=200)
        return response
    return render_template_string('methode POST uniquement')



@app.route('/api/cash_movements', methods=['POST'])
def create_cash_movement():
    data = json.loads(request.get_json())
    # Expecting a list of cash movements
    if isinstance(data, list):
        cash_movements = []
        for item in data:
            cash_movement = CashMovement(**item)
            
            #try:
            db.session.add(cash_movement)
            db.session.commit()
            cash_movement.createProcess()
            cash_movement.validateAuto()
            #cash_movements.append(cash_movement)

            #except IntegrityError:
                #db.session.rollback()
        response = app.response_class(status=200)
        return response

    return jsonify({'error': 'Invalid request'}), 400




@apis_bp.route('/api/setaccounts', methods=['POST'])
def set_accounts():
    if request.method == 'POST':
        account_list = json.loads(request.get_json())
        for account_data in account_list:
            account = Account.query.filter_by(key=account_data['key']).first()

            if account:
                # account exists, update it
                try:    
                    print('account_data',account_data)
                    account.update(account_data)
                except ValueError as ve:
                    return jsonify({"error": str(ve)}), 400
            else:
                # account does not exist, create it
                try:
                    new_account = Account(**account_data)
                    db.session.add(new_account)
                except ValueError as ve:
                    return jsonify({"error": str(ve)}), 400
                    
        db.session.commit()
        response = app.response_class(status=200)
        return response
        




