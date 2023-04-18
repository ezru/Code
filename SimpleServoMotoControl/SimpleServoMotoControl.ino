#include <Servo.h>

Servo rightBicepServo;



int pos = 0;


void setup() {
  rightBicepServo.attach(9);
}

void loop() {
  rightBicepServo.write(0);
  delay(1000);
  rightBicepServo.write(100);
  delay(1000);

}
