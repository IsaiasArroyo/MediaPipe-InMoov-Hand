# MediaPipe InMoov Hand Control

Sistema de control para una mano robótica del modelo **InMoov** utilizando visión por computadora.

El programa utiliza **MediaPipe** para detectar los movimientos de los dedos desde una cámara web y enviar los ángulos al **Arduino** mediante comunicación serial.  
El Arduino controla los servos de la mano usando un **controlador PCA9685**.

---

# Funcionamiento del sistema

1. La cámara captura la mano del usuario.
2. MediaPipe detecta los **landmarks de la mano**.
3. Se calculan los **ángulos de cada dedo**.
4. Python envía los valores al Arduino por **Serial**.
5. Arduino mueve los **servos de la mano InMoov**.

---

# Tecnologías utilizadas

- Python
- MediaPipe
- OpenCV
- Arduino
- PCA9685
- Comunicación Serial

---

# Hardware utilizado

- Arduino
- Controlador de servos **PCA9685**
- Servomotores (MG996R / MG995)
- Cámara web
- Mano robótica **InMoov**

---

# Instalación

Clonar el repositorio:
git clone https://github.com/IsaiasArroyo/MediaPipe-InMoov-Hand.git

Entrar a la carpeta del proyecto:
cd MediaPipe-InMoov-Hand


Instalar dependencias:
pip install -r requirements.txt

