# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 16:17:06 2019

@author: Callum Wayman

Example of Principal Components Analysis (PCA)

Dataset: Water chemistry data from several surface water and groundwater sites in central Pennsylvania. 
The sites include two sets of surface water and groundwater samples from two different continuously monitored catchments. The 
remaining sample sites are three surface water locations along a larger stream, and precipitation data retrieved from 
National Atmospheric Deposition Program (NADP). 

Each site was sampled over a period of time, so each pair of calculated principal components corresponds to a specific day at
a specific sampling site. 

"""

#%%
#Package Import
'''Relevant packages are imported for PCA calculations and data visualization'''

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler

from sklearn.preprocessing import Imputer

imputer = Imputer()

#%%
#File Input and Data Frame Creation
'''Selecting the file from the correct path and creating a pandas dataframe from the excel file'''

user = 'Callum Wayman'

filename = 'PCA_Data.xlsx'

data_file = pd.ExcelFile(os.getcwd()+'\\'+filename)

dat_df = pd.read_excel(data_file)

#%%
#Data Processing
'''Here the relevant features (analytes) are selected to calculate principal components for each sampling date and site, and for each of 
these features, nan values are replaced with mean values for that feature at the corresponding site'''

#features variable is the assignment of selected analytes to be included in pca
features = ['Analyte 1','Analyte 2','Analyte 3','Analyte 4','Analyte 5','Analyte 6','Analyte 7','Analyte 8','Analyte 9','Analyte 10']
#sites variable is the assignment of sites that will be analyzed in pca
sites = ['WShed1_SW', 'WShed1_GW', 'WShed2_SW','WShed2_GW1','WShed2_GW2','WShed3_SW','WShed3_GW','StreamSite_1','StreamSite_2','StreamSite_3','Precipitation']

'''The nan_mean_fill function is used to replace nan values in the dataframe. nan values can not be in the dataframe 
in which principal components are calculated. Although this code uses mean values for nan replacement, zeros, minimums,
and maximums can also be used. The function cycles through each analyte and each site within the dataframe. The given site
is then used to create a site_index variable which is the index locations for that site within the larger dataframe. The given index range for that analyte
and site is then checked to see if size is greater than 1. If the size is not greater than 1, then a mean value can not be calculated for the nan points.
Finally, nan values are replaced the the new dataframe is eventually returned after all site and analyte combinations are iterated through.'''

def nan_mean_fill(df,features,sites):
    for feat in features:
        for site in sites:
            site_index = df.loc[df['Site'] == site].index
            if np.array(df.loc[site_index,feat]).size > 1:
                if df.loc[site_index,feat].isnull().any() == True:
                    df.loc[site_index,feat] = df.loc[site_index,feat].fillna(df.loc[site_index,feat].mean(),inplace=False) 
                else:
                    pass
    return(df)

dat_df = nan_mean_fill(dat_df,features,sites)

#%%
#PCA and Factor Analysis calculations

#Comment this section

#x is the variable created to hold the array where the rows represent sampling dates at distinct sites, and columns reprent selected analytes
x = dat_df.loc[:, features].values

#The following four lines calculate two principal components for each sampling date, and the array of principal components is inserted into a new dataframe
x = StandardScaler().fit_transform(x)

pca = PCA(n_components = 2)

principalComponents = pca.fit_transform(x)

principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])

#These four lines calculate the factors corresponding to each principal component. These factors represent the primary analytes controlling variation in each principal component
fa = FactorAnalysis(1)

fa.n_components = 2

fa.fit(x)

fa_df = pd.DataFrame(data = fa.components_, columns = features)

fa_df['Principal Components'] = pd.Series([1,2])
cols = ['Principal Components','Analyte 1','Analyte 2','Analyte 3','Analyte 4','Analyte 5','Analyte 6','Analyte 7','Analyte 8','Analyte 9','Analyte 10']

fa_df_new = fa_df[cols]
#%%
#Visualizing data

#finalDf is the finalized dataframe which will be used to plot data. 
#It is the array of principal components with corresponding site and season columns added to identify principal components
finalDf = pd.concat([principalDf, dat_df[['Site']], dat_df[['Season']]], axis =1)

plt.close('all')

#Set the y and x axes limits

#ymin = -6
#ymax = 4
#
#xmin = -3
#xmax = 6

#Fontsize variables for title (fsT), axis labels (fsa), and tick labels (fst).
fsT = 20
fst = 16
fsa = 16

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = fsa)
ax.set_ylabel('Principal Component 2', fontsize = fsa)
ax.set_title('',fontsize = fsT)
#ax2.set_ylim(ymin,ymax)
#ax2.set_xlim(xmin,xmax)

sites = ['WShed1_SW', 'WShed1_GW', 'WShed2_SW','WShed2_GW1','WShed2_GW2','WShed3_SW','WShed3_GW','StreamSite_1','StreamSite_2','StreamSite_3','Precipitation']
ecolors = [(0,0.3,0.7), (0,0.3,0.7), (0,0.6,0), (0,0.6,0), (0,0.6,0),(1,0.5,0), (1,0.5,0),'k','k','k',(0,0.6,1)]
fcolors = ['none', (0,0.3,0.7), 'none', (0,0.6,0), (0,0.6,0),'none', (1,0.5,0),'k','none','none',(0,0.6,1)]
markers = ['o','o','o','o','*','o','o','+','^','s','o']
i = 1
for site, ecolor, fcolor, marker in zip(sites,ecolors, fcolors, markers):
    indicesToKeep = finalDf['Site'] == site
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , edgecolor = ecolor
               , facecolor = fcolor
               , s = 100
               , linewidth = 1
               , marker = marker
               , zorder = i)
    i += 1
ax.legend(sites,frameon=True, facecolor = 'w',edgecolor = 'k')
plt.xticks(fontsize = fst)
plt.yticks(fontsize = fst)


#%%
#Data Output

#Specify file name that will contain pca and fa results
output_file_name = 'PCA_FA_Output_Data'
#Choose file output type
file_type = 'xlsx'

writer = pd.ExcelWriter(os.getcwd()+'\\'+ output_file_name + '.' + file_type, engine = 'xlsxwriter')

finalDf.to_excel(writer,sheet_name = 'PCA Values')
fa_df_new.to_excel(writer,sheet_name = 'Factor Analysis')

writer.save()





