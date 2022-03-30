from theory.i_music_object import IMusicObject
from theory.key import *

class Note(IPitchedObject, IMusicObject):
    
    def __init__(self, p_key, p_duration, p_velocity = 127, p_parent_interval_list_item = None):
        self.key = p_key
        self.duration = Note.find_closest_duration(p_duration)
        self.velocity = p_velocity
        self.parent_interval_list_item = p_parent_interval_list_item

        self.get_key().set_parent_interval_list_item(self.get_parent_interval_list_item())

    def getattr_BL(self, p_attr): 
        return getattr(self.get_key(), p_attr)

    ##################
    # Representation #
    ##################

    def hash_BL(self): 
        new_hash = hash((self.key.hash_BL(), self.duration, self.velocity))
        return new_hash

    def str_BL(self): 
        new_string = str(self.get_key()) + " " + (Note.rhythm_tree[4 / self.get_duration()] if not self.is_dotted_BL() else Note.rhythm_tree[4 / (self.get_duration() - (self.get_duration() / 3))] + " dotted")
        return new_string
    
    def repr_BL(self): 
        new_string = self.str_BL()
        return new_string

	##############
	# Comparison #
	##############

    def eq_BL(self, p_other): 
        new_boolean = type(self) == type(p_other) and self.get_key() == p_other.get_key() and self.get_duration() == p_other.get_duration()
        return new_boolean

    def ne_BL(self, p_other): 
        new_boolean = not self.eq_BL(p_other)
        return new_boolean

    def gt_BL(self, p_other): 
        new_boolean = self.get_key() > p_other.get_key()
        return new_boolean

    def lt_BL(self, p_other): 
        new_boolean = self.get_key() < p_other.get_key()
        return new_boolean

    def ge_BL(self, p_other): 
        new_boolean = self.gt_BL(p_other) or self.eq_BL(p_other)
        return new_boolean

    def le_BL(self, p_other): 
        new_boolean = self.lt_BL(p_other) or self.eq_BL(p_other)
        return new_boolean

    ##############
    # Arithmetic #
    ##############

    def radd_BL(self, p_other, *p_args):
        if isinstance(p_other, str): 
            new_object = p_other.add_BL(self, *p_args)
            return new_object

        new_object = self.add_BL(p_other, *p_args)
        return new_object

    def rsub_BL(self, p_other, *p_args):
        new_object = self.sub_BL(p_other, *p_args)
        return new_object

    def rmul_BL(self, p_other, *p_args):
        new_object = self.mul_BL(p_other, *p_args)
        return new_object

    def rdiv_BL(self, p_other, *p_args):
        new_object = self.div_BL(p_other, *p_args)
        return new_object

    def add_BL(self, p_other):
        if isinstance(p_other, Interval):
            new_note = Note(self.get_key() + p_other, self.get_duration(), self.get_parent_interval_list_item())
            return new_note

        else: return p_other.add_BL(self)

    def sub_BL(self, p_other): 
        if isinstance(p_other, Interval): 
            new_note = self.add_BL(-p_other)
            return new_note

        if isinstance(p_other, Note): 
            new_interval = self.get_key() - p_other.get_key()
            return new_interval

        else: (-p_other).add_BL(self)

    def mul_BL(self, p_other):
        if isinstance(p_other, int): 
            new_note = Note(self.get_key(), self.get_duration() / p_other, self.get_parent_interval_list_item())
            return new_note

        else: return p_other.mul_BL(self)

    def div_BL(self, p_other):
        if isinstance(p_other, int): 
            new_note = Note(self.get_key(), self.get_duration() * p_other, self.get_parent_interval_list_item())
            return new_note

        else: return p_other.div_BL(self)

    ###########################
    # Playable Object Methods #
    ###########################

    def play_BL(self): 
        pass

    def to_midi_data_BL(self): 
        return [self]

    ##################
    # Static Methods #
    ##################

    @staticmethod
    def find_closest_duration(p_duration):
        non_dotted_rhythms = [4 / 2**i for i in range(0, 6)]
        dotted_rhythms = [6 / 2**i for i in range(0, 6)]
        closest_rhythms = [min(non_dotted_rhythms, key=lambda x:abs(x-p_duration)), min(dotted_rhythms, key=lambda x:abs(x-p_duration))]
       
        new_int = min(closest_rhythms, key=lambda x:abs(x-p_duration))
        return new_int

    @staticmethod
    def ticks_to_duration(p_ticks):
        if p_ticks == 0: 
            new_int = 0
            return new_int

        new_int = Note.rhythm_tree[(Note.time_division / p_ticks)] if (Note.time_division / p_ticks) in Note.rhythm_tree else Note.rhythm_tree[min(Note.rhythm_tree.keys(), key=lambda k: abs(k - (Note.time_division / p_ticks)))]
        return new_int

    @staticmethod
    def duration_to_ticks(p_duration):
        if p_duration == 0: 
            new_int = 0
            return new_int

        new_int = Note.time_division / p_duration
        return new_int

    ##########################
    # Business Logic Methods #
    ##########################

    def is_dotted_BL(self):
        new_boolean = self.duration in [6 / 2**i for i in range(0, 6)]
        return new_boolean

    def get_abs_position_BL(self):
        new_int = self.getParentSequencer().get_abs_position_BL()
        return new_int

    def get_tone_BL(self):
        new_tone = self.get_key().get_tone_BL()
        return new_tone

    def get_relative_BL(self, p_accidental_limit = None):
        new_list = [Note(key, self.get_duration(), self.get_velocity(), self.get_parent_interval_list_item()) for key in self.get_key().get_relative_BL(p_accidental_limit)]
        return new_list

    def simplify_BL(self):
        new_note = Note(self.get_key().simplify_BL(), self.get_duration(), self.get_parent_interval_list_item())
        return new_note

    def build_BL(self, p_object, **p_args):
        new_object = p_object(self, **p_args)
        return new_object

    def get_ticks_BL(self):
        new_int = self.duration_to_ticks(self.get_duration())
        return new_int

    ###################
    # Wrapper Methods #
    ###################

    def __hash__(self): 
        return self.hash_BL()

    def __str__(self):  
        return self.str_BL()

    def __repr__(self): 
        return self.repr_BL()

    def __eq__(self, p_other): 
        return self.eq_BL(p_other)

    def __ne__(self, p_other): 
        return self.ne_BL(p_other)

    def __lt__(self, p_other): 
        return self.lt_BL(p_other)

    def __ge__(self, p_other): 
        return self.ge_BL(p_other)

    def __le__(self, p_other): 
        return self.le_BL(p_other)

    def __radd__(self, p_other, *p_args): 
        return self.radd_BL(p_other, *p_args)

    def __rsub__(self, p_other, *p_args): 
        return self.rsub_BL(p_other, *p_args)

    def __rmul__(self, p_other, *p_args): 
        return self.rmul_BL(p_other, *p_args)

    def __rdiv__(self, p_other, *p_args): 
        return self.rdiv_BL(p_other, *p_args)

    def __add__(self, p_other): 
        return self.add_BL(p_other)
        
    def __sub__(self, p_other): 
        return self.sub_BL(p_other)

    def __mul__(self, p_other):
        return self.mul_BL(p_other)

    def __div__(self, p_other):
        return self.div_BL(p_other)

    def is_dotted(self): 
        return self.is_dotted_BL()

    def get_abs_position(self): 
        return self.get_abs_position_BL()

    def get_tone(self): 
        return self.get_tone_BL()

    def get_relative(self, p_accidental_limit = None): 
        return self.get_relative_BL(p_accidental_limit)

    def simplify(self): 
        return self.simplify_BL()

    def build(self, p_object, **p_args): 
        return self.build_BL(p_object, **p_args)

    def get_ticks(self): 
        return self.get_ticks_BL()

    #####################################
    # Overridden Business Logic Methods #
    #####################################

    def get_attributes(self): 
        return {
            "p_key": self.get_key(),
            "p_duration": self.get_duration(),
            "p_velocity": self.get_velocity(),
            "p_parent_interval_list_item": self.get_parent_interval_list_item()
        }

    #######################
    # Getters and Setters #
    #######################

    def get_key(self): 
        return self.key
        
    def get_duration(self): 
        return self.duration
        
    def get_velocity(self): 
        return self.velocity

    def get_parent_interval_list_item(self): 
        return self.parent_interval_list_item

    def set_key(self, p_key): 
        self.key = p_key
        
    def set_duration(self, p_duration): 
        self.duration = p_duration
        
    def set_velocity(self): 
        self.velocity = p_velocity

    def set_parent_interval_list_item(self, p_parent_interval_list_item): 
        self.parent_interval_list_item = p_parent_interval_list_item