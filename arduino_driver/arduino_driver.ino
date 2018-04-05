#include <DHT.h>
#include <DHT_U.h>
#include "DHT.h"
//Make sure to install DHT22 and Adafruit Universal Libraries

#define DHTPIN 3     // DHT sensor pin
#define floatSwitch 2 //Float input pin
#define led 13        //LED pin

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321 
DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor.

#define sensorPin A0 //Analog pin, aka pin 14
#define offset 0.00 //Calibration variable, maybe not useful
//pH sensor to be plugged into A0 (blue), 5v (red), and ground (black)

int pHRead;

void setup() {
  pinMode(floatSwitch, INPUT_PULLUP);
  pinMode(led, OUTPUT);
  Serial.begin(9600);

  //dht sensor
  dht.begin();
  Serial.println("The strings will be outputted as: T,h,Float switch, pH");
}

void loop() {
  delay(2000);
  //float switch
  int floatVal = digitalRead(floatSwitch);
  if (floatVal == 1) {
    digitalWrite(led, HIGH);
    //Serial.println("Switch is Open!");
  }
  else {
    digitalWrite(led, LOW);
    //Serial.println("Switch is Closed!");
  }

  //temperature sensor code
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);
  //pH meter readings
  static float pHValue, pHVoltage;
  pHRead = analogRead(sensorPin);
  pHVoltage = pHRead * 5.0 / 1024;
  pHValue = 3.5 * pHVoltage + offset; //for calibration, need to play with 3.5 and offse


}
