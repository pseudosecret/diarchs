import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

connection = None

# PostgreSQL commands to create the tables
create_users = '''CREATE TABLE Users
      (user_id      SERIAL   PRIMARY KEY  NOT NULL,
      time_regd TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
      team_id       SMALLINT              NOT NULL,
      first_name    TEXT                  NOT NULL,
      last_name     TEXT                  NOT NULL,
      age           SMALLINT              NOT NULL,
      gender_id     SMALLINT              NOT NULL,
      fav_shape_id  SMALLINT                      
      );''' 
create_user_scores = '''CREATE TABLE UserScores
      (user_id      INT     PRIMARY KEY   NOT NULL,
      wins          INT      DEFAULT 0    NOT NULL,
      losses        INT      DEFAULT 0    NOT NULL,
      neutrals      INT      DEFAULT 0    NOT NULL,
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
      time TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
      );'''
create_outcomes = '''CREATE TABLE Outcomes
      (outcome_id   BIGSERIAL PRIMARY KEY NOT NULL,
      date          DATE                  NOT NULL,
      win           INT,
      neutral       INT,
      loss          INT,
      draw          BOOLEAN  DEFAULT FALSE NOT NULL
      );'''
create_expenditures = '''CREATE TABLE Expenditures
      (expenditure_id BIGSERIAL PRIMARY KEY NOT NULL,
      user_id       INT                   NOT NULL,
      user_team_id  SMALLINT              NOT NULL,
      target_team_id SMALLINT             NOT NULL,
      amount        INT                   NOT NULL,
      time TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
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

robots = ['''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Ivan', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Kevin', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Donald', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Marie', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Molly', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Aaron', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Laura', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Wotan', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Ricky', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Patrick', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Millie', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Nevaeh', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Sammy', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Dean', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Ben', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Jerusha', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Dylan', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Forrest', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Giovanni', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Shadow', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Waxwell', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Kefka', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Orpheus', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Meghan', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'James', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Erin', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (1, 'Josh', 'de la Computadora', 0, 4);
          ''',
          '''INSERT INTO Users (team_id, first_name, last_name, age, gender_id)
             VALUES (2, 'Michael', 'de la Computadora', 0, 4);
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
    connection.commit()
    cursor.close()
    print("Finished! :D")
except psycopg2.DatabaseError as exception:
    print(exception)
finally:
    if connection:
        connection.close()