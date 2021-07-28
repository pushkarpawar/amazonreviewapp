import pandas as pd
import requests
from bs4 import BeautifulSoup

import warnings
from flask import request,redirect, url_for
warnings.filterwarnings('ignore')

import pickle
import flask

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import matplotlib.colors as colors

from datetime import datetime

import warnings
from scipy import stats
warnings.filterwarnings('ignore')


s = pd.Series([1, 2, 3])
fig, ax = plt.subplots()
s.plot.bar()
plt.savefig('/usr/src/app/templates/rating_distribution.png')

