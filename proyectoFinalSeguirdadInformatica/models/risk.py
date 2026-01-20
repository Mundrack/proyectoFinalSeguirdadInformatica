class Risk:
    def __init__(self, asset, threat, probability, impact):
        self.asset = asset
        self.threat = threat
        self.probability = probability
        self.impact = impact

    def risk_level(self):
        return self.probability * self.impact
