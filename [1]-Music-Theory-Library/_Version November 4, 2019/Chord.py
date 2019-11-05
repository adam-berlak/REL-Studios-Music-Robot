from Scale import *
from Constants import *

def intToRoman(num):
	val = [
		1000, 900, 500, 400,
		100, 90, 50, 40,
		10, 9, 5, 4,
		1
		]
	syb = [
		"M", "CM", "D", "CD",
		"C", "XC", "L", "XL",
		"X", "IX", "V", "IV",
		"I"
		]
	roman_num = ''
	i = 0
	while  num > 0:
		for _ in range(num // val[i]):
			roman_num += syb[i]
			num -= val[i]
		i += 1
	return roman_num

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
		result = "["
		for degree in self.getDegrees():
			result = result + degree.__str__() + ", "
		return result[:-2] + "]"
		
	def __getitem__(self, p_other):
		if (isinstance(p_other, slice)):
			new_chord = Chord(self.getDegrees()[p_other.start - 1:p_other.stop])
			new_chord.setParentDegree(new_chord.getDegrees()[0])
			return new_chord
		else:
			return self.getDegrees()[p_other - 1]
		
	def resolveChord(self, p_voice_leading_rules = circleOfFifths):
		return p_voice_leading_rules(self)

	def getRelativeChord(self):
		return self - 2

	def getSecondaryDominant(self):
		return self.getParentDegree().buildScaleWithIntervals(major)[5].buildChord()

	def printQuality(self, system = "western", style = 2):
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
	# def transformChordTo(self, p_intervals):
	# def getParallelChord(self):

	def printNumeral(self, system = "western"):
		numeral = intToRoman(self.getParentDegree().getPosition())
		if (self[1:3].printQuality(system, 0) == "minor"):
			numeral = position.lower()
		accidental = self.getParentDegree().getInterval().getAccidental()
		return  accidental + numeral

	def jazzNumeralNotation(self, system = "western"):
		return self.printNumeral() + self.printQuality() 

	def getDegrees(self):
		return self.degrees
	def getParentDegree(self):
		return self.parent_degree
	def getIntervals(self):
		chord = self.getParentDegree().buildScale()[1].buildChord(len(self.getDegrees()))
		intervals = []
		padding = 0
		previous = chord.getDegrees()[0].getInterval().getSemitones()
		for degree in chord.getDegrees():
			if (degree.getInterval().getSemitones() < previous):	
				padding = 12
			intervals.append(Intervals[chord.getParentDegree().distanceFromNext(degree) + padding])
			previous = degree.getInterval().getSemitones()
		return intervals

	def setDegrees(self, p_degrees):
		self.degrees = p_degrees
	def setParentDegree(self, p_parent_degree):
		self.parent_degree = p_parent_degree