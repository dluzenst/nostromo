# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from pandas import Series, DataFrame
import pandas as pd
import csv
import requests
import numpy as np
import unicodedata as uni
import re
from BeautifulSoup import BeautifulSoup


### VARIABLES IMPORTANTES
API_KEY_C = 'AIzaSyCIjnHYw6D1Mn829dC09ep5k8VJKUJ5Iys'
API_KEY_D = 'AIzaSyC7d9cBib4H734ta4lHc0JEQ7LMIdm3njQ'
API_KEY_W = 'AIzaSyDW_ZDyMTvaAj2um4b_YqyfiMVjLRu56Eg'
API_KEY_W2 = 'AIzaSyCymrpJJ1asvVV9uZGCVavUh_aFPC-bAPo'

#AIzaSyDW_ZDyMTvaAj2um4b_YqyfiMVjLRu56Eg
API_KEY = API_KEY_W2
url_api_maps="https://maps.googleapis.com/maps/api/geocode/json?address="



###### FONCTIONS 

# FONCTION QUI CREE LA COLONNE ADRESSE
def adresse(x):
#    x[u'adresse']  = str(x[u'v1'])+" " +str(x[u'libellevoie'])+" "+str(x[u'Codepos'])+" " +str(x[u'Commune'])+", France"
    x[u'adresse']  = str(x[u'Codepos'])+" " +str(x[u'Commune'])+", France"
    return x


# FONCTION de groupe QUI RECHERCHE LATITUDE ET LONGITUDE PAR API MAPS
def rech_lat_long(x):
    url=url_api_maps+x.name+"&key="+API_KEY
    print x.name
    results_api = requests.get(url)
    johnny = results_api.json()
    if johnny['status']=='OK':
        x['latG'] = johnny['results'][0]['geometry']['location']['lat']
        x['longG'] = johnny['results'][0]['geometry']['location']['lng']
#        print row[u'latG'],row[u'longG']
    else:
        print 'Lat-Lon not found'
        x[u'latG'] = None
        x[u'longG'] = None

    return x



# FONCTION DE TEST  
def myfunc(x):
#    print x[u'adresse']
    print x.name
    x['latG']=len(x.name)
    return x



####### PROGRAMME

# 1. LECTURE DU FICHIER DES ACCIDENTS
csv.field_size_limit(sys.maxsize)
df_acc=pd.read_csv("fic_acc.csv",sep=',',low_memory=False,error_bad_lines=False)

print "df_acc shape après lecture : ", df_acc.shape
#print "columns : " , df_acc.columns

# attention ne pas faire de df_acc.dropna() car cela drop toutes les lignes !!
df_acc.dropna(how='all') 
print "df_acc shape après drop NA all ", df_acc.shape

# 2. FILTRAGE ET NETTOYAGE
#On sélectionne ceux qui ont lat renseignés : long=0 on garde car c'est vraisemblable en France
df_acc_lat_long = df_acc[df_acc[u'lat']>0]
print "df_acc shape avec lat renseignées", df_acc_lat_long.shape

# on sélectionne ceux qui ont dep et com renseignés 
df_accn = df_acc[df_acc[u'dep']>0]
df_accn = df_accn[df_accn[u'com']>0]
print "df_accn shape avec com ", df_accn.shape
#df_acc shape avec com  (439332 LIGNES)

# définition des colonnes qui nous intéressent
#columns=[u'numac',u'lum', u'atm', u'col', u'com', u'dep', u'catr', u'infra', u'voie', u'v1', u'v2', u'pr', u'pr1', u'prof', u'plan', u'ttue', u'tbg', u'tbl', u'tindm', u'libellevoie', u'grav', u'gps', u'lat', u'long', u'adr']
columns=[u'numac',u'lum', u'atm', u'com', u'dep', u'v1', u'grav', u'libellevoie', u'catr',u'int',u'prof',u'plan',u'lat', u'long']

# on réduit le nombre de colonnes
df_accn=df_accn[columns]
print "df_accn shape réduit ", df_accn.shape

