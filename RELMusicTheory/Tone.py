from Interval import *

class Tone:

    tone_names = []
    accidentals = []
    
    def __init__(self, p_tone_name, p_accidental = 0):
        self.tone_name = p_tone_name
        self.accidental = p_accidental

    def __eq__logic(self, p_other): return (self.getToneName() == p_other.getToneName()) and (self.getAccidental() == p_other.getAccidental())

    def __str__logic(self):

        if (self.getAccidental() < 0): return self.getToneName() + (Tone.accidentals[-1] * abs(self.getAccidental()))
        elif (self.getAccidental() > 0): return self.getToneName() + (Tone.accidentals[1] * abs(self.getAccidental()))
        else: return self.getToneName() + Tone.accidentals[0]

    def __repr__logic(self): return str(self)

    def __add__logic(self, p_other):
        
        if (isinstance(p_other, Interval)):

            if (p_other < Interval(0, 1)): return self - abs(p_other)

            index = Tone.tone_names.index(self.getToneName()) 

            numeral_count = 0
            semitones_count = (-1 * self.getAccidental())

            while(numeral_count != p_other.getNumeral()):     
                if ((Tone.tone_names * 20)[index] != None): numeral_count = numeral_count + 1

                semitones_count = semitones_count + 1
                index = index + 1

            new_tone_name = (Tone.tone_names * 20)[index - 1]
            new_accidental = p_other.getSemitones() - (semitones_count - 1)

            return Tone(new_tone_name, new_accidental)

    def __sub__logic(self, p_other):

        if (isinstance(p_other, Interval)):

            if (p_other < Interval(0, 1)): return self + abs(p_other)

            index = Tone.tone_names.index(self.getToneName()) + 12

            numeral_count = 0
            semitones_count = (-1 * self.getAccidental())

            while(numeral_count != p_other.getNumeral()):          
                if ((Tone.tone_names * 20)[index] != None): numeral_count = numeral_count + 1

                semitones_count = semitones_count + 1
                index = index - 1

            new_tone_name = (Tone.tone_names * 20)[index + 1]
            new_accidental = (p_other.getSemitones() - (semitones_count - 1)) * -1

            return Tone(new_tone_name, new_accidental)

        if (isinstance(p_other, Tone)):

            if (self.getToneName() == p_other.getToneName() and self.getAccidental() == p_other.getAccidental()): return Interval(0, 1)

            index = Tone.tone_names.index(p_other.getToneName()) + 1
            numeral_count = 1
            semitones_count = 0

            while((Tone.tone_names * 2)[index] != self.getToneName()):
                if ((Tone.tone_names * 2)[index] != None): numeral_count = numeral_count + 1
                semitones_count = semitones_count + 1
                index = index + 1
                
            return Interval((semitones_count + 1) - p_other.getAccidental() + self.getAccidental(), numeral_count + 1)

    def __simplify(self):
        index = Tone.tone_names.index(self.getToneName()) + 12
        
        if ((Tone.tone_names * 20)[index + self.getAccidental()] == None):
            if (self.getAccidental() > 0): return [self.getMinimalAccidental(), self.flipAccidental().getMinimalAccidental()]
            else: return [self.flipAccidental().getMinimalAccidental(), self.getMinimalAccidental()]
        else:
            return Tone((Tone.tone_names * 20)[index + self.getAccidental()])

    def __getMinimalAccidental(self):
        index = Tone.tone_names.index(self.getToneName()) + 12 + self.getAccidental()
        semitones_count = 0

        while((Tone.tone_names * 20)[index] == None):
            index = index + int((self.getAccidental() / abs(self.getAccidental())) * -1)
            semitones_count = semitones_count + int(self.getAccidental() / abs(self.getAccidental()))

        return Tone((Tone.tone_names * 20)[index], semitones_count)

    def __flipAccidental(self): return Tone(self.getToneName(), (12 - abs(self.getAccidental())) * (int(self.getAccidental()/abs(self.getAccidental())) * -1))

    def __build(self, p_object, *args): return p_object(self, *args)

    ###################
    # Wrapper Methods #
    ###################

    def __eq__(self, p_other): return self.__eq__logic(p_other)

    def __repr__(self): return self.__repr__logic()
    def __str__(self): return self.__str__logic()

    def __add__(self, p_other): return self.__add__logic(p_other)
    def __sub__(self, p_other): return self.__sub__logic(p_other)
    
    def simplify(self): return self.__simplify()
    def getMinimalAccidental(self): return self.__getMinimalAccidental()
    def flipAccidental(self): return self.__flipAccidental()
    def build(self, p_object, *args): return self.__build(p_object, *args)

    #######################
    # Getters and Setters #
    #######################

    def getToneName(self): return self.tone_name
    def getAccidental(self): return self.accidental

    def setToneName(p_tone_name): self.tone_name = p_tone_name
    def setAccidental(p_accidental): self.accidental = p_accidental
