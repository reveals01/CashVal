from flask_wtf import FlaskForm
from wtforms import Form,StringField, PasswordField, BooleanField, SubmitField,SelectField,HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length



class newClientForm(FlaskForm):
    id = HiddenField('id')

    key = StringField('Key',
            validators=[DataRequired(), Length(min=3, max=100)], render_kw={"placeholder": "Client Key", "class":"form-control", "size":32})
    description = StringField('Description',
            validators=[Length(max=500)], render_kw={"placeholder": "Description", "class":"form-control", "size":32})
    email = StringField('Email',
            validators=[DataRequired(), Email(), Length(min=6, max=100)], render_kw={"placeholder": "Client Email", "class":"form-control", "size":32})
    phone = StringField('Phone',
            validators=[DataRequired(), Length(min=3, max=50)], render_kw={"placeholder": "Client Phone", "class":"form-control", "size":32})
    country = StringField('Country',
            validators=[DataRequired(), Length(min=2, max=2)], render_kw={"placeholder": "Country (ISO 3166-1 alpha-2 code)", "class":"form-control", "size":2})
    submit = SubmitField('Register')
    typeForm = 'NEW'

    def __init__(self, *args, **kwargs):
        super(newClientForm, self).__init__(*args, **kwargs)
        try:
            self.typeForm = kwargs['typeForm']
        except:
            pass
        print(self.typeForm)