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

// =====================================================
// HOMBRO (MOTOR DC + PUENTE H)
// =====================================================
#define IN1 8
#define IN2 9

#define POT_PIN A0

// =====================================================
// VARIABLES
// =====================================================
char data[64];

int objetivoHombro = 884;

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

  Wire.setClock(100000);

  Serial.begin(115200);

  pca9685.begin();

  pca9685.setPWMFreq(50);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  delay(500);

  // ===============================================
  // POSICION INICIAL
  // ===============================================
  moverServo(THUMB_CH, 90);
  moverServo(INDEX_CH, 90);
  moverServo(MIDDLE_CH, 90);
  moverServo(RING_CH, 90);
  moverServo(PINKY_CH, 90);

  moverServo(WRIST_CH, 90);

  moverServo(BICEP_CH, 0);
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

      h = constrain(h,400,1022);

      objetivoHombro = h;

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
    }
  }

  // ===========================================
  // CONTROL HOMBRO
  // ===========================================
  int posicion = analogRead(POT_PIN);

  if (posicion < objetivoHombro - 10) {

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);

  }
  else if (posicion > objetivoHombro + 10) {

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);

  }
  else {

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
  }

  // ===========================================
  // DEBUG
  // ===========================================
  /*
  Serial.print("Pot: ");
  Serial.print(posicion);

  Serial.print("  Obj: ");
  Serial.println(objetivoHombro);
  */
}