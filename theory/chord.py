import itertools

from theory.scale import *

class Chord(IntervalList, IMusicObject):
	
	def __init__(self,  
		p_item_1, 
		p_item_2 = None, 
		p_unaltered_intervals = [],
		p_type_dict = {},
		p_sublist = True,
		p_altered = True,
		p_floor = None,
		p_roof = None,
		p_direction = 1, 
		p_root = None,
		p_bass_triad_quality = None,
		p_extensions_quality = None, 
		p_extensions_size = 7,
		p_modulate_parent = False): 

		defaults = {
			"p_item_1": p_item_1,
			"p_item_2": p_item_2, 
			"p_unaltered_intervals": p_unaltered_intervals,
			"p_type_dict": p_type_dict,
			"p_sublist": p_sublist,
			"p_altered": p_altered,
			"p_floor": p_floor,
			"p_roof": p_roof, 
			"p_direction": p_direction,
			"p_root": p_root,
			"p_bass_triad_quality": p_bass_triad_quality,
			"p_extensions_quality": p_extensions_quality, 
			"p_extensions_size": p_extensions_size,
			"p_modulate_parent": p_modulate_parent
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
		p_root: defaults["p_root"]
		p_bass_triad_quality: defaults["p_bass_triad_quality"]
		p_extensions_quality: defaults["p_extensions_quality"]
		p_extensions_size: defaults["p_extensions_size"]
		p_modulate_parent: defaults["p_modulate_parent"]

		intervals = Chord.configure_intervals(p_item_1, p_item_2)
		type_dict = p_type_dict

		self.sublist = p_sublist
		self.altered = p_altered

		bounds = Chord.configure_bounds(p_floor, p_roof, p_direction, intervals)

		self.direction = p_direction
		self.floor = bounds["floor"]
		self.roof = bounds["roof"]

		quality_data = Chord.configure_quality(p_item_2, p_root, intervals, p_bass_triad_quality, p_extensions_quality, p_fixed_invert = self.roof - self.floor)

		self.root = quality_data["Root"]
		self.bass_triad_quality = quality_data["Bass Triad Quality"]
		self.extensions_quality = quality_data["Extensions Quality"]
		self.extensions_size = int(quality_data["Extensions Size"])

		parent_item = Chord.configure_reference_point(p_item_1, self.bass_triad_quality, self.extensions_quality)
		parent_item = Chord.configure_extensions(parent_item, self.root, self.bass_triad_quality, self.extensions_quality, self.extensions_size, p_modulate_parent)

		# There is no check to verify if parent item is an item object and not a reference point
		# Configure Parent Item and configureUnalteredIntervals_BL should be static
		self.parent_item = Chord.configure_parent_item(parent_item, intervals, self.sublist)
		self.unaltered_intervals = Chord.configure_unaltered_intervals(intervals, p_unaltered_intervals, self.sublist, self.parent_item, (self.roof - self.floor))

		# Should add ability to grab type dict from parent item
		self.tonic_tone = self.parent_item.get_reference_point_BL()

		self.derived_attributes = {}
		self.build_items(intervals, type_dict)

	##################
	# Object Methods #
	#################

	'''
	def __div__(self, p_other):
		delta = p_other.getReferencePoint() - self.getReferencePoint()
		new_interval_list = self

		if delta not in self.get_intervals():
			new_interval_list = new_interval_list.add_interval_BL(delta, p_attributes = {"p_temp": True})

		new_args = new_interval_list.get_attributes()
		new_args["p_compound"] = 

		new_interval_list = type(self)(**new_args)

		if delta not in self.get_intervals():
			new_interval_list = self.add_interval_BL(delta, p_attributes = {"p_temp": True})

		new_interval_list = new_interval_list.getitem_BL(delta).build_BL(Chord, **p_other.get_attributes())
	'''
	
	#########################
	# Configuration Methods #
	#########################

	def set_parent_item(self, p_item): 
		if p_item == None: return
		self.parent_item = self.configureParentItem(p_item, self.get_intervals())

	@staticmethod
	def configure_intervals(p_item_1, p_item_2):
		if isinstance(p_item_2, str):
			new_intervals = Utilities.string_to_pitch_class(p_item_2)
			return new_intervals

		else: 
			new_intervals = IntervalList.configure_intervals(p_item_1, p_item_2)
			return new_intervals

	@staticmethod
	def configure_quality(p_item_2, p_root, p_intervals, p_bass_triad_quality, p_extensions_quality, p_fixed_invert):
		if isinstance(p_item_2, str):
			quality_data = Utilities.string_quality_to_data(p_item_2)
			quality_data["Root"] = [P1, P1]
			
			new_dict = quality_data
			return new_dict

		else:
			static_parent_chord_data = Utilities.get_parent_chord_static(p_intervals, p_root, p_bass_triad_quality, p_extensions_quality, p_fixed_invert)
			quality_data = Utilities.intervals_to_quality(static_parent_chord_data["Parent Chord"])
			quality_data["Root"] = static_parent_chord_data["Root"]
			
			new_dict = quality_data
			return new_dict

	@staticmethod
	def configure_reference_point(p_item_1, p_bass_triad_quality, p_extensions_quality):
		if isinstance(p_item_1, Chord.Part):
			new_reference_point = p_item_1.find_in_parent_BL()
			return new_reference_point

		elif issubclass(type(p_item_1), IntervalList):
			new_reference_point = p_item_1.get_parent_item() if p_item_1.get_parent_item() is not None else Scale(p_item_1, Utilities.identify_parent_scale(p_bass_triad_quality, p_extensions_quality)).get_items()[0]
			return new_reference_point

		else: 
			new_reference_point = IntervalList.configure_reference_point(p_item_1)
			return new_reference_point

	@staticmethod
	def configure_extensions(p_item_1, p_root, p_bass_triad_quality, p_extensions_quality, p_extension_size, p_modulate_parent):
		root_position = p_root[1].simplify() if p_root is not None else P1

		unaltered_intervals_quality = Utilities.identify_parent_scale(p_bass_triad_quality, p_extensions_quality, p_extension_size)
		unaltered_intervals_quality_rotated = Utilities.sort_intervals([(item + root_position).simplify() for item in unaltered_intervals_quality])
		new_reference_point = p_item_1

		if isinstance(p_item_1, Scale.Degree):
			unaltered_intervals_parent = Utilities.derive_unaltered_intervals_from_parent(p_item_1) if p_item_1 is not None else []

			if p_item_1 is not None and all(item in unaltered_intervals_parent for item in unaltered_intervals_quality_rotated) and not p_modulate_parent:
				return p_item_1

		new_unaltered_intervals = Utilities.identify_parent_scale(p_bass_triad_quality, p_extensions_quality)
		new_unaltered_intervals = Utilities.sort_intervals([(item + root_position).simplify() for item in new_unaltered_intervals])
		new_intervals = new_unaltered_intervals

		if P1 not in new_intervals:
			new_intervals = [P1] + new_intervals

		new_scale = Scale(new_reference_point, new_intervals, new_unaltered_intervals).get_items()[0]
		return new_scale

	#################
	# Sugar Methods #
	#################

	def get_parts(self): 
		return self.get_items()

	def get_parent_degree(self): 
		return self.get_parent_item()

	def set_parts(self, p_parts):
		self.set_items(p_parts)

	def set_parent_degree(self, p_parent_item):
		self.set_parent_item(p_parent_item)

	def get_parent_scale(self): 
		return self.get_parent_interval_list_BL()

	def get_part_by_interval(self, p_interval): 
		return self.get_item_by_interval_BL(p_interval)

	def get_part_by_numeral(self, p_numeral): 
		return self.get_item_by_numeral_BL(p_numeral)
		
	##########################
	# Business Logic Methods #
	##########################

	def get_secondary_dominant_BL(self):
		new_reference_point = self.get_parent_item().getitem_BL(slice(None, None, None)).getitem_BL(5)
		
		new_chord = type(self)(new_reference_point.getitem_BL(tuple([P1, M3, P5, m7])))
		return new_chord

	def get_secondary_sub_dominant_BL(self):
		new_reference_point = self.get_parent_item().getitem_BL(slice(None, None, None)).getitem_BL(2)
		
		new_chord = type(self)(new_reference_point.getitem_BL(slice(None, None, 3)))
		return new_chord

	def get_secondary_tonic_BL(self):
		new_reference_point = self.get_parent_item().getitem_BL(slice(None, None, None)).getitem_BL(1)
		
		new_chord = type(self)(new_reference_point.getitem_BL(slice(None, None, 3)))
		return new_chord

	def get_secondary_neopolitan_BL(self):
		new_chord.get_secondary_sub_dominant_BL().get_items()[0].transform_BL(-1)
		return new_chord

	def get_secondary_augmented_six_BL(self):
		new_chord = self.get_secondary_dominant_BL().get_secondary_tritone_substitution_BL()
		return new_chord

	def get_secondary_tritone_substitution_BL(self):
		new_chord = self.get_secondary_dominant_BL().get_items()[2].transform_BL(-1)
		return new_chord

	def transform_chord_to_BL(self, p_intervals):
		new_args = self.get_attributes()
		new_args["p_item_2"] = p_intervals

		new_chord = type(self)(**new_args)
		return new_chord

	def get_all_inversions_BL(self):
		new_list = [self.invert_BL(item) for item in range(len(self.get_intervals()))]
		return new_list

	def build_on_thirds_BL(self):
		new_args = self.get_attributes()
		new_args["p_item_1"] = self.get_parent_item()
		new_args["p_item_2"] = [item for item in Utilities.re_arrange_intervals_as_thirds(self.get_intervals()) if item != None]
		
		new_chord = type(self)(**new_args)
		return new_chord

	def simplify_BL(self):
		new_args = self.get_attributes()
		new_args["p_item_1"] = self.get_parent_item()
		new_args["p_item_2"] = Utilities.simplify(self.get_intervals())

		new_chord = type(self)(**new_args)
		return new_chord

	def next_BL(self):
		new_chord = self.add_BL(2)
		return new_chord

	def previous_BL(self):
		new_chord = self.add_BL(-2)
		return new_chord

	def get_parent_chord_BL(self):
		new_chord = self.get_root_position_BL().build_on_thirds_BL()
		return new_chord

	def get_parent_chord_quality_data_BL(self, p_system = DEFAULT_SYSTEM):
		new_dict = Utilities.intervals_to_quality(self.get_parent_chord_BL().get_intervals(), self.get_bass_triad_quality(), self.get_extensions_quality(), p_system)
		return new_dict

	def get_parent_chord_quality_BL(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		data = self.get_parent_chord_quality_data_BL(p_system)
		modifications = data["Bass Triad Accidentals"] + data["Bass Triad Omissions"] + data["Extensions Accidentals"] + data["Extensions Omissions"]
		modifications.sort(key=lambda x: x[1].get_numeral())
		
		new_string = data["Bass Triad Quality"][p_style] + (data["Extensions Quality"][p_style] if data["Bass Triad Quality"] != data["Extensions Quality"] else "") + str(data["Extensions Size"]) + (''.join([item[0] + str(item[1]) for item in modifications]))
		return new_string

	def get_quality_data_BL(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		parent_chord_quality_data = self.get_parent_chord_quality_data_BL(p_system)
		temp_first_inversion_intervals = self.get_root_position_BL().get_intervals()
		add = []
		sus = []

		for interval in temp_first_inversion_intervals:
			if (not (interval.get_numeral() - 1) % 2) == 0:
				if (interval.get_numeral() in [2, 4]) and (3 not in [item.get_numeral() for item in temp_first_inversion_intervals]): sus.append((SUSPENDED_NOTATION[p_system], interval))
				else: add.append((ADDITION_NOTATION[p_system], interval))

		parent_chord_quality_data["Added"] = add
		parent_chord_quality_data["Suspended"] = sus

		new_dict = parent_chord_quality_data
		return new_dict

	def get_quality_BL(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		data = self.get_quality_data_BL(p_style, p_system)
		modifications = data["Bass Triad Accidentals"] + data["Bass Triad Omissions"] + data["Extensions Accidentals"] + data["Extensions Omissions"] + data["Added"] + data["Suspended"]
		modifications.sort(key=lambda x: x[1].get_numeral())
		
		new_string = data["Bass Triad Quality"][p_style] + (data["Extensions Quality"][p_style] if data["Bass Triad Quality"] != data["Extensions Quality"] else "") + str(data["Extensions Size"]) + (''.join([item[0] + str(item[1]) for item in modifications]))
		return new_string

	def get_numeral_BL(self, p_with_quality = False, p_style = 2, p_cascade = False, p_system = DEFAULT_SYSTEM):
		root_item = self.getitem_BL(self.get_root()[1]).find_in_parent_BL()

		new_string = root_item.get_numeral_notation_BL(p_cascade) + self.get_parent_chord_quality_BL(p_style, p_system) if p_with_quality else root_item.get_numeral_notation_BL(p_cascade)
		return new_string

	def get_numeral_with_context_BL(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):
		secondary_information = "\\" + type(self)(self.get_parent_interval_list().get_parent_item().getitem_BL(slice(None, 8, 3))).get_numeral_BL(p_cascade = True) if self.get_parent_interval_list().get_parent_item() is not None else ""
		
		new_string = self.get_numeral_BL(p_with_quality, p_style, False, p_system) + secondary_information
		return new_string

	def get_figured_bass_BL(self, p_slice = -1):
		new_string = self.get_parent_chord_BL().get_numeral_BL(False) + " " + self.pitch_class_to_figured_bass_BL(p_slice)
		return new_string

	def pitch_class_to_figured_bass_BL(self, p_slice):
		temp_chord = self.invert_BL(1)

		for temp_chord in self.get_all_inversions_BL()[1:]:
			if temp_chord.get_intervals()[::-1][:p_slice] == self.get_intervals()[::-1][:p_slice] and p_slice != len(self.get_intervals()): 
				return self.pitch_class_to_figured_bass_BL(p_slice + 1)

			temp_chord = temp_chord.invert_BL(1)

		string = ""

		if p_slice == -1: 
			p_slice == 1

		for numeral in [item.get_numeral() for item in self.get_intervals()[::-1]][:p_slice]: 
			string = string + str(numeral) + "/"\

		new_string = string[:-1]
		return new_string

	def resolve_chord_BL(self, p_system = DEFAULT_SYSTEM):
		new_chord = self.resolve_chord_into_BL((self.get_root_position_BL().build_on_thirds_BL() + RESOLUTION_SYSTEM[p_system]).getitem_BL(slice(1, 8, 3)))
		return new_chord

	def resolve_chord_into_BL(self, p_next_chord, p_system = DEFAULT_SYSTEM):
		resolution_list = []

		for item in self.get_items():
			possible_motion = item.get_motion_to_closest_item_BL(p_next_chord)
			resolution_list.append(possible_motion)

		all_combinations = list(itertools.product(*resolution_list))
		possible_chords = []

		for combination in all_combinations:
			new_reference_points = []
			index = 1

			for move in combination:
				new_reference_point = self.get_items()[index - 1].getitem_BL(move).get_reference_point()
				new_reference_points.append(new_reference_point)
				index += 1

			new_intervals = Utilities.tones_to_pitch_class(new_reference_points)
			new_intervals = Utilities.normalize_intervals(new_intervals)
			possible_chords.append((combination, new_intervals))

		'''
		for combination in all_combinations:
			new_chord = self
			new_chord_size = len(new_chord.get_intervals())
			index = 1

			for move in combination:
				new_chord = new_chord.get_items()[index - 1].move_BL(move)

				if len(new_chord.get_intervals()) != new_chord_size: 
					new_chord_size = len(new_chord.get_intervals())
					continue

				index += 1

			possible_chords.append(new_chord)
		'''

		min_chord = None
		min_chord_count = 1000
		max_chord_size = 0
		best_fit_index = 0
		index = 0

		for combination, new_intervals in possible_chords:
			temp_chord_count = Utilities.get_item_repetition_count(new_intervals)
			temp_chord_size = len(new_intervals)

			if temp_chord_count < min_chord_count or (temp_chord_count == min_chord_count and temp_chord_size > max_chord_size):
				min_chord = combination
				min_chord_count = temp_chord_count
				max_chord_size = temp_chord_size
				best_fit_index = index

			index += 1

		new_chord = self
		index = 1

		for move in min_chord:
			new_chord = new_chord.get_items()[index - 1].move_BL(move)
			index += 1

		return new_chord

	def get_possible_parent_scales_BL(self, p_cardinality = 7, p_distinct = True):
		new_list = {}

		for i in range(4096):
			if len([item for item in str('{0:012b}'.format(i)) if item == '1']) == p_cardinality:
				new_scale = Scale(self.get_items()[0].get_reference_point_BL(), Utilities.decimal_to_pitch_class(i))

				if Utilities.is_distinct(new_scale.get_intervals()) == p_distinct and self in new_scale: 
					new_list[new_scale.getName()] = new_scale

		return new_list

	def invert_BL(self, p_inversion_number = 1):
		sign = int(p_inversion_number / abs(p_inversion_number) if p_inversion_number != 0 else 1)
		p_inversion_number += sign

		new_chord = self.rotate_BL(p_inversion_number)
		return new_chord

	def get_inversion_BL(self):
		if not self.is_rootless_BL():
			root_interval = self.get_root()[1].simplify()
			new_object = len(self.get_items()) - ([item for item in self.get_items() if item.get_interval().simplify() == root_interval][0].get_position_BL() - 1)
			
			new_int = new_object if new_object != len(self.get_items()) else 0
			return new_int

		else: 
			print("Failed to retrieve inversion of Chord as the Chord is rootless")
			return 0

	def is_rootless_BL(self):
		new_boolean = not self.get_root()[1].simplify() in Utilities.simplify_intervals(self.get_intervals())
		return new_boolean

	def get_root_position_BL(self):
		new_chord = self.invert_BL(-self.get_inversion_BL())
		return new_chord

	#####################################
	# Overridden Business Logic Methods #
	#####################################

	def hash_BL(self): 
		new_hash = hash((self.tonic_tone,
						make_hash(self.parent_item),
						make_hash(self.get_type_dict()),
						make_hash(self.unaltered_intervals),
						self.sublist,
						self.altered,
						self.floor,
						self.roof,
						self.direction,
						make_hash(self.root),
						self.bass_triad_quality,
						self.extensions_quality,
						self.extensions_size))
		return new_hash

	def add_BL(self, p_other, p_generic_interval_args = {}, p_args = {}):
		if issubclass(type(p_other), IntervalList.Item):
			new_args = p_args.copy()

			new_args["p_root"] = None
			new_args["p_bass_triad_quality"] = None
			new_args["p_extensions_quality"] = None

			new_chord = super().add_BL(p_other, p_generic_interval_args, new_args)
			return new_chord

		else: return super().add_BL(p_other, p_generic_interval_args, p_args)

	def remove_BL(self, p_item_index, p_args = {}):
		new_args = p_args.copy()

		new_chord = super().remove_BL(p_item_index, new_args)
		return new_chord

	def add_interval_BL(self, p_interval, p_attributes = {}, p_args = {}):
		new_args = p_args.copy()

		new_chord = super().add_interval_BL(p_interval, p_attributes, new_args)
		return new_chord

	def replace_at_numeral_with_BL(self, p_numeral, p_interval, p_args = {}):
		new_args = p_args.copy()

		new_chord = super().replace_at_numeral_with_BL(p_numeral, p_interval, new_args)
		return new_chord

	def flip_axis_BL(self, p_args = {}):
		new_args = p_args.copy()

		new_args["p_root"] = None
		new_args["p_bass_triad_quality"] = None
		new_args["p_extensions_quality"] = None

		new_chord = super().flip_axis_BL(new_args)
		return new_chord

	def get_relative_BL(self, p_reflection_point = 5, p_args = {}):
		new_args = p_args.copy()

		new_args["p_root"] = None
		new_args["p_bass_triad_quality"] = None
		new_args["p_extensions_quality"] = None

		new_chord = super().get_relative_BL(p_reflection_point, new_args)
		return new_chord

	def get_parallel_BL(self, p_reflection_point = 5, p_args = {}):
		new_args = p_args.copy()

		new_args["p_root"] = None
		new_args["p_bass_triad_quality"] = None
		new_args["p_extensions_quality"] = None

		new_chord = super().get_parallel_BL(p_reflection_point, new_args)
		return new_chord

	def get_negative_BL(self, p_reflection_point = 5, p_args = {}):
		new_args = p_args.copy()

		new_args["p_root"] = [P1, Utilities.invert_intervals(self.get_root())[0]]
		new_args["p_bass_triad_quality"] = None
		new_args["p_extensions_quality"] = None

		new_chord = super().get_negative_BL(p_reflection_point, new_args)
		return new_chord
	
	def build_items(self, p_intervals, p_type_dict):
		self.items = []

		for i in range(len(p_intervals)):
			self.items.append(type(self).Part(p_intervals[i], self, **p_type_dict[p_intervals[i]] if p_intervals[i] in p_type_dict.keys() else {}))

	def get_attributes(self):
		new_args = super().get_attributes()

		new_args.update({
			"p_root": self.get_root(),
			"p_bass_triad_quality": self.get_bass_triad_quality(),
			"p_extensions_quality": self.get_extensions_quality()
		})

		return new_args

	###################
	# Wrapper Methods #
	###################

	def get_secondary_dominant(self):
		return self.get_secondary_dominant_BL()

	def get_secondary_sub_dominant(self):
		return self.get_secondary_sub_dominant_BL()

	def get_secondary_tonic(self):
		return self.get_secondary_tonic_BL()

	def get_secondary_neopolitan(self):
		return self.get_secondary_neopolitan_BL()

	def get_secondary_augmented_six(self):
		return self.get_secondary_augmented_six_BL()

	def get_secondary_tritone_substitution(self):
		return self.get_secondary_tritone_substitution_BL()

	def transform_chord_to(self, p_intervals):
		return self.transform_chord_to_BL(p_intervals)

	def get_all_inversions(self):
		return self.get_all_inversions_BL()

	def build_on_thirds(self):
		return self.build_on_thirds_BL()

	def simplify(self):
		return self.simplify_BL()

	def next(self):
		return self.next_BL()

	def previous(self):
		return self.previous_BL()

	def get_parent_chord(self):
		return self.get_parent_chord_BL()

	def get_parent_chord_quality_data(self, p_system = DEFAULT_SYSTEM):
		return self.get_parent_chord_quality_data_BL(p_system)

	def get_parent_chord_quality(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		return self.get_parent_chord_quality_BL(p_style, p_system)

	def get_quality_data(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		return self.get_quality_data_BL(p_style, p_system)

	def get_quality(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		return self.get_quality_BL(p_style, p_system)

	def get_numeral(self, p_with_quality = False, p_style = 2, p_cascade = False, p_system = DEFAULT_SYSTEM):
		return self.get_numeral_BL(p_with_quality, p_style, p_cascade, p_system)

	def get_numeral_with_context(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):
		return self.get_numeral_with_context_BL(p_with_quality, p_style, p_system)

	def get_figured_bass(self, p_slice = -1):
		return self.get_figured_bass_BL(p_slice)

	def pitch_class_to_figured_bass(self, p_slice):
		return self.pitch_class_to_figured_bass_BL(p_slice)

	def resolve_chord(self, p_system = DEFAULT_SYSTEM):
		return self.resolve_chord_BL(p_system)

	def resolve_chord_into(self, p_next_chord, p_system = DEFAULT_SYSTEM):
		return self.resolve_chord_into_BL(p_next_chord, p_system)

	def get_possible_parent_scales(self, p_cardinality = 7, p_distinct = True):
		return self.get_possible_parent_scales_BL(p_cardinality, p_distinct)

	def invert(self, p_inversion_number = 1):
		return self.invert_BL(p_inversion_number)

	def get_inversion(self):
		return self.get_inversion_BL()

	def is_rootless(self):
		return self.is_rootless_BL()

	def get_root_position(self):
		return self.get_root_position_BL()

	#######################
	# Getters and Setters #
	#######################

	def set_root(self, p_root): 
		self.root = p_root

	def set_bass_triad_quality(self, p_bass_triad_quality): 
		self.bass_triad_quality = p_bass_triad_quality

	def set_extensions_quality(self, p_extensions_quality): 
		self.extensions_quality = p_extensions_quality

	def set_extensions_size(self, p_extensions_size):
		self.extensions_size = p_extensions_size

	def get_root(self): 
		return self.root

	def get_bass_triad_quality(self): 
		return self.bass_triad_quality

	def get_extensions_quality(self): 
		return self.extensions_quality

	def get_extensions_size(self):
		return self.extensions_size

	class Part(IntervalList.Item):

		def __init__(self, p_interval, p_parent_scale,  p_temp = False, p_antecedent_parts = None, p_consequent_parts = None):
			super().__init__(p_interval, p_parent_scale, p_temp)
			self.antecedent_parts = p_antecedent_parts
			self.consequent_parts = p_consequent_parts

		#################
		# Sugar Methods #
		#################

		def get_parent_chord_BL(self): 
			return self.get_parent_interval_list()

		##########################
		# Business Logic Methods #
		##########################

		'''
		def resolveVoice(self):
			new_part = self.nextInVoice()
			if new_part is None: return
			return new_part if new_part.getReferencePoint() != self.getReferencePoint() else new_part.nextInVoice()

		def nextInVoice(self):
			new_index = self.getPositionInParentVoice() + 1

			if new_index >= len(self.getParentVoice().get_items()):
				print("Error: No subsequent part found")
				return None

			new_part = self.getParentVoice().get_items(new_index)
			return new_index
		'''

		def is_enharmonic_BL(self):
			new_boolean = self.find_in_parent_chord_BL().get_interval().get_numeral() > 7 or self.isAltered_BL()
			return new_boolean

		def find_in_parent_chord_BL(self):
			temp_delta_to_root = self.get_root()[1]
			temp_intervals = Utilities.scale_intervals_by_order([temp_delta_to_root, self.get_interval()])
			temp_intervals = Utilities.normalize_intervals(temp_intervals)
			temp_intervals = Utilities.build_on_thirds_static(temp_intervals)
			
			new_chord = self.get_parent_interval_list().get_parent_chord_BL().get_items()[0].add_BL(temp_intervals[-1])
			return new_chord

		def move_BL(self, p_interval, p_generic_interval_args = {"p_ignore_parent": True, "p_cascade_args": False, "p_ignore_altered": False, "p_remove_temp": True}):
			new_chord = (self.__add__(p_interval)).__getitem__(tuple([1]), p_generic_interval_args, p_preserve_parent = True)

			if self.get_position_BL() != 1: 
				new_chord_start = self.get_parent_interval_list().getitem_BL(slice(1, self.get_position_BL(), 2), p_generic_interval_args)

				if new_chord_start.getitem_BL(len(new_chord_start.get_intervals()), p_generic_interval_args).get_reference_point_BL() != new_chord.get_items()[0].get_reference_point_BL(): 
					new_chord = new_chord_start.add_BL(new_chord, p_generic_interval_args)

				else: new_chord = new_chord_start
				
			if self.get_position_BL() != len(self.get_parent_interval_list().get_intervals()): 
				new_chord_end = self.get_parent_interval_list().getitem_BL(slice(self.get_position_BL() + 1, len(self.get_parent_interval_list().get_intervals()) + 1, 2), p_generic_interval_args)
				
				if new_chord_end.get_items()[0].get_reference_point_BL() != new_chord.getitem_BL(len(new_chord.get_intervals()), p_generic_interval_args).get_reference_point_BL(): 
					new_chord = new_chord.add_BL(new_chord_end, p_generic_interval_args)

				else: new_chord = new_chord.getitem_BL(slice(1, len(new_chord.get_intervals()) - 1, None), p_generic_interval_args).add_BL(new_chord_end, p_generic_interval_args) if len(new_chord.get_intervals()) > 1 else new_chord_end
				
			return new_chord

		def get_motion_to_closest_item_BL(self, p_next_chord):
			min_positive_distance = min([(tone.get_tone() - self.get_reference_point_BL().get_tone()).simplify() for tone in p_next_chord.get_reference_points_BL()])
			min_negative_distance = min([(self.get_reference_point_BL().get_tone() - tone.get_tone()).simplify() for tone in p_next_chord.get_reference_points_BL()])
			
			new_list = [min_positive_distance, -min_negative_distance]
			return new_list

		#####################################
		# Overridden Business Logic Methods #
		#####################################

		def transform_BL(self, p_accidental, p_args = {}):
			new_args = p_args.copy()

			new_chord = super().transform_BL(p_accidental, new_args)
			return new_chord

		def add_BL(self, p_other, p_generic_interval_args = {}, p_args = {}):
			if issubclass(type(p_other), IntervalList.Item):
				new_args = p_args.copy()

				new_args["p_root"] = None
				new_args["p_bass_triad_quality"] = None
				new_args["p_extensions_quality"] = None

				new_chord = super().add_BL(p_other, p_generic_interval_args, new_args)
				return new_chord

			else: return super().add_BL(p_other, p_generic_interval_args, p_args)

		def getitem_BL(self, p_index, p_generic_interval_args = {}, p_preserve_parent = False, p_bi_directional = False, p_args = {}): 
			if isinstance(p_index, tuple):
				new_root = (self.get_parent_interval_list().get_root()[1] - self.get_interval()).simplify()

				new_args = p_args.copy()
				new_args["p_root"] = [P1, new_root]
				
				new_chord = super().getitem_BL(p_index, p_generic_interval_args, p_preserve_parent, p_bi_directional, new_args)
				return new_chord

			else: return super().getitem_BL(p_index, p_generic_interval_args, p_preserve_parent, p_bi_directional, p_args)

		def get_attributes(self): 
			new_args = super().get_attributes()
			
			new_args.update({
				"p_antecedent_parts": self.get_antecedent_parts(),
				"p_consequent_parts": self.get_consequent_parts()
			})

			return new_args

		##############################
		# Overridden Wrapper Methods #
		##############################

		def __getattr__(self, p_attr):
			return getattr(self.find_in_parent_BL(), p_attr)

		###################
		# Wrapper Methods #
		###################

		def is_enharmonic(self):
			return self.is_enharmonic_BL()

		def find_in_parent_chord(self):
			return self.find_in_parent_chord_BL()

		def move(self, p_interval, p_generic_interval_args = {"p_ignore_parent": True, "p_cascade_args": False, "p_ignore_altered": False, "p_remove_temp": True}):
			return self.move_BL(p_interval, p_generic_interval_args)

		def get_motion_to_closest_item(self, p_next_chord):
			return self.get_motion_to_closest_item_BL(p_next_chord)

		#######################
		# Getters and Setters #
		#######################

		def get_antecedent_parts(self): 
			return self.antecedent_parts

		def get_consequent_parts(self): 
			return self.consequent_parts

		def set_antecedent_parts(self, p_antecedent_parts): 
			self.antecedent_parts = p_antecedent_parts

		def set_consequent_parts(self, p_consequent_parts): 
			self.consequent_parts = p_consequent_parts