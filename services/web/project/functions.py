import pandas as pd 
import os, shutil 
from datetime import timedelta, datetime
from flask_login import current_user
from flask import current_app
from . import db 
from .users.models import User
import re
class Position(UserMixin, db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True) 
    Date=db.Column(db.Date) 
    PortfolioId=db.Column(db.String, db.ForeignKey("account.AccountID"))
    Security=db.Column(db.String(30)) 
    ISIN=db.Column(db.String(30)) 
    Bloomberg=db.Column(db.String(30)) 
    SecurityCcy=db.Column(db.String(30)) 
    AccountCcy	=db.Column(db.String(30)) 
    Quantity= db.Column(db.Float) 
    Price	= db.Column(db.Float) 
    ValueSecurityCcy=db.Column(db.Float) 
    ValueAccountCcy=db.Column(db.Float) 	
    AccruedInterest=db.Column(db.Float)

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
        super().__init__(**dico_in_new)

    @property
    def DateV(self):
        return self.Date.strftime("%m/%d/%Y, %H:%M:%S")

class Dim:
    def __init__(self, tableClass, funcKey):
        self.tableClass = tableClass
        self.funcKey=funcKey

       



def getClientDict(object,json_comp):
    file_param=os.path.join(os.path.abspath(os.path.dirname(__file__)),"INTERF/PARAM.xlsx")
    print(file_param)
          
    Clientdict={}
    #df_glossary=pd.read_excel("INTERF/PARAM.xlsx")
    df_glossary=pd.read_excel(file_param)
    df_glossary=df_glossary[df_glossary['OBJECT'].map(str.strip)==object.strip()]

    df_new_items=df_glossary[df_glossary['OBJECT']=='rien']
    dict_glossary=dict(zip(df_glossary['EXTRACT_NAME'], df_glossary['DB_NAME']))
    #print('dict_glossary',dict_glossary)
    #print('json_comp.keys',pd.json_normalize(json_comp,max_level=2).T)
    df_json_comp=pd.json_normalize(json_comp,max_level=2).T
    for key in df_json_comp.index:
        try:
            #Clientdict[dict_glossary[key]]=json_comp[key]
            #print('lockey',type(df_json_comp.loc[key,0]))
            Clientdict[dict_glossary[key]]=df_json_comp.loc[key,0]
            print('glossary',dict_glossary[key],df_json_comp.loc[key,0]) 
        except:
            df_new_items=df_new_items.append(pd.Series([object,key,'to define',''],index=df_new_items.columns.tolist()),ignore_index=True)
    
    if df_new_items.shape[0]>0:
        df_new_items.drop_duplicates().to_excel(os.path.join(os.path.abspath(os.path.dirname(__file__)),"INTERF/TO_DEFINE.xlsx"))
        
    #print('Clientdict',Clientdict)

    Clientdict['createdDate']=datetime.now().strftime('%d/%m/%Y')
    Clientdict['dateDeb']= datetime.now()
    Clientdict['dateFin']= datetime(9999,12,31) 
    Clientdict['fk']=Clientdict['id'+object] +'#' + datetime(9999,12,31).strftime("%Y%m%d")
    Clientdict['isCurrent']=True
    #Clientdict['riskProfile']='Low'
    
    #Clientdict['nextDateUBO']=Clientdict['createdDate'] 
    #Clientdict['nextDateRCS']=Clientdict['createdDate'] 
    

    
 
    
    return Clientdict





def scd_Update(tableClass,funcKey,newOccurDict):
    dateChange=datetime.now()

    CurrentOccur=tableClass.query.filter_by(**{funcKey:newOccurDict[funcKey],'isCurrent':True}).first()
    
    newRow=dict(CurrentOccur.__dict__)
    newRow.update(newOccurDict)
    del newRow['id'] 
    del newRow['_sa_instance_state']
    
    CurrentOccur.isCurrent=False
    CurrentOccur.dateFin=dateChange
    CurrentOccur.dateFin=dateChange
    CurrentOccur.fk=CurrentOccur.fk +'#' + dateChange.strftime("%Y%m%d")
    
    print('newRow',newRow)
    newOccur=tableClass(newRow)
    newOccur.isCurrent=True
    newOccur.dateDeb=dateChange
    newOccur.dateFin=datetime(9999,12,31)
    print(newOccur.__dict__)
    db.session.add(newOccur)
    db.session.commit()
    
    return




