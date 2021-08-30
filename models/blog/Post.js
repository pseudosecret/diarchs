const mongoose = require('mongoose')

const Schema = mongoose.Schema

let post = new Schema({
    title: {
        type: String,
        required: [true, 'Posts have a title.']
    },
    author: {
        type: String,
        required: [true, 'Posts have an author.'],
    },
    published: {
        type: Date,
        required: [true, 'Posts are published at a static point in time.'],
        default: Date.now
    },
    description: {
        type: String,
        required: [true, 'Posts have a description.']
    },
    content: {
        type: String,
        required: [true, 'Posts have content.']
    }
}, { collection: 'Posts' })

const Post = mongoose.model('posts', post)

module.exports = Post