import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import re

credit_cards = 'Thanks for paying with 1098-1203-1233-2354 and with 1212-1234-1265-4566'

## finding digits by 4
cred = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}')
cred = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}')
#find last 2x4digits at end of string
cred = re.compile(r'\d{4}-\d{4}$')


pattern = r'([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})'
##extract email patterns

df = DataFrame
df.columns
df.index
df.index = df.index.map(lambda x: 'Eleve ' + str(x))

df.rename(columns = {0: 'firstname', 1: 'lastname', 2: 'ecole', 3: 'domain'})
df.duplicated('firstname')
df.duplicated().sum
df.drop_duplicates()