def clean(noeud):
    noeud1 = re.sub("[\(].*?[\)]", "", noeud)
    noeud2=noeud1.rstrip().upper().replace('É','E').replace('È','E').replace('Â','A'). \
    replace('(','').replace(' :','').replace(')','').replace(' / ','_').replace(',','').replace('  ','').replace(' ','_').        \
    replace('À','A').replace('__','_').replace('°','').replace("'",'_').replace('✔_','').replace('\n','')
    return noeud2



def getObjectDict(NomClass,json_comp):
    # fonction de construction fonctionnelle du dictionnaire à insérer dans la base : 
    file_param=os.path.join(os.path.abspath(os.path.dirname(__file__)),"INTERF/PARAM.xlsx")
    ObjectDict={}
    df_glossary=pd.read_excel(file_param)
    df_glossary=df_glossary[df_glossary['OBJECT']==NomClass]
    df_new_items=df_glossary[df_glossary['OBJECT']=='rien']
    dict_glossary=dict(zip(df_glossary['EXTRACT_NAME'], df_glossary['DB_NAME']))
    
    for key in json_comp.keys():
        try:
            ObjectDict[dict_glossary[key]]=json_comp[key]
        except:
            df_new_items=df_new_items.append(pd.Series([NomClass,key,'to define',''],index=df_new_items.columns.tolist()),ignore_index=True)
    
    if df_new_items.shape[0]>0:
        df_new_items.drop_duplicates().to_excel(os.path.join(os.path.abspath(os.path.dirname(__file__)),"INTERF/TO_DEFINE.xlsx"))
       

    return ObjectDict




def scd_Update2(tableClass,funcKey,CurrentOccur,newOccurDict):
    dateChange=datetime.now()
    #CurrentOccur=tableClass.query.filter_by(**{funcKey:newOccurDict[funcKey],'isCurrent':True}).first()
    newRow=dict(CurrentOccur.__dict__)
    newRow.update(newOccurDict)
    del newRow['id'] 
    del newRow['_sa_instance_state']
    CurrentOccur.isCurrent=False
    CurrentOccur.dateFin=dateChange
    CurrentOccur.fk=newOccurDict[funcKey] +'#' + dateChange.strftime("%Y%m%d_%H:%M:%S")
    print('newRow',newRow)

    newOccur=tableClass(**newRow)
    newOccur.isCurrent=True
    newOccur.dateDeb=dateChange
    newOccur.dateFin=datetime(9999,12,31)
    print(newOccur.__dict__)

    db.session.add(newOccur)
    db.session.commit()
    
    return newOccur





def insertObj(TableClass,newOccurDict ,funcKey: str):
    print("insert obj")
    # fonction d'insert dans la DB :
    # creation des champs techniques : 
    #newOccurDict['createdDate']=datetime.now().strftime('%d/%m/%Y')
    newOccurDict['dateDeb']= datetime.now()
    newOccurDict['dateFin']= datetime(9999,12,31) 
    newOccurDict['fk']=newOccurDict[funcKey] +'#' + datetime(9999,12,31).strftime("%Y%m%d_%H:%M:%S")
    newOccurDict['isCurrent']=True
    # 1. Test sur la clé naturelle : 
    CurrentOccur=TableClass.query.filter_by(**{funcKey:newOccurDict[funcKey],'isCurrent':True}).first()
    res='error'
    print('-----------')
    print(CurrentOccur)
    print(CurrentOccur is not None)
    if not CurrentOccur :
        print('isNone')
        res='creation'
        # creation d'un nouvel objet 
        newOccur=TableClass(**newOccurDict)
        db.session.add(newOccur)
        db.session.commit()
        
    else : 
        print('update')
        # update d'un objet existant 
        newOccur= scd_Update2(TableClass,funcKey,CurrentOccur,newOccurDict)
        res='update'

    print('resultat=',res)
    return newOccur,res



