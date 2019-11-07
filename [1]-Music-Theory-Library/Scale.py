from Interval import Interval
from Constants import *
from HelperMethods import *

import collections

# Class Name: Scale
# Parameters: p_tonic_note (The tonic note the scale will be built off of), p_intervals (the interval pattern of the scale)
# Info: A scale object requires a tonic tone and an interval pattern
# Method getDegree: Retrieves the nth degree in the scale
# Method getDegreeByInterval: Retrieves the degree that is a certain interval from the tonic
class Scale:
	def __init__(self, p_tonic_note, p_intervals):
		self.tonic_note = p_tonic_note
		self.intervals = p_intervals
		self.degrees = []

		for i in range(len(p_intervals)):
			self.degrees.append(_Degree(self.intervals[i], self))

		try:
			counter = 0
			try:
				white_notes = (self.getTonicNote()[0] + ("ABCDEFG"*2).split(self.getTonicNote()[0])[1])*4
			except: 
				print("Something went wrong, ensure your tonic note is correctly assigned")
			for i in range(len(self.getDegrees())):
				degree = self.getDegrees()[i]
				possible_notes = (TONES.get(System)*4)[([TONES.get(System).index(item) for item in TONES.get(System) if self.getTonicNote() in item][0] + degree.getInterval().getSemitones())]
				next_note = [item for item in possible_notes if white_notes[counter] in item][0]
				degree.setNote(next_note)
				if (i != len(self.getDegrees()) - 1):
					skip_size = self.getDegrees()[i + 1].getInterval().getNumeral() - degree.getInterval().getNumeral()
					counter = counter + skip_size
		except:
			print("Something went wrong when assigning notes to your scale, ensure the intervals are sorted by increasing size")

	#####################################
	# Methods concerning class behavior #
	#####################################
	
	def __str__(self):
		result = "["
		for degree in self.getDegrees():
			result = result + degree.__str__() + ", "
		return result[:-2] + "]"

	def __eq__(self, p_other):
		if (isInstance(p_other, Scale)):
			return (self.getIntervals() == p_other.getIntervals()) and (self.getTonicNote() == p_other.getTonicNote())

	def __getitem__(self, p_index):
		try:
			return self.getDegrees()[p_index - 1]
		except: 
			print("Error: Scale indices return scale degrees, ranging from (1-n) where the n is the cardinality of your scale")
	
	def __contains__(self, p_other):
		if (isinstance(p_other, Scale)):
			if (all(elem in self.getNotes() for elem in p_other.getNotes())):
				return True
			return False
		if (isinstance(p_other, Chord)):
			if (all(elem in self.getNotes() for elem in p_other.getNotes())):
				return True
			return False
		if (isinstance(p_other, str)):
			if (p_other in self.getNotes()):
				return True
			return False
		if (isinstance(p_other, list)):
			if (isinstance(p_other[0], Interval)):
				for degree in self.getDegrees():
					if (all(elem in degree.buildPitchClass() for elem in p_other)):
						return True
				return False

	def __add__(self, p_other):
		if (isinstance(p_other, int)):
			try:
				possible_tonics = (TONES.get(System)*2)[([TONES.get(System).index(item) for item in TONES.get(System) if self.getTonicNote() in item][0] + p_other)]
				min_length = 1000
				for item in possible_tonics:
					scale = Scale(item, self.getIntervals())
					if (len(scale.__str__()) < min_length):
						min_length = len(scale.__str__())
						result = scale
				return result
			except:
				print("Error: Failed to assign notes to the new scale")

		if (isinstance(p_other, str)):
			return str(self) + p_other

	def __radd__(self, p_other):
		if (isinstance(p_other, str)):
			return p_other + str(self)

	########
	# Misc #
	########

	def getDegreeByInterval(self, p_interval):
		for degree in self.getDegrees():
			if (degree.getInterval() == p_interval):
				return degree
			return -1

	######################################################
	# Methods for logically calculating scale properties #
	######################################################

	def getCardinality(self, system = "western"):
		return cardinality["western"][len(self.getDegrees())]

	def getImperfections(self):
		try:
			counter = 0
			for degree in self.getDegrees():
				if (P5 not in degree.buildPitchClass()):
					counter = counter + 1
			return counter
		except:
			print("Error: Failed to get imperfections")
	
	def getRotationalSymmetry(self):
		try:
			parent_pitch_class = self.getScaleSteps(self.getIntervals())
			result = []
			for degree in self.getDegrees():
				child_pitch_class = self.getScaleSteps(degree.buildPitchClass())
				if (parent_pitch_class == child_pitch_class):
					result.append(degree.getPosition())
			return result
		except:
			print("Error: Failed to get rotational symmetry")

	def getHemitonia(self):
		return self.countIntervals(1)

	def getTritonia(self):
		return self.countIntervals(6)

	def countIntervals(self, p_interval_size):
		counter = collections.Counter(self.getScaleSteps(self.getIntervals()))
		return counter[p_interval_size]

	def getReflectionAxes(self):
		try:
			result = []
			for degree in self.getDegrees():
				scale_steps = self.getScaleSteps(degree.buildPitchClass())
				if (scale_steps == scale_steps[::-1]):
					result.append(degree.getPosition())
			return result 
		except:
			print("Error: Failed to get reflection axes")

	def getIntervalVector(self, system = "western"):
		try: 
			all_intervals = []
			for degree in self.getDegrees():
				all_intervals = all_intervals + degree.buildPitchClass()[1:]
			all_pitch_classes = []
			for interval in all_intervals:
				semitones = interval.getSemitones()
				if (semitones > 11):
					semitones = semitones - 12
				all_pitch_classes.append(Interval_Spectrum[system][semitones])
			counter = collections.Counter(all_pitch_classes)
			result = ""
			for key in counter.keys():
				result = result + key + "(" + str(int(counter[key]/2)) + ")"
			return result
		except:
			print("Error: Failed to retrieve interval vector for scale")

	def isChiral(self):
		try:
			reflection = self.getScaleSteps(self.getIntervals())[::-1]
			result = []
			for degree in self.getDegrees():
				rotation = self.getScaleSteps(degree.buildPitchClass())
				if (rotation == reflection):
					return False
			return True
		except:
			print("Error: Failed to check if scale is chiral")

	def getCohemitonic(self):
		try:
			result = []
			scale_steps = (self.getScaleSteps(self.getIntervals())*2)
			for i in range(int(len(scale_steps)/2)):
				if (scale_steps[i] == 1 and scale_steps[i + 1] == 1):
					result.append(i + 1)
			return result
		except:
			print("Error: Failed to retrieve cohemitonic note")

	def hasCohemitonia(self):
		if (len(self.getCohemitonic()) != 0):
			return True
		return False

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
					inverted_pitch_class = self.getPitchClass(self.getScaleSteps(degree.buildPitchClass()))

					sum = 0
					for interval in inverted_pitch_class:
						sum = sum + interval.getSemitones()
					if (sum < min_count):
						prime_mode = str(degree.getPosition()) + "Inverted"
						min_count = sum
				
			return prime_mode
		except:
			print("Error: Failed to get prime mode of scale")

	def isPrime(self):
		if (self.getPrimeMode() == 1):
			return True
		return False
			
	# TODO 
	# def isPalindromic(self)
	# def isHelotonic(self)
	# def isMaximallyEven(self)
	# def isBalanced(self)

	def getScaleSteps(self, p_pitch_class):
		try:
			result = []
			previous = 0
			for interval in p_pitch_class[1:]:
				result.append(interval - previous)
				previous = interval.getSemitones()
			result.append(abs(p_pitch_class[-1].getSemitones() - 12))
			return result
		except:
			print("Error: Failed to retrieve scale steps")

	def getPitchClass(self, p_scale_steps):
		try:
			result = []
			count = 0
			for integer in p_scale_steps:
				count = count + integer
				result.append(Intervals[count])
			return result
		except:
			print("Error: Failed to retrieve pitch class")

	def getNotes(self):
		result = []
		for degree in self.getDegrees():
			result.append(degree.getNote())
		return result

	def findDegreeInParent(self, p_degree):
		for degree in self.getParentDegree().getParentScale():
			if (degree.getNote() == p_degree.getNote()):
				return degree
		return -1

	#######################
	# Getters and Setters #
	#######################
   
	def getIntervals(self):
		return self.intervals
	def getDegrees(self):
		return self.degrees
	def getTonicNote(self):
		return self.tonic_note
	def getParentDegree(self):
		return self.parent_degree

	def setIntervals(self, p_intervals):
		self.intervals = p_intervals
	def setDegrees(self, p_degrees):
		self.degrees = p_degrees
	def setTonicNote(self, p_tonic_note):
		self.tonic_note = p_tonic_note
	def setParentDegree(self, p_parent_degree):
		self.parent_degree = p_parent_degree

