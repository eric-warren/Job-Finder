const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const locationSchema = new Schema({
  city: String,
  counrty: String,
  continent: String,
  eu: Boolean,
  tags: [String],
}, {
  timestamps: true,
});

const Location = mongoose.model('Location', locationSchema);

module.exports = Location;