def UpdateDim(tableClass,CurrentOccur,newOccurDict,dateChange=datetime.now()):
    changes={}
    newOccur=None

    # fonction d'update de ligne, avec gestion de l'historisation
    

    # mise en place la nouvelle ligne
    newRow=dict(CurrentOccur.__dict__)
    newRow.pop('_sa_instance_state')
    newRow.pop('id')

    currentRow=dict(CurrentOccur.__dict__)
    # update des champs 
    newRow.update(newOccurDict)

    # comparaison de tous les champs, et construction du dictionnaire des changements 
    for key in newRow.keys():
        print('keys :',key,newRow[key],currentRow[key])
        if (newRow[key]==currentRow[key]) or (key=='dateDeb'):
            continue
        else:
            changes[key]={currentRow[key]:newRow[key]}
            
        print('changes',changes)

    # si le dictionnaire des changements n'est pas nul, on update la dimension : 
    #if len(changes)>0:
    # mise à jour des champs et ajout dans la base d'une nouvelle row : 
    newOccur=tableClass(**newRow)

    newOccur.isCurrent=True
    newOccur.dateDeb=dateChange
    newOccur.dateFin=datetime(9999,12,31)
    print('newOccur',newRow)

    # mise à jour des champs sur la précédente :   
    CurrentOccur.isCurrent=False
    CurrentOccur.dateFin=dateChange
    CurrentOccur.fk=CurrentOccur.fk.split('#')[0]  +'#' + dateChange.strftime("%Y%m%d_%H:%M:%S")
    print('CurrentOccur',CurrentOccur)

    # enregistrement dans la BD : 
    db.session.add(newOccur)
    db.session.commit()
    
    return newOccur,changes




def insertDim(self,newOccurDict,dateChange=datetime.now()):
    funcKey=self.funcKey
    TableClass=self.TableClass
    # fonction d'insert dans la DB :
    # creation des champs techniques : 
    #newOccurDict['createdDate']=datetime.now().strftime('%d/%m/%Y')
    # funcKey is an existing key in newOccurDict to define the natural key : 
    newOccurDict['dateDeb']= datetime.now()
    newOccurDict['dateFin']= datetime(9999,12,31) 
    newOccurDict['isCurrent']=True
    newOccurDict[funcKey]=newOccurDict[funcKey]
    newOccurDict['fk']=  newOccurDict[funcKey] +'#' + newOccurDict['dateFin'].strftime("%Y%m%d_%H:%M:%S")
    print("newOccurDict",newOccurDict)
    # 1. Test sur la clé naturelle : 
    CurrentOccur=TableClass.query.filter_by(**{funcKey:newOccurDict[funcKey],'isCurrent':True}).first()
    res='error'
    print('-----------')
    print(CurrentOccur)
    print(CurrentOccur is not None)
    changes={}
    # si la clé naturelle n'existe pas dans l'objet, on crée une nouvelle occurence 
    if not CurrentOccur :
        res='creation'
        # creation d'un nouvel objet de Classe 
        newOccur=TableClass(**newOccurDict)
        db.session.add(newOccur)
        db.session.commit()
    else : 
        res='update'
        # update d'un objet existant 
        newOccur,changes= UpdateDim(TableClass,CurrentOccur,newOccurDict,dateChange)
        

    print('resultat=',res,newOccur,changes)
    return res,newOccur,changes





def insertUbos(json_ubos,extractionDate,idUser):
    resComp=[]
    listIdCrees=[]
    listIdError=[]
    listIdPresent=[]
    retours={}


    for idCli in json_ubos.keys():
        try:
            dictUbos=json_ubos[idCli]

            # creation de l'objet UBO_extract : 
            ubo_extract_dico = {'idUBO_extract':idCli,'extractionDate':extractionDate,'idUser':idUser}
            res,ubo_extract,changes=insertDim(UBO_extract,ubo_extract_dico,'idUBO_extract',extractionDate)
            
            # ajout de l'entreprise : 
            client=Client.query.filter_by(idCli=idCli,isCurrent=True).first()
            ubo_extract.client=client
            db.session.commit()
            
            
            for dictUbo in dictUbos['LISTE_RBE']:
                # creation ou update des objets Ubo : 
                dictObjUbo=getObjectDict('Ubo',dictUbo)
                dictObjUbo['extractionDate']=extractionDate
                dictObjUbo['idUser']=idUser
                # creation de la clé naturelle : 
                dictObjUbo['idUbo']= clean(dictObjUbo['firstName']+'_'+dictObjUbo['lastName']+'_'+dictObjUbo['dateBirth'])
                #dictObjUbo['riskProfile']='Low'
                res,newOccur,changes=insertDim(Ubo,dictObjUbo,'idUbo')

                ubo_extract.ubos.append(newOccur)
                db.session.commit()

                if res=='creation':
                    listIdCrees+=[idCli +' - '+ dictObjUbo['idUbo']]             
                elif res=='update':
                    listIdPresent+=[idCli +' - '+dictObjUbo['idUbo']]
        
        except:
            listIdError+=[idCli]

        resComp+=[idCli]
    
    retours['created']=listIdCrees   
    retours['present']=listIdPresent
    retours['error']=listIdError

    return retours



