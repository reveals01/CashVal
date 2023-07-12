from flask_wtf import FlaskForm
from wtforms import Form,StringField, PasswordField, BooleanField, SubmitField,SelectField,HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from .models import User

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



class newUserForm(FlaskForm):
    id = HiddenField('id')

    name = StringField('Name',
            validators=[DataRequired(), Length(min=3, max=32)],render_kw={"placeholder": "Your name","class":"form-control", "size":32})
    surname = StringField('Surname',
            validators=[DataRequired(), Length(min=3, max=32)],render_kw={"placeholder": "Your surname","class":"form-control", "size":32})
    email = StringField('Email',
            validators=[DataRequired(), Email(), Length(min=6, max=40)],render_kw={"placeholder": "Your email","class":"form-control", "size":32})
    
    role=SelectField('Role',validators=[DataRequired()],render_kw={"placeholder": "Your role",'class':'form-select'},
                     choices=[("ADMIN","ADMIN"),("RISK","RISK"),("FRONT","FRONT")])

    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=4, max=64)],render_kw={"placeholder": "Your password","class":"form-control", "size":32})
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')],render_kw={"placeholder": "Confirm password","class":"form-control", "size":32})
    submit = SubmitField('Register')
    typeForm='NEW'

    def __init__(self, *args, **kwargs):
        super(newUserForm, self).__init__(*args, **kwargs)
        try:
            self.typeForm=kwargs['typeForm']
        except:
            pass
        print(self.typeForm)

