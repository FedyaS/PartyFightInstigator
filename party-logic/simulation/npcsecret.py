from simulation.utils import apply_random_modifier, create_id, load_json

class NPCSecret:
    def __init__(self, id=None, text='', hash_text='', conceal_score=500, randomize_stats=0, subject_ids=None, from_json=''):
        data = load_json(from_json, 'npcsecret')
        if data:
            self.id = data['id']
            self.text = data['text']
            self.hash_text = data['hash_text']
            self.conceal_score = data['conceal_score']
            self.subject_ids = data['subject_ids']

        else:
            if subject_ids is None:
                subject_ids = []

            self.id = id or create_id()
            self.text = text
            self.hash_text = hash_text
            self.conceal_score = apply_random_modifier(conceal_score, randomize_stats)
            self.subject_ids = subject_ids

    def pretty_print(self, indent=4):
        attrs = {
            "ID": self.id,
            "Text": self.text,
            "Concealment": self.conceal_score,
            "Subjects IDs": self.subject_ids if self.subject_ids else "None"
        }
        print("NPCSecret:")
        for key, value in attrs.items():
            print(f"{' ' * indent}{key}: {value}")