#1. recherche de tous les extraits UBO 
# entrée UBO : 
#def getAncestors(Class,Obj,NatKey):
#    listAncestors=Class.query.filter_by({NatKey:Obj.NatKey}).all()
#    return listAncestors


#def getCurrent(Class,Obj,NatKey):
#    CurrentOne=Class.query.filter_by(id=Obj.id,NatKey=Obj.NatKey,isCurrent=True).first()
#    return CurrentOne


#def getAllCurrentRelations(Class,KeyIn,ValIn,ListKeysOut):
#    ListCurrentExtracts=Class.query.filter_by(id=ValIn,isCurrent=True).all()
#    ListKeysOut=list(set([EachRow.KeyOut for EachRow in ListCurrentExtracts]))
#    return ListKeysOut




class HTML_label:
    def __init__(self,lexique,langue):
    # on lit le fichier :
        self.df_lex=pd.read_excel(lexique)
        self.df_lex.rename(columns={'LABEL_'+langue:'LABEL'},inplace=True,errors="raise")
        

    def getLab(self,objectName,dico_in):
        dico_out={}
        for var_in in dico_in:
            try:
                traduc=self.df_lex[(self.df_lex['OBJECT']==objectName) & (self.df_lex['DB_NAME']==var_in) ]['LABEL'].unique()[0]
                dico_out[var_in]=traduc
            except:
                raise Exception('label HTML non défini :',var_in)

        return dico_out



#mydico=HMTL_label('/Users/david/EnvPy/kyce/Kyce/INTERF/PARAM.xlsx','EN')
#print(mydico.getLab('Client','tradeName'))


#Clientdict=getClientDict('Client',{'key1':'val1','key2':'val2','key3':'val3'})


def addDocToDB(idCli,typeDoc,rcsFileName,path_in): 
    current_dt=datetime.now()
    dictObjDoc={}
    dictObjDoc['client_fk']=idCli+'#' + datetime(9999,12,31).strftime("%Y%m%d_%H:%M:%S")
    #dictObjDoc['idCli']=idCli
    dictObjDoc['type']=typeDoc
    dictObjDoc['format']=rcsFileName.split('.')[1].upper()
    
    file=rcsFileName.split('.')[0]+'_'+current_dt.strftime("%Y%m%d")+'.'+rcsFileName.split('.')[1]
    
    dictObjDoc['docName']=file
    dictObjDoc['idDoc']=file.split('.')[0]
    dictObjDoc['docLink']=current_app.config['DB_DOCUMENTS']+'/'+file

    dictObjDoc['createdDate']=current_dt.strftime('%d/%m/%Y')
    #dictObjDoc['dateDeb']= current_dt
    #dictObjDoc['dateFin']= datetime(9999,12,31) 
   
    #dictObjDoc['fk']=dictObjDoc['idDoc'] +'#' + datetime(9999,12,31).strftime("%Y%m%d")
    dictObjDoc['isCurrent']=True
    new_doc,res=insertObj(Doc,dictObjDoc ,'idDoc')
    shutil.move(os.path.join(path_in,rcsFileName),os.path.join(current_app.root_path,dictObjDoc['docLink']))
    return res,new_doc
    


def addDocToDB2(idCli,typeDoc,rcsFileName,path_in): 
    current_dt=datetime.now()
    dictObjDoc={}
    dictObjDoc['client_fk']=idCli+'#' + datetime(9999,12,31).strftime("%Y%m%d_%H:%M:%S")
    #dictObjDoc['idCli']=idCli
    dictObjDoc['type']=typeDoc
    
    file=rcsFileName.split('.')[0]+'_'+current_dt.strftime("%Y%m%d")+'.'+rcsFileName.split('.')[1]
    
    dictObjDoc['docName']=file
    dictObjDoc['idDoc']=file.split('.')[0]
    dictObjDoc['docLink']=current_app.config['DB_DOCUMENTS']+'/'+file

    dictObjDoc['createdDate']=current_dt.strftime('%d/%m/%Y')
    #dictObjDoc['dateDeb']= current_dt
    #dictObjDoc['dateFin']= datetime(9999,12,31) 
   
    #dictObjDoc['fk']=dictObjDoc['idDoc'] +'#' + datetime(9999,12,31).strftime("%Y%m%d")
    dictObjDoc['isCurrent']=True
    new_doc,res=insertObj(Doc,dictObjDoc ,'idDoc')
    shutil.move(os.path.join(path_in,rcsFileName),os.path.join(current_app.root_path,dictObjDoc['docLink']))
    return new_doc
 



