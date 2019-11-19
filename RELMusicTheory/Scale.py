
import collections

from Interval import Interval
from Constants import *
from HelperMethods import *

# Class Name: Scale
# Parameters: p_tonic_tone (The tonic tone the scale will be built off of), p_intervals (the interval pattern of the scale)
# Info: A scale object requires a tonic tone and an interval pattern
# Method getDegree: Retrieves the nth degree in the scale
# Method getDegreeByInterval: Retrieves the degree that is a certain interval from the tonic

class Scale:

	def __init__(self, p_tonic_tone, p_intervals):
		self.tonic_tone = p_tonic_tone
		self.intervals = p_intervals
		self.degrees = [[]]

		tones = self.intervalsToTones(p_tonic_tone, p_intervals)

		for i in range(len(p_intervals)):
			child_degree = _Degree(self.intervals[i], self)
			child_degree.setTone(tones[i])
			child_degree.setOctaves(0)
			
			self.degrees[0].append(child_degree)

	#####################################
	# Methods concerning class behavior #
	#####################################
	
	def __str__(self):
		result = "["

		for degree in self.getDegrees():
			result = result + str(degree) + ", "

		return result[:-2] + "]"

	def __eq__(self, p_other):
		return (self.getIntervals() == p_other.getIntervals()) and (self.getTonicTone() == p_other.getTonicTone())

	def __getitem__(self, p_index):
		return self.getDegrees()[p_index - 1]
	
	def __contains__(self, p_other):

		if (isinstance(p_other, Scale)):
			return all(elem in self.getTones() for elem in p_other.getTones())

		if (isinstance(p_other, Chord)):
			return all(elem in self.getTones() for elem in p_other.getTones())

		if (isinstance(p_other, str)):
			return p_other in self.getTones()

		if (isinstance(p_other, list)):

			if (isinstance(p_other[0], Interval)):

				for degree in self.getDegrees():
					if (all(elem in degree.buildPitchClass() for elem in p_other)):
						return True

				return False

	##############
	# Arithmetic #
	##############

	def __mul__(self, p_other):

		try:
			list_of_degree_lists = self.getDegrees(-1)

			for i in range(1, p_other):
				list_of_degree_lists.append([])

				for degree in self.getDegrees():
					copied_degree = degree.__copy__()
					copied_degree.setOctaves(i)
					list_of_degree_lists[i].append(copied_degree)
			
			return self

		except:
			print("Error: Failed to multiply scale")

	def __add__(self, p_other):

		try:

			if (isinstance(p_other, Interval)):
					min_length = 1000

					for item in [item for item in (self[1] + p_other) if len(item.getTone()) < 3]:
						scale = item.buildScaleWithIntervals(self.getIntervals())
						
						if (len(str(scale)) < min_length):
							min_length = len(str(scale))
							result = scale
							
					return result

			if (isinstance(p_other, int)):
				return (self[1] + p_other).buildScaleWithIntervals(self.getIntervals())

			if (isinstance(p_other, str)):
				return str(self) + p_other

		except:
			print("Error: Failed to add " + str(p_other) + " to " + str(self))

	def __radd__(self, p_other):

		if (isinstance(p_other, str)):
			return p_other + str(self)

	def __sub__(self, p_other):
		return -1

	##################
	# Helper Methods #
	##################

	def pitchClassToScaleSteps(self, p_pitch_class):

		try:
			result = []

			# Counters
			previous = 0

			# Loop through every element of the pitch class list except the first
			for interval in p_pitch_class[1:]:
				result.append(interval - previous)
				previous = interval.getSemitones()

			# Add the distance between the last degree and the first
			result.append(abs(p_pitch_class[-1].getSemitones() - 12))

			return result

		except:
			print("Error: Failed to retrieve scale steps")

	def scaleStepsToPitchClass(self, p_scale_steps, p_system = DEFAULT_SYSTEM):

		try:
			intervals = self.getInterval().generateIntervalList()
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

	def intervalsToTones(self, p_tonic_tone, p_intervals, p_system = DEFAULT_SYSTEM):
		
		try:
			result = []

			# Counters
			counter = 0

			# Loop until interval list is traversed
			for i in range(len(p_intervals)):
				interval = p_intervals[i]

				# find the tone that matches semitones and position with respect to the degree of the interval
				next_tone = self.intervalToTone(self.getTonicTone(), interval, p_system)

				# add the resulting tone to the list
				result.append(next_tone)

				# keeps track of how many tones to skip in the white_tones list
				if (i != len(p_intervals) - 1):
					skip_size = p_intervals[i + 1].getNumeral() - interval.getNumeral()
					counter = counter + skip_size

			return result

		except:
			print("Something went wrong when assigning tones to your scale, ensure the intervals are sorted by increasing size")

	def intervalToTone(self, p_principle_tone, p_interval, p_system = DEFAULT_SYSTEM):
		try:
			white_tones = (p_principle_tone + ("ABCDEFG"*2).split(p_principle_tone)[1])*4
			possible_tones = (TONES.get(p_system)*4)[([TONES.get(p_system).index(item) for item in TONES.get(p_system) if p_principle_tone in item][0] + p_interval.getSemitones())]
			next_tone = [item for item in possible_tones if white_tones[p_interval.getNumeral() - 1] in item][0]

			return next_tone
		
		except:
			print("Error: Failed to convert " + p_interval + " to a tone using a principle tone of " + p_principle_tone + " and the system " + p_system)

	def getTones(self):
		result = []

		for degree in self.getDegrees():
			result.append(degree.getTone())

		return result

	def getDegreeByInterval(self, p_interval):
		for degree in self.getDegrees():
			if (degree.getInterval() == p_interval):
				return degree

		return -1

	def findDegreeInParent(self, p_degree):
		for degree in self.getParentDegree().getParentScale():
			if (degree.getTone() == p_degree.getTone()):
				return degree	

		return -1

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
		return self.intervals
	def getDegrees(self, p_octaves = 0):
		if (p_octaves == -1):
			return self.degrees
		if (p_octaves == -2):
			return [item for sublist in self.degrees for item in sublist]
		return self.degrees[p_octaves]
	def getTonicTone(self):
		return self.tonic_tone
	def getParentDegree(self):
		return self.parent_degree

	def setIntervals(self, p_intervals):
		self.intervals = p_intervals
	def setDegrees(self, p_degrees):
		self.degrees = p_degrees
	def setTonicTone(self, p_tonic_tone):
		self.tonic_tone = p_tonic_tone
	def setParentDegree(self, p_parent_degree):
		self.parent_degree = p_parent_degree

	# TODO 
	# def isPalindromic(self)
	# def isHelotonic(self)
	# def isMaximallyEven(self)
	# def isBalanced(self)

