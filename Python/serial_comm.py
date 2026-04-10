import serial
from config import SERIAL_PORT, BAUDRATE

arduino = None

def conectar():

    global arduino

    try:
        arduino = serial.Serial(SERIAL_PORT, BAUDRATE)
        print("Arduino conectado")
    except:
        print("Modo simulacion (sin Arduino)")

def enviar(datos):

    if arduino:
        arduino.write((datos + "\n").encode())