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
├── python
│   ├── main.py
│   ├── config.py
│   ├── serial_comm.py
│   ├── control
│   ├── vision
│   └── utils
│
├── arduino
│   └── inmoov
│       │
│       ├── InMoov_Hand_Controller
│       │   └── InMoov_Hand_Controller.ino
│       │
│       ├── CalibracionServos
│       │   └── CalibracionServos.ino
│       │
│       └── PCA9685
│           └── PCA9685.ino
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Requisitos

Este proyecto fue probado con:

```
Python 3.10.11
```

Se recomienda usar **un entorno virtual** para evitar conflictos de dependencias.

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

---

# Crear entorno virtual

Crear el entorno virtual con:

```
python -m venv venv
```

Esto creará una carpeta llamada **venv** con el entorno de Python.

---

# Activar entorno virtual

En **Windows**:

```
venv\Scripts\activate
```

Si se activó correctamente verás algo como:

```
(venv) C:\MediaPipe-InMoov-Hand>
```

---

# Instalar dependencias

Con el entorno virtual activo ejecutar:

```
pip install -r requirements.txt
```

---

# Ejecución

Entrar a la carpeta de Python:

```
cd python
```

Ejecutar el programa principal:

```
python main.py
```

---

# Configuración

Antes de ejecutar el programa, asegúrate de configurar correctamente el puerto serial en el archivo:

```
python/config.py
```

Ejemplo:

```
SERIAL_PORT = "COM8"
```

---

# Firmware Arduino

El firmware utilizado para controlar los servos se encuentra en:

```
arduino/inmoov/InMoov_Hand_Controller
```

Abrir el archivo en **Arduino IDE**:

```
InMoov_Hand_Controller.ino
```

y subirlo al Arduino antes de ejecutar el programa en Python.

---

