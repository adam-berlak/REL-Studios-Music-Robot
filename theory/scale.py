import re
import collections
import itertools
import statistics

from theory.interval_list import *

class Scale(IntervalList, IMusicObject):
	
	def __init__(self, 
		p_item_1, 
		p_item_2 = None, 
		p_unaltered_intervals = [], 
		p_type_dict = {}, 
		p_sublist = False, 
		p_altered = True,
		p_floor = None,
		p_roof = None, 
		p_direction = 1):

		defaults = {
			"p_item_1": p_item_1,
			"p_item_2": p_item_2, 
			"p_unaltered_intervals": p_unaltered_intervals,
			"p_type_dict": p_type_dict,
			"p_sublist": p_sublist,
			"p_altered": p_altered,
			"p_floor": p_floor,
			"p_roof": p_roof, 
			"p_direction": p_direction
		}

		if isinstance(p_item_1, IntervalList):
			defaults.update(p_item_1.getAttributes())

		p_item_1 = defaults["p_item_1"]
		p_item_2 = defaults["p_item_2"]
		p_unaltered_intervals = defaults["p_unaltered_intervals"]
		p_type_dict = defaults["p_type_dict"]
		p_sublist = defaults["p_sublist"]
		p_altered = defaults["p_altered"]
		p_floor = defaults["p_floor"]
		p_roof = defaults["p_roof"]
		p_direction = defaults["p_direction"]

		parent_item = Scale.configure_reference_point(p_item_1)
		intervals = Scale.configure_intervals(p_item_1, p_item_2)
		type_dict = p_type_dict

		self.sublist = p_sublist
		self.altered = p_altered

		self.tonic_tone = parent_item.get_reference_point() if isinstance(parent_item, IntervalList.Item) else parent_item
		self.parent_item = Scale.configure_parent_item(parent_item, intervals, self.sublist) if isinstance(parent_item, IntervalList.Item) else None

		bounds = Scale.configure_bounds(p_floor, p_roof, p_direction, intervals)

		self.direction = p_direction
		self.floor = bounds["floor"]
		self.roof = bounds["roof"]
		
		self.unaltered_intervals = Scale.configure_unaltered_intervals(intervals, p_unaltered_intervals, self.sublist, self.parent_item, (self.roof - self.floor))
	
		self.derived_attributes = {}
		self.build_items(intervals, type_dict)

	##################
	# Object Methods #
	##################

	#########################
	# Configuration Methods #
	#########################

	@staticmethod
	def configure_intervals(p_item_1, p_item_2):
		if issubclass(type(p_item_2), int):
			new_intervals = Utilities.decimal_to_pitch_class(p_item_2)
			return new_intervals

		else: 
			new_intervals = IntervalList.configure_intervals(p_item_1, p_item_2)
			return new_intervals

	#################
	# Sugar Methods #
	#################

	def get_modes(self): 
		return [self.rotate_BL(integer) for integer in range(1, len(self.get_intervals()) + 1)]

	def get_tonic(self): 
		return self.get_items()[0]

	def get_included_degrees(self): 
		return [item for item in self.get_items() if not item.is_omitted()]

	def get_diatonc_degrees(self): 
		return [item for item in self.get_items() if not item.is_chromatic()]

	def get_parent_scale(self): 
		return self.get_parent_interval_list_BL()

	def get_degree_by_interval(self, p_interval): 
		return self.get_item_by_interval_BL(p_interval)

	def get_degree_by_numeral(self, p_numeral): 
		return self.get_item_by_numeral_BL(p_numeral)

	def get_degrees(self): 
		return self.get_items()

	def get_parent_degree(self): 
		return self.get_parent_item()

	def set_degrees(self, p_degrees):
		self.set_item(p_degrees)

	def set_parent_degree(self, p_parent_degree):
		self.set_parent_item(p_parent_degree)

	##########################
	# Business Logic Methods #
	##########################

	def get_name_BL(self): 
		new_list = scale_names[Utilities.pitch_class_to_decimal([item.get_interval() for item in self.get_included_degrees()])]
		return new_list

	def get_mode_names_BL(self): 
		new_list = [(self.add_BL(item + 1)).get_name_BL() for item in range(len(self.get_intervals()))]
		return new_list
		
	def get_hemitonia_BL(self): 
		new_int = self.count_intervals_BL(1)
		return new_int
		
	def get_tritonia_BL(self): 
		new_int = self.count_intervals_BL(6)
		return new_int

	def get_cardinality_BL(self, p_system = DEFAULT_SYSTEM): 
		new_string = CARDINALITY[p_system][len(self.get_items())]
		return new_string

	def has_cohemitonia_BL(self): 
		new_boolean = len(self.get_cohemitonic_BL()) != 0
		return new_boolean

	def is_prime_BL(self): 
		new_boolean = self.get_prime_mode_BL() == self
		return new_boolean

	def count_intervals_BL(self, p_interval_size):
		new_int = 0
		next_scale = self

		for i in range(len(self.get_intervals())):
			
			if p_interval_size in next_scale.get_semitones_BL():
				new_int += 1

			next_scale = next_scale.rotate()

		if p_interval_size == 6: 
			new_int /= 2

		return new_int

	def get_imperfections_BL(self):
		new_int = 0

		for degree in self.get_items(): 
			if P5 not in degree.getitem_BL(slice(None, None, None)).get_intervals():
				new_int += 1

		return new_int
	
	def get_rotational_symmetry_BL(self):
		parent_pitch_class = Utilities.pitch_class_to_scale_steps(self.get_intervals())
		new_object = []

		for degree in self.get_items():
			if degree == self.get_items()[0]: continue

			child_pitch_class = Utilities.pitch_class_to_scale_steps(degree.getitem_BL(slice(None, None, None)).get_intervals())

			if parent_pitch_class == child_pitch_class: new_object.append(degree.get_position_BL())

		return new_object

	def get_reflection_axes_BL(self):
		new_object = []

		for degree in self.get_items():
			scale_steps = Utilities.pitch_class_to_scale_steps(degree.getitem_BL(slice(None, None, None)).get_intervals())

			if scale_steps == scale_steps[::-1]: new_object.append(degree.get_position_BL())

		return new_object 

	def get_interval_vector_BL(self, p_system = DEFAULT_SYSTEM):
		all_intervals = []

		for degree in self.get_items(): 
			all_intervals = all_intervals + degree.getitem_BL(slice(None, None, None)).get_intervals()[1:]

		all_pitch_classes = []

		for interval in all_intervals:
			semitones = interval.get_semitones_BL()

			if semitones > 11: semitones = semitones - 12
			
			all_pitch_classes.append(INTERVAL_SPECTRUM[p_system][semitones])

		counter = collections.Counter(all_pitch_classes)
		new_object = {}

		for key in counter.keys(): 
			new_object[key] = int(counter[key]/2)

		return new_object

	def is_chiral_BL(self, p_intervals):
		reflection_scale_steps = Utilities.pitch_class_to_scale_steps(p_intervals)[::-1]
		new_object = []

		for rotation_ammount in len(p_intervals):
			rotation_pitch_class = Utilities.invert_static(p_intervals, rotation_ammount + 1)
			rotation_scale_steps = Utilities.pitch_class_to_scale_steps(rotation_pitch_class)

			if rotation_scale_steps == reflection_scale_steps: return False

		return True

	def get_cohemitonic_BL(self, p_intervals):
		new_object = []
		scale_steps = Utilities.pitch_class_to_scale_steps(p_intervals) * 2

		for i in range(int(len(scale_steps) / 2)):
			if scale_steps[i] == 1 and scale_steps[i + 1] == 1: 
				new_object.append(i + 1)

		return new_object

	def get_prime_mode_BL(self, p_consider_negative_modes = False):
		min_count = 1000

		for degree in self.get_items():
			new_scale = degree.getitem_BL(slice(None, None, None))
			temp_sum = sum([item.get_semitones_BL() for item in new_scale.get_intervals()])

			if temp_sum < min_count:
				prime_mode = new_scale
				min_count = temp_sum
			
			if p_consider_negative_modes:
				new_scale = new_scale.get_negative()
				temp_sum = sum([item.get_semitones_BL() for item in new_scale.get_intervals()])

				if temp_sum < min_count:
					prime_mode = new_scale
					min_count = temp_sum

		return new_scale

	###################
	# Wrapper Methods #
	###################

	def get_name(self): 
		return self.get_name_BL()

	def get_mode_names(self): 
		return self.get_mode_names_BL()

	def get_hemitonia(self): 
		return self.get_hemitonia_BL()

	def get_tritonia(self): 
		return self.get_tritonia_BL()

	def get_cardinality(self, p_system = DEFAULT_SYSTEM): 
		return self.get_cardinality_BL(p_system)

	def has_cohemitonia(self): 
		return self.has_cohemitonia_BL()

	def is_prime(self): 
		return self.is_prime_BL()

	def count_intervals(self, p_interval_size):
		return self.count_intervals_BL(p_interval_size)

	def get_imperfections(self):
		return self.get_imperfections_BL()

	def get_rotational_symmetry(self):
		return self.get_rotational_symmetry_BL()

	def get_reflection_axes(self):
		return self.get_reflection_axes_BL()

	def get_interval_vector(self, p_system = DEFAULT_SYSTEM):
		return self.get_interval_vector_BL(p_system)

	def is_chiral(self, p_intervals):
		return self.is_chiral_BL(p_intervals)

	def get_cohemitonic(self, p_intervals):
		return self.get_cohemitonic_BL(p_intervals)

	def get_prime_mode(self, p_consider_negative_modes = False):
		return self.get_prime_mode_BL(p_consider_negative_modes)

	#####################################
	# Overridden Business Logic Methods #
	#####################################
	
	def build_items(self, p_intervals, p_type_dict):
		self.items = []

		for i in range(len(p_intervals)):
			self.items.append(type(self).Degree(p_intervals[i], self, **p_type_dict[p_intervals[i]] if p_intervals[i] in p_type_dict.keys() else {}))

	###################
	# Wrapper Methods #
	###################

	def get_name(self): 
		return self.get_name_BL()

	def get_mode_names(self): 
		return self.get_mode_names_BL()

	class Degree(IntervalList.Item):

		#################
		# Sugar Methods #
		#################

		def is_chromatic(self): 
			new_boolean = self.is_altered()
			return new_boolean

		def build_scale(self, *p_args):
			new_interval_list = self.build_interval_list_BL(*p_args)
			return new_interval_list

		def get_parent_scale(self): 
			new_interval_list = self.get_parent_interval_list()
			return new_interval_list

		##########################
		# Business Logic Methods #
		##########################

		def get_name_BL(self, p_system = DEFAULT_SYSTEM): 
			new_string = SCALE_DEGREE_NAMES[p_system][self.get_interval()]
			return new_string

		###################
		# Wrapper Methods #
		###################

		def get_name(self):
			return self.get_name_BL()