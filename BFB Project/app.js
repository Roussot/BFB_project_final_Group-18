// app.js - cleaned ES5-compatible core helpers for the demo
// LocalStorage-backed tiny DB + domain helpers (pricing, orders, logistics)

var DB = {
  load: function(k, d){ if (typeof d === 'undefined') d = []; try { var raw = localStorage.getItem(k); if (!raw) return d; var parsed = JSON.parse(raw); return (parsed !== null && typeof parsed !== 'undefined') ? parsed : d; } catch (e) { return d; } },
  save: function(k, v){ localStorage.setItem(k, JSON.stringify(v)); },
  uid: function(){ return (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') ? crypto.randomUUID() : Math.random().toString(36).slice(2); }
};

var usersKey = 'users';
var stockKey = 'farmer_stock';
var demandKey = 'buyer_demand';
var ordersKey = 'orders';
var logsKey = 'logistics';

function avgPriceForCrop(crop){
  var stock = DB.load(stockKey, []);
  var arr = [];
  for (var i=0;i<stock.length;i++){ if (stock[i].crop === crop) arr.push(Number(stock[i].pricePerKg)||0); }
  if (!arr.length) return null;
  var sum = 0; for (var j=0;j<arr.length;j++) sum += arr[j];
  return Math.round(sum / arr.length);
}

function suggestPrice(price, crop){
  var avg = avgPriceForCrop(crop);
  if (avg == null) return { suggested: price, reason: 'No history' };
  var delta = price - avg;
  if (Math.abs(delta / avg) > 0.15){
    var suggested = Math.round(avg * 100) / 100;
    return { suggested: suggested, reason: 'Aligned to market avg ' + avg };
  }
  return { suggested: price, reason: 'Within band' };
}

function findDemandMatches(stock){
  var demands = DB.load(demandKey, []);
  var out = [];
  for (var i=0;i<demands.length;i++){ if (demands[i].crop === stock.crop && demands[i].qtyNeeded > 0) out.push(demands[i]); }
  return out;
}

function createOrder(stock, buyerId, qty){
  var orders = DB.load(ordersKey, []);
  var price = Number(stock.pricePerKg) || 0;
  var total = Math.round(qty * price * 100) / 100;
  var order = { id: DB.uid(), stockId: stock.id, buyerId: buyerId, qtyKg: qty, pricePerKg: price, total: total, capacityOK: null, logistics: null, status: 'PENDING_CAPACITY' };
  orders.push(order);
  DB.save(ordersKey, orders);
  return order;
}

function setCapacity(orderId, ok){
  var orders = DB.load(ordersKey, []);
  for (var i=0;i<orders.length;i++){ if (orders[i].id === orderId){ orders[i].capacityOK = !!ok; orders[i].status = ok ? 'READY_FOR_LOGISTICS' : 'NO_CAPACITY_ALT_BUYER'; DB.save(ordersKey, orders); return orders[i]; } }
}

function setLogistics(orderId, mode){
  var orders = DB.load(ordersKey, []);
  for (var i=0;i<orders.length;i++){
    var o = orders[i];
    if (o.id === orderId){
      var discount = 0, cost = 0, carrier = null;
      if (mode === 'buyer') discount = 0.05;
      if (mode === 'external'){ cost = Math.max(200, o.qtyKg * 0.5); carrier = 'External Courier'; }
      o.logistics = { id: DB.uid(), orderId: orderId, mode: mode, discount: discount, cost: cost, carrier: carrier, status: 'SCHEDULED' };
      o.status = 'IN_TRANSIT';
      DB.save(ordersKey, orders);
      return o;
    }
  }
}

function confirmDelivery(orderId){
  var orders = DB.load(ordersKey, []);
  var stock = DB.load(stockKey, []);
  for (var i=0;i<orders.length;i++){
    if (orders[i].id === orderId){
      var o = orders[i];
      for (var j=0;j<stock.length;j++){ if (stock[j].id === o.stockId){ stock[j].qtyKg = Math.max(0, stock[j].qtyKg - o.qtyKg); DB.save(stockKey, stock); break; } }
      o.status = 'DELIVERED';
      DB.save(ordersKey, orders);
      return o;
    }
  }
}

// seed demo users on first load
(function seed(){
  var existing = DB.load(usersKey, []);
  if (Array.isArray(existing) && existing.length) return;
  DB.save(usersKey, [
    { id: 'u_farmer', role: 'farmer', name: 'Ama Farmer', email: 'farmer@example.com', password: 'pass123' },
    { id: 'u_buyer', role: 'buyer', name: 'Bongi Buyer', email: 'buyer@example.com', password: 'pass123' },
    { id: 'u_dist', role: 'distributor', name: 'Dumi Logistics', email: 'dist@example.com', password: 'pass123' }
  ]);
})();
