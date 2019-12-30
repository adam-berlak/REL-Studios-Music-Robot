import re
import collections
import itertools
import statistics

from Configuration import *
from HelperMethods import *

class Scale:

	def __init__(self, p_item_1, p_item_2 = -1):

		if (isinstance(p_item_1, Scale)): 
			scale = p_item_1
			p_tonic_tone = scale[1].getTone()
			p_item = scale.getIntervals()

		if (isinstance(p_item_1, list)): 
			if (isinstance(p_item_1[0], Tone)): 
				intervals = Scale.tonesToPitchClass(p_item_1)
				p_item_1 = p_item_1[0]

		elif (isinstance(p_item_2, list)):
			if (isinstance(p_item_2[0], Interval)): intervals = p_item_2
			if (isinstance(p_item_2[0], int)): intervals = Scale.scaleStepsToPitchClass(p_item_2)

		elif (isinstance(p_item_2, int)): intervals = Scale.decimalToPitchClass(p_item_2)

		self.tonic_tone = p_item_1
		self.parent_degree = None
		self.degrees = []

		for i in range(len(intervals)): self.degrees.append(type(self)._Degree(intervals[i], self))

	#####################################
	# Methods concerning class behavior #
	#####################################

	def __repr__logic(self): return self.__str__logic()
	
	def __str__logic(self):
		result = "<"
		for degree in self.getDegrees(): result = result + str(degree) + ", "
		return result[:-2] + ">"

	def __getitem__logic(self, p_index): 
		
		if (isinstance(p_index, slice)):
			if (p_index.stop == 0): return type(self)(self.getTonicTone(), [])
			new_interval_list = (self.__add__logic(p_index.start)).getIntervals()[:(p_index.stop + 1) - p_index.start]
			new_scale = self.__getitem__logic(p_index.start)._Degree__findInParent()._Degree__build(type(self), new_interval_list)
			return new_scale
		
		else: return self.getDegrees()[0]._Degree__add__logic(p_index)
	
	def __contains__logic(self, p_other):
		if (isinstance(p_other, Tone)): return p_other in self.__getTones()
		if (isinstance(p_other, Interval)): return p_other.simplify() in self.getIntervals()
		if (isinstance(p_other, Scale)): return all(elem in self.__getTones() for elem in p_other.getTones())
		if (isinstance(p_other, Scale._Degree)): return p_other in self.getDegrees()
		if (isinstance(p_other, list) and isinstance(p_other[0], Interval)): return (True in [all(elem.simplify() in degree._Degree__buildPitchClass() for elem in p_other) for degree in self.getDegrees()])
		return False
	
	##############
	# Comparison #
	##############

	def __eq__logic(self, p_other): return (type(self) == type(p_other)) and ((self.getIntervals() == p_other.getIntervals()) and (self.getTonicTone() == p_other.getTonicTone()))
	def __ne__logic(self, p_other): return not (self.__eq__logic(p_other))

	##############
	# Arithmetic #
	##############

	def __add__logic(self, p_other):

		try:
			if (isinstance(p_other, str)): return str(self) + p_other
			if (isinstance(p_other, int)): return (self.__getitem__logic(1)._Degree__add__logic(p_other))._Degree__build(type(self), len(self.getIntervals()), 2)
			if (isinstance(p_other, Interval)): return (self.__getitem__logic(1)._Degree__add__logic(p_other))._Degree__build(type(self), self.getIntervals())

			if (isinstance(p_other, Scale._Degree)):
				new_intervals = self.getIntervals()
				new_intervals.append(p_other.getInterval() + (p_other.getParentScale()[1].getTone() - self[1].getTone()))
				new_intervals = Scale.scaleIntervalsByOrder(new_intervals)
				new_scale = type(self)(self.__getitem__logic(1).getTone(), new_intervals)

				if (self.getParentDegree() != None): new_scale.setParentDegree(self.getParentDegree())
				return new_scale
			
			if (isinstance(p_other, Scale)):
				new_intervals = self.getIntervals()
				other_intervals = [item + (p_other[1].getTone() - self.__getitem__logic(1).getTone()) for item in p_other.getIntervals()]
				new_intervals = new_intervals + other_intervals
				new_intervals = Scale.scaleIntervalsByOrder(new_intervals)
				new_scale = type(self)(self.__getitem__logic(1).getTone(), new_intervals)

				if (self.getParentDegree() != None): new_scale.setParentDegree(self.getParentDegree())
				return new_scale

		except: print("Error: Failed to add " + str(p_other) + " to " + str(self))

	def __sub__logic(self, p_other):
		
		try:
			if (isinstance(p_other, int)): return (self.__getitem__logic(1)._Degree__sub__logic(p_other))._Degree__build(type(self), len(self.getIntervals()), 2)
			if (isinstance(p_other, Interval)): return (self.__getitem__logic(1)._Degree__sub__logic(p_other))._Degree__build(type(self), self.getIntervals())

		except: print("Error: Failed to subtract " + str(p_other) + " from " + str(self))

	def __radd__logic(self, p_other):
		if (isinstance(p_other, str)): return p_other + self.__str__logic()

	################################
	# Methods concerned with names #
	################################

	def __getName(self): return scale_names[Scale.pitchClassToDecimal(self.getIntervals())]

	def __getModeNames(self): return [(self.__add__logic(item + 1)).__getName() for item in range(len(self.getIntervals()))]

	def __printTones(self):
		result = ""
		for tone in self.__getTones(): result = result + str(tone) + ", "
		return "[" + result[:-2] + "]"

	##########################
	# Transformation methods #
	##########################

	def __addInterval(self, p_interval):
		new_pitch_class = self.getIntervals()[:]
		new_pitch_class.append(p_interval)
		new_pitch_class.sort(key=lambda x: x.getSemitones())
		new_scale = type(self)(self.__getitem__logic(1).getTone(), new_pitch_class)

		if (self.getParentDegree() != None): new_scale.setParentDegree(self.getParentDegree())
		return new_scale

	def __replaceAtNumeralWith(self, p_numeral, p_interval):
		list_items = [item for item in self.getIntervals() if item.getNumeral() == p_numeral]

		if (len(list_items) != 0):
			index = self.getIntervals().index(list_items[0])
			new_scale_beginning = self.getIntervals()[:index]
			new_scale_beginning.append(p_interval)
			new_scale_ending = self.getIntervals()[index + 1:]
			new_scale_intervals = new_scale_beginning + new_scale_ending

		else: return self.__addInterval(p_interval)
		new_scale = type(self)(self.__getitem__logic(1).getTone(), new_scale_intervals)

		if (self.getParentDegree() != None): new_scale.setParentDegree(self.getParentDegree())
		return new_scale

	#################
	# Sugar Methods #
	#################

	def __getParallelScale(self):
		if (self.__getitem__logic(1)._Degree__buildPitchClass(2, 3) == [P1, m3]): return self.__getitem__logic(1)._Degree__buildScaleWithIntervals((self.__sub__logic(6)).getIntervals())
		elif (self.__getitem__logic(1)._Degree__buildPitchClass(2, 3) == [P1, M3]): return self.__getitem__logic(1)._Degree__buildScaleWithIntervals((self.__add__logic(6)).getIntervals())
		else: return self

	def __getRelativeScale(self):
		if (self.__getitem__logic(1)._Degree__buildPitchClass(2, 3) == [P1, m3]): return (self.__sub__logic(6))
		elif (self.__getitem__logic(1)._Degree__buildPitchClass(2, 3) == [P1, M3]): return (self.__add__logic(6))		
		else: return self

	def __getNegativeScale(self, p_axis_point = 3): 
		new_scale = Scale((self.__getitem__logic(p_axis_point)._Degree__add__logic(3)).getTone(), Scale.scaleStepsToPitchClass(Scale.pitchClassToScaleSteps((self[p_axis_point] - 3).buildPitchClass())[::-1]))
		if (self.getParentDegree() != None): new_scale.setParentDegree(self.getParentDegree())
		return new_scale

	def __isDistinct(self): return (len([item.simplify().getNumeral() for item in self.getIntervals()]) == len(set([item.simplify().getNumeral() for item in self.getIntervals()])))

	def __transpose(self, p_interval): return (self.__add__logic(p_interval))
	def __rotate(self): return (self.__transpose(2))

	def __getRoot(self): return self.__getitem__logic(1)
	def __getParentScale(self): return self.getParentDegree().getParentScale()
	def __getNumerals(self): return [item.getNumeral() for item in self.getIntervals()]
	def __getSemitones(self): return [item.getSemitones() for item in self.getIntervals()]
	def __getIntervals(self): return [item.getInterval() for item in self.getDegrees()]
	def __getTones(self): return [item.getTone() for item in self.getDegrees()]
	def __getDegreeByInterval(self, p_interval): return [item for item in self.getDegrees() if item.getInterval() == p_interval][0]
	def __getDegreeByNumeral(self, p_numeral): return [item for item in self.getDegrees() if item.getInterval().getNumeral() == p_numeral][0]

	###################
	# Wrapper Methods #
	###################

	def __repr__(self): return self.__repr__logic()
	def __str__(self): return self.__str__logic()

	def __eq__(self, p_other): return self.__eq__logic(p_other)
	def __ne__(self, p_other): return self.__ne__logic(p_other)

	def __contains__(self, p_other): return self.__contains__logic(p_other)
	def __getitem__(self, p_index): return self.__getitem__logic(p_index)

	def __add__(self, p_other): return self.__add__logic(p_other)
	def __sub__(self, p_other): return self.__sub__logic(p_other)
	def __radd__(self, p_other): return self.__radd__logic(p_other)

	def getName(self): return self.__getName()
	def getModeNames(self): return self.__getModeNames()
	def printTones(self): return self.__printTones()
	def addInterval(self, p_interval): return self.__addInterval(p_interval)
	def replaceAtNumeralWith(self, p_numeral, p_interval): return self.__replaceAtNumeralWith(p_numeral, p_interval)
	def getParallelScale(self): return self.__getParallelScale()
	def getRelativeScale(self): return self.__getRelativeScale()
	def getNegativeScale(self, p_axis_point = 3): return self.__getNegativeScale(p_axis_point)
	def transpose(self, p_interval): return self.__transpose(p_interval)
	def rotate(self): return self.__rotate()
	def getRoot(self): return self.__getRoot()
	def isDistinct(self): return self.__isDistinct()
	def getParentScale(self): return self.__getParentScale()
	def getNumerals(self): return self.__getNumerals()
	def getSemitones(self): return self.__getSemitones()
	def getIntervals(self): return self.__getIntervals()
	def getTones(self): return self.__getTones()
	def getDegreeByInterval(self, p_interval): return self.__getDegreeByInterval(p_interval)
	def getDegreeByNumeral(self, p_numeral): return self.__getDegreeByNumeral(p_numeral)

	######################################################
	# Methods for logically calculating scale properties #
	######################################################

	def getHemitonia(self): return self.countIntervals(1)
	def getTritonia(self): return self.countIntervals(6)
	def getCardinality(self, p_system = DEFAULT_SYSTEM): return CARDINALITY[p_system][len(self.getDegrees())]
	def hasCohemitonia(self): return (len(self.getCohemitonic()) != 0)
	def isPrime(self): return (self.getPrimeMode() == self)

	def countIntervals(self, p_interval_size):

		try:
			counter = 0
			next_scale = self

			for i in range(len(self.getIntervals())):
				if (p_interval_size in next_scale.getSemitones()): counter = counter + 1
				next_scale = next_scale.rotate()

			if (p_interval_size == 6): counter = counter / 2
			return counter

		except: print("Error: Failed to count intervals for scale: " + str(self))

	def getImperfections(self):

		try:
			counter = 0

			for degree in self.getDegrees(): 
				if (P5 not in degree.buildPitchClass()): counter = counter + 1

			return counter

		except: print("Error: Failed to get imperfections for scale: " + str(self))
	
	def getRotationalSymmetry(self):

		try:
			parent_pitch_class = self.pitchClassToScaleSteps(self.getIntervals())
			result = []

			for degree in self.getDegrees():
				if (degree == self[1]): continue
				child_pitch_class = self.pitchClassToScaleSteps(degree.buildPitchClass())
				if (parent_pitch_class == child_pitch_class): result.append(degree.getPosition())

			return result

		except: print("Error: Failed to get rotational symmetry for scale: " + str(self))

	def getReflectionAxes(self):

		try:
			result = []

			for degree in self.getDegrees():
				scale_steps = self.pitchClassToScaleSteps(degree.buildPitchClass())
				if (scale_steps == scale_steps[::-1]): result.append(degree.getPosition())

			return result 

		except: print("Error: Failed to get reflection axes for scale: " + str(self))

	def getIntervalVector(self, p_system = DEFAULT_SYSTEM):

		try: 
			all_intervals = []
			for degree in self.getDegrees(): all_intervals = all_intervals + degree.buildPitchClass()[1:]
			all_pitch_classes = []

			for interval in all_intervals:
				semitones = interval.getSemitones()
				if (semitones > 11): semitones = semitones - 12
				all_pitch_classes.append(INTERVAL_SPECTRUM[p_system][semitones])

			counter = collections.Counter(all_pitch_classes)
			result = {}
			for key in counter.keys(): result[key] = int(counter[key]/2)
			return result

		except: print("Error: Failed to retrieve interval vector for scale: " + str(self))

	def isChiral(self):

		try:
			reflection = self.pitchClassToScaleSteps(self.getIntervals())[::-1]
			result = []

			for degree in self.getDegrees():
				rotation = self.pitchClassToScaleSteps(degree.buildPitchClass())
				if (rotation == reflection): return False

			return True

		except: print("Error: Failed to check chirality for scale: " + str(self))

	def getCohemitonic(self):

		try:
			result = []
			scale_steps = (self.pitchClassToScaleSteps(self.getIntervals())*2)

			for i in range(int(len(scale_steps)/2)):
				if (scale_steps[i] == 1 and scale_steps[i + 1] == 1): result.append(i + 1)

			return result

		except: print("Error: Failed to retrieve cohemitonic tone")

	def getPrimeMode(self, p_consider_negative_modes = False):

		try: 
			min_count = 1000

			for degree in self.getDegrees():
				new_scale = degree.buildScale()
				temp_sum = sum([item.getSemitones() for item in new_scale.getIntervals()])

				if (temp_sum < min_count):
					prime_mode = new_scale
					min_count = temp_sum
				
				if (p_consider_negative_modes):
					new_scale = new_scale.getNegative()
					temp_sum = sum([item.getSemitones() for item in new_scale.getIntervals()])

					if (temp_sum < min_count):
						prime_mode = new_scale
						min_count = temp_sum
				
			return prime_mode

		except: print("Error: Failed to get prime mode of scale: " + str(self))

	##################
	# Static Methods #
	##################

	@staticmethod
	def fromInt(p_int): return Scale.decimalToPitchClass(p_int)

	@staticmethod
	def pitchClassToScaleSteps(p_pitch_class):

		try:
			result = []
			previous = P1

			for interval in p_pitch_class[1:]:
				result.append((interval - previous).getSemitones())
				previous = interval

			result.append(abs(p_pitch_class[-1].simplify().getSemitones() - 12))
			return result

		except: print("Error: Failed to retrieve scale steps")

	@staticmethod
	def pitchClassToDecimal(p_intervals): return int(Scale.pitchClassToBinary(p_intervals), 2)

	@staticmethod
	def pitchClassToBinary(p_intervals):

		try:
			result = ""

			for i in range(12):
				if (len([item for item in p_intervals if i == item.getSemitones()]) == 0): result = result + "0"
				else: result = result + "1"

			return result[::-1]

		except: print("Error: Failed to convert pitch class " + p_intervals + " to decimal")

	@staticmethod
	def decimalToPitchClass(p_integer, p_use_distinct_intervals = False): return Scale.binaryToPitchClass('{0:012b}'.format(p_integer))

	@staticmethod
	def binaryToPitchClass(p_binary): return Scale.scaleStepsToDistinctPitchClass(Scale.binaryToScaleSteps(p_binary))

	@staticmethod
	def binaryToScaleSteps(p_binary):
		
		binary = p_binary[len(p_binary)::-1]
		binary = (binary + binary[0])[1:]
		scale_steps = []
		semitones = 0

		for i in range(len(binary)):
			if (binary[i] == '0'): semitones = semitones + 1
			else:
				semitones = semitones + 1
				scale_steps.append(semitones)
				semitones = 0
		
		return scale_steps

	@staticmethod
	def scaleStepsToPitchClass(p_scale_steps, p_system = DEFAULT_SYSTEM):

		counter = 0
		possible_intervals_collection = [(P1, P1, P1)]

		for i in range(len(p_scale_steps) - 1):
			integer = p_scale_steps[i]
			counter = counter + integer
			possible_intervals_collection.append(Interval.getPossibleIntervals(counter))

		all_combinations = list(itertools.product(*possible_intervals_collection))

		min_combination = None
		min_repeat_size = 1000
		min_accidental_count = 1000
		min_sharp_count = 1000

		for combination in all_combinations:
			temp_repeat_size = statistics.mean([len(list(group)) for key, group in itertools.groupby([item.getNumeral() for item in combination])])
			temp_accidental_count = len([item for item in combination if item.getAccidental() != ACCIDENTALS[p_system][0]])
			temp_sharp_count = len([item for item in combination if ACCIDENTALS[p_system][1] in item.getAccidental()])

			if (temp_repeat_size < min_repeat_size):
				min_combination = combination
				min_repeat_size = temp_repeat_size
				min_accidental_count = temp_accidental_count

			if (temp_repeat_size == min_repeat_size and (temp_accidental_count < min_accidental_count or temp_sharp_count < min_sharp_count)):
				min_combination = combination
				min_accidental_count = temp_accidental_count
				min_sharp_count = temp_sharp_count

		return list(min_combination)

	@staticmethod
	def scaleStepsToDistinctPitchClass(p_scale_steps):

		try: 
			result = [P1]
			semitones = 0

			for i in range(len(p_scale_steps) - 1):
				semitones = semitones + p_scale_steps[i]
				result.append(Interval(semitones, i + 2))

			if (len([item for item in result if len(item.getAccidental()) > ACCIDENTAL_LIMIT]) > 0): return Scale.scaleStepsToPitchClass(p_scale_steps)
			return result

		except: print("Error: Failed to create list of distinct intervals")

	@staticmethod
	def scaleIntervalsByOrder(p_intervals):

		try: 
			result = []
			previous = -m2

			for interval in p_intervals:
				while (interval <= previous): interval = interval + P8
				previous = interval
				result.append(interval)

			return result

		except: print("Error: Failed to order intervals")

	@staticmethod
	def tonesToPitchClass(p_tones): return Scale.scaleIntervalsByOrder([tone - p_tones[0] for tone in p_tones])

	#######################
	# Getters and Setters #
	#######################
   
	def getDegrees(self): return self.degrees
	def getTonicTone(self): return self.tonic_tone
	def getParentDegree(self): return self.parent_degree

	def setDegrees(self, p_degrees): self.degrees = p_degrees
	def setTonicTone(self, p_tonic_tone): self.tonic_tone = p_tonic_tone
	def setParentDegree(self, p_parent_degree): self.parent_degree = p_parent_degree
	
	class _Degree:
		
		def __init__(self, p_interval, p_parent_scale):

			self.interval = p_interval
			self.parent_scale = p_parent_scale

			degree_tone = self.getParentScale().getTonicTone() + self.getInterval()
			self.setTone(degree_tone)

		#####################################
		# Methods concerning class behavior #
		#####################################

		def __str__logic(self):
			if (not DEGREE_SIMPLE_REPRESENTATION): return self.getNumeral() + ": " + str(self.getTone())
			else: return str(self.getTone())

		##############
		# Comparison #
		##############

		def __eq__logic(self, p_other): return (type(self) == type(p_other)) and ((self.getInterval() == p_other.getInterval()) and (self.getTone() == p_other.getTone()))
		def __ne__logic(self, p_other): return not (self.__eq__logic(p_other))

		##############
		# Arithmetic #
		##############

		def __add__logic(self, p_other):

			if (isinstance(p_other, str)): return str(self) + p_other

			if (isinstance(p_other, int)):
				if (p_other < 0): return self.__sub__logic(abs(p_other))		
				elif (p_other == 1): return self
				else: return self.__next().__add__logic(p_other - 1)
			
			if (isinstance(p_other, Interval)):

				try:
					if (p_other < Interval(0, 0)): return self.__sub__logic(abs(p_other))
					if (p_other == P1): return self
					new_interval = (self.getInterval() + p_other).simplify() 

					if (new_interval not in self.getParentScale()):

						if (self.getParentScale().isDistinct()):
							if (new_interval.getNumeral() == 1): return self.getParentScale()[1].transform(new_interval.getAccidental())[1]
							elif (new_interval.getNumeral() in self.getParentScale().getNumerals()): return self.getParentScale().replaceAtNumeralWith(new_interval.getNumeral(), new_interval).getDegreeByInterval(new_interval)
							else: return self.getParentScale().addInterval(new_interval).getDegreeByInterval(new_interval)

						else: return self.getParentScale().addInterval(new_interval).getDegreeByInterval(new_interval)
					else: return self.getParentScale().getDegreeByInterval(new_interval)

				except: print("Error: Failed to assign tones to the new scale")

			if (isinstance(p_other, Scale)): 
				new_scale = (self.__add__logic(p_other[1])) + (p_other[2:len(p_other.getIntervals())])
				if (self.getParentScale().getParentDegree() != None): new_scale.setParentDegree(self.getParentScale().getParentDegree())
				return new_scale
			
			if (isinstance(p_other, Scale._Degree)): 
				new_intervals = [self.getInterval(), p_other.getInterval() + (p_other.getParentScale()[1].getTone() - self.getParentScale()[1].getTone())]
				new_intervals = Scale.scaleIntervalsByOrder(new_intervals)
				new_intervals = [interval - self.getInterval() for interval in new_intervals]
				new_scale = type(self.getParentScale())(self.getTone(), new_intervals)
				if (self.getParentScale().getParentDegree() != None): new_scale.setParentDegree(self.getParentScale().getParentDegree())
				return new_scale

		def __sub__logic(self, p_other):

			if (isinstance(p_other, int)):
				if (p_other < 0): return self.__add__logic(abs(p_other))
				elif (p_other == 1): return self
				else: return self.__previous().__sub__logic((p_other - 1))

			if (isinstance(p_other, Interval)):

				try:
					if (p_other < Interval(0, 0)): return self.__add__logic(abs(p_other))
					if (p_other == P1): return self
					
					new_interval = (self.getInterval() - p_other).simplify()
					while (new_interval.getNumeral() < 0): new_interval = new_interval + P8

					if (new_interval not in self.getParentScale()):

						if (self.getParentScale().isDistinct()):
							if (new_interval.getNumeral() == 1): return self.getParentScale()[1].transform(new_interval.getAccidental())[1]
							elif (new_interval.getNumeral() in self.getParentScale().getNumerals()): return self.getParentScale().replaceAtNumeralWith(new_interval.getNumeral(), new_interval).getDegreeByInterval(new_interval)
							else: return self.getParentScale().addInterval(new_interval).getDegreeByInterval(new_interval)
						
						else: return self.getParentScale().addInterval(new_interval).getDegreeByInterval(new_interval)
					else: return self.getParentScale().getDegreeByInterval(new_interval)

				except: print("Error: Failed to assign tones to the new scale")

			if (isinstance(p_other, Scale._Degree)): 
				new_scale = p_other.__add__(self)
				return new_scale[1].distanceFromNext(new_scale[2])
		
		def __radd__(self, p_other):
			if (isinstance(p_other, str)): return p_other + str(self)

		################################
		# Methods concerned with names #
		################################

		def __getName(self, p_system = DEFAULT_SYSTEM): return SCALE_DEGREE_NAMES[p_system][self.getInterval()]

		def __getNumeral(self):

			try:
				numeral = intToRoman(self.getInterval().getNumeral()) 
				if (self.buildPitchClass(2, 3) == [P1, m3]): numeral = numeral.lower()
				accidental = self.getInterval().getAccidental()
				return accidental + numeral
			
			except: print("Error: Failed to print numeral of chord: " + str(self))

		##########################
		# Transformation methods #
		##########################

		def __transform(self, p_accidental):

			try:
				new_interval = self.getInterval().transform(p_accidental)
				new_pitch_class = self.getParentScale().getIntervals()[:]
				new_pitch_class = [item for item in new_pitch_class if item != self.getInterval()]
				new_pitch_class.append(new_interval)
				new_pitch_class.sort(key=lambda x: x.getNumeral())

				if (self.getPosition() == 1):
					difference = new_interval.getSemitones()
					new_pitch_class = [Interval(item.getSemitones() - difference, item.getNumeral()) for item in new_pitch_class]
					return type(self.getParentScale())(self.getParentScale()[1].getTone() + Interval(difference, 1), new_pitch_class)

				return type(self.getParentScale())(self.getParentScale()[1].getTone(), new_pitch_class)

			except: print("Error: Failed to transform " + self + " by " + p_accidental)

		#############################################################
		# Methods concerned with measuring distance between degrees #
		#############################################################

		def __distanceFrom(self, p_other):
			if (self.getInterval().getSemitones() < p_other.getInterval().getSemitones()): return p_other.getInterval() - self.getInterval()
			else: return self.getInterval() - p_other.getInterval() 

		def __distanceFromNext(self, p_other):	
			if (self.getInterval().getSemitones() < p_other.getInterval().getSemitones()): return p_other.getInterval() - self.getInterval()
			else: return ((self.getParentScale().getIntervals()[-1] + (P8 - self.getParentScale().getIntervals()[-1].simplify())) - self.getInterval()) + p_other.getInterval()

		######################################################
		# Methods concerned with operations on scale degrees #
		######################################################

		def __build(self, object_type, p_item_1 = 4, p_item_2 = 3, *args):

			try:
				if (isinstance(p_item_1, list)):
					if (isinstance(p_item_1[0], int)): child_object = object_type(self.getTone(), [(self.__distanceFromNext(self + item)).simplify() for item in p_item_1], *args)
					if (isinstance(p_item_1[0], Interval)): child_object = object_type(self.getTone(), p_item_1, *args)
				elif (isinstance(p_item_1, str)): child_object = object_type(self.getTone(), object_type.fromString(p_item_1), *args)
				else: child_object = object_type(self.getTone(), self.__buildPitchClass(p_item_1, p_item_2)[:p_item_1], *args)

				child_object.setParentDegree(self)
				return child_object

			except: print("Error: Failed to build object")

		def __buildScale(self):

			try:
				child_intervals = self.__buildPitchClass()
				child_scale = Scale(self.getTone(), child_intervals)
				child_scale.setParentDegree(self)
				return child_scale

			except: print("Error: Failed to build scale")

		def __buildScaleWithIntervals(self, p_intervals):

			try:
				new_scale = Scale(self.getTone(), p_intervals)
				new_scale.setParentDegree(self)
				return new_scale

			except: print("Error: Failed to build custom scale!")

		def __buildPitchClass(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM):

			try:
				if (p_num_tones == -1): p_num_tones = len(self.getParentScale().getIntervals())
				child_intervals = []
				p_leap_size = p_leap_size - 1
				next_degree = self
				counter = 0

				while (counter < p_num_tones - 1):
					for j in range(p_leap_size): next_degree = next_degree.__next()
					new_interval = self.__distanceFromNext(next_degree)
					child_intervals.append(new_interval)
					counter = counter + 1
					
				return Scale.scaleIntervalsByOrder([P1] + child_intervals)

			except: print("Error: Failed to build pitch class set")

		#################
		# Sugar methods #
		#################

		def __getPosition(self): return self.getParentScale().getDegrees().index(self) + 1
		def __getPositionInParent(self): return self.findInParent().getPosition()

		def __findInParent(self):
			if (self.getParentScale().getParentDegree() != None): return self.getParentScale().getParentDegree().getParentScale().getDegreeByInterval((self.getParentScale().getParentDegree().getInterval() + self.getInterval()).simplify())
			else: return self

		def __next(self):	
			if (self.__getPosition() == len(self.getParentScale().getDegrees())): return self.getParentScale().getDegrees()[0]
			return self.getParentScale().getDegrees()[(self.__getPosition() - 1) + 1]

		def __previous(self):
			if (self.__getPosition() == 1): return self.getParentScale().getDegrees()[-1]
			return self.getParentScale().getDegrees()[(self.__getPosition() - 1) - 1]

		###################
		# Wrapper methods #
		###################

		def __str__(self): return self.__str__logic()

		def __eq__(self, p_other): return self.__eq__logic(p_other)
		def __ne__(self, p_other): return self.__ne__logic(p_other)

		def __add__(self, p_other): return self.__add__logic(p_other)
		def __sub__(self, p_other): return self.__sub__logic(p_other)

		def getName(self, p_system = DEFAULT_SYSTEM): return self.__getName(p_system)
		def getNumeral(self): return self.__getNumeral()
		def transform(self, p_accidental): return self.__transform(p_accidental)
		def distanceFrom(self, p_other): return self.__distanceFrom(p_other)
		def distanceFromNext(self, p_other): return self.__distanceFromNext(p_other)
		def build(self, p_object_type, p_num_tones = 4, p_leap_size = 3, *args): return self.__build(p_object_type, p_num_tones, p_leap_size, *args)
		def buildScale(self): return self.__buildScale()
		def buildScaleWithIntervals(self, p_intervals): return self.__buildScaleWithIntervals(p_intervals)
		def buildPitchClass(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM): return self.__buildPitchClass(p_num_tones, p_leap_size, p_system)
		def getPosition(self): return self.__getPosition()
		def getPositionInParent(self): return self.__getPositionInParent()
		def findInParent(self): return self.__findInParent()
		def next(self):	return self.__next()
		def previous(self): return self.__previous()

		#######################
		# Getters and Setters #
		#######################
		
		def getOctaves(self): return self.octaves
		def getTone(self): return self.tone	
		def getInterval(self): return self.interval
		def getParentScale(self): return self.parent_scale

		def setOctaves(self, p_octaves): self.octaves = p_octaves
		def setTone(self, p_tone): self.tone = p_tone
		def setInterval(self, p_interval): self.interval = p_interval
		def setParentScale(self, p_parent_scale): self.parent_scale = p_parent_scale
			