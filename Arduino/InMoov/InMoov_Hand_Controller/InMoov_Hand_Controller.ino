#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca9685 = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 500

// =====================================================
// CANALES PCA9685
// =====================================================
#define THUMB_CH   0
#define INDEX_CH   1
#define MIDDLE_CH  2
#define RING_CH    3
#define PINKY_CH   4
#define WRIST_CH   5
#define BICEP_CH   6
#define SHOULDER_CH 7

// =====================================================
// VARIABLES
// =====================================================
char data[64];

// =====================================================
// MAPEO ANGULO -> PWM
// =====================================================
int anguloToPWM(int angulo){

  angulo = constrain(angulo, 0, 180);

  return map(
    angulo,
    0,
    180,
    SERVOMIN,
    SERVOMAX
  );
}

// =====================================================
// MOVER SERVO
// =====================================================
void moverServo(int canal, int angulo){

  int pwm = anguloToPWM(angulo);

  pca9685.setPWM(
    canal,
    0,
    pwm
  );
}

// =====================================================
// SETUP
// =====================================================
void setup() {

  Wire.begin();

  // IMPORTANTE
  // Mejora estabilidad I2C
  Wire.setClock(100000);

  Serial.begin(115200);

  pca9685.begin();

  pca9685.setPWMFreq(50);

  delay(500);

  // Posicion inicial
  moverServo(THUMB_CH, 90);
  moverServo(INDEX_CH, 90);
  moverServo(MIDDLE_CH, 90);
  moverServo(RING_CH, 90);
  moverServo(PINKY_CH, 90);
  moverServo(WRIST_CH, 90);
  moverServo(BICEP_CH, 0);
  moverServo(SHOULDER_CH, 90);
}

// =====================================================
// LOOP
// =====================================================
void loop() {

  // ===============================================
  // LEER SERIAL
  // ===============================================
  if (Serial.available()) {

    int len = Serial.readBytesUntil(
      '\n',
      data,
      sizeof(data) - 1
    );

    // terminar string
    data[len] = '\0';

    // ===========================================
    // VARIABLES
    // ===========================================
    int t,i,m,r,p,w,b,h;

    // ===========================================
    // PARSEAR DATOS
    // ===========================================
    int valores = sscanf(
      data,
      "%d,%d,%d,%d,%d,%d,%d,%d",
      &t,&i,&m,&r,&p,&w,&b,&h
    );

    // ===========================================
    // VALIDAR
    // ===========================================
    if (valores == 8) {

      t = constrain(t,0,180);
      i = constrain(i,0,180);
      m = constrain(m,0,180);
      r = constrain(r,0,180);
      p = constrain(p,0,180);
      w = constrain(w,0,180);
      b = constrain(b,0,180);
      h = constrain(h,0,180);

      // =======================================
      // MOVER SERVOS
      // =======================================
      moverServo(THUMB_CH,  t);
      moverServo(INDEX_CH,  i);
      moverServo(MIDDLE_CH, m);
      moverServo(RING_CH,   r);
      moverServo(PINKY_CH,  p);

      moverServo(WRIST_CH,  w);

      moverServo(BICEP_CH,  b);

      moverServo(SHOULDER_CH, h);
    }
  }
}