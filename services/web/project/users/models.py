from flask_login import UserMixin
from project import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date,datetime

class globalTable(UserMixin,db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    createdDate=db.Column(db.DateTime)
    updatedDate=db.Column(db.DateTime)
    @property
    def createdDateV(self):
        return self.createdDate.strftime("%m/%d/%Y, %H:%M:%S")
    
    @property
    def updatedDateV(self):
        return self.updatedDate.strftime("%m/%d/%Y, %H:%M:%S")
    
    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    key = db.Column(db.String(50),unique=True)
    #fk= db.Column(db.String(50)) 
    email = db.Column(db.String(50),unique=True)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(100))
    role = db.Column(db.String(50))
    business=db.Column(db.String(100))
    group = db.Column(db.String(50))
    surname = db.Column(db.String(100))
    createdDate=db.Column(db.DateTime)
    updatedDate=db.Column(db.DateTime)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @property
    def createdDateV(self):
        return self.createdDate.strftime("%m/%d/%Y, %H:%M:%S")
    
    @property
    def updatedDateV(self):
        return self.updatedDate.strftime("%m/%d/%Y, %H:%M:%S")

    @password.setter
    def password(self, password):
        print('password',password)
        self.password_hash = generate_password_hash(password)
        print('password',self.password_hash)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @hybrid_property
    def dictFields(self):
         res=self.__dict__
         del res['_sa_instance_state']
         return res
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def update(self,dico_in):
        theDate=datetime.now()
        dico_in['updatedDate']=theDate
        for key in self.__dict__.keys() :
            if (key in dico_in.keys()) & (key != 'id') :
                    setattr(self,key,dico_in[key])
                    
            self.password=dico_in['password']
            print(dico_in)
        db.session.commit()
    


    def __init__(self, *args,**kwargs):
        print('kwargs',kwargs)
        theDate=datetime.now()
        dico_in=kwargs
        dico_in['createdDate']=theDate
        dico_in['updatedDate']=theDate
        #dico_in['key']=dico_in['email']
        dico_in_new={}
        # Check if a similar record already exists
        existing = User.query.filter_by(key=dico_in['key']).first()
        if existing is None:
            for key in dico_in.keys() :
                if (key in User.__dict__.keys()) & ((key != 'id') & (key != 'password')) :
                    dico_in_new[key]=dico_in[key]
            super().__init__(**dico_in_new)
            self.password=dico_in['password']
            db.session.commit()



class Process(UserMixin, db.Model):
    __tablename__ = 'process'
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Integer, primary_key=True)
    movementId = db.Column(db.ForeignKey("cashmovement.id"))
    userId = db.Column(db.ForeignKey("user.id"))
    nextUserId = db.Column(db.ForeignKey("user.id"))
    lastUpdate = db.Column(db.DateTime)
    statusLabel = db.Column(db.String(50), default='Pending')  # 'Pending' as default statusLabel
    isCurrent = db.Column(db.Boolean)
    flagAuto = db.Column(db.Boolean)
    cashmovement = db.relationship("CashMovement", backref="process", lazy="joined", uselist=False)
    user = db.relationship("User", foreign_keys=[userId], backref="processes")
    nextUser = db.relationship("User", foreign_keys=[nextUserId], backref="nextProcesses")

    def __init__(self, **kwargs):
        dateOp=datetime.now()
        kwargs['id']=kwargs['movementId']
        process=Process.query.filter_by(movementId=kwargs['movementId']).first()
        if process:
            setattr(process,'isCurrent',False)
            setattr(process,'lastUpdate',dateOp)
            kwargs['step']=process.step+1
            
        else:
            kwargs['step']=0

        if 'userKey' in kwargs.keys():
            theUser=User.query().filter_by(key=kwargs['userKey']).first()
            if theUser is not None:
                kwargs['userId']=theUser.id
        
        super(Process, self).__init__(**kwargs)
        self.lastUpdate=dateOp
        self.isCurrent=True




