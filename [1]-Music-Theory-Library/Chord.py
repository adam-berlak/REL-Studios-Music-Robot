from Degree import _Degree
from Scale import Scale

def circleOfFifths(p_chord):
	return p_chord + 5
def circleOfFourths(p_chord):
	return p_chord + 4

class Chord:
	def __init__(self, p_intervals):
		self.intervals = p_intervals
	def __add__(self, p_other):
		return self.getParentDegree().__add__(p_other).buildChord()
		
	def resolveChord(self, p_voice_leading_rules = circleOfFifths):
		return p_voice_leading_rules(self)
	def getRelativeChord(self):
		return self - 2
	# def transformChordTo(self, p_intervals):
	# def getParallelChord(self):

	def getIntervals(self):
		return self.intervals
	def getParentDegree(self):
		return self.parent_degree

	def setIntervals(self, p_intervals):
		self.intervals = p_intervals
	def setParentDegree(self, p_degree):
		self.parent_degree = p_parent_degree