# Internal Class Name: _Degree
# Parameters: p_interval (Interval associated with the degree), p_parent_scale (scale associated with scale degree)
# Info: The degree object is part of the scale object, you cannot create a scale degree without a scale
# Method distanceFromClosest: Finds the smallest distance from this degree note to another degree note within the scale
# Method distanceFromNext: Finds the distance to the next repetition of a scale degree note
# Method buildChord: Builds and returns a chord on the current scale degree givin a number of notes and the leap between each note in the chord
# Method buildScale: Builds and returns a scale on the current scale degree based off the parent scale
# Method buildScaleWithIntervals: Builds and returns a scale on the current scale degree based off an scale parameter		
class _Degree:
	def __init__(self, p_interval, p_parent_scale):
		self.interval = p_interval
		self.parent_scale = p_parent_scale

	#####################################
	# Methods concerning class behavior #
	#####################################

	def __eq__(self, p_other):
		return (self.getInterval().getSemitones() == p_other.getInterval().getSemitones()) and (self.getNote() == p_other.getNote())

	def __str__(self):
		return self.getNote()

	def __add__(self, p_other):
		try:
			if (isinstance(p_other, int)):
				return (self.getParentScale().getDegrees()*2)[self.getParentScale().getDegrees().index(self) + p_other]
		except:
			print("Error: Failed to add " + str(p_other) + " to degree")

	def __sub__(self, p_other):
		return (self.getParentScale().getDegrees()*2)[self.getParentScale().getDegrees().index(self) - p_other]

	#############################################################
	# Methods concerned with measuring distance between degrees #
	#############################################################

	def distanceFromClosest(self, p_other):
		return abs(self.getInterval().getSemitones() - p_other.getInterval().getSemitones())

	def distanceFromNext(self, p_other):
		result = self.getInterval().getSemitones() - p_other.getInterval().getSemitones()
		while (result > 0):
			result -= 12
		return abs(result)

	######################################################
	# Methods concerned with operations on scale degrees #
	######################################################

	def buildChord(self, p_num_notes = 4, p_leap_size = 2):
		# try:
			child_intervals = self.buildPitchClass(p_leap_size)[:p_num_notes]
			child_chord = Chord(self.getNote(), child_intervals)
			child_chord.setParentDegree(self)
			child_chord.setLeapSize(p_leap_size)
			return child_chord
		# except:
		# 	print("Error: Failed to build chord")

	def buildScale(self):
		try:
			child_intervals = self.buildPitchClass()
			child_scale = Scale(self.getNote(), child_intervals)
			child_scale.setParentDegree(self)
			return child_scale
		except:
			print("Error: Failed to build scale")

	def buildPitchClass(self, p_leap_size = 1, system = "western"):
		# try:
			parent_degrees = self.getParentScale().getDegrees() * 3
			previous = 0
			padding = 0
			child_intervals = [P1]
			i = parent_degrees.index(self) + p_leap_size
			degree_count = 1 + p_leap_size
			while (parent_degrees[i] != self):
				interval_semitones = self.distanceFromNext(parent_degrees[i])
				if (interval_semitones < previous):
					padding = padding + 12
				possible_intervals = Intervals[system][interval_semitones + padding]
				matches = [item for item in possible_intervals if degree_count == item.getNumeral()]
				if (len(matches) != 0):
					selected_interval = matches[0]
				else:
					selected_interval = min(possible_intervals, key=lambda x:abs(x.getNumeral()-degree_count))
				child_intervals.append(selected_interval)
				previous = self.distanceFromNext(parent_degrees[i])
				i = i + p_leap_size
				degree_count = degree_count + p_leap_size
			return child_intervals
		# except:
		# 	print("Error: Failed to build pitch class set")

	def buildScaleWithIntervals(self, p_intervals):
		try:
			new_scale = Scale(self.getNote(), p_intervals)
			new_scale.setParentDegree(self)
			return new_scale
		except:
			print("Error: Failed to build custom scale!")

	def getPosition(self):
		return self.getParentScale().getDegrees().index(self) + 1

	#######################
	# Getters and Setters #
	#######################
	
	def getNote(self):
		return self.note	
	def getInterval(self):
		return self.interval
	def getParentScale(self):
		return self.parent_scale

	def setNote(self, p_note):
		self.note = p_note
	def setInterval(self, p_interval):
		self.interval = p_interval
	def setParentScale(self, p_parent_scale):
		self.parent_scale = p_parent_scale

