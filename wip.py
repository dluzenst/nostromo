# -*- coding: utf8 -*-
import requests
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import re

import pdb
from datetime import datetime
from dateutil.parser import parse

death_data = pd.read_csv('CausesOfDeath_France_2001-2008.csv')
death_data['Value'] = death_data['Value'].str.replace(' ','')

print death_data.groupby('SEX').size()

print death_data.groupby('TIME','SEX')['VALUE'].sum()