import sys
import re
import classifier_helper, pickle
import importlib
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

importlib.reload(sys)
sys.setdefaultencoding = 'utf-8'

#start class
class BaselineClassifier:
	""" Classifier using baseline method """
	#variables    
	#start __init__
	def __init__(self, data):
		#Instantiate classifier helper
		#self.helper = classifier_helper.ClassifierHelper('data/feature_list.txt')
		self.lenTweets = len(data)
		self.tweets = []
		self.tweets = data
		self.results = {}
		self.neut_count = [0] * self.lenTweets
		self.pos_count = [0] * self.lenTweets
		self.neg_count = [0] * self.lenTweets
		#self.html = html_helper.HTMLHelper()
	#end
	
	
	
   
	#start classify
	def classify(self):
		#load positive keywords file          
		inpfile = open("data/positive_words.txt", "r")            
		line = inpfile.readline()
		positive_words = []
		while line:
			positive_words.append(line.strip())
			line = inpfile.readline()
			
		#load negative keywords file    
		inpfile = open("data/negative_words.txt", "r")            
		line = inpfile.readline()
		negative_words = []
		while line:
			negative_words.append(line.strip())
			line = inpfile.readline()
			
		#start processing each tweet        
   
		tw = self.tweets
		count = 0
		i=0
		res = {}
		for t in tw:
			
			neg_words = [word for word in negative_words if(self.string_found(word, str(t)))]
			pos_words = [word for word in positive_words if(self.string_found(word, str(t)))]
		
			if(len(pos_words) > len(neg_words)):
				label = 'positive'
				self.pos_count[i] += 1
			elif(len(pos_words) < len(neg_words)):
				label = 'negative'
				self.neg_count[i] += 1
			else:
				if(len(pos_words) > 0 and len(neg_words) > 0):
					label = 'positive'
					self.pos_count[i] += 1
				else:
					label = 'neutral'
					self.neut_count[i] += 1
				
			result = {'text': t, 'label': label}
			self.results[count] = result
			
			count += 1
			i=i+1
			print('again loop')
			
		#end outer loop   
		print('loop end')
		filename = 'data/sentiment_tweet_file'
		outfile = open(filename, 'wb')        
		pickle.dump(self.results, outfile)        
		outfile.close()
		'''
		inpfile = open('data/sentiment_tweet_file')
		self.results = pickle.load(inpfile)
		inpfile.close()
		'''
	#end
	
	#start substring whole word match
	def string_found(self, string1, string2):
		
		if re.search(r"\b" + re.escape(string1) + r"\b", string2):
			print('inside string found')
			return True
		return False
	#end
	
	#start writeOutput
	def writeOutput(self, filename, writeOption='w'):
		fp = open(filename, writeOption)
		tweet = []
		senti = []
		#start loop
		for i in self.results:
			text=str(self.results[i]['text']).strip()
			label=str(self.results[i]['label']).strip()
			#to write excel file
			tweet.append(text)
			senti.append(label)
			
			writeStr = text+" | "+label+"\n"
			fp.write(writeStr)
		#end loop      
		
		rd=pd.DataFrame({'Tweets':tweet,'Sentiment':senti})
		writer=ExcelWriter('Baseline_output.xlsx')
		rd.to_excel(writer,"Sheet1",index=False)
		writer.save()

	#end writeOutput
	
	'''#start printStats
	def getHTML(self):
		return self.html.getResultHTML(self.keyword, self.results, self.time, self.pos_count, \
									   self.neg_count, self.neut_count, 'baseline')
	#end'''
#end class    
