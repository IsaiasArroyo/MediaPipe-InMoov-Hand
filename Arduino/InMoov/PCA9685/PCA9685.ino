#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca9685 = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 500

// Canales PCA9685
#define thumb   0
#define index   1
#define majeure 2
#define ring    3
#define pinky   4
#define bicep   6

int angulo(int ang){
  return map(ang, 0, 180, SERVOMIN, SERVOMAX);
}

void setup() {

  Serial.begin(115200);

  pca9685.begin();
  pca9685.setPWMFreq(50);

  alltorest();

  delay(2000);
}

void loop() {

  //alltorest();
  calibrarBicep();

  delay(3000);
}

// ==============================
// FUNCION DE CALIBRACION
// ==============================
void calibrarBicep(){

  // Va de 0 a 85 grados lentamente
  for(int grados = 0; grados <= 75; grados++){

    pca9685.setPWM(bicep, 0, angulo(grados));

    Serial.print("Bicep en grados: ");
    Serial.println(grados);

    delay(50); // velocidad del movimiento
  }

  delay(2000);

  // Regresa lentamente de 85 a 0
  for(int grados = 75; grados >= 0; grados--){

    pca9685.setPWM(bicep, 0, angulo(grados));

    Serial.print("Bicep en grados: ");
    Serial.println(grados);

    delay(50);
  }
}

// equivalente a servothumb.write(0)
void alltorest(){

  pca9685.setPWM(thumb,   0, angulo(0));
  pca9685.setPWM(index,   0, angulo(0));
  pca9685.setPWM(majeure, 0, angulo(0));
  pca9685.setPWM(ring,    0, angulo(0));
  pca9685.setPWM(pinky,   0, angulo(0));
  pca9685.setPWM(bicep,   0, angulo(0));
}

// equivalente a servothumb.write(180)
void alltomax(){

  pca9685.setPWM(thumb,   0, angulo(180));
  pca9685.setPWM(index,   0, angulo(180));
  pca9685.setPWM(majeure, 0, angulo(180));
  pca9685.setPWM(ring,    0, angulo(180));
  pca9685.setPWM(pinky,   0, angulo(180));
  pca9685.setPWM(bicep,   0, angulo(75));
}