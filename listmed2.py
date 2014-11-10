"""Exercice medicaments"""
# -*- coding: utf8 -*-

import pandas as pd
from pandas import DataFrame, Series
import re
import io

filename = 'MEDICAM 2008-2013-AMELI.xls'
df = pd.io.excel.read_excel(filename, 1)

#find and remove NaN rows at end
nullRows = pd.isnull(df).any(1).nonzero()[0]
df = df.drop(nullRows)
(m,n) = df.shape

#Note:
#df.ix[line] #returns line
#index = df.index #returns index

colNames = df.columns  #noms des colonnes

#colNames[9:15] remboursements 08-13
#derembourses en 2013
df['Deremb'] = (df[colNames[9:14]].sum(axis=1)>0) * (df[colNames[15]]==0)
#rembourses en 2013
df['Remb'] = (df[colNames[9:14]].sum(axis=1)==0) * (df[colNames[15]]>0)

# ## Trouver dosage, forme
# nomCourt = df['NOM COURT']
# produit = df['PRODUIT']
# df['Dosage'] = ''
# df['Forme'] = ''

def getInfo(x):
	a = x['NOM COURT']
	a.replace(x['PRODUIT'],'+++++++++++').strip()
	print a, x['PRODUIT']
	return a

def findDosage(x,regex_dosage):
	result = re.findall(regex_dosage,x)
	if result:
		dosage = result[0]
	else:
		dosage = ['']
	return dosage

nomCourt = df['NOM COURT']
produit = df['PRODUIT']

df2=df['NOM COURT','PRODUIT'].apply(lambda x : getInfo(x),axis=1 )

regex_dosage = re.compile(
	r'(\d{1,},?\d{0,}\s?\w+\/?\d{1,},?\d{0,}\s?\w+|\d{1,},?\d{0,}\s?\w+\/?\w+|\d{1,},?\d{0,}\%)')
df['dosage'] = df2['NOM COURT'].apply(lambda x : findDosage(x,regex_dosage) )

filename = 'medicaments_2.csv'
df.to_csv(filename, encoding='utf-8')