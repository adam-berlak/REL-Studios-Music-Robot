import collections

from Configuration import *
from TheoryCollections.IntervalListUtilities import *
from TheoryComponents.IPitchedObject import * 

class IntervalList:

	def __init__(self, 
		p_item_1, 
		p_intervals, 
		p_unaltered_intervals = [], 
		p_type_dict = {},
		p_sublist = False,
		p_altered = True,
		p_fixed_invert = None):

		if issubclass(type(p_item_1), IntervalList):
			self.tonic_tone = p_item_1.getItems()[0].getReferencePoint_BL()
			self.intervals = p_item_1.getIntervals()
			self.parent_item = p_item_1.getParentItem() if p_item_1.getParentItem() is not None else None
			self.unaltered_intervals = IntervalListUtilities.getValidUnalteredIntervals(self.intervals, p_unaltered_intervals)
			self.type_dict = p_type_dict
			self.sublist = p_sublist
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()

		if issubclass(type(p_item_1), IntervalList.Item):	
			self.tonic_tone = p_parent_item.getReferencePoint_BL()
			self.intervals = p_intervals
			self.parent_item = self.configureParentItem_BL(p_item_1, self.intervals)
			self.unaltered_intervals = IntervalListUtilities.getValidUnalteredIntervals(self.intervals, p_unaltered_intervals)
			self.type_dict = p_type_dict
			self.sublist = p_sublist
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()

		elif isinstance(p_item_1, IPitchedObject):
			self.tonic_tone = p_item_1
			self.intervals = p_intervals
			self.parent_item = None
			self.unaltered_intervals = IntervalListUtilities.getValidUnalteredIntervals(self.intervals, p_unaltered_intervals)
			self.type_dict = p_type_dict
			self.sublist = p_sublist
			self.altered = p_altered
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()

		self.buildItems()

	#####################################
	# Methods concerning class behavior #
	#####################################

	def repr_BL(self): 
		return self.str_BL()

	def str_BL(self):
		result = "<" + type(self).__name__ + " "
		for item in self.getItems(): result += str(item) + ", "
		return result[:-2] + ">"

	def getitem_BL(self, p_index, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): 
		if isinstance(p_index, slice):
			new_intervals = IntervalListUtilities.normalizeIntervals(self.getIntervals()[p_index.start - 1:p_index.stop])
			new_reference_point = self.getitem_BL(p_index.start, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
			new_interval_list = new_reference_point.build_BL(type(self), new_intervals, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, p_args = {"p_sublist": True})
			return new_interval_list

		elif isinstance(p_index, tuple):
			new_interval_list = self.getItems()[0].build_BL(type(self), list(p_index), p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, p_args = {"p_sublist": True})
			return new_interval_list
		
		else: return self.getItems()[0].add_BL(p_index, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

	def contains_BL(self, p_other):
		if isinstance(p_other, IPitchedObject): 
			return p_other.simplify() in [item.simplify() for item in self.getReferencePoints_BL()]

		elif isinstance(p_other, Tone): 
			return p_other.simplify() in [item.simplify() for item in self.getTones()]

		elif isinstance(p_other, int): 
			return Interval.getSimpleNumeral(p_other) in [item.getNumeral() for item in self.getIntervals()]

		elif isinstance(p_other, Interval): 
			return any(p_other.simplify() in IntervalListUtilities.simplifyIntervals(elem.buildIntervalList().getIntervals()) for elem in self.getItems())
			
		elif isinstance(p_other, list) and len(p_other) > 0 and isinstance(p_other[0], Interval): 
			return any(all(item.buildIntervalList().contains_BL(elem) for elem in p_other) for item in self.getItems())

		elif issubclass(type(p_other), IntervalList.Item): 
			return self.contains_BL(p_other.getTone())

		elif issubclass(type(p_other), IntervalList): 
			return all(self.contains_BL(elem) for elem in p_other.getTones())

		return False

	##############
	# Comparison #
	##############

	def eq_BL(self, p_other): 
		return type(self) == type(p_other) and self.getTonicTone() == p_other.getTonicTone() and self.getIntervals() == p_other.getIntervals() and self.getAttributes() == p_other.getAttributes()

	def ne_BL(self, p_other): 
		return not self.eq_BL(p_other)

	##############
	# Arithmetic #
	##############

	def add_BL(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True):
		if isinstance(p_other, str): 
			return str(self) + p_other

		if isinstance(p_other, int): 
			new_interval_list = self.transpose_BL(p_other)
			return new_interval_list

		if isinstance(p_other, Interval): 
			if self.getParentItem() != None:
				new_reference_point = self.getItems()[0].findInParent_BL().add_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

			else: new_reference_point = self.getItems()[0].getReferencePoint_BL() + p_other

			new_interval_list = type(self)(new_reference_point, self.getIntervals(), **self.getAttributes())
			return new_interval_list

		if issubclass(type(p_other), IntervalList.Item):
			delta = p_other.getParentIntervalList().getTonicTone() - self.getTonicTone()
			new_intervals = self.getIntervals() + [p_other.getInterval() + delta]
			new_intervals = IntervalListUtilities.sortIntervals(new_intervals)
			new_intervals = IntervalListUtilities.normalizeIntervals(new_intervals)

			if self.getParentItem() is not None:
				new_reference_point = self.getParentItem() if (p_other.getReferencePoint_BL() - self.getItems()[0].getReferencePoint_BL()) > P1 else self.getParentItem() + delta

			else: new_reference_point = self.getItems()[0].getReferencePoint_BL() if (p_other.getReferencePoint_BL() - self.getItems()[0].getReferencePoint_BL()) > P1 else p_other.getReferencePoint_BL()
			
			new_attributes = self.getAttributes()
			new_attributes["p_type_dict"] = IntervalListUtilities.intervalsToTypeDict(new_intervals)
			new_attributes["p_unaltered_intervals"] = IntervalListUtilities.getNewUnalteredIntervals(new_intervals)
			new_interval_list = type(self)(new_reference_point, new_intervals, **new_attributes)
			return new_interval_list
		
		if issubclass(type(p_other), IntervalList):
			if len(p_other.getIntervals()) == 1: return self.add_BL(p_other.getItems()[0])
			return self.add_BL(p_other.getItems()[0], p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp).add_BL(p_other.remove_BL(1), p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

	def sub_BL(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True):
		if isinstance(p_other, int): 
			return self.add_BL(-p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
			
		if isinstance(p_other, Interval): 
			return self.add_BL(-p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

	def radd_BL(self, p_other):
		if isinstance(p_other, str): 
			return p_other + self.str_BL()

	################################
	# Methods concerned with names #
	################################

	def printTones_BL(self):
		result = ""
		for tone in self.getReferencePoints_BL(): result = result + str(tone) + ", "
		return "[" + result[:-2] + "]"

	################
	# list methods #
	################

	def getItemWhere_BL(self, p_lambda_expression):
		items = [item for item in self.getItems() if p_lambda_expression(item)]
		return items[0] if len(items) > 0 else None

	def getItemByInterval_BL(self, p_interval): 
		return self.getItemWhere_BL(lambda item: item.getInterval() == p_interval)

	def getItemByNumeral_BL(self, p_numeral): 
		return self.getItemWhere_BL(lambda item: item.getInterval().getNumeral() == p_numeral)

	def remove_BL(self, p_item_index):
		new_intervals = self.getIntervals()[:]
		new_intervals.pop(p_item_index - 1)

		if self.getParentItem() is not None:
			new_reference_point = self.getItems()[0].findInParent_BL() + new_intervals[0]

		else: new_reference_point = self.getTonicTone() + new_intervals[0]

		new_intervals = IntervalListUtilities.normalizeIntervals(new_intervals)
		new_attributes = self.getAttributes()
		new_attributes["p_type_dict"] = IntervalListUtilities.intervalsToTypeDict(new_intervals)
		new_interval_list = type(self)(new_reference_point, new_intervals, **new_attributes)
		return new_interval_list

	def addInterval_BL(self, p_interval, p_attributes = {}):
		new_pitch_class = self.getIntervals()[:]
		new_interval = type(self.getItems()[0])(p_interval, None, **p_attributes).getInterval()

		if new_interval not in new_pitch_class:
			new_pitch_class.append(new_interval)
			new_pitch_class = IntervalListUtilities.sortIntervals(new_pitch_class)
			new_pitch_class = IntervalListUtilities.normalizeIntervals(new_pitch_class)

		if self.getParentItem() is not None:
			new_reference_point = self.getParentItem() if new_interval.getSemitones() > 0 else self.getParentItem() + new_interval
		
		else: new_reference_point = self.getItems()[0].getReferencePoint_BL() if new_interval.getSemitones() > 0 else self.getItems()[0].getReferencePoint_BL() + new_interval

		new_attributes = self.getAttributes()
		new_attributes["p_type_dict"] = IntervalListUtilities.intervalsToTypeDict(new_pitch_class)
		new_interval_list = type(self)(new_reference_point, new_pitch_class, **new_attributes)
		return new_interval_list

	def replaceAtNumeralWith_BL(self, p_numeral, p_interval):
		list_items = [item for item in self.getIntervals() if item.getNumeral() == p_numeral]

		if len(list_items) != 0:
			index = self.getIntervals().index(list_items[0])
			new_interval_list_beginning = self.getIntervals()[:index]
			new_interval_list_beginning.append(p_interval)
			new_interval_list_ending = self.getIntervals()[index + 1:]
			new_interval_list_intervals = new_interval_list_beginning + new_interval_list_ending

		else: return self.addInterval_BL(p_interval)

		if self.getParentItem() is not None:
			new_reference_point = self.getParentItem()

		else: new_reference_point = self.getItems()[0].getReferencePoint_BL()

		new_attributes = self.getAttributes()
		new_interval_list = type(self)(new_reference_point, new_interval_list_intervals, **new_attributes)
		return new_interval_list

	#################
	# Sugar Methods #
	#################

	def rotate_BL(self, p_other = 2, p_ignore_parent = True, p_cascade_args = False, p_ignore_altered = False, p_remove_temp = True, p_preserve_parent = True, p_sublist = True):
		new_reference_point = self.getItems()[0].add_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
		new_interval_list = new_reference_point.build_BL(type(self), -1, 2, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, p_preserve_parent, p_sublist)
		return new_interval_list

	def transpose_BL(self, p_other = 2, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, p_preserve_parent = True, p_sublist = True):
		new_reference_point = self.getItems()[0].add_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
		new_intervals = self.getGenericIntervals_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
		new_interval_list = new_reference_point.build_BL(type(self), new_intervals, 2, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, p_preserve_parent, p_sublist)
		return new_interval_list

	def getParentIntervalList_BL(self): 
		return self.getParentItem().getParentIntervalList()

	def getNumerals_BL(self): 
		return [item.getNumeral() for item in self.getIntervals()]

	def getSemitones_BL(self): 
		return [item.getSemitones() for item in self.getIntervals()]

	def getGenericIntervals_BL(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True):
		return [item.getGenericInterval_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp) for item in self.getItems()]

	def getIntervalsWhere_BL(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = False, p_remove_temp = True): 
		ignore_parent = p_ignore_parent if p_ignore_parent is not None else not self.isSublist()

		if not ignore_parent:
			return self.getParentItem().buildPitchClass_BL(-1, 2) if not p_cascade_args else self.getParentItem().buildPitchClass_BL(-1, 2, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

		return [item.getInterval() for item in self.getItems() if (item.isUnAltered_BL() or (not p_ignore_altered))]

	def getIntervals_BL(self): 
		return [item.getInterval() for item in self.getItems()]

	def getTones_BL(self):
		return [item.getTone() for item in self.getReferencePoints_BL()]

	def getReferencePoints_BL(self): 
		return [item.getReferencePoint_BL() for item in self.getItems()]

	#################
	# Configuration #
	#################

	def configureParentItem_BL(self, p_item, p_intervals, p_modulate_parent = False):
		result_scale = p_item.getParentIntervalList()
		root_altered = False

		for interval in p_intervals:
			interval_in_parent = (p_item.getInterval() + interval)
			interval_in_parent = interval_in_parent.simplify()

			if (interval_in_parent not in result_scale.getIntervals()):
				if (p_modulate_parent and IntervalListUtilities.isDistinct(p_intervals)):
					if (interval_in_parent.getNumeral() == 1):
						root_altered = True
						alteration = interval_in_parent.getAccidental()
					result_scale = result_scale.replaceAtNumeralWith(interval_in_parent.getNumeral(), interval_in_parent)
				else: result_scale = result_scale.addInterval_BL(interval_in_parent, p_attributes = {"p_temp": True})
					
		if (root_altered): return result_scale.getItemByNumeral(p_item.getInterval().getNumeral())
		return result_scale.getItemByInterval(p_item.getInterval())

	###################
	# Wrapper Methods #
	###################

	def __repr__(self): return self.repr_BL()
	def __str__(self): return self.str_BL()

	def __eq__(self, p_other): return self.eq_BL(p_other)
	def __ne__(self, p_other): return self.ne_BL(p_other)

	def __contains__(self, p_other): return self.contains_BL(p_other)
	def __getitem__(self, p_index, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): return self.getitem_BL(p_index, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

	def __add__(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): return self.add_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
	def __sub__(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): return self.sub_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
	def __radd__(self, p_other): return self.radd_BL(p_other)

	def printTones(self): return self.printTones_BL()
	def getItemWhere(self, p_lambda_expression): return self.getItemWhere_BL(p_lambda_expression)
	def getItemByInterval(self, p_interval): return self.getItemByInterval_BL(p_interval)
	def getItemByNumeral(self, p_numeral): return self.getItemByNumeral_BL(p_numeral)
	def remove(self, p_item_index): return self.remove_BL(p_item_index)
	def addInterval(self, p_interval, p_attributes = {}): return self.addInterval_BL(p_interval, p_attributes)
	def replaceAtNumeralWith(self, p_numeral, p_interval): return self.replaceAtNumeralWith_BL(p_numeral, p_interval)
	def rotate(self, p_other = 2, p_ignore_parent = True, p_cascade_args = False, p_ignore_altered = False, p_remove_temp = True, p_preserve_parent = True, p_sublist = True): return self.rotate_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, p_preserve_parent, p_sublist)
	def transpose(self, p_other = 2, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, p_preserve_parent = True, p_sublist = True): return self.transpose_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, p_preserve_parent, p_sublist)
	def getParentIntervalList(self): return self.getParentIntervalList_BL()
	def getNumerals(self): return self.getNumerals_BL()
	def getSemitones(self): return self.getSemitones_BL()
	def getGenericIntervals(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): return self.getGenericIntervals_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
	def getIntervalsWhere(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = False, p_remove_temp = True): return self.getIntervalsWhere_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
	def getIntervals(self): return self.getIntervals_BL()
	def getTones(self): return self.getTones_BL()
	def getReferencePoints(self): return self.getReferencePoints_BL()
	def configureParentItem(self, p_item, p_intervals, p_modulate_parent = False): return self.configureParentItem_BL(p_item, p_intervals, p_modulate_parent)
	

	##############################
	# Overridable Business Logic #
	##############################

	def buildItems(self):
		self.items = []

		for i in range(len(self.intervals)):
			self.items.append(IntervalList.Item(self.intervals[i], self, **self.type_dict[self.intervals[i]] if self.intervals[i] in self.type_dict.keys() else {}))

	def getAttributes(self):
		return {
			"p_unaltered_intervals": self.getUnalteredIntervals(),
			"p_type_dict": self.getTypeDict(),
			"p_sublist": self.isSublist(),
			"p_altered": self.isAltered()
		}

	######################
	# Derived Attributes #
	######################

	def getTypeDict(self): 
		temp_type_dict = {}
		
		for item in self.getItems():
			temp_type_dict[item.getInterval()] = item.getAttributes()

		return temp_type_dict

	#######################
	# Getters and Setters #
	#######################

	def getItems(self): return self.items
	def getTonicTone(self): return self.tonic_tone
	def getUnalteredIntervals(self): return self.unaltered_intervals
	def isSublist(self): return self.sublist
	def isAltered(self): return self.altered
	def getFixedInvert(self): return self.fixed_invert
	def getParentItem(self): return self.parent_item

	def setItems(self, p_items): self.items = p_items
	def setTonicTone(self, p_tonic_tone): self.tonic_tone = p_tonic_tone
	def setUnalteredIntervals(self, p_unaltered_intervals): self.unaltered_intervals = p_unaltered_intervals
	def setSublist(self, p_sublist): self.sublist = p_sublist
	def setAltered(self, p_chromatic): self.altered = p_altered
	def setFixedInvert(self, p_fixed_invert): self.fixed_invert = p_fixed_invert

	class Item:
		
		def __init__(self, p_interval, p_parent_interval_list, p_temp = False):
			new_interval = Interval(p_interval.getSemitones(), p_interval.getNumeral(), self)
			self.interval = new_interval
			self.parent_interval_list = p_parent_interval_list
			self.temp = p_temp

		def getattr_BL(self, p_attr):
			if hasattr(self.getReferencePoint_BL(), p_attr): 
				return getattr(self.getReferencePoint_BL(), p_attr)

			elif hasattr(self.getInterval(), p_attr): 
				return getattr(self.getInterval(), p_attr)

		#####################################
		# Methods concerning class behavior #
		#####################################

		def repr_BL(self): 
			return self.str_BL()

		def str_BL(self):
			if not DEGREE_SIMPLE_REPRESENTATION: 
				return self.getNumeralNotation_BL() + ": " + str(self.getReferencePoint_BL())

			else: return str(self.getReferencePoint_BL())

		##############
		# Comparison #
		##############

		def eq_BL(self, p_other): 
			return type(self) == type(p_other) and self.getInterval() == p_other.getInterval() and self.getParentIntervalList() == p_other.getParentIntervalList() and self.getAttributes() == p_other.getAttributes()

		def ne_BL(self, p_other): 
			return not self.eq_BL(p_other)

		##############
		# Arithmetic #
		##############

		def add_BL(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True):
			if isinstance(p_other, str): 
				return str(self) + p_other

			if isinstance(p_other, int):	
				if abs(p_other) == 1: return self
				else: return self.next_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp).add_BL(p_other - 1, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp) if p_other > 0 else self.previous_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp).add_BL(p_other + 1, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
			
			if isinstance(p_other, list) and len(p_other) > 0 and (isinstance(p_other[0], Interval) or isinstance(p_other[0], int)):
				if len(p_other) == 1: return self.add_BL(p_other[0])
				return self.add_BL(p_other[0]).add_BL(p_other[1:])
			
			if isinstance(p_other, Interval):
				if abs(p_other) == P1: return self
				new_interval = self.getInterval() + p_other

				if new_interval < P1:
					return (self.getParentIntervalList().add_BL(-self.getParentIntervalList().getFixedInvert(), p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)).getItems()[self.getPosition_BL() - 1].add_BL(p_other + self.getParentIntervalList().getFixedInvert(), p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
				
				if new_interval >= self.getParentIntervalList().getFixedInvert():
					return (self.getParentIntervalList().add_BL(self.getParentIntervalList().getFixedInvert(), p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)).getItems()[self.getPosition_BL() - 1].add_BL(p_other - self.getParentIntervalList().getFixedInvert(), p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

				if new_interval not in self.getParentIntervalList().getIntervals():
					return self.getParentIntervalList().addInterval_BL(new_interval, p_attributes = {"p_temp": True}).getItemByInterval(new_interval)

				else: return self.getParentIntervalList().getItemByInterval(new_interval)

			if issubclass(type(p_other), IntervalList):
				new_interval_list = (self.add_BL(p_other.getItems()[0], p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)).add_BL(p_other.remove_BL(1), p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
				return new_interval_list
			
			if issubclass(type(p_other), IntervalList.Item):
				delta = p_other.getParentIntervalList().getTonicTone() - self.getParentIntervalList().getTonicTone()
				new_intervals = [self.getInterval(), p_other.getInterval() + delta] if self != p_other else [self.getInterval()]
				new_intervals = IntervalListUtilities.sortIntervals(new_intervals)
				new_intervals = IntervalListUtilities.normalizeIntervals(new_intervals)

				if self.getParentIntervalList().getParentItem() is not None:
					new_reference_point = self if (p_other.getReferencePoint_BL() - self.getReferencePoint_BL()) > P1 else self + delta

				else: new_reference_point = self if (p_other.getReferencePoint_BL() - self.getReferencePoint_BL()) > P1 else p_other
			
				new_attributes = self.getParentIntervalList().getAttributes()
				new_attributes["p_type_dict"] = IntervalListUtilities.intervalsToTypeDict(new_intervals)
				new_attributes["p_unaltered_intervals"] = IntervalListUtilities.getNewUnalteredIntervals(new_intervals)
				new_interval_list = type(self.getParentIntervalList())(new_reference_point, new_intervals, **new_attributes)
				return new_interval_list

		def sub_BL(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True):
			if isinstance(p_other, int):
				return self.add_BL(-p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

			if isinstance(p_other, Interval):
				return self.add_BL(-p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

			if issubclass(type(p_other), IntervalList.Item): 
				new_interval = self.getReferencePoint_BL() - p_other.getReferencePoint_BL()
				new_type_dict = {new_interval: self.getAttributes()}
				return type(self.getParentIntervalList())(p_other.getReferencePoint_BL(), [P1, new_interval], p_type_dict = new_type_dict).getItems()[1]
				
		def __radd__(self, p_other):
			if isinstance(p_other, str): 
				return p_other + str(self)

		################################
		# Methods concerned with names #
		################################

		def getNumeralNotation_BL(self):
			numeral = Interval.intToRoman(self.getInterval().getNumeral()) 

			if self.buildPitchClass_BL(2, 3) == [P1, m3]: 
				numeral = numeral.lower()

			accidental = self.getInterval().getAccidental()
			return accidental + numeral

		##########################
		# Transformation methods #
		##########################

		def transform_BL(self, p_accidental):	
			new_interval = self.getInterval().transform(p_accidental)
			new_pitch_class = [item for item in self.getParentIntervalList().getIntervals() if item != self.getInterval()] + [new_interval]
			new_pitch_class = IntervalListUtilities.sortIntervals(new_pitch_class)
			new_pitch_class = IntervalListUtilities.normalizeIntervals(new_pitch_class)

			if self.getParentIntervalList().getParentItem() is not None:
				new_reference_point = self.getParentIntervalList().getParentItem() + new_interval if self.getPosition_BL() == 1 else self.getParentIntervalList().getParentItem()

			else: new_reference_point = self.getParentIntervalList().getItems()[0].getReferencePoint_BL() + new_interval if self.getPosition_BL() == 1 else self.getParentIntervalList().getItems()[0].getReferencePoint_BL()

			new_attributes = self.getParentIntervalList().getAttributes()
			new_attributes["p_type_dict"] = IntervalListUtilities.intervalsToTypeDict(new_pitch_class)
			new_interval_list = type(self.getParentIntervalList())(new_reference_point, new_pitch_class, **new_attributes)
			return new_interval_list

		####################################################
		# Methods concerned with operations on scale items #
		####################################################

		def buildIntervalList_BL(self):
			new_interval_list = type(self.getParentIntervalList())(self, self.buildPitchClass())
			return new_interval_list

		def build_BL(self, object_type, p_item_1 = -1, p_item_2 = 2, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, p_preserve_parent = False, p_sublist = True, p_args = {}):
			if isinstance(p_item_1, int) and isinstance(p_item_2, int):
				new_reference_point = self if not p_preserve_parent or self.getParentIntervalList().getParentItem() is None else self.findInParent_BL()
				new_intervals = self.buildPitchClass_BL(p_item_1, p_item_2, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
				new_unaltered_intervals = IntervalListUtilities.deriveUnalteredIntervalsFromParent(self) if p_sublist else []
				p_args["p_sublist"] = p_sublist
				p_args["p_fixed_invert"] = self.getParentIntervalList().getFixedInvert()
				new_interval_list = object_type(new_reference_point, new_intervals, new_unaltered_intervals, **p_args)

			elif isinstance(p_item_1, list) and len(p_item_1) > 0 and (isinstance(p_item_1[0], int) or isinstance(p_item_1[0], Interval)):
				new_reference_point = self if not p_preserve_parent or self.getParentIntervalList().getParentItem() is None else self.findInParent_BL()
				new_intervals = self.buildPitchClass_BL(p_item_1, p_item_2, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
				new_unaltered_intervals = IntervalListUtilities.deriveUnalteredIntervalsFromParent(self) if p_sublist else []
				p_args["p_sublist"] = p_sublist
				p_args["p_fixed_invert"] = self.getParentIntervalList().getFixedInvert()
				new_interval_list = object_type(new_reference_point, new_intervals, new_unaltered_intervals, **p_args)
			else: 
				new_reference_point = self if not p_preserve_parent or self.getParentIntervalList().getParentItem() is None else self.findInParent_BL()
				p_args["p_sublist"] = p_sublist
				p_args["p_fixed_invert"] = self.getParentIntervalList().getFixedInvert()
				new_interval_list = object_type(new_reference_point, p_item_1, **p_args)

			return new_interval_list

		def buildPitchClass_BL(self, p_item_1 = -1, p_item_2 = 2, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, p_system = DEFAULT_SYSTEM):
			new_generic_intervals = []

			if isinstance(p_item_1, int) and isinstance(p_item_2, int):
				p_item_1 = len(self.getParentIntervalList().getIntervalsWhere_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)) if p_item_1 == -1 else p_item_1
				new_generic_intervals = [i + 1 for i in range(0, ((p_item_2 - 1) * (p_item_1 - 1)) + 1, p_item_2 - 1)]
				#new_generic_intervals = [i + 1 for i in range(0, (Interval(1, p_item_2 - 1) * p_item_1).getNumeral() + 2, p_item_2 - 1)]

			elif isinstance(p_item_1, list) and len(p_item_1) > 0 and (isinstance(p_item_1[0], int) or isinstance(p_item_1[0], Interval)):
				new_generic_intervals = p_item_1

			items = [self.add_BL(item, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp) for item in new_generic_intervals]
			result = items[0]
			
			for item in items:
				result += item

			return result.getIntervals()

		#################
		# Sugar methods #
		#################

		def transpose_BL(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True):
			return self.getParentIntervalList().transpose_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp).getItems()[self.getPosition_BL() - 1]

		def isUnAltered_BL(self): 
			return self.getInterval().simplify() in self.getParentIntervalList().getUnalteredIntervals()

		def isAltered_BL(self):
			return not self.isUnAltered_BL()

		def isOmitted_BL(self): 
			return self.isTemp() and (not self.findInParent_BL().isTemp() if self.getParentIntervalList().getParentItem() is not None else False)

		def resolve_BL(self):
			return self.add_BL(-self.getAlteration_BL())

		def getAlteration_BL(self):
			return self.getInterval().simplify() - [item for item in self.getParentIntervalList().getUnalteredIntervals() if item.getNumeral() == self.getInterval().simplify().getNumeral()][0]

		def getReferencePoint_BL(self): 
			return self.getParentIntervalList().getTonicTone() + self.getInterval()

		def getGenericInterval_BL(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args):
			ignore_parent = p_ignore_parent if p_ignore_parent is not None else not self.getParentIntervalList().isSublist()
			ignore_altered = p_ignore_altered if p_ignore_altered is not None else self.getParentIntervalList().isAltered()

			if not ignore_parent:
				reference_point_generic_interval = self.getParentIntervalList().getItems()[0].findInParent_BL().getGenericInterval_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args) if p_cascade_args else self.getParentIntervalList().getItems()[0].findInParent_BL().getGenericInterval_BL()
				generic_interval = self.findInParent_BL().getGenericInterval_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args) if p_cascade_args else self.findInParent_BL().getGenericInterval_BL()
				
				if isinstance(reference_point_generic_interval, list) or isinstance(generic_interval, list):
					reference_point_generic_portion = reference_point_generic_interval[0] if isinstance(reference_point_generic_interval, list) else reference_point_generic_interval
					reference_point_specific_portion = reference_point_generic_interval[1] if isinstance(reference_point_generic_interval, list) else P1
					generic_portion = generic_interval[0] if isinstance(generic_interval, list) else generic_interval
					specific_portion = generic_interval[1] if isinstance(generic_interval, list) else P1
					return [generic_portion - (reference_point_generic_portion - 1), specific_portion]
				
				return generic_interval - (reference_point_generic_interval - 1)

			if not self.isUnAltered_BL(): 
				return [self.resolve_BL().getGenericInterval_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args), self.getAlteration_BL()]

			if ignore_parent and not ignore_altered: 
				return self.getParentIntervalList().getItems().index(self) + 1
			else:
				new_intervals = self.getParentIntervalList().getIntervalsWhere_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
				return new_intervals.index(self.getInterval()) + 1
			
			'''
			reference_point = self.getParentIntervalList().getItems()[0]
			counter = 1
			new_item = reference_point

			while new_item.getInterval() != self.getInterval():
				counter += 1
				new_item = reference_point.add_BL(counter, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

				if new_item.getInterval() > self.getInterval(): 
					print("Error: Unable to find Generic Interval")
					return self.getInterval()
			
			return counter
			'''

		def getPosition_BL(self):
			return self.getParentIntervalList().getItems().index(self) + 1
			
		def getPositionInParent_BL(self): 
			return self.findInParent_BL().getPosition_BL()

		def findInParent_BL(self):
			if self.getParentIntervalList().getParentItem() != None: return self.getParentIntervalList().getParentItem().getParentIntervalList().__getitem__(self.getParentIntervalList().getParentItem().getInterval() + self.getInterval())
			else: return None

		def next_BL(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args):
			ignore_parent = p_ignore_parent if p_ignore_parent is not None else not self.getParentIntervalList().isSublist()
			ignore_altered = p_ignore_altered if p_ignore_altered is not None else self.getParentIntervalList().isAltered()

			if self.getParentIntervalList().getParentItem() is not None and not ignore_parent:
				new_item = self.findInParent_BL().next_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args if p_cascade_args else {})
				delta = new_item.getParentIntervalList().getItems()[0].getReferencePoint_BL() - self.getParentIntervalList().getItems()[0].getReferencePoint_BL()
				new_interval = new_item.getInterval() + delta - self.getInterval()
				new_item = self.add_BL(new_interval)

			elif self.getPosition_BL() == len(self.getParentIntervalList().getItems()): 
				if self.getParentIntervalList().getParentItem() is not None:
					new_reference_point = self.getParentIntervalList().getParentItem() + self.getParentIntervalList().getFixedInvert()

				else: new_reference_point = self.getParentIntervalList().getItems()[0].getReferencePoint_BL() + self.getParentIntervalList().getFixedInvert()
				
				new_attributes = self.getParentIntervalList().getAttributes()
				new_interval_list = type(self.getParentIntervalList())(new_reference_point, self.getParentIntervalList().getIntervals(), **new_attributes)
				new_item = new_interval_list.getItems()[0]

			else: new_item = self.getParentIntervalList().getItems()[(self.getPosition_BL() - 1) + 1]

			if self.isTemp() and p_remove_temp:
				new_interval_list = new_item.getParentIntervalList()

				if new_interval_list.getItemByInterval(self.getInterval()).getPosition_BL() != new_item.getPosition_BL():
					new_interval_list = new_interval_list.remove_BL(new_interval_list.getItemByInterval(self.getInterval()).getPosition_BL())
					new_item = new_interval_list.getItemByInterval(new_item.getInterval())

			if (not new_item.isUnAltered_BL()) and ignore_altered and ignore_parent:
				return new_item.next_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

			return new_item

		def previous_BL(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args):	
			ignore_parent = p_ignore_parent if p_ignore_parent is not None else not self.getParentIntervalList().isSublist()
			ignore_altered = p_ignore_altered if p_ignore_altered is not None else self.getParentIntervalList().isAltered()

			if self.getParentIntervalList().getParentItem() is not None and not ignore_parent:
				new_item = self.findInParent_BL().previous_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args if p_cascade_args else {})
				delta = new_item.getParentIntervalList().getItems()[0].getReferencePoint_BL() - self.getParentIntervalList().getItems()[0].getReferencePoint_BL()
				new_interval = new_item.getInterval() + delta - self.getInterval()
				new_item = self.add_BL(new_interval)

			elif self.getPosition_BL() == 1: 
				if self.getParentIntervalList().getParentItem() is not None:
					new_reference_point = self.getParentIntervalList().getParentItem() - self.getParentIntervalList().getFixedInvert()

				else: new_reference_point = self.getParentIntervalList().getItems()[0].getReferencePoint_BL() - self.getParentIntervalList().getFixedInvert()
				
				new_attributes = self.getParentIntervalList().getAttributes()
				new_interval_list = type(self.getParentIntervalList())(new_reference_point, self.getParentIntervalList().getIntervals(), **new_attributes)
				new_item = new_interval_list.getItems()[-1]

			else: new_item = self.getParentIntervalList().getItems()[(self.getPosition_BL() - 1) - 1]

			if self.isTemp() and p_remove_temp:
				new_interval_list = new_item.getParentIntervalList()

				if new_interval_list.getItemByInterval(self.getInterval()).getPosition_BL() != new_item.getPosition_BL():
					new_interval_list = new_interval_list.remove_BL(new_interval_list.getItemByInterval(self.getInterval()).getPosition_BL())
					new_item = new_interval_list.getItemByInterval(new_item.getInterval())

			if (not new_item.isUnAltered_BL()) and ignore_altered and ignore_parent:
				return new_item.previous_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

			return new_item

		###################
		# Wrapper methods #
		###################

		def __getattr__(self, p_attr): return self.getattr_BL(p_attr)

		def __repr__(self): return self.repr_BL()
		def __str__(self): return self.str_BL()

		def __eq__(self, p_other): return self.eq_BL(p_other)
		def __ne__(self, p_other): return self.ne_BL(p_other)

		def __add__(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): return self.add_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
		def __sub__(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): return self.sub_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)

		def getNumeralNotation(self): return self.getNumeralNotation_BL()
		def transform(self, p_accidental): return self.transform_BL(p_accidental)
		def buildIntervalList(self): return self.buildIntervalList_BL()
		def build(self, p_object_type, p_num_tones = 7, p_leap_size = 2, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, p_preserve_parent = False, p_sublist = True, p_args = {}): return self.build_BL(p_object_type, p_num_tones, p_leap_size, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, p_preserve_parent, p_sublist, p_args)
		def buildPitchClass(self, p_num_tones = -1, p_leap_size = 2, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, p_system = DEFAULT_SYSTEM): return self.buildPitchClass_BL(p_num_tones, p_leap_size, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, p_system)
		def transpose(self, p_other, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): return self.transpose_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
		def isUnAltered(self): return self.isUnAltered_BL()
		def isAltered(self): return self.isAltered_BL()
		def isOmitted(self): return self.isOmitted_BL()
		def resolve(self): return self.resolve_BL()
		def getAlteration(self): return self.getAlteration_BL()
		def getReferencePoint(self): return self.getReferencePoint_BL()	
		def getGenericInterval(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True): return self.getGenericInterval_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
		def getPosition(self): return self.getPosition_BL()
		def getPositionInParent(self): return self.getPositionInParent_BL()
		def findInParent(self): return self.findInParent_BL()
		def next(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args): return self.next_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)
		def previous(self, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True, *p_args): return self.previous_BL(p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp, *p_args)

		##############################
		# Overridable Business Logic #
		##############################

		def getAttributes(self): 
			return {
				"p_temp": self.isTemp()
			}

		#######################
		# Getters and Setters #
		#######################

		def getInterval(self): return self.interval
		def getParentIntervalList(self): return self.parent_interval_list
		def isTemp(self): return self.temp