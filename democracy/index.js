var http = require("http");
var path = require("path");
var logger = require("morgan");
var express = require("express");
var app = express();
var server = require("http").createServer(app);
var io = require("socket.io")(server);
var async = require("async");
var promise = require('bluebird');
var redis = require("redis");
var rclient = redis.createClient();

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
        var query = 'SELECT count(*) AS count FROM Votes WHERE shape_id = $1 AND vote_time::date = NOW()::date;';
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


server.listen(3000, function() {
    console.log("democracy has started on port 3000...");
});