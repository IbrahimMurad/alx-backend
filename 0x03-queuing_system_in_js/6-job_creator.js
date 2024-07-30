import { createQueue } from 'kue';

const push_notification_code = createQueue();
const JobData = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account',
}

const job = push_notification_code.create('push_notification_code', JobData).save((err) => {
  if (err) {
    console.log('Notification job failed');
  } else {
    console.log(`Notification job created: ${job.id}`);
  }
});

