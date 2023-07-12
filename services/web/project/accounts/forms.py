from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from ..clients.models import Client
from ..users.models import User

class newAccountForm(FlaskForm):
    id = HiddenField('id')

    key = StringField('Key',
                      validators=[DataRequired(), Length(min=3, max=100)],
                      render_kw={"placeholder": "Account Key", "class": "form-control", "size": 32})
    description = StringField('Description',
                              validators=[Length(max=500)],
                              render_kw={"placeholder": "Description", "class": "form-control", "size": 32})
    balance = StringField('Balance',
                          validators=[DataRequired(), Length(min=1, max=50)],
                          render_kw={"placeholder": "Account Balance", "class": "form-control", "size": 32})
    clientId = SelectField('Client',
                           coerce=int,
                           validators=[DataRequired()],
                           render_kw={"class": "form-select","label":"Client"})
    
    officerId = SelectField('Officer', 
                            coerce=int, 
                            validators=[DataRequired()], 
                            render_kw={"class": "form-select ","label":"Officer"})
                            
    validatorId = SelectField('Senior Officer', 
                              coerce=int, 
                              validators=[DataRequired()], 
                              render_kw={"class": "form-select ","label":"Senior Officer"})

    
    
    typeForm = 'NEW'
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(newAccountForm, self).__init__(*args, **kwargs)
        try:
            self.typeForm = kwargs['typeForm']
        except KeyError:
            pass

        # Query the database for all clients
        clients = Client.query.all()

        # Create a list of tuples for each client
        client_choices = [(client.id, client.key) for client in clients]

        # Set the choices for the clientId field
        self.clientId.choices = client_choices

        # Query the database for all officers and senior officers
        officers = User.query.filter(User.role == 'Officer').all()
        senior_officers = User.query.filter(User.role == 'Senior Officer').all()

        # Create a list of tuples for each officer and senior officer
        officer_choices = [(officer.id, officer.name) for officer in officers]
        senior_officer_choices = [(so.id, so.name) for so in senior_officers]

        # Set the choices for the officerId and validatorId field
        self.officerId.choices = officer_choices
        self.validatorId.choices = senior_officer_choices

