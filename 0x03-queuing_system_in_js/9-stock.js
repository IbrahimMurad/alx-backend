import { createClient } from 'redis';
import { promisify } from 'util';
const express = require('express');

const listProducts = [
  {
    id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4
  },
  {
    id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10
  },
  {
    id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2
  },
  {
    id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5
  },
];

function getItemById (id) {
  return listProducts.find((item) => item.id === id);
}

const app = express();

app.get('/list_products', (req, res) => {
  const list = listProducts.map(({ id, name, price, stock }) => ({ 'itemId': id, 'itemName': name, 'price': price, 'initialAvailableQuantity': stock }));
  res.json(list);
});


app.listen(1245);

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected');
});

function reserveStockById(itemId, stock) {
  client.set(`itemId.${itemId}`, stock);
}

const getAsync = promisify(client.get).bind(client);
async function getCurrentReservedStockById(itemId) {
  const reply = await getAsync(`itemId.${itemId}`);
  return reply;
}

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));
  if (!item) {
    res.status(404).json({"status":"Product not found"});
    return;
  }
  const currentQuantity = await getCurrentReservedStockById(itemId);
  const itemWithStock = {
    'itemId': item.id,
    'itemName':item.name,
    'price': item.price,
    'initialAvailableQuantity': item.stock,
    'currentQuantity': parseInt(currentQuantity)
  };
  res.json(itemWithStock);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));
  if (!item) {
    res.status(404).json({"status":"Product not found"});
    return;
  }
  const currentQuantity = await getCurrentReservedStockById(itemId);
  if (parseInt(currentQuantity) < 1) {
    res.status(403).json({"status":"Not enough stock available","itemId":item.id});
    return;
  }
  reserveStockById(itemId, parseInt(currentQuantity) - 1);
  res.json({'status': 'Reservation confirmed', "itemId": itemId});
});
