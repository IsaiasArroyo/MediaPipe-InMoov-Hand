#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca9685 = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 500

// ===== CANALES PCA9685 =====
#define thumb   0
#define index   1
#define majeure 2
#define ring    3
#define pinky   4
#define wrist   5
#define bicep   6

String data = "";

int angulo(int ang){
  return map(ang,0,180,SERVOMIN,SERVOMAX);
}

void setup() {

  Serial.begin(115200);

  pca9685.begin();
  pca9685.setPWMFreq(50);
}

void loop() {

  if(Serial.available()){

    data = Serial.readStringUntil('\n');

    int t,i,m,r,p,w,b;

    sscanf(data.c_str(),
           "%d,%d,%d,%d,%d,%d,%d",
           &t,&i,&m,&r,&p,&w,&b);

    moverServos(t,i,m,r,p,w,b);
  }
}

void moverServos(int t,int i,int m,int r,int p,int w,int b){

  //===== HAND =====
  pca9685.setPWM(thumb,0,angulo(t));
  pca9685.setPWM(index,0,angulo(i));
  pca9685.setPWM(majeure,0,angulo(m));
  pca9685.setPWM(ring,0,angulo(r));
  pca9685.setPWM(pinky,0,angulo(p));
  pca9685.setPWM(wrist,0,angulo(w));

  // ===== BICEP =====
  pca9685.setPWM(bicep,0,angulo(b));
}