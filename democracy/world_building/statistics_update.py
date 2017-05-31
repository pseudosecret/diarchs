import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import redis
rclient = redis.StrictRedis(host='localhost', port=6379, db=0)

rps_votes_yesterday = '''SELECT  (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 1
	        AND vote_time::date = NOW()::date - INTERVAL '1 DAY') AS rock,
	        (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 2
	        AND vote_time::date = NOW()::date - INTERVAL '1 DAY') AS paper,
	        (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 3
	        AND vote_time::date = NOW()::date - INTERVAL '1 DAY') AS scissors;
            '''
rps_votes_last_week = '''SELECT  (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 1
	        AND vote_time::date < NOW()::date
	        AND vote_time::date >= NOW()::date - INTERVAL '8 DAY') AS rock,
	        (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 2
	        AND vote_time::date < NOW()::date
	        AND vote_time::date >= NOW()::date - INTERVAL '8 DAY') AS paper,
	        (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 3
	        AND vote_time::date < NOW()::date
	        AND vote_time::date >= NOW()::date - INTERVAL '8 DAY') AS scissors;
            '''
rps_votes_past30 = '''SELECT  (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 1
	        AND vote_time::date < NOW()::date
	        AND vote_time::date >= NOW()::date - INTERVAL '31 DAY') AS rock,
	        (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 2
	        AND vote_time::date < NOW()::date
	        AND vote_time::date >= NOW()::date - INTERVAL '31 DAY') AS paper,
	        (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 3
	        AND vote_time::date < NOW()::date
	        AND vote_time::date >= NOW()::date - INTERVAL '31 DAY') AS scissors;
            '''
rps_votes_all_time = '''SELECT  (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 1) AS rock,
	        (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 2) AS paper,
	        (SELECT COUNT(*) FROM Votes
	        WHERE shape_id = 3) AS scissors;
            '''
rps_votes_team = '''SELECT 1 AS team_id,
            (SELECT COUNT(*) FROM Votes
            INNER JOIN Users
            ON Users.user_id = Votes.user_id
            WHERE team_id = {}
            AND shape_id = 1) AS rock,
            (SELECT COUNT(*) FROM Votes
            INNER JOIN Users
            ON Users.user_id = Votes.user_id
            WHERE team_id = {}
            AND shape_id = 2) AS paper,
            (SELECT COUNT(*) FROM Votes
            INNER JOIN Users
            ON Users.user_id = Votes.user_id
            WHERE team_id = {}
            AND shape_id = 3) AS scissors;
'''
rps_votes_by_age = '''SELECT  (SELECT COUNT(*) FROM Votes
	        INNER JOIN Users
	        ON Users.user_id = Votes.user_id
	        WHERE shape_id = 1
	        AND age >= {}
	        AND age <= {}) AS rock_rangex_to_y,
	        (SELECT COUNT(*) FROM Votes
	        INNER JOIN Users
	        ON Users.user_id = Votes.user_id
	        WHERE shape_id = 2
	        AND age >= {}
	        AND age <= {}) AS paper_rangex_to_y,
	        (SELECT COUNT(*) FROM Votes
	        INNER JOIN Users
	        ON Users.user_id = Votes.user_id
	        WHERE shape_id = 3
	        AND age >= {}
	        AND age <= {}) AS scissors_rangex_to_y;
'''
rps_votes_by_gender = '''SELECT 1 AS gender_id,
	    (SELECT COUNT(*) FROM Votes
	    INNER JOIN Users
	    ON Users.user_id = Votes.user_id
	    WHERE gender_id = {}
	    AND shape_id = 1) AS rock,
	    (SELECT COUNT(*) FROM Votes
	    INNER JOIN Users
	    ON Users.user_id = Votes.user_id
	    WHERE gender_id = {}
	    AND shape_id = 2) AS paper,
	    (SELECT COUNT(*) FROM Votes
	    INNER JOIN Users
	    ON Users.user_id = Votes.user_id
	    WHERE gender_id = {}
	    AND shape_id = 3) AS scissors;
        '''
vlnue_each_shape = '''SELECT  (SELECT COUNT(*) FROM Outcomes
	        WHERE draw = TRUE
	        AND unequal IS NULL) AS draws,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE win = 1) AS rock_wins,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE neutral = 1) AS rock_neutrals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE loss = 1) AS rock_neutrals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE unequal = 1) AS rock_unequals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE draw = TRUE
	        AND unequal != 1) AS rock_equals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE win = 2) AS paper_wins,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE neutral = 2) AS paper_neutrals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE loss = 2) AS paper_neutrals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE unequal = 2) AS paper_unequals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE draw = TRUE
	        AND unequal != 2) AS paper_equals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE win = 3) AS scissors_wins,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE neutral = 3) AS scissors_neutrals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE loss = 3) AS scissors_neutrals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE unequal = 3) AS scissors_unequals,
	        (SELECT COUNT(*) FROM Outcomes
	        WHERE draw = TRUE
	        AND unequal != 3) AS scissors_equals;
            '''
