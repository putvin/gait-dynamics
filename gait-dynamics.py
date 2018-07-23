"""
Gait Pattern labels
Control = 1
ALS = 2
Huntington's = 3
Parkinson's = 4
"""

import numpy as np
import os
import math
import pandas as pd
import scipy
import seaborn as sb
import sklearn
from sklearn import model_selection
from sklearn import svm, tree, linear_model, neighbors, naive_bayes, ensemble, discriminant_analysis, gaussian_process
#from xgboost import XGBClassifier
import matplotlib.pyplot as plt


# These values will need to be modified based on the experimental conditions.
samplewindow = 40
address = "C:/Users/Lauren/Documents/DataScience/gaitndd/"
gait = {
        "als" : 2,
        "con" : 1,
        "hun" : 3,
        "par" : 4,
        }
rows = []

# This will need to be modified based upon the sensors that are used.
used_features = ['pfreqw','pmagw', 'meanw', 'pentw', 'rpfreqw', 'rpmagw', 'rmeanw', 'rpentw', 
                 'pfreqra','pmagra', 'meanra', 'pentra', 'rpfreqra', 'rpmagra', 'rmeanra', 'rpentra']

for file in os.listdir(address):
    if file.endswith(".ts"):
        data = pd.read_csv(address + file, sep='\s+', header=None)
        numwindows = divmod(len(data), samplewindow)

        tempf = {
#Create variable for gait and dummy variables for different patterns
                'gait' : gait.get(file[0:3]),
                'control': file[0:3] == 'con',
                'als': file[0:3] == 'als',
                'huntington': file[0:3] == 'hun',
                'parkinson': file[0:3] == 'par'
                }
        
        for i in range(0, numwindows[0]):

            numstart = math.floor(numwindows[1] / 2) + i*samplewindow
            numend = numstart + samplewindow

            tempf['leftstridemean'] = data.loc[numstart:numend,1].mean()
            tempf['leftstridestd'] = data.loc[numstart:numend, 1].std()
            tempf['rightstridemean'] = data.loc[numstart:numend, 2].mean()
            tempf['rightstridestd'] = data.loc[numstart:numend, 2].std()
            tempf['leftswingmean'] = data.loc[numstart:numend, 3].mean()
            tempf['leftswingstd'] = data.loc[numstart:numend, 3].std()
            tempf['rightswingmean'] = data.loc[numstart:numend, 4].mean()
            tempf['rightswingstd'] = data.loc[numstart:numend, 4].std()
            tempf['dsmean'] = data.loc[numstart:numend, 11].mean()
            tempf['dsstd'] = data.loc[numstart:numend, 11].std()
            
# Append to temporary storage.      
            rows.append(tempf)

# Create the dataframe from the rows.       
features = pd.DataFrame.from_dict(rows)
# features['prange'] = features['pmaxw'] - features['pminw']

# Data visualization.
sb.violinplot(x = 'gait', y = 'leftstridestd', data = features)
sb.pairplot(features, hue = 'gait')
plt.matshow(features.corr())