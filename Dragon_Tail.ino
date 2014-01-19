/******Dragon Tail Example Code*******************

 created 26 Oct 2011
 By Jeremie Boulianne for Solarbotics Ltd.

 This example code is in the public domain.

*************************************************/

#include <Servo.h>

// Setup objects from Libraries
Servo panServo;              // Panning Servo located at the front of the DragonTail
Servo LServo;                // Left continous Rotation Servo
Servo RServo;                // Right continous Rotation Servo

// Initialize Variables
int RBump = 5;               // Right bump sensor attached to digital pin 5
int LBump = 3;               // Left bump sensor attached to digital pin 3
int BumpLVal = 0;            // Value for Left Bump Sensor
int BumpRVal = 0;            // Value for Left Bump Sensor
int sensorPin = 17;          // Infrared distance sensor attached to Analog pin 3 aka pin 17
int sensorVal = 0;           // Value for Infrared distance Sensor
int sensThres = 400;         // Infrared distance sensor threshold value, lower this value for higher sensitivity (longer range)
int delayVal = 700;          // Delay value for turning, lower this value for a shorter turn
int pos = 0;                 // Value for Servo position

/*************Setup Function*********************/
void setup() 
{
 
  Serial.begin(57600);    // Initialize serial communication
  pinMode(RBump, INPUT);  // Configure Right bump Sensor pin (5) as an Input
  pinMode(LBump, INPUT);  // Configure Left bump Sensor pin (3) as an Input
  LServo.attach(2);       // Left Servo attached to digital pin 2
  RServo.attach(4);       // Right Servo attached to digital pin 4
  panServo.attach(6);     // Panning Servo attached to Pin 6
  panServo.write(90);     // Start panServo at 90º looking from the 
                          // tail of the robot to the front 
                          // 45 = pan right to the 45º position, 135 = pan left to 135º
  delay(250);             // Make sure the panServo is set and ready
 
}


/*************Main Loop*********************/
void loop()
{
                          // Remove the slashes to enable Test modes but at the same time
                         // add slashes to the other functions so you don't get mixed results
                         
  //motorTest();
  //sensorTest();        
  roaming();
  
}

/***************Functions*********************/

// Demo function to test Servos
void motorTest()
{
    StopMtrs();
    delay(250);
 
    panServo.write(90);
    delay(500);
  
    MtrsFwd();
    
    panServo.write(45);
    delay(500);                       

    StopMtrs();
    delay(250);
 
    panServo.write(90);
    delay(500);
  
    MtrsBwd(); 
  
    panServo.write(135);
    delay(500);                       
  
    StopMtrs();
    delay(250);
} 

// Demo Function to test Sensors
void sensorTest(){

Serial.print("IRsensor Value = ");
Serial.println(analogRead(sensorPin));      // Display the analog value of the Infrared sensor
Serial.print("RBump Value = ");
Serial.println(digitalRead(RBump));        // Display the status of the Right Bump Sensor, default being '0' and '1' when activated
Serial.print("LBump Value = ");
Serial.println(digitalRead(LBump));        // Display the status of the Left Bump Sensor, default being '0' and '1' when activated
delay(200);

}

// Roaming function to cruise around and avoid obstacles
void roaming()
{

 for(pos = 90; pos < 135; pos += 1){  // Servo sweeps from 90 degrees to 135 degrees in steps of 1 degree 
                                      
    panServo.write(pos);              // Tell servo to go to position in variable 'pos' 
    BumpTest();                       // Test to see if any of the bump sensors were activated
    MtrsFwd();                        // Move DragonTail forward
    
     sensorVal = analogRead(sensorPin);   
     if (sensorVal > sensThres){     // Test to see if the Infrared sensor has seen anything above the threshold
    
         MtrsL();                    // Turn left for as long as the delayVal is set for
         delay(delayVal);      
        } 
        
        delay(10);                   // This delay helps overcome current spikes from the servos to avoid brownouts on the Arduino
 }
  for(pos = 135; pos>=90; pos-=1){   // Servo sweeps from 135 degrees to 90 degrees in steps of 1 degree 
                                 
    panServo.write(pos);              
    BumpTest();
    MtrsFwd();
    
      sensorVal = analogRead(sensorPin); 
      if (sensorVal > sensThres){ 
    
         MtrsL();
         delay(delayVal);      
        }
       
       delay(10); 
  }
  
  
  for(pos = 90; pos>=45; pos-=1){     // Servo sweeps from 90 degrees to 45 degrees in steps of 1 degree 
                                  
    panServo.write(pos);              
    BumpTest();
    MtrsFwd();
    
    sensorVal = analogRead(sensorPin); 
      if (sensorVal > sensThres){ 
    
         MtrsR();
         delay(delayVal);     
        } 
        
        delay(10);
  }
  
  for(pos = 45; pos < 90; pos += 1){  // Servo sweeps from 45 degrees to 90 degrees in steps of 1 degree 
                                   
    panServo.write(pos);               
    BumpTest();
    MtrsFwd();
    
     sensorVal = analogRead(sensorPin);   
         
         if (sensorVal > sensThres){ 
    
         MtrsR();
         delay(delayVal);      
        } 
       
       delay(10);
  }
  }

// Function used by  to poll the front Bump Sensors for hits  
void BumpTest(){

BumpLVal = digitalRead(RBump);
BumpRVal = digitalRead(LBump);

while (BumpRVal == HIGH && BumpLVal == HIGH) { // If both bump sensors are activated move DragonTail Right
  
  MtrsR();
  delay(100); 
  BumpLVal = digitalRead(RBump);
  BumpRVal = digitalRead(LBump);
  
}

while (BumpRVal == HIGH && BumpLVal == LOW) { // If the Right bump sensor is activated move DragonTail Left
 
  MtrsL();
  delay(100); 
  BumpLVal = digitalRead(RBump);
  BumpRVal = digitalRead(LBump);
}

while (BumpRVal == LOW && BumpLVal == HIGH) { // If the Left bump sensor is activated move DragonTail Right
 
  MtrsR();
  delay(100); 
  BumpLVal = digitalRead(RBump);
  BumpRVal = digitalRead(LBump);
}

}
  
// Function to Stop robot movement
void StopMtrs(){
  
LServo.write(90);
RServo.write(90);
    
}

// Function to move robot Forward
void MtrsFwd(){
  
LServo.write(180);
RServo.write(0);
    
}

// Function to move robot Backward
void MtrsBwd(){
  
LServo.write(0);
RServo.write(180);
    
}

// Function to move robot Left
void MtrsL(){
  
LServo.write(180);
RServo.write(180);
    
}

// Function to move robot Right
void MtrsR(){
  
LServo.write(0);
RServo.write(0);
    
}



