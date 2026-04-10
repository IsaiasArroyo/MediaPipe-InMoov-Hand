from control.mapping import map_servo
from control.filters import zona_muerta, limitar_velocidad
from config import open_hand, closed_hand

def calcular_dedos(valores, servos):

    thumb,index,middle,ring,pinky = valores

    servo_thumb,servo_index,servo_middle,servo_ring,servo_pinky = servos

    target_thumb  = map_servo(thumb,closed_hand[0],open_hand[0],180,0)
    target_index  = map_servo(index,closed_hand[1],open_hand[1],180,0)
    target_middle = map_servo(middle,closed_hand[2],open_hand[2],180,0)
    target_ring   = map_servo(ring,closed_hand[3],open_hand[3],180,0)
    target_pinky  = map_servo(pinky,closed_hand[4],open_hand[4],180,0)

    targets=[target_thumb,target_index,target_middle,target_ring,target_pinky]
    servos=list(servos)

    for i in range(5):

        targets[i]=max(0,min(180,targets[i]))

        targets[i]=zona_muerta(servos[i],targets[i])

        servos[i]=limitar_velocidad(servos[i],targets[i])

    return servos