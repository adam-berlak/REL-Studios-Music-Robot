from TheoryComponents.IPitchedObject import *
from TheoryComponents.Interval import *

class Tone:
    
    def __init__(self, p_tone_name, p_accidental = 0):
        self.tone_name = p_tone_name
        self.accidental = p_accidental

    def __eq__(self, p_other): 
        return (type(self) == type(p_other)) and (self.getToneName() == p_other.getToneName()) and (self.getAccidental() == p_other.getAccidental())
    
    def __str__(self):
        if (self.getAccidental() < 0): 
            return self.getToneName() + (Tone.accidentals[-1] * abs(self.getAccidental()))
            
        elif (self.getAccidental() > 0): 
            return self.getToneName() + (Tone.accidentals[1] * abs(self.getAccidental()))

        else: return self.getToneName() + Tone.accidentals[0]

    def __repr__(self): 
        return str(self)

    def __add__(self, p_other):
        if (isinstance(p_other, int)):
            if p_other == 0: return self
            index = Tone.tone_names.index(self.getToneName()) + self.getAccidental() + 12
            sign = int(p_other / abs(p_other))
            tone_names = (Tone.tone_names * 3)
            
            if tone_names[index + sign] is None:
                return Tone(self.getToneName(), self.getAccidental() + sign).__add__(p_other - sign)
            
            else: return Tone(tone_names[index + sign], 0).__add__(p_other - sign)

        if (isinstance(p_other, Interval)):
            if p_other.getNumeral() == 0: return self
            if abs(p_other.getNumeral()) == 1: return Tone(self.getToneName(), self.getAccidental() + p_other.getSemitones())
            index = Tone.tone_names.index(self.getToneName()) + 12
            sign = int(p_other.getNumeral() / abs(p_other.getNumeral()))

            numeral_count = 0
            semitones_count = ((sign * -1) * self.getAccidental())

            while(numeral_count != abs(p_other.getNumeral())):     
                if ((Tone.tone_names * 20)[index] != None): numeral_count = numeral_count + 1

                semitones_count = semitones_count + 1
                index += sign

            new_tone_name = (Tone.tone_names * 20)[index - sign]
            new_accidental = (abs(p_other.getSemitones()) - (semitones_count - 1)) * sign
            return Tone(new_tone_name, new_accidental) 
            

    def __sub__(self, p_other):
        if (isinstance(p_other, int)):
            return self.__add__(-p_other)

        if (isinstance(p_other, Interval)):
            return self.__add__(-p_other)

        if (isinstance(p_other, Tone)):
            if (self.getToneName() == p_other.getToneName()): return Interval(p_other.getAccidental() - self.getAccidental() if p_other.getAccidental() > self.getAccidental() else self.getAccidental() - p_other.getAccidental(), 1)

            index = Tone.tone_names.index(p_other.getToneName()) + 1
            numeral_count = 1
            semitones_count = 0

            while((Tone.tone_names * 2)[index] != self.getToneName()):
                if ((Tone.tone_names * 2)[index] != None): numeral_count = numeral_count + 1
                semitones_count = semitones_count + 1
                index = index + 1
                
            return Interval((semitones_count + 1) - p_other.getAccidental() + self.getAccidental(), numeral_count + 1)

    #################
    # Sugar Methods #
    #################

    def getRelatives(self):
        relatives = []

        for i in range(Tone.accidental_limit + 1):
            new_tone = self.removeAccidental()
            while (new_tone - self).getSemitones() < i: new_tone = new_tone.next().removeAccidental()
            new_accidental = ((self - new_tone) if self.getToneName() == new_tone.getToneName() and self.getAccidental() > new_tone.getAccidental() else -(new_tone - self)).getSemitones()
            new_tone = Tone(new_tone.getToneName(), new_accidental)
            if new_tone not in relatives and abs(new_tone.getAccidental()) < Tone.accidental_limit + 1: relatives.append(new_tone)

            new_tone = self.removeAccidental()
            while (self - new_tone).getSemitones() < i: new_tone = new_tone.previous().removeAccidental()
            new_accidental = (-(new_tone - self) if self.getToneName() == new_tone.getToneName() and new_tone.getAccidental() > self.getAccidental() else (self - new_tone)).getSemitones()
            new_tone = Tone(new_tone.getToneName(), new_accidental)
            if new_tone not in relatives and abs(new_tone.getAccidental()) < Tone.accidental_limit + 1: relatives.append(new_tone) 

        return relatives

    def removeAccidental(self): 
        return Tone(self.getToneName(), 0)

    def next(self):
        index = Tone.tone_names.index(self.getToneName()) + 12 + 1
        tone_names = (Tone.tone_names * 3)
        while tone_names[index] is None or tone_names[index] == self.getToneName(): index += 1
        return Tone(tone_names[index], self.getAccidental())

    def previous(self):
        index = Tone.tone_names.index(self.getToneName()) + 12 - 1
        tone_names = (Tone.tone_names * 3)
        while tone_names[index] is None or tone_names[index] == self.getToneName(): index -= 1
        return Tone(tone_names[index], self.getAccidental())

    def simplify(self):
        index = Tone.tone_names.index(self.getToneName()) + 12
        
        if ((Tone.tone_names * 20)[index + self.getAccidental()] == None):
            if (self.getAccidental() > 0): return [self.getMinimalAccidental(), self.flipAccidental().getMinimalAccidental()]
            else: return [self.flipAccidental().getMinimalAccidental(), self.getMinimalAccidental()]
            
        else: return Tone((Tone.tone_names * 20)[index + self.getAccidental()])

    def getMinimalAccidental(self):
        index = Tone.tone_names.index(self.getToneName()) + 12 + self.getAccidental()
        semitones_count = 0

        while((Tone.tone_names * 20)[index] == None):
            index = index + int((self.getAccidental() / abs(self.getAccidental())) * -1)
            semitones_count = semitones_count + int(self.getAccidental() / abs(self.getAccidental()))

        return Tone((Tone.tone_names * 20)[index], semitones_count)

    def flipAccidental(self): 
        return Tone(self.getToneName(), (12 - abs(self.getAccidental())) * (int(self.getAccidental() / abs(self.getAccidental())) * -1))
        
    def build(self, p_object, p_intervals, p_args): 
        return p_object(self, p_intervals, **p_args)

    #######################
    # Getters and Setters #
    #######################

    def getTone(self): return self
    def getToneName(self): return self.tone_name
    def getAccidental(self): return self.accidental