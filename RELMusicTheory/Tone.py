from Interval import *

class Tone:

    tone_names = []
    accidentals = []
    
    def __init__(self, p_tone_name, p_accidental = 0):
        self.tone_name = p_tone_name
        self.accidental = p_accidental

    def __eq__(self, p_other):
        return (self.getToneName() == p_other.getToneName()) and (self.getAccidental() == p_other.getAccidental())

    def __str__(self):

        if (self.getAccidental() < 0): return self.getToneName() + (Tone.accidentals[-1] * abs(self.getAccidental()))
        elif (self.getAccidental() > 0): return self.getToneName() + (Tone.accidentals[1] * abs(self.getAccidental()))
        else: return self.getToneName() + Tone.accidentals[0]

    def __repr__(self):
        return str(self)

    def __add__(self, p_other):
        
        if (isinstance(p_other, Interval)):
            index = Tone.tone_names.index(self.getToneName()) 

            numeral_count = 0
            semitones_count = (-1 * self.getAccidental())

            while(numeral_count != p_other.getNumeral()):
                
                if ((Tone.tone_names * 20)[index] != None):
                    numeral_count = numeral_count + 1

                semitones_count = semitones_count + 1
                index = index + 1

            new_tone_name = (Tone.tone_names * 20)[index - 1]
            new_accidental = p_other.getSemitones() - (semitones_count - 1)

            return Tone(new_tone_name, new_accidental)

    def __sub__(self, p_other):

        if (isinstance(p_other, Interval)):
            index = Tone.tone_names.index(self.getToneName()) + 12

            numeral_count = 0
            semitones_count = (-1 * self.getAccidental())

            while(numeral_count != p_other.getNumeral()):
                
                if ((Tone.tone_names * 20)[index] != None):
                    numeral_count = numeral_count + 1

                semitones_count = semitones_count + 1
                index = index - 1

            new_tone_name = (Tone.tone_names * 20)[index + 1]
            new_accidental = (p_other.getSemitones() - (semitones_count - 1)) * -1

            return Tone(new_tone_name, new_accidental)

    def simplify(self):
        index = Tone.tone_names.index(self.getToneName()) + 12
        
        if ((Tone.tone_names * 20)[index + self.getAccidental()] == None):

            index = index + self.getAccidental()
            semitones_count = 0

            while((Tone.tone_names * 20)[index] == None):
                index = index + int((self.getAccidental() / abs(self.getAccidental())) * -1)
                semitones_count = semitones_count + int(self.getAccidental() / abs(self.getAccidental()))

            return Tone((Tone.tone_names * 20)[index], semitones_count)
        else:
            return Tone((Tone.tone_names * 20)[index + self.getAccidental()])

    def getToneName(self):
        return self.tone_name

    def getAccidental(self):
        return self.accidental

    def setToneName(p_tone_name):
        self.tone_name = p_tone_name

    def setAccidental(p_accidental):
        self.accidental = p_accidental
