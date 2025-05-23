from simulation.utils import create_id

class Rumor:
    def __init__(self, id=None, text='', plausibility=500, harmfulness=500, subjects=None, originators=None):
        if subjects is None:
            subjects = []
        if originators is None:
            originators = []

        self.id = id or create_id()
        self.text = text
        self.plausibility = plausibility
        self.harmfulness = harmfulness
        self.subjects = subjects
        self.originators = originators

    def pretty_print(self, indent=4):
        attrs = {
            "ID": self.id,
            "Text": self.text,
            "Plausibility": self.plausibility,
            "Harmfulness": self.harmfulness,
            "Subjects": self.subjects if self.subjects else "None",
            "Originators": self.originators if self.originators else "None"
        }
        print("Rumor:")
        for key, value in attrs.items():
            print(f"{' ' * indent}{key}: {value}")