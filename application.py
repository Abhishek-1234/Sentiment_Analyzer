import pandas as pd
import os
from pandas import ExcelWriter
from pandas import ExcelFile
from nltk.sentiment.util import *
from nltk import tokenize

import  pre_processed_data, stem_example \
		,baseline_classifier , prepare_feature_list, split__data

print("\n\t\t\t\tWelcome to sentiment analyzer")
print("\t\t\t\t^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
inp = input("Would you like to clean your data : (0/1) ?")
if(inp == '0'):
	if(os.path.isfile("Initial_data.xlsx")):
		print("\n\tCleaned file already exist :)")
	else:
		print("\n\tBye Bye, See you around !!!")
		sys.exit()
elif(inp == '1'):
	if(os.path.isfile("Initial_data.xlsx")):
		print("\n\tCleaned file already exist :)")
	else:
		print("\n\tworking on it")
		pp=pre_processed_data.PreprocessData("tweets_demonetisation.xlsx")
		pp.loadAndProcess()
		pp.writeOutput()
else:
	print("\nWrong choice")
	sys.exit()
	
	
inp = input("\nWould you like to do further stemming and lemmatisation in your cleaned file (0/1)?")
if(inp == '0'):
	if(os.path.isfile("Stemmed_DATA.xlsx")):
		print("\n\tMore cleaned file already exist :)")
	else:
		print("\n\tBye Bye, See you around !!!")
		sys.exit()
elif(inp == '1'):
	if(os.path.isfile("Stemmed_DATA.xlsx")):
		print("\n\tMore cleaned file already exist :)")
	else:
		print("\n\tworking on it")
		further_cleaning = stem_example.StemAndLemmatise("Initial_data.xlsx")
		further_cleaning.readFile()
		further_cleaning.processAll()
		further_cleaning.writeFile()
else:
	print("\n\tWrong choice")
	sys.exit()
	

print("\nNow apply baseline classifier to check the basic polarity at sentence level using the meaning of words\n")
inp = input("Press 0/1 to continue ... ")

if(inp == '0'):
	if(os.path.isfile("sentiment_tweet_list.txt")):
		print("\n\tBaseline classifier has been already applied. Please Move to next steps :)\n")
	else:
		print("\tSystem exiting now. Visit again !!!\n")
		sys.exit()
elif(inp == '1'):
	if(os.path.isfile("sentiment_tweet_list.txt")):
		print("\tBaseline classifier has been already applied. Please Move to next steps :)\n")
	else:
		print("\tworking on it\n")
		df=pd.read_excel("Stemmed_DATA.xlsx" ,sheet_name = "Sheet1")
		list_tweets=df['Stemming tweet']
		bc=baseline_classifier.BaselineClassifier(list_tweets)
		bc.classify()
		bc.writeOutput('sentiment_tweet_list.txt','w')
else:
	print("\tWrong choice. System exiting now.\n")
	sys.exit()

	
print("Split the data into Train and Test dataset.\n")
inp = input("Press 0/1 to continue ... ")	
if(inp == '0'):
	if(os.path.isfile("Data_to_split.xlsx") and  os.path.isfile("train_data.xlsx") and os.path.isfile("test_data.xlsx")):
		print("\tAll required files already exist. :)\n")
	else:
		print("\tSystem exiting now. Visit again and then press 1 !!!\n")
		sys.exit()
elif(inp == '1'):
	if(os.path.isfile("Data_to_split.xlsx") and os.path.isfile("train_data.xlsx") and os.path.isfile("test_data.xlsx")):
		print("\tAll required files already exist. :)\n")
	else:
		print("\tworking on it\n")
		splitData = split__data.SplitData("sentiment_tweet_list.txt")
		splitData.readAndWriteFile()
		splitData.splitDataset(0.70)
else:
	print("\tWrong choice. System exiting now.")
	sys.exit()

	
print("Prepare feature list from train_data file.\n")
inp = input("Press 0/1 to continue ... ")	
if(inp == '0'):
	if(os.path.isfile("data/feature_list.txt")):
		print("\n\tFeature list is already prepared. Move forward please :)")
	else:
		print("\n\tSystem exiting now. Visit again and then press 1 !!!")
		sys.exit()
elif(inp == '1'):
	if(os.path.isfile("data/feature_list.txt")):
		print("\n\tFeature list is already prepared. Move forward please :)")
	else:
		print("\n\tworking on it")
		df=pd.read_excel("train_data.xlsx" ,sheet_name="Sheet1")
		list_tweets=df['Stemmed tweet']
		word_list=[]
		pfl=prepare_feature_list.PrepareFeatureList(list_tweets)
		feature_list=pfl.getFeatureList()
		pfl.writeOutput('data/feature_list.txt','w')
		print('\n\t\t\tsuccesfully completed feature_list and file has been saved :)')
else:
	print("\tWrong choice. System exiting now.")
	sys.exit()


