from flask_login import UserMixin
from project import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Float, Boolean
from ..users.users import User
#from sqlalchemy.orm import *
from datetime import datetime 
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    creationDate = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(2))  # ISO 3166-1 alpha-2 code
    business = db.Column(db.String(50)) 
    def __init__(self, data):
        for field in data:
            if hasattr(self, field):
                if 'date' in field and data[field]:  # it's a date field and not null
                    data[field] = datetime.strptime(data[field], "%d/%m/%Y %H:%M:%S")
                setattr(self, field, data[field])

    
    def __init__(self, **kwargs):
        for field in ['creationDate']:
            if field in kwargs:
                if isinstance(kwargs[field], str):
                    kwargs[field] = datetime.strptime(kwargs[field], "%d/%m/%Y %H:%M:%S")

        
        # Avoid duplication based on Clients
        if 'key' in kwargs:
            existing_client = Client.query.filter_by(key=kwargs['key']).first()
            if existing_client:
                raise ValueError(f"Account with key {kwargs['key']} already exists")

        super(Client, self).__init__(**kwargs)   



class Orga(UserMixin, db.Model):
    __tablename__ = 'orga'
    id = db.Column(db.Integer, primary_key=True)
    idClient = db.Column(db.Integer, db.ForeignKey("client.id"), unique=True)
    business = db.Column(db.String(50)) 
    idOfficer = db.Column(db.Integer, db.ForeignKey("user.id"))
    idValidator = db.Column(db.Integer, db.ForeignKey("user.id"))

    officer = db.relationship("User", foreign_keys=[idOfficer])
    validator = db.relationship("User", foreign_keys=[idValidator])
    client = db.relationship("Client", backref=backref("orga", uselist=False), foreign_keys=[idClient])

    @hybrid_property
    def key(self):
        return str(self.idClient) + "_" + self.business

    def __init__(self, **kwargs):
        print('kwargs',kwargs)
        # Retrieve the corresponding userId if it's provided
        if 'officerKey' in kwargs:
            officer = User.query.filter_by(key=kwargs['officerKey']).first()
            if officer:
                kwargs['idOfficer'] = officer.id
            del kwargs['officerKey']

        if 'validatorKey' in kwargs:
            validator = User.query.filter_by(key=kwargs['validatorKey']).first()
            if validator:
                kwargs['idValidator'] = validator.id
            del kwargs['validatorKey']
        
        # Retrieve the corresponding clientId if it's provided
        if 'clientKey' in kwargs:
            client = Client.query.filter_by(key=kwargs['clientKey']).first()
            if client:
                kwargs['idClient'] = client.id
            del kwargs['clientKey']

        # Avoid duplication based on key
        existing_orga = Orga.query.filter_by(key=str(kwargs['idClient'])+'_'+kwargs['business']).first()
        if existing_orga:
            raise ValueError(f"Orga with key {kwargs['idClient']+'_'+kwargs['business']} already exists")
        
        super(Orga, self).__init__(**kwargs) 


        
   

