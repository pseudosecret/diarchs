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