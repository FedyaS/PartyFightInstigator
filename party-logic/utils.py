import random
import string

def floor_ceiling_round(value):
    rounded = int(round(value))
    not_below = max(0, rounded)
    not_above = min(not_below, 100)
    
    return not_above

def create_id():
    return ''.join(random.choices(string.ascii_uppercase, k=6))

def apply_random_modifier(value, randradius):
    multiplier = random.uniform(-1, 1)
    deviation = multiplier * randradius
    value += deviation
    value = floor_ceiling_round(value)
    return value