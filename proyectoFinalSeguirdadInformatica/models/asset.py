class Asset:
    def __init__(self, name, category, confidentiality, integrity, availability, responsible=""):
        self.name = name
        self.category = category
        self.confidentiality = confidentiality
        self.integrity = integrity
        self.availability = availability
        self.responsible = responsible

    def criticality(self):
        return self.confidentiality + self.integrity + self.availability
