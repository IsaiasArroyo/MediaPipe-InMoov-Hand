# MediaPipe InMoov Hand Control

Sistema de control para una **mano robótica del modelo InMoov** utilizando visión por computadora.

El programa utiliza **MediaPipe** para detectar los movimientos de la mano desde una cámara web y enviar los ángulos de los dedos al **Arduino** mediante comunicación serial.

El Arduino controla los servomotores de la mano utilizando un **controlador PCA9685**.

---

# Funcionamiento del sistema

1. La cámara captura la mano del usuario.
2. MediaPipe detecta los **landmarks de la mano**.
3. Se calculan los **ángulos de cada dedo**.
4. Los valores se convierten a posiciones de **servos**.
5. Python envía los datos al **Arduino por comunicación serial**.
6. Arduino mueve los **servos de la mano InMoov**.

---

# Tecnologías utilizadas

* Python
* MediaPipe
* OpenCV
* Arduino
* PCA9685
* Comunicación Serial

---

# Hardware utilizado

* Arduino
* Controlador de servos **PCA9685**
* Servomotores **MG996R / MG995**
* Cámara web
* Mano robótica **InMoov**

---

# Estructura del proyecto

```
MediaPipe
│
├── main.py
├── config.py
├── serial_comm.py
│
├── vision
│   └── hand_rotation.py
│
├── control
│   ├── fingers_controller.py
│   ├── wrist_controller.py
│   ├── filters.py
│   └── mapping.py
│
└── utils
    └── math_utils.py
```

---

# Instalación

Clonar el repositorio:

```
git clone https://github.com/IsaiasArroyo/MediaPipe-InMoov-Hand.git
```

Entrar a la carpeta del proyecto:

```
cd MediaPipe-InMoov-Hand
```

Instalar dependencias:

```
pip install -r requirements.txt
```

---

# Ejecución

Ejecutar el programa principal:

```
python main.py
```

---

# Configuración

Antes de ejecutar el programa, asegúrate de configurar correctamente el puerto serial en el archivo:

```
config.py
```

Ejemplo:

```
SERIAL_PORT = "COM8"
```

---
