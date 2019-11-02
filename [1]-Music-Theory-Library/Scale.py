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

		for degree in self.getDegrees():
			note = (TONES.get(System)*2)[TONES.get(System).index(self.getTonicNote()) + degree.distanceFromClosest(self.getDegree(1))]
			degree.setNote(note)
	def __str__(self):
		result = "[ "
		for degree in self.getDegrees():
			result = result + degree.__str__() + " "
		return result + "]"
	def __eq__(self, p_other):
		return (self.getIntervals() == p_other.getIntervals()) and (self.getTonicNote() == p_other.getTonicNote())
	def __getitem__(self, p_index):
		return self.getDegrees()[p_index - 1]
	def __add__(self, p_other):
		if (isinstance(p_other, int)):
			return Scale(TONES.get("western")[TONES.get("western").index(self.getTonicNote()) + p_other], self.getIntervals())
		if (isinstance(p_other, str)):
			return str(self) + p_other
	def __radd__(self, p_other):
		if (isinstance(p_other, str)):
			return p_other + str(self)
	
	def getDegree(self, p_index):
		return self.getDegrees()[p_index - 1]		
	def getDegreeByInterval(self, p_interval):
		for degree in self.getDegrees():
			if (degree.getInterval() == p_interval):
				return degree
			return None
   
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
		parent_degrees = self.getParentScale().getDegrees() * 2
		child_intervals = [P1]
		i = parent_degrees.index(self) + 1
		while (parent_degrees[i] != self):
			child_intervals.append(Intervals[self.distanceFromNext(parent_degrees[i])])
			i = i + 1
		child_scale = Scale(self.getNote(), child_intervals)
		child_scale.setParentDegree(self)
		return child_scale
	def buildScaleWithIntervals(self, p_intervals):
		new_scale = Scale(self.getNote(), p_intervals)
		new_scale.setParentDegree(self)
		return new_scale
	
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