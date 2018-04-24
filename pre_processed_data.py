import re
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from pandas import ExcelWriter
from pandas import ExcelFile

stopwords=set(stopwords.words('english'))
stopwords.add('__HASH_')
stopwords.add('__HNDL_')
stopwords.add('__URL')
stopwords.add('__PUNC_ELLP')
stopwords.add('__PUNC_EXCL')
stopwords.add('__PUNC_QUES')


class PreprocessData:
	
	def __init__(self,filename):
		
		#file which has initial data
		self.filename = filename
		
		#list that will contain the tweets read from self.filename
		self.listTweetText = []
		
		self.list_cleaned_tweets = []
		
		#Retweet symbol
		self.retweet_regex = re.compile("rt ")
		
		#unknown tags
		self.unknown_tags = re.compile("\b<\S+>\b")	
	
		#Whitespaces multiple
		self.whitespace_regex = re.compile("[\s]+")
		
		#Hashtags
		self.hash_regex= re.compile(r"#(\w+)")		
		
		#Handles:
		self.handl_regex= re.compile(r"@(\w+)")
		
		#URLs:
		self.url_regex=re.compile(r"(http|https|ftp)://[a-zA-Z0-9\./]+")		
		
		#Repeating characters of words:
		self.rpt_regex=re.compile(r"(.)\1{1,}",re.IGNORECASE)

		# Spliting by word boundaries
		self.word_bound_regex = re.compile(r"\W+")
		
		#self.text = ""
		
		'''
		#regex for emoticons
		self.emoticons_regex = [ (repl, re.compile(regex_union(escape_paren(regx))) ) \
						for (repl, regx) in emoticons ]
	
		#Emoticons:
		self.emoticons=\
				[	('__EMOT_SMILEY',	[':-)', ':)', '(:', '(-:', ] )	,\
					('__EMOT_LAUGH',	[':-D', ':D', 'X-D', 'XD', 'xD', ] )	,\
					('__EMOT_LOVE',		['<3', ':\*', ] )	,\
					('__EMOT_WINK',		[';-)', ';)', ';-D', ';D', '(;', '(-;', ] )	,\
					('__EMOT_FROWN',		[':-(', ':(', '(:', '(-:', ] )	,\
					('__EMOT_CRY',		[':,(', ':\'(', ':"(', ':(('] )	,\
				]
		'''
		# Punctuations
		self.punctuations = \
			[	('',		['.', ] )	,\
				('',		[',', ] )	,\
				('',		['\'', '\"', ] )	,\
				('__PUNC_EXCL',		['!', '¡', ] )	,\
				('__PUNC_QUES',		['?', '¿', ] )	,\
				('__PUNC_ELLP',		['...', '…', ] )	,\
				
			]
	
	def retweet_replace(match):
		return ''

	def unknown_tags_replace(match):
		return ''

	def whitespace_replace(match):
		return ' '


	def hash_replace(self,match):
		return '__HASH_ '+match.group(1).upper()


	def handl_replace(self,match):
		return '__HNDL_ '
		

	def url_replace(self,match):
		return '__URL '
		
	def rpt_replace(self,match):
		return match.group(1)+match.group(1)
	'''
	#Printing functions for info
	def print_config(cfg):
		for (x, arr) in cfg:
			print (x, '\t',)
			for a in arr:
				print (a, '\t',)
			print ('')
	'''		
				
	def print_emoticons():
		print_config(emoticons)

	def print_punctuations():
		print_config(punctuations)		

	#For punctuation replacement
	def punctuations_repl(self,match):
		text = match.group(0)
		repl = []
		for (key, parr) in self.punctuations :
			for punc in parr :
				if punc in text:
					repl.append(key)
		if( len(repl)>0 ) :
			return ' '+' '.join(repl)+' '
		else :
			return ' '

	def processHashtags( self,text):
		return re.sub( self.hash_regex, self.hash_replace, text )

	def processHandles( 	self,text):
		return re.sub( self.handl_regex, self.handl_replace, text )

	def processUrls( 		self,text):
		return re.sub( self.url_regex, ' __URL ', text )
	'''
	def processEmoticons( 	self,text):
		for (repl, regx) in self.emoticons_regex :
			text = re.sub(regx, ' '+repl+' ', text)
		return text
	'''	
	def processPunctuations(self,text):
		return re.sub( self.word_bound_regex , self.punctuations_repl, text )
		
	def processRepeatings( 	self,text):
		return re.sub( self.rpt_regex, self.rpt_replace, text )
	
	'''
	def countHandles(self,text):
		return len( re.findall( handl_regex, text) )
		
	def countHashtags(self,text):
		return len( re.findall( hash_regex, text) )
		
	def countUrls(self,text):
		return len( re.findall( url_regex, text) )
		
	def countEmoticons(self,text):
		count = 0
		for (repl, regx) in emoticons_regex :
			count += len( re.findall( regx, text) )
		return count
	'''
	


	
	def processStopwords(self, text):
		words=word_tokenize(text)
		words_filtered=[]
		for w in words:
			if w not in stopwords:
				if(len(w)>2):
					words_filtered.append(w)
				
		return ' '.join(words_filtered)
	
	
	#''', subject='', query=[]''' : part of processAll() function
	def processAll( self,text):

	#	if(len(query)>0):
	#		query_regex = "|".join([ re.escape(q) for q in query])
	#		text = re.sub( query_regex, '__QUER', text, flags=re.IGNORECASE )
	#	for (repl, regx) in emoticons_regex :
	#		text = re.sub(regx, ' '+repl+' ', text)
	#text = text.replace('\'','')
		# FIXME: Jugad

		#text = re.sub( word_bound_regex , punctuations_repl, text )
		
		text = text.lower()
		text = re.sub(self.retweet_regex,'',text)
		text = re.sub(self.unknown_tags,'',text)
		text = re.sub(self.whitespace_regex,' ',text)
		text = self.processHashtags(text)
		text = self.processHandles(text)
		text = self.processUrls(text)
		text = self.processPunctuations(text)
		text = self.processRepeatings(text)
		
		text = self.processStopwords(text)
		text = text.lower()
		return text
	
	def loadAndProcess(self):
		print('Cleaning tweets:')
		df=pd.read_excel(self.filename ,sheet_name="Sheet1")
		self.listTweetText = df['text']
		for t in self.listTweetText:
			stra = str(t)
			
			self.list_cleaned_tweets.append(self.processAll(stra))
			
	def writeOutput(self):
		rd=pd.DataFrame({'Cleaned_Tweets':self.list_cleaned_tweets})
		writer=ExcelWriter('Initial_data.xlsx')
		rd.to_excel(writer,"Sheet1",index=False)
		writer.save()
		print("Cleaning is completed.")

		





