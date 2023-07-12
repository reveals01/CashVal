from flask_wtf import FlaskForm
from wtforms import Form,StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from ..users.models import User

#class LoginForm(FlaskForm):
#    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "Your email"})
#    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Your password"})
#    #remember_me = BooleanField('Remember Me')
#    submit = SubmitField('Log In')

class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "Your email"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Your password"})
    submit = SubmitField('Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self,extra_validators=None):
        
        initial_validation = super(LoginForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user :
            self.email.errors.append('Unknown email')
            return False
        
        if not user.verify_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False
        
        return True



class RegisterForm(FlaskForm):
    name = StringField('Name',
            validators=[DataRequired(), Length(min=3, max=32)],render_kw={"placeholder": "Your name","class":"form-control", "size":32})
    surname = StringField('Surname',
            validators=[DataRequired(), Length(min=3, max=32)],render_kw={"placeholder": "Your surname","class":"form-control", "size":32})
    email = StringField('Email',
            validators=[DataRequired(), Email(), Length(min=6, max=40)],render_kw={"placeholder": "Your email","class":"form-control", "size":32})
    
    role=SelectField('Role',validators=[DataRequired()],render_kw={"placeholder": "Your role",'class':'form-select'},
                     choices=[(1,"ADMIN"),(2,"RISK"),(3,"FRONT")])

    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=8, max=64)],render_kw={"placeholder": "Your password","class":"form-control", "size":32})
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')],render_kw={"placeholder": "Confirm password","class":"form-control", "size":32})
    submit = SubmitField('Register')


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def validate(self,extra_validators=None,type='NEW'):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(surname=self.surname.data,name=self.name.data).first()
        #if user:
            #self.surname.errors.append("Username already registered")
            #return False
        user = User.query.filter_by(email=self.email.data).first()
        if (type=="NEW"):
            if user :
                self.email.errors.append("Email already registered")
                return False
        return True