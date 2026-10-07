# SmartPredict AI – setup

```
smartpredict-ai/
├── dashboard/smartpredict-ai.html   open in a browser on the same computer as the backend
├── backend/                         Express API + Arduino serial bridge
└── arduino/sensor_reader/           sketch for Arduino Uno + DHT22 (pin 2)
```

## 1. Backend
Install Node.js (LTS). MongoDB is optional: without it the API stores readings in memory.
```
cd backend
npm install
npm run sim          # API on http://localhost:5000 with SIMULATED readings for M001-M004
```
Check http://localhost:5000/api/health and http://localhost:5000/api/readings

## 2. Dashboard
Open `dashboard/smartpredict-ai.html`. The header badge turns LIVE within ~5 s.
Click the badge to change the API URL if the backend runs elsewhere.

## 3. Real Arduino
1. Wire the DHT22 (VCC->5V, DATA->pin 2 with 10k pull-up to VCC, GND->GND), install the "DHT sensor library" (Adafruit), upload `sensor_reader.ino`.
2. Close the Serial Monitor.
3. Terminal A: `npm run sim-extra` (simulated M002-M004; the Arduino is M001), or `npm start` for real data only.
4. Terminal B: `node bridge.js COM3` (use your port; Linux: /dev/ttyUSB0).

## Notes
- Sample readings are simulated; label them as such in your viva.
- Failure probability and anomaly flags use the dashboard's demo rules until a Python model service answers POST http://localhost:8000/predict.
- Set MONGO_URL to use Atlas or a different MongoDB.
