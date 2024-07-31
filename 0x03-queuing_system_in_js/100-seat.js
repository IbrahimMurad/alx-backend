import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';
const express = require('express');

const client = createClient();
const getAsync = promisify(client.get).bind(client);

function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return availableSeats;
}

reserveSeat(50);

let reservationEnabled = true;

const queue = createQueue();

const app = express();
app.listen(1245);

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ 'numberOfAvailableSeats': availableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ 'status': 'Reservation are blocked' });
    return;
  }
  const job = queue.create('reserve_seat', {}).save((err) => {
    if (err) {
      res.json({ "status": "Reservation failed" });
    } else {
      res.json({ 'status': 'Reservation in progress' });
    }
  });
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  })
  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  })
});

app.get('/process', (req, res) => {
  const job = queue.process('reserve_seat', async (job, done) => {
    let availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      done(Error('Not enough seats available'));
    } else {
      availableSeats -= 1;
      reserveSeat(availableSeats);
      if (availableSeats === 0) {
        reservationEnabled = false;
      }
      done();
    }
  });
  res.json({ 'status': 'Queue processing' });
});
