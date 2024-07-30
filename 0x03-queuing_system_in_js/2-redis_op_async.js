import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('error', err => console.log(`Redis client not connected to the server: ${err}`, err));

client.on('connect', () => console.log('Redis client connected to the server'));

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, (err, reply) => console.log(`Reply: ${reply}`));
}

const getAsync = promisify(client.get).bind(client);
const displaySchoolValue = async (schoolName) => {
  try {
    const reply = await getAsync(schoolName);
    console.log(`${reply}`);
  } catch (error) {
    // do nothing for now.
  }
}


displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
