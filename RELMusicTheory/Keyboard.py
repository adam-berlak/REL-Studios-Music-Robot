from Scale import *

class Tone:
    def __init__(self, p_tone, p_octaves, p_aliases):
        self.tone = p_tone
        self.octaves = p_octaves
        self.aliases = p_aliases
        self.scale_tone = False

    ##################
    # Representation #
    ##################

    def __str__(self):
        return self.getTone() + str(self.getOctaves)

    def __repr__(self):
         return str(self)

    ##############
    # Arithmetic #
    ##############

    def __add__(self, p_other):

        if (isinstance(p_other, Interval)):

            if (p_other == P1):
                return self
            
            return self.next() + (p_other - m2)

        if (isinstance(p_other, int)):

            if (p_other == 0):
                return self
            elif (self.next().isScaleTone()):
                return self.next() + (p_other - 1)
            else:
                return self.next() + p_other

    def __sub__(self, p_other):

        if (isinstance(p_other, Interval)):

            if (p_other == P1):
                return self
            
            return self.previous() - (p_other - m2)

        if (isinstance(p_other, int)):

            if (p_other == 0):
                return self
            elif (self.next().isScaleTone()):
                return self.previous() - (p_other - 1)
            else:
                return self.previous() - p_other

    ###############
    # Equivalence #
    ###############
    
    def __eq__(self, p_other):

        if (isinstance(p_other, str)):
            return p_other in self.getAliases()

        if (isinstance(p_other, Tone)):
            return (self.getTone() == p_other.getTone() and self.getOctaves() == p_other.getOctaves())

    def __ne__(self, p_other):
        return not (self == p_other)

    ##############################################
    # Methods concerned with operations on Tones #
    ##############################################

    def build(self, p_object_type):
        self.getParentKeyboard().apply(self, p_object_type)

    ####################
    # Courtesy Methods #
    ####################

    def getPosition(self):
        for i in range(len(self.getParentKeyboard().getTonesFlattened())):
            if (self.getParentKeyboard()[i] == self):
                return i

    def next(self):

        if (self.getPosition() == len(self.getParentKeyboard().getTones())):
            return self.getParentKeyboard().getTonesFlattened()[0]

        return self.getParentKeyboard()[self.getPosition() + 1]

    def previous(self):

        if (self.getPosition() == 0):
            return self.getParentKeyboard().getTonesFlattened()[-1]

        return self.getParentKeyboard()[self.getPosition() - 1]

    #######################
    # Getters and Setters #
    #######################

    def getParentKeyboard(self):
        return self.keyboard
    def getDegree(self):
        return self.degree
    def getTone(self):
        return self.tone
    def getOctaves(self):
        return self.octaves
    def getAliases(self):
        return self.aliases

    def setParentKeyboard(self, p_keyboard):
        self.keyboard = p_keyboard
    def setDegree(self, p_degree):
        self.degree = p_degree
    def setTone(self, p_tone):
        self.tone = p_tone
    def setOctaves(self, p_octaves):
        self.octaves = p_octaves
    def setAliases(self, p_aliases):
        self.aliases = p_aliases

class Keyboard:

    def __init__(self, p_tone_list, p_keyboard_size = 7):
        self.tones = []

        for i in range(p_keyboard_size + 1):
            list = []

            for tone in p_tone_list:
                new_tone = Tone(tone, i)
                new_tone.setParentKeyboard(self)
                list.append(new_tone)

            self.getTones().append(list)

    ##################
    # Representation #
    ##################

    def __str__():
        return str(self.getScaleTones())

    def __repr__():
        return str(self)

    ###########
    # Indices #
    ###########

    def __getitem__(self, p_other):
        return self.getTones()[p_other]
        
    def apply(self, p_principle_tone, p_scale_object):
        self.setScale(p_scale_object)

        for tone in self.getTonesFlattened():
            if tone in p_scale_object():
                tone.setScaleTone(True)
                tone.setDegree(degree)

    def getScaleTones(self):
        result = []
        for tone in self.getTonesFlattened():
            if (tone.isScaleTone()):
                result.append(tone)

        return result

    def getTonesFlattened(self):
        return [item for sublist in self.tones for item in sublist]

    #######################
    # Getters and Setters #
    #######################

    def getTones(self):
        return self.tones

    def getScale(self):
        return self.scale

    def setTones(self, p_tones):
        self.tones = p_tones

    def setScale(self, p_scale_object):
        self.scale = p_scale_object