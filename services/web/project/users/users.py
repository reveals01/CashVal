from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user
from flask_login import login_required
from project import db,app
import datetime
from functools import wraps
from flask_login import login_user, login_required, logout_user
from werkzeug.datastructures import ImmutableMultiDict
from sqlalchemy import delete

from .models import User 
from .forms import newUserForm,LoginForm


    

users_bp = Blueprint('users', __name__,template_folder='templates')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form._fields)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        return redirect(url_for('users.user'))
        
    return render_template('login.html', title='Sign In', form=form)


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


##@users_bp.route('/signup', methods=["GET", "POST"])
#def signup():
#    form = newUserForm(request.form, csrf_enabled=False)
#    if form.validate_on_submit():
#        new_user = User(form.data)
#        db.session.add(new_user)
#        #db.session.commit()
#
#        return redirect(url_for('users.login'))
#    return render_template('signup.html', form=form)



@users_bp.route('/users',methods=('GET', 'POST'))
@login_required
def users():
    if (request.method == 'POST') & (request.form.get('fname') in ['Delete']):
        idUser=request.form.get('idUser')
        User.query.filter(User.id == idUser).delete()
        db.session.commit()
        flash('Utilisateur supprimé',category='error')
        return redirect(url_for('users.users'))

    listUsers = User.query.all()
    return render_template('users.html',listUsers=listUsers,navActive='users')
        

@users_bp.route('/user',methods=('GET', 'POST'))
@login_required
def user():
    form = newUserForm(request.form, csrf_enabled=False)
    usrList=User.query.filter_by().all()

    if (request.method == 'POST') & (request.form.get('fname') in ['userModify']) :
        theUser=User.query.filter_by(id=form.id.data).first()  
        idUserSelected=theUser.id
        if form.validate_on_submit():
            theUser.update(form.data)
            flash('Utilisateur modifié',)
            return redirect(url_for('users.users'))
        

    if (request.method == 'POST') & (request.form.get('fname') in ['Edit','userSelect']) :
        oneUser=User.query.filter_by(id=request.form.get('idUser')).first()
        data=oneUser.__dict__
        data['typeForm']='MODIFY'
        form = newUserForm(data=data,csrf_enabled=False)   
        idUserSelected=oneUser.id
        print('idUserSelected',idUserSelected)
        return render_template('user.html',form=form,navActive='user',usrList=usrList,idUserSelected=idUserSelected)


    if (request.method != 'POST'):
        oneUser=User.query.filter_by().first()
        data=oneUser.__dict__
        data['typeForm']='MODIFY'
        form = newUserForm(data=data,csrf_enabled=False) 
        idUserSelected=oneUser.id

    
    return render_template('user.html',form=form,navActive='user',usrList=usrList,idUserSelected=idUserSelected)





@users_bp.route('/newUser', methods=["GET", "POST"])
@login_required
def newUser():
    form = newUserForm(request.form, csrf_enabled=False,typeForm='MOD')
    if form.validate_on_submit():
        new_user = User(**form.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users.users'))
    return render_template('newUser.html', form=form,navActive='newUser')