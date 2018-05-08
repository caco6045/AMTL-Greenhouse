#include <DHT.h>
#include <DHT_U.h>
#include "DHT.h"
//Make sure to install DHT22 and Adafruit Universal Libraries

#define DHTPIN 3     // DHT sensor pin
#define floatSwitch 2 //Float input pin
#define led 13        //LED pin
#define fan 11 //fan pin
#define pump 4 //pump pin

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321 
DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor.

#define sensorPin A0
#define offset -2.00 //Calibration Variable
int pHRead;
float temp_max=200;  //used for debugging
//initialize variables used in timer code
int pump_timer;
int light_timer;
int pump_timer_off;
int light_timer_off;
float time_run;
float light_end=0;
float light_on=0;
float pump_end=0;
bool pump_on=0;
bool pump_switch=0;
float pump_switch_end=0;
int on=0;

void setup() {
  pinMode(floatSwitch,INPUT_PULLUP);  //pin initialization
  pinMode(fan,OUTPUT);
  pinMode(pump,OUTPUT);
  Serial.begin(9600);
  
  //dht sensor
  dht.begin();  //temp sensor initialization
}

void loop() {
  char serIn;
  
  //temperature sensor code
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  //float h=20; //used for debugging
  // Read temperature as Celsius (the default)
  //float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true)-1.5;
  //float f=70;  //used for debugging

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
  //static float pHValue=7.1;  //used for debugging
  
  if (floatVal == 1){
    Serial.println(floatVal);  //send float sensor data to serial port
  }
  else{
    Serial.println(floatVal);
  }

    Serial.println(h);  //send sensor data to serial port
    Serial.println(f);
    Serial.println(pHValue);

    //data from pi
  while(Serial.available()>0){
    serIn=Serial.read();
    if (serIn=='A') { //Patio Tomato
      temp_max=30;
      pump_timer=900;
      pump_timer_off=13500;  //timer values for each plant
      light_timer=43200;
      light_timer_off=43200;
      pump_end=0;
      pump_on=0;
      light_end=0;
      light_on=0;
    }
    else if (serIn=='B') {  //Spinach
      temp_max=30;
      pump_timer=900;
      pump_timer_off=13500;
      light_timer=64800;
      light_timer_off=21600;
      pump_end=0;
      pump_on=0;
      light_end=0;
      light_on=0;
    }
    else if(serIn=='C') {  //Broccoli
      temp_max=30;
      pump_timer=900;
      pump_timer_off=43200;
      light_timer=64800;
      light_timer_off=21600;
      pump_end=0;
      pump_on=0;
      light_end=0;
      light_on=0;
    }
    else if(serIn=='D') {  //if pump button is pressed
      pump_switch=1;
    }
  }

  if(f>temp_max)
  {
    digitalWrite(fan,HIGH);   //if temp is too hot turn on fan
  }
  else
  {
    digitalWrite(fan,LOW);  //if temp is back in range turn fan off
  }

  time_run=millis()/1000;  //time in seconds arduino has been running

  if(pump_switch==1)  //if pump button has been pressed
  {
    if(pump_switch_end==0)  //first pass through loop
    {
      if(floatVal==on)  //float sensor indicates pumping is ok
        digitalWrite(pump,HIGH); //pump
      pump_switch_end=time_run+30;  //set end time of pumping to be 30 seconds
    }

    if(time_run>=pump_switch_end) //if 30 seconds of pumping is up
    {
      digitalWrite(pump,LOW); //turn pump off
      pump_switch_end=0;  //reset variables
      pump_switch=0;
    }
    else  //otherwise pump is still in 30 second time period
      if(floatVal==!on)  //if float says not ok to pump turn off pump
        digitalWrite(pump,LOW);
  }
  
  if(pump_end==0)  //first time through loop
  {
    if(floatVal==on&&pump_switch==0) //as long as pumping is allowed by float value and pump button hasnt been pressed
      digitalWrite(pump,HIGH); //begin pumping
    pump_end=time_run+pump_timer;  //pump for time given above
    pump_on=1; //set pump to being on
  }

  if(pump_on==1) //if pump is already on
  {
    if(time_run>=pump_end) //time is now outside of pumping time period
    {
      if(pump_switch==0) //if pump button hasn't been pressed turn off pump
        digitalWrite(pump,LOW);
      pump_on=0;
      pump_end=time_run+pump_timer_off;
    }
    else
      if(floatVal==!on&&pump_switch==0) //else still pumping
        digitalWrite(pump,LOW);
  }
  else if(pump_on==0) //pump is currently off
  {
    if(time_run>=pump_end)  //pump should begin to pump
    {
      if(floatVal==on&&pump_switch==0)  //as long as resevor has water and pump button not pressed begin pumping
        digitalWrite(pump,HIGH);
      pump_on=1;
      pump_end=time_run+pump_timer;  //set amount of time for pump to be on
    }
  }
 

  if(light_end==0)  //light timer code is same as pump timer except with different timer values and it isn't affected by the float sensor or pump button
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
      light_end=time_run+light_timer_off;
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
  
  delay(1000); //one second delay between loop iterations


}
