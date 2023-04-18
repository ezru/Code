#include <Servo.h>

String rightArmCmds;

Servo bicepServo, sholderLtRt, sholderFwdBkd, shoulderUpDown;
int bicepAngle, sholderLtRtAngle, sholderFwdBkdAngle, shoulderUpDownAngle;

void setup() {
  Serial.begin(9600);
  bicepServo.attach(7);
  sholderLtRt.attach(6);
  sholderFwdBkd.attach(5);
  shoulderUpDown.attach(4);
  
  bicepServo.write(020);
  sholderLtRt.write(020);
  sholderFwdBkd.write(020);
  shoulderUpDown.write(020);

}

void loop() {
  while(!Serial.available()){
    delay(10);
  }

  bicepServo.write(65);

  rightArmCmds = Serial.readStringUntil('\r');

  bicepAngle = rightArmCmds.substring(0, 2).toInt();
  sholderLtRtAngle = rightArmCmds.substring(2, 5).toInt();
  sholderFwdBkdAngle = rightArmCmds.substring(5, 8).toInt();
  shoulderUpDownAngle = rightArmCmds.substring(8, 10).toInt();

  if (bicepAngle > 65){
    bicepServo.write(65);
  }
  else if (bicepAngle < 0){
    bicepServo.write(10);
  }
  else if (bicepAngle <= 65 && bicepAngle >= 10){
    bicepServo.write(bicepAngle);
  }
  else {
    bicepServo.write(40);
  }

  if (shoulderUpDownAngle > 90){
    shoulderUpDown.write(90);
  }
  else if (shoulderUpDownAngle < 0){
    shoulderUpDown.write(0);
  }
  else if (shoulderUpDownAngle <= 90 && shoulderUpDownAngle >= 0){
    shoulderUpDown.write(shoulderUpDownAngle);
  }
  else {
    shoulderUpDown.write(40);
  }

  sholderLtRt.write(sholderLtRtAngle);
  sholderFwdBkd.write(sholderFwdBkdAngle);

}

