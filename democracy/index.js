var http = require("http");
var path = require("path");
var express = require("express");
var logger = require("morgan");

var app = express();

app.set("views", path.resolve(__dirname, "views"));
app.set("view engine", "ejs");

app.use(logger("tiny"));

app.use("/static", express.static(path.join(__dirname, "static")))

app.get("/", function(request, response) {
    response.render("home");
});

app.get("/about", function(request, response) {
    response.render("about");
});

app.get("/faq", function(request, response) {
    response.render("faq");
});

app.get("/profile", function(request, response) {
    response.render("profile");
});

app.get("/statistics", function(request, response) {
    response.render("statistics");
});

app.use(function(request, response) {
    response.status(404).render("404");
})

http.createServer(app).listen(3000, function() {
    console.log("democracy has started on port 3000...");
})