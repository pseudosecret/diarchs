const express = require('express')
const md = require('markdown-it')()
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const router = express.Router()
const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

/**
 * Democracy page routing
 */
const Vote = require('../models/democracy/DemocracyVote.js')
const User = require('../models/democracy/DemocracyUser.js')

router.get('/democracy/home', (req, res) => {
    res.render('democracy/home.pug', { title: 'Democracy!' })
})



/**
 * Blog page routing
 */
const Post = require('../models/blog/Post.js')

router.get('/blog/404', (req, res) => {
    res.render('blog/404.pug', {
        title: 'The Wilbur Industries Blog'
    })
})

router.get('/blog/admin', (req, res) => {
    res.render('blog/admin.pug', {
        title: 'The Wilbur Industries Blog'
    })
})

router.post('/blog/admin', (req, res) => {
    
})

router.get('/blog/home', async (req, res) => {
    const posts = await Post.find({})
    res.render('blog/home.pug', { 
        posts: posts,
        title: 'The Wilbur Industries Blog' 
    })
})

router.get('/blog/about', (req, res) => {
    res.render('blog/about.pug', { title: 'The Wilbur Industries Blog' })
})

router.get('/blog/contact', (req, res) => {
    res.render('blog/contact.pug', { title: 'The Wilbur Industries Blog' })
})

router.get('/blog/create', (req, res) => {
    res.render('blog/create.pug', { title: 'The Wilbur Industries Blog' })
})

router.post('/blog/create', (req, res) => {
    Post.create(req.body, (error, post) => {
        console.log(req.body)
        res.redirect('/blog/home')
    })
})

router.get('/blog/post/:id', async (req, res) => {
    try {
        let post = await Post.findById(req.params.id).orFail()
        console.log('data --->' + post)
        res.render('blog/post.pug', { 
            title: 'The Wilbur Industries Blog',
            post: post,
            content: DOMPurify.sanitize(md.render(post.content))
        })
    } catch(error) {
        console.log('Error encountered: ' + error)
        res.redirect('/blog/404')
    }
})

router.get('/blog/*', (req, res) => {
    res.redirect('/blog/404')
})



/**
 * Main Wilbur Industries pages
 */
router.get('/', (req, res) => {
    res.render('wilburindustries/home.pug', { title: 'Wilbur Industries' })
})

router.get('/placeholder', (req, res) => {
    res.render('wilburindustries/placeholder.pug', { title: 'Wilbur Industries placeholder' })
})


/**
 * Export all the router stuff
 */
module.exports = router
