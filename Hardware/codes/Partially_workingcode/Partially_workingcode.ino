#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "OnePlus Nord CE5 z7ce";
const char* password = "wjac2877";

String apiKey = "VKEHGV4CW6FUS4YK";

#define RXD2 16
#define TXD2 17

uint8_t npkQuery[]   = {0x01,0x03,0x00,0x1E,0x00,0x03,0x65,0xCD};
uint8_t phQuery[]    = {0x01,0x03,0x00,0x06,0x00,0x01,0x64,0x0B};
uint8_t moistQuery[] = {0x01,0x03,0x00,0x12,0x00,0x01,0x24,0x0F};
uint8_t tempQuery[]  = {0x01,0x03,0x00,0x13,0x00,0x01,0x75,0xCF};
uint8_t condQuery[]  = {0x01,0x03,0x00,0x15,0x00,0x01,0x95,0xCE};

uint8_t resp[11];

bool sendQuery(uint8_t *q) {
  while (Serial2.available()) Serial2.read();

  Serial2.write(q, 8);
  delay(300);

  int i = 0;
  unsigned long start = millis();

  while (i < 11 && millis() - start < 1000) {
    if (Serial2.available()) {
      resp[i++] = Serial2.read();
    }
  }

  if (i < 7) return false; 
  return true;
}

void connectWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n WiFi Connected!");
}

void sendToThingSpeak(float moisture, float temp, float ph, int ec, int n, int p, int k) {

  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;

  String url = "http://api.thingspeak.com/update?api_key=" + apiKey +
               "&field1=" + String(moisture) +
               "&field2=" + String(temp) +
               "&field3=" + String(ph) +
               "&field4=" + String(ec) +
               "&field5=" + String(n) +
               "&field6=" + String(p) +
               "&field7=" + String(k);

  Serial.println("📡 Sending to ThingSpeak...");
  Serial.println(url);

  http.begin(url);
  int httpCode = http.GET();

  Serial.print("HTTP Response: ");
  Serial.println(httpCode);

  if (httpCode == 200) {
    Serial.println(" Upload Success");
  } else {
    Serial.println(" Upload Failed");
  }

  http.end();
}

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);

  connectWiFi();
}

void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Reconnecting WiFi...");
    connectWiFi();
  }

  float moisture = 0, temp = 0, ph = 0;
  int ec = 0, n = 0, p = 0, k = 0;

  if (sendQuery(moistQuery)) {
    moisture = (resp[3] << 8 | resp[4]) / 10.0;
  }

  if (sendQuery(tempQuery)) {
    temp = (resp[3] << 8 | resp[4]) / 10.0;
  }

  if (sendQuery(phQuery)) {
    ph = (resp[3] << 8 | resp[4]) / 100.0;
  }

  if (sendQuery(condQuery)) {
    ec = (resp[3] << 8 | resp[4]);
  }

  if (sendQuery(npkQuery)) {
    n = (resp[3] << 8 | resp[4]);
    p = (resp[5] << 8 | resp[6]);
    k = (resp[7] << 8 | resp[8]);
  }

  Serial.println("\n----- SENSOR DATA -----");
  Serial.print("Moisture: "); Serial.println(moisture);
  Serial.print("Temp: "); Serial.println(temp);
  Serial.print("pH: "); Serial.println(ph);
  Serial.print("EC: "); Serial.println(ec);
  Serial.print("N: "); Serial.println(n);
  Serial.print("P: "); Serial.println(p);
  Serial.print("K: "); Serial.println(k);
  Serial.println("----------------------");

  sendToThingSpeak(moisture, temp, ph, ec, n, p, k);

  delay(20000);
}