class Chord(Scale):
	def __init__(self, p_note, p_intervals):
		super().__init__(p_note, p_intervals)

	#####################################
	# Methods concerning class behavior #
	#####################################

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
		
	def __getitem__(self, p_other):
		if (isinstance(p_other, slice)):
			new_chord = self.findDegreeInParent(self[p_other.start]).buildChord(p_other.stop - (p_other.start - 1), self.getLeapSize())
			return new_chord
		else:
			return self.getDegrees()[p_other - 1]

	######################################################
	# Methods concerning string representaton of a chord #
	######################################################

	def printQuality(self, system = "western", style = 2):
		try: 
			chord_intervals = self.getIntervals()
			smallest_difference = 1000
			accidentals = ""
			for key in Chord_Qualities[system].keys():
				temp_accidentals = ""
				count = 0
				i = 0
				while(i < len(chord_intervals)):
					if (chord_intervals[i] != Chord_Qualities[system][key][i]):
						count = count + 1
						if (chord_intervals[i].getSemitones() < Chord_Qualities[system][key][i].getSemitones()):
							temp_accidentals = temp_accidentals + "b" + str(((i + 1) * 2) - 1)
						else:
							temp_accidentals = temp_accidentals + "#" + str(((i + 1) * 2) - 1)
					i = i + 1
				if (count < smallest_difference):
					closest_match = key
					smallest_difference = count
					accidentals = temp_accidentals
			
			return closest_match[style] + str((len(self.getDegrees())*2)-1) + accidentals
		except: 
			print("Error: Failed to create string represention of the chord")

	def printNumeral(self, system = "western"):
		numeral = intToRoman(self.getParentDegree().getInterval().getNumeral())
		if (self[1:3].printQuality(system, 0) == "minor"):
			numeral = position.lower()
		accidental = self.getParentDegree().getInterval().getAccidental()
		return  accidental + numeral

	def jazzNumeralNotation(self, system = "western"):
		return self.printNumeral() + self.printQuality() 

	###########################################################
	# Methods concerning harmonic movement and transformation #
	###########################################################

	def resolveChord(self, p_voice_leading_rules = circleOfFifths):
		return p_voice_leading_rules(self)

	def getRelativeChord(self):
		return self - 2

	def getSecondaryDominant(self):
		return self.getParentDegree().buildScaleWithIntervals(major)[5].buildChord()

	def getLeapSize(self):
		return self.leap_size

	def setLeapSize(self, p_leap_size):
		self.leap_size = p_leap_size

	# TODO 
	# def transformChordTo(self, p_intervals):
	# def getParallelChord(self):
		