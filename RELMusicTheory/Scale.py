
import collections
import re

from Interval import *
from Constants import *
from HelperMethods import *
from scalesDictionary import scale_names

# Class Name: Scale
# Parameters: p_tonic_tone (The tonic tone the scale will be built off of), p_intervals (the interval pattern of the scale)
# Info: A scale object requires a tonic tone and an interval pattern

## STATIC Methods
# STATIC Method pitchClassToScaleSteps: Converts a list of intervals organized as a pitch-class into a list of scale-steps
# STATIC Method scaleStepsToPitchClass: Converts a list of scale-steps into a list of intervals organized as a pitch-class
# STATIC Method intervalsToTones: Given a tonic_tone and a pitch-class, this method applies the pitch-class to the tone and returns the resulting list of tones
# STATIC Method intervalToTone: Given a tone and an interval, the tone resulting from applying the interval to the tone is returned

## Helper Methods
# Method getTones: Returns the tones associated with the degrees of the parent scale
# Method getDegreeByInterval: Retrieves the degree that is a certain interval from the tonic if it exists
# Method findDegreeInParent: Given a scale degree, if the associated scale is a child of another scale (IE built off a degree of a parent scale) the degree of the parent scale that is the same pitch as the principle is returned

## Properties of Scales
# Method countIntervals: Given an interval, count how many times the interval occures in the parent scale
# Method getHemitonia: Count how many intervals containing one semitone exist in the parent scale (IE Major Scale = 2)
# Method getTritonia: Count how many intervals containing six semitones exist in the parent scale (IE Major Scale = 1)
# Method getCardinality: Return the name associated with parent scales number of degrees (IE Major Scale = Heptatonic)
# Method getImperfections: Count how many degrees in the parent scale do not have a degree a perfect fifth above them (IE Major Scale = 1, the 7th degree)
# Method getRotationalSymmetry: Count how many modes of the parent scale are identical to the parent scale (IE Major Scale = 0) *FIX CONVERTING TO PITCH CLASS*
# Method getReflectionAxes: Return list of degrees that have associated modes which are identical to their inversion *POSSIBLY INCORRECT IMPLEMENTATION*
# Method getIntervalVector: Return a list of tuples containing interval types and how frequently they appear
# Method getCohemitonia: Return a degree that has two semitones following dirrectly after it
# Method getPrimeMode: Returns the mode of the parent scale whos pitch class has the smallest set of intervals *POSSIBLY NEED TO FIX INVERTED MODES IMPLEMENTATION*
# Method isPrime: Checks if the parent mode is prime
# Method isChiral: Checks if any of the modes are equivalent to the reflection of the parent scale. (IE Major Scale = True, the aeolian mode)
# Method hasCohemitonia: Checks if two semitones occure next to eachother within the parent scale

# TODO 
# def isPalindromic(self)
# def isHelotonic(self)
# def isMaximallyEven(self)
# def isBalanced(self)

