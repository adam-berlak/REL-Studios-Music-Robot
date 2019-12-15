import re

from Configuration import *
from HelperMethods import *

class Scale:

	def __init__(self, p_tonic_tone, p_item):
		self.tonic_tone = p_tonic_tone
		self.parent_degree = None
		self.degrees = []

		if (isinstance(p_item, list)):
			if (isinstance(p_item[0], Interval)): intervals = p_item
			if (isinstance(p_item[0], int)): intervals = Scale.scaleStepsToPitchClass(p_item)

		elif (isinstance(p_item, int)): intervals = Scale.decimalToPitchClass(p_item)
		for i in range(len(intervals)): self.degrees.append(type(self)._Degree(intervals[i], self))

	#####################################
	# Methods concerning class behavior #
	#####################################
	
	def __str__(self):
		result = "<"
		for degree in self.getDegrees(): result = result + str(degree) + ", "
		return result[:-2] + ">"

	def __getitem__(self, p_index): return self.getDegrees()[p_index - 1]
	
	def __contains__(self, p_other):
		if (isinstance(p_other, Scale)): return all(elem in self.getTones() for elem in p_other.getTones())
		if (issubclass(type(p_other), Scale)): return all(elem in self.getTones() for elem in p_other.getTones())
		if (isinstance(p_other, Tone)): return p_other in self.getTones()
		if (isinstance(p_other, type(self)._Degree)): return p_other in self.getDegrees()
		if (isinstance(p_other, Interval)): return p_other.simplify() in self.getIntervals()

		if (isinstance(p_other, list)):

			if (isinstance(p_other[0], Interval)):

				for degree in self.getDegrees():		
					if (all(elem.simplify() in degree.buildPitchClass() for elem in p_other)): return True

				return False
	
	##############
	# Comparison #
	##############

	def __eq__(self, p_other): return (type(self) == type(p_other)) and ((self.getIntervals() == p_other.getIntervals()) and (self.getTonicTone() == p_other.getTonicTone()))

	def __ne__(self, p_other): return not (self == p_other)

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):

		try:
			if (isinstance(p_other, Interval)): return (self[1] + p_other).buildWithIntervals(type(self), self.getIntervals())
			if (isinstance(p_other, int)): return (self[1] + p_other).build(type(self), len(self.getIntervals()), 2)

			if (isinstance(p_other, Scale._Degree)):
				new_intervals = self.getIntervals()
				new_intervals.append(p_other.getInterval())
				new_intervals = Scale.scaleIntervalsByOrder(new_intervals)
				return type(self)(self[1].getTone(), new_intervals)

			if (isinstance(p_other, type(self))):
				new_intervals = self.getIntervals()
				new_intervals = list(dict.fromkeys(new_intervals + p_other.getIntervals()))
				new_intervals.sort(key=lambda x: x.getSemitones())
				return type(self)(self[1].getTone(), new_intervals)

			if (isinstance(p_other, str)): return str(self) + p_other

		except: print("Error: Failed to add " + str(p_other) + " to " + str(self))

	def __radd__(self, p_other):
		if (isinstance(p_other, str)): return p_other + str(self)

	def __sub__(self, p_other):

		try:
			if (isinstance(p_other, Interval)): return (self[1] - p_other).buildWithIntervals(type(self), self.getIntervals())
			if (isinstance(p_other, int)): return (self[1] - p_other).build(type(self), len(self.getIntervals()), 2)

		except: print("Error: Failed to subtract " + str(p_other) + " from " + str(self))

	################################
	# Methods concerned with names #
	################################

	def getName(self): return scale_names[Scale.pitchClassToDecimal(self.getIntervals())]

	def getModeNames(self): return [(self + (item + 1)).getName() for item in range(len(self.getIntervals()))]

	def printTones(self):
		result = ""
		for tone in self.getTones(): result = result + str(tone) + ", "
		return "[" + result[:-2] + "]"

	##########################
	# Transformation methods #
	##########################

	def addInterval(self, p_interval):
		new_pitch_class = self.getIntervals()[:]
		new_pitch_class.append(p_interval)
		new_pitch_class.sort(key=lambda x: x.getSemitones())
		new_scale = type(self)(self[1].getTone(), new_pitch_class)
		new_scale.setParentDegree(self.getParentDegree())
		return new_scale

	def replaceAtNumeralWith(self, p_numeral, p_interval):
		index = self.getIntervals().index([item for item in self.getIntervals() if item.getNumeral() == p_numeral][0])
		result_scale_beggining = self.getIntervals()[:index]
		result_scale_beggining.append(p_interval)
		result_scale_ending = self.getIntervals()[index + 1:]
		result_scale_intervals = result_scale_beggining + result_scale_ending

		parent_degree = self.getParentDegree()
		result_scale = type(self)(self[1].getTone(), result_scale_intervals)
		result_scale.setParentDegree(parent_degree)
		return result_scale

	########################
	# Common Functionality #
	########################

	def getParallelScale(self):
		if (self[1].buildPitchClass(2, 3) == [P1, m3]): return self[1].buildScaleWithIntervals((self - 6).getIntervals())
		elif (self[1].buildPitchClass(2, 3) == [P1, M3]): return self[1].buildScaleWithIntervals((self + 6).getIntervals())
		else: return self

	def getRelativeScale(self):
		if (self[1].buildPitchClass(2, 3) == [P1, m3]): return (self - 6)
		elif (self[1].buildPitchClass(2, 3) == [P1, M3]): return (self + 6)		
		else: return self

	def rotate(self): return (self + 2)

	def getRoot(self): return self[1]

	#################
	# Sugar Methods #
	#################

	def isDistinct(self): return (len([item.getNumeral() for item in self.getIntervals()]) == len(set([item.getNumeral() for item in self.getIntervals()])))

	def getParentScale(self): return self.getParentDegree().getParentScale()

	def getNumerals(self): return [item.getNumeral() for item in self.getIntervals()]

	def getSemitones(self): return [item.getSemitones() for item in self.getIntervals()]

	def getIntervals(self): return [item.getInterval() for item in self.getDegrees()]

	def getTones(self): return [item.getTone() for item in self.getDegrees()]
	
	def getDegreeByInterval(self, p_interval): return [item for item in self.getDegrees() if item.getInterval() == p_interval][0]

	##################
	# Static Methods #
	##################

	@staticmethod
	def pitchClassToScaleSteps(p_pitch_class):

		try:
			result = []

			# Counters
			previous = P1

			# Loop through every element of the pitch class list except the first
			for interval in p_pitch_class[1:]:
				result.append((interval - previous).getSemitones())
				previous = interval

			# Add the distance between the last degree and the first
			result.append(abs(p_pitch_class[-1].getSemitones() - 12))
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
	def scaleStepsToPitchClass(p_scale_steps):

		try:
			intervals = Interval.generateIntervalList(UNALTERED_INTERVALS[DEFAULT_SYSTEM])
			result = [P1]

			# Counters
			counter = 0

			# Loop until scale steps list is traversed
			for i in range(len(p_scale_steps) - 1):
				integer = p_scale_steps[i]
				counter = counter + integer

				# find the interval that matches semitones and degree
				possible_intervals = intervals[counter]
				matches = [item for item in possible_intervals if ((i + 2) == item.getNumeral())]

				# If such a degree is found select it, otherwise select the one with the degree closest to the degree desired
				if (len(matches) != 0): selected_interval = matches[0]
				else: selected_interval = min(possible_intervals, key=lambda x:abs(x.getNumeral()-(i + 1)))
				result.append(selected_interval)

			return result

		except: print("Error: Failed to retrieve pitch class")

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
			previous = P1

			for interval in p_intervals:
				while (interval < previous): interval = interval + P8
				previous = interval
				result.append(interval)

			return result

		except: print("Error: Failed to order intervals")

	######################################################
	# Methods for logically calculating scale properties #
	######################################################

	def getHemitonia(self): return self.countIntervals(1)

	def getTritonia(self): return self.countIntervals(6)

	def countIntervals(self, p_interval_size): return collections.Counter(self.pitchClassToScaleSteps(self.getIntervals()))[p_interval_size]

	def getCardinality(self, p_system = DEFAULT_SYSTEM): return CARDINALITY[p_system][len(self.getDegrees())]

	def hasCohemitonia(self): return (len(self.getCohemitonic()) != 0)

	def isPrime(self): return (self.getPrimeMode() == 1)

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
			result = ""
			for key in counter.keys(): result = result + key + "(" + str(int(counter[key]/2)) + ")"
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

	def getPrimeMode(self, p_consider_inverted_modes = False):

		try: 
			min_count = 1000

			for degree in self.getDegrees():
				pitch_class = degree.buildPitchClass()
				temp_sum = sum([item.getSemitones() for item in pitch_class])

				if (temp_sum < min_count):
					prime_mode = str(degree.getPosition())
					min_count = temp_sum
				
				if (p_consider_inverted_modes):
					inverted_pitch_class = self.scaleStepsToPitchClass(self.pitchClassToScaleSteps(degree.buildPitchClass()))
					temp_sum = sum([item.getSemitones() for item in inverted_pitch_class])

					if (temp_sum < min_count):
						prime_mode = str(degree.getPosition()) + "Inverted"
						min_count = temp_sum
				
			return prime_mode

		except: print("Error: Failed to get prime mode of scale: " + str(self))

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
		def __init__(self, p_interval, p_parent_scale, p_octaves = 0):
			self.interval = p_interval
			self.parent_scale = p_parent_scale
			degree_tone = self.getParentScale().getTonicTone() + self.getInterval()
			self.setTone(degree_tone)

		#####################################
		# Methods concerning class behavior #
		#####################################

		def __copy__(self): return _Degree(self.getInterval(), self.getParentScale())

		def __str__(self):
			if (not DEGREE_SIMPLE_REPRESENTATION): return self.printNumeral() + ": " + str(self.getTone())
			else: return str(self.getTone())

		##############
		# Comparison #
		##############

		def __eq__(self, p_other): return (type(self) == type(p_other)) and ((self.getInterval() == p_other.getInterval()) and (self.getTone() == p_other.getTone()))

		def __ne__(self, p_other): return (not self == p_other)

		##############
		# Arithmetic #
		##############

		def __add__(self, p_other):

			if (isinstance(p_other, Interval)):

				try:
					new_interval = (self.getInterval() + p_other).simplify()
					if (not new_interval in self.getParentScale() and not self.getParentScale().isDistinct()): return self.getParentScale().addInterval(new_interval).getDegreeByInterval(new_interval)
					elif (not new_interval in self.getParentScale() and self.getParentScale().isDistinct()): return self.getParentScale().replaceAtNumeralWith(new_interval.getNumeral(), new_interval).getDegreeByInterval(new_interval)
					return self.getParentScale().getDegreeByInterval(new_interval)

				except: print("Error: Failed to assign tones to the new scale")

			if (isinstance(p_other, int)):
				if (p_other < 0): return self - abs(p_other)			
				if (p_other == 1): return self
				if (type(self) != Scale._Degree): return super(type(self), self).next() + (p_other - 1)
				else: return self.next() + (p_other - 1)

			if (isinstance(p_other, Scale)): return p_other + self	
			if (isinstance(p_other, Scale._Degree)): return type(self.getParentScale())(self.getTone(), [P1, self.distanceFromNext(p_other)])
			if (isinstance(p_other, str)): return str(self) + p_other
		
		def __radd__(self, p_other):
			if (isinstance(p_other, str)): return p_other + str(self)

		def __sub__(self, p_other):

			if (isinstance(p_other, Interval)):

				try:
					new_interval = (self.getInterval() - p_other).simplify()

					while (new_interval < P1): new_interval = new_interval + P8

					if not new_interval in self.getParentScale():
						new_scale = self.getParentScale().addInterval(new_interval)
						return new_scale.getDegreeByInterval(new_interval)

					return self.getParentScale().getDegreeByInterval(new_interval)

				except: print("Error: Failed to assign tones to the new scale")

			if (isinstance(p_other, int)):

				if (p_other < 0): return self + abs(p_other)
				if (p_other == 1): return self
				if (type(self) != Scale._Degree): return super(type(self), self).previous() - (p_other - 1)
				else: return self.previous() - (p_other - 1)

		################################
		# Methods concerned with names #
		################################

		def getName(self, p_system = DEFAULT_SYSTEM): return SCALE_DEGREE_NAMES[p_system][self.getInterval()]

		def printNumeral(self):

			try:
				# Convert numeral integer into roman numeral
				numeral = intToRoman(self.getInterval().getNumeral())

				# Check quality of triad built on this degree, and change numeral to lower if minor     
				if (self.buildPitchClass(2, 3) == [P1, m3]): numeral = numeral.lower()

				# Obtain the accidental of the associated interval
				accidental = self.getInterval().getAccidental()
				return accidental + numeral
			
			except: print("Error: Failed to print numeral of chord: " + str(self))

		##########################
		# Transformation methods #
		##########################

		def transform(self, p_accidental):

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

		def distanceFrom(self, p_other):
			if (self.getInterval().getSemitones() < p_other.getInterval().getSemitones()): return p_other.getInterval() - self.getInterval()
			else: return self.getInterval() - p_other.getInterval() 

		def distanceFromNext(self, p_other):	
			if (self.getInterval().getSemitones() < p_other.getInterval().getSemitones()): return p_other.getInterval() - self.getInterval()
			else: return (P8 - self.getInterval()) + p_other.getInterval()

		######################################################
		# Methods concerned with operations on scale degrees #
		######################################################

		def build(self, object_type, p_num_tones = 4, p_leap_size = 3, *args):

			try:
				if (type(self) != Scale._Degree): child_intervals = super(type(self), self).buildPitchClass(p_num_tones, p_leap_size)[:p_num_tones]
				else: child_intervals = self.buildPitchClass(p_num_tones, p_leap_size)[:p_num_tones]
				child_object = object_type(self.getTone(), child_intervals, *args)
				child_object.setParentDegree(self)
				return child_object

			except: print("Error: Failed to build chord")

		def buildWithIntervals(self, object_type, p_pitch_class, *args):

			try:
				child_object = object_type(self.getTone(), p_pitch_class, *args)
				child_object.setParentDegree(self)
				return child_object

			except: print("Error: Failed to build chord with intervals")

		def buildWithGenericIntervals(self, object_type, p_generic_intervals, *args):

			try:
				pitch_class = []
				for i in range(len(p_generic_intervals)): pitch_class.append((self.distanceFromNext(self + p_generic_intervals[i])).simplify())
				pitch_class = Scale.scaleIntervalsByOrder(pitch_class)
				child_object = object_type(self.getTone(), pitch_class, *args)
				child_object.setParentDegree(self)
				return child_object

			except: print("Error: Failed to build chord with generic intervals")

		def buildScale(self):

			try:
				if (type(self) != Scale._Degree): child_intervals = super(type(self), self).buildPitchClass()
				else: child_intervals = self.buildPitchClass()
				child_scale = Scale(self.getTone(), child_intervals)
				child_scale.setParentDegree(self)
				return child_scale

			except: print("Error: Failed to build scale")


		def buildScaleWithIntervals(self, p_intervals):

			try:
				new_scale = Scale(self.getTone(), p_intervals)
				new_scale.setParentDegree(self)
				return new_scale

			except: print("Error: Failed to build custom scale!")

		def buildPitchClass(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM):

			try:
				if (p_num_tones == -1): p_num_tones = len(self.getParentScale().getIntervals())
				child_intervals = []
				p_leap_size = p_leap_size - 1

				# Counters
				next_degree = self
				counter = 0

				# Loop until we have reached the starting degree
				while (counter < p_num_tones - 1):

					for j in range(p_leap_size):
						if (type(self) != Scale._Degree): next_degree = super(type(next_degree), next_degree).next()
						else: next_degree = next_degree.next()

					new_interval = self.distanceFromNext(next_degree)

					# Add degree to list
					child_intervals.append(new_interval)

					# Increment
					counter = counter + 1
					
				return Scale.scaleIntervalsByOrder([P1] + child_intervals)

			except: print("Error: Failed to build pitch class set")

		#################
		# Sugar methods #
		#################

		def getPosition(self): return self.getParentScale().getDegrees().index(self) + 1

		def getPositionInParent(self): return self.getParentScale().getParentScale().getDegrees().index(self.findInParent()) + 1

		def findInParent(self):
			if (self.getParentScale().getParentDegree() != None): return self.getParentScale().getParentDegree().getParentScale().getDegreeByInterval((self.getParentScale().getParentDegree().getInterval() + self.getInterval()).simplify())
			else: return self

		def next(self):		
			if (self.getPosition() == len(self.getParentScale().getDegrees())): return self.getParentScale()[1]
			return self.getParentScale()[self.getPosition() + 1]

		def previous(self):
			if (self.getPosition() == 1): return self.getParentScale()[-0]
			return self.getParentScale()[self.getPosition() - 1]

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
			