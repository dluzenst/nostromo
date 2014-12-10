# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 16:55:16 2014

@author: wei he
"""

import pandas as pd
from pandas import DataFrame
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

def cenRedu(column, mean, std, name):
    result = column    
    if std != 0:
        result = (column - mean)/std
    else:
        print "Warning : returning same column ", name
    return result

csv.field_size_limit(sys.maxsize)

dataAcci = pd.read_csv("fic_acc.csv", error_bad_lines=False, low_memory=False)
dataVehi = pd.read_csv("fic_veh.csv", error_bad_lines=False, low_memory=False)

shorten = 0
shortenstep = 50
if(shorten):
    arr_len = dataAcci.shape[0]
    dfAcciShort = dataAcci[0:arr_len:shortenstep]
else:
    dfAcciShort = dataAcci

dfVehicules = DataFrame(dataVehi)

#dataMerge = pd.merge(dfAcciShort, dfVehicules, on='numac')
dataMerge = pd.merge(dfAcciShort, dfVehicules, on='numac')
cols=['lum','agg','anmc','col','atm','int','catr','situ','catv','grav']
dataMerge = dataMerge[cols]

#raise SystemExit
dataMerge = dataMerge[dataMerge['anmc']>1970]
dataMerge = dataMerge[dataMerge['catv']<99]
# 9 ==15
classVeh = {1:'Bicycle',# velos
            2:'2 wheels',# 2 roues< 125cm3
            3:'No-licence car',# voiturette
            4:'Car', # VL seul
            5:'Car + caravan/trailer',# VL avec remorque ou caravane
            6:'Commercial vehicle',# VU avec ou sans remorque
            7:'Van', # PL seul 3.5T < PTCA <=7.5T
            8:'Heavy truck', # PL > 7.5T
            9:'Van/truck + trailer', # PL > 3.5T + remorque
            10:'Tractor',
            11:'Tractor trailer',
            12:'Public transport',
            13:'Tram',
            14:'Special vehicles',
            15:'Agricultural tractor',
            16:'Bigger 2 wheels', # Quad lourd
            17:'Quad', # Quad lourd
            18:'Bus',
            19:'Coach',
            20:'Train'}


dataMerge.loc[(dataMerge['catv']==4), 'catv'] = 2
dataMerge.loc[(dataMerge['catv']==5), 'catv'] = 2
dataMerge.loc[(dataMerge['catv']==6), 'catv'] = 2
dataMerge.loc[(dataMerge['catv']==30), 'catv'] = 2
dataMerge.loc[(dataMerge['catv']==31), 'catv'] = 2
dataMerge.loc[(dataMerge['catv']==32), 'catv'] = 2
dataMerge.loc[(dataMerge['catv']==7), 'catv'] = 4
dataMerge.loc[(dataMerge['catv']==8), 'catv'] = 5
dataMerge.loc[(dataMerge['catv']==9), 'catv'] = 5
dataMerge.loc[(dataMerge['catv']==10), 'catv'] = 6
dataMerge.loc[(dataMerge['catv']==11), 'catv'] = 6
dataMerge.loc[(dataMerge['catv']==12), 'catv'] = 6
dataMerge.loc[(dataMerge['catv']==13), 'catv'] = 7
dataMerge.loc[(dataMerge['catv']==14), 'catv'] = 8
dataMerge.loc[(dataMerge['catv']==15), 'catv'] = 9
dataMerge.loc[(dataMerge['catv']==16), 'catv'] = 10
dataMerge.loc[(dataMerge['catv']==17), 'catv'] = 11
dataMerge.loc[(dataMerge['catv']==18), 'catv'] = 12
dataMerge.loc[(dataMerge['catv']==19), 'catv'] = 13
dataMerge.loc[(dataMerge['catv']==40), 'catv'] = 13
dataMerge.loc[(dataMerge['catv']==20), 'catv'] = 14
dataMerge.loc[(dataMerge['catv']==21), 'catv'] = 15
dataMerge.loc[(dataMerge['catv']==33), 'catv'] = 16
dataMerge.loc[(dataMerge['catv']==34), 'catv'] = 16
dataMerge.loc[(dataMerge['catv']==35), 'catv'] = 17
dataMerge.loc[(dataMerge['catv']==36), 'catv'] = 17
dataMerge.loc[(dataMerge['catv']==37), 'catv'] = 18
dataMerge.loc[(dataMerge['catv']==38), 'catv'] = 19
dataMerge.loc[(dataMerge['catv']==39), 'catv'] = 20


imageformat='.svg'

facteurs = ['lum','agg','anmc','col','atm','int','catr','situ','catv']
factNoms = {'lum':'Luminosity index',
            'agg':'Urban agglomeration type index',
            'anmc':'First year of vehicle circulation',
            'col':'Collision type index',
            'atm':'Atmospheric conditions index',
            'int':'Intersection type index',
            'catr':'Road type index',
            'situ':'Accident emplacement index',
            'catv':'Vehicle type index'}

#facteurs = ['anmc', 'atm']
doSubPlots = 1
if(doSubPlots): fig1=plt.figure(figsize=(18,12))
fig1=plt.figure(figsize=(18,12))
dataMerge_cr = DataFrame()
pltCount = 0
for facteur in facteurs:
    pltCount += 1
    valMax = dataMerge[facteur].max()
    valMin = dataMerge[facteur].min()
    newDF=np.zeros([valMax,3])    
    for i in np.arange(0,valMax):
        myMean = dataMerge[dataMerge[facteur]==i+1]['grav'].mean()
        myStd = dataMerge[dataMerge[facteur]==i+1]['grav'].std()
        #print myMean, myStd
        newDF[i][0] = i+1
        newDF[i][1] = myMean
        newDF[i][2] = myStd
    
    dataMerge_cr0 = (dataMerge[facteur]-dataMerge.describe()[facteur].get('mean'))/dataMerge.describe()[facteur].get('std')
    dataMerge_cr = pd.concat([dataMerge_cr, dataMerge_cr0],axis=1)


    # if(~doSubPlots): 
    #     plt.close('all')
    #     fig1=plt.figure(figsize=(12,8))
    #     ax2 = fig1.add_subplot(111)
    # else:
    #     ax2 = fig1.add_subplot(3,3,pltCount)
    ax2 = fig1.add_subplot(3,3,pltCount)
    
    dataMergePositive = dataMerge[facteur]>0
    ax2.scatter(dataMerge[dataMergePositive][facteur], dataMerge[dataMergePositive]['grav'], alpha=0.3)
    
    ax2.errorbar(newDF[:,0], newDF[:,1],newDF[:,2], fmt='-D',color='red', linewidth=1)
    #ax2.set_xlabel(facteur+" index")
    ax2.set_xlabel(factNoms[facteur])
    ax2.set_ylabel("Accident gravity index")
    ax2.set_ylim([-30,100])
    pExtL = 1; pExtR = 1
    if(valMin <= 0): pExtL = 0
    ax2.set_xlim([valMin-pExtL,valMax+pExtR])
    h1=plt.plot((valMin-pExtL, valMax+pExtR), (0, 0), 'k:')
    #plt.show()
    # if(~doSubPlots):
    #     filename="facteur_"+facteur
    #     #image_name=filename+imageformat
    #     image_name=filename+".png"
    #     fig1.savefig(image_name)

if(doSubPlots): fig1.savefig('allPlots.png')
fig1.savefig('allPlots.png')

facteur = 'grav'
dataMerge_cr0 = (dataMerge[facteur]-dataMerge.describe()[facteur].get('mean'))/dataMerge.describe()[facteur].get('std')
dataMerge_cr = pd.concat([dataMerge_cr, dataMerge_cr0],axis=1)


"""
Notes: 
corr = -0.047389 pour anmc partir de 1970
corr = -0.045755 pour anmc partir de 1985
"""

"""
for i in np.arange(0,valMax):
    myMean = dataMerge[dataMerge['lum']==i+1]['grav'].mean()
    myStd = dataMerge[dataMerge['lum']==i+1]['grav'].std()
    print myMean, myStd
    newDF[i][0] = i+1
    newDF[i][1] = myMean
    newDF[i][2] = myStd

