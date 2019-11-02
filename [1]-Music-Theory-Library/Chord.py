from Scale import *
from Constants import *

class Chord:
	def __init__(self, p_degrees):
		self.degrees = p_degrees
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
	def __str__(self):
		result = "[ "
		for degree in self.getDegrees():
			result = result + degree.__str__() + " "
		return result + "]"
		
	def resolveChord(self, p_voice_leading_rules = circleOfFifths):
		return p_voice_leading_rules(self)
	def getRelativeChord(self):
		return self - 2
	def getSecondaryDominant(self):
		return self.getParentDegree().buildScaleWithIntervals(major)[5].buildChord()
	# def transformChordTo(self, p_intervals):
	# def getParallelChord(self):

	def getDegrees(self):
		return self.degrees
	def getParentDegree(self):
		return self.parent_degree

	def setDegrees(self, p_degrees):
		self.degrees = p_degrees
	def setParentDegree(self, p_parent_degree):
		self.parent_degree = p_parent_degree