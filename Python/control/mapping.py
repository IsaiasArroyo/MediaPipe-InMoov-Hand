def map_servo(valor, in_min, in_max, out_min, out_max):

    return int((valor - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)