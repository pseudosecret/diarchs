const mongoose = require('mongoose')

const Schema = mongoose.Schema

let post = new Schema({
    title: {
        type: String,
        required: [true, 'Posts have a title.']
    },
    subtitle: {
        type: String,
        required: [false, 'Posts do not have to have a subtitle.']
    },
    author: {
        type: String,
        required: [true, 'Posts have an author.']
    },
    image: {
        type: String,
        required: [true, 'Posts have an image associated with them.'],
        default: 'red-factory.jpg'
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
    typeOfPost: {
        type: String,
        required: [true, 'Posts have a type, e.g. poetry or blog entry or whatever.']
    },
    content: {
        type: String,
        required: [true, 'Posts have content.']
    }
}, { collection: 'Posts' })

const Post = mongoose.model('posts', post)

module.exports = Post