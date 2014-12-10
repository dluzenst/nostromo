# -*- coding: utf-8 -*-
"""
@author: Luz
"""

import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt #for plots
#from functionscours8 import LSLassoCV, PredictionError, ScenarioEquiCor, ridge_path
from sklearn.linear_model import LassoCV, RidgeCV
#from functionscours8 import Refitting

import pandas as pd
from sklearn import linear_model
from sklearn.linear_model import lasso_path
#import statsmodels.api as sm
import os

###################################################################################
# Plot initialization
import matplotlib.pyplot as plt #for plots
dirname="../srcimages/"
dirname="./"
imageformat='.jpg'

plt.close('all')


################------ Exercice 2 ------###############################
# Load data
filew = 'winequality-white.csv'
filer = 'winequality-red.csv'

#read table data
dataw = pd.read_csv(filew,sep=';')
datar = pd.read_csv(filer,sep=';')


################------ Exercice 2.1 ------###############################

data = datar
noms = data.columns.values
#data.shape

y = data[noms[11]]
X = data[noms[0:11]]
(nsamples,nfeatures)=X.shape



################------ Exercice 2.1.a ------###############################

mymodel = linear_model.LinearRegression(fit_intercept=True)
mymodel.fit(X,y)
print("2.1.a ) Coefs modele lineaire + intercept")
print([mymodel.coef_ , mymodel.intercept_])

print "2.1.a) Nombre d'observations: ", y.shape[0]



################------ Exercice 2.1.b ------###############################

y_cr = (y-y.mean())/y.std()
X_cr = (X-np.mean(X))/np.std(X)

print "2.1.b) lignes 158, 159, 213 de X_cr\n", X_cr.iloc[[158,159,213]]
print "2.1.b) lignes 158, 159, 213 de y_cr\n", y_cr[[158,159,213]]



################------ Exercice 2.3 ------###############################

data = dataw
noms = data.columns.values
#data.shape

y = data[noms[11]]
X = data[noms[0:11]]
(nsamples,nfeatures)=X.shape

y_cr = (y-y.mean())/y.std()
X_cr = (X-np.mean(X))/np.std(X)

def simpleLasso(X,y,lambdapar,fit_inter):
    #print "simpleLasso: lambdapar = ", lambdapar
    clf = linear_model.Lasso(lambdapar,fit_intercept=fit_inter)
    clf.fit(X, y)
    Yhat = clf.predict(X)
    # print(clf.coef_)
    # print(Yhat)
    return clf.coef_, Yhat

npoints = 25
lend = 1
eps = 1e-4
lstart = lend*eps
alphas = np.logspace(np.log10(lend),np.log10(lstart),npoints)

for alpha in alphas:
    simpLasCoefs, Yhat = simpleLasso(X,y,alpha,True)
    # print "alpha = ", alpha
    # print simpLasCoefs
    # print Yhat
    simpLasCoefsCR, YhatCR = simpleLasso(X_cr,y_cr,alpha,False)
    # print simpLasCoefsCR
    # print YhatCR



################------ Exercice 2.4 ------###############################
print "Ex. 2.4: Figure"
#_, theta_lasso, _ =lasso_path(np.array(X), np.array(y), alphas=alphas,  fit_intercept=True, return_models=False)
_, theta_lasso_CR, _ =lasso_path(np.array(X_cr), np.array(y_cr), alphas=alphas,  fit_intercept=False, return_models=False)

# plot lasso path
# fig1=plt.figure(figsize=(12,8))
# plt.title("Chemin du Lasso: "+ r"$p={0}, n={1} $".format(nfeatures,nsamples),fontsize = 16)
# ax1 = fig1.add_subplot(111)
# ax1.plot(alphas,np.transpose(theta_lasso),linewidth=3)
# ax1.set_xscale('log')
# ax1.set_xlabel(r"$\lambda$")
# ax1.set_ylabel("Amplitude des coefficients")
# ax1.set_ylim([-2,0.5])
# ax1.set_xlim([lstart,lend])
# plt.show(block=False)

