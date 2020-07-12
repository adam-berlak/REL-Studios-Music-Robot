class Voice:

    def __init__(self, p_parts = []):
        self.parts = p_parts

    def add(self, p_part):
        p_part.setParentVoice(len(self.getParts()), self)
        self.getParts().add(p_part)

    def getParts(self): return self.parts
    def setParts(self, p_parts): self.parts = p_parts