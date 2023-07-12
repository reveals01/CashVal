from flask_login import UserMixin
from project import db
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Float, Boolean
#from sqlalchemy.orm import *

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date,datetime
from ..models import Dimension

Base = declarative_base()

class Parameter(db.Model):
    __tablename__ = 'parameter'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    idParameter = db.Column(db.String(250))
    typeLabel = db.Column(db.String(50))
    label = db.Column(db.String(200))
    
    def __init__(self, *args,**kwargs):
        dico_in=kwargs
        dico_in['idParameter']=dico_in['typeLabel'].strip()+'_'+dico_in['label'].strip()
        super().__init__(**dico_in)
        db.session.commit()
