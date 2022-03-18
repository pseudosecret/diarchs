const mongoose = require('mongoose')

const Schema = mongoose.Schema

let comment = new Schema({
    name: {
        type: String,
        required: [true, 'Comments have the name of the commenter.']
    },
    email: {
        type: String,
        required: [true, 'Comments have an email associated with them.'],
        default: 'red-factory.jpg'
    },
    published: {
        type: Date,
        required: [true, 'Comments are published at a static point in time.'],
        default: Date.now
    },
    content: {
        type: String,
        required: [true, 'Comments have content.']
    }
}, { collection: 'Comments' })

const Comment = mongoose.model('comments', comment)

module.exports = Comment