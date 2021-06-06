const mongoose = require('mongoose');

let location = require('./location.model');

const Schema = mongoose.Schema;

const companySchema = new Schema({
  website: String,
  name: String,
  size: Number,
  industry: String,
  rating: Number,
  culture: Number,
  diversity: Number,
  balance: Number,
  management: Number,
  comp: Number,
  oportunity: Number,
  location: location.schema,
}, {
  timestamps: true,
});

const Company = mongoose.model('Company', companySchema);

module.exports = Company;