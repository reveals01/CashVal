from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user, login_required
from project import db,app
from .models import Account 
from .forms import newAccountForm 

accounts_bp = Blueprint('accounts', __name__,template_folder='templates')

@accounts_bp.route('/accounts',methods=('GET', 'POST'))
@login_required
def accounts():
    if (request.method == 'POST') & (request.form.get('fname') in ['Delete']):
        idAccount=request.form.get('idAccount')
        Account.query.filter(Account.id == idAccount).delete()
        db.session.commit()
        flash('Account deleted',category='error')
        return redirect(url_for('accounts.accounts'))
    listAccounts = Account.query.filter_by().all()
    print('listAccounts',listAccounts)
    search_param = request.args.get('client', '')
    return render_template('accounts.html',listAccounts=listAccounts,navActive='accounts',selected=search_param)



@accounts_bp.route('/account',methods=('GET', 'POST'))
@login_required
def account():
    print('coucou')
    form = newAccountForm(request.form, csrf_enabled=False)
    accountList=Account.query.filter_by().all()
    if (request.method == 'POST') & (request.form.get('fname') in ['accountModify']) :
        theAccount=Account.query.filter_by(id=form.id.data).first()  
        idAccountSelected=theAccount.id
        if form.validate_on_submit():
            theAccount.update(form.data)
            flash('Account updated',)
            return redirect(url_for('accounts.accounts'))

    if (request.method == 'POST') & (request.form.get('fname') in ['Edit','accountSelect']) :
        oneAccount=Account.query.filter_by(id=request.form.get('idAccount')).first()
        data=oneAccount.__dict__
        data['typeForm']='MODIFY'
        form = newAccountForm(data=data,csrf_enabled=False)   
        idAccountSelected=oneAccount.id
        return render_template('account.html',form=form,navActive='account',accountList=accountList,idAccountSelected=idAccountSelected)

    if (request.method != 'POST'):
        oneAccount=Account.query.filter_by().first()
        data=oneAccount.__dict__
        data['typeForm']='MODIFY'
        form = newAccountForm(data=data,csrf_enabled=False) 
        idAccountSelected=oneAccount.id

    return render_template('account.html',form=form,navActive='account',accountList=accountList,idAccountSelected=idAccountSelected)


@accounts_bp.route('/newAccount', methods=["GET", "POST"])
@login_required
def newAccount():
    form = newAccountForm(request.form, csrf_enabled=False,typeForm='MOD')
    if form.validate_on_submit():
        new_account = Account(**form.data)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('accounts.accounts'))
    return render_template('newAccount.html', form=form,navActive='newAccount')
