from textblob import TextBlob
import csv
from models import db, users, feedbackQuestions, feedback

#this file may actually not be needed but keeps things cleaner for now

#thing akram made, guess it just makes the output nicer
def getValues(string):
    strin = TextBlob(string)
    string.correct()
    string.lower()
    return strin

#process all the feedback for a given event, this will be dictated by which event is being accessed though the website??? either way here is just a parameter
def processFeedbackData(eventID)

    #query db for the feedback relating to the given eventID
    #get feedback and feedbackDateTime where event_id == eventID
    #take this and then add the polarity and subjectivity
    #further define a generic metric which is the two combined
    #learn about chart.js in order to make nice graphs


    feedback = []


    feedBackList = []

    #from a previos train of thought, but still somewhat relevant
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

