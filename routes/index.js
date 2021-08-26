const express = require('express')

const router = express.Router()

router.get('/placeholder', (req, res) => {
    res.render('wilburindustries/placeholder.pug', { title: 'Wilbur Industries placeholder' })
})

router.get('/democracy', (req, res) => {
    res.render('democracy/home.pug', { title: 'Democracy!' })
})



router.get('/', (req, res) => {
    res.render('wilburindustries/home.pug', { title: 'Wilbur Industries' })
})

module.exports = router
