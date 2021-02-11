DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users(
  UserID 				integer NOT NULL, 
  Username   		varchar(30) NOT NULL,
  Password			varchar(30) NOT NULL,
  PRIMARY KEY		(UserID)
);

DROP TABLE IF EXISTS eventTable CASCADE;
CREATE TABLE eventTable(
  EventID 			integer NOT NULL,
  EventDesc				varchar(30) NOT NULL,
  EventType 			varchar(30) NOT NULL,
  EventStart				date NOT NULL,
  EventEnd 			date NOT NULL,
  EventCompleted 		integer NOT NULL CHECK (EventCompleted == 1 or EventCompleted == 0),
  PRIMARY KEY 			(OrderID)
);

DROP TABLE IF EXISTS eventAttendees CASCADE;
CREATE TABLE eventAttendees(
  UserID			integer NOT NULL,
  EventID			integer NOT NULL,
  PRIMARY KEY 			(UserID, EventID),
  FOREIGN KEY			(UserID) REFERENCES users(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY 			(EventID) REFERENCES eventTable(EventID) ON DELETE CASCADE ON UPDATE CASCADE
    
);

DROP TABLE IF EXISTS eventHosts CASCADE;
CREATE TABLE eventHosts(
  UserID			integer NOT NULL,
  EventID			integer NOT NULL,
  PRIMARY KEY 			(UserID, EventID),
  FOREIGN KEY			(UserID) REFERENCES users(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY 			(EventID) REFERENCES eventTable(EventID) ON DELETE CASCADE ON UPDATE CASCADE
    
);

DROP TABLE IF EXISTS feedback CASCADE;
CREATE TABLE feedback(
  FeedbackID					integer NOT NULL,
  FeedbackQuestionID	integer NOT NULL
  EventID							integer NOT NULL,
  UserID							integer NOT NULL,
  Message							varChar(300) NOT NULL,
  FeedbackDate				date NOT NULL.
  Mood								float NOT NULL.
  Sentiment						float NOT NULL.
  PRIMARY KEY 			(FeedbackID),
  FOREIGN KEY			(UserID) REFERENCES users(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY 			(EventID) REFERENCES eventTable(EventID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY			(FeedbackQuestionID) REFERENCES feedbackQuestions(FeedbackQuestionID) ON DELETE CASCADE ON UPDATE CASCADE
    
);

DROP TABLE IF EXISTS feedbackQuestions CASCADE;
CREATE TABLE feedbackQuestions(
  FeedbackQuestionID			integer NOT NULL,
  FeedbackQuestion			varchar(100) NOT NULL,
  PRIMARY KEY 			(FeedbackQuestionID)
      
);











