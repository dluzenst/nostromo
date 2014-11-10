# -*- coding: utf-8 -*-
import sys
from pandas import Series, DataFrame
import pandas as pd
import csv
import requests
import numpy as np

csv.field_size_limit(sys.maxsize)


df_acc=pd.read_csv("fic_acc.csv",sep=',',low_memory=False,error_bad_lines=False)
#df_veh=pd.read_csv("fic_veh.csv",sep=',',low_memory=False,error_bad_lines=False)

#df_veh['anmc'].unique()
#df_veh = df_veh.dropna()
#print "df_veh shape ", df_veh.shape
#df_veh['anmc'].value_counts()


print "df_acc shape après 1er filtre : ", df_acc.shape
print "columns : " , df_acc.columns

#print "data_acc shape ", data_acc.shape

# attention ne pas faire de df_acc.dropna() car cela drop toutes les lignes !!
df_acc.dropna(how='all') 
print "df_acc shape après drop NA all ", df_acc.shape


# on sélectionne ceux qui ont lat renseignés : long=0 on garde car c'est vraisemblable en France
df_acc_lat_long = df_acc[df_acc[u'lat']>0]
print "df_acc shape avec lat renseignées", df_acc_lat_long.shape

# on sélectionne ceux qui ont dep et com renseignés 
df_accn = df_acc[df_acc[u'dep']>0]
print "df_acc shape avec dep ", df_accn.shape
df_accn = df_accn[df_accn[u'com']>0]
print "df_acc shape avec com ", df_accn.shape
#df_acc shape avec com  (439332, 36)

columns=[u'numac',u'lum', u'atm', u'col', u'com', u'dep', u'catr', u'infra', u'voie', u'v1', u'v2', u'pr', u'pr1', u'prof', u'plan', u'ttue', u'tbg', u'tbl', u'tindm', u'libellevoie', u'grav', u'gps', u'lat', u'long', u'adr']

df_accn=df_accn[columns]

#on nettoie la colonne "dep" : 411297 rows >99
#print "dep avant"
#print df_accn[df_accn[u'dep']>99][u'dep'].value_counts()
df_accn.loc[(df_accn[u'dep']>99),u'dep'] /=10
print "dep APRES"  
print df_accn[u'dep'].value_counts()
   
# on crée la colonne code insee
df_accn[u'insee']=df_accn[u'dep']*1000+df_accn[u'com']
df_accn[u'insee']=df_accn[u'insee'].astype('int64')
print "code insee VALUES"
print df_accn[u'insee'].value_counts()


# on retrouve le code postal,  avec le fichier "INSEE.csv"
df_insee=pd.read_csv("insee.csv",sep=',',low_memory=False)

df_accn = pd.merge(df_accn,df_insee,left_on='insee',right_on='INSEE',how='outer')
print "df_acc shape avec code insee ", df_accn.shape
# ??? df_acc shape avec code insee  (454049, 30) ?????

# v1 = numero de l'adresse dans la rue
df_accn.loc[(df_accn[u'v1']==0),u'v1'] =""
df_accn[u'adr']= df_accn[u'adr'].fillna(' ')
df_accn[u'Commune']= df_accn[u'Commune'].fillna(' ')

# on retrouve lat et long avec API Google
API_KEY_C = 'AIzaSyCIjnHYw6D1Mn829dC09ep5k8VJKUJ5Iys'
API_KEY_D = 'AIzaSyC7d9cBib4H734ta4lHc0JEQ7LMIdm3njQ'
API_KEY = API_KEY_D

url_api_maps="https://maps.googleapis.com/maps/api/geocode/json?address="

def rech_lat_long(row):
    adresse = str(row[u'v1'])+" " +str(row[u'adr'])+" "+str(row[u'Codepos'])+" " +str(row[u'Commune'])+", France"
    url=url_api_maps+adresse+"&key="+API_KEY
    results_api = requests.get(url)
    johnny = results_api.json()
#    print "adresse : ",adresse    
#    print johnny
    print row[u'numac'], adresse, johnny['status']
    if johnny['status']=='OK':
        row[u'lat'] = johnny['results'][0]['geometry']['location']['lat']
        row[u'long'] = johnny['results'][0]['geometry']['location']['lng']
        print row[u'lat'],row[u'long']
    else:
        print 'Lat-Lon not found'
        row[u'lat'] = None
        row[u'long'] = None
    #return row[u'lat'],row[u'long']
    return row




dfshort = df_accn[1100:1150]
dfshort = dfshort.apply(lambda x: rech_lat_long(x),axis=1)

# df_accn = df_accn.apply(lambda x: rech_lat_long(x),axis=1)

#    return lat,long


#for index, row in df_accn.iterrows():

    
   

# on remet le tout dans 1 csv
#df_accn.to_csv('out.csv')
dfshort.to_csv('out_short.csv')
