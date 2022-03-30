import collections
from theory.config import *
from theory.i_music_object import IMusicObject
from theory.i_pitched_object import IPitchedObject
from theory.interval import Interval
from theory.interval import GenericInterval
from theory.utilities import Utilities
from theory.meta_class import *

class IntervalList(IMusicObject):

	def __init__(self, 
		p_item_1, 
		p_item_2, 
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
			defaults.update(p_item_1.get_attributes())

		p_item_1 = defaults["p_item_1"]
		p_item_2 = defaults["p_item_2"]
		p_unaltered_intervals = defaults["p_unaltered_intervals"]
		p_type_dict = defaults["p_type_dict"]
		p_sublist = defaults["p_sublist"]
		p_altered = defaults["p_altered"]
		p_floor = defaults["p_floor"]
		p_roof = defaults["p_roof"]
		p_direction = defaults["p_direction"]

		parent_item = IntervalList.configure_reference_point(p_item_1)
		intervals = IntervalList.configure_intervals(p_item_1, p_item_2)
		type_dict = p_type_dict

		self.sublist = p_sublist
		self.altered = p_altered

		self.tonic_tone = parent_item.get_reference_point_BL() if isinstance(parent_item, IntervalList.Item) else parent_item
		self.parent_item = IntervalList.configure_parent_item(parent_item, intervals, self.sublist) if isinstance(parent_item, IntervalList.Item) else None

		bounds = IntervalList.configure_bounds(p_floor, p_roof, p_direction, intervals)

		self.direction = p_direction
		self.floor = bounds["floor"]
		self.roof = bounds["roof"]
		
		self.unaltered_intervals = IntervalList.configure_unaltered_intervals(intervals, p_unaltered_intervals, self.sublist, self.parent_item, (self.roof - self.floor))
	
		self.derived_attributes = {}
		self.build_items(intervals, type_dict)

	##################
	# Object Methods #
	##################

	# Representation #

	#@hashable_lru
	def play_BL(self):
		return

	#@hashable_lru
	def to_midi_data_BL(self): 
		try: return self.get_items()
		except: print("Error: Unable to convert object to midi data as it does not contain playable objects")

	#def to_json(self):

	def from_json(self, p_json):
		new_interval_list = Empty()
		new_interval_list.__class__ = type(self)

		for (key, value) in p_json:
			setattr(new_interval_list, key, from_json(value))

		return new_interval_list
	
	def deepcopy_BL(self, p_memo):
		new_interval_list = type(self)(**self.get_attributes())
		return new_interval_list

	def hash_BL(self): 
		new_hash = hash((self.tonic_tone,
						make_hash(self.parent_item),
						make_hash(self.get_type_dict()),
						make_hash(self.unaltered_intervals),
						self.sublist,
						self.altered,
						self.floor,
						self.roof,
						self.direction))
		return new_hash

	#@hashable_lru
	def repr_BL(self): 
		new_string = self.str_BL()
		return new_string

	#@hashable_lru
	def str_BL(self):
		new_string = "<" + type(self).__name__ + " "

		for item in self.get_items(): 
			new_string += str(item) + ", "

		new_string = new_string[:-2] + ">"
		return new_string

	# Comparison #

	def eq_BL(self, p_other): 
		new_boolean = type(self) == type(p_other) and self.get_tonic_tone() == p_other.get_tonic_tone() and self.get_intervals() == p_other.get_intervals() and self.get_attributes() == p_other.get_attributes()
		return new_boolean

	def ne_BL(self, p_other): 
		new_boolean = not self.eq_BL(p_other)
		return new_boolean

	# Arithmetic #

	def radd_BL(self, p_other, *p_args):
		if isinstance(p_other, str):
			new_object = p_other.__add__(self, *p_args)
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

	#@hashable_lru
	def add_BL(self, p_other, p_generic_interval_args = {}, p_args = {}):
		if isinstance(p_other, str): 
			new_string = str(self) + p_other
			return new_string

		if isinstance(p_other, int): 
			new_interval_list = self.transpose_BL(p_other)
			return new_interval_list

		if isinstance(p_other, Interval): 
			if self.get_parent_item() != None:
				new_parent_interval_list = self.get_parent_item().get_parent_interval_list().add_BL(p_other, p_generic_interval_args)
				new_reference_point = new_parent_interval_list.get_items()[self.get_reference_item_BL().get_position_in_parent_BL() - 1]

			else: new_reference_point = self.get_tonic_tone() + p_other

			new_args = self.get_attributes()
			new_args.update(p_args)

			new_args["p_item_1"] = new_reference_point

			new_interval_list = type(self)(**new_args)
			return new_interval_list

		if issubclass(type(p_other), IntervalList.Item):
			delta = p_other.get_parent_interval_list().get_tonic_tone() - self.get_tonic_tone()

			if self.get_parent_item() is not None:
				new_reference_point = self.get_parent_item()

			else: new_reference_point = self.get_tonic_tone()

			new_intervals = self.get_intervals() + [p_other.get_interval() + delta]
			new_intervals = Utilities.sort_intervals(new_intervals)

			new_args = self.get_attributes()
			new_args.update(p_args)

			new_args["p_item_1"] = new_reference_point
			new_args["p_item_2"] = new_intervals
			new_args["p_type_dict"] = Utilities.intervals_to_type_dict(new_intervals)

			new_interval_list = type(self)(**new_args)
			return new_interval_list
		
		if issubclass(type(p_other), IntervalList):
			if len(p_other.get_intervals()) == 1: 
				new_interval_list = self.add_BL(p_other.get_items()[0])
				return new_interval_list

			new_interval_list = self.add_BL(p_other.get_items()[0], p_generic_interval_args).add_BL(p_other.remove_BL(1), p_generic_interval_args)
			return new_interval_list

	#@hashable_lru
	def sub_BL(self, p_other, p_generic_interval_args = {}, p_args = {}):
		if isinstance(p_other, int): 
			return self.add_BL(-p_other, p_generic_interval_args)
			
		elif isinstance(p_other, Interval): 
			return self.add_BL(-p_other, p_generic_interval_args)

	def mul_BL(self, p_other):
		print("Error: Mulitplication for " + str(type(self))+ " has not been implemented")
		return -1

	def div_BL(self, p_other):
		print("Error: Division for " + str(type(self))+ " has not been implemented")
		return -1

	# List %

	def getitem_BL(self, p_index, p_generic_interval_args = {}, p_preserve_parent = False, p_bi_directional = False): 
		new_object = self.get_reference_item_BL().getitem_BL(p_index, p_generic_interval_args, p_preserve_parent, p_bi_directional)
		return new_object

	def contains_BL(self, p_other):
		if isinstance(p_other, IPitchedObject): 
			new_boolean = p_other.simplify_BL() in [item.simplify_BL() for item in self.get_reference_points_BL()]
			return new_boolean

		elif isinstance(p_other, Tone): 
			new_boolean = p_other.simplify_BL() in [item.simplify_BL() for item in self.get_tones_BL()]
			return new_boolean

		elif isinstance(p_other, int): 
			new_boolean = Interval.get_simple_numeral_BL(p_other) in [item.get_numeral() for item in self.get_intervals()]
			return new_boolean

		elif isinstance(p_other, Interval): 
			new_boolean = any(p_other.simplify_BL() in Utilities.simplify_intervals(elem.getitem_BL(slice(None, None, None)).get_intervals()) for elem in self.get_items())
			return new_boolean
			
		elif isinstance(p_other, list) and len(p_other) > 0 and isinstance(p_other[0], Interval): 
			new_boolean = any(all(item.getitem_BL(slice(None, None, None)).contains_BL(elem) for elem in p_other) for item in self.get_items())
			return new_boolean

		elif issubclass(type(p_other), IntervalList.Item): 
			new_boolean = self.contains_BL(p_other.get_tone_BL())
			return new_boolean

		elif issubclass(type(p_other), IntervalList): 
			new_boolean = all(self.contains_BL(elem) for elem in p_other.get_tones_BL())
			return new_boolean

		return False

	#########################
	# Configuration Methods #
	#########################

	@staticmethod
	def configure_bounds(p_floor, p_roof, p_direction, p_intervals):
		new_dict = {}

		if p_floor is not None and IntervalList.within_lower_limit_static(p_intervals[0], p_floor, p_direction):
			new_dict["floor"] = p_floor

		else: new_dict["floor"] = p_intervals[0].floor() if not (p_intervals[0] == P1 and IntervalList.within_lower_limit_static(P1, P1, p_direction)) else P1

		if p_roof is not None and IntervalList.within_upper_limit_static(p_intervals[-1], p_roof, p_direction):
			new_dict["roof"] = p_roof
			
		else: new_dict["roof"] = p_intervals[-1].roof() if not (p_intervals[-1] == P1 and IntervalList.within_upper_limit_static(P1, P1, p_direction)) else P1

		return new_dict

	@staticmethod
	def configure_unaltered_intervals(p_intervals, p_unaltered_intervals, p_sublist, p_parent_item, p_roof):
		if p_sublist and p_parent_item is not None:
			new_list = Utilities.derive_unaltered_intervals_from_parent(p_parent_item, p_roof)
			return new_list

		elif p_unaltered_intervals is not None:
			new_list = Utilities.get_valid_unaltered_intervals(p_intervals, p_unaltered_intervals)
			return new_list

		else:
			new_list = Utilities.get_valid_unaltered_intervals(p_intervals, [])
			return new_list

	@staticmethod
	def configure_parent_item(p_item, p_intervals, p_sublist):
		new_interval_list = p_item.get_parent_interval_list()

		if p_sublist:
			for interval in p_intervals:
				interval_in_parent = (p_item.get_interval() + interval)

				while not new_interval_list.within_upper_limit(interval_in_parent):
					interval_in_parent -= new_interval_list.get_fixed_invert_BL()

				while not new_interval_list.within_lower_limit(interval_in_parent):
					interval_in_parent += new_interval_list.get_fixed_invert_BL()

				if interval_in_parent not in new_interval_list.get_intervals():
					new_interval_list = new_interval_list.add_interval_BL(interval_in_parent, p_attributes = {"p_temp": True})
				
			new_item = new_interval_list.get_item_by_interval(p_item.get_interval())
			return new_item
		
		else: return p_item

	def set_parent_item(self, p_item): 
		if p_item == None: return
		self.parent_item = self.configure_parent_item(p_item, self.get_intervals())

	@staticmethod
	def configure_intervals(p_item_1, p_item_2):
		if issubclass(type(p_item_1), IntervalList):
			new_list = p_item_1.get_intervals()
			return new_list

		elif isinstance(p_item_1, list) and len(p_item_1) > 0 and (isinstance(p_item_1[0], IPitchedObject) or isinstance(p_item_1[0], Tone)):
			new_list = [item - p_item_1[0] for item in p_item_1]
			return new_list

		elif isinstance(p_item_2, list) and len(p_item_2) > 0 and isinstance(p_item_2[0], int):
			new_list = Utilities.scale_steps_to_pitch_class(p_item_2)
			return new_list

		else: 
			new_list = p_item_2
			return new_list

	@staticmethod
	def configure_reference_point(p_item_1):
		if isinstance(p_item_1, Tone):
			new_reference_point = Key(p_item_1, 4)
			return new_reference_point
		
		elif isinstance(p_item_1, IPitchedObject):
			new_reference_point = p_item_1
			return new_reference_point
		
		elif isinstance(p_item_1, IntervalList.Item):
			new_reference_point = p_item_1
			return new_reference_point

		elif issubclass(type(p_item_1), IntervalList):
			new_reference_point = p_item_1.get_parent_item()
			return new_reference_point

		elif isinstance(p_item_1, list) and len(p_item_1) > 0 and isinstance(p_item_1[0], IPitchedObject):
			new_reference_point = p_item_1[0]
			return new_reference_point

		elif isinstance(p_item_1, list) and len(p_item_1) > 0 and isinstance(p_item_1[0], Tone):
			new_reference_point = Key(p_item_1[0], 4)
			return new_reference_point

		else: return None

	##################
	# Static Methods #
	##################

	@staticmethod
	#@hashable_lru
	def within_lower_limit_static(p_other, p_floor, p_direction):
		greater_than_floor = p_other.get_numeral() > p_floor.get_numeral()
		equal_to_floor = p_other.get_numeral() == p_floor.get_numeral() or (abs(p_other.get_numeral()) == 1 and abs(p_floor.get_numeral()) == 1)
		new_boolean = greater_than_floor or (equal_to_floor and p_direction == 1)
		return new_boolean

	@staticmethod
	#@hashable_lru
	def within_upper_limit_static(p_other, p_roof, p_direction):
		less_than_roof = p_other.get_numeral() < p_roof.get_numeral()
		equal_to_roof = p_other.get_numeral() == p_roof.get_numeral() or (abs(p_other.get_numeral()) == 1 and abs(p_roof.get_numeral()) == 1)
		new_boolean = less_than_roof or (equal_to_roof and p_direction == -1)
		return new_boolean

	##########################
	# Business Logic Methods #
	##########################

	#@hashable_lru
	def print_tones_BL(self):
		new_object = ""

		for tone in self.get_reference_points_BL(): 
			new_object = new_object + str(tone) + ", "

		new_string = "[" + new_object[:-2] + "]"
		return new_string
	
	#@hashable_lru
	def within_lower_limit_BL(self, p_other):
		new_boolean = IntervalList.within_lower_limit_static(p_other, self.get_floor(), self.get_direction())
		return new_boolean

	#@hashable_lru
	def within_upper_limit_BL(self, p_other):
		new_boolean = IntervalList.within_upper_limit_static(p_other, self.get_roof(), self.get_direction())
		return new_boolean

	#@hashable_lru
	def get_fixed_invert_BL(self): 
		new_interval = self.get_roof() - self.get_floor()
		return new_interval

	def get_item_where_BL(self, p_lambda_expression):
		items = [item for item in self.get_items() if p_lambda_expression(item)]
		new_item = items[0] if len(items) > 0 else None
		return new_item

	#@hashable_lru
	def get_item_by_interval_BL(self, p_interval): 
		new_item = self.get_item_where_BL(lambda item: item.get_interval() == p_interval)
		return new_item

	#@hashable_lru
	def get_item_by_numeral_BL(self, p_numeral): 
		new_item = self.get_item_where_BL(lambda item: item.get_interval().get_numeral() == p_numeral)
		return new_item

	def remove_BL(self, p_item_index, p_args = {}):
		new_intervals = self.get_intervals()[:]
		new_intervals.pop(p_item_index - 1)
		
		new_args = self.get_attributes()
		new_args.update(p_args)

		new_args["p_item_2"] = new_intervals
		new_args["p_type_dict"] = Utilities.intervals_to_type_dict(new_intervals)

		new_interval_list = type(self)(**new_args)
		return new_interval_list

	def add_interval_BL(self, p_interval, p_attributes = {}, p_args = {}):
		new_interval = type(self.get_items()[0])(p_interval, None, **p_attributes).get_interval()

		if self.get_parent_item() is not None:
			new_reference_point = self.get_parent_item()
		
		else: new_reference_point = self.get_tonic_tone()

		new_intervals = self.get_intervals()[:]

		if new_interval not in new_intervals:
			new_intervals.append(new_interval)
			new_intervals = Utilities.sort_intervals(new_intervals)

		new_args = self.get_attributes()
		new_args.update(p_args)

		new_args["p_item_1"] = new_reference_point
		new_args["p_item_2"] = new_intervals
		new_args["p_type_dict"] = Utilities.intervals_to_type_dict(new_intervals)

		new_interval_list = type(self)(**new_args)
		return new_interval_list

	def replace_at_numeral_with_BL(self, p_numeral, p_interval, p_args = {}):
		if self.get_parent_item() is not None:
			new_reference_point = self.get_parent_item()

		else: new_reference_point = self.get_tonic_tone()

		new_intervals = [item if item.get_numeral() != p_numeral else p_interval for item in self.get_intervals()]
		
		new_args = self.get_attributes()
		new_args.update(p_args)

		new_args["p_item_1"] = new_reference_point
		new_args["p_item_2"] = new_intervals
		new_args["p_type_dict"] = Utilities.intervals_to_type_dict(new_intervals)

		new_interval_list = type(self)(**new_args)
		return new_interval_list

	#@hashable_lru
	def flip_axis_BL(self, p_args = {}):
		new_args = self.get_attributes()
		new_args.update(p_args)

		new_args["p_item_2"] = self.getitem_BL(slice(None, None, 2 * self.get_direction() * -1), p_generic_interval_args = {"p_ignore_parent": None, "p_cascade_args": False, "p_ignore_altered": False, "p_remove_temp": True}, p_bi_directional = True).get_intervals()
		new_args["p_floor"] = self.get_floor() * -1
		new_args["p_roof"] = self.get_roof() * -1
		new_args["p_direction"] = self.get_direction() * -1

		new_interval_list = type(self)(**new_args)
		return new_interval_list

	#@hashable_lru
	def get_relative_BL(self, p_reflection_point = 5, p_args = {}):
		parallel_interval_list = self.get_parallel_BL(p_reflection_point, p_args)
		
		if self.is_sublist():
			modes = self.get_parent_interval_list().getModes()
			parallel_intervals = Utilities.simplify_intervals(parallel_interval_list.get_parent_interval_list().get_intervals())
			
		else: 
			modes = self.getModes()
			parallel_intervals = parallel_interval_list.get_intervals()

		relative_modes = [mode for mode in modes if all(item in mode.get_intervals() for item in parallel_intervals)]

		if len(relative_modes) > 0:
			new_args = parallel_interval_list.get_attributes()
			new_args.update(p_args)

			new_args["p_item_1"] = relative_modes[0].get_reference_item_BL()

			new_interval_list = type(parallel_interval_list)(**new_args)
			return new_interval_list

		else: 
			print("Error: Scale has no reflection axis, relative Scale could not be found")
			return -1

	#@hashable_lru
	def get_parallel_BL(self, p_reflection_point = 5, p_args = {}):
		if self.is_sublist():
			parallel_parent = self.get_parent_item().get_parent_interval_list().get_parallel(p_reflection_point)
			parallel_parent_shifted = parallel_parent.get_items()[self.get_items()[0].get_position_in_parent() - 1].getitem_BL(slice(None, None, None))

			new_args = self.get_attributes()
			new_args.update(p_args)

			new_args["p_item_1"] = parallel_parent.get_items()[(self.get_items()[0].get_position_in_parent()) - 1]
			new_args["p_item_2"] = parallel_parent_shifted.getitem_BL(tuple([GenericInterval(item.get_numeral(), -item.get_interval()) for item in self.get_generic_intervals_BL()])).get_intervals()

			new_interval_list = type(self)(**new_args)
			return new_interval_list

		else:
			negative = self.get_negative_BL(p_reflection_point, p_args)
			negative = negative.flip_axis_BL()

			new_interval_list = negative.add_BL(-p_reflection_point)
			return new_interval_list

	#@hashable_lru
	def get_negative_BL(self, p_reflection_point = 5, p_args = {}): 
		if self.get_parent_item() is not None:
			parent_interval_list = self.get_parent_item().get_parent_interval_list()
			new_reference_point = parent_interval_list.get_parallel_BL(p_reflection_point).get_items()[self.get_parent_item().get_position() - 1].add_BL(p_reflection_point)

		else: new_reference_point = self.getitem_BL(p_reflection_point).get_reference_point_BL()	

		new_intervals = Utilities.invert_intervals(self.get_intervals())
		new_unaltered_intervals = Utilities.invert_intervals(self.get_unaltered_intervals())
		new_unaltered_intervals = Utilities.simplify_intervals(new_unaltered_intervals)
		new_unaltered_intervals = Utilities.sort_intervals(new_unaltered_intervals)

		new_args = self.get_attributes()
		new_args.update(p_args)

		new_args["p_item_1"] = new_reference_point
		new_args["p_item_2"] = new_intervals
		new_args["p_unaltered_intervals"] = new_unaltered_intervals
		new_args["p_type_dict"] = Utilities.intervals_to_type_dict(new_intervals)
		new_args["p_floor"] = new_intervals[0].floor() if not (new_intervals[0] == P1 and IntervalList.within_lower_limit_static(P1, P1, self.get_direction() * -1)) else P1
		new_args["p_roof"] = new_intervals[-1].roof() if not (new_intervals[-1] == P1 and IntervalList.within_upper_limit_static(P1, P1, self.get_direction() * -1)) else P1
		new_args["p_direction"] = self.get_direction() * -1

		new_interval_list = type(self)(**new_args)
		return new_interval_list

	#@hashable_lru
	def rotate_BL(self, p_other = 2, p_generic_interval_args = {"p_ignore_parent": True, "p_cascade_args": False, "p_ignore_altered": False, "p_remove_temp": True}, p_preserve_parent = True):
		new_reference_point = self.get_reference_item_BL().add_BL(p_other, p_generic_interval_args)
		new_interval_list = new_reference_point.getitem_BL(slice(None, None, None), p_generic_interval_args, p_preserve_parent)
		return new_interval_list

	#@hashable_lru
	def transpose_BL(self, p_other = 2, p_generic_interval_args = {}, p_preserve_parent = True, p_sublist = True, p_args = {}):
		new_reference_point = self.get_reference_item_BL().add_BL(p_other, p_generic_interval_args)

		new_args = self.get_attributes()
		new_args.update(p_args)

		new_args["p_item_1"] = new_reference_point
		new_args["p_item_2"] = new_reference_point.getitem_BL(tuple(self.get_generic_intervals_BL(p_generic_interval_args)), p_generic_interval_args, p_preserve_parent).get_intervals()
		new_args["p_sublist"] = p_sublist

		new_interval_list = type(self)(**new_args)
		return new_interval_list

	#@hashable_lru
	def get_generic_intervals_BL(self, p_generic_interval_args = {}):
		new_list = [item.get_generic_interval_BL(**p_generic_interval_args) for item in self.get_items()]
		return new_list

	#@hashable_lru
	def get_intervals_where_BL(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = False, p_remove_temp = True): 
		ignore_parent = p_ignore_parent if p_ignore_parent is not None else not self.is_sublist()

		if not ignore_parent:
			new_list = self.get_parent_item().getitem_BL(slice(None, None, None)).get_intervals() if not p_cascade_args else self.get_parent_item().getitem_BL(slice(None, None, None), p_generic_interval_args).get_intervals()
			return new_list

		new_list = [item.get_interval() for item in self.get_items() if (item.is_un_altered_BL() or (not p_ignore_altered))]
		return new_list

	##@hashable_lru
	def get_intervals_BL(self): 
		new_list = [item.get_interval() for item in self.get_items()]
		return new_list

	#@hashable_lru
	def get_numerals_BL(self): 
		new_list = [item.get_numeral() for item in self.get_intervals()]
		return new_list

	#@hashable_lru
	def get_semitones_BL(self): 
		new_list = [item.get_semitones() for item in self.get_intervals()]	
		return new_list

	#@hashable_lru
	def get_tones_BL(self):
		new_list = [item.get_tone_BL() for item in self.get_reference_points_BL()]
		return new_list

	#@hashable_lru
	def get_reference_points_BL(self): 
		new_list = [item.get_reference_point_BL() for item in self.get_items()]
		return new_list

	#@hashable_lru
	def get_reference_point_position_BL(self):
		new_list = P1 - self.get_items()[0].get_interval()
		return new_list

	#@hashable_lru
	def get_reference_item_BL(self):
		if P1 in self.get_intervals():
			new_reference_item = self.get_item_where_BL(lambda item: (abs(item.get_interval()) == P1))

		else: new_reference_item = self.add_interval_BL(P1).get_item_where_BL(lambda item: item.get_interval() == P1)
		return new_reference_item

	def get_parent_interval_list_BL(self): 
		new_interval_list = self.get_parent_item().get_parent_interval_list()
		return new_interval_list

	def build_items(self, p_intervals, p_type_dict):
		self.items = []

		for i in range(len(p_intervals)):
			self.items.append(IntervalList.Item(p_intervals[i], self, **p_type_dict[p_intervals[i]] if p_intervals[i] in p_type_dict.keys() else {}))

	def get_attributes(self):
		new_dict = {
			"p_item_1": self.get_tonic_tone() if self.get_parent_item() is None else self.get_parent_item(),
			"p_item_2": [item.get_interval() for item in self.get_items()],
			"p_unaltered_intervals": self.get_unaltered_intervals(),
			"p_type_dict": self.get_type_dict(),
			"p_sublist": self.is_sublist(),
			"p_altered": self.is_altered(),
			"p_floor": self.get_floor(),
			"p_roof": self.get_roof(),
			"p_direction": self.get_direction()
		}

		return new_dict

	def get_type_dict(self): 
		temp_type_dict = {}
		
		for item in self.get_items():
			temp_type_dict[item.get_interval()] = item.get_attributes()

		new_dict = temp_type_dict
		return new_dict

	###################
	# Wrapper Methods #
	###################

	# Representation #

	def __play__(self):
		return self.play_BL()

	def __to_midi_data__(self): 
		return self.to_midi_data_BL()

	def __deepcopy__(self, p_memo):
		return self.deepcopy_BL(p_memo)

	def __repr__(self): 
		return self.repr_BL()

	def __hash__(self):
		print("test")
		return self.hash_BL()

	def __str__(self): 
		return self.str_BL()

	def __eq__(self, p_other): 
		return self.eq_BL(p_other)
		
	def __ne__(self, p_other): 
		return self.ne_BL(p_other)

	def __radd__(self, p_other, *p_args):
		return self.radd_BL(p_other, *p_args)

	def __rsub__(self, p_other, *p_args):
		return self.rsub_BL(p_other, *p_args)

	def __rmul__(self, p_other, *p_args):
		return self.rmul_BL(p_other, *p_args)

	def __rdiv__(self, p_other, *p_args):
		return self.rdiv_BL(p_other, *p_args)

	def __add__(self, p_other, p_generic_interval_args = {}, p_args = {}): 
		return self.add_BL(p_other, p_generic_interval_args, p_args)

	def __sub__(self, p_other, p_generic_interval_args = {}, p_args = {}): 
		return self.sub_BL(p_other, p_generic_interval_args, p_args)

	def __mul__(self, p_other, *p_args):
		return self.mul_BL(p_other, *p_args)

	def __div__(self, p_other, *p_args):
		return self.div_BL(p_other, *p_args)
		
	def __getitem__(self, p_index, p_generic_interval_args = {}, p_preserve_parent = False, p_bi_directional = False): 
		return self.getitem_BL(p_index, p_generic_interval_args, p_preserve_parent, p_bi_directional)

	def __contains__(self, p_other): 
		return self.contains_BL(p_other)
	
	def print_tones(self): 
		return self.print_tones_BL()

	def within_lower_limit(self, p_other):
		return self.within_lower_limit_BL(p_other)

	def within_upper_limit(self, p_other):
		return self.within_upper_limit_BL(p_other)

	def get_fixed_invert(self):
		return self.get_fixed_invert_BL()

	def get_item_where(self, p_lambda_expression): 
		return self.get_item_where_BL(p_lambda_expression)

	def get_item_by_interval(self, p_interval): 
		return self.get_item_by_interval_BL(p_interval)

	def get_item_by_numeral(self, p_numeral): 
		return self.get_item_by_numeral_BL(p_numeral)

	def remove(self, p_item_index, p_args = {}): 
		return self.remove_BL(p_item_index, p_args)

	def add_interval(self, p_interval, p_attributes = {}, p_args = {}): 
		return self.add_interval_BL(p_interval, p_attributes, p_args)

	def replace_at_numeral_with(self, p_numeral, p_interval, p_args = []): 
		return self.replace_at_numeral_with_BL(p_numeral, p_interval, p_args)

	def flip_axis(self, p_args = {}):
		return self.flip_axis_BL(p_args)

	def get_relative(self, p_reflection_point = 5, p_args = {}):
		return self.get_relative_BL(p_reflection_point, p_args)

	def get_parallel(self, p_reflection_point = 5, p_args = {}): 
		return self.get_parallel_BL(p_reflection_point, p_args)

	def get_negative(self, p_reflection_point = 5, p_args = {}):
		return self.get_negative_BL(p_reflection_point, p_args)
		
	def rotate(self, p_other = 2, p_generic_interval_args = {"p_ignore_parent": True, "p_cascade_args": False, "p_ignore_altered": False, "p_remove_temp": True}, p_preserve_parent = True): 
		return self.rotate_BL(p_other, p_generic_interval_args, p_preserve_parent)
		
	def transpose(self, p_other = 2, p_generic_interval_args = {}, p_preserve_parent = True, p_sublist = True, p_args = {}): 
		return self.transpose_BL(p_other, p_generic_interval_args, p_preserve_parent, p_sublist, p_args)

	def get_generic_intervals(self, p_generic_interval_args = {}): 
		return self.get_generic_intervals_BL(p_generic_interval_args)

	def get_intervals_where(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = False, p_remove_temp = True):
		return self.get_intervals_where_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

	def get_intervals(self): 
		return self.get_intervals_BL()

	def get_numerals(self): 
		return self.get_numerals_BL()

	def get_semitones(self): 
		return self.get_semitones_BL()

	def get_tones(self): 
		return self.get_tones_BL()

	def get_reference_points(self): 
		return self.get_reference_points_BL()

	def get_reference_point_position(self):
		return self.get_reference_point_position_BL()	

	def get_reference_item(self):
		return self.get_reference_item_BL()

	def get_parent_interval_list(self): 
		return self.get_parent_interval_list_BL()

	#######################
	# Getters and Setters #
	#######################

	def get_items(self): 
		return self.items
		
	def get_tonic_tone(self): 
		return self.tonic_tone

	def get_unaltered_intervals(self): 
		return self.unaltered_intervals

	def is_sublist(self): 
		return self.sublist

	def is_altered(self): 
		return self.altered

	def get_floor(self):
		return self.floor

	def get_roof(self):
		return self.roof

	def get_direction(self):
		return self.direction
		
	def get_parent_item(self): 
		return self.parent_item

	def set_items(self, p_items): 
		self.items = p_items

	def set_tonic_tone(self, p_tonic_tone): 
		self.tonic_tone = p_tonic_tone

	def set_unaltered_intervals(self, p_unaltered_intervals): 
		self.unaltered_intervals = p_unaltered_intervals

	def set_sublist(self, p_sublist): 
		self.sublist = p_sublist

	def set_altered(self, p_chromatic): 
		self.altered = p_altered

	def set_floor(self, p_floor):
		self.floor = p_floor

	def set_roof(self, p_roof):
		self.roof = p_roof

	def set_direction(self, p_direction):
		self.direction = p_direction

	class Item:
		
		def __init__(self, p_interval, p_parent_interval_list, p_temp = False):
			new_interval = Interval(p_interval.get_semitones(), p_interval.get_numeral(), self)
			self.interval = new_interval
			self.parent_interval_list = p_parent_interval_list
			self.temp = p_temp

		##################
		# Object Methods #
		##################

		def getattr_BL(self, p_attr):
			if hasattr(self.get_reference_point_BL(), p_attr): 
				return getattr(self.get_reference_point_BL(), p_attr)

			elif hasattr(self.get_interval(), p_attr): 
				return getattr(self.get_interval(), p_attr)

		# Representation #

		def deepcopy_BL(self, p_memo):
			new_interval_list = self.get_parent_interval_list().deepcopy_BL(p_memo)
			new_item = [item for item in new_interval_list.get_items() if item.get_interval() == self.get_interval()][0]
			return new_item

		def hash_BL(self): 
			new_hash = hash((make_hash(self.get_parent_interval_list().get_attributes()),
							self.get_interval().hash_BL(),
							self.is_temp()))
			return new_hash

		#@hashable_lru
		def repr_BL(self): 
			new_string = self.str_BL()
			return new_string

		#@hashable_lru
		def str_BL(self):
			if not DEGREE_SIMPLE_REPRESENTATION:
				new_string = self.get_numeral_notation_BL() + ": " + str(self.get_reference_point_BL())
				return new_string

			else:
				new_string = str(self.get_reference_point_BL())
				return new_string

		# Comparison #

		def eq_BL(self, p_other): 
			new_boolean = type(self) == type(p_other) and self.get_interval() == p_other.get_interval() and self.get_parent_interval_list() == p_other.get_parent_interval_list() and self.get_attributes() == p_other.get_attributes()
			return new_boolean

		def ne_BL(self, p_other): 
			new_boolean = not self.eq_BL(p_other)
			return new_boolean

		# Arithmetic #

		def radd_BL(self, p_other, *p_args):
			if isinstance(p_other, str):
				new_object = p_other.__add__(self, *p_args)
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

		#@hashable_lru
		def add_BL(self, p_other, p_generic_interval_args = {"p_ignore_parent": None, "p_cascade_args": False, "p_ignore_altered": True, "p_remove_temp": True}, p_args = {}):
			if isinstance(p_other, str):
				new_string = str(self) + p_other
				return new_string

			if isinstance(p_other, int):	
				if abs(p_other) == 1:
					new_item = self
					return new_item

				elif p_other > 0: 
					new_item = self.next_BL(**p_generic_interval_args).add_BL(p_other - 1, p_generic_interval_args)
					return new_item
				
				else: 
					new_item = self.previous_BL(**p_generic_interval_args).add_BL(p_other + 1, p_generic_interval_args)
					return new_item
			
			if isinstance(p_other, list) and len(p_other) > 0 and (isinstance(p_other[0], Interval) or isinstance(p_other[0], int)):
				if len(p_other) == 1: 
					new_item = self.add_BL(p_other[0])
					return new_item

				new_item = self.add_BL(p_other[0]).add_BL(p_other[1:])
				return new_item
			
			if isinstance(p_other, Interval):
				if abs(p_other) == P1: 
					new_item = self
					return new_item

				new_interval = self.get_interval() + p_other

				if not self.get_parent_interval_list().within_lower_limit_BL(new_interval):
					new_item = (self.get_parent_interval_list().add_BL(-self.get_parent_interval_list().get_fixed_invert_BL(), p_generic_interval_args)).get_items()[self.get_position_BL() - 1].add_BL(p_other + self.get_parent_interval_list().get_fixed_invert_BL(), p_generic_interval_args)
					return new_item
				
				if not self.get_parent_interval_list().within_upper_limit_BL(new_interval):
					new_item = (self.get_parent_interval_list().add_BL(self.get_parent_interval_list().get_fixed_invert_BL(), p_generic_interval_args)).get_items()[self.get_position_BL() - 1].add_BL(p_other - self.get_parent_interval_list().get_fixed_invert_BL(), p_generic_interval_args)
					return new_item

				if new_interval not in self.get_parent_interval_list().get_intervals():
					new_item = self.get_parent_interval_list().add_interval_BL(new_interval, {"p_temp": True}, p_args).get_item_by_interval(new_interval)
					return new_item

				else: 
					new_item = self.get_parent_interval_list().get_item_by_interval(new_interval)
					return new_item

			if isinstance(p_other, GenericInterval):
				generic_portion = self.add_BL(p_other.get_numeral(), p_generic_interval_args, p_args)
				new_item = generic_portion.add_BL(p_other.get_interval(), p_generic_interval_args, p_args)
				return new_item

			if issubclass(type(p_other), IntervalList.Item):
				delta = p_other.get_parent_interval_list().get_tonic_tone() - self.get_parent_interval_list().get_tonic_tone()
				new_reference_point = self

				new_intervals = [self.get_interval(), p_other.get_interval() + delta] if self != p_other else [self.get_interval()]
				new_intervals = Utilities.sort_intervals(new_intervals)
				
				new_args = self.get_parent_interval_list().get_attributes()
				new_args.update(p_args)

				new_args["p_item_1"] = new_reference_point
				new_args["p_item_2"] = new_intervals
				new_args["p_type_dict"] = Utilities.intervals_to_type_dict(new_intervals)

				new_interval_list = type(self.get_parent_interval_list())(**new_args)
				return new_interval_list

			if issubclass(type(p_other), IntervalList):
				new_reference_point = self.add_BL(p_other.get_reference_item_BL(), p_generic_interval_args)
				new_interval_list = new_reference_point.add_BL(p_other.remove_BL(1), p_generic_interval_args)
				return new_interval_list

		#@hashable_lru
		def sub_BL(self, p_other, p_generic_interval_args = {"p_ignore_parent": None, "p_cascade_args": False, "p_ignore_altered": True, "p_remove_temp": True}, p_args = {}):
			if isinstance(p_other, int):
				return self.add_BL(-p_other, p_generic_interval_args, p_args)

			if isinstance(p_other, Interval):
				return self.add_BL(-p_other, p_generic_interval_args, p_args)

			if isinstance(p_other, GenericInterval):
				return self.add_BL(-p_other, p_generic_interval_args, p_args)

			if issubclass(type(p_other), IntervalList.Item):
				if not self.is_un_altered_BL(): 
					new_numeral = self.resolve_BL().sub_BL(p_other, p_generic_interval_args).get_numeral()
					new_interval = self.get_alteration_BL()
					new_generic_interval = GenericInterval(new_numeral, new_interval)
					return new_generic_interval

				new_intervals = self.get_parent_interval_list().get_intervals_where_BL(**p_generic_interval_args)

				if P1 not in new_intervals:
					new_intervals += [P1]
					new_intervals = Utilities.sort_intervals(new_intervals)
				
				temp_interval_list = self.get_parent_interval_list()
				temp_boolean = lambda x: x.is_sublist() or p_generic_interval_args["p_ignore_parent"] == False

				while temp_boolean(temp_interval_list) or temp_interval_list.get_parent_item() is not None:
					temp_interval_list = temp_interval_list.get_parent_item().get_parent_interval_list()

					if p_generic_interval_args["p_cascade_args"] is not None and p_generic_interval_args["p_cascade_args"]:
						temp_boolean = lambda x: False

				new_roof = temp_interval_list.get_roof()
				new_floor = temp_interval_list.get_floor()
				new_fixed_invert = temp_interval_list.get_fixed_invert_BL()
				new_interval = self.get_reference_point_BL() - p_other.get_parent_interval_list().get_reference_item_BL().get_reference_point()

				while not IntervalList.within_upper_limit_static(new_interval, new_roof, p_other.get_parent_interval_list().get_direction()):
					new_intervals += [item + new_fixed_invert for item in new_intervals]
					new_roof += new_fixed_invert
					new_fixed_invert += new_fixed_invert
				
				while not IntervalList.within_lower_limit_static(new_interval, new_floor, p_other.get_parent_interval_list().get_direction()):
					new_intervals = [item - new_fixed_invert for item in new_intervals] + new_intervals
					new_floor -= new_fixed_invert
					new_fixed_invert += new_fixed_invert
					
				reference_point_index = new_intervals.index(p_other.get_interval())
				self_index = new_intervals.index(new_interval)
				new_index = self_index - reference_point_index

				if reference_point_index <= self_index:
					new_index += 1

				else: new_index -= 1
				
				new_generic_interval = GenericInterval(new_index, P1)
				return new_generic_interval

		# List #

		def getitem_BL(self, p_index, p_generic_interval_args = {}, p_preserve_parent = False, p_bi_directional = False, p_args = {}): 
			if isinstance(p_index, slice):
				if p_index.step == P1:
					print("Error: Step cannot be a P1")
					return -1

				if p_index.step is None:
					step = 2 * self.get_parent_interval_list().get_direction()
					sign = self.get_parent_interval_list().get_direction()

				else: 
					step = p_index.step
					sign = int(step / abs(step)) if isinstance(step, int) else step.get_sign_BL()

				if isinstance(p_index.start, int):
					new_item = self.getitem_BL(p_index.start, p_generic_interval_args, p_preserve_parent)
					start = new_item.get_reference_point_BL() - self.get_reference_point_BL()
				
				elif p_index.start is None:
					start = self.get_parent_interval_list().get_floor() if sign == self.get_parent_interval_list().get_direction() else -self.get_parent_interval_list().get_roof()
					
				else: start = p_index.start

				if isinstance(p_index.stop, int):
					new_item = self.getitem_BL(p_index.stop, p_generic_interval_args, p_preserve_parent)
					stop = new_item.get_reference_point_BL() - self.get_reference_point_BL()
				
				elif p_index.stop is None:
					stop = self.get_parent_interval_list().get_roof() if sign == self.get_parent_interval_list().get_direction() else -self.get_parent_interval_list().get_floor()
					
				else: stop = p_index.stop
				
				direction = sign
				new_intervals = []
				sign_neg = sign * -1
				
				if isinstance(step, int):
					if p_bi_directional:
						multiplier = -1
						product = Interval.numeral_mul(step, multiplier)
						new_item = self.getitem_BL(product, p_generic_interval_args, p_preserve_parent)
						new_interval = new_item.get_reference_point_BL() - self.get_reference_point_BL()

						while ((IntervalList.within_lower_limit_static(new_interval, start, direction) and sign_neg == -1) or (IntervalList.within_upper_limit_static(new_interval, stop, direction)) and sign_neg == 1):
							if IntervalList.within_lower_limit_static(new_interval, start, direction) and IntervalList.within_upper_limit_static(new_interval, stop, direction):
								new_intervals.append(new_interval)
							
							multiplier -= 1
							product = Interval.numeral_mul(step, multiplier)
							new_item = self.getitem_BL(product, p_generic_interval_args, p_preserve_parent)
							new_interval = new_item.get_reference_point_BL() - self.get_reference_point_BL()

					multiplier = 0
					product = Interval.numeral_mul(step, multiplier)
					new_item = self.getitem_BL(product, p_generic_interval_args, p_preserve_parent)
					new_interval = new_item.get_reference_point_BL() - self.get_reference_point_BL()

					while ((IntervalList.within_lower_limit_static(new_interval, start, direction) and sign == -1) or (IntervalList.within_upper_limit_static(new_interval, stop, direction)) and sign == 1):
						if IntervalList.within_lower_limit_static(new_interval, start, direction) and IntervalList.within_upper_limit_static(new_interval, stop, direction):
							new_intervals.append(new_interval)
						
						multiplier += 1
						product = Interval.numeral_mul(step, multiplier)
						new_item = self.getitem_BL(product, p_generic_interval_args, p_preserve_parent)
						new_interval = new_item.get_reference_point_BL() - self.get_reference_point_BL()
				else:
					if p_bi_directional:
						multiplier = -1
						new_interval = step.__mul__(multiplier)

						while ((IntervalList.within_lower_limit_static(new_interval, start, direction) and sign_neg == -1) or (IntervalList.within_upper_limit_static(new_interval, stop, direction)) and sign_neg == 1):
							if IntervalList.within_lower_limit_static(new_interval, start, direction) and IntervalList.within_upper_limit_static(new_interval, stop, direction):
								new_intervals.append(new_interval)

							multiplier -= 1
							new_interval = step.__mul__(multiplier)

					multiplier = 0
					new_interval = step.__mul__(multiplier)

					while ((IntervalList.within_lower_limit_static(new_interval, start, direction) and sign == -1) or (IntervalList.within_upper_limit_static(new_interval, stop, direction)) and sign == 1):
						if IntervalList.within_lower_limit_static(new_interval, start, direction) and IntervalList.within_upper_limit_static(new_interval, stop, direction):
							new_intervals.append(new_interval)

						multiplier += 1
						new_interval = step.__mul__(multiplier)

				new_intervals = Utilities.sort_intervals(new_intervals)
				new_interval_list = self.getitem_BL(tuple(new_intervals), p_generic_interval_args, p_preserve_parent)
				return new_interval_list

			elif isinstance(p_index, tuple):
				new_intervals = []

				for item in list(p_index):
					new_reference_point = self.getitem_BL(item, p_generic_interval_args).get_reference_point()
					new_interval = new_reference_point - self.get_reference_point()
					new_intervals.append(new_interval)

				new_reference_point = self if not p_preserve_parent or self.get_parent_interval_list().get_parent_item() is None else self.find_in_parent_BL()
				new_intervals = Utilities.sort_intervals(new_intervals)
				new_unaltered_intervals = Utilities.intervals_relative_to(-self.get_interval(), self.get_parent_interval_list().get_unaltered_intervals(), self.get_parent_interval_list().get_fixed_invert_BL())			
				new_unaltered_intervals = Utilities.simplify_intervals(new_unaltered_intervals)

				new_args = self.get_parent_interval_list().get_attributes()
				new_args.update(p_args)

				new_args["p_item_1"] = new_reference_point
				new_args["p_item_2"] = new_intervals
				new_args["p_unaltered_intervals"] = new_unaltered_intervals
				new_args["p_type_dict"] = Utilities.intervals_to_type_dict(new_intervals)
				new_args["p_sublist"] = True
				new_args["p_floor"] = new_intervals[0].floor()
				new_args["p_roof"] = new_intervals[-1].roof()

				new_interval_list = type(self.get_parent_interval_list())(**new_args)
				return new_interval_list
			
			else: return self.add_BL(p_index, p_generic_interval_args)

		##########################
		# Business Logic Methods #
		##########################

		#@hashable_lru
		def get_numeral_notation_BL(self, p_cascade = False):
			if p_cascade and self.get_parent_interval_list().get_parent_item() is not None:
				return self.find_in_parent_BL().get_numeral_notation_BL(True)

			sign = self.get_parent_interval_list().get_direction()
			numeral = Interval.int_to_roman(abs(self.get_interval().get_numeral()))
			third = self.getitem_BL(tuple([1, 3])) if sign == 1 else self.getitem_BL(tuple([-3, 1]))

			if third.get_intervals() == [P1, m3] or third.get_intervals() == [-m3, P1]: 
				numeral = numeral.lower()

			accidental = self.get_interval().get_accidental_BL()

			new_string = ("-" if self.get_interval().get_sign_BL() == -1 else "") + accidental + numeral
			return new_string

		#@hashable_lru
		def is_reference_item_BL(self):
			new_boolean = self.get_interval() == P1
			return new_boolean

		def transform_BL(self, p_accidental, p_args = {}):	
			if self.get_parent_interval_list().get_parent_item() is not None:
				new_reference_point = self.get_parent_interval_list().get_parent_item() + new_interval if self.is_reference_item_BL() else self.get_parent_interval_list().get_parent_item()

			else: new_reference_point = self.get_parent_interval_list().get_tonic_tone() + new_interval if self.is_reference_item_BL() else self.get_parent_interval_list().get_tonic_tone()

			new_interval = self.get_interval().transform(p_accidental)
			new_intervals = [item for item in self.get_parent_interval_list().get_intervals() if item != self.get_interval()] + [new_interval]
			new_intervals = Utilities.sort_intervals(new_intervals)

			new_args = self.get_parent_interval_list().get_attributes()
			new_args.update(p_args)

			new_args["p_item_1"] = new_reference_point
			new_args["p_item_2"] = new_intervals
			new_args["p_type_dict"] = Utilities.intervals_to_type_dict(new_intervals)

			new_interval_list = type(self.get_parent_interval_list())(**new_args)
			return new_interval_list

		def build_interval_list_BL(self, *p_args):
			new_interval_list = IntervalList(self, *p_args)
			return new_interval_list

		def build_BL(self, p_object_type, *p_args):
			new_interval_list = p_object_type(self, *p_args)
			return new_interval_list

		def transpose_BL(self, p_other, p_generic_interval_args = {}):
			new_item = self.get_parent_interval_list().transpose_BL(p_other, p_generic_interval_args).get_items()[self.get_position_BL() - 1]
			return new_item

		#@hashable_lru
		def is_un_altered_BL(self): 
			new_boolean = self.get_interval().simplify_BL() in self.get_parent_interval_list().get_unaltered_intervals()
			return new_boolean

		#@hashable_lru
		def is_altered_BL(self):
			new_boolean = not self.is_un_altered_BL()
			return new_boolean

		#@hashable_lru
		def is_omitted_BL(self): 
			new_boolean = self.is_temp() and (not self.find_in_parent_BL().is_temp() if self.get_parent_interval_list().get_parent_item() is not None else False)
			return new_boolean

		#@hashable_lru
		def resolve_BL(self):
			new_item = self.add_BL(-self.get_alteration_BL())
			return new_item

		#@hashable_lru
		def get_alteration_BL(self):
			new_interval = self.get_interval().simplify_BL() - [item for item in self.get_parent_interval_list().get_unaltered_intervals() if item.get_numeral() == self.get_interval().simplify_BL().get_numeral()][0]
			return new_interval

		#@hashable_lru
		def get_reference_point_BL(self):
			new_reference_point = self.get_parent_interval_list().get_tonic_tone() + self.get_interval()
			return new_reference_point

		#@hashable_lru
		def get_position_BL(self):
			new_int = self.get_parent_interval_list().get_items().index(self) + 1
			return new_int

		#@hashable_lru
		def get_position_in_parent_BL(self): 
			new_int = self.find_in_parent_BL().get_position_BL()
			return new_int

		#@hashable_lru
		def find_in_parent_BL(self):
			if self.get_parent_interval_list().get_parent_item() != None: 
				new_item = self.get_parent_interval_list().get_parent_item().get_parent_interval_list().__getitem__(self.get_parent_interval_list().get_parent_item().get_interval() + self.get_interval())
				return new_item
			
			else: return None

		#@hashable_lru
		def get_generic_interval_BL(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args):
			new_generic_interval = self.sub_BL(self.get_parent_interval_list().get_reference_item_BL(), p_generic_interval_args = {"p_ignore_parent": p_ignore_parent, "p_cascade_args": p_cascade_args, "p_ignore_altered": p_ignore_altered, "p_remove_temp": p_remove_temp})
			return new_generic_interval

		#@hashable_lru
		def next_BL(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args):
			ignore_parent = p_ignore_parent if p_ignore_parent is not None else not self.get_parent_interval_list().is_sublist()
			ignore_altered = p_ignore_altered if p_ignore_altered is not None else self.get_parent_interval_list().is_altered()

			if self.get_parent_interval_list().get_parent_item() is not None and not ignore_parent:
				new_item = self.find_in_parent_BL().next_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args if p_cascade_args else {})
				delta = new_item.get_parent_interval_list().get_tonic_tone() - self.get_parent_interval_list().get_tonic_tone()
				new_interval = new_item.get_interval() + delta - self.get_interval()
				new_item = self.add_BL(new_interval)

			elif self.get_position_BL() == len(self.get_parent_interval_list().get_items()): 
				if self.get_parent_interval_list().get_parent_item() is not None:
					new_reference_point = self.get_parent_interval_list().get_parent_item() + self.get_parent_interval_list().get_fixed_invert_BL()

				else: new_reference_point = self.get_parent_interval_list().get_tonic_tone() + self.get_parent_interval_list().get_fixed_invert_BL()
				
				new_attributes = self.get_parent_interval_list().get_attributes()
				new_attributes["p_item_1"] = new_reference_point

				new_interval_list = type(self.get_parent_interval_list())(**new_attributes)
				new_item = new_interval_list.get_items()[0]

			else: new_item = self.get_parent_interval_list().get_items()[(self.get_position_BL() - 1) + 1]

			if self.is_temp() and p_remove_temp:
				new_interval_list = new_item.get_parent_interval_list()

				if new_interval_list.get_item_by_interval(self.get_interval()).get_position_BL() != new_item.get_position_BL():
					new_interval_list = new_interval_list.remove_BL(new_interval_list.get_item_by_interval(self.get_interval()).get_position_BL())
					new_item = new_interval_list.get_item_by_interval(new_item.get_interval())

			if (not new_item.is_un_altered_BL()) and ignore_altered and ignore_parent:
				return new_item.next_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

			return new_item

		#@hashable_lru
		def previous_BL(self, p_ignore_parent = None, p_cascade_args = False,  p_ignore_altered = True, p_remove_temp = True, *p_args):	
			ignore_parent = p_ignore_parent if p_ignore_parent is not None else not self.get_parent_interval_list().is_sublist()
			ignore_altered = p_ignore_altered if p_ignore_altered is not None else self.get_parent_interval_list().is_altered()
			
			if self.get_parent_interval_list().get_parent_item() is not None and not ignore_parent:
				new_item = self.find_in_parent_BL().previous_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args if p_cascade_args else {})
				delta = new_item.get_parent_interval_list().get_tonic_tone() - self.get_parent_interval_list().get_tonic_tone()
				new_interval = new_item.get_interval() + delta - self.get_interval()
				new_item = self.add_BL(new_interval)

			elif self.get_position_BL() == 1: 
				if self.get_parent_interval_list().get_parent_item() is not None:
					new_reference_point = self.get_parent_interval_list().get_parent_item() - self.get_parent_interval_list().get_fixed_invert_BL()

				else: new_reference_point = self.get_parent_interval_list().get_tonic_tone() - self.get_parent_interval_list().get_fixed_invert_BL()
				
				new_attributes = self.get_parent_interval_list().get_attributes()
				new_attributes["p_item_1"] = new_reference_point

				new_interval_list = type(self.get_parent_interval_list())(**new_attributes)
				new_item = new_interval_list.get_items()[-1]

			else: new_item = self.get_parent_interval_list().get_items()[(self.get_position_BL() - 1) - 1]

			if self.is_temp() and p_remove_temp:
				new_interval_list = new_item.get_parent_interval_list()

				if new_interval_list.get_item_by_interval(self.get_interval()).get_position_BL() != new_item.get_position_BL():
					new_interval_list = new_interval_list.remove_BL(new_interval_list.get_item_by_interval(self.get_interval()).get_position_BL())
					new_item = new_interval_list.get_item_by_interval(new_item.get_interval())

			if (not new_item.is_un_altered_BL()) and ignore_altered and ignore_parent:
				return new_item.previous_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

			return new_item

		#####################################
		# Overridden Business Logic Methods #
		#####################################

		def get_attributes(self): 
			return {
				"p_temp": self.is_temp()
			}

		###################
		# Wrapper methods #
		###################

		def __getattr__(self, p_attr): 
			return self.getattr_BL(p_attr)

		def __deepcopy__(self, p_memo):
			return self.deepcopy_BL(p_memo)

		def __hash__(self):
			return self.hash_BL()

		def __repr__(self): 
			return self.repr_BL()

		def __str__(self): 
			return self.str_BL()

		def __eq__(self, p_other): 
			return self.eq_BL(p_other)

		def __ne__(self, p_other): 
			return self.ne_BL(p_other)

		def __radd__(self, p_other, *p_args):
			return self.radd_BL(p_other, *p_args)

		def __rsub__(self, p_other, *p_args):
			return self.rsub_BL(p_other, *p_args)

		def __rmul__(self, p_other, *p_args):
			return self.rmul_BL(p_other, *p_args)

		def __rdiv__(self, p_other, *p_args):
			return self.rdiv_BL(p_other, *p_args)

		def __add__(self, p_other, p_generic_interval_args = {"p_ignore_parent": None, "p_cascade_args": False, "p_ignore_altered": True, "p_remove_temp": True}): 
			return self.add_BL(p_other, p_generic_interval_args)
		
		def __sub__(self, p_other, p_generic_interval_args = {"p_ignore_parent": None, "p_cascade_args": False, "p_ignore_altered": True, "p_remove_temp": True}): 
			return self.sub_BL(p_other, p_generic_interval_args)

		def __getitem__(self, p_index, p_generic_interval_args = {}, p_preserve_parent = False, p_bi_directional = False, p_args = {}):
			return self.getitem_BL(p_index, p_generic_interval_args, p_preserve_parent, p_bi_directional, p_args)

		def get_numeral_notation(self, p_cascade = True): 
			return self.get_numeral_notation_BL(p_cascade)

		def is_reference_item(self):
			return self.is_reference_item_BL()

		def transform(self, p_accidental, p_args = {}): 
			return self.transform_BL(p_accidental, p_args)

		def build_interval_list(self, *p_args): 
			return self.build_interval_list_BL(*p_args)

		def build(self, p_object_type, *p_args): 
			return self.build_BL(p_object_type, *p_args)

		def transpose(self, p_other, p_generic_interval_args = {}): 
			return self.transpose_BL(p_other, p_generic_interval_args)

		def is_un_altered(self): 
			return self.is_un_altered_BL()

		def is_altered(self): 
			return self.is_altered_BL()

		def is_omitted(self): 
			return self.is_omitted_BL()

		def resolve(self): 
			return self.resolve_BL()

		def get_alteration(self): 
			return self.get_alteration_BL()

		def get_reference_point(self): 
			return self.get_reference_point_BL()				

		def get_position(self): 
			return self.get_position_BL()

		def get_position_in_parent(self): 
			return self.get_position_in_parent_BL()

		def find_in_parent(self): 
			return self.find_in_parent_BL()

		def get_generic_interval(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args): 
			return self.get_generic_interval_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

		def next(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args): 
			return self.next_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

		def previous(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args): 
			return self.previous_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

		#######################
		# Getters and Setters #
		#######################

		def get_interval(self): 
			return self.interval

		def get_parent_interval_list(self): 
			return self.parent_interval_list

		def is_temp(self): 
			return self.temp

		def set_interval(self, p_interval): 
			self.interval = p_interval

		def set_parent_interval_list(self, p_parent_interval_list): 
			self.parent_interval_list = p_parent_interval_list

		def set_temp(self, p_temp): 
			self.temp = p_temp