class Scale:

	def __init__(self, p_tonic_tone, p_intervals):
		self.tonic_tone = p_tonic_tone
		self.intervals = p_intervals
		self.parent_degree = None
		self.degrees = []

		for i in range(len(p_intervals)):
			self.degrees.append(type(self)._Degree(self.intervals[i], self))

	#####################################
	# Methods concerning class behavior #
	#####################################
	
	def __str__(self):
		result = "["

		for degree in self.getDegrees():
			result = result + str(degree) + ", "

		return result[:-2] + "]"

	def __getitem__(self, p_index):
		return self.getDegrees()[p_index - 1]
	
	def __contains__(self, p_other):

		if (isinstance(p_other, Scale)):
			return all(elem in self.getTones() for elem in p_other.getTones())

		if (issubclass(type(p_other), Scale)):
			return all(elem in self.getTones() for elem in p_other.getTones())

		if (isinstance(p_other, str)):
			return p_other in self.getTones()

		if (isinstance(p_other, type(self)._Degree)):
			return p_other in self.getDegrees()

		if (isinstance(p_other, Interval)):
			return p_other.minimize() in self.getIntervals()

		if (isinstance(p_other, list)):

			if (isinstance(p_other[0], Interval)):

				for degree in self.getDegrees():
					if (all(elem.minimize() in degree.buildPitchClass() for elem in p_other)):
						return True

				return False
	
	##############
	# Comparison #
	##############

	def __eq__(self, p_other):
		return (type(self) == type(p_other)) and ((self.getIntervals() == p_other.getIntervals()) and (self.getTonicTone() == p_other.getTonicTone()))

	def __ne__(self, p_other):
		return not (self == p_other)

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):

		try:

			if (isinstance(p_other, Interval)):
				return (self[1] + p_other).buildWithIntervals(type(self), self.getIntervals())

			if (isinstance(p_other, int)):
				return (self[1] + p_other).build(type(self), len(self.getIntervals()), 2)

			if (isinstance(p_other, str)):
				return str(self) + p_other

		except:
			print("Error: Failed to add " + str(p_other) + " to " + str(self))

	def __radd__(self, p_other):

		if (isinstance(p_other, str)):
			return p_other + str(self)

	def __sub__(self, p_other):

		try:

			if (isinstance(p_other, Interval)):
				return (self[1] - p_other).buildScaleWithIntervals(self.getIntervals())

			if (isinstance(p_other, int)):
				return (self[1] - p_other).buildScaleWithIntervals(self.getIntervals())

		except:
			print("Error: Failed to subtract " + str(p_other) + " from " + str(self))

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

		except:
			print("Error: Failed to retrieve scale steps")

	@staticmethod
	def scaleStepsToPitchClass(p_scale_steps, p_system = DEFAULT_SYSTEM):

		try:
			intervals = self.getInterval().generateIntervalList(Unaltered_Intervals[DEFAULT_SYSTEM])
			result = []

			# Counters
			counter = 0

			# Loop until scale steps list is traversed
			for i in range(len(p_scale_steps)):
				integer = p_scale_steps[i]
				counter = counter + integer

				# find the interval that matches semitones and degree
				possible_intervals = intervals[counter]
				matches = [item for item in possible_intervals if (i + 1) == item.getNumeral()]

				# If such a degree is found select it, otherwise select the one with the degree closest to the degree desired
				if (len(matches) != 0):
					selected_interval = matches[0]
				else:
					selected_interval = min(possible_intervals, key=lambda x:abs(x.getNumeral()-(i + 1)))

				result.append(selected_interval)

			return result

		except:
			print("Error: Failed to retrieve pitch class")

	@staticmethod
	def pitchClassToBinary(p_intervals):

		try:
			result = ""

			for i in range(12):

				if (len([item for item in p_intervals if i == item.getSemitones()]) == 0):
					result = result + "0"
				else:
					result = result + "1"

			return result[::-1]

		except:
			print("Error: Failed to convert pitch class " + p_intervals + " to decimal")

	@staticmethod
	def pitchClassToDecimal(p_intervals):
		return int(Scale.pitchClassToBinary(p_intervals), 2)

	@staticmethod
	def scaleIntervalsByOrder(p_intervals):

		try: 
			result = []
			previous = P1

			for interval in p_intervals:

				while (interval < previous):
					interval = interval + P8

				previous = interval
				result.append(interval)

			return result

		except:
			print("Error: Failed to order intervals")


	@staticmethod
	def intervalsToTones(p_tonic_tone, p_intervals, p_system = DEFAULT_SYSTEM):
		
		try:
			result = []

			# Counters
			counter = 0

			# Loop until interval list is traversed
			for i in range(len(p_intervals)):
				interval = p_intervals[i]

				# find the tone that matches semitones and position with respect to the degree of the interval
				next_tone = Scale.intervalToTone(p_tonic_tone, interval, p_system)

				# add the resulting tone to the list
				result.append(next_tone)

				# keeps track of how many tones to skip in the white_tones list
				if (i != len(p_intervals) - 1):
					skip_size = p_intervals[i + 1].getNumeral() - interval.getNumeral()
					counter = counter + skip_size

			return result

		except:
			print("Something went wrong when assigning tones to your scale, ensure the intervals are sorted by increasing size")

	@staticmethod
	def intervalToTone(p_principle_tone, p_interval, p_system = DEFAULT_SYSTEM):

		try:
			white_tones = (p_principle_tone[0] + ("ABCDEFG"*2).split(p_principle_tone[0])[1])*4
			possible_tones = (TONES.get(p_system)*4)[([TONES.get(p_system).index(item) for item in TONES.get(p_system) if p_principle_tone in item][0] + p_interval.getSemitones())]
			next_tone = [item for item in possible_tones if white_tones[p_interval.getNumeral() - 1] in item][0]

			return next_tone
		
		except:
			print("Error: Failed to convert " + p_interval + " to a tone using a principle tone of " + p_principle_tone + " and the system " + p_system)

	####################
	# Courtesy Methods #
	####################

	def printQuality(self):
		return scale_names[Scale.pitchClassToDecimal(self.getIntervals())]

	def getParentScale(self):
		return self.getParentDegree().getParentScale()

	def rotate(self):
		return self + 2
	
	def getRoot(self):
		return self[1]

	def getIntervals(self):
		result = []

		for degree in self.getDegrees():
			result.append(degree.getInterval())

		return result

	def getTones(self):
		result = []

		for degree in self.getDegrees():
			result.append(degree.getTone())

		return result

	def getDegreeByInterval(self, p_interval):

		for degree in self.getDegrees():

			if (degree.getInterval() == p_interval):
				return degree

		return None

	def findDegreeInParent(self, p_degree):
		parent_scale = self.getParentDegree().getParentScale()

		for degree in parent_scale:

			if (degree.getInterval() == (self.getParentDegree().getInterval() + p_degree.getInterval()).minimize()):
				return degree	

		return None

	##########################
	# Transformation methods #
	##########################

	def addInterval(self, p_interval):
		new_pitch_class = self.getIntervals()[:]
		new_pitch_class.append(p_interval)
		new_pitch_class.sort(key=lambda x: x.getSemitones())
		new_scale = type(self)(self[1].getTone(), new_pitch_class)

		return new_scale

	######################################################
	# Methods for logically calculating scale properties #
	######################################################

	def getHemitonia(self):
		return self.countIntervals(1)

	def getTritonia(self):
		return self.countIntervals(6)

	def countIntervals(self, p_interval_size):
		return collections.Counter(self.pitchClassToScaleSteps(self.getIntervals()))[p_interval_size]

	def getCardinality(self, p_system = DEFAULT_SYSTEM):
		return cardinality[p_system][len(self.getDegrees())]

	def hasCohemitonia(self):
		return (len(self.getCohemitonic()) != 0)

	def isPrime(self):
		return (self.getPrimeMode() == 1)

	def getImperfections(self):

		try:
			counter = 0

			for degree in self.getDegrees():

				if (P5 not in degree.buildPitchClass()):
					counter = counter + 1

			return counter

		except:
			print("Error: Failed to get imperfections for scale: " + str(self))
	
	def getRotationalSymmetry(self):

		try:
			parent_pitch_class = self.pitchClassToScaleSteps(self.getIntervals())
			result = []

			for degree in self.getDegrees():
				child_pitch_class = self.pitchClassToScaleSteps(degree.buildPitchClass())

				if (parent_pitch_class == child_pitch_class):
					result.append(degree.getPosition())

			return result

		except:
			print("Error: Failed to get rotational symmetry for scale: " + str(self))

	def getReflectionAxes(self):

		try:
			result = []

			for degree in self.getDegrees():
				scale_steps = self.pitchClassToScaleSteps(degree.buildPitchClass())

				if (scale_steps == scale_steps[::-1]):
					result.append(degree.getPosition())

			return result 

		except:
			print("Error: Failed to get reflection axes for scale: " + str(self))

	def getIntervalVector(self, p_system = DEFAULT_SYSTEM):

		try: 
			all_intervals = []

			for degree in self.getDegrees():
				all_intervals = all_intervals + degree.buildPitchClass()[1:]

			all_pitch_classes = []

			for interval in all_intervals:
				semitones = interval.getSemitones()

				if (semitones > 11):
					semitones = semitones - 12

				all_pitch_classes.append(Interval_Spectrum[p_system][semitones])

			counter = collections.Counter(all_pitch_classes)
			result = ""

			for key in counter.keys():
				result = result + key + "(" + str(int(counter[key]/2)) + ")"

			return result

		except:
			print("Error: Failed to retrieve interval vector for scale: " + str(self))

	def isChiral(self):

		try:
			reflection = self.pitchClassToScaleSteps(self.getIntervals())[::-1]
			result = []

			for degree in self.getDegrees():
				rotation = self.pitchClassToScaleSteps(degree.buildPitchClass())

				if (rotation == reflection):
					return False

			return True

		except:
			print("Error: Failed to check chirality for scale: " + str(self))

	def getCohemitonic(self):

		try:
			result = []
			scale_steps = (self.pitchClassToScaleSteps(self.getIntervals())*2)

			for i in range(int(len(scale_steps)/2)):

				if (scale_steps[i] == 1 and scale_steps[i + 1] == 1):
					result.append(i + 1)

			return result

		except:
			print("Error: Failed to retrieve cohemitonic tone")

	def getPrimeMode(self, p_consider_inverted_modes = False):

		try: 
			min_count = 1000

			for degree in self.getDegrees():
				pitch_class = degree.buildPitchClass()
				sum = 0

				for interval in pitch_class:
					sum = sum + interval.getSemitones()

				if (sum < min_count):
					print(sum)
					prime_mode = str(degree.getPosition())
					min_count = sum
				
				if (p_consider_inverted_modes):
					inverted_pitch_class = self.scaleStepsToPitchClass(self.pitchClassToScaleSteps(degree.buildPitchClass()))
					sum = 0

					for interval in inverted_pitch_class:
						sum = sum + interval.getSemitones()

					if (sum < min_count):
						prime_mode = str(degree.getPosition()) + "Inverted"
						min_count = sum
				
			return prime_mode

		except:
			print("Error: Failed to get prime mode of scale: " + str(self))

	#######################
	# Getters and Setters #
	#######################
   
	def getIntervals(self):
		result = []
		for degree in self.getDegrees():
			result.append(degree.getInterval())

		return result
	def getDegrees(self):
		return self.degrees
	def getTonicTone(self):
		return self.tonic_tone
	def getParentDegree(self):
		if (self.parent_degree != None):
			return self.parent_degree

		return None

	def setIntervals(self, p_intervals):
		self.intervals = p_intervals
	def setDegrees(self, p_degrees):
		self.degrees = p_degrees
	def setTonicTone(self, p_tonic_tone):
		self.tonic_tone = p_tonic_tone
	def setParentDegree(self, p_parent_degree):
		self.parent_degree = p_parent_degree

	# Internal Class Name: _Degree
	# Parameters: p_interval (Interval associated with the degree), p_parent_scale (scale associated with scale degree)
	# Info: The degree object is part of the scale object, you cannot create a scale degree without a scale
	# Method distanceFromClosest: Finds the smallest distance from this degree tone to another degree tone within the scale
	# Method distanceFromNext: Finds the distance to the next repetition of a scale degree tone
	# Method buildChord: Builds and returns a chord on the current scale degree givin a number of tones and the leap between each tone in the chord
	# Method buildScale: Builds and returns a scale on the current scale degree based off the parent scale
	# Method buildScaleWithIntervals: Builds and returns a scale on the current scale degree based off an scale parameter

	# TODO 
	# def getAppoggiaturas()
	class _Degree:
		def __init__(self, p_interval, p_parent_scale, p_octaves = 0):
			self.interval = p_interval
			self.parent_scale = p_parent_scale

			degree_tone = self.getParentScale().intervalToTone(self.getParentScale().getTonicTone(), p_interval, DEFAULT_SYSTEM)
			self.setTone(degree_tone)

		#####################################
		# Methods concerning class behavior #
		#####################################

		def __copy__(self):
			new_degree = _Degree(self.getInterval(), self.getParentScale())
			return new_degree

		def __str__(self):
			return self.getTone()

		##############
		# Comparison #
		##############

		def __eq__(self, p_other):
			return (type(self) == type(p_other)) and ((self.getInterval() == p_other.getInterval()) and (self.getTone() == p_other.getTone()))

		def __ne__(self, p_other):
			return (not self == p_other)

		##############
		# Arithmetic #
		##############

		def __add__(self, p_other):

			if (isinstance(p_other, Interval)):

				try:

					new_interval = (self.getInterval() + p_other).minimize()

					if not new_interval in self.getParentScale():
						new_scale = self.getParentScale().addInterval(new_interval)

						return new_scale.getDegreeByInterval(new_interval)

					return self.getParentScale().getDegreeByInterval(new_interval)

				except:
					print("Error: Failed to assign tones to the new scale")

			if (isinstance(p_other, int)):
				
				if (p_other == 1):
					return self

				return self.next() + (p_other - 1)

			if (isinstance(p_other, str)):
				return str(self) + p_other
		
		def __radd__(self, p_other):

			if (isinstance(p_other, str)):
				return p_other + str(self)

		def __sub__(self, p_other):

			if (isinstance(p_other, Interval)):

				try:

					new_interval = (self.getInterval() - p_other).minimize()

					while (new_interval < P1):
						new_interval = new_interval + P8

					if not new_interval in self.getParentScale():
						new_scale = self.getParentScale().addInterval(new_interval)

						return new_scale.getDegreeByInterval(new_interval)

					return self.getParentScale().getDegreeByInterval(new_interval)

				except:
					print("Error: Failed to assign tones to the new scale")

			if (isinstance(p_other, int)):

				if (p_other == 1):
					return self

				return self.previous() - (p_other - 1)


		#############################################################
		# Methods concerned with measuring distance between degrees #
		#############################################################

		def distanceFrom(self, p_other):

			if (self.getInterval().getSemitones() < p_other.getInterval().getSemitones()):
				return p_other.getInterval() - self.getInterval()
			else: 
				return self.getInterval() - p_other.getInterval() 

		def distanceFromNext(self, p_other):

			if (self.getInterval().getSemitones() < p_other.getInterval().getSemitones()):
				return p_other.getInterval() - self.getInterval()
			else:
				return (P8 - self.getInterval()) + p_other.getInterval()

		######################################################
		# Methods concerned with operations on scale degrees #
		######################################################

		def build(self, object_type, p_num_tones = 4, p_leap_size = 3, *args):

			#try:
				child_intervals = self.buildPitchClass(p_leap_size)[:p_num_tones]

				child_object = object_type(self.getTone(), child_intervals, *args)
				child_object.setParentDegree(self)

				return child_object

			#except:
			# 	print("Error: Failed to build chord")

		def buildWithIntervals(self, object_type, p_pitch_class, *args):

			#try:
				child_object = object_type(self.getTone(), p_pitch_class, *args)
				child_object.setParentDegree(self)

				return child_object

			#except:
			#	print("Error: Failed to build chord")

		def buildScale(self):

			try:
				child_intervals = self.buildPitchClass()
				child_scale = Scale(self.getTone(), child_intervals)
				child_scale.setParentDegree(self)
				return child_scale

			except:
				print("Error: Failed to build scale")


		def buildScaleWithIntervals(self, p_intervals):

			try:
				new_scale = Scale(self.getTone(), p_intervals)
				new_scale.setParentDegree(self)

				return new_scale

			except:
				print("Error: Failed to build custom scale!")

		def buildPitchClass(self, p_leap_size = 2, p_system = DEFAULT_SYSTEM):

			try:
				parent_degrees = self.getParentScale().getDegrees() * 7
				child_intervals = [P1]
				p_leap_size = p_leap_size - 1

				# Counters
				i = parent_degrees.index(self) + p_leap_size		

				# Loop until we have reached the starting degree
				while (parent_degrees[i] != self):
					new_interval = self.distanceFromNext(parent_degrees[i])

					# Add degree to list
					child_intervals.append(new_interval)

					# Increment
					i = i + p_leap_size
					
				return child_intervals

			except:
				print("Error: Failed to build pitch class set")

		##########################
		# Transformation methods #
		##########################

		def transform(self, p_accidental, p_system = DEFAULT_SYSTEM):

			try:
				new_interval = self.getInterval().transform(p_accidental)
				new_pitch_class = self.getParentScale().getIntervals()[:]
				new_pitch_class = [item for item in new_pitch_class if item != self.getInterval()]
				new_pitch_class.append(new_interval)
				new_pitch_class.sort(key=lambda x: x.getNumeral())
				new_object = type(self.getParentScale())(self.getParentScale()[1].getTone(), new_pitch_class)

				return new_object

			except:
				print("Error: Failed to transform " + self + " by " + p_accidental)

		####################
		# Courtesy methods #
		####################

		def getPosition(self):
			return self.getParentScale().getDegrees().index(self) + 1

		def next(self):
			if (self.getPosition() == len(self.getParentScale().getDegrees())):
				return self.getParentScale()[1]

			return self.getParentScale()[self.getPosition() + 1]

		def previous(self):
			if (self.getPosition() == 1):
				return self.getParentScale()[-0]

			return self.getParentScale()[self.getPosition() - 1]

		#######################
		# Getters and Setters #
		#######################
		
		def getOctaves(self):
			return self.octaves
		def getTone(self):
			return self.tone	
		def getInterval(self):
			return self.interval
		def getParentScale(self):
			return self.parent_scale

		def setOctaves(self, p_octaves):
			self.octaves = p_octaves
		def setTone(self, p_tone):
			self.tone = p_tone
		def setInterval(self, p_interval):
			self.interval = p_interval
		def setParentScale(self, p_parent_scale):
			self.parent_scale = p_parent_scale
			