vlnue_for_team_1 = '''SELECT 
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 1
	AND draw = TRUE
	AND unequal IS NULL) AS team_1_draws,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 1
	AND win = shape_id) AS team_1_wins,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 1
	AND loss = shape_id) AS team_1_losses,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 1
	AND neutral = shape_id) AS team_1_neutrals,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 1
	AND draw = TRUE
	AND unequal = shape_id) AS team_1_unequals,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 1
	AND draw = TRUE
	AND unequal != shape_id) AS team_1_equals;
'''
vlnue_for_team_2 = '''SELECT 
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 2
	AND draw = TRUE
	AND unequal IS NULL) AS team_2_draws,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 2
	AND win = shape_id) AS team_2_wins,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 2
	AND loss = shape_id) AS team_2_losses,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 2
	AND neutral = shape_id) AS team_2_neutrals,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 2
	AND draw = TRUE
	AND unequal = shape_id) AS team_2_unequals,
	(SELECT COUNT(*) FROM Outcomes
	INNER JOIN Votes
	ON vote_time::date = vote_date
	INNER JOIN Users
	ON Votes.user_id = Users.user_id
	WHERE team_id = 2
	AND draw = TRUE
	AND unequal != shape_id) AS team_2_equals;
'''
time_of_votes = '''SELECT  (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '00:00:00'
	        AND vote_time::time < '02:00:00') AS zero_to_two,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '02:00:00'
	        AND vote_time::time < '04:00:00') AS two_to_four,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '04:00:00'
	        AND vote_time::time < '06:00:00') AS four_to_six,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '06:00:00'
	        AND vote_time::time < '08:00:00') AS six_to_eight,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '08:00:00'
	        AND vote_time::time < '10:00:00') AS eight_to_ten,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '10:00:00'
	        AND vote_time::time < '12:00:00') AS ten_to_twelve,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '12:00:00'
	        AND vote_time::time < '14:00:00') AS twelve_to_fourteen,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '14:00:00'
	        AND vote_time::time < '16:00:00') AS fourteen_to_sixteen,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '16:00:00'
	        AND vote_time::time < '18:00:00') AS sixteen_to_eighteen,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '18:00:00'
	        AND vote_time::time < '20:00:00') AS eighteen_to_twenty,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '20:00:00'
	        AND vote_time::time < '22:00:00') AS twenty_to_twentytwo,
	        (SELECT COUNT(*) FROM votes
	        WHERE vote_time::time >= '22:00:00'
	        AND vote_time::time < '24:00:00') AS twentytwo_to_twentyfour;
'''







