import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import redis
rclient = redis.StrictRedis(host='localhost', port=6379, db=0)

connection = None

# PostgreSQL commands to create the tables
create_users = '''CREATE TABLE Users
      (user_id      SERIAL   PRIMARY KEY  NOT NULL,
      time_regd TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
      team_id       SMALLINT              NOT NULL,
      first_name    TEXT                  NOT NULL,
      last_name     TEXT                  NOT NULL,
      age           SMALLINT              NOT NULL,
      birthdate     DATE                  NOT NULL,
      gender_id     SMALLINT              NOT NULL,
      fav_shape_id  SMALLINT                      
      );''' 
create_user_scores = '''CREATE TABLE UserScores
      (user_id      INT     PRIMARY KEY   NOT NULL,
      wins          INT      DEFAULT 0    NOT NULL,
      losses        INT      DEFAULT 0    NOT NULL,
      neutrals      INT      DEFAULT 0    NOT NULL,
      equals        INT      DEFAULT 0    NOT NULL,
      unequals      INT      DEFAULT 0    NOT NULL,
      draws         INT      DEFAULT 0    NOT NULL,
      current_points INT     DEFAULT 0    NOT NULL,
      total_points  INT      DEFAULT 0    NOT NULL,
      last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
      );'''
create_passwords = '''CREATE TABLE Passwords
      (user_id      INT      PRIMARY KEY  NOT NULL,
      hash          TEXT      DEFAULT ''  NOT NULL,
      salt          TEXT      DEFAULT ''  NOT NULL
      );'''
create_teams = '''CREATE TABLE Teams
      (team_id    SMALLSERIAL PRIMARY KEY NOT NULL,
      name          TEXT                  NOT NULL,
      victories     INT       DEFAULT 0   NOT NULL
      );'''
create_team_points = '''CREATE TABLE TeamPoints
      (team_id      INT PRIMARY KEY       NOT NULL,
      current_points INT    DEFAULT 0     NOT NULL,
      points_to_win INT     DEFAULT 3500  NOT NULL
      );'''
create_genders = '''CREATE TABLE Genders
      (gender_id  SMALLSERIAL PRIMARY KEY NOT NULL,
      name          TEXT                  NOT NULL
      );'''
create_shapes = '''CREATE TABLE Shapes
      (shape_id   SMALLSERIAL PRIMARY KEY NOT NULL,
      name          TEXT                  NOT NULL
      );'''
create_votes = '''CREATE TABLE Votes
      (vote_id     BIGSERIAL PRIMARY KEY  NOT NULL,
      user_id      INT                    NOT NULL,
      shape_id     SMALLINT               NOT NULL,
      vote_time TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
      );'''
create_outcomes = '''CREATE TABLE Outcomes
      (outcome_id   BIGSERIAL PRIMARY KEY NOT NULL,
      vote_date     DATE                  NOT NULL,
      win           INT,
      neutral       INT,
      loss          INT,
      unequal       INT,
      draw          BOOLEAN  DEFAULT FALSE NOT NULL
      );'''
create_expenditures = '''CREATE TABLE Expenditures
      (expenditure_id BIGSERIAL PRIMARY KEY NOT NULL,
      user_id       INT                   NOT NULL,
      user_team_id  SMALLINT              NOT NULL,
      target_team_id SMALLINT             NOT NULL,
      amount        INT                   NOT NULL,
      expenditure_time TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
      );'''
create_faq_helpful = '''CREATE TABLE FaqHelpful
      (faq_vote_id  BIGSERIAL PRIMARY KEY NOT NULL,
      helpful       BOOLEAN               NOT NULL,
      vote_time TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
      );'''

# Populate the tables as needed

teams = ["INSERT INTO Teams (team_id, name) VALUES (1, 'Geraniums');",
         "INSERT INTO Teams (team_id, name) VALUES (2, 'Chrysanthemums');"]

genders = ["INSERT INTO Genders (gender_id, name) VALUES (1, 'Female');",
           "INSERT INTO Genders (gender_id, name) VALUES (2, 'Male');",
           "INSERT INTO Genders (gender_id, name) VALUES (3, 'Nonbinary');"
           "INSERT INTO Genders (gender_id, name) VALUES (4, 'None; AI')"]

shapes = ["INSERT INTO Shapes (shape_id, name) VALUES (1, 'Rock');",
          "INSERT INTO Shapes (shape_id, name) VALUES (2, 'Paper');",
          "INSERT INTO Shapes (shape_id, name) VALUES (3, 'Scissors');"]

robots = ['''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Ivan', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Kevin', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Donald', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Marie', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Molly', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Aaron', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Laura', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Wotan', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Ricky', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Patrick', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Millie', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Nevaeh', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Sammy', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Dean', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Ben', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Jerusha', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Dylan', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Forrest', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Giovanni', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Shadow', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Waxwell', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Kefka', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Orpheus', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Meghan', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'James', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Erin', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (1, 'Josh', 'de la Computadora', -999, NOW()::date, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, birthdate, gender_id)
             VALUES (2, 'Michael', 'de la Computadora', -999, NOW()::date, 4);
          ''']

