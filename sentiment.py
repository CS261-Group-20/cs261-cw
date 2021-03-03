from textblob import TextBlob
import csv 

#take from the db
feedback = []
#also take from the db
time = []



def getValues(string):
    strin = TextBlob(string)
    string.correct()
    string.lower()
    return strin

feedBackList = []

#grabs the values for each and shoves into a nice list
for fb in feedback:
    tempList = []
    f = getValues(fb)
    tempList.append(fb)
    tempList.append(f.sentiment.polarity)
    tempList.append(1 - f.sentiment.subjectivity)
    feedBackList.append(tempList)



'''general = []
for i in range(0, len(polarity)-1):
    if polarity[i] <= 0:
        if mood[i] == 0:
            polarity[i] *= 0.75
        elif mood[i] == 1:
            polarity[i] *= 0.5
        else:
            polarity[i] *= 1
    else:
        if mood[i] == 0:
            polarity[i] *= 0.75
        elif mood[i] == -1:
            polarity[i] *= 0.5
        else:
            polarity[i] *= 1

    general.append(polarity[i]*objectivity[i])'''

