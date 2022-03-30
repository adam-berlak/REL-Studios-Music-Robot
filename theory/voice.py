class Voice:

    def __init__(self, p_parts = []):
        self.parts = p_parts

    def add(self, p_part):
        p_part.set_parent_voice_BL(len(self.get_parts()), self)
        self.get_parts().add(p_part)

    def set_parts(self, p_parts): 
        self.parts = p_parts

    def get_parts(self): 
        return self.parts