# Internal Class Name: _Degree
# Parameters: p_interval (Interval associated with the degree), p_parent_scale (scale associated with scale degree)
# Info: The degree object is part of the scale object, you cannot create a scale degree without a scale
# Method distanceFromClosest: Finds the smallest distance from this degree tone to another degree tone within the scale
# Method distanceFromNext: Finds the distance to the next repetition of a scale degree tone
# Method buildChord: Builds and returns a chord on the current scale degree givin a number of tones and the leap between each tone in the chord
# Method buildScale: Builds and returns a scale on the current scale degree based off the parent scale
# Method buildScaleWithIntervals: Builds and returns a scale on the current scale degree based off an scale parameter

class _Degree:
	def __init__(self, p_interval, p_parent_scale, p_octaves = 0):
		self.interval = p_interval
		self.parent_scale = p_parent_scale

	#####################################
	# Methods concerning class behavior #
	#####################################

	def __eq__(self, p_other):
		return (self.getInterval() == p_other.getInterval()) and (self.getTone() == p_other.getTone())

	def __copy__(self):
		new_degree = _Degree(self.getInterval(), self.getParentScale())
		new_degree.setTone(self.getTone())
		return new_degree

	def __str__(self):
		return self.getTone()

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):

		if (isinstance(p_other, Interval)):

			try:
				degree_tone = self.getParentScale().intervalToTone(self.getTone(), p_other, DEFAULT_SYSTEM)
				degree = _Degree(p_other, self.getParentScale())
				degree.setTone(degree_tone)
				return degree

			except:
				print("Error: Failed to assign tones to the new scale")

		if (isinstance(p_other, int)):
			return self.getParentScale().getDegrees(-2)[self.getParentScale().getDegrees(-2).index(self) + p_other]

		if (isinstance(p_other, str)):
			return str(self) + p_other
	
	def __radd__(self, p_other):

		if (isinstance(p_other, str)):
			return p_other + str(self)

	def __sub__(self, p_other):

		if (isinstance(p_other, int)):
			return (self.getParentScale().getDegrees()*2)[self.getParentScale().getDegrees().index(self) - p_other]

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

	def buildChord(self, p_num_tones = 4, p_leap_size = 2):

		try:
			child_intervals = self.buildPitchClass(p_leap_size)[:p_num_tones]

			child_chord = Chord(self.getTone(), child_intervals)
			child_chord.setParentDegree(self)
			child_chord.setLeapSize(p_leap_size)
			return child_chord

		except:
		 	print("Error: Failed to build chord")

	def buildScale(self):

		try:
			child_intervals = self.buildPitchClass()
			child_scale = Scale(self.getTone(), child_intervals)
			child_scale.setParentDegree(self)
			return child_scale

		except:
			print("Error: Failed to build scale")

	def buildPitchClass(self, p_leap_size = 1, p_system = DEFAULT_SYSTEM):

		try:
			parent_degrees = (self.getParentScale()*7).getDegrees(-2)
			child_intervals = [P1]

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

	def buildScaleWithIntervals(self, p_intervals):

		try:
			new_scale = Scale(self.getTone(), p_intervals)
			new_scale.setParentDegree(self)

			return new_scale

		except:
			print("Error: Failed to build custom scale!")

	def getPosition(self):
		return self.getParentScale().getDegrees().index(self) + 1

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

	# TODO 
	# def getAppoggiaturas()

