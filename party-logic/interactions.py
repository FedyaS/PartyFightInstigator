from person import Person
from relationships import RelationshipManager
from utils import floor_ceiling_round

def average_out(v1, v2, strength):
    """
    Make two values closer to each other.
    At strength   1   both values become the average.
    At strength   0.5 both values move halfway to the average.
    At strength   0   values don't move.
    """
    average = (v1 + v2)/2
    adjust1 = (average - v1) * strength
    adjust2 = (average - v2) *  strength
    v1 += adjust1
    v2 += adjust2

    v1 = floor_ceiling_round(v1)
    v2 = floor_ceiling_round(v2)

    return v1, v2    

def compound(v1, v2, strength):
    """
    Compound two values so both grow proportional to one another.
    At strength  1   both values grow by the other.
    At strength  0.5 both values grow by half of the other.
    At strength  0   values don't move. 
    """

    v1_impact = v1 * strength
    v2_impact = v2 * strength

    v1 += v2_impact
    v2 += v1_impact

    v1 = floor_ceiling_round(v1)
    v2 = floor_ceiling_round(v2)

    return v1, v2

def interact(P1: Person, P2: Person, strength=1):
    new_joy_1, new_joy_2 = average_out(P1.ES.joy, P2.ES.joy, strength) # Average out joy
    new_anger_1, new_anger_2 = compound(P1.ES.anger, P2.ES.anger, strength) # Compound anger
    new_anxiety_1, new_anxiety_2 = average_out(P1.ES.anxiety, P2.ES.anxiety, strength) # Average out anxiety
    new_jealousy_1, new_jealousy_2 = compound(P1.ES.jealousy, P2.ES.jealousy, strength) # Compound jealousy
    new_cur_1, new_cur_2 = average_out(P1.ES.curiosity, P2.ES.curiosity, strength) # Average out curiosity

    P1.ES.set_emotional_state(joy=new_joy_1, anger=new_anger_1, anxiety=new_anxiety_1, jealousy=new_jealousy_1, curiosity = new_cur_1)
    P2.ES.set_emotional_state(joy=new_joy_2, anger=new_anger_2, anxiety=new_anxiety_2, jealousy=new_jealousy_2, curiosity = new_cur_2)


def interact_with_relationship(P1: Person, P2: Person, RM: RelationshipManager, strength=1):
    p1_thinks_of_p2 = RM.get_relationship(P1, P2)
    p2_thinks_of_p1 = RM.get_relationship(P2, P1)

    trust_factor = (p1_thinks_of_p2.trust + p2_thinks_of_p1.trust) / 2 / 100

    # Interact Emotional State Simple
    interact(P1, P2, strength=trust_factor*strength)

    # Spread some rumors
    