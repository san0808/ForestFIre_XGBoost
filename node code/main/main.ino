#include <ESP8266WiFi.h>
#include <DHT.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define DHTPIN D2
#define DHTTYPE DHT11
#define WIFI_SSID "Sandeep" // Replace with your WiFi SSID
#define WIFI_PASSWORD "Sandeep6261" // Replace with your WiFi Password
#define SERVER_URL "http://192.168.1.41:8000/predict"

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  connectToWiFi();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" *C ");

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    sendToServer(temperature, humidity);
  }

  delay(10000); // Delay between readings
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println(" connected");
}

void sendToServer(float temperature, float humidity) {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client; // Create a WiFiClient object
    HTTPClient http;

    http.begin(client, SERVER_URL); // Use the new begin() method
    http.addHeader("Content-Type", "application/json"); // Specify content-type header

    // Prepare JSON data
    DynamicJsonDocument doc(1024);
    doc["temp"] = temperature;
    doc["RH"] = humidity;
    doc["rain"] = 0.0;
    doc["wind"] = 0.0;
    String jsonPayload;
    serializeJson(doc, jsonPayload);
    Serial.println(jsonPayload);
    int httpCode = http.POST(jsonPayload); // Send the request
    Serial.print("HTTP Status Code: ");
    Serial.println(httpCode);

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Received response:");
      Serial.println(payload);
    } else {
      Serial.print("Error sending POST request: ");
      Serial.println(httpCode);
      Serial.println(http.errorToString(httpCode).c_str()); // Print HTTP error
    }



    http.end(); // Close connection
  } else {
    Serial.println("Not connected to WiFi");
  }
}




