aliments['traces'].dropna()
aliments_with_traces = aliments.ix[aliments.traces.dropna().index]
traces_iter = (set(x.split(',')) for ...)

#Note: toujours uiliser pandas dataframes. cast to dataframe

pd.getdummies(aliments['nutrition_grade_fr'].dropna())
aliments['nutrition_grade_fr'].unique()
aliments['nutrition_grade_fr'].value_counts()
aliments['nutrition_grade_fr'].isnull().sum()
aliments[u'energy_100g'].mean()  ##pandas mean ne compte pas les NaNs

pd.qcut(aliments[u'energy_100g'].dropna(),5)
pd.qcut(aliments[u'energy_100g'].dropna(),5).levels
pd.cut(aliments[u'energy_100g'].dropna(),5)


### pandas join de sql implementee dans pandas
insee1 = pd.read_csv('base-cc-....csv')
pd.merge(insee1,insee2,on='...')
pd.merge(insee1,insee2,right_on='CODGEO')
insee1 = insee1.set_index('CODGEO')


##Series

Series(rihanna).apply(lambda x:regex_video.findall(x))