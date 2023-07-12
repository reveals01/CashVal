from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required
from project import db
from .models import CashMovement 
#from .forms import newMovementForm 
from ..clients.models import Client
from ..users.models import Process,User
from ..accounts.models import Account
from sqlalchemy import func
import json


movements_bp = Blueprint('movements', __name__,template_folder='templates')

@movements_bp.route('/movements',methods=('GET', 'POST'))
@login_required
def movements():
    if (request.method == 'POST') & (request.form.get('fname') in ['Delete']):
        idMovement=request.form.get('idMovement')
        CashMovement.query.filter(CashMovement.id == idMovement).delete()
        db.session.commit()
        flash('Movement deleted',category='error')
        return redirect(url_for('movements.movements'))

    listMovements = CashMovement.query.all()
    return render_template('movements.html',listMovements=listMovements,navActive='movements')

@movements_bp.route('/get-businesses')
def get_businesses():
    businesses = Client.query.with_entities(Client.business).distinct().all()
    businesses = [business[0] for business in businesses]
    print('businesses',businesses)
    return jsonify(businesses=businesses)

'''
@movements_bp.route('/movement',methods=('GET', 'POST'))
@login_required
def movement():
    form = newMovementForm(request.form, csrf_enabled=False)
    movementList=CashMovement.query.filter_by().all()

    if (request.method == 'POST') & (request.form.get('fname') in ['movementModify']):
        theMovement=CashMovement.query.filter_by(id=form.id.data).first()  
        idMovementSelected=theMovement.id
        if form.validate_on_submit():
            theMovement.update(form.data)
            flash('Movement modified',)
            return redirect(url_for('movements.movements'))

    if (request.method == 'POST') & (request.form.get('fname') in ['Edit','movementSelect']) :
        oneMovement=CashMovement.query.filter_by(id=request.form.get('idMovement')).first()
        data=oneMovement.__dict__
        data['typeForm']='MODIFY'
        form = newMovementForm(data=data,csrf_enabled=False)   
        idMovementSelected=oneMovement.id
        return render_template('movement.html',form=form,navActive='movement',movementList=movementList,idMovementSelected=idMovementSelected)

    if (request.method != 'POST'):
        oneMovement=CashMovement.query.filter_by().first()
        data=oneMovement.__dict__
        data['typeForm']='MODIFY'
        form = newMovementForm(data=data,csrf_enabled=False) 
        idMovementSelected=oneMovement.id

    return render_template('movement.html',form=form,navActive='movement',movementList=movementList,idMovementSelected=idMovementSelected)
'''


@movements_bp.route('/dashboard2')
def dashboard2():
    # Calculate total number of movements
    totalMovements = db.session.query(Process.id).count()

    # Calculate counts of each status
    statuses = db.session.query(Process.statusLabel).distinct().all()
    statuses = [status[0] for status in statuses]
    statusCounts = db.session.query(Process.statusLabel, func.count(Process.statusLabel)).group_by(Process.statusLabel).all()
    print('statusCounts',statusCounts)
    statusCounts = [count[1] for count in statusCounts]

    # Calculate the number of pending movements per nextUser
    nextUsers = db.session.query(User.name).join(Process, User.id == Process.nextUserId).all()
    nextUsers = [user[0] for user in nextUsers]
    pendingCounts = db.session.query(func.count(Process.id)).filter(Process.statusLabel == 'pending').group_by(Process.nextUserId).all()
    pendingCounts = [count[0] for count in pendingCounts]

    return render_template('dashboard.html', statusCounts=statusCounts, totalMovements=totalMovements, statuses=statuses, nextUsers=nextUsers, pendingCounts=pendingCounts)



@movements_bp.route('/dashboard')
def dashboard():
    # Retrieve all the current movements
    currentMovements = Process.query.filter_by(isCurrent=True).all()
    # Convert movements to a format that can be serialized to JSON
    currentMovementsData = [{'id': movement.id, 
                             'user': movement.user.key if movement.user is not None else "N/A", 
                             'statusLabel': movement.statusLabel,
                             'nextUser': movement.nextUser.key if movement.nextUser is not None else "N/A", 
                             'business': movement.cashmovement.account.client.business if movement.cashmovement.account.client is not None else "N/A",
                             'client': movement.cashmovement.account.client.key if movement.cashmovement.account.client is not None else "N/A"} 
                            for movement in currentMovements]
    return render_template('dashboard.html', allMovements=json.dumps(currentMovementsData))





@movements_bp.route('/udpateprocess', methods=['POST'])
def udpateprocess():
    print('prout' )
    # Get the form data
    form_data = json.loads(request.get_data())
    # Get the id of the movement
    print('movement',form_data)
    movement_id = form_data['movementId']
    
    # Get the status label
    status_label = form_data.get('status')
    # Query the movement with the given id
    movement = CashMovement.query.get(movement_id)
    print('movement',movement.id)
    if not movement:
        return jsonify({'message': f'Movement with ID {movement_id} not found'}), 404

    # Get the last process of this movement
    last_process = Process.query.filter_by(movementId=movement_id, isCurrent=True).first()

    # If there is a last process, set its isCurrent field to False
    if last_process:
        last_process.isCurrent = False

    # Create a new process instance
    kwargs = {'movementId': movement_id}
    new_process = Process(**kwargs)

    # Set the movementId of the new process
    new_process.movementId = movement_id

    # Set the statusLabel of the new process
    new_process.statusLabel = status_label

    # Check if the status is 'to be validated'
    if status_label == 'to be validated':
        # If yes, then set the nextUserId to be the validatorId of the client of the account of the movement
        new_process.nextUserId = movement.account.client.validatorId

    # Add the new process to the database session
    db.session.add(new_process)

    # Commit the session to save changes
    db.session.commit()

    return jsonify({'message': 'New process instance created successfully'}), 201




@movements_bp.route('/kpis', methods=['GET'])
def kpis():
    officer_id = request.args.get('officerId', None)
    validator_id = request.args.get('validatorId', None)
    bank_name = request.args.get('bankName', None)

    # Construct a database query based on the provided parameters
    query = db.session.query(Process)
    if officer_id is not None:
        query = query.filter(Process.userId == officer_id)
    if validator_id is not None:
        query = query.filter(Process.nextUserId == validator_id)
    if bank_name is not None:
        query = query.join(Process.cashmovement).join(CashMovement.account).filter(Account.bankName == bank_name)

    # Calculate the total movements
    total_movements = query.count()

    # Calculate the count of each status
    status_counts = db.session.query(Process.statusLabel, func.count(Process.statusLabel))\
        .group_by(Process.statusLabel).all()

    # Convert the result into a dictionary
    status_counts = {status: count for status, count in status_counts}

    nextUsers = db.session.query(User.name).join(Process, User.id == Process.nextUserId).all()
    nextUsers = [user[0] for user in nextUsers]
    pendingCounts = db.session.query(func.count(Process.id)).filter(Process.statusLabel == 'Pending').group_by(Process.nextUserId).all()
    pendingCounts = [count[0] for count in pendingCounts]

    return render_template('dashboard.html', statusCounts=statusCounts, totalMovements=totalMovements, statuses=statuses, nextUsers=nextUsers, pendingCounts=pendingCounts)


    # Combine the KPIs into a single dictionary
    kpis = {
        'totalMovements': total_movements,
        'statusCounts': status_counts
    }

    return render_template('dashboard.html', kpis=kpis)

