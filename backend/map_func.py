import math

def isclose(curr_position, target_position):
    R = 6378.137 #Radius of earth in KM
    dLat = curr_position[0] * math.pi / 180 - target_position[0] * math.pi / 180
    dLon = curr_position[1] * math.pi / 180 - target_position[1] * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(target_position[0] * math.pi / 180) * math.cos(curr_position[0] * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    distance = d * 1000
    return distance <= 50

def string_to_tup(string_tup) -> tuple:
    string_tup = string_tup[1:-1]

    return tuple(map(int, string_tup.split(',')))

