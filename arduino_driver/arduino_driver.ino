#include <DHT.h>
#include <DHT_U.h>
#include "DHT.h"
//Make sure to install DHT22 and Adafruit Universal Libraries

#define DHTPIN 3     // DHT sensor pin
#define floatSwitch 2 //Float input pin
#define led 13        //LED pin
#define fan 11 //fan pin
#define pump 12 //pump pin

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321 
DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor. 

#define sensorPin A0
#define offset 0.00 //Calibration Variable
int pHRead;
float temp_max=200;
int pump_timer;
int light_timer;
float time_run;
float light_end=0;
float light_on=0;
float pump_end=0;
bool pump_on=0;
bool pump_switch=0;
float pump_switch_end=0;

void setup() {
  pinMode(floatSwitch,INPUT_PULLUP);
  pinMode(fan,OUTPUT);
  pinMode(pump,OUTPUT);
  Serial.begin(9600);
  
  //dht sensor
  dht.begin();
}

void loop() {

  char serIn;
  
  //temperature sensor code
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  //float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(f)) {
    float failed=-1;
    Serial.println(failed);
    return;
  }
  
  // Compute heat index in Fahrenheit (the default)
  //float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  //float hic = dht.computeHeatIndex(t, h, false);

  //float switch
  int floatVal = digitalRead(floatSwitch); 

  //pH sensor
  static float pHValue, pHVoltage;
  pHRead = analogRead(sensorPin);
  pHVoltage = pHRead*5.0/1024;
  pHValue = 3.5*pHVoltage + offset;
  
  if (floatVal == 1){
    Serial.println(floatVal);
  }
  else{
    Serial.println(floatVal);
  }

    Serial.println(h);
    Serial.println(f);
    Serial.println(pHValue);

    //data from pi
  while(Serial.available()>0){
    serIn=Serial.read();
    if (serIn=='A') {
      temp_max=79;
      pump_timer=2;
      light_timer=2;
      pump_end=0;
      pump_on=0;
      light_end=0;
      light_on=0;
    }
    else if (serIn=='B') {
      temp_max=80;
      pump_timer=10;
      light_timer=10;
      pump_end=0;
      pump_on=0;
      light_end=0;
      light_on=0;
    }
    else if(serIn=='C') {
      temp_max=70;
      pump_timer=20;
      light_timer=20;
      pump_end=0;
      pump_on=0;
      light_end=0;
      light_on=0;
    }
    else if(serIn=='D') {
      pump_switch=1;
    }
  }

  if(f>temp_max)
  {
    digitalWrite(fan,HIGH);
  }
  else
  {
    digitalWrite(fan,LOW);
  }

  time_run=millis()/1000;

  if(pump_switch==1)
  {
    if(pump_switch_end==0)
    {
      if(floatVal==1)
        digitalWrite(pump,HIGH);
      pump_switch_end=time_run+30;
    }

    if(time_run>=pump_switch_end)
    {
      digitalWrite(pump,LOW);
      pump_switch_end=0;
      pump_switch=0;
    }
  }
  else if(pump_switch==0)
  {
    if(pump_end==0)  
    {
      if(floatVal==1)
        digitalWrite(pump,HIGH);
      pump_end=time_run+pump_timer;
      pump_on=1;
    }
  
    if(pump_on==1)
    {
      if(time_run>=pump_end)
      {
        digitalWrite(pump,LOW);
        pump_on=0;
        pump_end=time_run+pump_timer;
      }
    }
    else if(pump_on==0)
    {
      if(time_run>=pump_end)
      {
        if(floatVal==1)
          digitalWrite(pump,HIGH);
        pump_on=1;
        pump_end=time_run+pump_timer;
      }
    }
  }
  
  if(light_end==0)  
  {
    
    digitalWrite(led,HIGH);
    light_end=time_run+light_timer;
    light_on=1;
  }

  if(light_on==1)
  {
    if(time_run>=light_end)
    {
      digitalWrite(led,LOW);
      light_on=0;
      light_end=time_run+light_timer;
    }
  }
  else if(light_on==0)
  {
    if(time_run>=light_end)
    {
      digitalWrite(led,HIGH);
      light_on=1;
      light_end=time_run+light_timer;
    }
  }
  delay(1000);


}
