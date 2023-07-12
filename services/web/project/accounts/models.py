from flask_login import UserMixin
from project import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime 
from ..models import Dimension
from ..clients.models import Client 
from ..users.models import User 



class Account(UserMixin, db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True) 
    clientId=db.Column(db.ForeignKey("client.id"))
    userId=db.Column(db.ForeignKey("user.id"))
    officerId = db.Column(db.ForeignKey("user.id"))
    validatorId = db.Column(db.ForeignKey("user.id"))
    managerId = db.Column(db.ForeignKey("user.id"))
    bankName=db.Column(db.String(50)) 
    currency=db.Column(db.String(5)) 
    key=db.Column(db.String(100)) 
    accountName=db.Column(db.String(50)) 
    iban=db.Column(db.String(30)) 
    bic=db.Column(db.String(30)) 
    creationDate=db.Column(db.DateTime) 
    openingDate=db.Column(db.DateTime) 
    closingDate=db.Column(db.DateTime) 
    lastUpdate=db.Column(db.DateTime) 
    positions= db.relationship("Position", backref="account",lazy="joined")
    client= db.relationship("Client", backref="accounts",lazy="joined")
    
    user=db.relationship("User", foreign_keys=[userId], backref="accounts_as_usr")
    officer=db.relationship("User", foreign_keys=[officerId], backref="accounts_as_ofr")
    validator=db.relationship("User", foreign_keys=[validatorId], backref="accounts_as_sor")
    manager=db.relationship("User", foreign_keys=[managerId], backref="accounts_val")
 
    def update(self,data):
        for key, value in data.items():
            if hasattr(self, key):
                if key not in ['creationDate', 'openingDate', 'lastUpdate','closingDate']:
                    setattr(self, key, value)
                else:
                    setattr(self, key, datetime.strptime(value, "%d/%m/%Y %H:%M:%S"))


    def __init__(self, **kwargs):
        for field in ['creationDate', 'openingDate', 'lastUpdate','closingDate']:
            if field in kwargs:
                if isinstance(kwargs[field], str):
                    kwargs[field] = datetime.strptime(kwargs[field], "%d/%m/%Y %H:%M:%S")

        # Retrieve the corresponding userId if it's provided
        if 'userKey' in kwargs:
            user = User.query.filter_by(key=kwargs['userKey']).first()
            if user:
                kwargs['userId'] = user.id
            kwargs.pop('userKey')
                #raise ValueError(f"No user found with idUser: {kwargs['userId']}")


        # Retrieve the corresponding clientId if it's provided
        if 'clientKey' in kwargs:
            client = Client.query.filter_by(key=kwargs['clientKey']).first()
            if client:
                kwargs['clientId'] = client.id
            kwargs.pop('clientKey')
                #raise ValueError(f"No user found with idUser: {kwargs['userId']}")
        
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


        
        # Retrieve the officerId from Orga :
        #orga = Orga.query.filter_by(business=kwargs['business'],idClient=kwargs['clientId']).first()
        #if orga:
            #kwargs['officerId']=orga.idOfficer
            #kwargs['validatorId']=orga.idValidator
            
        

        # Avoid duplication based on AccountName
        if 'key' in kwargs:
            existing_account = Account.query.filter_by(key=kwargs['key']).first()
            if existing_account:
                raise ValueError(f"Account with key {kwargs['key']} already exists")

        super(Account, self).__init__(**kwargs)    


def none(theStr):
        print(type(theStr))
        if type(theStr)==str:
            res=theStr.strip()
        else:
            res='none'
        return res





class CashPosition(UserMixin, db.Model):
    __tablename__ = 'cashposition'
    id = db.Column(db.Integer, primary_key=True) 
    accountId=db.Column(db.ForeignKey("account.id"))
    Date=db.Column(db.Date) 
    Assets= db.Column(db.Float) 
    account=db.relationship("Account", backref="cashpositions", lazy="joined")
    @property
    def DateV(self):
        return self.Date.strftime("%m/%d/%Y")





        
            
            
                
                






class Position(UserMixin, db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True) 
    Date=db.Column(db.Date) 
    PortfolioId=db.Column(db.ForeignKey("account.id"))
    Security=db.Column(db.String(50)) 
    ISIN=db.Column(db.String(50)) 
    Bloomberg=db.Column(db.String(50)) 
    SecurityCcy=db.Column(db.String(50)) 
    AccountCcy	=db.Column(db.String(50)) 
    Quantity= db.Column(db.Float) 
    Price= db.Column(db.Float) 
    ValueSecurityCcy=db.Column(db.Float) 
    ValueAccountCcy=db.Column(db.Float) 	
    AccruedInterest=db.Column(db.Float)
    idPosition=db.Column(db.String(100))

    
    def addPos(self):
        # constitution de la clé primaire fonctionnelle 
        #self['idPosition']=self['Security'].strip() +'_'+self['ISIN'].strip() +'_'+self['Bloomberg'].strip()+ '_' + datetime.strftime(self['Date'],"%d/%m/%Y")
        existingPosition=Position.query.filter_by(idPosition=self.idPosition).first()
        if not existingPosition:
            db.session.add(self)
        else:   
            Position.query.filter_by(idPosition=self.idPosition).delete()
            db.session.commit()
            db.session.add(self)
        db.session.commit()



    def __init__(self, *args,**kwargs):
        dico_in=kwargs
        dico_in_new={}
        for key in dico_in.keys() :
            if (key in Position.__dict__.keys()) & ((key != 'id')) :
                if ('dt' in key) or ('Date' in key):
                    if dico_in[key] != '':
                        dico_in_new[key]=datetime.strptime(dico_in[key],"%d/%m/%Y")
                else:
                    dico_in_new[key]=dico_in[key]
        dico_in_new['idPosition']=none(dico_in_new['PortfolioId'])  \
        +'_'+none(dico_in_new['Security'])  \
        +'_'+none(dico_in_new['ISIN']) \
        +'_'+none(dico_in_new['Bloomberg']) \
        +'_'+none(dico_in_new['ValueAccountCcy']) \
        +'_'+datetime.strftime(dico_in_new['Date'],"%d/%m/%Y")
        
        #print('query',Account.query.filter_by(AccountID=dico_in_new['PortfolioId']).first().__dict__['id'])

        dico_in_new['PortfolioId']=Account.query.filter_by(AccountID=dico_in_new['PortfolioId']).first().__dict__['id']
        super().__init__(**dico_in_new)

    @property
    def DateV(self):
        return self.Date.strftime("%d/%m/%Y")
    
    @property
    def ValueAccountCcyV(self):
        return '{0:,}'.format(self.ValueAccountCcy)