class Chord(Scale):
	def __init__(self, p_tone, p_intervals):
		super().__init__(p_tone, p_intervals)

	#####################################
	# Methods concerning class behavior #
	#####################################

	def __getitem__(self, p_other):
		
		if (isinstance(p_other, slice)):
			new_chord = self.findDegreeInParent(self[p_other.start]).buildChord(p_other.stop - (p_other.start - 1), self.getLeapSize())
			return new_chord
		else:
			return self.getDegrees()[p_other - 1]


	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):

		if (isinstance(p_other, str)):
			return str(self) + p_other

		if (isinstance(p_other, int)):
			return self.getParentDegree().__add__(p_other).buildChord()

	def __radd__(self, p_other):

		if (isinstance(p_other, str)):
			return p_other + str(self)

		if (isinstance(p_other, int)):
			return self.getParentDegree().__add__(p_other).buildChord()

	def __sub__(self, p_other):

		if (isinstance(p_other, int)):
			return self.getParentDegree().__sub__(p_other).buildChord()
		
	######################################################
	# Methods concerning string representaton of a chord #
	######################################################

	def printQuality(self, p_system = DEFAULT_SYSTEM, style = 2):
		#try: 
			chord_intervals = self.rearrangeIntervalsAsThirds()

			# Counters
			smallest_difference = 1000
			accidentals = ""

			# Loop through all known chord qualities
			for key in Chord_Qualities[p_system].keys():

				# Counters
				temp_accidentals = ""
				count = 0
				i = 0

				# Loop through all the chord intervals
				while(i < len(chord_intervals)):

					# Check if chord interval is not None object
					if (chord_intervals[i]):

						# Check if interval does not match with interval in dictionary
						if (chord_intervals[i] != Chord_Qualities[p_system][key][i]):
							count = count + 1

							# Add a flat if the interval of the parent chord is smaller than the dictionary interval
							if (chord_intervals[i] < Chord_Qualities[p_system][key][i]):
								temp_accidentals = temp_accidentals + "b" + str(((i + 1) * 2) - 1)

							# Otherwise add a sharp
							else:
								temp_accidentals = temp_accidentals + "#" + str(((i + 1) * 2) - 1)
					else:
						temp_accidentals = temp_accidentals + "(omit" + str(((i + 1) * 2) - 1) + ")"

					i = i + 1

				# Check if the current match is the closest to the parent chords pitch class
				if (count < smallest_difference):
					closest_match = key
					smallest_difference = count
					accidentals = temp_accidentals

			return closest_match[style] + str(max([x.getNumeral() for x in chord_intervals if x])) + accidentals

		#except: 
		#	print("Error: Failed to create string represention of the chord")

	def printNumeral(self, p_system = DEFAULT_SYSTEM):
		numeral = intToRoman(self.getParentDegree().getInterval().getNumeral())
		if (self[1:3].printQuality(p_system, 0) == "minor"):
			numeral = position.lower()
		accidental = self.getParentDegree().getInterval().getAccidental()
		return  accidental + numeral

	def jazzNumeralNotation(self, p_system = DEFAULT_SYSTEM):
		return self.printNumeral(p_system) + self.printQuality(p_system) 

	def rearrangeIntervalsAsThirds(self, p_system = DEFAULT_SYSTEM):
		# try: 
			new_interval_list = []

			# Loop through all degrees in the chord
			for degree in self.getDegrees():
				possible_intervals = []

				# If the interval cannot be built on a sequence of thirds and it is less than 12 semitones large add 12
				if (((degree.getInterval().getNumeral() - 1) % 2) != 0 and degree.getInterval() < P8):
					new_interval = degree.getInterval() + P8

				# If the interval cannot be built on a sequence of thirds and it is greater than 12 semitones large subtract 12
				elif ((degree.getInterval().getNumeral() - 1) % 2 != 0 and degree.getInterval() > P8):
					new_interval = degree.getInterval()

					# subtract 12 until interval semitones is below 12
					while (new_interval > P8):
						new_interval -= P8
				else:
					new_interval = degree.getInterval()

				new_interval_list.append(new_interval)

			# Sort the new interval list by number of semitones in the intervals
			new_interval_list.sort(key=lambda x: x.getSemitones())

			# Counters
			previous_numeral = -1
			i = 0

			# Loop through the new interval list
			while (i < len(new_interval_list)):

				# If the previous degrees of the chard is missing place Nones in their position
				if (new_interval_list[i].getNumeral() - previous_numeral != 2):
					difference = new_interval_list[i].getNumeral() - previous_numeral

					# for all missing degrees do the following
					for j in range(int((difference - 2)/2)):
						new_interval_list.insert(i, None)
						i = i + 1

				previous_numeral = new_interval_list[i].getNumeral()
				i = i + 1

			return new_interval_list
		
		# except:
		#	print("Error: Failed to rearrange intervals of parent chord as thirds")

	###########################################################
	# Methods concerning harmonic movement and transformation #
	###########################################################

	def resolveChord(self, p_voice_leading_rules = circleOfFifths):
		return p_voice_leading_rules(self)

	def getRelativeChord(self):
		return self - 2

	def getSecondaryDominant(self):
		return self.getParentDegree().buildScaleWithIntervals(major)[5].buildChord()

	#######################
	# Getters and Setters #
	#######################

	def getLeapSize(self):
		return self.leap_size

	def setLeapSize(self, p_leap_size):
		self.leap_size = p_leap_size

	# TODO 
	# def transformChordTo(self, p_intervals):
	# def getParallelChord(self):
		