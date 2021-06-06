const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

const URI = process.env.DB_URI;
mongoose.connect(URI, { useNewUrlParser: true, useCreateIndex: true, useUnifiedTopology: true });
const connection = mongoose.connection;
connection.once('open', () => {
    console.log('DB Connection made')
})

const jobsRouter = require('./routes/jobs');
const usersRouter = require('./routes/users');
const locationsRouter = require('./routes/locations');

//app.use('/jobs', jobsRouter);
app.use('/users', usersRouter);
app.use('/locations', locationsRouter);

app.listen(PORT, () =>{
    console.log(`Server is runnng on port: $(port)`)
});

