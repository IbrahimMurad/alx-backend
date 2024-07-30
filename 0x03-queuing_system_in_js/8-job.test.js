import kue from 'kue';
import { expect } from 'chai';
import sinon from 'sinon';
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();

const list = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
];

before(() => {
  queue.testMode.enter();
});

afterEach(() => {
  queue.testMode.clear();
  sinon.restore(); // Restore original methods after each test
});

after(() => {
  queue.testMode.exit();
});

describe('createPushNotificationsJobs', () => {
  it('display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw('Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {
    // Mock the job creation to include an ID
    const createStub = sinon.stub(queue, 'create').callsFake((type, data) => {
      const job = {
        id: Math.floor(Math.random() * 1000), // Mock job ID
        data,
        type,
        save: () => {
          console.log(`Notification job created: ${job.id}`)
        },
        on: function(event, callback) {
          return this;
        }
      };
      return job;
    });

    createPushNotificationsJobs(list, queue);
    
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.eql(list[0]);
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.eql(list[1]);
  });
});
