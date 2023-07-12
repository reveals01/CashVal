from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user
from flask_login import login_required
from project import db,app
import datetime
from functools import wraps
from flask_login import login_required, logout_user
from werkzeug.datastructures import ImmutableMultiDict
from sqlalchemy import delete

from .models import Client 
from .forms import newClientForm 

clients_bp = Blueprint('clients', __name__,template_folder='templates')


@clients_bp.route('/clients',methods=('GET', 'POST'))
@login_required
def clients():
    if (request.method == 'POST') & (request.form.get('fname') in ['Delete']):
        idClient=request.form.get('idClient')
        Client.query.filter(Client.id == idClient).delete()
        db.session.commit()
        flash('Client supprimé',category='error')
        return redirect(url_for('clients.clients'))

    listClients = Client.query.all()
    return render_template('clients.html',listClients=listClients,navActive='clients')
        

@clients_bp.route('/client',methods=('GET', 'POST'))
@login_required
def client():
    form = newClientForm(request.form, csrf_enabled=False)
    clientList=Client.query.filter_by().all()

    if (request.method == 'POST') & (request.form.get('fname') in ['clientModify']) :
        theClient=Client.query.filter_by(id=form.id.data).first()  
        idClientSelected=theClient.id
        if form.validate_on_submit():
            theClient.update(form.data)
            flash('Client modifié',)
            return redirect(url_for('clients.clients'))
        

    if (request.method == 'POST') & (request.form.get('fname') in ['Edit','clientSelect']) :
        oneClient=Client.query.filter_by(id=request.form.get('idClient')).first()
        data=oneClient.__dict__
        data['typeForm']='MODIFY'
        form = newClientForm(data=data,csrf_enabled=False)   
        idClientSelected=oneClient.id
        print('idClientSelected',idClientSelected)
        return render_template('client.html',form=form,navActive='client',clientList=clientList,idClientSelected=idClientSelected)


    if (request.method != 'POST'):
        oneClient=Client.query.filter_by().first()
        data=oneClient.__dict__
        data['typeForm']='MODIFY'
        form = newClientForm(data=data,csrf_enabled=False) 
        idClientSelected=oneClient.id

    return render_template('client.html',form=form,navActive='client',clientList=clientList,idClientSelected=idClientSelected)





@clients_bp.route('/newClient', methods=["GET", "POST"])
@login_required
def newClient():
    form = newClientForm(request.form, csrf_enabled=False,typeForm='MOD')
    if form.validate_on_submit():
        new_client = Client(**form.data)
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('clients.clients'))
    return render_template('newClient.html', form=form,navActive='newClient')
