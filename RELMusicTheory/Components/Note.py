from Components.IPitchedObject import *
from Components.Interval import *
from Components.Key import *

class Note(IPitchedObject):
    
    def __init__(self, p_key, p_duration, p_velocity = 127):
        self.key = p_key
        self.duration = p_duration
        self.velocity = p_velocity

    def __eq__(self, p_other): return (type(self) == type(p_other)) and (self.getKey() == p_other.getKey()) and (self.getDuration() == p_other.getDuration())

    def __getattr__(self, p_attr): return getattr(self.getKey(), p_attr)

    ##################
    # Representation #
    ##################

    def __str__(self): return str(self.getKey()) + " " + Note.rhythm_tree[self.getDuration()]
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

    ##################
    # Static Methods #
    ##################

    @staticmethod
    def ticksToDuration(p_ticks):
        return Note.rhythm_tree[(Note.whole_note_tick_length / p_ticks)] if (Note.whole_note_tick_length / p_ticks) in Note.rhythm_tree else Note.rhythm_tree[min(Note.rhythm_tree.keys(), key=lambda k: abs(k - (Note.whole_note_tick_length / p_ticks)))]

    #################
    # Sugar Methods #
    #################

    def simplify(self): return Note(self.getKey().simplify(), self.getDuration())
    def build(self, p_object, *args): return p_object(self, *args)

    #######################
    # Getters and Setters #
    #######################

    def getTone(self): return self.getKey().getTone()
    def getKey(self): return self.key
    def getDuration(self): return self.duration
    def getVelocity(self): return self.velocity