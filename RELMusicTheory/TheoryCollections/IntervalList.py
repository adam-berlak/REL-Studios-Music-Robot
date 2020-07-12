import collections

from Configuration import *

from TheoryCollections.IntervalListUtilities import *
from TheoryComponents.IPitchedObject import * 

class IntervalList:

	def __init__(self, p_item_1, p_intervals, p_type_dict = {}):
		if issubclass(type(p_item_1), IntervalList.Item):	
			self.parent_item = p_item_1
			self.tonic_tone = p_parent_item.getReferencePoint_BL()
			self.intervals = p_intervals
			self.type_dict = p_type_dict

		elif isinstance(p_item_1, IPitchedObject):
			self.parent_item = None
			self.tonic_tone = p_item_1
			self.intervals = p_intervals
			self.type_dict = p_type_dict

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

	def getitem_BL(self, p_index): 
		if isinstance(p_index, slice):
			new_intervals = IntervalListUtilities.normalizeIntervals(self.getIntervals()[p_index.start - 1:p_index.stop])
			new_interval_list = self.getitem_BL(p_index.start).findInParent().build_BL(type(self), new_intervals)
			return new_interval_list

		if isinstance(p_index, tuple):
			items = [self.getItems()[0].add_BL(item) for item in p_index]
			result = items[0]
			
			for item in items[1:]:
				result += item

			return result
		
		else: return self.getItems()[0].add_BL(p_index)

	def contains_BL(self, p_other):
		if isinstance(p_other, IPitchedObject): 
			return p_other.simplify() in [item.simplify() for item in self.getReferencePoints_BL()]

		elif isinstance(p_other, Tone): 
			return p_other.simplify() in [item.simplify() for item in self.getTones()]

		elif isinstance(p_other, int): 
			return Interval.getSimpleNumeral(p_other) in [item.getNumeral() for item in self.getIntervals()]

		elif isinstance(p_other, Interval): 
			return p_other.simplify() in IntervalListUtilities.simplifyIntervals(self.getIntervals())
			
		elif isinstance(p_other, list) and len(p_other) > 0 and isinstance(p_other[0], Interval): 
			return any(all(item.build(type(self)).contains_BL(elem) for elem in p_other) for item in self.getItems())

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

	def add_BL(self, p_other):
		if isinstance(p_other, str): 
			return str(self) + p_other

		if isinstance(p_other, int): 
			return (self.getItems()[0].add_BL(p_other)).build_BL(type(self), len(self.getIntervals()), 2, self.getAttributes())

		if isinstance(p_other, Interval): 
			new_interval_list = (self.getItems()[0].getReferencePoint_BL() + p_other).build(type(self), self.getIntervals(), self.getAttributes())
			if self.getParentItem() != None: new_interval_list.setParentItem((self.getParentIntervalList_BL().add_BL(p_other)).getitem_BL(self.getParentItem().getPosition()))
			return new_interval_list

		if issubclass(type(p_other), IntervalList.Item):
			new_intervals = self.getIntervals() + [self.getIntervals()[-1] + (p_other.getReferencePoint_BL() - self.getItems()[-1].getReferencePoint_BL())]
			new_intervals = IntervalListUtilities.sortIntervals(new_intervals)
			new_intervals = IntervalListUtilities.normalizeIntervals(new_intervals)
			new_intervals = IntervalListUtilities.scaleIntervalsByOrder(new_intervals)
			new_interval_list = type(self)(self.getItems()[0].getReferencePoint_BL() if (p_other.getReferencePoint_BL() - self.getItems()[0].getReferencePoint_BL()) > P1 else p_other.getReferencePoint_BL(), new_intervals, **self.getAttributes())
			return new_interval_list
		
		if issubclass(type(p_other), IntervalList):
			if len(p_other.getIntervals()) == 1: return self.add_BL(p_other.getItems()[0])
			return self.add_BL(p_other.getItems()[0]).add_BL(p_other.remove_BL(1))

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
		new_interval_list = type(self)(self.getitem_BL(2).getReferencePoint_BL() if p_item_index == 1 else self.getTonicTone(), IntervalListUtilities.normalizeIntervals(new_intervals))
		new_interval_list.setParentItem(self.getParentItem())
		return new_interval_list

	def addInterval_BL(self, p_interval, p_attributes = {}):
		new_pitch_class = self.getIntervals()[:]

		if p_interval not in new_pitch_class:
			new_pitch_class.append(p_interval)
			new_pitch_class = IntervalListUtilities.sortIntervals(new_pitch_class)
			new_pitch_class = IntervalListUtilities.normalizeIntervals(new_pitch_class)

		if self.getParentItem() is not None:
			new_reference_point = self.getParentItem() if p_interval > P1 else self.getParentItem() + p_interval
		else:
			new_reference_point = self.getItems()[0].getReferencePoint() if p_interval > P1 else self.getItems()[0].getReferencePoint() + p_interval
		
		new_attributes = self.getAttributes()
		new_type_dict = new_attributes["p_type_dict"]
		new_type_dict[p_interval] = p_attributes
		if p_interval.getSemitones() < 0: new_type_dict = IntervalListUtilities.normalizeTypeDict(new_type_dict, p_interval)
		new_attributes["p_type_dict"] = new_type_dict
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
		new_interval_list = type(self)(self.getItems()[0].getReferencePoint_BL(), new_interval_list_intervals)
		new_interval_list.setParentItem(self.getParentItem())
		return new_interval_list

	#################
	# Sugar Methods #
	#################

	def getParentIntervalList_BL(self): 
		return self.getParentItem().getParentIntervalList()

	def getNumerals_BL(self): 
		return [item.getNumeral() for item in self.getIntervals()]

	def getSemitones_BL(self): 
		return [item.getSemitones() for item in self.getIntervals()]

	def getIntervals_BL(self): 
		return [item.getInterval() for item in self.getItems()]

	def getReferencePoints_BL(self): 
		return [item.getReferencePoint_BL() for item in self.getItems()]

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
	def getReferencePoints(self): return self.getReferencePoints_BL()
	

	##############################
	# Overridable Business Logic #
	##############################

	def buildItems(self):
		self.items = []

		for i in range(len(self.intervals)): 
			self.items.append(IntervalList.Item(self.intervals[i], self, **self.type_dict[self.intervals[i]] if self.intervals[i] in self.type_dict.keys() else {}))

	def getAttributes(self): return {}

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
	def getParentItem(self): return self.parent_item

	def setItems(self, p_items): self.items = p_items
	def setTonicTone(self, p_tonic_tone): tonic_tone = p_tonic_tone
	def setParentItem(self, p_parent_item): 
		self.parent_item = p_parent_item
		self.tonic_tone = p_parent_item.getReferencePoint_BL()

	class Item:
		
		def __init__(self, p_interval, p_parent_interval_list):
			self.interval = p_interval
			self.parent_interval_list = p_parent_interval_list

		def getattr_BL(self, p_attr):
			return getattr(self.getReferencePoint_BL(), p_attr)

		#####################################
		# Methods concerning class behavior #
		#####################################

		def repr_BL(self): 
			return self.str_BL()

		def str_BL(self):
			if not DEGREE_SIMPLE_REPRESENTATION: 
				return self.getNumeral() + ": " + str(self.getReferencePoint_BL())

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
					return (self.getParentIntervalList().sub_BL(P8)).getitem_BL(self.getPosition()).sub_BL(p_other - P8)
				
				if new_interval >= self.getParentIntervalList().getIntervals()[-1].roof():
					return (self.getParentIntervalList().add_BL(P8)).getitem_BL(self.getPosition()).add_BL(p_other - P8)

				if new_interval not in self.getParentIntervalList():
					if IntervalListUtilities.isDistinct(self.getParentIntervalList().getIntervals()):
						if new_interval.getNumeral() == 1: return self.getParentIntervalList().getItems()[0].transform(new_interval.getAccidental()).getItems()[0]
						elif new_interval.getNumeral() in self.getParentIntervalList().getNumerals(): return self.getParentIntervalList().replaceAtNumeralWith(new_interval.getNumeral(), new_interval).getItemByInterval(new_interval)
						else: return self.getParentIntervalList().addInterval(new_interval).getItemByInterval(new_interval)
					else: return self.getParentIntervalList().addInterval(new_interval).getItemByInterval(new_interval)
				else: return self.getParentIntervalList().getItemByInterval(new_interval)

			if issubclass(type(p_other), IntervalList):
				new_interval_list = (self.add_BL(p_other.getItems()[0])).add_BL(p_other.getitem_BL(slice(2, len(p_other.getIntervals()), None)))
				return new_interval_list
			
			if issubclass(type(p_other), IntervalList.Item):
				new_intervals = [P1, p_other.getReferencePoint_BL() - self.getReferencePoint_BL()]
				new_intervals = IntervalListUtilities.sortIntervals(new_intervals)
				new_intervals = IntervalListUtilities.normalizeIntervals(new_intervals)
				new_intervals = IntervalListUtilities.scaleIntervalsByOrder(new_intervals)
				new_reference_point = self.getReferencePoint_BL() if (p_other.getReferencePoint_BL() - self.getReferencePoint_BL()) > P1 else p_other.getReferencePoint_BL()
				new_interval_list = type(self.getParentIntervalList())(new_reference_point, new_intervals)
				return new_interval_list

		def sub_BL(self, p_other):
			if isinstance(p_other, int):
				return self.add_BL(-p_other)

			if isinstance(p_other, Interval):
				return self.add_BL(-p_other)

			if issubclass(type(p_other), IntervalList.Item): 
				return self.getReferencePoint_BL() - p_other.getReferencePoint_BL()
		
		def __radd__(self, p_other):
			if isinstance(p_other, str): 
				return p_other + str(self)

		################################
		# Methods concerned with names #
		################################

		def getNumeral_BL(self):
			numeral = Interval.intToRoman(self.getInterval().getNumeral()) 
			if self.buildPitchClass(2, 3) == [P1, m3]: numeral = numeral.lower()
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
				new_reference_point = self.getParentIntervalList().getParentItem() + new_interval if self.getPosition() == 1 else self.getParentIntervalList().getParentItem()
			else:
				new_reference_point = self.getParentIntervalList().getItems()[0].getReferencePoint_BL() + new_interval if self.getPosition() == 1 else self.getParentIntervalList().getItems()[0].getReferencePoint_BL()

			new_attributes = self.getParentIntervalList().getAttributes()
			new_type_dict = new_attributes["p_type_dict"]
			new_type_dict.pop(self.getInterval())
			new_type_dict[new_interval] = self.getAttributes()
			if self.getPosition() == 1: new_type_dict = IntervalListUtilities.normalizeTypeDict(new_type_dict, new_interval)
			new_attributes["p_type_dict"] = new_type_dict
			return type(self.getParentIntervalList())(new_reference_point, new_pitch_class, **new_attributes)

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
				child_object = object_type(self, [(self.distanceFromNext_BL(self.add_BL(item))).simplify() for item in p_item_1], **p_args)
				
			elif isinstance(p_item_1, int) and isinstance(p_item_2, int):
				child_object = object_type(self, self.buildPitchClass_BL(p_item_1, p_item_2)[:p_item_1], **p_args)

			else: child_object = object_type(self, p_item_1, **p_args)

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

		def getTones_BL(self):
			return [item.getTone() for item in self.getReferencePoints_BL()]

		def getReferencePoint_BL(self): 
			return self.getParentIntervalList().getTonicTone() + self.getInterval()

		def getPosition_BL(self): 
			return self.getParentIntervalList().getItems().index(self) + 1
			
		def getPositionInParent_BL(self): 
			return self.findInParent().getPosition()

		def findInParent_BL(self):
			if self.getParentIntervalList().getParentItem() != None: return self.getParentIntervalList().getParentItem().getParentIntervalList().__getitem__(self.getParentIntervalList().getParentItem().getInterval() + self.getInterval())
			else: return self

		def next_BL(self):
			if self.getPosition_BL() == len(self.getParentIntervalList().getItems()): 
				if self.getParentIntervalList().getParentItem() is not None:
					new_reference_point = self.getParentIntervalList().getParentItem() + self.getParentIntervalList().getItems()[-1].getInterval().roof()
				else:
					new_reference_point = self.getParentIntervalList().getItems()[0].getReferencePoint_BL() + self.getParentIntervalList().getItems()[-1].getInterval().roof()

				new_attributes = self.getParentIntervalList().getAttributes()
				new_object = type(self.getParentIntervalList())(new_reference_point, self.getParentIntervalList().getIntervals(), **new_attributes)
				return new_object.getItems()[0]

			return self.getParentIntervalList().getItems()[(self.getPosition_BL() - 1) + 1]

		def previous_BL(self):
			if self.getPosition_BL() == 1: 
				if self.getParentIntervalList().getParentItem() is not None:
					new_reference_point = self.getParentIntervalList().getParentItem() - self.getParentIntervalList().getItems()[-1].getInterval().roof()
				else:
					new_reference_point = self.getParentIntervalList().getItems()[0].getReferencePoint_BL() - self.getParentIntervalList().getItems()[-1].getInterval().roof()

				new_attributes = self.getParentIntervalList().getAttributes()
				new_object = type(self.getParentIntervalList())(new_reference_point, self.getParentIntervalList().getIntervals())
				return new_object.getItems()[-1]

			return self.getParentIntervalList().getItems()[(self.getPosition_BL() - 1) - 1]

		###################
		# Wrapper methods #
		###################

		def __getattr__(self, p_attr): return self.getattr_BL(p_attr)

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
		def buildPitchClass(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM): return self.buildPitchClass_BL(p_num_tones, p_leap_size, p_system)
		def getTones(self): return self.getTones_BL()
		def getReferencePoint(self): return self.getReferencePoint_BL()
		def getPosition(self): return self.getPosition_BL()
		def getPositionInParent(self): return self.getPositionInParent_BL()
		def findInParent(self): return self.findInParent_BL()
		def next(self):	return self.next_BL()
		def previous(self): return self.previous_BL()

		##############################
		# Overridable Business Logic #
		##############################

		def getAttributes(self): 
			return {}

		#######################
		# Getters and Setters #
		#######################

		def getInterval(self): return self.interval
		def getParentIntervalList(self): return self.parent_interval_list