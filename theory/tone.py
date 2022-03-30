from theory.i_pitched_object import IPitchedObject
from theory.interval import Interval

class Tone:

    def __init__(self, p_item_1, p_accidental = 0, p_parent_interval_list_item = None):
        if isinstance(p_item_1, str):
            self.tone_number = Tone.tone_names.index(p_item_1)

        elif isinstance(p_item_1, int):
            self.tone_number = p_item_1

        self.accidental = p_accidental
        self.parent_interval_list_item = p_parent_interval_list_item

    def hash_BL(self): 
        new_hash = hash((self.tone_number, self.accidental))
        return new_hash

    def str_BL(self):
        if self.get_accidental() < 0: 
            new_string = self.get_tone_name_BL() + (Tone.accidentals[-1] * abs(self.get_accidental()))
            return new_string

        elif self.get_accidental() > 0: 
            new_string = self.get_tone_name_BL() + (Tone.accidentals[1] * abs(self.get_accidental()))
            return new_string

        else: 
            new_string = self.get_tone_name_BL() + Tone.accidentals[0]
            return new_string

    def repr_BL(self):
        new_string = str(self)
        return new_string

	##############
	# Comparison #
	##############

    def eq_BL(self, p_other): 
        new_boolean = type(self) == type(p_other) and self.get_tone_number() == p_other.get_tone_number() and self.get_accidental() == p_other.get_accidental()
        return new_boolean

    def ne_BL(self, p_other): 
        new_boolean = not self.eq_BL(p_other)
        return new_boolean

    def gt_BL(self, p_other): 
        new_boolean = (self.get_tone_number() + self.get_accidental()) > (p_other.get_tone_number() + p_other.get_accidental())
        return new_boolean

    def lt_BL(self, p_other): 
        new_boolean = (self.get_tone_number() + self.get_accidental()) < (p_other.get_tone_number() + p_other.get_accidental())
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
        if isinstance(p_other, int):
            if p_other == 0: 
                return self

            sign = int(p_other / abs(p_other))

            if sign == 1:
                new_tone = self.next_BL().add_BL(p_other - 1)
                return new_tone

            new_tone = self.previous_BL().add_BL(p_other + 1)
            return new_tone

        if (isinstance(p_other, Interval)):
            if p_other.get_numeral() == 0: 
                return self
                
            if p_other.get_numeral() == 1: 
                return Tone(self.get_tone_number(), self.get_accidental() + p_other.get_semitones(), self.get_parent_interval_list_item())

            index = self.get_tone_number()
            sign = p_other.get_sign_BL()

            numeral_count = 0
            semitones_count = ((sign * -1) * self.get_accidental())

            while numeral_count != abs(p_other.get_numeral()):
                if index >= 12:
                    index -= 12

                elif index < 0:
                    index += 12

                if Tone.tone_names[index] != None: 
                    numeral_count += 1

                semitones_count += 1
                index += sign

            new_tone_number = index - sign
            new_accidental = (abs(p_other.get_semitones()) - (semitones_count - 1)) * sign
            new_tone = Tone(new_tone_number, new_accidental, self.get_parent_interval_list_item())
            return new_tone
        
        else: return p_other.add_BL(self)

    def sub_BL(self, p_other):
        if isinstance(p_other, int):
            return self.add_BL(-p_other)

        if isinstance(p_other, Interval):
            return self.add_BL(-p_other)

        if isinstance(p_other, Tone):
            if self.get_tone_number() == p_other.get_tone_number(): 
                new_interval = Interval(self.get_accidental() - p_other.get_accidental(), 1)
                return new_interval

            index = p_other.get_tone_number() + 1
            numeral_count = 1
            semitones_count = 0
            tone_name_x2 = Tone.tone_names * 2

            while tone_name_x2[index] != self.get_tone_name_BL():
                if tone_name_x2[index] != None: 
                    numeral_count += 1

                semitones_count += 1
                index += 1

            new_interval = Interval((semitones_count + 1) - p_other.get_accidental() + self.get_accidental(), numeral_count + 1, self.get_parent_interval_list_item())
            return new_interval

        else: return (-p_other).add_BL(self)

    def mul_BL(self, p_other):
        print("Error: Mulitplication for " + str(type(self))+ " has not been implemented")
        return -1

    def div_BL(self, p_other):
        print("Error: Division for " + str(type(self))+ " has not been implemented")
        return -1

    ##########################
    # Business Logic Methods #
    ##########################

    '''
    def get_relatives_BL(self, p_accidental_limit = None):
        relatives = []
        accidental_limit = Tone.accidental_limit + 1 if p_accidental_limit is None else p_accidental_limit + 1

        for i in range(accidental_limit):
            new_tone = self.remove_accidental_BL()
            while (new_tone - self).get_semitones() < i: new_tone = new_tone.next_BL().remove_accidental_BL()
            new_accidental = ((self - new_tone) if self.get_tone_name_BL() == new_tone.get_tone_name_BL() and self.get_accidental() > new_tone.get_accidental() else -(new_tone - self)).get_semitones()
            new_tone = Tone(new_tone.get_tone_name_BL(), new_accidental, self.get_parent_interval_list_item())
            if new_tone not in relatives and abs(new_tone.get_accidental()) < accidental_limit: relatives.append(new_tone)

            new_tone = self.remove_accidental_BL()
            while (self - new_tone).get_semitones() < i: new_tone = new_tone.previous_BL().remove_accidental_BL()
            new_accidental = (-(new_tone - self) if self.get_tone_name_BL() == new_tone.get_tone_name_BL() and new_tone.get_accidental() > self.get_accidental() else (self - new_tone)).get_semitones()
            new_tone = Tone(new_tone.get_tone_name_BL(), new_accidental, self.get_parent_interval_list_item())
            if new_tone not in relatives and abs(new_tone.get_accidental()) < accidental_limit: relatives.append(new_tone) 

        return relatives
    '''

    def get_relatives_BL(self, p_accidental_limit = None):
        relatives = []
        accidental_limit = Tone.accidental_limit + 1 if p_accidental_limit is None else p_accidental_limit + 1

        for i in range(accidental_limit):
            relatives += [Tone((self - i).get_tone_number(), (self - i).get_accidental() + i, self.get_parent_interval_list_item())]
            relatives += [Tone((self + i).get_tone_number(), (self + i).get_accidental() - i, self.get_parent_interval_list_item())]
            relatives += [Tone((self - (12 - i)).get_tone_number(), (self - (12 - i)).get_accidental() - i, self.get_parent_interval_list_item())]
            relatives += [Tone((self + (12 - i)).get_tone_number(), (self + (12 - i)).get_accidental() + i, self.get_parent_interval_list_item())]

        new_list = list(dict.fromkeys(relatives))
        return new_list

    def remove_accidental_BL(self):
        new_tone = Tone(self.get_tone_number(), 0, self.get_parent_interval_list_item())
        return new_tone

    '''
    def next_BL(self):
        index = Tone.tone_names.index(self.get_tone_name_BL()) + 12 + 1
        tone_names = (Tone.tone_names * 3)
        while tone_names[index] is None or tone_names[index] == self.get_tone_name_BL(): index += 1
        return Tone(tone_names[index], self.get_accidental(), self.get_parent_interval_list_item())

    def previous_BL(self):
        index = Tone.tone_names.index(self.get_tone_name_BL()) + 12 - 1
        tone_names = (Tone.tone_names * 3)
        while tone_names[index] is None or tone_names[index] == self.get_tone_name_BL(): index -= 1
        return Tone(tone_names[index], self.get_accidental(), self.get_parent_interval_list_item())
    '''

    def next_BL(self):
        index = self.get_tone_number() + self.get_accidental() + 12
        tone_names = Tone.tone_names * 2

        new_tone_number = index + 1 if tone_names[index + 1] is not None else self.get_tone_number()

        if new_tone_number < 0:
            new_tone_number += 12

        elif new_tone_number >= 12:
            new_tone_number -= 12

        new_accidental = 0 if tone_names[index + 1] else self.get_accidental() + 1
        new_tone =Tone(new_tone_number, new_accidental, self.get_parent_interval_list_item())
        return new_tone

    def previous_BL(self):
        index = self.get_tone_number() + self.get_accidental() + 12
        tone_names = Tone.tone_names * 2

        new_tone_number = index - 1 if tone_names[index - 1] is not None else self.get_tone_number()

        if new_tone_number < 0:
            new_tone_number += 12

        elif new_tone_number >= 12:
            new_tone_number -= 12

        new_accidental = 0 if tone_names[index - 1] else self.get_accidental() - 1
        new_tone =  Tone(new_tone_number, new_accidental, self.get_parent_interval_list_item())
        return new_tone

    def simplify_BL(self):
        index = self.get_tone_number() + 12
        tone_names_x20 = Tone.tone_names * 20
        
        if tone_names_x20[index + self.get_accidental()] == None:
            if self.get_accidental() > 0: 
                return [self.get_minimal_accidental_BL(), self.flip_accidental_BL().get_minimal_accidental_BL()]

            else: return [self.flip_accidental_BL().get_minimal_accidental_BL(), self.get_minimal_accidental_BL()]
            
        else: 
            new_tone_number = index + self.get_accidental()
   
            if new_tone_number < 0:
                new_tone_number += 12

            elif new_tone_number >= 12:
                new_tone_number -= 12

            new_tone = Tone(new_tone_number, 0, self.get_parent_interval_list_item())
            return new_tone

    def get_minimal_accidental_BL(self):
        index = self.get_tone_number() + 12 + self.get_accidental()
        semitones_count = 0
        tone_names_x20 = Tone.tone_names * 20

        while tone_names_x20[index] == None:
            index = index + int((self.get_accidental() / abs(self.get_accidental())) * -1)
            semitones_count = semitones_count + int(self.get_accidental() / abs(self.get_accidental()))

        new_tone_number = index

        if new_tone_number < 0:
            new_tone_number += 12

        elif new_tone_number >= 12:
            new_tone_number -= 12

        new_tone = Tone(new_tone_number, semitones_count, self.get_parent_interval_list_item())
        return new_tone

    def flip_accidental_BL(self): 
        new_tone = Tone(self.get_tone_number(), (12 - abs(self.get_accidental())) * (int(self.get_accidental() / abs(self.get_accidental())) * -1), self.get_parent_interval_list_item())
        return new_tone
        
    def build_BL(self, p_object, **p_args):
        new_object = p_object(self, **p_args)
        return new_object

    def get_tone_name_BL(self): 
        new_tone_name = Tone.tone_names[self.get_tone_number()]
        return new_tone_name

    def get_tone_BL(self):
        new_tone = self
        return new_tone

    #####################################
    # Overridden Business Logic Methods #
    #####################################

    def get_attributes(self): 
        return {
            "p_tone_number": self.get_tone_number(),
            "p_accidental": self.get_accidental(),
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

    def remove_accidental(self): 
        return self.remove_accidental_BL()

    def next(self): 
        return self.next_BL()

    def previous(self): 
        return self.previous_BL()

    def simplify(self): 
        return self.simplify_BL()

    def get_minimal_accidental(self): 
        return self.get_minimal_accidental_BL()

    def flip_accidental(self): 
        return self.flip_accidental_BL()
        
    def build(self, p_object, **p_args):
        return self.build_BL(p_object, **p_args)

    def get_tone_name(self): 
        return self.get_tone_name_BL()

    def get_tone(self):
        return self.get_tone_BL()

    #######################
    # Getters and Setters #
    #######################

    def get_tone_number(self): 
        return self.tone_number

    def get_accidental(self): 
        return self.accidental

    def get_parent_interval_list_item(self): 
        return self.parent_interval_list_item

    def set_tone_number(self, p_tone_number): 
        self.tone_number = p_tone_number

    def set_accidental(self, p_accidental): 
        self.accidental = p_accidental

    def set_parent_interval_list_item(self, p_parent_interval_list_item): 
        self.parent_interval_list_item = p_parent_interval_list_item