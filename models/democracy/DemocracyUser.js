const mongoose = require('mongoose')

const Schema = mongoose.Schema

let user = new Schema({
    name: [
        {
            first: { 
                type: String, 
                required: [true, 'A person must have a first name.']
            },
            last: {
                type: String, 
                required: [true, 'A person must have a last name.']
            }
        }
    ],
    dob: {
        type: Date,
        required: [true, 'A person is born at a time, not everywhen or nowhen.'],
        default: Date.now
    },
    registered: {
        type: Date,
        required: [true, 'A person joins democracy at a time, not everywhen or nowhen.'],
        default: Date.now
    },
    team: {
        type: Number,
        required: [true, 'A person belongs to a team.']
    }
}, { collection: 'Users' })



const User = mongoose.model('users', user)

module.exports = User