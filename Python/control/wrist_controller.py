from control.mapping import map_servo
from control.filters import suavizar
from config import WRIST_MIN, WRIST_MAX

def calcular_muñeca(rot, servo_actual):

    target = map_servo(rot,-60,60,WRIST_MIN,WRIST_MAX)

    target=max(WRIST_MIN,min(WRIST_MAX,target))

    servo = suavizar(
        servo_actual,
        target,
        alpha=0.4
    )

    return servo