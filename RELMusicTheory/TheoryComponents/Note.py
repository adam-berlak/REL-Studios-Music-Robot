from TheoryComponents.IPitchedObject import *
from TheoryComponents.Interval import *
from TheoryComponents.Key import *

from IMusicObject import *

class Note(IPitchedObject, IMusicObject):
    
    def __init__(self, p_key, p_duration, p_velocity = 127, p_dotted = False):
        self.key = p_key
        self.duration = Note.findClosestDuration(p_duration)
        self.velocity = p_velocity
        self.dotted = self.duration in [6 / 2**i for i in range(0, 34)]

    def __eq__(self, p_other): return (type(self) == type(p_other)) and (self.getKey() == p_other.getKey()) and (self.getDuration() == p_other.getDuration())

    def __getattr__(self, p_attr): return getattr(self.getKey(), p_attr)

    ##################
    # Representation #
    ##################

    def __str__(self): 
        return str(self.getKey()) + " " + (Note.rhythm_tree[4 / self.getDuration()] if not self.isDotted() else Note.rhythm_tree[4 / (self.getDuration() - (self.getDuration() / 3))] + " dotted")
    def __repr__(self): return self.__str__()

    ##############
    # Arithmetic #
    ##############

    def __add__(self, p_other):
        if (isinstance(p_other, Interval)): return Note(self.getKey() + p_other, self.getDuration())

    def __sub__(self, p_other): 
        if (isinstance(p_other, Interval)): return self.__add__(-p_other)
        if (isinstance(p_other, Note)): return self.getKey() - p_other.getKey()

    def __div__(self, p_other):
        if (isinstance(p_other, int)): return Note(self.getKey(), self.getDuration() * p_other)

    def __mul__(self, p_other):
        if (isinstance(p_other, int)): return Note(self.getKey(), self.getDuration() / p_other)

    ###########################
    # Playable Object Methods #
    ###########################

    def __play__(self): pass
    def __toMidiData__(self): return [self]

    ##################
    # Static Methods #
    ##################

    @staticmethod
    def findClosestDuration(p_duration):
        non_dotted_rhythms = [4 / 2**i for i in range(0, 34)]
        dotted_rhythms = [6 / 2**i for i in range(0, 34)]
        closest_rhythms = [min(non_dotted_rhythms, key=lambda x:abs(x-p_duration)), min(dotted_rhythms, key=lambda x:abs(x-p_duration))]
        closest_rhythm = min(closest_rhythms, key=lambda x:abs(x-p_duration))
        return closest_rhythm

    @staticmethod
    def ticksToDuration(p_ticks):
        if p_ticks == 0: return 0
        return Note.rhythm_tree[(Note.whole_note_tick_length / p_ticks)] if (Note.whole_note_tick_length / p_ticks) in Note.rhythm_tree else Note.rhythm_tree[min(Note.rhythm_tree.keys(), key=lambda k: abs(k - (Note.whole_note_tick_length / p_ticks)))]

    @staticmethod
    def durationToTicks(p_duration):
        if p_duration == 0: return 0
        return Note.whole_note_tick_length / p_duration

    #################
    # Sugar Methods #
    #################

    def simplify(self): return Note(self.getKey().simplify(), self.getDuration())
    def build(self, p_object, p_intervals, p_args): return p_object(self, p_intervals, **p_args)

    #######################
    # Getters and Setters #
    #######################

    def getTone(self): return self.getKey().getTone()
    def getKey(self): return self.key
    def getTicks(self): return self.durationToTicks(self.getDuration())
    def getDuration(self): return self.duration
    def getVelocity(self): return self.velocity
    def isDotted(self): return self.dotted

    def setDotted(self, p_dotted): self.dotted = p_dotted