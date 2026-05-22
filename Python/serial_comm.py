import serial
from config import SERIAL_PORT, BAUDRATE

arduino = None

def conectar():

    global arduino

    try:
        arduino = serial.Serial(
            SERIAL_PORT,
             BAUDRATE,
            timeout=0,
            write_timeout=0
        )
        print("Arduino conectado")
    except:
        print("Modo simulacion (sin Arduino)")

def enviar(datos):

    global arduino

    if arduino:

        try:
            arduino.write((datos + "\n").encode())

        except:
            pass