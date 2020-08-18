from TheoryComponents.IPitchedObject import *
from TheoryComponents.Interval import *
from TheoryComponents.Tone import *

class Key(IPitchedObject):

    def __init__(self, p_tone, p_octave):
        self.octave = p_octave
        self.tone = p_tone

    def __eq__(self, p_other): return (type(self) == type(p_other)) and (self.getTone() == p_other.getTone()) and (self.getOctave() == p_other.getOctave())

    ##################
    # Representation #
    ##################

    def __str__(self): return self.getTone().__str__() + str(self.getOctave())
    def __repr__(self): return self.__str__()

    ##############
    # Arithmetic #
    ##############

    def __add__(self, p_other):
        if (isinstance(p_other, Interval)):
            if (p_other < Interval(0, 0)): return self - abs(p_other)
            if (p_other >= Interval(12, 8)): return Key(self.getTone(), self.getOctave() + 1).__add__(p_other - Interval(12, 8))

            distance_till_next_octave = Key.start_point.__sub__(self.getTone()).getSemitones()
            if (self.getTone() == Key.start_point): distance_till_next_octave = 12

            octave = self.getOctave()
            if (p_other.getSemitones() >= distance_till_next_octave): octave += 1
            return Key(self.getTone().__add__(p_other), octave)

        else: return self.getTone().__add__(p_other)

    def __sub__(self, p_other):
        if (isinstance(p_other, Interval)):
            if (p_other < Interval(0, 0)): return self + abs(p_other)
            if (p_other >= Interval(12, 8)): return Key(self.getTone(), self.getOctave() - 1).__sub__(p_other - Interval(12, 8))

            distance_till_next_octave = self.getTone().__sub__(Key.start_point).getSemitones()
            
            octave = self.getOctave()
            if (p_other.getSemitones() > distance_till_next_octave): octave -= 1
            return Key(self.getTone().__sub__(p_other), octave)

        if (isinstance(p_other, Key)):
            if (p_other.getOctave() < self.getOctave()): return Interval(12, 8) + ((self - Interval(12, 8)) - p_other)
            if (p_other.getOctave() > self.getOctave()): return -(p_other - self)
            
            if ((self - (self.getTone().__sub__(p_other.getTone()))).getOctave() != self.getOctave()): return -(p_other.getTone().__sub__(self.getTone()))
            return (self.getTone().__sub__(p_other.getTone()))

    ##################
    # Static Methods #
    ##################

    @staticmethod
    def decimalToKey(p_decimal_number):
        temp_key_semitones = p_decimal_number - 21
        return Key(Tone("A", 0), 0) + min(Interval.getPossibleIntervals(temp_key_semitones), key=lambda x: x.getAccidentalAsSemitones())

    #################
    # Sugar Methods #
    #################
    
    def getRelatives(self):
        return [Key(tone, self.getOctave()) for tone in self.getTone().getRelatives()]

    def simplify(self): return Key(self.getTone().simplify(), self.getOctave())
    def toDecimal(self): return (self - Key(Tone("A", 0), 0)).getSemitones() + 21
    def build(self, p_object, p_intervals, p_args): return p_object(self, p_intervals, **p_args)

    #######################
    # Getters and Setters #
    #######################

    def getOctave(self): return self.octave
    def getTone(self): return self.tone