import psycopg2
import random
from random import randrange
import datetime
from datetime import datetime

connection = None

print("It is: {}".format(datetime.now()))
# Check to see if random voting will occur
if randrange(5) < 1:
    print("No robot voting this time!")
    quit()

# Do random voting
try:
    print("Connecting to democracydb...")
    connection = psycopg2.connect(
        dbname='democracydb', user='exampleuser', password='thiswillnotbelive')
    cursor = connection.cursor()
    cursor.execute('''
                   SELECT Users.user_id, Users.first_name, Users.last_name FROM Users
                   LEFT JOIN (SELECT * FROM Votes 
                              WHERE (Votes.time::date - NOW()::date = 0)) AS TodaysVotes 
                   ON TodaysVotes.user_id = Users.user_id
                   WHERE TodaysVotes.user_id IS NULL
                   ORDER BY RANDOM()
                   LIMIT 1;
                   ''')
    result = cursor.fetchone()
    if result == None:
        print("No robots left to vote!")
        cursor.close()
    else:
        user = result[0]
        user_name = result[1] + " " + result[2]
        shape = randrange(1,4)
        print("User: {}, {}, is casting a vote for shape {}.".format(user, user_name, shape))
        cursor.execute('''
                       INSERT INTO Votes (user_id, shape_id)
                       VALUES ({}, {});
                       '''.format(user, shape))
        cursor.execute('''
                       SELECT time FROM Votes
                       WHERE user_id = {}
                       ORDER BY time DESC
                       LIMIT 1;
                       '''.format(user))
        result = cursor.fetchone()
        time_voted = result[0]
        cursor.execute('''
                       UPDATE UserScores 
                       SET last_activity = '{}'
                       WHERE user_id = {}
                       '''.format(time_voted, user))
        cursor.close()
        connection.commit()
except psycopg2.DatabaseError as exception:
    print(exception)
finally:
    if connection:
        connection.close()