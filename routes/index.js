const express = require('express')

const router = express.Router()

router.get('/placeholder', (req, res) => {
    res.render('wilburindustries/placeholder.pug', { title: 'Wilbur Industries placeholder' })
})

router.get('/democracy/home', (req, res) => {
    res.render('democracy/home.pug', { title: 'Democracy!' })
})

router.get('/blog/home', (req, res) => {
    res.render('blog/home.pug', { title: 'a Wilbur Industries blog' })
})

router.get('/blog/contact', (req, res) => {
    res.render('blog/contact.pug', { title: 'a Wilbur Industries blog' })
})

router.get('/blog/post', (req, res) => {
    res.render('blog/post.pug', { title: 'a Wilbur Industries blog' })
})

router.get('/blog/about', (req, res) => {
    res.render('blog/about.pug', { title: 'a Wilbur Industries blog' })
})

router.get('/', (req, res) => {
    res.render('wilburindustries/home.pug', { title: 'Wilbur Industries' })
})

module.exports = router
