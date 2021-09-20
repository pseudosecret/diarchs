const express = require('express')
const md = require('markdown-it')()
const createDOMPurify = require('dompurify')
const { JSDOM } = require('jsdom')

const router = express.Router()
const window = new JSDOM('').window
const DOMPurify = createDOMPurify(window)


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
const Post = require('../models/writing/Post.js')

router.get('/writing/404', (req, res) => {
    res.render('writing/404.pug', {
        title: 'The Wilbur Industries Blog',
        headerImage: '404-flames.jpg', 
        path: ''
    })
})

router.get('/writing/home', async (req, res) => {
    try {
        const page = typeof(req.query.page) !== undefined ? req.query.page : 1
        const pageSize = 10 
        const posts = await Post.find({}).orFail()
                                .skip((page - 1) * pageSize)
                                .limit(pageSize)
        res.render('writing/home.pug', { 
            posts: posts,
            title: 'The Wilbur Industries Blog',
            path: '',
            headerImage: 'red-factory.jpg'
        })
    } catch(error) {
        console.log("Error: " + error)
        res.redirect('/writing/404')
    }
})

router.get('/writing/about', (req, res) => {
    res.render('writing/about.pug', { 
        title: 'The Wilbur Industries Blog',
        path: '',
        headerImage: 'red-factory.jpg'
    })
})

router.get('/writing/contact', (req, res) => {
    res.render('writing/contact.pug', { 
        title: 'The Wilbur Industries Blog',
        path: '',
        headerImage: 'contact-bg.jpg'
    })
})
 
router.get('/writing/create', (req, res) => {
    res.render('writing/create.pug', { 
        title: 'The Wilbur Industries Blog',
        path: '',
        headerImage: 'home-bg.jpg'
    })
})
 
router.post('/writing/create', async (req, res) => {
    try {
        const post = new Post({
            'title': req.body.title,
            'subtitle': req.body.subtitle,
            'author': req.body.author,
            'description': req.body.description,
            'content': req.body.content,
            'typeOfPost': req.body.typeofpost
        })
        let savePost = await post.save()
        console.log('created ' + savePost + ' with following data: \n' + req.body)
        res.redirect('/writing/home')
    } catch(error) {
        console.log('Error encountered: ' + error)
        res.redirect('/writing/404')
    }
})

router.get('/writing/post/:id', async (req, res) => {
    try {
        let post = await Post.findById(req.params.id).orFail()
        console.log('data --->' + post)
        res.render('writing/post.pug', { 
            title: 'The Wilbur Industries Blog',
            path: '',
            post: post,
            content: DOMPurify.sanitize(md.render(post.content))
        })
    } catch(error) {
        console.log('Error encountered: ' + error)
        res.redirect('/writing/404')
    }
})
 
router.get('/writing/edit/:id', async (req, res) => {
    try {
        let post = await Post.findById(req.params.id).orFail()
        console.log('data --->' + post)
        res.render('writing/edit.pug', { 
            title: 'Edit post',
            path: '/edit',
            post: post
        })
    } catch(error) {
        console.log('Error encountered: ' + error)
        res.redirect('/writing/404')
    }
})

router.post('/writing/edit', async (req, res) => {
    try {
        let update = await Post.updateOne({ _id: req.body._id }, {
            title: req.body.newtitle,
            subtitle: req.body.newsubtitle,
            author: req.body.newauthor,
            description: req.body.newdescription,
            content: req.body.newcontent,
            typeOfPost: req.body.newtypeofpost
        })
        console.log(update + 'has been updated to--->' + 
                    '\n' + req.body.newtitle + 
                    '\n' + req.body.newsubtitle + 
                    '\n' + req.body.newauthor + 
                    '\n' + req.body.newdescription + 
                    '\n' + req.body.newcontent +
                    '\n' + req.body.typeofpost)
        res.redirect('/writing/post/' + req.body._id)
    } catch(error) {
        console.log('Error encountered: ' + error)
        res.redirect('/writing/404')
    }
})

router.post('/writing/', (req, res) => {
    res.redirect('/writing/home')
})

router.get('/writing/*', (req, res) => {
    res.redirect('/writing/404')
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