#on nettoie la colonne "dep" : /10 puis partie entière
df_accn[u'dep']=np.floor(df_accn[u'dep']/10)


# on retire les lignes de CP > 95 (DOM TOM)   
df_accn = df_accn[df_accn[u'dep']<96]
print "dep APRES NETTOYAGE "  
print df_accn[u'dep'].value_counts()
print "df_accn shape METROPOLE ", df_accn.shape
# METROPOLE :  (425659, 10)

# 3. RECHERCHE DES DONNEES MANQUANTES 
# 3.1  CODE POSTAL ET COMMUNE
# on crée la colonne code insee
df_accn[u'insee']=df_accn[u'dep']*1000+df_accn[u'com']
df_accn[u'insee']=df_accn[u'insee'].astype('int64')
#print "code insee VALUES : "
#print df_accn[u'insee'].value_counts()

# on retrouve le code postal,  avec le fichier "INSEE.csv"
# 
df_insee=pd.read_csv("insee.csv",sep=',',low_memory=False)

df_accn = pd.merge(df_accn,df_insee,left_on='insee',right_on='INSEE',how='left')
print "df_acc shape avec code insee ", df_accn.shape
#print df_accn[u'Commune'].value_counts


# 3.2 LATITUDE ET LONGITUDE
#Formatage du champ adresse : n°, voie, code postal, ville
# v1 = numero de l'adresse dans la rue
df_accn.loc[(df_accn[u'v1']==0),u'v1'] =""

df_accn[u'v1']= df_accn[u'v1'].fillna('')
df_accn[u'libellevoie']= df_accn[u'libellevoie'].fillna('')
df_accn[u'Commune']= df_accn[u'Commune'].fillna('')
df_accn[u'Codepos']= df_accn[u'Codepos'].fillna('')

df_accn[u'Codepos']= df_accn[u'Codepos'].apply(lambda x: str(x).zfill(5))

# on retire les lignes de CP non trouvé   (414336, 19)
df_accn = df_accn[df_accn[u'Codepos']!="00000"]
print "df_accn shape Codes postaux corrects ", df_accn.shape
print "codes postaux : "
print df_accn[u'Codepos'].value_counts()


# Nettoyage des caractères bizarres
### regex pour enlever les caractères "bizarres" exemple : GROSSO (JUSQU'AU Nﾰ 58/77) du numacc 15022
df_accn[u'libellevoie']=df_accn[u'libellevoie'].apply(lambda x: re.sub(r"\W"," ",x))


# on crée le champ adresse dans le df pour puvoir grouper dessus
df_accn[u'adresse'] = None 
# On crée des  nouveaux champs lat long /on garde ceux du fichier
df_accn[u'latG'] = None
df_accn[u'longG'] = None

dfshort = df_accn[0:49999]

dfshort = df_accn[15000:15200]
dfvary = df_accn[:][0:40000:200]
print "dfshort shape  ", dfshort.shape

##df_accn = df_accn.apply(lambda x: adresse(x),axis=1)
dfshort = dfshort.apply(lambda x: adresse(x),axis=1)



# # on retrouve lat et long avec API Google
# # df_accn = df_accn.apply('adresse').apply(rech_lat_long)
# dfshort = dfshort.groupby('adresse').apply(rech_lat_long)
# print 'nb adresses : ' len(dfshort.groupby('adresse'))

# Load the SVG map
svg = open('communes.svg', 'r').read()
#svg = open('communes_p.svg', 'r').read()

# Load into Beautiful Soup
soup = BeautifulSoup(svg)
soup2 = BeautifulSoup(svg)
soup3 = BeautifulSoup(svg)

 
# Find counties
paths = soup.findAll('path')
polygons = soup.findAll('polygon')
element_list = paths+polygons
 
paths2 = soup2.findAll('path')
polygons2 = soup2.findAll('polygon')
element_list2 = paths2+polygons2
 
paths3 = soup3.findAll('path')
polygons3 = soup3.findAll('polygon')
element_list3 = paths3+polygons3

