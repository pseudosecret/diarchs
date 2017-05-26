var http = require("http");
var path = require("path");
var logger = require("morgan");
var express = require("express");
var app = express();
var server = require("http").createServer(app);
var io = require("socket.io")(server);
var async = require("async");
var promise = require('bluebird');

// Initialization Options
var options = {
  promiseLib: promise
};

var pgp = require('pg-promise')(options);
var connectionString = {
    user: "exampleuser", 
    database: "democracydb", 
    password: "thiswillnotbelive", 
    host: "localhost", 
    port: 5432
};
var db = pgp(connectionString);


var t1_points = 0;
var t2_points = 0;
var t1_goal = 0;
var t2_goal = 0;

app.set("views", path.resolve(__dirname, "views"));
app.set("view engine", "ejs");
app.use("/static", express.static(path.join(__dirname, "static")));
app.use("/jquery", express.static(__dirname + "/node_modules/jquery/dist/"));
app.use("/chartjs", express.static(__dirname + "/node_modules/chart.js/dist/"))

app.use(logger("tiny"));



app.all("*", function(req, res, next) {
    var get_team_points = "SELECT * FROM TeamPoints ORDER BY team_id;";
    db.any(get_team_points)
        .then(function(data) {
            t1_points = data[0].current_points;
            t2_points = data[1].current_points;
            t1_goal = data[0].points_to_win;
            t2_goal = data[1].points_to_win;
            next();
    })
    .catch(function(error) {
        return console.error('error running query', err);
    });
});


app.get("/", function (request, response) {
    db.task(function (t) {
        var query = 'SELECT count(*) FROM Votes WHERE shape_id = $1 AND time::date = NOW()::date;';
        return t.batch([
            t.one(query, 1, a => +a.count),
            t.one(query, 2, a => +a.count),
            t.one(query, 3, a => +a.count)
        ]);
    })
        .then(function (data) {
            response.render('home', {
                rock: data[0],
                paper: data[1],
                scissors: data[2],
                t1_points: t1_points,
                t2_points: t2_points,
                t1_goal: t1_goal,
                t2_goal: t2_goal,
            });
        })
        .catch(function (error) {
            // handle the error here
        });
});

/*
app.get("/", function(request, response) {
    var rock_query = "SELECT COUNT(*) AS number FROM Votes WHERE shape_id = 1 AND time::date = NOW()::date;";
    var paper_query = "SELECT COUNT(*) AS number FROM Votes WHERE shape_id = 2 AND time::date = NOW()::date;";
    var scissors_query = "SELECT COUNT(*) AS number FROM Votes WHERE shape_id = 3 AND time::date = NOW()::date;";
    async.series([
        function() {
            pool.query(rock_query, function(err, res) {
                if(err) {
                    return console.error('error running query', err);
                }
                rock = res.rows[0].number;
                console.log("Rock votes: " + rock);
            });
            pool.query(paper_query, function(err, res) {
                if(err) {
                    return console.error('error running query', err);
                }
                paper = res.rows[0].number;
                console.log("Paper votes: " + paper);
            });
            pool.query(scissors_query, function(err, res) {
                if(err) {
                    return console.error('error running query', err);
                }
                scissors = res.rows[0].number;
                console.log("Scissors votes: " + scissors);
            });
        }, 
        function(error) {
            if (!error) {
                response.render("home", {
                    t1_points: t1_points,
                    t2_points: t2_points,
                    t1_goal: t1_goal,
                    t2_goal: t2_goal,
                    rock: rock,
                    paper: paper,
                    scissors: scissors,
                });
            }
        }
    ]);
}); */

/*
app.get("/", function(request, response) {
    var votes = [];
    var query = "SELECT COUNT(*) AS number FROM Votes WHERE shape_id = $1 AND time::date = NOW()::date;"
    for (i = 1; i < 4; i++) {
        pool.query(query, [i], function(err, res) {
            if(err) {
                return console.error('error running query', err);
            }
        votes.push(res.rows[0].number);
        });
    }
    console.log('number of votes for shape 1: ', votes[0]);
    console.log('number of votes for shape 2: ', votes[1]);
    console.log('number of votes for shape 3: ', votes[2]);
    response.render("home", {
        rock: votes[0],
        paper: votes[1],
        scissors: votes[2]
    });
}); */

app.get("/about", function(request, response) {
    response.render("about", {
        t1_points: t1_points,
        t2_points: t2_points,
        t1_goal: t1_goal,
        t2_goal: t2_goal,
    });
});

app.get("/faq", function(request, response) {
    response.render("faq", {
        t1_points: t1_points,
        t2_points: t2_points,
        t1_goal: t1_goal,
        t2_goal: t2_goal,
    });
});

app.get("/profile", function(request, response) {
    response.render("profile", {
        t1_points: t1_points,
        t2_points: t2_points,
        t1_goal: t1_goal,
        t2_goal: t2_goal,
    });
});

app.get("/statistics", function(request, response) {
    response.render("statistics", {
        t1_points: t1_points,
        t2_points: t2_points,
        t1_goal: t1_goal,
        t2_goal: t2_goal,
    });
});

app.use(function(request, response) {
    response.status(404).render("404", {
        t1_points: t1_points,
        t2_points: t2_points,
        t1_goal: t1_goal,
        t2_goal: t2_goal,
    });
});


var listened = db.connect({direct: true})
    .then(sco => {
        sco.client.on('notification', data => {
            console.log('Received: ', data);
            // data.payload = 'my payload string'
        });
        return sco.none('LISTEN $1~', 'Votes');
    })
    .catch(error => {
        console.log('Error:', error);
    });



var rock = 0;
var paper = 0;
var scissors = 0;

io.on('connection', function(socket) {  
    console.log('a user connected');    
    var rock_query = 'SELECT count(*) FROM Votes WHERE shape_id = 1 AND time::date = NOW()::date;'
    var paper_query = 'SELECT count(*) FROM Votes WHERE shape_id = 2 AND time::date = NOW()::date;'
    var scissors_query = 'SELECT count(*) FROM Votes WHERE shape_id = 3 AND time::date = NOW()::date;'
    socket.on('update rock', function(data) {
        db.one(rock_query).then(function(result) {
            if(result[0] != rock) {
                console.log('updating rock to ' + rock);
                socket.emit('update rock', rock);
            }
        });
    });
    
    socket.on('update paper', function(data) {
        db.one(paper_query).then(function(result) {
            if(result[0] != paper) {
                socket.emit('update paper', paper);
                console.log('updating paper to ' + paper);
            }
        });
    });
    
    socket.on('update scissors', function(data) {
        db.one(scissors_query).then(function(result) {
            if(result[0] != scissors) {
                socket.emit('update scissors', scissors)
                console.log('updating scissors to ' + scissors);
            }
        });        
    });
    
    socket.on('disconnect', function(data) {
        console.log('user disconnected');
    });
});


server.listen(3000, function() {
    console.log("democracy has started on port 3000...");
});