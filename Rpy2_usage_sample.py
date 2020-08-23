# -*- coding: utf-8 -*-


import os

#Specify path to R
os.environ['R_HOME']='C:\Program Files/R/R-3.4.2
import pandas as pd
import rpy2
print(rpy2.__version__)
from rpy2.robjects.packages import importr

#Import R objects into python
import rpy2.robjects.packages as rpackages
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

#Activate pands to r translation
pandas2ri.activate
from rpy2.objectsvectors import DataFrame, StrVector, IntVector, ListVector

base = importr('base')

#Import R script in order to load R envinronment (Global Variables)
Imported_R_Envinronment=ro.r('source("path_to_R_file.R")')

#Load particular R function from recently loaded R envinronment as a Python instance function
R_FUN_Loaded=ro.r('R')

def DF_Python_To_R(df,Factor_Cols="Amount","AmountUSD"]):
	#Function which translates Python DataFrame into Python DataFrame
	#Inputs are:
	#-DataFrame wchich is going to to be tranlsted
	#-Columns names whcih feature StringAsFactors equals True
	#The purpose is to avoid issue with rpy2 translation, once StringAsFactors = True columns are turned values are turned into column names
	def df_Str(tab,col):
		return DataFrame({col:base.I(StrVector(tab[col]))})
	#Internal function for columns to be "StringAsFactors=True in R world
	def df_Fac(tab,col):
		return DataFrame({col:base.I(tab[col])})
	
	#Import 'cbind' from R universe
	cbind=ro.r('cbind')
	String_Cols=list(set(list(df)).difference(set(Factor_Cols)))
	R_DF=df_Str(df,String_Cols[0])
	for column in String_Cols[1:]:
		R_DF=cbind(R_DF,df_Str(df,column))
	for column in Factor_Cols:
		R_DF=cbind(R_DF,df_Fac(df ,column))
	return R_DF

#Transform input data frame
R_FUN_output = DF_Python_To_R(Python_Input_DataFrame)

#Call R function on Python DataFrame input
R_DataFrame_Output = R_FUN_Loaded(R_FUN_output)

#Translate results back to Python universe
Python_DataFrame_Output=pandas2ri.ri2py_dataframe(R_DataFrame_Output)
print(Python_DataFrame_Output)

