#include <Servo.h>

String myCmd;
Servo myServo;

void setup() {
  Serial.begin(9600);
  myServo.attach(4);


}

void loop() {
  while(!Serial.available()){
    delay(10);
  }

  myCmd = Serial.readStringUntil('\r');
  if (myCmd.toInt() > 80){
    myServo.write(80);
  }
  else if (myCmd.toInt() < 0){
    myServo.write(0);
  }
  else if (myCmd.toInt() <= 80 && myCmd.toInt() >= 0){
    myServo.write(myCmd.toInt());
  }
  else {
    myServo.write(40);
  }
  

}

