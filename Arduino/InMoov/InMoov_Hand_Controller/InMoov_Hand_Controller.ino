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

// ===== MOTOR HOMBRO =====
#define IN1 8
#define IN2 9
#define POT_HOMBRO A0

// ===== CALIBRACION =====
#define POT_MIN 200
#define POT_MAX 800

#define TOLERANCIA 10

String data = "";

// =====================================================
// ANGULO -> PWM
// =====================================================
int angulo(int ang){
  return map(ang,0,180,SERVOMIN,SERVOMAX);
}

// =====================================================
// ANGULO -> POT
// =====================================================
int anguloPot(int ang){
  return map(ang,0,180,POT_MIN,POT_MAX);
}

void setup() {

  Serial.begin(115200);

  // PCA9685
  pca9685.begin();
  pca9685.setPWMFreq(50);

  // Motor hombro
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

// =====================================================
// LOOP
// =====================================================
void loop() {

  if(Serial.available()){

    data = Serial.readStringUntil('\n');

    int t,i,m,r,p,w,b,h;

    sscanf(data.c_str(),
           "%d,%d,%d,%d,%d,%d,%d,%d",
           &t,&i,&m,&r,&p,&w,&b,&h);

    moverServos(t,i,m,r,p,w,b);

    moverHombro(h);
  }
}

// =====================================================
// SERVOS PCA9685
// =====================================================
void moverServos(int t,int i,int m,int r,int p,int w,int b){

  pca9685.setPWM(thumb,0,angulo(t));
  pca9685.setPWM(index,0,angulo(i));
  pca9685.setPWM(majeure,0,angulo(m));
  pca9685.setPWM(ring,0,angulo(r));
  pca9685.setPWM(pinky,0,angulo(p));
  pca9685.setPWM(wrist,0,angulo(w));

  // BICEP SIGUE NORMAL
  pca9685.setPWM(bicep,0,angulo(b));
}

// =====================================================
// CONTROL HOMBRO
// =====================================================
void moverHombro(int anguloDeseado){

  int objetivo = anguloPot(anguloDeseado);

  int posicion = analogRead(POT_HOMBRO);

  Serial.print("Hombro: ");
  Serial.print(posicion);
  Serial.print(" -> ");
  Serial.println(objetivo);

  // Mover adelante
  if(posicion < objetivo - TOLERANCIA){

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
  }

  // Mover atras
  else if(posicion > objetivo + TOLERANCIA){

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
  }

  // Detener
  else{

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
  }
}