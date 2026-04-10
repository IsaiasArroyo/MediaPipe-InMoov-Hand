#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca9685 = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 500

// Canales PCA9685
#define thumb 0
#define index 1
#define majeure 2
#define ring 3
#define pinky 4

int angulo(int ang){
  return map(ang,0,180,SERVOMIN,SERVOMAX);
}

void setup() {

  pca9685.begin();
  pca9685.setPWMFreq(50);

}

void loop() {

  alltorest();
  delay(4000);

  alltomax();
  delay(2000);

}

// equivalente a servothumb.write(0) etc
void alltorest(){

  pca9685.setPWM(thumb,0,angulo(0));
  pca9685.setPWM(index,0,angulo(0));
  pca9685.setPWM(majeure,0,angulo(0));
  pca9685.setPWM(ring,0,angulo(0));
  pca9685.setPWM(pinky,0,angulo(0));

}

// equivalente a servothumb.write(180) etc
void alltomax(){

  pca9685.setPWM(thumb,0,angulo(180));
  pca9685.setPWM(index,0,angulo(180));
  pca9685.setPWM(majeure,0,angulo(180));
  pca9685.setPWM(ring,0,angulo(180));
  pca9685.setPWM(pinky,0,angulo(180));

}