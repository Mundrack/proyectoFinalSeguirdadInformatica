class Asset:
    def __init__(self, name, category, confidentiality, integrity, availability):
        self.name = name
        self.category = category
        self.confidentiality = confidentiality
        self.integrity = integrity
        self.availability = availability

    def criticality(self):
        return self.confidentiality + self.integrity + self.availability
