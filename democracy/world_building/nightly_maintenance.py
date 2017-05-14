import psycopg2

connection = None
count_votes = '''
              SELECT COUNT(*) FROM Votes
              WHERE shape_id = {}
              AND time::date = NOW()::date - INTERVAL '1 DAY';
              '''
win_points = 5
neutral_points = 2
loss_points = 1
draw_points = 3
    
try:
    print("Connecting to democracydb...")
    connection = psycopg2.connect(
        dbname='democracydb', user='exampleuser', password='thiswillnotbelive')
    cursor = connection.cursor()
    print("Counting votes...")
    # count all rock votes from yesterday
    cursor.execute(count_votes.format(1))
    result = cursor.fetchone()
    rock = result[0]
    # count all paper votes from yesterday
    cursor.execute(count_votes.format(2))
    result = cursor.fetchone()
    paper = result[0]
    # count all scissor votes from yesterday
    cursor.execute(count_votes.format(3))
    result = cursor.fetchone()
    scissors = result[0]
    # determine which is the victor, if any
    win = "NULL"
    neutral = "NULL"
    loss = "NULL"
    draw = "FALSE"
    if rock == paper or rock == scissors or paper == scissors:
        draw = "TRUE"
    elif rock > paper and paper > scissors:
        win = 1
        neutral = 2
        loss = 3
    elif scissors > paper and paper > rock:
        win = 1
        neutral = 2
        loss = 3
    elif paper > scissors and scissors > rock:
        win = 2
        neutral = 3
        loss = 1
    elif rock > scissors and scissors > paper:
        win = 2
        neutral = 3
        loss = 1
    elif scissors > rock and rock > paper:
        win = 3
        neutral = 1
        loss = 2
    else: # should only be: paper > rock and rock > scissors:
        win = 3
        neutral = 1
        loss = 2
    cursor.execute('''
                   INSERT INTO Outcomes (date, win, neutral, loss, draw)
                   VALUES (NOW()::date - INTERVAL '1 DAY', 
                   {}, {}, {}, {});
                   '''.format(win, neutral, loss, draw))
    # distribute points to users
    print("Doling out points...")
    if draw == "TRUE":
        cursor.execute('''
                       UPDATE UserScores
                       SET draws = draws + 1,
                           current_points = current_points + {},
                           total_points = total_points + {}
                       FROM Votes AS t2
                       WHERE UserScores.user_id = t2.user_id
                       AND time::date = NOW()::date - INTERVAL '1 DAY'
                       '''.format(draw_points, draw_points))
    else:
        cursor.execute('''
                       UPDATE UserScores
                       SET wins = wins + 1,
                           current_points = current_points + {},
                           total_points = total_points + {}
                       FROM Votes AS t2
                       WHERE UserScores.user_id = t2.user_id
                       AND time::date = NOW()::date - INTERVAL '1 DAY'
                       AND t2.shape_id = {};
                       '''.format(win_points, win_points, win))
        cursor.execute('''
                       UPDATE UserScores
                       SET neutrals = neutrals + 1,
                           current_points = current_points + {},
                           total_points = total_points + {}
                       FROM Votes AS t2
                       WHERE UserScores.user_id = t2.user_id
                       AND time::date = NOW()::date - INTERVAL '1 DAY'
                       AND t2.shape_id = {};
                       '''.format(neutral_points, neutral_points, neutral))
        cursor.execute('''
                       UPDATE UserScores
                       SET losses = losses + 1,
                           current_points = current_points + {},
                           total_points = total_points + {}
                       FROM Votes AS t2
                       WHERE UserScores.user_id = t2.user_id
                       AND time::date = NOW()::date - INTERVAL '1 DAY'
                       AND t2.shape_id = {};
                       '''.format(loss_points, loss_points, loss))
    cursor.close()
    connection.commit()
except psycopg2.DatabaseError as exception:
    print(exception)
finally:
    if connection:
        connection.close()
