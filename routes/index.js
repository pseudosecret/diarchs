const express = require('express')
const md = require('markdown-it')()
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const router = express.Router()
const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);


/**
 * Main Wilbur Industries pages
 */
 router.get('/', (req, res) => {
    res.render('wilburindustries/home.pug', { 
        title: 'Wilbur Industries' 
    })
})

router.get('/placeholder', (req, res) => {
    res.render('wilburindustries/placeholder.pug', { 
        title: 'Wilbur Industries placeholder' 
    })
})

router.get('/wilburindustriesadmin', (req, res) => {
    res.render('wilburindustries/admin.pug', { 
        title: 'Admin' 
    })
})

router.post('/adminlogin', (req, res) => {
    res.render('wilburindustries/admin.pug', {
        title: 'Admin'
    })
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

router.get('/blog/home', async (req, res) => {
    try {
        const page = typeof(req.query.page) !== undefined ? req.query.page : 1
        const pageSize = 1 
        const posts = await Post.find({}).orFail()
                                .skip((page - 1) * pageSize)
                                .limit(pageSize)
        res.render('blog/home.pug', { 
            posts: posts,
            title: 'The Wilbur Industries Blog'
        })
    } catch(error) {
        console.log("Error: " + error)
        res.redirect('/blog/404')
    }
})

router.get('/blog/about', (req, res) => {
    res.render('blog/about.pug', { title: 'The Wilbur Industries Blog' })
})

router.get('/blog/contact', (req, res) => {
    res.render('blog/contact.pug', { title: 'The Wilbur Industries Blog' })
})
 
router.get('/blog/create', (req, res) => {
    res.render('blog/create.pug', { 
        title: 'The Wilbur Industries Blog'
    })
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
 
router.get('/blog/edit/:id', async (req, res) => {
    try {
        let post = await Post.findById(req.params.id).orFail()
        console.log('data --->' + post)
        res.render('blog/edit.pug', { 
            title: 'Edit post',
            post: post
        })
    } catch(error) {
        console.log('Error encountered: ' + error)
        res.redirect('/blog/404')
    }
})

router.post('/blog/edit', async (req, res) => {
    try {
        let update = await Post.updateOne({ _id: req.body._id }, {
            title: req.body.newtitle,
            subtitle: req.body.newsubtitle,
            author: req.body.newauthor,
            description: req.body.newdescription,
            content: req.body.newcontent
        }).orFail()
        console.log(update + 'has been updated to--->' + 
                    '\n' + req.body.newtitle + 
                    '\n' + req.body.newsubtitle + 
                    '\n' + req.body.newauthor + 
                    '\n' + req.body.newdescription + 
                    '\n' + req.body.newcontent)
        res.redirect('/blog/post/' + req.body._id)
    } catch(error) {
        console.log('Error encountered: ' + error)
        res.redirect('/blog/404')
    }
})

router.post('/blog/')

router.get('/blog/*', (req, res) => {
    res.redirect('/blog/404')
 })
 
 
 
 /**
 * Democracy page routing
 */
const Vote = require('../models/democracy/DemocracyVote.js')
const User = require('../models/democracy/DemocracyUser.js')

router.get('/democracy/home', (req, res) => {
    res.render('democracy/home.pug', { title: 'Democracy!' })
})



/**
 * Export all the router stuff
 */
module.exports = router
