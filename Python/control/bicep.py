import math

from control.mapping import map_servo
from control.filters import limitar_velocidad
from config import BICEP_MIN, BICEP_MAX


# =========================================================
# CALCULO BICEP
# Detecta flexion real del codo tipo "conejo"
# =========================================================
def calcular_bicep(lm, lado="derecho"):

    # ==========================================
    # LANDMARKS
    # ==========================================
    if lado == "derecho":

        shoulder = lm[12]
        elbow    = lm[14]
        wrist    = lm[16]

    else:

        shoulder = lm[11]
        elbow    = lm[13]
        wrist    = lm[15]

    # ==========================================
    # DISTANCIA HOMBRO -> MUÑECA
    # ==========================================
    dist_sw = math.sqrt(
        (shoulder.x - wrist.x)**2 +
        (shoulder.y - wrist.y)**2
    )

    # ==========================================
    # LONGITUD TOTAL DEL BRAZO
    # hombro -> codo + codo -> muñeca
    # ==========================================
    dist_se = math.sqrt(
        (shoulder.x - elbow.x)**2 +
        (shoulder.y - elbow.y)**2
    )

    dist_ew = math.sqrt(
        (elbow.x - wrist.x)**2 +
        (elbow.y - wrist.y)**2
    )

    largo_brazo = dist_se + dist_ew

    # ==========================================
    # EVITAR DIVISION POR CERO
    # ==========================================
    if largo_brazo == 0:
        return 0

    # ==========================================
    # RELACION NORMALIZADA
    # extendido ≈ 1.0
    # flexionado ≈ 0.3
    # ==========================================
    relacion = dist_sw / largo_brazo

    # limitar rango
    relacion = max(0.3, min(1.0, relacion))

    # ==========================================
    # CONVERTIR A 0-180
    # ==========================================
    angulo_bicep = int(
        (relacion - 0.3) / (1.0 - 0.3) * 180
    )

    # invertir
    # extendido -> 0
    # flexionado -> 180
    angulo_bicep = 180 - angulo_bicep

    return angulo_bicep


# =========================================================
# CONTROL SERVO BICEP
# =========================================================
def controlar_bicep(angulo_bicep, servo_actual):

    # ==========================================
    # LIMITAR ANGULOS
    # ==========================================
    angulo_bicep = max(0, min(180, angulo_bicep))

    # ==========================================
    # MAPEAR A SERVO
    # ==========================================
    target = map_servo(
         angulo_bicep,
        0,
        180,
         0,
        75
    )

    # ==========================================
    # LIMITAR SERVO
    # ==========================================
    target = max(BICEP_MIN, min(BICEP_MAX, target))

    # ==========================================
    # SUAVIZAR MOVIMIENTO
    # ==========================================
    servo = limitar_velocidad(
        servo_actual,
        target
    )

    return servo