#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca9685 = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 500

// =====================================================
// MODO SIMULACION
// true  = movimientos automaticos
// false = usar MediaPipe por Serial
// =====================================================
bool simulacion = false;

// =====================================================
// CANALES PCA9685
// =====================================================
#define thumb   0
#define index   1
#define majeure 2
#define ring    3
#define pinky   4
#define wrist   5
#define bicep   6

// =====================================================
// MOTOR HOMBRO
// =====================================================
#define IN1 8
#define IN2 9
#define POT_HOMBRO A0

// =====================================================
// CALIBRACION
// =====================================================
#define POT_MIN 125
#define POT_MAX 1023

#define TOLERANCIA 10

String data = "";

// =====================================================
// ANGULO -> PWM
// =====================================================
int angulo(int ang){

  return map(ang, 0, 180, SERVOMIN, SERVOMAX);
}

// =====================================================
// ANGULO -> POT
// =====================================================
int anguloPot(int ang){

  return map(ang, 0, 180, POT_MIN, POT_MAX);
}

// =====================================================
// SETUP
// =====================================================
void setup() {

  Serial.begin(115200);

  // Timeout serial
  Serial.setTimeout(10);

  // PCA9685
  pca9685.begin();
  pca9685.setPWMFreq(50);

  // Posicion inicial segura
  pca9685.setPWM(bicep, 0, angulo(0));

  // Motor hombro
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  Serial.println("Sistema iniciado");
}

// =====================================================
// LOOP
// =====================================================
void loop() {

  // =================================================
  // MODO SIMULACION
  // =================================================
  if(simulacion){

    static int ang = 0;
    static bool subir = true;

    moverServos(
      ang,
      ang,
      ang,
      ang,
      ang,
      ang,
      ang
    );

    moverHombro(90);

    Serial.print("Simulacion: ");
    Serial.println(ang);

    // =============================================
    // BICEP SOLO 0-75
    // =============================================
    if(subir){

      ang += 5;

      if(ang >= 75){

        ang = 75;
        subir = false;
      }
    }
    else{

      ang -= 5;

      if(ang <= 0){

        ang = 0;
        subir = true;
      }
    }

    delay(200);
  }

  // =================================================
  // MODO SERIAL / MEDIAPIPE
  // =================================================
  else{

    if(Serial.available() > 0){

      data = Serial.readStringUntil('\n');

      // quitar espacios y saltos raros
      data.trim();

      int t,i,m,r,p,w,b,h;

      // =========================================
      // LEER 8 VALORES
      // =========================================
      int valores = sscanf(
        data.c_str(),
        "%d,%d,%d,%d,%d,%d,%d,%d",
        &t,&i,&m,&r,&p,&w,&b,&h
      );

      // =========================================
      // DEBUG SERIAL
      // =========================================
      Serial.print("RECIBIDO: ");
      Serial.println(data);

      // =========================================
      // VALIDAR
      // =========================================
      if(valores == 8){

        moverServos(t,i,m,r,p,w,b);

        moverHombro(h);

        Serial.println("DATOS OK");
      }
      else{

        Serial.print("ERROR SERIAL -> ");
        Serial.println(valores);
      }
    }
  }
}

// =====================================================
// CONTROL SERVOS PCA9685
// =====================================================
void moverServos(int t,int i,int m,int r,int p,int w,int b){

  // =========================================
  // SERVOS NORMALES
  // =========================================
  pca9685.setPWM(thumb,   0, angulo(t));
  pca9685.setPWM(index,   0, angulo(i));
  pca9685.setPWM(majeure, 0, angulo(m));
  pca9685.setPWM(ring,    0, angulo(r));
  pca9685.setPWM(pinky,   0, angulo(p));
  pca9685.setPWM(wrist,   0, angulo(w));

  // =========================================
  // BICEP SOLO 0-75 REALES
  // =========================================
  b = constrain(b, 0, 75);

  pca9685.setPWM(
    bicep,
    0,
    angulo(b)
  );

  // =========================================
  // DEBUG
  // =========================================
  Serial.print("Bicep Final: ");
  Serial.println(b);
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

  // =========================================
  // MOVER ADELANTE
  // =========================================
  if(posicion < objetivo - TOLERANCIA){

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
  }

  // =========================================
  // MOVER ATRAS
  // =========================================
  else if(posicion > objetivo + TOLERANCIA){

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
  }

  // =========================================
  // DETENER
  // =========================================
  else{

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
  }
}