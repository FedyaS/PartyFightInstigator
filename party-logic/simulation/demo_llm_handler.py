from simulation.llm_handler import get_llm_response
from simulation.person import Person
from simulation.relationships import Relationship

Me = Person(is_npc=False)
Nicholas = Person(from_json='person-Nicholas.json')
us_rel = Relationship(Me, Nicholas, 500, 0)

input_text = 'Hi Nicholas'

def handle(input_text):
    resp = get_llm_response(Nicholas, input_text, us_rel.trust, us_rel.animosity)
    print(resp)
    us_rel.modify_trust(resp.trust_change)
    us_rel.modify_animosity(resp.animosity_change)
    Nicholas.modify_anger(resp.anger_change)

def runme():
    while True:
        txt = input('\nur msg: ')
        if txt == 'q':
            break
        handle(txt)
