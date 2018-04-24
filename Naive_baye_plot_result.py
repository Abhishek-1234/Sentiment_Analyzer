import pandas as pd
import matplotlib.pyplot as plt
 
df = pd.read_excel("Naive_result.xlsx" ,sheet_name="Sheet1")
opinions = df['Opinion after NB']  

 
def countPosNegNeu():
	countPos = 0
	countNeg = 0
	countNeu = 0
	for sentiment in opinions:
		if(sentiment == 'negative'):
			countNeg = countNeg+1
		elif(sentiment == 'positive'):
			countPos = countPos+1
		elif(sentiment == 'neutral'):
			countNeu = countNeu+1
	return (countPos, countNeg, countNeu)
 
countPos, countNeg, countNeu = countPosNegNeu()

 
# Data to plot
labels = 'Positive', 'Negative', 'Neutral'
sizes = [countPos, countNeg, countNeu]
colors = ['gold', 'lightcoral', 'lightskyblue']
#explode = (0.1, 0, 0, 0)  # explode 1st slice
 
# Plot
plt.pie(sizes, explode=None, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()