from Tone import *
from Interval import *

class Key(Tone):

    def __init__(self, p_tone, p_octave):
        self.octave = p_octave
        super().__init__(p_tone.getToneName(), p_tone.getAccidental())

    def __str__(self): return super().__str__() + str(self.getOctave())
    def __repr__(self): return self.__str__()

    def __add__(self, p_other):

        if (isinstance(p_other, Interval)):
            if (p_other < Interval(0, 0)): return self - abs(p_other)
            if (p_other >= Interval(12, 8)): return Key(super(), self.getOctave() + 1).__add__(p_other - Interval(12, 8))

            distance_till_next_octave = Key.start_point.__sub__(self).getSemitones()
            if (super() == Key.start_point): distance_till_next_octave = 12

            octave = self.getOctave()
            if (p_other.getSemitones() >= distance_till_next_octave): octave += 1
            return Key(super().__add__(p_other), octave)

        else: return super().__add__(p_other)

    def __sub__(self, p_other):

        if (isinstance(p_other, Interval)):
            if (p_other < Interval(0, 0)): return self + abs(p_other)
            if (p_other >= Interval(12, 8)): return Key(super(), self.getOctave() - 1).__sub__(p_other - Interval(12, 8))

            distance_till_next_octave = super().__sub__(Key.start_point).getSemitones()
            
            octave = self.getOctave()
            if (p_other.getSemitones() > distance_till_next_octave): octave -= 1
            return Key(super().__sub__(p_other), octave)

        if (isinstance(p_other, Key)):
            if (p_other.getOctave() < self.getOctave()): return Interval(12, 8) + ((self - Interval(12, 8)) - p_other)
            if (p_other.getOctave() > self.getOctave()): return -(p_other - self)
            
            if ((self - (super().__sub__(super(Key, p_other)))).getOctave() != self.getOctave()): return -(super(Key, p_other).__sub__(super()))
            return (super().__sub(super(Key, p_other)))

        else: return super().__sub__(p_other)

    def simplify(self): return Key(super().simplify(), self.getOctave())

    def getOctave(self): return self.octave
    def setOctave(self, p_octave): self.octave = octave