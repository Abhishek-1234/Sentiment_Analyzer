import nltk
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from nltk.tokenize import sent_tokenize, word_tokenize
from stemming.porter2 import stem
from nltk import WordNetLemmatizer


"""
file_one=open('positive_words.txt','r')
positive = [line.split(',') for line in file_one.readlines()]
positive_list=[]
for sublist in positive:
	for item in sublist:
		item=item.replace('\n','')
		positive_list.append(item)

file_two=open(negative_words,'r')
negative = [line.split(',') for line in file_two.readlines()]
negative_list=[]
for sublist in negative:
	for item in sublist:
		item=item.replace('\n','')
		negative_list.append(item)

"""

class StemAndLemmatise:

	def __init__(self,filename):
		self.filename = filename
		self.list_tweets = []
		self.stemmed_tweets = []
		self.lemma= nltk.WordNetLemmatizer()
	
	def readFile(self):
		df=pd.read_excel(self.filename ,sheet_name="Sheet1")
		self.list_tweets=df['Cleaned_Tweets']
				
	def  processStemming(self,list):
		print('Performing porter2 stemming ... ')
		tweets=[]
		for l in list:
			words=word_tokenize(str(l))
			i=0
			for w in words:
				w=stem(w)
				words[i]=w
				i=i+1
			tweets.append(' '.join(words))
		return tweets	
	
	def processLemmatizer(self,list):
		print('Performing lemmatisation ...')
		tweets = []
		for l in list:
			words = word_tokenize(str(l)) 
			lemmas = [self.lemma.lemmatize(w) for w in words]
			tweets.append(' '.join(lemmas))
		return tweets
	
	def processAll(self):
		#self.stemmed_tweets = self.processStemming(self.list_tweets)
		self.stemmed_tweets = self.processLemmatizer(self.list_tweets)
		self.stemmed_tweets = list(set(self.stemmed_tweets))
		print('Both operations are succesfully completed!!')
		
		
	def writeFile(self):
		rd=pd.DataFrame({'Stemming tweet':self.stemmed_tweets})
		writer=ExcelWriter('Stemmed_DATA.xlsx')
		rd.to_excel(writer,"Sheet1",index=False)
		writer.save()
	
	



	



