# -*- coding: utf8 -*-

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import re
import pdb
from datetime import datetime
from dateutil.parser import parse

time = '08-10-1998'
date = datetime.strptime(time,'%d-%m-%Y')
datetime.strptime(time,'%d-%m-%Y').year
date_from_parse = parse(time)
date_from_parse2 = parse(time,dayfirst='True')

wiki_data = pd.read_csv('smallwikipedia.csv', sep=';')
wiki_data = wiki_data.drop(0)
wiki_data = wiki_data.set_index('Date')
wiki_data.index = 

wiki_data.resample('M',how='sum').dropna()

pd.date_range('1/1/2000',periods=10, freq='1h30min')


wiki_data.index[0]

wiki_data.index[0].year