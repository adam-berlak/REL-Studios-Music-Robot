import collections

from Configuration import *
from HelperMethods import *

from MusicCollections.IntervalListUtilities import *
from Components.IPitchedObject import * 

class IntervalList:

	def __init__(self, p_parent_item, p_intervals, p_type_dict = {}):
		self.parent_item = p_parent_item
		self.intervals = p_intervals
		self.type_dict = p_type_dict
		self.buildComponents()

	#####################################
	# Methods concerning class behavior #
	#####################################

	def repr_BL(self): 
		return self.str_BL()

	def str_BL(self):
		result = "<" + type(self).__name__ + " "
		for item in self.getItems(): result += str(item) + ", "
		return result[:-2] + ">"

	def getitem_BL(self, p_index): 
		if isinstance(p_index, slice):
			new_interval_list = IntervalListUtilities.normalizeIntervals(self.getIntervals()[p_index.start - 1:p_index.stop])
			new_scale = self.getitem_BL(p_index.start).findInParent().build_BL(type(self), new_interval_list)
			return new_scale

		if isinstance(p_index, tuple):
			items = [self.getitem_BL(1).add_BL(item) for item in p_index]
			result = items[0]
			
			for item in items[1:]:
				result += item

			return result
		
		else: return self.getItems()[0].add_BL(p_index)

	def contains_BL(self, p_other):
		if isinstance(p_other, Tone) or isinstance(p_other, Key): 
			return p_other.simplify() in [item.simplify() for item in self.getTones_BL()]

		if isinstance(p_other, int): 
			return Interval.getSimpleNumeral(p_other) in [item.getNumeral() for item in self.getIntervals()]

		if isinstance(p_other, Interval): 
			return p_other.simplify() in self.getIntervals()

		if issubclass(type(p_other), IntervalList): 
			return all(elem in self.getTones_BL() for elem in p_other.getTones())

		if issubclass(type(p_other), IntervalList.Item): 
			return p_other in self.getItems()

		if isinstance(p_other, list) and len(p_other) > 0 and isinstance(p_other[0], Interval): 
			return (True in [all(elem.simplify() in item.buildPitchClass_BL() for elem in p_other) for item in self.getItems()])

		return False

	##############
	# Comparison #
	##############

	def eq_BL(self, p_other): 
		return type(self) == type(p_other) and self.getIntervals() == p_other.getIntervals() and self.getTonicTone() == p_other.getTonicTone()

	def ne_BL(self, p_other): 
		return not self.eq_BL(p_other)

	##############
	# Arithmetic #
	##############

	def add_BL(self, p_other):
		if isinstance(p_other, str): 
			return str(self) + p_other

		if isinstance(p_other, int): 
			return (self.getitem_BL(1).add_BL(p_other)).build_BL(type(self), len(self.getIntervals()), 2)

		if isinstance(p_other, Interval): 
			new_scale = (self.getitem_BL(1).getTone() + p_other).build(type(self), self.getIntervals())
			if self.getParentItem() != None: new_scale.setParentItem((self.getParentItem().getParentIntervalList() + p_other)[self.getParentItem().getPosition()])
			return new_scale

		if issubclass(type(p_other), IntervalList.Item):
			new_intervals = self.getIntervals() + [self.getIntervals()[-1] + (p_other.getTone() - self.getItems()[-1].getTone())]
			new_intervals = IntervalListUtilities.sortIntervals(new_intervals)
			new_intervals = IntervalListUtilities.normalizeIntervals(new_intervals)
			new_intervals = IntervalListUtilities.scaleIntervalsByOrder(new_intervals)
			new_scale = type(self)(self.getItems()[0].getTone() if (p_other.getTone() - self.getItems()[0].getTone()) > P1 else p_other.getTone(), new_intervals, **self.getAttributes())
			return new_scale
		
		if issubclass(type(p_other), IntervalList):
			if len(p_other.getIntervals()) == 1: return self + p_other[1]
			return self.add_BL(p_other[1]) + p_other.remove_BL(1)

	def sub_BL(self, p_other):
		if isinstance(p_other, int): 
			return self.add_BL(-p_other)
			
		if isinstance(p_other, Interval): 
			return self.add_BL(-p_other)

	def radd_BL(self, p_other):
		if isinstance(p_other, str): 
			return p_other + self.str_BL()

	################################
	# Methods concerned with names #
	################################

	def printTones_BL(self):
		result = ""
		for tone in self.getTones_BL(): result = result + str(tone) + ", "
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
		new_scale = type(self)(self.getitem_BL(2).getTone() if p_item_index == 1 else self.getTonicTone(), IntervalListUtilities.normalizeIntervals(new_intervals))
		new_scale.setParentItem(self.getParentItem())
		return new_scale

	def addInterval_BL(self, p_interval, p_attributes = {}):
		new_pitch_class = self.getIntervals()[:]

		if p_interval not in new_pitch_class:
			new_pitch_class.append(p_interval)
			new_pitch_class.sort(key=lambda x: x.getSemitones())
			
		new_reference_point = self.getParentItem() if self.getParentItem() is not None else self.getitem_BL(1).getTone()
		new_scale = type(self)(new_reference_point, new_pitch_class, p_type_dict = {p_interval: p_attributes})
		return new_scale

	def replaceAtNumeralWith_BL(self, p_numeral, p_interval):
		list_items = [item for item in self.getIntervals() if item.getNumeral() == p_numeral]

		if len(list_items) != 0:
			index = self.getIntervals().index(list_items[0])
			new_scale_beginning = self.getIntervals()[:index]
			new_scale_beginning.append(p_interval)
			new_scale_ending = self.getIntervals()[index + 1:]
			new_scale_intervals = new_scale_beginning + new_scale_ending

		else: return self.addInterval_BL(p_interval)
		new_scale = type(self)(self.getitem_BL(1).getTone(), new_scale_intervals)
		new_scale.setParentItem(self.getParentItem())
		return new_scale

	#################
	# Sugar Methods #
	#################

	def getParentIntervalList_BL(self): return self.getParentItem().getParentIntervalList()
	def getNumerals_BL(self): return [item.getNumeral() for item in self.getIntervals()]
	def getSemitones_BL(self): return [item.getSemitones() for item in self.getIntervals()]
	def getIntervals_BL(self): return [item.getInterval() for item in self.getItems()]
	def getTones_BL(self): return [item.getTone() for item in self.getItems()]

	###################
	# Wrapper Methods #
	###################

	def __repr__(self): return self.repr_BL()
	def __str__(self): return self.str_BL()

	def __eq__(self, p_other): return self.eq_BL(p_other)
	def __ne__(self, p_other): return self.ne_BL(p_other)

	def __contains__(self, p_other): return self.contains_BL(p_other)
	def __getitem__(self, p_index): return self.getitem_BL(p_index)

	def __add__(self, p_other): return self.add_BL(p_other)
	def __sub__(self, p_other): return self.sub_BL(p_other)
	def __radd__(self, p_other): return self.radd_BL(p_other)

	def printTones(self): return self.printTones_BL()
	def getItemWhere(self, p_lambda_expression): return self.getItemWhere_BL(p_lambda_expression)
	def getItemByInterval(self, p_interval): return self.getItemByInterval_BL(p_interval)
	def getItemByNumeral(self, p_numeral): return self.getItemByNumeral_BL(p_numeral)
	def remove(self, p_item_index): return self.remove_BL(p_item_index)
	def addInterval(self, p_interval, p_attributes = {}): return self.addInterval_BL(p_interval, p_attributes)
	def replaceAtNumeralWith(self, p_numeral, p_interval): return self.replaceAtNumeralWith_BL(p_numeral, p_interval)
	def getParentIntervalList(self): return self.getParentIntervalList_BL()
	def getNumerals(self): return self.getNumerals_BL()
	def getSemitones(self): return self.getSemitones_BL()
	def getIntervals(self): return self.getIntervals_BL()
	def getTones(self): return self.getTones_BL()

	##############################
	# Overridable Business Logic #
	##############################

	def buildComponents(self):
		self.items = []

		for i in range(len(self.intervals)): 
			self.items.append(IntervalList.Item(self.intervals[i], self, **self.type_dict[self.intervals[i]] if self.intervals[i] in self.type_dict.keys() else {}))

	def getAttributes(self): return {}

	#######################
	# Getters and Setters #
	#######################

	def getItems(self): return self.items
	def getTonicTone(self): return self.tonic_tone
	def getParentItem(self): return self.parent_item
	def getTypeDict(self): return self.type_dict

	def setParentItem(self, p_parent_item): 
		if p_parent_item == None: return
		self.parent_item = p_parent_item

	class Item:
		
		def __init__(self, p_interval, p_parent_scale):
			self.interval = p_interval
			self.parent_scale = p_parent_scale

		#####################################
		# Methods concerning class behavior #
		#####################################

		def repr_BL(self): 
			return self.str_BL()

		def str_BL(self):
			if not DEGREE_SIMPLE_REPRESENTATION: 
				return self.getNumeral() + ": " + str(self.getTone())
			else: 
				return str(self.getTone())

		##############
		# Comparison #
		##############

		def eq_BL(self, p_other): 
			return type(self) == type(p_other) and self.getInterval() == p_other.getInterval() and self.getTone() == p_other.getTone()

		def ne_BL(self, p_other): 
			return not self.eq_BL(p_other)

		##############
		# Arithmetic #
		##############

		def add_BL(self, p_other):
			if isinstance(p_other, str): 
				return str(self) + p_other

			if isinstance(p_other, int):	
				if abs(p_other) == 1: return self
				return self.next_BL().add_BL(p_other - 1) if p_other > 0 else self.previous_BL().add_BL(p_other + 1)
			
			if isinstance(p_other, Interval):
				if abs(p_other) == P1: return self
				new_interval = self.getInterval() + p_other

				if new_interval < P1:
					return (self.getParentIntervalList().sub_BL(P8)).getitem_BL(self.getPosition()) - (p_other - P8)
				
				if new_interval >= self.getParentIntervalList().getIntervals()[-1].roof():
					return (self.getParentIntervalList().add_BL(P8)).getitem_BL(self.getPosition()) + (p_other - P8)

				if new_interval not in self.getParentIntervalList():
					if IntervalListUtilities.isDistinct(self.getParentIntervalList().getIntervals()):
						if new_interval.getNumeral() == 1: return self.getParentIntervalList()[1].transform(new_interval.getAccidental())[1]
						elif new_interval.getNumeral() in self.getParentIntervalList().getNumerals(): return self.getParentIntervalList().replaceAtNumeralWith(new_interval.getNumeral(), new_interval).getItemByInterval(new_interval)
						else: return self.getParentIntervalList().addInterval(new_interval).getItemByInterval(new_interval)
					else: return self.getParentIntervalList().addInterval(new_interval).getItemByInterval(new_interval)
				else: return self.getParentIntervalList().getItemByInterval(new_interval)

			if issubclass(type(p_other), IntervalList):
				new_scale = (self.add_BL(p_other[1])) + (p_other[2:len(p_other.getIntervals())])
				return new_scale
			
			if issubclass(type(p_other), IntervalList.Item):
				new_intervals = [P1, p_other.getTone() - self.getTone()]
				new_intervals = IntervalListUtilities.sortIntervals(new_intervals)
				new_intervals = IntervalListUtilities.normalizeIntervals(new_intervals)
				new_intervals = IntervalListUtilities.scaleIntervalsByOrder(new_intervals)
				new_scale = type(self.getParentIntervalList())(self.getTone() if (p_other.getTone() - self.getTone()) > P1 else p_other.getTone(), new_intervals)
				return new_scale

		def sub_BL(self, p_other):
			if isinstance(p_other, int):
				return self.add_BL(-p_other)

			if isinstance(p_other, Interval):
				return self.add_BL(-p_other)

			if issubclass(type(p_other), IntervalList.Item): 
				return self.getTone() - p_other.getTone()
		
		def __radd__(self, p_other):
			if isinstance(p_other, str): return p_other + str(self)

		################################
		# Methods concerned with names #
		################################

		def getNumeral_BL(self):
			numeral = intToRoman(self.getInterval().getNumeral()) 
			if self.buildPitchClass(2, 3) == [P1, m3]: numeral = numeral.lower()
			accidental = self.getInterval().getAccidental()
			return accidental + numeral

		##########################
		# Transformation methods #
		##########################

		def transform_BL(self, p_accidental):	
			new_interval = self.getInterval().transform(p_accidental)
			new_pitch_class = self.getParentIntervalList().getIntervals()[:]
			new_pitch_class = [item for item in new_pitch_class if item != self.getInterval()]
			new_pitch_class.append(new_interval)
			new_pitch_class.sort(key=lambda x: x.getNumeral())

			if self.getPosition() == 1:
				difference = new_interval.getSemitones()
				new_pitch_class = [Interval(item.getSemitones() - difference, item.getNumeral()) for item in new_pitch_class]
				return type(self.getParentIntervalList())(self.getParentIntervalList()[1].getTone() + Interval(difference, 1), new_pitch_class)

			return type(self.getParentIntervalList())(self.getParentIntervalList()[1].getTone(), new_pitch_class)

		#############################################################
		# Methods concerned with measuring distance between items #
		#############################################################

		def distanceFrom_BL(self, p_other):
			if self.getInterval().getSemitones() < p_other.getInterval().getSemitones(): return p_other.getInterval() - self.getInterval()
			else: return self.getInterval() - p_other.getInterval() 

		def distanceFromNext_BL(self, p_other):	
			if self.getInterval().getSemitones() < p_other.getInterval().getSemitones(): return p_other.getInterval() - self.getInterval()
			else: return ((self.getParentIntervalList().getIntervals()[-1] + (P8 - self.getParentIntervalList().getIntervals()[-1].simplify())) - self.getInterval()) + p_other.getInterval()

		######################################################
		# Methods concerned with operations on scale items #
		######################################################

		def build_BL(self, object_type, p_item_1 = 4, p_item_2 = 3, p_args = {}):
			if isinstance(p_item_1, list) and len(p_item_1) > 0 and isinstance(p_item_1[0], int):
				child_object = object_type(self, [(self.distanceFromNext_BL(self + item)).simplify() for item in p_item_1], **p_args)
			elif isinstance(p_item_1, int) and isinstance(p_item_2, int):
				child_object = object_type(self, self.buildPitchClass_BL(p_item_1, p_item_2)[:p_item_1], **p_args)
			else:
				child_object = object_type(self, p_item_1, **p_args)

			return child_object

		def buildPitchClass_BL(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM):
			if p_num_tones == -1: p_num_tones = len(self.getParentIntervalList().getIntervals())
			child_intervals = []
			p_leap_size = p_leap_size - 1
			next_item = self
			counter = 0

			while (counter < p_num_tones - 1):
				for j in range(p_leap_size): next_item = next_item.next_BL()
				new_interval = self.distanceFromNext_BL(next_item)
				child_intervals.append(new_interval)
				counter = counter + 1
			
			return IntervalListUtilities.scaleIntervalsByOrder([P1] + child_intervals)

		#################
		# Sugar methods #
		#################

		def getPosition_BL(self): return self.getParentIntervalList().getItems().index(self) + 1
		def getPositionInParent_BL(self): return self.findInParent().getPosition()

		def findInParent_BL(self):
			if self.getParentIntervalList().getParentItem() != None: return self.getParentIntervalList().getParentItem().getParentIntervalList().__getitem__(self.getParentIntervalList().getParentItem().getInterval() + self.getInterval())
			else: return self

		def next_BL(self):
			if self.getPosition_BL() == len(self.getParentIntervalList().getItems()): 
				new_tonic_tone = self.getParentIntervalList().getItems()[0].getTone() + self.getParentIntervalList().getItems()[-1].getInterval().roof()
				new_object = type(self.getParentIntervalList())(new_tonic_tone, self.getParentIntervalList().getIntervals())
				if self.getParentIntervalList().getParentItem() != None: new_object.setParentItem(self.getParentIntervalList().getParentItem())
				return new_object.getItems()[0]

			return self.getParentIntervalList().getItems()[(self.getPosition_BL() - 1) + 1]

		def previous_BL(self):
			if self.getPosition_BL() == 1: 
				new_tonic_tone = self.getParentIntervalList().getItems()[0].getTone() - self.getParentIntervalList().getItems()[-1].getInterval().roof()
				new_object = type(self.getParentIntervalList())(new_tonic_tone, self.getParentIntervalList().getIntervals())
				if self.getParentIntervalList().getParentItem() != None: new_object.setParentItem(self.getParentIntervalList().getParentItem())
				return new_object.getItems()[-1]

			return self.getParentIntervalList().getItems()[(self.getPosition_BL() - 1) - 1]

		###################
		# Wrapper methods #
		###################

		def __repr__(self): return self.repr_BL()
		def __str__(self): return self.str_BL()

		def __eq__(self, p_other): return self.eq_BL(p_other)
		def __ne__(self, p_other): return self.ne_BL(p_other)

		def __add__(self, p_other): return self.add_BL(p_other)
		def __sub__(self, p_other): return self.sub_BL(p_other)

		def getNumeral(self): return self.getNumeral_BL()
		def transform(self, p_accidental): return self.transform_BL(p_accidental)
		def distanceFrom(self, p_other): return self.distanceFrom_BL(p_other)
		def distanceFromNext(self, p_other): return self.distanceFromNext_BL(p_other)
		def build(self, p_object_type, p_num_tones = 4, p_leap_size = 3, p_args = {}): return self.build_BL(p_object_type, p_num_tones, p_leap_size, p_args)
		def buildIntervalList(self): return self.buildIntervalList_BL()
		def buildIntervalListWithIntervals(self, p_intervals): return self.buildIntervalListWithIntervals_BL(p_intervals)
		def buildPitchClass(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM): return self.buildPitchClass_BL(p_num_tones, p_leap_size, p_system)
		def getPosition(self): return self.getPosition_BL()
		def getPositionInParent(self): return self.getPositionInParent_BL()
		def findInParent(self): return self.findInParent_BL()
		def next(self):	return self.next_BL()
		def previous(self): return self.previous_BL()

		#######################
		# Getters and Setters #
		#######################

		def getTone(self): return self.getParentIntervalList().getTonicTone() + self.getInterval()
		def getInterval(self): return self.interval
		def getParentIntervalList(self): return self.parent_scale