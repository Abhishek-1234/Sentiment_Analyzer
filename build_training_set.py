import nltk, sys , pickle
import classifier_helper , os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from classifier_helper import *
from nltk.tokenize import sent_tokenize, word_tokenize


df=pd.read_excel("test_data.xlsx" ,sheet_name="Sheet1")
to_process_data = df['Stemmed tweet']
inpfile = open("sentiment_tweet_list.txt", "r")
line = inpfile.readline()
count = 1
tweetItems = []
opinions = []

while line:    
	count += 1
	splitArr = line.split('|')
	processed_tweet = splitArr[0].strip()
	opinion = splitArr[1].strip()
	tweet_item = processed_tweet, opinion
	if(opinion != 'neutral' and opinion != 'negative' and opinion != 'positive'):
		print('Error with tweet = %s, Line = %s') % (processed_tweet, count)
	tweetItems.append(tweet_item)
	line = inpfile.readline()



#end while loop
featureList = []
tweets = []    
for (words, sentiment) in tweetItems:
	words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
	featureList.extend(words_filtered)
	tweets.append((words_filtered, sentiment))
featureList = list(set(featureList))  


#start extract_features
def extract_features(document):
	document_words = set(document)
	features = {}
	for word in featureList:
		features['contains(%s)' % word] = (word in document_words)
	
	#print(features)
	return features
#end	
	
def getNBTrainedClassifier(classifierDumpFile):
	print('training nb classifier')
	training_set = nltk.classify.apply_features(extract_features, tweets)
	
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	outfile = open(classifierDumpFile, 'wb')        
	pickle.dump(classifier, outfile)        
	outfile.close()
	print ('Accuracy of NB classifier ---> ')
	print(nltk.classify.accuracy(classifier, training_set))

	
		 
  
def getFeatureVector(tweet):
	words_filter = []
	words = word_tokenize(tweet)
	for e in words:
		if(len(e)>=3):
			words_filter.append(e.lower())
	
	return words_filter
		
def TestData(classifier):
	featureVector = []
	print('inside testdata')
	for tweet in to_process_data:
		featureVector = getFeatureVector(tweet)
		#print(featureVector)
		sentiment = classifier.classify(extract_features(featureVector))
		opinions.append(sentiment)
	
	
		
def processNB():
	
	
	classifierDumpFile = 'data/naive_bayes_trained_model.pickle'
	if(os.path.isfile(classifierDumpFile)):
		print('file exist')
		
		if(os.path.getsize(classifierDumpFile) > 0):
			print('Naive bayes classifier already trained')
			f1 = open(classifierDumpFile,'rb')
			classifier = pickle.load(f1)
			f1.close()
			print('classifier opened successfully')
			TestData(classifier)
			print('test data return control')
		else:
			print('elsepart')
		
	else:
		print('trained classifier do not exist')
		inp = input("Would you like to train NB classifier (0/1) ?")
		if(inp == '0'):
			print('You have to do it to get results.')
			sys.exit()
		elif(inp == '1'):
			print('Training classifier...')
			getNBTrainedClassifier(classifierDumpFile)
		else:
			print('wrong choice')
			sys.exit()
		if(os.path.getsize(classifierDumpFile)>0):
			f1 = open(classifierDumpFile,'rb')
			classifier = pickle.load(f1)
			f1.close()
			TestData(classifier)
		
	rd=pd.DataFrame({'Test tweets':to_process_data,'Opinion after NB':opinions})
	writer=ExcelWriter('Naive_result.xlsx')
	rd.to_excel(writer,"Sheet1",index=False)
	writer.save()
	
	print('process completed successfully!!!')

processNB()

'''
tweet = 'im so sad'
print (classifier.classify(extract_features(tweet.split())))
print (nltk.classify.accuracy(classifier, training_set))
classifier.show_most_informative_features(20)
'''