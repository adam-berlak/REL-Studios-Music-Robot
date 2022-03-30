import re
import json

class Interval:

	unaltered_intervals = []
	accidentals = []

	def __init__(self, p_semitones, p_numeral, p_parent_interval_list_item = None):
		self.semitones = p_semitones
		self.numeral = p_numeral if not (p_numeral == -1) else 1
		self.parent_interval_list_item = p_parent_interval_list_item

	def toJson(self):
		data_set = {
			"semitones": self.get_semitones(),
			"numeral": self.get_numeral()
		}
		
		return data_set
		
	def deepcopy_BL(self, p_memo):
		new_interval = type(self)(self.get_semitones(), self.get_numeral())
		return new_interval

	def hash_BL(self): 
		new_hash = hash((self.semitones, self.numeral))
		return new_hash

	def str_BL(self): 
		prefix = ""

		if self.get_numeral() < 0: 
			prefix = "-"

		new_string = prefix + (abs(self).get_accidental_BL() + str(abs(self).get_numeral()))
		return new_string

	def repr_BL(self):
		new_string = str(self)
		return new_string

	##############
	# Comparison #
	##############

	def eq_BL(self, p_other): 
		new_boolean = type(self) == type(p_other) and self.get_semitones() == p_other.get_semitones() and self.get_numeral() == p_other.get_numeral()
		return new_boolean

	def ne_BL(self, p_other): 
		new_boolean = not self.eq_BL(p_other)
		return new_boolean

	def gt_BL(self, p_other): 
		new_boolean = self.get_numeral() > p_other.get_numeral() if self.get_numeral() != p_other.get_numeral() else self.get_semitones() > p_other.get_semitones()
		return new_boolean

	def lt_BL(self, p_other): 
		new_boolean = self.get_numeral() < p_other.get_numeral() if self.get_numeral() != p_other.get_numeral() else self.get_semitones() < p_other.get_semitones() 
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

	def abs_BL(self):
		new_interval = Interval(abs(self.get_semitones()) if self.get_numeral() != 1 else self.get_semitones(), abs(self.get_numeral()), self.get_parent_interval_list_item())
		return new_interval

	def neg_BL(self):
		new_interval = Interval(-self.get_semitones(), -self.get_numeral(), self.get_parent_interval_list_item())
		return new_interval

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
			new_semitones = self.get_semitones() + p_other.get_semitones()
			new_numeral = Interval.numeral_add(self.get_numeral(), p_other.get_numeral())
			new_interval = Interval(new_semitones, new_numeral, self.get_parent_interval_list_item())
			return new_interval

		if isinstance(p_other, int): 
			if p_other == 0: 
				new_interval = self
				return new_interval
			
			elif self.next_BL().remove_accidental_BL().get_semitones() == self.get_semitones() + 1: 
				new_interval = Interval(self.get_semitones() + 1, self.next_BL().get_numeral(), self.get_parent_interval_list_item()).add_BL(p_other - 1)
				return new_interval

			else: 
				new_interval = Interval(self.get_semitones() + 1, self.get_numeral(), self.get_parent_interval_list_item()).add_BL(p_other - 1)
				return new_interval

		if isinstance(p_other, str):
			new_string = str(self) + p_other
			return new_string

		else: return p_other.add_BL(self)

	def sub_BL(self, p_other):
		if isinstance(p_other, Interval): 
			return self.add_BL(-p_other)
			
		else: return (-p_other).add_BL(self)

	def mul_BL(self, p_other):
		if isinstance(p_other, int):
			if p_other == 0:
				new_interval = Interval(0, 1)
				return new_interval

			sign = p_other / abs(p_other) if p_other is not 0 else 1
			new_object = self
			counter = p_other

			while counter != sign:
				new_object += self
				counter -= sign

			if sign == -1:
				new_interval = Interval(-new_object.get_semitones(), -new_object.get_numeral(), self.get_parent_interval_list_item())
				return new_interval
			
			return new_object

		else: return p_other.mul_BL(self)

	def div_BL(self, p_other):
		print("Error: Division for " + str(type(self))+ " has not been implemented")
		return -1

	##################
	# Static Methods #
	##################

	@staticmethod
	def int_to_roman(p_integer):
		if p_integer < 0:
			return "-" + Interval.int_to_roman(abs(p_integer))

		val = [
			1000, 900, 500, 400,
			100, 90, 50, 40,
			10, 9, 5, 4,
			1
			]

		syb = [
			"M", "CM", "D", "CD",
			"C", "XC", "L", "XL",
			"X", "IX", "V", "IV",
			"I"
			]

		roman_num = ''
		i = 0

		while  p_integer > 0:
			for _ in range(p_integer // val[i]):
				roman_num += syb[i]
				p_integer -= val[i]

			i += 1

		return roman_num

	@staticmethod
	def string_to_accidental(p_accidental):
		new_list = list(Interval.accidentals.keys())[list(Interval.accidentals.values()).index(p_accidental)]
		return new_list

	@staticmethod
	def get_simple_numeral(p_numeral):
		while p_numeral > 7: 
			p_numeral -= 7

		while p_numeral < 1: 
			p_numeral += 7

		new_int = p_numeral
		return new_int

	@staticmethod
	def get_simple_semitones(p_semitones):
		while p_semitones > 11: 
			p_semitones -= 12

		while p_semitones < 0: 
			p_semitones += 12

		new_int = p_semitones
		return new_int

	@staticmethod
	def in_range(p_start, p_stop, p_step, p_direction = 1):
		new_numerals = []
		step = p_step if p_step is not None else 2

		for i in range(p_stop):
			multiplier = i

			if isinstance(step, int):
				new_item = Interval.numeral_mul(step, multiplier)
				
				if (new_item > p_start and new_item < p_stop) or (new_item == p_start and p_direction == 1) or (new_item == p_stop and p_direction == -1):
					new_numerals.append(new_item)

			elif isinstance(step, Interval):
				new_item = step.mul_BL(multiplier)

				if (new_item.get_numeral() > p_start and new_item.get_numeral() < p_stop) or (new_item.get_numeral() == p_start and p_direction == 1) or (new_item.get_numeral() == p_stop and p_direction == -1):
					new_numerals.append(new_item)

		new_list = new_numerals
		return new_list

	@staticmethod
	def numeral_mul(p_item_1, p_item_2):
		if p_item_2 == 0: 
			new_numeral = 1
			return new_numeral

		sign = int(p_item_2 / abs(p_item_2))
		new_numeral = 1

		for i in range(abs(p_item_2)):
			new_numeral = Interval.numeral_add(new_numeral, p_item_1)

		new_numeral = new_numeral * sign
		return new_numeral

	@staticmethod
	def numeral_add(p_item_1, p_item_2):
		sign_item_1 = int(p_item_1 / abs(p_item_1))
		sign_item_2 = int(p_item_2 / abs(p_item_2))

		p_item_1 -= sign_item_1
		p_item_2 -= sign_item_2
		
		new_numeral = p_item_1 + p_item_2

		if new_numeral <= 0:
			new_numeral -= 1

		else: new_numeral += 1

		if abs(new_numeral) == 1:
			new_numeral *= -sign_item_1

		return new_numeral

	@staticmethod
	def string_to_interval(p_string):
		intervals = Interval.multiply_semitone_list(Interval.unaltered_intervals, 20)
		numeral = int(re.findall(r'\d+', p_string)[0])
		regex = "[" + str([item for item in Interval.accidentals.values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1] + "]"
		accidentals = re.findall(re.compile(regex), p_string)
		semitones = intervals[numeral - 1]

		if len(accidentals) != 0:
			accidental = accidentals[0]
			semitones = semitones + list(Interval.accidentals.keys())[list(Interval.accidentals.values()).index(accidental)]

		new_interval = Interval(semitones, numeral)
		return new_interval

	@staticmethod
	def get_possible_intervals(p_semitones):
		previous_list = Interval.generate_interval_list(Interval.unaltered_intervals)
		octaves = 1

		while len(previous_list) <= p_semitones:
			temp_list = previous_list[:]

			for intervals in previous_list[:12]: 
				temp_list.append([item + (Interval(12, 8) * octaves) for item in intervals])

			previous_list = temp_list[:]
			octaves += 1

		new_list = previous_list[p_semitones]
		return new_list

	@staticmethod
	def generate_interval_list(p_unaltered_intervals):
		new_object = []
		degree_count = 1

		for i in range(max(p_unaltered_intervals) + 1):
			if i not in p_unaltered_intervals: 
				new_object.append([Interval(i, degree_count - 1), Interval(i, degree_count)])
				
			else:
				new_object.append([Interval(i, degree_count)])
				degree_count = degree_count + 1

		return new_object

	@staticmethod
	def multiply_semitone_list(p_semitone_list, p_multiplier):
		new_object = p_semitone_list[:]

		for i in range(1, p_multiplier):
			for semitones in p_semitone_list:
				new_semitones = semitones + (12 * i)
				new_object.append(new_semitones)

		return new_object

	@staticmethod
	def multiply_pitch_class(p_pitch_class, p_multiplier):
		new_object = p_pitch_class

		for i in range(1, p_multiplier):
			for interval in p_pitch_class:
				new_interval = Interval(interval.get_semitones() + (12 * i), interval.get_numeral() + (7 * i))
				new_object.append(new_interval)

		return new_object

	##########################
	# Business Logic Methods #
	##########################

	def get_accidental_BL(self):
		if self.get_sign_BL() == -1:
			new_string = self.neg_BL().get_accidental_BL()
			return new_string

		accidental = self.get_accidental_as_semitones_BL()

		if accidental < 0: 
			new_string = Interval.accidentals[-1] * abs(accidental)
			return new_string

		elif accidental > 0: 
			new_string = Interval.accidentals[1] * abs(accidental)
			return new_string

		else:
			new_string = Interval.accidentals[0]
			return new_string

	def get_accidental_as_semitones_BL(self):
		default_semitones = Interval.multiply_semitone_list(Interval.unaltered_intervals, 20)[self.get_numeral() - 1]
		new_int = self.get_semitones() - default_semitones
		return new_int

	def transform_BL(self, p_accidental):
		if isinstance(p_accidental, str): 
			new_semitones = self.get_semitones() + Interval.string_to_accidental(p_accidental)
			new_interval = Interval(new_semitones, self.get_numeral(), self.get_parent_interval_list_item())
			return new_interval

		elif isinstance(p_accidental, int):
			new_interval = Interval(self.get_semitones() + p_accidental, self.get_numeral(), self.get_parent_interval_list_item())
			return new_interval

	def flip_axis_BL(self):
		new_interval = self.simplify_BL()
		new_interval = new_interval - Interval(12, 8) if self.get_sign_BL() == 1 else new_interval
		new_interval = new_interval + (-self.get_octave_range_BL() * Interval(12, 8))
		return new_interval

	def get_sign_BL(self):
		new_int = int(self.get_numeral() / abs(self.get_numeral()))
		return new_int

	def remove_accidental_BL(self):
		new_interval = Interval(self.get_semitones() - self.get_accidental_as_semitones_BL(), self.get_numeral(), self.get_parent_interval_list_item())
		return new_interval

	def get_octave_range_BL(self): 
		if self < Interval(0, 0): 
			new_int = -int(abs(self.get_semitones()) / 12) - 1
			return new_int

		new_int = int(self.get_semitones() / 12)
		return new_int

	def get_identical_intervals_BL(self): 
		new_list = Interval.get_possible_intervals(self.get_semitones())
		return new_list
	
	def roof_BL(self): 
		if self < Interval(0, 0): 
			return -abs(self).floor_BL()

		elif self == Interval(0, 1):
			return self

		new_interval = self + (Interval(12, 8) - self.simplify_BL())
		return new_interval

	def floor_BL(self):
		if self < Interval(0, 0): 
			return -abs(self).roof_BL()

		elif self == Interval(0, 1):
			return self

		new_interval = self - (self.simplify_BL())
		return new_interval

	def simplify_BL(self):
		sign = self.get_sign_BL()
		new_object = self
		delta = Interval(12, 8) * sign
		
		while abs(new_object.get_numeral()) >= 8 or new_object.get_numeral() < 1:
			if new_object >= Interval(12, 8) and sign == -1:
				new_object -= Interval(12, 8)
				break

			new_object -= delta

		return new_object

	def next_BL(self):
		if self.get_numeral() == len(Interval.unaltered_intervals): 
			new_interval = Interval(Interval.unaltered_intervals[0] + self.get_accidental_as_semitones_BL(), 1, self.get_parent_interval_list_item())
			shift = Interval(12, 8) * (self.get_octave_range_BL() + 1)
		
		else:
			new_interval = Interval(Interval.unaltered_intervals[(self.simplify_BL().get_numeral() - 1) + 1] + self.get_accidental_as_semitones_BL(), self.simplify_BL().get_numeral() + 1, self.get_parent_interval_list_item())
			shift = Interval(12, 8) * self.get_octave_range_BL()

		new_interval += shift
		return new_interval

	#####################################
	# Overridden Business Logic Methods #
	#####################################

	def get_attributes(self): 
		return {
			"p_semitones": self.get_semitones(),
			"p_numeral": self.get_numeral(),
			"p_parent_interval_list_item": self.get_parent_interval_list_item()
		}
	
	###################
	# Wrapper Methods #
	###################

	def __deepcopy__(self, p_memo):
		return self.deepcopy_BL(p_memo)

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

	def __abs__(self):
		return self.abs_BL()

	def __neg__(self):
		return self.neg_BL()

	def __radd__(self, p_other, *p_args): 
		return self.radd_BL(p_other, *p_args)

	def __rsub__(self, p_other, *p_args): 
		return self.rsub_BL(p_other, *p_args)

	def __rmul__(self, p_other, *p_args):
		return self.rmul_BL(p_other, *p_args)

	def __add__(self, p_other): 
		return self.add_BL(p_other)
		
	def __sub__(self, p_other): 
		return self.sub_BL(p_other)

	def __mul__(self, p_other):
		return self.mul_BL(p_other)

	def get_accidental(self):
		return self.get_accidental_BL()
		
	def get_accidental_as_semitones(self):
		return self.get_accidental_as_semitones_BL()

	def transform(self, p_accidental):
		return self.transform_BL(p_accidental)

	def flip_axis(self):
		return self.flip_axis_BL()

	def get_sign(self):
		return self.get_sign_BL()

	def remove_accidental(self):
		return self.remove_accidental_BL()

	def get_octave_range(self):
		return self.get_octave_range_BL()

	def get_identical_intervals(self):
		return self.get_identical_intervals_BL()

	def roof(self): 
		return self.roof_BL()

	def floor(self):
		return self.floor_BL()

	def simplify(self):
		return self.simplify_BL()

	def next(self):
		return self.next_BL()

	#######################
	# Getters and Setters #
	#######################
		
	def set_semitones(self, p_semitones): 
		self.semitones = p_semitones

	def set_numeral(self, p_numeral): 
		self.numeral = p_numeral

	def set_parent_interval_list_item(self, p_parent_interval_list_item): 
		self.parent_interval_list_item = p_parent_interval_list_item
		
	def get_semitones(self): 
		return self.semitones

	def get_numeral(self): 
		return self.numeral

	def get_parent_interval_list_item(self): 
		return self.parent_interval_list_item

class GenericInterval:

	def __init__(self, p_numeral, p_interval):
		self.numeral = p_numeral
		self.interval = p_interval

	##################
	# Representation #
	##################

	def hash_BL(self): 
		new_hash = hash((self.numeral, self.interval.hash_BL()))
		return new_hash

	def str_BL(self):
		new_string = "(" if self.get_interval() != Interval(0, 1) else ""

		new_string += str(self.get_numeral()) + (" + " + (str(self.get_interval()) + ")") if self.get_interval() != Interval(0, 1) else "")
		return new_string

	def repr_BL(self):
		new_string = self.str_BL()
		return new_string

	##############
	# Arithmetic #
	##############

	def neg_BL(self):
		new_numeral = -self.get_numeral()
		new_interval = self.get_interval().neg_BL()
		
		new_generic_interval = GenericInterval(new_numeral, new_interval)
		return new_generic_interval

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
			new_numeral = Interval.numeral_add(self.get_numeral(), p_other)
			new_interval = self.get_interval()

			new_generic_interval = GenericInterval(new_numeral, new_interval)
			return new_generic_interval

		if isinstance(p_other, Interval):
			new_numeral = self.get_numeral()
			new_interval = self.get_interval().add_BL(p_other)

			new_generic_interval = GenericInterval(new_numeral, new_interval)
			return new_generic_interval

		if isinstance(p_other, GenericInterval):
			new_numeral = Interval.numeral_add(self.get_numeral(), p_other.get_numeral())
			new_interval = self.get_interval().add_BL(p_other.get_interval())

			new_generic_interval = GenericInterval(new_numeral, new_interval)
			return new_generic_interval

		else: return p_other.add_BL(self)

	def sub_BL(self, p_other):
		if isinstance(p_other, int):
			new_generic_interval = self.add_BL(-p_other)
			return new_generic_interval

		if isinstance(p_other, Interval):
			new_generic_interval = self.add_BL(-p_other)
			return new_generic_interval

		if isinstance(p_other, GenericInterval):
			new_generic_interval = self.add_BL(-p_other)
			return new_generic_interval

		else: return (-p_other).add_BL(self)

	def mul_BL(self, p_other):
		print("Error: Mulitplication for " + str(type(self))+ " has not been implemented")
		return -1

	def div_BL(self, p_other):
		print("Error: Division for " + str(type(self))+ " has not been implemented")
		return -1

	#####################################
	# Overridden Business Logic Methods #
	#####################################

	def get_attributes(self): 
		return {
			"p_interval": self.get_interval(),
			"p_numeral": self.get_numeral()
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

	def __neg__(self):
		return self.neg_BL()

	def __radd__(self, p_other, *p_args): 
		return self.radd_BL(p_other, *p_args)

	def __rsub__(self, p_other, *p_args): 
		return self.rsub_BL(p_other, *p_args)

	def __add__(self, p_other): 
		return self.add_BL(p_other)
		
	def __sub__(self, p_other): 
		return self.sub_BL(p_other)

	#######################
	# Getters and Setters #
	#######################

	def get_numeral(self):
		return self.numeral

	def get_interval(self):
		return self.interval