# Map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]     # Red-purple
# colors = ["#eff3ff", "#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C"]     # Blue
# colors = ["#f2f0f7", "#cbc9e2", "#9e9ac8", "#6a51a3"]                           # Purple
colors = ["#ffffcc", "#ffeda0", "#fed976", "#feb24c", "#fd8d3c", "#fc4e2a", "#e31a1c", "#bd0026", "#800026"]
 
# Defining style
#path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'
path_style = 'fill:'

def defineColorClass(colvar, colVect):
    #Linear scale
    if colvar > colVect[8]:
        color_class = 8
    elif colvar > colVect[7]:
        color_class = 7
    elif colvar > colVect[6]:
        color_class = 6
    elif colvar > colVect[5]:
        color_class = 5
    elif colvar > colVect[4]:
        color_class = 4
    elif colvar > colVect[3]:
        color_class = 3
    elif colvar > colVect[2]:
        color_class = 2
    elif colvar > colVect[1]:
        color_class = 1
    else:
        color_class = 0

    return color_class


def makeColorMap(element_list,element_list2,element_list3):
    # Color the communes based on variable colvar
    colVectSum = [0,1,5,10,50,100,500,1000,10000]
    colVectCnt = [0,1,5,10,50,100,500,1000,3000]
    colVectBad = [-1,0,2.5,5,10,25,50,75,100]
    dfcount = pd.DataFrame()
    icnt = 0
    for p, p2, p3 in zip(element_list,element_list2,element_list3):

        if not(icnt%100):
            print icnt, p['id']

        codeinsee = p['id'][0:5]
        acBad = 'NaN'
        acBadc = -1

        if (codeinsee.isnumeric()):
            pass
        else:
            print "Non-numeric INSEE: ", p['id']
            codeinsee=codeinsee[0]+'0'+codeinsee[2:5]

        acSum = df_accn[df_accn['INSEE']==int(codeinsee)]['grav'].sum()
        acCnt = df_accn[df_accn['INSEE']==int(codeinsee)]['grav'].count()
        if(acCnt > 10):
            acBad = acSum/acCnt
            acBadc = acBad

        color_class_Sum = defineColorClass(acSum, colVectSum)
        color_class_Cnt = defineColorClass(acCnt, colVectCnt)
        color_class_Bad = defineColorClass(acBadc, colVectBad)

        dfcount.loc[icnt,'commune'] = p['id'][6:]
        dfcount.loc[icnt,'insee'] = codeinsee
        dfcount.loc[icnt,'acSum'] = acSum
        dfcount.loc[icnt,'acCnt'] = acCnt
        dfcount.loc[icnt,'acBad'] = acBad

        #print color_class_Sum, color_class_Cnt, color_class_Bad
        color = colors[color_class_Sum]
        p['style'] = path_style + color

        color = colors[color_class_Cnt]
        p2['style'] = path_style + color

        color = colors[color_class_Bad]
        p3['style'] = path_style + color

        icnt += 1

    return dfcount


dfcount = makeColorMap(element_list,element_list2,element_list3)

# #print soup.prettify()

# correct svg attrs 
aa = soup.svg.attrs
aa[2] = (u'viewBox',aa[2][1])
aa[3] = (u'preserveAspectRatio',aa[3][1])

aa = soup2.svg.attrs
aa[2] = (u'viewBox',aa[2][1])
aa[3] = (u'preserveAspectRatio',aa[3][1])

aa = soup3.svg.attrs
aa[2] = (u'viewBox',aa[2][1])
aa[3] = (u'preserveAspectRatio',aa[3][1])

html = soup.prettify("utf-8")
with open("communes_sum.svg", "wb") as file:
    file.write(html)

html = soup2.prettify("utf-8")
with open("communes_cnt.svg", "wb") as file:
    file.write(html)

html = soup3.prettify("utf-8")
with open("communes_bad.svg", "wb") as file:
    file.write(html)

# on remet le tout dans 1 csv
#df_accn.to_csv('out.csv')
dfshort.to_csv('out_short.csv')
dfcount.to_csv('count.csv')