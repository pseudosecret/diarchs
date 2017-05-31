import psycopg2
import random
from random import randrange

connection = None

# Check to see if random point spending will occur
if randrange(5) < 2:
    print("No robot spending points at this time!")
    quit()

# Do random voting
try:
    print("Connecting to database...")
    connection = psycopg2.connect(
        dbname='democracydb', user='exampleuser', password='thiswillnotbelive')
    cursor = connection.cursor()
    print("Picking a robot to spend points...")
    cursor.execute('''
                   SELECT t1.user_id, t1.first_name, t1.last_name, t3.team_id, t4.name, t2.current_points
                   FROM Users AS t1
                   INNER JOIN UserScores AS t2
                   ON t2.user_id = t1.user_id
                   INNER JOIN Users AS t3
                   ON t3.user_id = t1.user_id
                   INNER JOIN Teams AS t4
                   ON t4.team_id = t1.team_id
                   WHERE t2.current_points > 0
                   ORDER BY RANDOM()
                   LIMIT 1;
                   ''')
    result = cursor.fetchone()
    if result == None:
        print("No robots left to spend points!")
        cursor.close()
    else:
        user = result[0]
        user_name = result[1] + " " + result[2]
        team = result[3]
        team_name = result[4]
        points = randrange(1, randrange(1, result[5] + 1))
        if team == 1:
            target_team = random.choice([1, 1, 2])
        else:
            target_team = random.choice([1, 2, 2])
        print("Robot {}, {} of team {}, will spend {} to affect team {}...".format(user, user_name, team, points, target_team))
        if team == target_team:
            # find the required points to win
            cursor.execute('''
                   SELECT current_points, points_to_win
                   FROM TeamPoints
                   WHERE team_id = {};
                   '''.format(team))
            result = cursor.fetchone()
            current_points = result[0]
            points_to_win = result[1]
            # determine if points spent are greater than the points required to win
            # if no refund, spend the points as normal; if they are, reduce points being spent
            refund = max(points - (points_to_win - current_points), 0)
            points_to_spend = points - refund
            print("{} will spend {} of {} points so not to go over...".format(user_name, points_to_spend, points))
            # insert into expenditure, update user's current points
            cursor.execute('''
                           INSERT INTO Expenditures (user_id, user_team_id, target_team_id, amount)
                           VALUES ({}, {}, {}, {});
                           '''.format(user, team, target_team, points_to_spend))
            cursor.execute('''
                           SELECT expenditure_time FROM Expenditures
                           WHERE user_id = {}
                           ORDER BY expenditure_time DESC
                           LIMIT 1;
                           '''.format(user))
            last_activity = cursor.fetchone()[0]
            cursor.execute('''
                           UPDATE UserScores 
                           SET last_activity = '{}', current_points = current_points - {}
                           WHERE user_id = {};
                           '''.format(last_activity, points_to_spend, user))
            cursor.execute('''
                           UPDATE TeamPoints
                           SET current_points = current_points + {}
                           WHERE team_id = {};
                           '''.format(points_to_spend, team))
            # check for victory; if victory, update everything relevant; else nothing.
            if points_to_spend + current_points == points_to_win:
                cursor.execute('''
                               SELECT COUNT(*)
                               FROM UserScores
                               WHERE last_activity::date BETWEEN NOW()::date - INTERVAL '1 DAY' AND NOW()::date
                               ''')
                new_points_goal = cursor.fetchone()[0] * 30 * 7
                cursor.execute('''
                               UPDATE TeamPoints
                               SET current_points = 0, points_to_win = {}
                               WHERE team_id = {};
                               '''.format(new_points_goal, team))
                cursor.execute('''
                               UPDATE Teams
                               SET victories = victories + 1
                               WHERE team_id = {};
                               '''.format(team))
        else:
            # find current points
            # find the required points to win
            cursor.execute('''
                   SELECT current_points
                   FROM TeamPoints
                   WHERE team_id = {};
                   '''.format(target_team))
            current_points = cursor.fetchone()[0]
            # determine if points spent would reduce points below zero
            # if not, spend the points as normal; if they would, reduce points being spent
            refund = max(points - current_points, 0)
            points_to_spend = points - refund
            print("{} will spend {} of {} points so not to go over...".format(user_name, points_to_spend, points))
            if points_to_spend > 0:
                # update user's current points
                cursor.execute('''
                               INSERT INTO Expenditures (user_id, user_team_id, target_team_id, amount)
                               VALUES ({}, {}, {}, 0 - {});
                               '''.format(user, team, target_team, points_to_spend))
                cursor.execute('''
                           SELECT expenditure_time FROM Expenditures
                           WHERE user_id = {}
                           ORDER BY expenditure_time DESC
                           LIMIT 1;
                           '''.format(user))
                last_activity = cursor.fetchone()[0]
                cursor.execute('''
                           UPDATE UserScores 
                           SET last_activity = '{}', current_points = current_points - {}
                           WHERE user_id = {};
                           '''.format(last_activity, points_to_spend, user))
                cursor.execute('''
                               UPDATE TeamPoints
                               SET current_points = current_points - {}
                               WHERE team_id = {};
                               '''.format(points_to_spend, target_team))
        cursor.close()
        connection.commit()
except psycopg2.DatabaseError as exception:
    print(exception)
finally:
    if connection:
        connection.close()