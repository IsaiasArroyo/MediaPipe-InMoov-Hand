int IN1 = 8;
int IN2 = 9;

int potPin = A0;

int objetivo = 600; // ajusta según tu montaje

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int posicion = analogRead(potPin);
  Serial.println(posicion);

  if (posicion < objetivo - 10) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
  }
  else if (posicion > objetivo + 10) {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
  }
  else {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW); // detener
  }
}