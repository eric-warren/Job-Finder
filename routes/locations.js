const router = require('express').Router();
const { query } = require('express');
let location = require('../models/location.model');

router.route('/').get((req, res) => {

  location.find()
    .then(locations => res.json(locations))
    .catch(err => res.status(400).json('Error: ' + err));

});

router.route('/:id').get((req, res) => {
    location.findById(req.params.id)
      .then(locations => res.json(locations))
      .catch(err => res.status(400).json('Error: ' + err));
  });

router.route('/:id').delete((req, res) => {
  location.findByIdAndDelete(req.params.id)
    .then(() => res.json('Location deleted.'))
    .catch(err => res.status(400).json('Error: ' + err));
});


router.route('/:id').patch((req, res) => {
  location.findById(req.params.id)
    .then(location => {
      if (req.body.city){
        location.city = req.body.city;
      }
      if (req.body.country){
        location.country = req.body.country;
      }
      if (req.body.continent){
        location.continent = req.body.continent;
      }
      if (req.body.eu){
        location.eu = Boolean(req.body.eu);;
      }
      if (req.body.tags){
        location.tags = req.body.tags;
      }

      location.save()
        .then(() => res.json('Location updated!'))
        .catch(err => res.status(400).json('Error: ' + err));
    })
    .catch(err => res.status(400).json('Error: ' + err));
});


router.route('/add').post((req, res) => {
  let set = 0;
  city = ''
  country = ''
  continent = ''
  eu = false
  tags = []

  if (req.body.city){
      city = req.body.city
      set += 1
  }
  else{city = ''}
  if (req.body.country){
    country = req.body.country
    set += 1
  }
  else{country = ''}
  if (req.body.continent){
    continent = req.body.continent
  }
  else{continent = ''}
  if (req.body.eu){
    eu = req.body.eu
  }
  else{eu = false}
  if (req.body.tags){
    tags = req.body.tags
  }
  else{tags = []}

  const newLocation = new location({
          city,
          country,
          continent,
          eu,
          tags,
        });

  newLocation.save()
    .then(() => res.json('Location added'))
    .catch(err => res.status(400).json('Error: ' + err));
});

module.exports = router;