#include <WiFi.h>
#include <HTTPClient.h>

#define RXD2 16
#define TXD2 17

const char* ssid = "OnePlus Nord CE5 z7ce";
const char* password = "wjac2877";
String apiKey = "VKEHGV4CW6FUS4YK";

uint8_t npkQuery[]  = {0x01,0x03,0x00,0x1E,0x00,0x03,0x65,0xCD};
uint8_t phQuery[]   = {0x01,0x03,0x00,0x06,0x00,0x01,0x64,0x0B};
uint8_t moistQuery[]= {0x01,0x03,0x00,0x12,0x00,0x01,0x24,0x0F};
uint8_t tempQuery[] = {0x01,0x03,0x00,0x13,0x00,0x01,0x75,0xCF};
uint8_t condQuery[] = {0x01,0x03,0x00,0x15,0x00,0x01,0x95,0xCE};

uint8_t resp[11];

void sendQuery(uint8_t *q) {
  while (Serial2.available()) Serial2.read();

  Serial2.write(q, 8);
  delay(300);

  for(int i = 0; i < 11; i++){
    if(Serial2.available()){
      resp[i] = Serial2.read();
    } else {
      resp[i] = 0;
    }
  }
}

void connectWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
}

void setup(){
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);

  connectWiFi();
}

void loop(){

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Reconnecting WiFi...");
    connectWiFi();
  }

  sendQuery(moistQuery);
  delay(100);
  float moisture = (resp[3]<<8 | resp[4]) / 10.0;

  sendQuery(tempQuery);
  delay(100);
  float temp = (resp[3]<<8 | resp[4]) / 10.0;

  sendQuery(phQuery);
  delay(100);
  float ph = (resp[3]<<8 | resp[4]) / 100.0;

  sendQuery(condQuery);
  delay(100);
  int ec = (resp[3]<<8 | resp[4]);

  sendQuery(npkQuery);
  delay(100);
  int n = (resp[3]<<8 | resp[4]);
  int p = (resp[5]<<8 | resp[6]);
  int k = (resp[7]<<8 | resp[8]);

  Serial.println("----- SENSOR DATA -----");
  Serial.print("Moisture: "); Serial.println(moisture);
  Serial.print("Temp: "); Serial.println(temp);
  Serial.print("pH: "); Serial.println(ph);
  Serial.print("EC: "); Serial.println(ec);
  Serial.print("N: "); Serial.println(n);
  Serial.print("P: "); Serial.println(p);
  Serial.print("K: "); Serial.println(k);

  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;

    String url = "http://api.thingspeak.com/update?api_key=" + apiKey +
                 "&field1=" + String(moisture) +
                 "&field2=" + String(temp) +
                 "&field3=" + String(ph) +
                 "&field4=" + String(ec) +
                 "&field5=" + String(n) +
                 "&field6=" + String(p) +
                 "&field7=" + String(k);

    Serial.println("Sending to ThingSpeak...");
    Serial.println(url); 

    http.begin(url);
    int httpCode = http.GET();

    Serial.print("HTTP Response: ");
    Serial.println(httpCode);

    if(httpCode == 200){
      Serial.println("Data uploaded successfully!");
    } else {
      Serial.println(" Upload failed!");
    }

    http.end();
  }

  Serial.println("-----------------------------");

  delay(20000);
}