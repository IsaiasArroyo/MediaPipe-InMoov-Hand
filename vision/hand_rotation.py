import numpy as np

def rotacion_mano_3d(lm):

    wrist = np.array([lm[0].x, lm[0].y, lm[0].z])
    index = np.array([lm[5].x, lm[5].y, lm[5].z])
    pinky = np.array([lm[17].x, lm[17].y, lm[17].z])

    v1 = index - wrist
    v2 = pinky - wrist

    normal = np.cross(v1, v2)

    rot = np.degrees(np.arctan2(normal[1], normal[2]))

    return rot