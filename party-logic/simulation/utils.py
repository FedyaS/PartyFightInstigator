import os
import random
import string
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

def floor_ceiling_round(value):
    rounded = int(round(value))
    not_below = max(0, rounded)
    not_above = min(not_below, 1000)
    
    return not_above

def create_id():
    return ''.join(random.choices(string.ascii_uppercase, k=8))

def apply_random_modifier(value, randradius):
    multiplier = random.uniform(-1, 1)
    deviation = multiplier * randradius
    value += deviation
    value = floor_ceiling_round(value)
    return value

def load_json(filename, class_type):
    if not filename:
        return None

    load_path = os.path.join(PROJECT_ROOT, 'json_classes', class_type, filename)
    if os.path.exists(load_path):
        with open(load_path, 'r') as file:
            data = json.load(file)
        return data
    return None