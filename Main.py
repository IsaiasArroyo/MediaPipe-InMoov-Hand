import cv2
import mediapipe as mp
import numpy as np
import serial
import time

WRIST_MIN = 20
WRIST_NEUTRO = 90
WRIST_MAX = 160
OFFSET_ROT = 173

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

servo_thumb=0
servo_index=0
servo_middle=0
servo_ring=0
servo_pinky=0
servo_wrist=WRIST_NEUTRO

last_send=0

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
        rot = rot - OFFSET_ROT

        target_thumb  = map_servo(thumb,closed_hand[0],open_hand[0],180,0)
        target_index  = map_servo(index,closed_hand[1],open_hand[1],180,0)
        target_middle = map_servo(middle,closed_hand[2],open_hand[2],180,0)
        target_ring   = map_servo(ring,closed_hand[3],open_hand[3],180,0)
        target_pinky  = map_servo(pinky,closed_hand[4],open_hand[4],180,0)
        target_wrist  = map_servo(rot,-60,60,WRIST_MIN,WRIST_MAX)

        target_thumb=max(0,min(180,target_thumb))
        target_index=max(0,min(180,target_index))
        target_middle=max(0,min(180,target_middle))
        target_ring=max(0,min(180,target_ring))
        target_pinky=max(0,min(180,target_pinky))
        target_wrist=max(WRIST_MIN,min(WRIST_MAX,target_wrist))

        target_thumb=zona_muerta(servo_thumb,target_thumb)
        target_index=zona_muerta(servo_index,target_index)
        target_middle=zona_muerta(servo_middle,target_middle)
        target_ring=zona_muerta(servo_ring,target_ring)
        target_pinky=zona_muerta(servo_pinky,target_pinky)

        servo_thumb=limitar_velocidad(servo_thumb,target_thumb)
        servo_index=limitar_velocidad(servo_index,target_index)
        servo_middle=limitar_velocidad(servo_middle,target_middle)
        servo_ring=limitar_velocidad(servo_ring,target_ring)
        servo_pinky=limitar_velocidad(servo_pinky,target_pinky)
        servo_wrist=limitar_velocidad(servo_wrist,target_wrist)

        if time.time()-last_send>0.03:

            datos=f"{servo_thumb},{servo_index},{servo_middle},{servo_ring},{servo_pinky},{servo_wrist}"

            print(datos)

            enviar(datos)

            last_send=time.time()

        cv2.putText(frame,datos,(20,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("InMoov Hand Control",frame)

    if cv2.waitKey(1)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()