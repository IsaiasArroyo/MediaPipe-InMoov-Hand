import cv2
import mediapipe as mp
import numpy as np
import serial
import time

WRIST_MIN = 50
WRIST_NEUTRO = 90
WRIST_MAX = 130

# conexion arduino
arduino=None
try:
    arduino = serial.Serial('COM8',115200)
    print("Arduino conectado")
except:
    print("Modo simulacion (sin Arduino)")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

# valores suavizados
servo_thumb=0
servo_index=0
servo_middle=0
servo_ring=0
servo_pinky=0
servo_wrist=WRIST_NEUTRO

alpha=0.3

# control de frecuencia
last_send=0

# calibracion
open_hand=[160,170,170,170,170]
closed_hand=[90,40,40,40,40]


def limitar_velocidad(actual, objetivo, paso=4):

    if objetivo > actual + paso:
        return actual + paso

    if objetivo < actual - paso:
        return actual - paso

    return objetivo


def zona_muerta(actual, objetivo, zona=3):

    if abs(objetivo-actual) < zona:
        return actual

    return objetivo


def angulo(a,b,c):

    a=np.array(a)
    b=np.array(b)
    c=np.array(c)

    ba=a-b
    bc=c-b

    cosang=np.dot(ba,bc)/(np.linalg.norm(ba)*np.linalg.norm(bc))
    cosang=np.clip(cosang,-1,1)

    ang=np.degrees(np.arccos(cosang))

    return ang


def map_servo(valor,in_min,in_max,out_min,out_max):

    return int((valor-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

def rotacion_mano_3d(lm):

    wrist = np.array([lm[0].x, lm[0].y, lm[0].z])
    index = np.array([lm[5].x, lm[5].y, lm[5].z])
    pinky = np.array([lm[17].x, lm[17].y, lm[17].z])

    v1 = index - wrist
    v2 = pinky - wrist

    normal = np.cross(v1, v2)

    rot = np.degrees(np.arctan2(normal[1], normal[2]))

    return rot

datos="---"

while True:

    ret,frame=cap.read()

    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    res=hands.process(rgb)

    if res.multi_hand_landmarks:

        hand=res.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)

        lm=hand.landmark

        thumb=angulo([lm[2].x,lm[2].y],[lm[3].x,lm[3].y],[lm[4].x,lm[4].y])
        index=angulo([lm[5].x,lm[5].y],[lm[6].x,lm[6].y],[lm[8].x,lm[8].y])
        middle=angulo([lm[9].x,lm[9].y],[lm[10].x,lm[10].y],[lm[12].x,lm[12].y])
        ring=angulo([lm[13].x,lm[13].y],[lm[14].x,lm[14].y],[lm[16].x,lm[16].y])
        pinky=angulo([lm[17].x,lm[17].y],[lm[18].x,lm[18].y],[lm[20].x,lm[20].y])
        rot = rotacion_mano_3d(lm)

        valores=[thumb,index,middle,ring,pinky]

        # mapeo calibrado
        target_thumb  = map_servo(valores[0],closed_hand[0],open_hand[0],180,0)
        target_index  = map_servo(valores[1],closed_hand[1],open_hand[1],180,0)
        target_middle = map_servo(valores[2],closed_hand[2],open_hand[2],180,0)
        target_ring   = map_servo(valores[3],closed_hand[3],open_hand[3],180,0)
        target_pinky  = map_servo(valores[4],closed_hand[4],open_hand[4],180,0)
        target_wrist = map_servo(rot,-60,60,WRIST_MIN,WRIST_MAX)


        # limitar rango
        target_thumb=max(0,min(180,target_thumb))
        target_index=max(0,min(180,target_index))
        target_middle=max(0,min(180,target_middle))
        target_ring=max(0,min(180,target_ring))
        target_pinky=max(0,min(180,target_pinky))
        target_wrist = max(WRIST_MIN,min(WRIST_MAX,target_wrist))
        

        # redondeo para reducir jitter
        target_thumb=round(target_thumb/2)*2
        target_index=round(target_index/2)*2
        target_middle=round(target_middle/2)*2
        target_ring=round(target_ring/2)*2
        target_pinky=round(target_pinky/2)*2

        # zona muerta
        target_thumb=zona_muerta(servo_thumb,target_thumb)
        target_index=zona_muerta(servo_index,target_index)
        target_middle=zona_muerta(servo_middle,target_middle)
        target_ring=zona_muerta(servo_ring,target_ring)
        target_pinky=zona_muerta(servo_pinky,target_pinky)

        # filtro exponencial
        servo_thumb  = int(servo_thumb  + alpha*(target_thumb  - servo_thumb))
        servo_index  = int(servo_index  + alpha*(target_index  - servo_index))
        servo_middle = int(servo_middle + alpha*(target_middle - servo_middle))
        servo_ring   = int(servo_ring   + alpha*(target_ring   - servo_ring))
        servo_pinky  = int(servo_pinky  + alpha*(target_pinky  - servo_pinky))
        servo_wrist = int(servo_wrist + alpha*(target_wrist-servo_wrist))

        # limitar velocidad
        servo_thumb=limitar_velocidad(servo_thumb,target_thumb)
        servo_index=limitar_velocidad(servo_index,target_index)
        servo_middle=limitar_velocidad(servo_middle,target_middle)
        servo_ring=limitar_velocidad(servo_ring,target_ring)
        servo_pinky=limitar_velocidad(servo_pinky,target_pinky)
        servo_wrist = limitar_velocidad(servo_wrist,target_wrist)

        # enviar datos cada 30 ms
        if time.time()-last_send > 0.03:

            datos=f"{servo_thumb},{servo_index},{servo_middle},{servo_ring},{servo_pinky},{servo_wrist}"

            print(datos)

            if arduino:
                arduino.write((datos+"\n").encode())

            last_send=time.time()

        cv2.putText(frame,datos,(20,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.putText(frame,"O = calibrar abierta",(20,400),
    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2)

    cv2.putText(frame,"C = calibrar cerrada",(20,430),
    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2)

    cv2.imshow("InMoov Hand Control",frame)

    key=cv2.waitKey(1)&0xFF

    if key==ord('o') and res.multi_hand_landmarks:
        open_hand=[thumb,index,middle,ring,pinky]
        print("Calibracion mano abierta guardada")

    if key==ord('c') and res.multi_hand_landmarks:
        closed_hand=[thumb,index,middle,ring,pinky]
        print("Calibracion mano cerrada guardada")

    if key==27:
        break

cap.release()
cv2.destroyAllWindows()