try:
    print("Connecting to democracydb...")
    connection = psycopg2.connect(
        dbname='democracydb', user='exampleuser', password='thiswillnotbelive')
    cursor = connection.cursor()
    # yesterday, past week, past month, all time
    print("Getting RPS votes for yesterday, last week, past month, and all time...")
    cursor.execute(rps_votes_yesterday)
    result = cursor.fetchone()
    rclient.set("YESTERDAY_rock", result[0])
    rclient.set("YESTERDAY_paper", result[1])
    rclient.set("YESTERDAY_scissors", result[2])
    cursor.execute(rps_votes_last_week)
    result = cursor.fetchone()
    rclient.set("PASTWEEK_rock", result[0])
    rclient.set("PASTWEEK_paper", result[1])
    rclient.set("PASTWEEK_scissors", result[2])
    cursor.execute(rps_votes_past30)
    result = cursor.fetchone()
    rclient.set("PAST30_rock", result[0])
    rclient.set("PAST30_paper", result[1])
    rclient.set("PAST30_scissors", result[2])
    cursor.execute(rps_votes_all_time)
    result = cursor.fetchone()
    rclient.set("ALLTIME_rock", result[0])
    rclient.set("ALLTIME_paper", result[1])
    rclient.set("ALLTIME_scissors", result[2])
    # Votes by team
    print("Getting RPS votes by team...")
    cursor.execute(rps_votes_team.format(1, 1, 1))
    result = cursor.fetchone()
    rclient.set("TEAM1_rock", result[0])
    rclient.set("TEAM1_paper", result[1])
    rclient.set("TEAM1_scissors", result[2])
    cursor.execute(rps_votes_team.format(2, 2, 2))
    result = cursor.fetchone()
    rclient.set("TEAM2_rock", result[0])
    rclient.set("TEAM2_paper", result[1])
    rclient.set("TEAM2_scissors", result[2])
    # Votes by age
    print("Getting RPS votes by age...")
    cursor.execute(rps_votes_by_age.format(0, 18, 0, 18, 0, 18))
    result = cursor.fetchone()
    rclient.set("AGE0-18_rock", result[0])
    rclient.set("AGE0-18_paper", result[1])
    rclient.set("AGE0-18_scissors", result[2])
    cursor.execute(rps_votes_by_age.format(19, 36, 19, 36, 19, 36))
    result = cursor.fetchone()
    rclient.set("AGE19-36_rock", result[0])
    rclient.set("AGE19-36_paper", result[1])
    rclient.set("AGE19-36_scissors", result[2])
    cursor.execute(rps_votes_by_age.format(37, 52, 37, 52, 37, 52))
    result = cursor.fetchone()
    rclient.set("AGE37-52_rock", result[0])
    rclient.set("AGE37-52_paper", result[1])
    rclient.set("AGE37-52_scissors", result[2])
    cursor.execute(rps_votes_by_age.format(53, 72, 53, 72, 53, 72))
    result = cursor.fetchone()
    rclient.set("AGE53-72_rock", result[0])
    rclient.set("AGE53-72_paper", result[1])
    rclient.set("AGE53-72_scissors", result[2])
    cursor.execute(rps_votes_by_age.format(73, 999, 73, 999, 73, 999))
    result = cursor.fetchone()    
    rclient.set("AGE73PLUS_rock", result[0])
    rclient.set("AGE73PLUS_paper", result[1])
    rclient.set("AGE73PLUS_scissors", result[2])
    # Votes by time
    print("Getting RPS votes by time of day...")
    cursor.execute(time_of_votes)
    result = cursor.fetchone()
    rclient.set("TIME00-02_votes", result[0])
    rclient.set("TIME02-04_votes", result[1])
    rclient.set("TIME04-06_votes", result[2])
    rclient.set("TIME06-08_votes", result[3])
    rclient.set("TIME08-10_votes", result[4])
    rclient.set("TIME10-12_votes", result[5])
    rclient.set("TIME12-14_votes", result[6])
    rclient.set("TIME14-16_votes", result[7])
    rclient.set("TIME16-18_votes", result[8])
    rclient.set("TIME18-20_votes", result[9])
    rclient.set("TIME20-22_votes", result[10])
    rclient.set("TIME22-24_votes", result[11])
    # Votes by gender
    print("Getting RPS votes by gender...")
    cursor.execute(rps_votes_by_gender.format(1, 1, 1))
    result = cursor.fetchone()
    rclient.set("GENDER1_rock", result[0])
    rclient.set("GENDER1_paper", result[1])
    rclient.set("GENDER1_scissors", result[2])
    cursor.execute(rps_votes_by_gender.format(2, 2, 2))
    result = cursor.fetchone()
    rclient.set("GENDER2_rock", result[0])
    rclient.set("GENDER2_paper", result[1])
    rclient.set("GENDER2_scissors", result[2])
    cursor.execute(rps_votes_by_gender.format(3, 3, 3))
    result = cursor.fetchone()
    rclient.set("GENDER3_rock", result[0])
    rclient.set("GENDER3_paper", result[1])
    rclient.set("GENDER3_scissors", result[2])
    cursor.execute(rps_votes_by_gender.format(4, 4, 4))
    result = cursor.fetchone()
    rclient.set("GENDER4_rock", result[0])
    rclient.set("GENDER4_paper", result[1])
    rclient.set("GENDER4_scissors", result[2])
    # Victory Loss Neutral Unequal Equal by shape
    print("Getting VLNUE by shape...")
    cursor.execute(vlnue_each_shape)
    result = cursor.fetchone()
    rclient.set("VLNUE_draw", result[0])
    rclient.set("VLNUEVICTORY_rock", result[1])
    rclient.set("VLNUEVICTORY_paper", result[6])
    rclient.set("VLNUEVICTORY_scissors", result[11])
    rclient.set("VLNUELOSS_rock", result[2])
    rclient.set("VLNUELOSS_paper", result[7])
    rclient.set("VLNUELOSS_scissors", result[12])
    rclient.set("VLNUENEUTRAL_rock", result[3])
    rclient.set("VLNUENEUTRAL_paper", result[8])
    rclient.set("VLNUENEUTRAL_scissors", result[13])
    rclient.set("VLNUEUNEQUAL_rock", result[4])
    rclient.set("VLNUEUNEQUAL_paper", result[9])
    rclient.set("VLNUEUNEQUAL_scissors", result[14])
    rclient.set("VLNUEEQUAL_rock", result[5])
    rclient.set("VLNUEEQUAL_paper", result[10])
    rclient.set("VLNUEEQUAL_scissors", result[15])
    # Victory Loss Neutral Unequal Equal by team
    print("Getting VLNUE by team...")
    cursor.execute(vlnue_for_team_1)
    result = cursor.fetchone()
    rclient.set("VLNUEDRAWTEAM_1", result[0])
    rclient.set("VLNUEVICTORYTEAM_1", result[1])
    rclient.set("VLNUELOSSTEAM_1", result[2])
    rclient.set("VLNUENEUTRALTEAM_1", result[3])
    rclient.set("VLNUEUNEQUALTEAM_1", result[4])
    rclient.set("VLNUEEQUALTEAM_1", result[5])
    cursor.execute(vlnue_for_team_2)
    result = cursor.fetchone()
    rclient.set("VLNUEDRAWTEAM_2", result[0])
    rclient.set("VLNUEVICTORYTEAM_2", result[1])
    rclient.set("VLNUELOSSTEAM_2", result[2])
    rclient.set("VLNUENEUTRALTEAM_2", result[3])
    rclient.set("VLNUEUNEQUALTEAM_2", result[4])
    rclient.set("VLNUEEQUALTEAM_2", result[5])

    cursor.close()
except psycopg2.DatabaseError as exception:
    print(exception)
finally:
    if connection:
        connection.close()