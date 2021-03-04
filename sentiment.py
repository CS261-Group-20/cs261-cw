from textblob import TextBlob
import csv
import datetime
from models import db, users, feedbackQuestions, feedback

#this file may actually not be needed but keeps things cleaner for now

#thing akram made, guess it just makes the output nicer
def doAnalysis(string):
    strin = TextBlob(string)
    string.correct()
    string.lower()
    return strin
#calculates the overall general metric
def calcGeneralValue(mood, polarity, subjectivity):
    if mood == 0:
        return ((polarity * (1-subjectivity) * 0.5) * 10)
    elif mood == 1: 
        if polarity > 0: #mood given matches polarity
            return ((polarity * (1-subjectivity)) * 10)
        elif polarity <= 0: #mood given does not match polarity
            return ((polarity * (1-subjectivity) * 0.25) * 10)
    else: #mood = -1
        if polarity < 0: #mood given matches polarity
            return ((polarity * (1-subjectivity)) * 10)
        elif polarity >= 0: #mood given does not match polarity
            return ((polarity * (1-subjectivity) * 0.25) * 10)

def roundTime(dt=None, dateDelta=datetime.timedelta(minutes=1)):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    roundTo = dateDelta.total_seconds()

    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)


def calcAverage(values, chosenColumn):
    total = 0
    for x in range(0, len(values) - 1):
        total += values[chosenColumn]
    return total/len(values)
#process all the feedback for a given event, this will be dictated by which event is being accessed though the website??? either way here is just a parameter
def processFeedbackData(eventID):

    #get feedback and feedbackDateTime where event_id == eventID
    #take this and then add the polarity and subjectivity
    #further define a generic metric which is the two combined
    #learn about chart.js in order to make nice graphs


    feedbackQuery = feedback.query.filter_by(event_id = eventID).all()

    feedBackList = []

    #grabs the values for each and shoves into a nice list
    for x in range(0, len(feedbackQuery)):
        tempList = []
        currentFB = feedbackQuery[x]
        f = doAnalysis(currentFB.message)
        tempList.append(currentFB.feedback_id)
        #tempList.append(currentFB.feedback_date)
        timestamp = datetime.datetime.strptime(currentFB.timestamp, '%Y-%m-%d %H:%M:%S.%f') #database needs modifying
        tempList.append(timestamp)
        tempList.append(currentFB.mood)
        tempList.append(currentFB.message)
        tempList.append(f.sentiment.polarity)
        tempList.append(f.sentiment.subjectivity)
        tempList.append(calcGeneralValue(currentFB.mood, f.sentiment.polarity, f.sentiment.subjectivity))
        feedBackList.append(tempList)
    
    #so in theory there is now a list which it itself is a list of messages, then the values for each message as well as id and date

    #for each list within this list, 0 = id, 1 = timestamp, 2 = mood, 3 = message, 4 = polarity, 5 = subjectivity, 6 = general score

    #make an assumption that entries are added to the database in order, therefore the first added is the start time, and the last added is the current final time
    startTime = feedBackList[0][1]
    endTime = feedBackList[len(feedBackList) - 1][1]

    timeDiff = endTime - startTime
    
    values = []
    labels = []

    if timeDiff < datetime.date(days = 1): #in theory checking if the difference between the two is less than one day, this lets us assume this was a one off event
        #round all of the times to the nearest 10 mins, for all values at the same time, average them
        
        for x in range(0, len(feedBackList) - 1):
            feedBackList[x][1] = roundTime(feedBackList[x][1], datetime.timedelta(minutes=10))
            
            if feedBackList[x][1] != feedBackList[x-1][1]:
                


        #so converted all timestamps to the nearest 10 minutes
