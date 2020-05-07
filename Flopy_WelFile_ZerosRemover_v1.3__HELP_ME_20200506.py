"""     Flopy Wel File Zeros Remover -  VERSION 1.3
             Started on 5/5/2020
             Last Updated 5/6/2020 (May 2020, I am American)

@author: Justin A. Clark

This program takes data from an existing MODFLOW Well file and creates a new MODFLOW Well file.
   --The DIS package is created first to initialize the well file data (Stress Periods and Layers).
   --3 text files and an excel file have the data to construct the DIS file.
   --USGS flopy and pandas are the primary libraries used.
"""
import numpy as np
import flopy
import pandas as pd
import sys
import os

#
## Assign name and create modflow model object
modelname = 'Pinal_AMA_SS2015_Flopy_20200505'
# modelname = 'Pinal_AMA_Flopy_20200331'
mf = flopy.modflow.Modflow(modelname, exe_name='mf2005')  ##Same as USGS Example

###### MAKE THE DISCRETIZATION (.dis) FILE ######
## Model domain and grid definition
nlay = 3
nrow = 196
ncol = 222
Lx = 2640*nrow
Ly = 2640*ncol
delr = Lx/nrow
delc = Ly/ncol

#
## Read Top and Bottom Elevations
fn = "Elev_TOP_L1_SV1.txt"
df = pd.read_csv(fn, header = None, sep = r'\t', engine = 'python')      ##header = None is necessary!
s = df.stack()
z = np.array(s)
ztop1 = np.reshape(z,(nrow,ncol))


fn = "Elev_BOT_L1_SV1.txt"
df = pd.read_csv(fn, header = None, sep = r'\t', engine = 'python')      ##header = None is necessary!
s = df.stack()
z = np.array(s)
zbot1 = np.reshape(z,(nrow,ncol))

fn = "Elev_BOT_L2_SV1.txt"
df = pd.read_csv(fn, header = None, sep = r'\t', engine = 'python')      ##header = None is necessary!
s = df.stack()
z = np.array(s)
zbot2 = np.reshape(z,(nrow,ncol))

fn = "Elev_BOT_L3_SV1.txt"
df = pd.read_csv(fn, header = None, sep = r'\t', engine = 'python')      ##header = None is necessary!
s = df.stack()
z = np.array(s)
zbot3 = np.reshape(z,(nrow,ncol))

botm = np.array([zbot1,zbot2,zbot3])

#
## TRIED AND FAILED TO USE A DICTIONARY TO READ IN FILES
# names_ElevsFiles = ['Elev_TOP_L1_SV1.txt','Elev_BOT_L1_SV1.txt','Elev_BOT_L2_SV1.txt','Elev_BOT_L3_SV1.txt']
# names_ElevsVars = ['s_top1', 's_bot1', 's_bot2', 's_bot3']

# d={}
# for x in range(1,10):
#         d["string{0}".format(x)]="Hello"

# Time step parameters
fn = 'Pinal_SS2015_DIS_TimeData_2020.xlsx'
df_time = pd.read_excel(fn)

nper = len(df_time.perlen)
perlen = list(df_time.perlen)
nstp = list(df_time.nstp)
steady = list(df_time.steady)

start_datetimestr = df_time.Start.iloc[0].strftime('%m-%d-%Y') ##Convert 1/1/1923 to string

#
## Create the discretization object
dis = flopy.modflow.ModflowDis(mf, nlay, nrow, ncol, delr=delr, delc=delc,
                               top=ztop1, botm=botm, nper=nper, perlen=perlen, 
                               nstp=nstp, steady=steady, lenuni = int(1), start_datetime=start_datetimestr)
# itmuniint = 4, default value (days)      # lenuniint = 1, feet

pkgs = mf.get_package_list()
mf.write_input()


#
## WELL FILE MAKER
# Read an existing well file and make it into a Wel Object within flopy
wel = flopy.modflow.ModflowWel.load('PM_SS2018_FREE_TEST.wel', mf)

# pkgs = mf.get_package_list()
# mf.write_input()

#
## Recreate the Wel Object with the stress period data extracted from the Wel Object
spd = wel.stress_period_data
df_wel = spd.df   ##Create a dataframe with the extracted Wel Stress Period Data
#wel = flopy.modflow.ModflowWel(mf, stress_period_data=spd)

# pkgs = mf.get_package_list()
# mf.write_input()

#
## WORKING WITH DICTIONARIES IS HARD
lst_wel_SP1 =[]
sp_var = 0 ##UNUSED VARIABLE
for x in range(0,df_wel.shape[0]):
    if df_wel.flux0[x] != 0:
        lst_wel_SP1.append(list([df_wel.k[x], df_wel.i[x], df_wel.j[x], df_wel.flux0[x]]))


lst_wel_SP2 =[]
sp_var = 1 ##UNUSED VARIABLE
for x in range(0,df_wel.shape[0]):
    if df_wel.flux1[x] != 0:
        lst_wel_SP2.append(list([df_wel.k[x], df_wel.i[x], df_wel.j[x], df_wel.flux1[x]]))

lst_wel_SP_X =[]
sp_var = 1
for x in range(0,df_wel.shape[0]):
    col= "flux"+str(sp_var)
    print(df_wel[col])
    if df_wel.flux1[x] != 0:
        lst_wel_SP_X.append(list([df_wel.k[x], df_wel.i[x], df_wel.j[x], df_wel.flux1[x]]))


range_SP = list(range(0,94))

spd_list = []
for y in range_SP:
    spd_list.append(lst_wel_SP2)

spd_list = []
for y in range_SP:
    spd_list.append(lst_wel_SP_X[y])


wel = flopy.modflow.ModflowWel(mf, stress_period_data=wel_dict)
pkgs = mf.get_package_list()
mf.write_input()

##############################################################################
##############################################################################
##############################################################################
#  ### ### ### ### ### #### ### ### ### ### ### #### ### ### ### ### ### ###  #
##   Example and Test Code Used for This Program   ##
"""

"""
###############################################################################
#  ### ### ### ### ### #### ### ### ### ### ### #### ### ### ### ### ### ###  #
##   Websites Visited   ##
"""
https://www2.hawaii.edu/~jonghyun/classes/S18/CEE696/files/18_qna3.pdf

https://stackoverflow.com/questions/5844672/delete-an-element-from-a-dictionary

https://realpython.com/iterate-through-dictionary-python/

https://www.geeksforgeeks.org/python-ways-to-change-keys-in-dictionary/

https://stackoverflow.com/questions/6900955/python-convert-list-to-dictionary

"""
###