#def export_table(idComp,ClassObj,ListIds,toExlude={},toTransform={}):
    #for id in ListIds:
        #ListObjClass=ClassObj.query.filter_by(id=id).all()
        


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def dico2Export(res,listDrop,dictChanges):
    res2={}
    for key in res.keys():
        if key in listDrop:
            continue

        if (type(res[key]).__name__=='datetime'):
            resValue=res[key].strftime("%d/%m/%Y")
        else:
            resValue=res[key]

        if key in dictChanges.keys():
            res2[dictChanges[key]]=resValue
        else:
            res2[key]=resValue
    return res2



def export_data(listComp):
    print(listComp)
    # Export CLIENT INFORMATION
    exportClientList=[]
    for idComp in listComp:
        # for each company :
        # signaletique : 
        linesCli=Client.query.filter_by(isCurrent=True,idCli=idComp).first()
        res=linesCli.__dict__
        listDrop=["nextDateUBO","fk","idUser","id","nextDateRCS","dateDeb","dateFin","isCurrent","_sa_instance_state"]
        dictChanges={"idCli":"Legal_Id"}
        res2=dico2Export(res,listDrop,dictChanges)
        res2["user"]=linesCli.user.name
        exportClientList.append(res2)
    # Transform client rows list in DataFrame
    excelPageClients = pd.DataFrame(exportClientList)
    
    # Export UBO INFORMATION
    exportUBOList = []
    for idComp in listComp:
        UboExtract=UBO_extract.query.filter_by(isCurrent=True).filter_by(idUBO_extract=idComp).first()
        linesUBO=UboExtract.ubos

        #linesUBO = []
        for UBOLine in linesUBO:
            res=UBOLine.__dict__
            listDrop=["dateDeb","dateFin","isCurrent","fk","id","idUser","idUbo","_sa_instance_state"]
            res2=dico2Export(res,listDrop,dictChanges)
            res2["Legal_Id"]=UboExtract.client.idCli
            res2["user"]=UboExtract.user.name
            exportUBOList.append(res2)
            #print('res2-UBO ',res2)

    # Transform UBO rows list in DataFrame
    excelPageUBO = pd.DataFrame(exportUBOList)

    # Export RCS_MAIN INFORMATION
    exportRCSList = []
    for idComp in listComp:
        # for each company :
        linesRCS=Rcsmain.query.filter_by(isCurrent=True,idRcsmain=idComp).first()

        if linesRCS is not None:

            res=linesRCS.__dict__
            listDrop=["dateDeb","dateFin","isCurrent","_sa_instance_state",'id','idUser','client_fk','fk']
            dictChanges={"idRcsmain":"Legal_Id"}
            res2=dico2Export(res,listDrop,dictChanges)
            res2["user"]=UboExtract.user.name
            exportRCSList.append(res2)
            
    
    # Transform RCS rows list in DataFrame
    excelPageRCS = pd.DataFrame(exportRCSList)
    
    # Export Director INFORMATION
    exportDirList = []
    for idComp in listComp:
        # for each company :
        linesDir=Director.query.filter_by(isCurrent=True).join(Rcsmain).filter_by(idRcsmain=idComp).all()

        for DirectorLine in linesDir:
            #if DirectorLine is not None:
            res=DirectorLine.__dict__
            listDrop=["dateDeb","dateFin","isCurrent","_sa_instance_state","fk","rcsmain_fk","idDirector","id","idUser"]
            dictChanges={"idRcsmain":"Legal_Id"}
            #res['RCS']=DirectorLine.rcsmain
            res2=dico2Export(res,listDrop,dictChanges)
            exportDirList.append(res2)
            print('res2',res2)
    
    # Transform Directors rows list in DataFrame
    excelPageDir = pd.DataFrame(exportDirList)

    # WRITE EXCEL FILE & SAVE IT IN DB_DOCUMENTS
    excelName = 'DB_EXPORTS_'+datetime.now().strftime('%d_%m_%Y_%H_%M_%S')+'.xlsx'
    excelLink = current_app.root_path+'/'+current_app.config['EXPORTS'] + '/'
    with pd.ExcelWriter(excelLink + excelName) as writer:
        # Write sheet Clients
        excelPageClients.to_excel(writer, sheet_name=f"CLIENTS")
        # Write sheet UBO
        excelPageUBO.to_excel(writer, sheet_name=f"UBO")
        # Write sheet RCS
        excelPageRCS.to_excel(writer, sheet_name=f"RCS")
        # Wirte sheet Director
        excelPageDir.to_excel(writer, sheet_name=f"DIRECTORS")
        
    return excelLink, excelName


  
    
    