robot_scores = ['''INSERT INTO UserScores (user_id)
                VALUES (1);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (2);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (3);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (4);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (5);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (6);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (7);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (8);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (9);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (10);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (11);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (12);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (13);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (14);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (15);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (16);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (17);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (18);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (19);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (20);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (21);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (22);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (23);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (24);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (25);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (26);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (27);
                ''',
                '''INSERT INTO UserScores (user_id)
                 VALUES (28);
                ''']

try:
    # Connect and create the DB to work on
    print("Connecting to database to create democracydb...")
    connection = psycopg2.connect(dbname='postgres', user='exampleuser', password='thiswillnotbelive')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    print("Creating fresh database: democracydb")
    cursor.execute("DROP DATABASE IF EXISTS democracydb;")
    cursor.execute("CREATE DATABASE democracydb;")
    cursor.close()
    connection.close()
    rclient.flushall()
    # Reconnect to database
    print("Connecting to democracydb...")
    connection = psycopg2.connect(
        dbname='democracydb', user='exampleuser', password='thiswillnotbelive')
    cursor = connection.cursor()
    # Create the tables
    print("Creating table 'Users'...")
    cursor.execute(create_users)
    print("Creating table 'UserScores'...")
    cursor.execute(create_user_scores)
    print("Creating table 'Passwords'...")
    cursor.execute(create_passwords)
    print("Creating table 'Teams'...")
    cursor.execute(create_teams)
    print("Creating table 'TeamPoints'...")
    cursor.execute(create_team_points)
    print("Creating table 'Genders'...")
    cursor.execute(create_genders)
    print("Creating table 'Shapes'...")
    cursor.execute(create_shapes)
    print("Creating table 'Votes'...")
    cursor.execute(create_votes)
    print("Creating table 'Outcomes'...")
    cursor.execute(create_outcomes)
    print("Creating table 'Expenditures'...")
    cursor.execute(create_expenditures)
    # Populate the Teams, Genders, Shapes, and Users tables
    print("Populating table 'Teams'...")
    for i in teams:
        cursor.execute(i)
    print("Populating table 'Genders'...")
    for i in genders:
        cursor.execute(i)
    print("Populating table 'Shapes'...")
    for i in shapes:
        cursor.execute(i)
    print("Populating table 'Users'...")
    for i in robots:
        cursor.execute(i)
    print("Populating table 'UserScores'...")
    for i in robot_scores:
        cursor.execute(i)
    # Setting all of the redis keys to 0
    print("Setting all of the redis database's keys to zero...")
    # basic stuff
    rclient.set("rock_votes", 0)
    rclient.set("paper_votes", 0)
    rclient.set("scissors_votes", 0)
    rclient.set("t1_points", 0)
    rclient.set("t2_points", 0)
    rclient.set("t1_goal", 3500)
    rclient.set("t2_goal", 3500)
    # note: the following redis can be skipped
    # or deleted if the statistics_update.py is
    # run. anyway...
    # yesterday, past week, past month, all time
    rclient.set("YESTERDAY_rock", 0)
    rclient.set("YESTERDAY_paper", 0)
    rclient.set("YESTERDAY_scissors", 0)
    rclient.set("PASTWEEK_rock", 0)
    rclient.set("PASTWEEK_paper", 0)
    rclient.set("PASTWEEK_scissors", 0)
    rclient.set("PAST30_rock", 0)
    rclient.set("PAST30_paper", 0)
    rclient.set("PAST30_scissors", 0)
    rclient.set("ALLTIME_rock", 0)
    rclient.set("ALLTIME_paper", 0)
    rclient.set("ALLTIME_scissors", 0)
    # Votes by team
    rclient.set("TEAM1_rock", 0)
    rclient.set("TEAM1_paper", 0)
    rclient.set("TEAM1_scissors", 0)
    rclient.set("TEAM2_rock", 0)
    rclient.set("TEAM2_paper", 0)
    rclient.set("TEAM2_scissors", 0)
    # Votes by age
    rclient.set("AGE0-18_rock", 0)
    rclient.set("AGE0-18_paper", 0)
    rclient.set("AGE0-18_scissors", 0)
    rclient.set("AGE19-36_rock", 0)
    rclient.set("AGE19-36_paper", 0)
    rclient.set("AGE19-36_scissors", 0)
    rclient.set("AGE37-52_rock", 0)
    rclient.set("AGE37-52_paper", 0)
    rclient.set("AGE37-52_scissors", 0)
    rclient.set("AGE53-72_rock", 0)
    rclient.set("AGE53-72_paper", 0)
    rclient.set("AGE53-72_scissors", 0)
    rclient.set("AGE73PLUS_rock", 0)
    rclient.set("AGE73PLUS_paper", 0)
    rclient.set("AGE73PLUS_scissors", 0)
    # Votes by time
    rclient.set("TIME00-02_votes", 0)
    rclient.set("TIME02-04_votes", 0)
    rclient.set("TIME04-06_votes", 0)
    rclient.set("TIME06-08_votes", 0)
    rclient.set("TIME08-10_votes", 0)
    rclient.set("TIME10-12_votes", 0)
    rclient.set("TIME12-14_votes", 0)
    rclient.set("TIME14-16_votes", 0)
    rclient.set("TIME16-18_votes", 0)
    rclient.set("TIME18-20_votes", 0)
    rclient.set("TIME20-22_votes", 0)
    rclient.set("TIME22-24_votes", 0)
    # votes for specific shapes by time
    rclient.set("TIME00-02_rock", 0)
    rclient.set("TIME00-02_paper", 0)
    rclient.set("TIME00-02_scissors", 0)
    rclient.set("TIME02-04_rock", 0)
    rclient.set("TIME02-04_paper", 0)
    rclient.set("TIME02-04_scissors", 0)
    rclient.set("TIME04-06_rock", 0)
    rclient.set("TIME04-06_paper", 0)
    rclient.set("TIME04-06_scissors", 0)
    rclient.set("TIME06-08_rock", 0)
    rclient.set("TIME06-08_paper", 0)
    rclient.set("TIME06-08_scissors", 0)
    rclient.set("TIME08-10_rock", 0)
    rclient.set("TIME08-10_paper", 0)
    rclient.set("TIME08-10_scissors", 0)
    rclient.set("TIME10-12_rock", 0)
    rclient.set("TIME10-12_paper", 0)
    rclient.set("TIME10-12_scissors", 0)
    rclient.set("TIME12-14_rock", 0)
    rclient.set("TIME12-14_paper", 0)
    rclient.set("TIME12-14_scissors", 0)
    rclient.set("TIME14-16_rock", 0)
    rclient.set("TIME14-16_paper", 0)
    rclient.set("TIME14-16_scissors", 0)
    rclient.set("TIME16-18_rock", 0)
    rclient.set("TIME16-18_paper", 0)
    rclient.set("TIME16-18_scissors", 0)
    rclient.set("TIME18-20_rock", 0)
    rclient.set("TIME18-20_paper", 0)
    rclient.set("TIME18-20_scissors", 0)
    rclient.set("TIME20-22_rock", 0)
    rclient.set("TIME20-22_paper", 0)
    rclient.set("TIME20-22_scissors", 0)
    rclient.set("TIME22-24_rock", 0)
    rclient.set("TIME22-24_paper", 0)
    rclient.set("TIME22-24_scissors", 0)
    # Votes by gender
    rclient.set("GENDER1_rock", 0)
    rclient.set("GENDER1_paper", 0)
    rclient.set("GENDER1_scissors", 0)
    rclient.set("GENDER2_rock", 0)
    rclient.set("GENDER2_paper", 0)
    rclient.set("GENDER2_scissors", 0)
    rclient.set("GENDER3_rock", 0)
    rclient.set("GENDER3_paper", 0)
    rclient.set("GENDER3_scissors", 0)
    rclient.set("GENDER4_rock", 0)
    rclient.set("GENDER4_paper", 0)
    rclient.set("GENDER4_scissors", 0)
    # Victory Loss Neutral Unequal Equal by shape 
    rclient.set("VLNUE_draw", 0)
    rclient.set("VLNUEVICTORY_rock", 0)
    rclient.set("VLNUEVICTORY_paper", 0)
    rclient.set("VLNUEVICTORY_scissors", 0)
    rclient.set("VLNUELOSS_rock", 0)
    rclient.set("VLNUELOSS_paper", 0)
    rclient.set("VLNUELOSS_scissors", 0)
    rclient.set("VLNUENEUTRAL_rock", 0)
    rclient.set("VLNUENEUTRAL_paper", 0)
    rclient.set("VLNUENEUTRAL_scissors", 0)
    rclient.set("VLNUEUNEQUAL_rock", 0)
    rclient.set("VLNUEUNEQUAL_paper", 0)
    rclient.set("VLNUEUNEQUAL_scissors", 0)
    rclient.set("VLNUEEQUAL_rock", 0)
    rclient.set("VLNUEEQUAL_paper", 0)
    rclient.set("VLNUEEQUAL_scissors", 0)
    # Victory Loss Neutral Unequal Equal by team
    rclient.set("VLNUEDRAWTEAM_1", 0)
    rclient.set("VLNUEDRAWTEAM_2", 0)
    rclient.set("VLNUEVICTORYTEAM_1", 0)
    rclient.set("VLNUEVICTORYTEAM_2", 0)
    rclient.set("VLNUELOSSTEAM_1", 0)
    rclient.set("VLNUELOSSTEAM_2", 0)
    rclient.set("VLNUENEUTRALTEAM_1", 0)
    rclient.set("VLNUENEUTRALTEAM_2", 0)
    rclient.set("VLNUEUNEQUALTEAM_1", 0)
    rclient.set("VLNUEUNEQUALTEAM_2", 0)
    rclient.set("VLNUEEQUALTEAM_1", 0)
    rclient.set("VLNUEEQUALTEAM_2", 0)
    connection.commit()
    cursor.close()
    print("Finished! :D")
except psycopg2.DatabaseError as exception:
    print(exception)
finally:
    if connection:
        connection.close()