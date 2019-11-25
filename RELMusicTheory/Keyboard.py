from Scale import *

class Tone:
    def __init__(self, p_tone, p_octaves):
        self.tone = p_tone
        self.octaves = p_octaves
        self.scale_tone = False

    def __add__(self, p_other):

        if (isinstance(p_other, int)):
            self.getParentKeyboard().getScaleTones()

    def isSameTone(self):
        return (self.getTone() == p_other.getTone())

    def build(self, p_scale_object):
        self.getParentKeyboard().apply(self, p_scale_object)

    def getParentKeyboard(self):
        return self.keyboard
    def getDegree(self):
        return self.degree
    def getTone(self):
        return self.tone
    def getOctaves(self):
        return self.octaves

    def setParentKeyboard(self, p_keyboard):
        self.keyboard = p_keyboard
    def setDegree(self, p_degree):
        self.degree = p_degree
    def setTone(self, p_tone):
        self.tone = p_tone
    def setOctaves(self, p_octaves):
        self.octaves = p_octaves

class Keyboard:
    def __init__(self, p_tone_list, p_keyboard_size = 7):
        self.tones = []

        for i in range(p_keyboard_size + 1):
            list = []

            for tone in p_tone_list:
                new_tone = Tone(tone, i)
                new_tone.setParentKeyboard(self)
                list.append(new_tone)
        
    def apply(self, p_principle_tone, p_scale_object):
        for tone in self.getTonesFlattened():
            for degree in p_scale_object.getDegrees():
                if (tone.isSameTone(degree.getTone())):
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

    def getTones(self):
        return self.tones