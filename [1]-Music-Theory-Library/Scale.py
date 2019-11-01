from Interval import Interval
from Degree import _Degree

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
		
		self.setParentDegree = None
	def __str__(self):
		result = "[ "
		for degree in self.getDegrees():
			result = result + degree.__str__() + " "
		return result + "]"
	def __eq__(self, p_other):
		return (self.getIntervals() == p_other.getIntervals()) and (self.getTonicNote() == p_other.getTonicNote())
	def __getitem__(self, p_index):
		return self.getDegrees()[p_index - 1]
	
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