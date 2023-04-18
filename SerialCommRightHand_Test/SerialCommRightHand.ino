#include<Servo.h>

String cmdCV2;
Servo thumb, index, middle, ring, pinky;

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);

}

void loop() {
  while(!Serial.available()){

  }

  myCmd = Serial.readStringUntil('\r');

  for (int i= 0; i<5; i++) {
    Serial.println(myCmd.substring(i,i+1));
    ledMode = myCmd.substring(i,i+1).toInt();
    digitalWrite(13, ledMode);
    delay(1000);    
  }
  /*
  if(myCmd == "ON") {
    digitalWrite(13, HIGH);
  }
  else if (myCmd == "OFF") {
    digitalWrite(13, LOW);
  }
  else {
  Serial.println("Unidentified Command Detected!");
  }
  */

}
