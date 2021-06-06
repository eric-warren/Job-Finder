const mongoose = require('mongoose');

const Schema = mongoose.Schema;

let location = require('./location.model');
let company = require('./company.model');

const jobSchema = new Schema({
  title: String,
  description: String,
  link: String,
  job_type: String,
  job_hash: String,
  latest_seen: Date,
  company: company.schema,
  location: location.schema,
}, {
  timestamps: true,
});

const Job = mongoose.model('Job', jobSchema);

module.exports = Job;