// DHT22 on pin 2 -> prints one JSON line every 5 s. Close Serial Monitor before running bridge.js
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT22   // change to DHT11 if that's your sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (!isnan(t) && !isnan(h)) {
    Serial.print("{\"machine_id\":\"M001\",\"temperature\":");
    Serial.print(t, 1);
    Serial.print(",\"humidity\":");
    Serial.print(h, 1);
    Serial.println("}");
  }
  delay(5000);
}
