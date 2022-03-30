from theory.tone import *

class Key(IPitchedObject):

    def __init__(self, p_tone, p_octave, p_parent_interval_list_item = None):
        self.octave = p_octave
        self.tone = p_tone
        self.parent_interval_list_item = p_parent_interval_list_item

        self.get_tone().set_parent_interval_list_item(self.get_parent_interval_list_item())

    ##################
    # Representation #
    ##################

    def hash_BL(self): 
        new_hash = hash((self.tone.hash_BL(), self.tone))
        return new_hash

    def str_BL(self): 
        new_string = self.get_tone().str_BL() + str(self.get_octave())
        return new_string

    def repr_BL(self): 
        new_string = self.str_BL()
        return new_string

	##############
	# Comparison #
	##############

    def eq_BL(self, p_other): 
        new_boolean = type(self) == type(p_other) and self.get_tone() == p_other.get_tone() and self.get_octave() == p_other.get_octave()
        return new_boolean

    def ne_BL(self, p_other): 
        new_boolean = not self.eq_BL(p_other)
        return new_boolean

    def gt_BL(self, p_other): 
        new_boolean = self.get_octave() < p_other.get_octave() if self.get_octave() != p_other.get_octave() else self.get_tone() < p_other.get_tone()
        return new_boolean

    def lt_BL(self, p_other): 
        new_boolean = self.get_octave() < p_other.get_octave() if self.get_octave() != p_other.get_octave() else self.get_tone() < p_other.get_tone()
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
            sign = p_other.get_sign_BL()
            other = abs(p_other)

            if other >= Interval(12, 8): 
                new_key = Key(self.get_tone(), self.get_octave() + sign, self.get_parent_interval_list_item()) + (sign * (other.sub_BL(Interval(12, 8))))
                return new_key

            distance_till_next_octave = (Key.start_point.sub_BL(self.get_tone())) if sign == 1 else (self.get_tone().sub_BL(Key.start_point))

            if self.get_tone().get_tone_name_BL() == Key.start_point.get_tone_name_BL() and sign == 1: 
                distance_till_next_octave = Interval(12, 8)

            octave = self.get_octave()

            if (other > distance_till_next_octave and (sign != -1 or other.get_numeral() != distance_till_next_octave.get_numeral())) or (sign == 1 and (other.get_numeral() == distance_till_next_octave.get_numeral())): 
                octave += sign

            new_key = Key(self.get_tone().add_BL(sign * other), octave, self.get_parent_interval_list_item())
            return new_key

        else: return p_other.add_BL(self)

    def sub_BL(self, p_other):
        if isinstance(p_other, Interval):
            return self.add_BL(-p_other)

        if isinstance(p_other, Key):
            if p_other.get_octave() < self.get_octave():
                new_interval = Interval(12, 8).add_BL(self.sub_BL(Interval(12, 8)).sub_BL(p_other))
                return new_interval

            if p_other.get_octave() > self.get_octave():
                new_interval = -p_other.sub_BL(self)
                return new_interval
            
            if (self - self.get_tone().sub_BL(p_other.get_tone())).get_octave() != self.get_octave(): 
                new_interval = -p_other.get_tone().sub_BL(self.get_tone())
                return new_interval

            new_interval = self.get_tone().sub_BL(p_other.get_tone())
            return new_interval

        else: return (-p_other).add_BL(self)

    def mul_BL(self, p_other):
        print("Error: Mulitplication for " + str(type(self))+ " has not been implemented")
        return -1

    def div_BL(self, p_other):
        print("Error: Division for " + str(type(self))+ " has not been implemented")
        return -1

    ##################
    # Static Methods #
    ##################

    @staticmethod
    def decimal_to_key(p_decimal_number):
        temp_key_semitones = p_decimal_number - 21
        
        new_key = Key(Tone("A", 0), 0, self.get_parent_interval_list_item()) + min(Interval.getPossibleIntervals(temp_key_semitones), key=lambda x: x.getAccidentalAsSemitones())
        return new_key

    ##########################
    # Business Logic Methods #
    ##########################
    
    def get_relatives_BL(self, p_accidental_limit = None):
        new_list = []

        for tone in self.get_tone().get_relatives_BL(p_accidental_limit):
            tone_motion = (tone - self.get_tone()) if tone.get_accidental() < self.get_tone().get_accidental() else -(self.get_tone() - tone)
            new_list += [self + tone_motion]

        return new_list

    def simplify_BL(self): 
        new_key = Key(self.get_tone().simplify_BL(), self.get_octave(), self.get_parent_interval_list_item())
        return new_key

    def to_decimal_BL(self):
        new_int = (self - Key(Tone("A", 0), 0, self.get_parent_interval_list_item())).get_semitones_BL() + 21
        return new_int

    def build_BL(self, p_object, **p_args):
        new_object = p_object(self, **p_args)
        return new_object

    def get_relatives_BL(self, p_accidental_limit = None):
        new_list = []

        for tone in self.get_tone().get_relatives_BL(p_accidental_limit):
            tone_motion = (tone - self.get_tone()) if tone.get_accidental() < self.get_tone().get_accidental() else -(self.get_tone() - tone)
            new_list += [self + tone_motion]

        return new_list

    def simplify_BL(self): 
        new_key = Key(self.get_tone().simplify_BL(), self.get_octave(), self.get_parent_interval_list_item())
        return new_key

    def to_decimal_BL(self):
        new_int = (self - Key(Tone("A", 0), 0, self.get_parent_interval_list_item())).get_semitones_BL() + 21
        return new_int

    def build_BL(self, p_object, **p_args):
        new_object = p_object(self, **p_args)
        return new_object

    #####################################
    # Overridden Business Logic Methods #
    #####################################

    def get_attributes(self): 
        return {
            "p_octave": self.get_octave(),
            "p_tone": self.get_tone(),
            "p_parent_interval_list_item": self.get_parent_interval_list_item()
        }

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

    def __add__(self, p_other): 
        return self.add_BL(p_other)
        
    def __sub__(self, p_other): 
        return self.sub_BL(p_other)

    def get_relatives(self, p_accidental_limit = None): 
        return self.get_relatives_BL(p_accidental_limit)

    def simplify(self): 
        return self.simplify_BL()

    def to_decimal(self): 
        return self.to_decimal_BL()

    def build(self, p_object, **p_args): 
        return self.build_BL(p_object, **p_args)

    def get_relatives(p_accidental_limit = None): 
        return self.get_relatives_BL(p_accidental_limit)

    def simplify(self): 
        return self.simplify_BL()

    def to_decimal(self): 
        return self.to_decimal_BL()

    def build(self, p_object, **p_args):
        return self.build_BL(p_object, **p_args)

    #######################
    # Getters and Setters #
    #######################

    def set_octave(self, p_octave): 
        self.octave = p_octave

    def set_tone(self, p_tone): 
        self.tone = p_tone

    def set_parent_interval_list_item(self, p_parent_interval_list_item): 
        self.parent_interval_list_item = p_parent_interval_list_item

    def get_octave(self): 
        return self.octave

    def get_tone(self): 
        return self.tone

    def get_parent_interval_list_item(self): 
        return self.parent_interval_list_item