def AddOrdersToDB(OrderRef,user_id,theDate):
    retours={}
    listIdCrees=[]
    listIdError=[]
    listIdPresent=[]
    for RCS in OrderRef.keys():
        dictOrder={'idRcsOrder':OrderRef[RCS],
        'idUser':user_id,
        'client_fk': RCS +'#' + datetime(9999,12,31).strftime("%Y%m%d_%H:%M:%S"),
        'status':'Ordered'}
        newOrder,res=insertObj(RcsOrder,dictOrder ,'idRcsOrder')
        
        if res=='creation':
            listIdCrees+=[RCS + '- order :' + dictOrder['idRcsOrder']]             
        elif res=='update':
            listIdPresent+=[RCS + '- order :' + dictOrder['idRcsOrder']]
        else:
            listIdError+=[RCS + '- order :' + dictOrder['idRcsOrder']]
    
    retours['created']=listIdCrees   
    retours['present']=listIdPresent
    retours['error']=listIdError
    print(retours)
    return retours



def AddExtractsToDB(ListExtracts,user_id,theDate):
    retours={}
    listIdCrees=[]
    listIdError=[]
    listIdPresent=[]
    for extracts in ListExtracts.keys():
        # on verifie si une clé existe déjà... 
        l_exist=[]
        l_exist=RcsOrder.query.filter_by(isCurrent=True,idRcsOrder=extracts).all()
        extract=ListExtracts[extracts]
        
        # ajout du JSON dans la DB 
        rcsJson=extract['excerptJson']
        if (rcsJson !='ERROR' ) and (len(l_exist)==0) :
            new_rcs_dict=getClientDict('Rcsmain',rcsJson)
            print('new_rcs_dict',new_rcs_dict)
            res,newRcs,changes=insertDim(Rcsmain,new_rcs_dict ,'idRcsmain')
            newRcs.client_fk=newRcs.fk

            # ajout de directeurs : 
            listJson=rcsJson['DIRECTOR_MANAGER']['LISTE']
            i=0
            for elem in listJson:
                elem['index_RCS']=new_rcs_dict['idRcsmain']+'_'+str(i)
                new_dir_dict=getClientDict('Director',elem)
                new_dir_dict['rcsmain_fk']=newRcs.fk
                res,newDir,changes=insertDim(Director,new_dir_dict ,'idDirector')
                i+=1
        
            # ajout de l'extrait  (PDF et XLS )et reçu 
            RCS=extract['idCli']
            print('order',ListExtracts[extracts])
            res,receipt=addDocToDB(RCS,'receipt',extract['receipt'],DIR_FILE)
            print('excerptXls',extract['excerptXls'])
            res,excerpt=addDocToDB(RCS,'excerpt',extract['excerpt'],DIR_FILE)
            res,excerptXls=addDocToDB(RCS,'excerpt',extract['excerptXls'].split('/')[-1],DIR_FILE)
            
            #receipt.rcsmain_fk=newRcs.fk
            excerpt.rcsmain_fk=newRcs.fk
            excerptXls.rcsmain_fk=newRcs.fk

            db.session.commit()

                    
            # update de la commande : 
            dictOrder={
            'idRcsOrder':extracts,
            'idUser':user_id,
            'client_fk': RCS +'#' + datetime(9999,12,31).strftime("%Y%m%d_%H:%M:%S"),
            'idRcsmain':newRcs.id,
            'idReceipt':receipt.id,
            #'idExcerpt':excerpt.id,
            'status':'Received'}

            newOrder,res=insertObj(RcsOrder,dictOrder ,'idRcsOrder')
           


            if res=='creation':
                listIdCrees+=[RCS + '- order :' + dictOrder['idRcsOrder']]             
            elif res=='update':
                listIdPresent+=[RCS + '- order :' + dictOrder['idRcsOrder']]
            else:
                listIdError+=[RCS + '- order :' + dictOrder['idRcsOrder']]
    
    retours['created']=listIdCrees   
    retours['present']=listIdPresent
    retours['error']=listIdError

    print(retours)
    return retours