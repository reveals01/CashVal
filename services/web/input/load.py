import pandas as pd
import os
import requests
from faker import Faker
import random

# Création d'une instance Faker
fake = Faker("fr_FR")

# Fonction pour générer un faux nom
def generer_faux_nom(l_input=["Monsieur", "Madame", "Société"]):
    prefixe = random.choice(l_input)
    if prefixe == "Société":
        nom = fake.company()
    else:
        nom = fake.name()
    return f"{prefixe} {nom}"

# Création du DataFrame
df = pd.DataFrame()

def newPosition():
    df_pos=pd.read_csv('./BANKVISTA_positions_20230503_20230504-190003.csv',sep=';')
    df_por=pd.read_csv('./BANKVISTA_portfolios_20230503_20230504-190004.csv',sep=';')

    # anonymmisation : 
    df_por["AccountName"] = [generer_faux_nom() for _ in range(0,df_por.shape[0])]  # Changer 10 par le nombre souhaité de faux noms
    df_por["AccountManager1"] = random.choices([generer_faux_nom(["Monsieur", "Madame"]) for _ in range(10)], k=df_por.shape[0])
    df_por["AccountManager2"] = random.choices([generer_faux_nom(["Monsieur", "Madame"]) for _ in range(10)], k=df_por.shape[0])
    df_por["RelationshipManager"] = random.choices([generer_faux_nom(["Monsieur", "Madame"]) for _ in range(10)], k=df_por.shape[0])
    
    merge_df=pd.merge(df_pos[['PortfolioId','ISIN']], df_por[['AccountID','RelationshipManager']], right_on='AccountID', left_on='PortfolioId', how='inner')
    managers=merge_df['RelationshipManager'].unique()
    managers_df = pd.DataFrame(columns=['name', 'surname', 'email', 'role', 'password'])
    for manager in managers:
        role = 'FRONT'
        managers_df = pd.concat([managers_df,pd.DataFrame({'name': manager.split(' ')[1], 'surname': manager.split(' ')[2].title(), 'email': manager.split(' ')[1].lower() + '.' + manager.split(' ')[0].lower() + '@gmail.com', 'role': role, 'password': 'Reveals'}, index=[0])], ignore_index=True)

    js_input=managers_df.to_json(orient='records')
    # api-endpoint
    URL = "http://127.0.0.1:5001/api/setusers"


    # defining a params dict for the parameters to be sent to the API
    json = js_input
    
    # sending get request and saving the response as response object
    r = requests.post(url = URL, json = json)
    
    # extracting data in json format
    print('Managers:', r)


    position = pd.merge(df_pos,df_por,left_on='PortfolioId',right_on='AccountID',how='left')
    
    
    position['AccountID']=position['AccountID'].astype('str')
    position['PortfolioId']=position['PortfolioId'].astype('str')

    def extractDate(x):
        t=x.split(' ')
        if len(t) > 1:
            y=t[0]
        else:
            y=x
        return y

    position['CreationDate']=position['CreationDate'].apply(extractDate)
    position['OpeningDate']=position['OpeningDate'].astype(str).apply(extractDate)
    position['ClosingDate']=position['ClosingDate'].astype(str).apply(extractDate)

    position['InvestmentPolicy']=position['InvestmentPolicy'].apply(lambda x: x.strip() if x==x else '')
    js_input=position.to_json(orient='records')

    URL = "http://127.0.0.1:5001/api/setpositions"

    # defining a params dict for the parameters to be sent to the API
    json = js_input

    # sending get request and saving the response as response object
    r = requests.post(url = URL, json = json)

    # extracting data in json format
    print(r)

def newPrice():
    df = pd.read_csv('./BANKVISTA_securities_20230504_20230505-080502.csv',sep=';')
    
    # selection des colonnes à remonter dans l'objet :
    cols=['SECURITIES','ID_ISIN','CRNCY','PX_CLOSE_DT','PX_LAST','RTG_SP','SP_EFF_DT',
    'RTG_SP_LT_LC_ISS_CRED_RTG_DT',
    'RTG_SP_LT_LC_ISSUER_CREDIT',
    'RTG_FITCH_LT_ISSUER_DFLT_RTG_DT',
    'RTG_FITCH',
    'RTG_FITCH_LT_ISSUER_DEFAULT',
    'RTG_FITCH_SEN_UNSEC_RTG_DT',
    'RTG_FITCH_SEN_UNSECURED',
    'RTG_MOODY_LONG_TERM_DATE',
    'RTG_MOODY',
    'RTG_MOODY_LONG_TERM',
    'RTG_MDY_ISSUER_RTG_DT',
    'RTG_MDY_ISSUER',
    'RTG_MDY_SEN_UNSECURED_DEBT']

    df_light=df[cols]

    # suppresssion des NA
    df_light2=df_light.apply(lambda x: x.apply(lambda x: '' if x=='N.A.' else x))

    # suppresssion des espaces vides
    df_light2=df_light2.apply(lambda x: x.apply(lambda x: x.strip() if type(x)==str else x))


    # passage des noms de colonnes en minuscule
    df_light2.columns=[x.lower() for x in df_light2.columns.tolist()]

    # Modification de la colonne px_close_dt en date
    df_light2['px_close_dt'] = pd.to_datetime(df_light2['px_close_dt'], errors='coerce')
    df_light2['px_close_dt'] = pd.to_datetime(df_light2['px_close_dt'], errors='coerce')

    df_light2['px_last']=df_light2['px_last'].apply(lambda x: 0 if x =='' else x)

    js_input=df_light2[['securities',
        'id_isin',
        'crncy',
        'px_close_dt',
        'px_last',
        'rtg_sp',
        'sp_eff_dt',
        'rtg_sp_lt_lc_iss_cred_rtg_dt',
        'rtg_sp_lt_lc_issuer_credit',
        'rtg_fitch_lt_issuer_dflt_rtg_dt',
        'rtg_fitch',
        'rtg_fitch_lt_issuer_default',
        'rtg_fitch_sen_unsec_rtg_dt',
        'rtg_fitch_sen_unsecured',
        'rtg_moody_long_term_date',
        'rtg_moody',
        'rtg_moody_long_term',
        'rtg_mdy_issuer_rtg_dt',
        'rtg_mdy_issuer',
        'rtg_mdy_sen_unsecured_debt']].to_json(orient='records')

    URL = "http://127.0.0.1:5001/api/setprices"
  
    
    # defining a params dict for the parameters to be sent to the API
    json = js_input
    
    # sending get request and saving the response as response object
    r = requests.post(url = URL, json = json)
    
    # extracting data in json format
    print(r)
    return df_light2
    


if __name__ == "__main__":
    newPosition()
    newPrice()
  




