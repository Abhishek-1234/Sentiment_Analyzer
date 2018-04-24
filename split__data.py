import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


#start class
class SplitData:
	
	#start init
	def __init__(self,file_name):
		
		self.inpfile = open(file_name, "r")
		self.tweetItems = []
		self.opinions = []
		self.train_1 = []
		self.train_2 = []
		self.test_1 = []
		self.test_2 = []	
		
	#end

	def readAndWriteFile(self):
		line = self.inpfile.readline()
		while line:    
			splitArr = line.split('|')
			self.tweetItems.append(splitArr[0].strip())
			self.opinions.append(splitArr[1].strip())
			line = self.inpfile.readline()
			
		rd=pd.DataFrame({'User_tweet':self.tweetItems, 'Opinion':self.opinions})
		writer=ExcelWriter('Data_to_split.xlsx')
		rd.to_excel(writer,"Sheet1",index=False)
		writer.save()
	
	
	#start
	def splitDataset(self,splitRatio):
		trainSize = int(len(self.tweetItems)*splitRatio)
		i=0
		for tweet in self.tweetItems:
			if(i > trainSize):
				self.test_1.append(tweet)
				self.test_2.append(self.opinions[i])
			else:
				self.train_1.append(tweet)
				self.train_2.append(self.opinions[i])
			i=i+1
		
		
		rd = pd.DataFrame({'Stemmed tweet':self.train_1, 'Opinion':self.train_2})
		writer = ExcelWriter('train_data.xlsx')
		rd.to_excel(writer,"Sheet1",index=False)
		writer.save()
		
		rd1 = pd.DataFrame({'Stemmed tweet':self.test_1, 'Opinion':self.test_2})
		writer1 = ExcelWriter('test_data.xlsx')
		rd1.to_excel(writer1,"Sheet1",index=False)
		writer1.save()
	#end	
		
		

#end class
'''		
#this portion of code executes the Data_to_split.xlsx file to split it into train and test dataset
df=pd.read_excel("Data_to_split.xlsx" ,sheet_name="Sheet1")
dataset = df['User_tweet']
sentiments =df['Opinion']
	
splitDataset(dataset, 0.70)
'''