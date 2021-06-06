const router = require('express').Router();
let location = require('../models/location.model');

router.route('/').get((req, res) => {

  const { city, country, continent, eu, tag } = req.query;

  location.find()
    .then(locations => res.json(users))
    .catch(err => res.status(400).json('Error: ' + err));

  if (firstName) {
    results = results.filter(r => r.firstName === firstName);
  }

  if (lastName) {
    results = results.filter(r => r.lastName === lastName);
  }
  
  if (age) {
    results = results.filter(r => +r.age === +age);
  }
});

router.route('/:id').get((req, res) => {
    location.findbtID(req.params.id)
      .then(() => res.json('Exercise deleted.'))
      .catch(err => res.status(400).json('Error: ' + err));
  });

router.route('/add').post((req, res) => {
  let set = 0;

  if (req.body.city){
      const city = req.body.city
      set += 1
  }
  else{const city = ''}
  if (req.body.country){
    const country = req.body.country
    set += 1
  }
  else{const country = ''}
  if (req.body.continent){
    const continent = req.body.continent
  }
  else{const continent = ''}
  if (req.body.eu){
    const eu = req.body.eu
  }
  else{const eu = false}
  if (req.body.tags){
    const tags = req.body.tags
  }
  else{const tags = []}

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