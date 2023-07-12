from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..users.models import User
from flask_login import login_user, login_required, logout_user
from .forms import LoginForm,RegisterForm

from .. import db

auth = Blueprint('auth', __name__,template_folder='templates')






@auth.route('/login2', methods=['GET', 'POST'])
def login2():
    form = LoginForm()
    print(form._fields)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        return redirect(url_for('users.user'))
        
    return render_template('login2.html', title='Sign In', form=form)


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                name=form.name.data,
                surname=form.surname.data,
                password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login2'))
    return render_template('register.html', form=form)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user :
        flash('User not defined. Please sign-in.')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Wrong password. Please try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('users.user'))



#@auth.route('/signup')
#def signup():
#    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Echec. Adresse email déjà existante')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    #if (new_user.id == 1):


    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    flash('Utilisateur créé')

    return redirect(url_for('auth.signup'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))