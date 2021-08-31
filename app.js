const express = require('express')
const path = require('path')
const routes = require('./routes/index')
const favicon = require('serve-favicon')

const app = express()

app.use(express.urlencoded({extended: true}))
app.use(express.json())

app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')

app.use('/static', express.static(path.join(__dirname, 'public')))
app.use(favicon(path.join(__dirname, 'public/favicon.ico')))

app.use('/', routes)


module.exports = app
