from simulation.llm_handler import get_llm_response
from simulation.person import Person
from simulation.relationships import Relationship

Me = Person(is_npc=False)
Nicholas = Person(from_json='person-Nicholas.json')
us_rel = Relationship(Me, Nicholas, 500, 0)

input_text = 'Hi Nicholas'

def handle(input_text):
    resp = get_llm_response(Nicholas, input_text, us_rel.trust, us_rel.animosity)

    us_rel.modify_trust(resp.trust_change*10)
    us_rel.modify_animosity(resp.animosity_change*10)
    Nicholas.modify_anger(resp.anger_change*10)

    print(f"    Anger: {resp.anger_change * 10} {'-' if resp.anger_change < 0 else ''}")
    print(f"Animosity: {resp.animosity_change * 10} {'-' if resp.animosity_change < 0 else ''}")
    print(f"    Trust: {resp.trust_change * 10} {'-' if resp.trust_change < 0 else ''}")
    print(resp.npc_response_to_player)
    print(resp.new_rumor_detected)

def runme():
    while True:
        txt = input('\nur msg: ')
        if txt == 'q':
            break
        handle(txt)
