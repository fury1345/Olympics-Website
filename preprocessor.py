import pandas as pd



def preprocess(athlete,noc):
    
    athlete=athlete[athlete['Season']=='Summer'] 
    athlete=athlete.merge(noc,on='NOC',how='left')
    athlete.drop_duplicates(inplace=True)
    athlete=pd.concat([athlete,pd.get_dummies(athlete['Medal'],dtype=int)],axis=1)
    return athlete
