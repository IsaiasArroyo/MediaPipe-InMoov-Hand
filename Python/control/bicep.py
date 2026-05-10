from utils.math_utils import angulo
from control.mapping import map_servo
from control.filters import limitar_velocidad
from config import BICEP_MIN, BICEP_MAX


def calcular_bicep(lm, lado="derecho"):

    if lado == "derecho":
        shoulder = [lm[12].x, lm[12].y, lm[12].z]
        elbow    = [lm[14].x, lm[14].y, lm[14].z]
        wrist    = [lm[16].x, lm[16].y, lm[16].z]
    else:
        shoulder = [lm[11].x, lm[11].y, lm[11].z]
        elbow    = [lm[13].x, lm[13].y, lm[13].z]
        wrist    = [lm[15].x, lm[15].y, lm[15].z]

    ang = angulo(shoulder, elbow, wrist)

    return ang


def controlar_bicep(angulo_bicep, servo_actual):

    # Limitar angulo real del brazo
    angulo_bicep = max(30, min(180, angulo_bicep))

    # Extendido = 0
    # Flexionado = 75
    target = map_servo(angulo_bicep, 180, 30, BICEP_MIN, BICEP_MAX)
    
    # Limitar servo
    target = max(BICEP_MIN, min(BICEP_MAX, target))

    # Suavizar movimiento
    servo = limitar_velocidad(servo_actual, target)

    return servo