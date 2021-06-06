const router = require('express').Router();
const { query } = require('express');
let company = require('../models/company.model');

router.route('/').get((req, res) => {

  company.find()
    .then(companies => res.json(companies))
    .catch(err => res.status(400).json('Error: ' + err));

});

router.route('/:id').get((req, res) => {
    company.findById(req.params.id)
      .then(companies => res.json(companies))
      .catch(err => res.status(400).json('Error: ' + err));
  });

router.route('/:id').delete((req, res) => {
  company.findByIdAndDelete(req.params.id)
    .then(() => res.json('Company deleted.'))
    .catch(err => res.status(400).json('Error: ' + err));
});


router.route('/:id').patch((req, res) => {
  company.findById(req.params.id)
    .then(company => {
      if (req.body.city){
        company.city = req.body.city;
      }
      if (req.body.country){
        company.country = req.body.country;
      }
      if (req.body.continent){
        company.continent = req.body.continent;
      }
      if (req.body.eu){
        company.eu = Boolean(req.body.eu);;
      }
      if (req.body.tags){
        company.tags = req.body.tags;
      }

      company.save()
        .then(() => res.json('Company updated!'))
        .catch(err => res.status(400).json('Error: ' + err));
    })
    .catch(err => res.status(400).json('Error: ' + err));
});


router.route('/add').post((req, res) => {
  website = ''
  compName = ''
  size = ''
  industry = ''
  rating = NaN
  culture = NaN
  diversity = NaN
  balance = NaN
  management = NaN
  comp = NaN
  oportunity = NaN
  location = null

  if (req.body.website){
    website = req.body.website
  }
  if (req.body.compName){
    compName = req.body.compName
  }
  if (req.body.size){
    size = req.body.size
  }
  if (req.body.industry){
    industry = req.body.industry
  }
  if (req.body.rating){
    rating = req.body.rating
  }
  if (req.body.culture){
    culture = req.body.culture
  }
  if (req.body.diversity){
    diversity = req.body.diversity
  }
  if (req.body.balance){
    balance = req.body.balance
  }
  if (req.body.management){
    management = req.body.management
  }
  if (req.body.comp){
    comp = req.body.comp
  }
  if (req.body.oportunity){
    oportunity = req.body.oportunity
  }
  if (req.body.location){
    //getobject here
  }

  const newcompany = new company({
          city,
          country,
          continent,
          eu,
          tags,
        });

  newcompany.save()
    .then(() => res.json('company added'))
    .catch(err => res.status(400).json('Error: ' + err));
});

module.exports = router;