fig1=plt.figure(figsize=(12,8))
ax1 = fig1.add_subplot(111)
#plt.scatter(newDF[:,0], newDF[:,1], alpha=0.5)
ax1.scatter(dataMerge['lum'], dataMerge['grav'], alpha=0.5)
ax1.errorbar(newDF[:,0], newDF[:,1],newDF[:,2])
ax1.set_xlabel("Luminosity index")
ax1.set_ylabel("Accident gravity index")
ax1.set_ylim([-30,100])
ax1.set_xlim([0,6])
plt.show()
"""


# for index in range(1,6):
#     dataMerge = dataMerge[dataMerge['lum']==index]
#     desciption = dataMerge.describe()
    
#     anmc_mean = desciption.anmc.get('mean')
#     anmc_std = desciption.anmc.get('std')
#     tuev_mean = desciption.tuev.get('mean')
#     tuev_std = desciption.tuev.get('std')
#     bgv_mean = desciption.bgv.get('mean')
#     bgv_std = desciption.bgv.get('std')
#     blv_mean = desciption.blv.get('mean')
#     blv_std = desciption.blv.get('std')
#     grav_mean = desciption.grav.get('mean')
#     grav_std = desciption.grav.get('std')
#     dataMerge['anmc_cr'] = cenRedu(dataMerge['anmc'], anmc_mean, anmc_std, 'anmc')
#     dataMerge['tuev_cr'] = cenRedu(dataMerge['tuev'], tuev_mean, tuev_std, 'tuev')
#     dataMerge['bgv_cr']  = cenRedu(dataMerge['bgv'], bgv_mean, bgv_std, 'bgv')
#     dataMerge['blv_cr']  = cenRedu(dataMerge['blv'], blv_mean, blv_std, 'blv')
#     dataMerge['grav_cr'] = cenRedu(dataMerge['grav'], grav_mean, grav_std, 'grav')
#     newDF = dataMerge[['lum','atm','int','dep','grav_cr']]
#     #pd.scatter_matrix(newDF, diagonal='kde', color='k', alpha=0.3)
#     dataMerge.to_csv('dataMerge'+str(index)+'.csv')

