import nltk
import sys
import pandas as pd
import importlib
from nltk.tokenize import sent_tokenize, word_tokenize

importlib.reload(sys)
sys.setdefaultencoding = 'utf-8'

class PrepareFeatureList:
	""" FeatureList Class """
	
	#start init
	def __init__(self,data):
		
		self.featureList=[]
		self.tweetsList=data
		
	#end
		
	#start	
	def getFeatureList(self):
		featureList=[]
		for t in self.tweetsList:
			words=word_tokenize(str(t))
			featureList.extend(words)
		
		featureList=list(set(featureList))
		self.featureList=featureList
	#end
	
	#start
	def writeOutput(self, filename , writeoption='w'):
		output=open(filename+'.txt',writeoption)
		for i in self.featureList:
			res=str(i)+"\n"
			output.write(res)
	#end