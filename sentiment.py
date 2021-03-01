from textblob import TextBlob
import matplotlib.pyplot as plt
import csv 

# call 'message' from feedback table to variable 'feedback'
# now im just using test csv(s)
feedback = []
#with open('C:\\Users\\akram\\Desktop\\TestData\\Feedbacktest.csv', 'r') as ft:
    #read = csv.reader(ft)
    #for row in read:
        #feedback.append(row)
# call 'mood' from "" to variable 'mood'
mood = []
#with open('C:\\Users\\akram\\Desktop\\TestData\\moodtest.csv', 'r') as mt:
    #reader = csv.reader(mt)
    #for row in reader:
        #mood.append(row)
# call 'feedback_date' from "" to variable 'time'
time = []
#with open('C:\\Users\\akram\\Desktop\\TestData\\timetest.csv', 'r') as tt:
    #red = csv.reader(tt)
    #for row in red:
     #   time.append(row)

# function to clean feedback strings
def clean(string):
    strin = TextBlob(string)
    string.correct()
    string.lower()
    return strin

polarity = []
objectivity = []

for fb in feedback:
    f = clean(fb)
        polarity.append(f.sentiment.polarity)
    objectivity.append(1 - f.sentiment.subjectivity)

# Plotting the graph for polarity
plt.plot(polarity, time)

# Plotting the graph for objectivity
plt.plot(objectivity, time)

# Plotting the graph for mood
plt.plot(mood, time)

general = []
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

    general.append(polarity[i]*objectivity[i])

# Plotting the graph for general sentiment
plt.plot(general, time)
