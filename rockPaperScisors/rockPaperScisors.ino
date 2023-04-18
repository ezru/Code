#include<Servo.h>

String fingerState;
Servo thumb, index, middle, ring, pinky;

Servo bicepServo, sholderLtRt, sholderFwdBkd, shoulderUpDown;
int bicepAngle, sholderLtRtAngle, sholderFwdBkdAngle, shoulderUpDownAngle;


void setup() {

  Serial.begin(9600);

  thumb.attach(13);
  index.attach(12);
  middle.attach(11);
  ring.attach(10);
  pinky.attach(9);

  bicepServo.attach(7);
  sholderLtRt.attach(6);
  sholderFwdBkd.attach(5);
  shoulderUpDown.attach(4);
  
  bicepServo.write(60);
  sholderLtRt.write(000);
  sholderFwdBkd.write(000);
  shoulderUpDown.write(020);

}

void loop() {

  while (Serial.available()) {

    fingerState = Serial.readStringUntil('\r');

   /* sholderLtRt.write(030);
    sholderFwdBkd.write(045);
    turnServo(bicepServo, 180, false);
    turnServo(bicepServo, 0, true);
    turnServo(bicepServo, 180, false);
    turnServo(bicepServo, 0, true);
    turnServo(bicepServo, 180, false);
    turnServo(bicepServo, 0, true);
*/

    fingerPos(thumb, fingerState.substring(0,1).toInt());
    fingerPos(index, fingerState.substring(1,2).toInt());
    fingerPos(middle, fingerState.substring(2,3).toInt());
    fingerPos(ring, fingerState.substring(3,4).toInt());
    fingerPos(pinky, fingerState.substring(4,5).toInt());
  }

}

void fingerPos(Servo finger, int state) {
  if (state == 1){
    finger.write(180);
  }else {
    finger.write(0);
  }

}

void turnServo(Servo myServo, int angle, bool rev) {
    if (rev == false) {
    for(int i = 0; i < angle; i++){
      myServo.write(i);
      Serial.println(i);
    }
  } else {
    for(int i = 180; i > angle; i--){
      myServo.write(i);
      Serial.println(i);
    }
  }
  
}