fig2=plt.figure(figsize=(12,8))
plt.title("Chemin du Lasso vars_CR: "+ r"$p={0}, n={1} $".format(nfeatures,nsamples),fontsize = 16)
ax1 = fig2.add_subplot(111)
ax1.plot(alphas,np.transpose(theta_lasso_CR),linewidth=3)
ax1.set_xscale('log')
ax1.set_xlabel(r"$\lambda$")
ax1.set_ylabel("Amplitude des coefficients")
ax1.set_ylim([-0.5,0.5])
ax1.set_xlim([lstart,lend])




################------ Exercice 2.5b ------###############################

l_indx = lend
nulvector =  np.zeros(nfeatures)
theta = nulvector
while ((theta == nulvector).all()):
    l_indx = l_indx-0.01
    theta,_ = simpleLasso(X_cr,y_cr,l_indx,False)
    #print l_indx," -- ",theta

print "2.5.b) Lambda_0: Plus petit lambda annulant tous les coefs (à moins de 0.01): ", l_indx


# Test de 25 valeurs ll < Lambda_0
print ("\n Test de %i valeurs" % 25)
for lambdapar in np.linspace(l_indx,lstart,25):
    coefs,_ = simpleLasso(X_cr,y_cr,lambdapar,False)
    print "Lambda: ", lambdapar
    print " Coefs: ", coefs



# plt.show(block=False)
# raise SystemExit

print ("\n 2.5.b) CV type leave-one-out, echantillon taille %i" % nsamples)
import sklearn.cross_validation
loo = sklearn.cross_validation.LeaveOneOut(nsamples)
clf = LassoCV(alphas=alphas,fit_intercept=False,normalize=False,cv=loo)
clf.fit(X_cr, y_cr)
coef_lasso=clf.coef_
print "2.5.b) Lambda déterminé par LassoCV:", clf.alpha_
# plot lasso path with CV choice
ax1.axvline(clf.alpha_, color='K',linestyle='-', linewidth= 3)
plt.annotate('CV',
         xy=(1.1*clf.alpha_,0.2), xycoords='data',
         xytext=(0, 0), textcoords='offset points', fontsize=18)
plt.show(block=False)
filename="lassoCV"
image_name=dirname+filename+imageformat
fig2.savefig(image_name)


################------ Exercice 2.5c ------###############################

xnew = [6,0.3,0.2,6,0.053,25,149,0.9934,3.24,0.35,10]
scorenew = clf.predict(xnew)
print "2.5.c) Prédiction de score pour xnew = \
    [6,0.3,0.2,6,0.053,25,149,0.9934,3.24,0.35,10]: ", scorenew 



################------ Exercice 2.5d ------###############################

mymodel = linear_model.LinearRegression(fit_intercept=False)
mymodel.fit(X_cr,y_cr)
print "coefs des MCOs"
#print ([mymodel.coef_ , mymodel.intercept_])
print (mymodel.coef_)
theta_LR = mymodel.coef_

# mymodel = linear_model.LinearRegression(fit_intercept=True)
# mymodel.fit(X,y)
# print "coefs des MCOs donnees non CR et ordonnee a l'origine"
# print ([mymodel.coef_ , mymodel.intercept_])
# theta_LR = mymodel.coef_


## Somme des carres des erreurs  
## Modele lineaire

ywsfit=mymodel.predict(X_cr)
yws=(y_cr - np.mean(y_cr))/np.std(y_cr)
MSE=(1.0/nsamples)*np.sum((yws-ywsfit)**2)
print "Somme des carrés des erreurs pour la régression linéaire :", MSE

## Somme des carres des erreurs  
## Lasso

# clf = LassoCV(alphas=alphas,fit_intercept=False,normalize=False,cv=loo)
# clf.fit(X_cr, y_cr)
print "coefs du Lasso"
print clf.coef_
ywsfit=clf.predict(X_cr)
yws = y_cr
MSE = (1.0/nsamples)*np.sum((yws-ywsfit)**2)
print "Somme des carrés des erreurs pour la régression Lasso :", MSE
