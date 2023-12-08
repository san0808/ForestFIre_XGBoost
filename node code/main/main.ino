#include <ESP8266WiFi.h>
#include <DHT.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define DHTPIN D2
#define DHTTYPE DHT11
#define WIFI_SSID "Sanket bhat" // Replace with your WiFi SSID
#define WIFI_PASSWORD "sankey123" // Replace with your WiFi Password
#define SERVER_IP "192.168.128.34"
#define SERVER_PORT 8000

DHT dht(DHTPIN, DHTTYPE);
WiFiClient client;

float humidity;
float temperature;

void setup() {
  Serial.begin(9600);
  dht.begin();
  while(connectToWiFi()) {}
}

void loop() {
  server.handleClient();
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" *C ");

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
  }

  delay(10000); // Delay between readings
}

bool connectToWiFi() {
  Serial.print("Connecting to WiFi \n");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  delay(1000);
  return WiFi.status() != WL_CONNECTED;
}

void sendToServer(float temperature, float humidity) {
  if (WiFi.status() == WL_CONNECTED) {
    if (client.connect(SERVER_IP, SERVER_PORT)) {
      Serial.println("Connected to server");

      // Prepare JSON data
      DynamicJsonDocument doc(1024);
      doc["temp"] = temperature;
      doc["RH"] = humidity;
      doc["rain"] = 0.0;
      doc["wind"] = 0.0;
      String jsonPayload;
      serializeJson(doc, jsonPayload);
      Serial.println(jsonPayload);

      // Send data to server
      client.print("POST /predict HTTP/1.1\r\n");
      client.print("Host: ");
      client.print(SERVER_IP);
      client.print(":");
      client.println(SERVER_PORT);
      client.println("Content-Type: application/json");
      client.print("Content-Length: ");
      client.println(jsonPayload.length());
      client.println();
      client.println(jsonPayload);

      // Wait for server response
      delay(1000);
      while (client.available()) {
        Serial.write(client.read());
      }

      client.stop();
    } else {
      Serial.println("Unable to connect to server");
    }
  } else {
    Serial.println("Not connected to WiFi");
  }
}





