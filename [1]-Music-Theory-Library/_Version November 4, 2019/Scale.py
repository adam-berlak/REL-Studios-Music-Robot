from Interval import Interval
from Chord import Chord
from Constants import *

# Internal Class Name: Scale
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

		counter = 0
		white_notes = self.getTonicNote()[0] + ("ABCDEFG"*2).split(self.getTonicNote()[0])[1]
		for degree in self.getDegrees():
			possible_notes = (TONES.get(System)*2)[([TONES.get(System).index(item) for item in TONES.get(System) if self.getTonicNote() in item][0] + degree.getInterval().getSemitones())]
			next_note = [item for item in possible_notes if white_notes[counter] in item][0]
			degree.setNote(next_note)
			counter = counter + 1

	def __str__(self):
		result = "["
		for degree in self.getDegrees():
			result = result + degree.__str__() + ", "
		return result[:-2] + "]"

	def __eq__(self, p_other):
		return (self.getIntervals() == p_other.getIntervals()) and (self.getTonicNote() == p_other.getTonicNote())

	def __getitem__(self, p_index):
		return self.getDegrees()[p_index - 1]

	def __add__(self, p_other):
		if (isinstance(p_other, int)):
			possible_tonics = (TONES.get(System)*2)[([TONES.get(System).index(item) for item in TONES.get(System) if self.getTonicNote() in item][0] + p_other)]
			min_length = 1000
			for item in possible_tonics:
				scale = Scale(item, self.getIntervals())
				if (len(scale.__str__()) < min_length):
					min_length = len(scale.__str__())
					result = scale
			return result

		if (isinstance(p_other, str)):
			return str(self) + p_other

	def __radd__(self, p_other):
		if (isinstance(p_other, str)):
			return p_other + str(self)
		
	def getDegreeByInterval(self, p_interval):
		for degree in self.getDegrees():
			if (degree.getInterval() == p_interval):
				return degree
			return -1

	# def getCardinality(self)
	# def getPrimeMode(self)
	def getImperfections(self):
		counter = 0
		for degree in self.getDegrees():
			if (P5 not in degree.buildPitchClass()):
				counter = counter + 1
		return counter
	def getReflectionAxes(self):
		for degree in self.getDegrees():
			scale_steps = self.getScaleSteps(degree.buildPitchClass())
			if (scale_steps == scale_steps[::-1]):
				result = degree.getPosition()
		return result 
	# def getIntervalVector(self)

	# def isPrime(self)
	# def isPalindromic(self)
	# def isHelotonic(self)
	# def isMaximallyEven(self)
	# def isBalanced(self)
	def getScaleSteps(self, p_pitch_class):
		result = []
		previous = 0
		for interval in p_pitch_class[1:]:
			result.append(interval - previous)
			previous = interval.getSemitones()
		result.append(abs(p_pitch_class[-1].getSemitones() - 12))
		return result
   
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

	def __eq__(self, p_other):
		return (self.getInterval() == p_other.getInterval()) and (self.getNote() == p_other.getNote())

	def __str__(self):
		return self.getNote()

	def __add__(self, p_other):
		if (isinstance(p_other, int)):
			return (self.getParentScale().getDegrees()*2)[self.getParentScale().getDegrees().index(self) + p_other]
		# elif (isinstance(p_other, Interval)):
		#	return self.getParentScale().getDegreeByInterval((Intervals*2)[self.getInterval() + p_other])

	def __sub__(self, p_other):
		return (self.getParentScale().getDegrees()*2)[self.getParentScale().getDegrees().index(self) - p_other]

	def distanceFromClosest(self, p_other):
		return abs(self.getInterval().getSemitones() - p_other.getInterval().getSemitones())

	def distanceFromNext(self, p_other):
		result = self.getInterval().getSemitones() - p_other.getInterval().getSemitones()
		while (result > 0):
			result -= 12
		return abs(result)

	def buildChord(self, p_num_notes = 4, p_leap_size = 2):
		parent_degrees = self.getParentScale().getDegrees() * 3
		chord_degrees = []
		i = parent_degrees.index(self)
		end = i + (p_leap_size * p_num_notes)
		while (i < end):
			chord_degrees.append(parent_degrees[i])
			i = i + p_leap_size
		child_chord = Chord(chord_degrees)
		child_chord.setParentDegree(self)
		return child_chord

	def buildScale(self):
		child_intervals = self.buildPitchClass()
		child_scale = Scale(self.getNote(), child_intervals)
		child_scale.setParentDegree(self)
		return child_scale

	def buildPitchClass(self):
		parent_degrees = self.getParentScale().getDegrees() * 2
		child_intervals = [P1]
		i = parent_degrees.index(self) + 1
		while (parent_degrees[i] != self):
			child_intervals.append(Intervals[self.distanceFromNext(parent_degrees[i])])
			i = i + 1
		return child_intervals

	def buildScaleWithIntervals(self, p_intervals):
		new_scale = Scale(self.getNote(), p_intervals)
		new_scale.setParentDegree(self)
		return new_scale

	def getPosition(self):
		return self.getParentScale().getDegrees().index(self) + 1
	
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