import numpy as np

from control.mapping import map_servo
from control.filters import suavizar, zona_muerta

from config import POT_MIN, POT_MAX, ROT_EXT, ROT_INT


# =====================================================
# ROTACION INTERNA / EXTERNA HOMBRO
# =====================================================
def calcular_hombro(lm, lado="derecho"):

    if lado == "derecho":

        shoulder = np.array([
            lm[12].x,
            lm[12].y,
            lm[12].z
        ])

        elbow = np.array([
            lm[14].x,
            lm[14].y,
            lm[14].z
        ])

    else:

        shoulder = np.array([
            lm[11].x,
            lm[11].y,
            lm[11].z
        ])

        elbow = np.array([
            lm[13].x,
            lm[13].y,
            lm[13].z
        ])

    brazo = elbow - shoulder

    rot = np.degrees(
        np.arctan2(
            brazo[2],
            brazo[0]
        )
    )

    # eliminar salto ±180°
    if rot > 90:
        rot -= 180

    if rot < -90:
        rot += 180

    print(f"ROT RAW = {rot:.1f}")
    return rot


# =====================================================
# CONVERTIR ROTACION -> POT
# =====================================================
def controlar_hombro(rot, objetivo_actual):

    target = map_servo(
        rot,
        ROT_EXT,
        ROT_INT,
        POT_MIN,
        POT_MAX
    )

    target = max(
        POT_MIN,
        min(POT_MAX, target)
    )

    target = zona_muerta(
        objetivo_actual,
        target
    )

    objetivo = suavizar(
        objetivo_actual,
        target
    )

    return int(objetivo)