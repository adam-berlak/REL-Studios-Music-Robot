from Interval import Interval
from Scale import Scale
from Chord import Chord

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
		return (self.getParentScale().getDegrees()*2)[self.getParentScale().getDegrees().index(self) + p_other]

	def distanceFromClosest(self, p_other):
		return abs(self.getInterval().getSemitones() - p_other.getInterval().getSemitones())
	def distanceFromNext(self, p_other):
		result = self.getInterval().getSemitones() - p_other.getInterval().getSemitones()
		while (result > 0):
			result -= 12
		return abs(result)

	def buildChord(self, p_num_notes = 4, p_leap_size = 2):
		parent_degrees = self.getParentScale().getIntervals() * 3
		chord_intervals = [P1]
		i = parent_degrees.index(self) + p_leap_size
		while (i < 24):
			chord_intervals.append(Intervals[self.distanceFromNext(parent_degrees[i])])
			i = i + p_leap_size
		child_chord = Chord(chord_intervals)
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
		# child_scale.setParentDegree(self)
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