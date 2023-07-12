from flask import Blueprint, render_template,request,flash,redirect,url_for,jsonify
from flask_login import current_user
from flask_login import login_required
from project import db,app
import datetime
from functools import wraps
from flask_login import login_user, login_required, logout_user
from werkzeug.datastructures import ImmutableMultiDict
from sqlalchemy import delete
import json
from .models import Parameter 


    

parameters_bp = Blueprint('parameters', __name__,template_folder='templates')

@parameters_bp.route('/parameters', methods=['GET', 'POST'])
@login_required
def parameters():
    if request.method=='GET':
        
        typeLabel=request.args['typeLabel']
        print(type)
        list_parameters=Parameter.query.filter_by(typeLabel=typeLabel).all()
        return render_template('parameters.html', title=typeLabel,listItems=list_parameters,)




@parameters_bp.route('/parameters_get', methods=['GET', 'POST'])
@login_required
def parameters_get():
    list_parameters=Parameter.query.filter_by().all()
    return jsonify(list_parameters)



@parameters_bp.route('/parameters_add', methods=['GET', 'POST'])
def parameters_add():
    if request.method == 'POST':
        typeParam = request.form['type']
        labelParam = request.form['label']
        idTypeLabel=typeParam.strip()+'_'+labelParam.strip()
        ExistingIem=Parameter.query.filter_by(idTypeLabel=idTypeLabel).first()
        print(request.form.__dict__)
        if ExistingIem:
            msg = 'ERROR - existing parameter' 
        else:        
            newParameter=Parameter(type=typeParam,label=labelParam)
            db.session.add(newParameter)
            db.session.commit()
            
            msg = 'New record created successfully'  
    return jsonify(msg)


@parameters_bp.route("/ajax_update",methods=["POST","GET"])
def ajax_update():
    msg='update'
    param=json.loads(request.get_data())
    
    ExistingIem=Parameter.query.filter_by(id=param['id']).first()
    if ExistingIem:
        ExistingIem.label=param['label']
    else:
        newParameter=Parameter(typeLabel=param['typeLabel'],label=param['label'])
        db.session.add(newParameter)
    db.session.commit()
    return jsonify(msg)    




  
@parameters_bp.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():
    msg = 'Record deleted successfully'  
    return jsonify(msg) 