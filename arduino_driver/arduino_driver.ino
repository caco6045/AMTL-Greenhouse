#include <DHT.h>
#include <DHT_U.h>
#include "DHT.h"
//Make sure to install DHT22 and Adafruit Universal Libraries

#define DHTPIN 3     // DHT sensor pin
#define floatSwitch 2 //Float input pin
#define led 13        //LED pin

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321 
DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor. 

void setup() {
  pinMode(floatSwitch,INPUT_PULLUP);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  
  //dht sensor
  dht.begin();
}

void loop() {
  char serIn;
  delay(2000);
  //data from pi
  while(Serial.available()>0){
    serIn=Serial.read();
    if (serIn=='A') { 
      digitalWrite(led, HIGH);
    }
    else if(serIn=='B'){
      digitalWrite(led, LOW);
    }
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

  //float switch
  int floatVal = digitalRead(floatSwitch); 
  if (floatVal == 1){
    //digitalWrite(led, HIGH);
    Serial.println(floatVal);
  }
  else{
    //digitalWrite(led, LOW);
    Serial.println(floatVal);
  }
  
//  Serial.print("Humidity: ");
    Serial.println(h);
    //Serial.print(" %\n");
//  Serial.print("Temperature: ");
//  Serial.print(t);
//  Serial.print(" *C ");
    Serial.println(f);
    //Serial.print(" *F\n");
//  Serial.print("Heat index: ");
//  Serial.print(hic);
//  Serial.print(" *C ");
//  Serial.print(hif);
//  Serial.println(" *F");
//  Serial.println(h);
//  Serial.println("%\n");


}
