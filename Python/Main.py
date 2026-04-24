import cv2
import mediapipe as mp
import time

from control.bicep import calcular_bicep, controlar_bicep
from config import *
from serial_comm import conectar, enviar

from utils.math_utils import angulo
from vision.hand_rotation import rotacion_mano_3d

from control.fingers_controller import calcular_dedos
from control.wrist_controller import calcular_muñeca


conectar()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose()
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

# ===== SERVOS =====
servo_thumb = 0
servo_index = 0
servo_middle = 0
servo_ring = 0
servo_pinky = 0
servo_wrist = WRIST_NEUTRO
servo_bicep = 90

angulo_bicep = 0

last_send = 0

while True:

    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ===== PROCESAMIENTO =====
    res_hands = hands.process(rgb)
    res_pose = pose.process(rgb)

    # ===== BICEP (POSE) =====
    if res_pose.pose_landmarks:

        lm_pose = res_pose.pose_landmarks.landmark

        angulo_bicep = calcular_bicep(lm_pose, "derecho")
        servo_bicep = controlar_bicep(angulo_bicep, servo_bicep)

    # ===== MANO =====
    if res_hands.multi_hand_landmarks:

        hand = res_hands.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        lm = hand.landmark

        thumb = angulo([lm[2].x, lm[2].y], [lm[3].x, lm[3].y], [lm[4].x, lm[4].y])
        index = angulo([lm[5].x, lm[5].y], [lm[6].x, lm[6].y], [lm[8].x, lm[8].y])
        middle = angulo([lm[9].x, lm[9].y], [lm[10].x, lm[10].y], [lm[12].x, lm[12].y])
        ring = angulo([lm[13].x, lm[13].y], [lm[14].x, lm[14].y], [lm[16].x, lm[16].y])
        pinky = angulo([lm[17].x, lm[17].y], [lm[18].x, lm[18].y], [lm[20].x, lm[20].y])

        rot = rotacion_mano_3d(lm)
        rot = rot - OFFSET_ROT

        servo_thumb, servo_index, servo_middle, servo_ring, servo_pinky = calcular_dedos(
            [thumb, index, middle, ring, pinky],
            [servo_thumb, servo_index, servo_middle, servo_ring, servo_pinky]
        )

        servo_wrist = calcular_muñeca(rot, servo_wrist)

    # ===== ENVÍO =====
    if time.time() - last_send > 0.03:

        datos = f"{servo_thumb},{servo_index},{servo_middle},{servo_ring},{servo_pinky},{servo_wrist},{servo_bicep}"

        print(datos)
        enviar(datos)

        last_send = time.time()

    # ===== VISUAL =====
    cv2.putText(frame, datos, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Bicep: {int(angulo_bicep)}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("InMoov Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()