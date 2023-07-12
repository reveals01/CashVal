from flask_login import UserMixin
from project import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime 
from sqlalchemy import Integer, ForeignKey, String, Column



def UpdateDim(NewOccur,CurrentOccur,typeScd=1):
    # fonction d'update de ligne, avec gestion de l'historisation

    dateChange=NewOccur._dateDeb
    # on cree une nouvelle ligne :
    newRowDict=dict(CurrentOccur.__dict__)
    newRowDict.pop('_sa_instance_state')
    newRowDict.pop('id')
    newRowDict.update(NewOccur.__dict__)

    # on reprend la ligne en table :
    currentRowDict=dict(CurrentOccur.__dict__)
    
    
    # comparaison de tous les champs, et construction du dictionnaire des changements 
    changes={}
    for key in newRowDict.keys():
        # on ne compare par les champs techniques 
        if (key[0] != '_') and (key[0] != 'id'):
            print('keys :',key,newRowDict[key],currentRowDict[key])
            if (newRowDict[key]==currentRowDict[key]):
                continue
            else:
                changes[key]=newRowDict[key]
        else:
            continue
    
    if len(changes)>0:
        print('changes :',changes)
        if typeScd==1:
        # scd de type 1 : on update la ligne de la dimension 
            #CurrentOccur.update(changes)
            changes['_dateDeb']=dateChange
            for key in changes.keys():
                setattr(CurrentOccur,key,changes[key])
            NewOccur=CurrentOccur
            db.session.commit()
            

        if typeScd ==2:
            # scd de type 2 : on garde la ligne précédente, en historisé
            CurrentOccur._isCurrent=False
            CurrentOccur._dateFin=dateChange
            CurrentOccur._fk=CurrentOccur._fk.split('#')[0]  +'#' + dateChange.strftime("%Y%m%d_%H:%M:%S")
 
            # enregistrement dans la BD de la nouvelle occurence :
            db.session.add(NewOccur)
            db.session.commit()
            
    else:
            print('changes :','NOTHING')
    
    return NewOccur,changes



class Dimension:
    _fk= db.Column(db.String(50))
    _dateDeb=db.Column(db.DateTime)
    _dateFin=db.Column(db.DateTime)
    _isCurrent=db.Column(db.Boolean)

    def __init__(self,funcKey,TableClass):
        print(self.__dict__)
        self._funcKey=funcKey
        self._TableClass=TableClass
        self._dateDeb= datetime.now()
        self._dateFin= datetime(9999,12,31) 
        self._isCurrent=True
        self._fk=self.__dict__[funcKey] +'#' + self._dateFin.strftime("%Y%m%d_%H:%M:%S")
 
    
    #def store(self,newOccurDict):
    #    CurrentOccur=self._TableClass.query.filter_by(**{self._funcKey:newOccurDict[self._funcKey],'_isCurrent':True}).first()
    #    changes={}
    #    if not CurrentOccur :
    #    # si la clé naturelle n'existe pas dans l'objet, on crée une nouvelle occurence 
    #        print('creation')
    #        res='creation'
    #        db.session.add(self)
    #        db.session.commit()
    #        newOccur=changes=self.__dict__
            
    #    else : 
    #    # si la clé naturelle existe, on update la dimension : 
    #        print('update')
    #        res='update'
    #        # update d'un objet existant 
    #        newOccur,changes= UpdateDim(self,CurrentOccur)


    def store2(self):
        CurrentOccur=self._TableClass.query.filter_by(**{self._funcKey:self.__dict__[self._funcKey],'_isCurrent':True}).first()
        changes={}
        if not CurrentOccur :
        # si la clé naturelle n'existe pas dans l'objet, on crée une nouvelle occurence 
            print('creation')
            res='creation'
            db.session.add(self)
            db.session.commit()
            newOccur=self
            changes=self.__dict__
            
        else : 
        # si la clé naturelle existe, on update la dimension : 
            print('update')
            res='update'
            
            # update d'un objet existant 

            newOccur,changes= UpdateDim(self,CurrentOccur)
            

        print('resultat=',res,newOccur,changes)
        return res,newOccur,changes
    

    @property
    def _dateDebV(self):
        return self._dateDeb.strftime("%d/%m/%Y, %H:%M:%S")
    
    @property
    def _dateFinV(self):
        return self._dateFin.strftime("%d/%m/%Y, %H:%M:%S")

    
    
    