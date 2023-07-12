from flask_login import UserMixin
from project import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Float, Boolean
from ..users.users import User
#from sqlalchemy.orm import *
from datetime import datetime 
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref
from ..accounts.models import Account
from ..users.models import Process


class CashMovement(UserMixin, db.Model):
    __tablename__ = 'cashmovement'
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.ForeignKey("account.id"))
    movementDate = db.Column(db.DateTime)
    movementValueDate = db.Column(db.DateTime)
    sense = db.Column(db.String(3))
    ctrParName = db.Column(db.String(50))
    ctrParIban = db.Column(db.String(50))
    ctrParCountry = db.Column(db.String(50))
    communication = db.Column(db.String(100))
    account = db.relationship("Account", backref="cashmovements", lazy="joined")
    amount = db.Column(db.Float)  

    @property
    def movementDateV(self):
        if self.movementDate is None:
            return ""  # or return any other default value you like
        return self.movementDate.strftime("%m/%d/%Y, %H:%M:%S")

    @property
    def movementValueDateV(self):
        if self.movementValueDate is None:
            return ""  # or return any other default value you like
        return self.movementValueDate.strftime("%m/%d/%Y, %H:%M:%S")

    #def createProcess(self): 
    #    process = Process(movementId=self.id,userId=self.account.userId)
    #    db.session.add(process)    
    #    db.session.commit()
    @property
    def currentProcess(self):
        return next((proc for proc in self.process if proc.isCurrent), None)
        

    
    def createProcess(self):      
        process = Process(movementId=self.id, nextUserId=self.account.officerId,statusLabel='pending',flagAuto=True)
        db.session.add(process)
        db.session.commit()
    
    def validateAuto(self):
        # mise en place des règles de validation automatique : 
        if (self.amount < 5000000) or (self.sense == 'IN'):
            process = Process(movementId=self.id, statusLabel='validated',flagAuto=True)
            db.session.add(process)
            db.session.commit()



    def __init__(self, **kwargs):
        date_format = "%d/%m/%Y %H:%M:%S"
        transformed = {}
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key in ['movementDate', 'movementValueDate'] and isinstance(value, str):
                    value = datetime.strptime(value, date_format)
                transformed[key] = value

        # Retrieve the officerId and validatorId
        if 'officerKey' in kwargs:
            user = User.query.filter_by(key=kwargs['officerKey']).first()
            if user:
                kwargs['officerId'] = user.id
            kwargs.pop('officerKey')

        if 'validatorKey' in kwargs:
            user = User.query.filter_by(key=kwargs['validatorKey']).first()
            if user:
                kwargs['validatorId'] = user.id
            kwargs.pop('validatorKey')

        # If 'account_number' is provided but 'accountId' is not, retrieve 'accountId' using 'account_number'
        transformed['accountId']=None
        if 'accountKey' in kwargs.keys():
            account = Account.query.filter_by(key=kwargs['accountKey']).first()
            if account is not None:
                transformed['accountId'] = account.id
            else:
                raise ValueError(f"No account found with number: {kwargs['accountKey']}")
            
            

        # Check if a similar record already exists
        existing = CashMovement.query.filter_by(
            accountId=transformed.get('accountId'),
            movementDate=transformed.get('movementDate'),
            sense=transformed.get('sense'),
            amount=transformed.get('amount')
        ).first()

        # If the record does not exist, create it
        if existing is None:
            for key, value in transformed.items():
                setattr(self, key, value)
