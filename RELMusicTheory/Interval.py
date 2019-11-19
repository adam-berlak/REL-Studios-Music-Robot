Unaltered_Intervals = {
	"western": [0, 2, 4, 5, 7, 9, 11]
}

# Class Name: Interval
# Parameters: p_semitones (Number of Semitones in interval), p_numeral (numeral representation), p_accidental (sharp/flat)

class Interval:
	def __init__(self, p_semitones, p_numeral):
		self.semitones = p_semitones
		self.numeral = p_numeral

	def __str__(self):
		return self.getAccidental() + str(self.getNumeral())

	##############
	# Comparison #
	##############

	def __eq__(self, p_other):
		return (self.getSemitones() == p_other.getSemitones() and self.getNumeral() == p_other.getNumeral())

	def __ne__(self, p_other):
		return not (self == p_other)

	def __gt__(self, p_other):
		return self.getSemitones() > p_other.getSemitones()

	def __lt__(self, p_other):
		return self.getSemitones() < p_other.getSemitones()

	def __ge__(self, p_other):
		return (self > p_other) or (self == p_other)

	def __le__(self, p_other):
		return (self < p_other) or (self == p_other)

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):

		if (isinstance(p_other, Interval)):
			return Interval(self.getSemitones() + p_other.getSemitones(), self.getNumeral() + p_other.getNumeral() - 1)

		if (isinstance(p_other, str)):
			return self.__str__() + p_other

	def __radd__(self, p_other):
		if (isinstance(p_other, str)):
			return p_other + self.__str__()

	def __sub__(self, p_other):
		if (isinstance(p_other, Interval)):
			return Interval(self.getSemitones() - p_other.getSemitones(), (self.getNumeral() + 1) - p_other.getNumeral())

	def __mul__(self, p_other):
		if (isinstance(p_other, int)):
			return Interval(self.getSemitones() * p_other, ((self.getNumeral() + 1) * p_other) - p_other)

	##################
	# Helper Methods #
	##################

	def generateIntervalList(self, p_unaltered_intervals):
		result = []
		degree_count = 1

		for i in range(max(p_unaltered_intervals["western"] + 1)):
			if i not in p_unaltered_intervals:
				result.append((Interval(i, degree_count - 1), Interval(i, degree_count)))
			else:
				result.append((Interval(i, degree_count),))
				degree_count = degree_count + 1

		return result

	def getIdenticalIntervals(self):
		return self.generateIntervalList()[self.getMinSemitones()]

	def getAccidental(self):
		default_semitones = Unaltered_Intervals["western"][self.getMinNumeral() - 1]

		if (self.getMinSemitones() < default_semitones):
			return "b"
		elif (self.getMinSemitones() > default_semitones):
			return "#"

		return ""

	def getMinNumeral(self):
		numeral = self.getNumeral()
		while (numeral > 7):
			numeral -= 7

		return numeral

	def getMinSemitones(self):
		semitones = self.getSemitones()
		while (semitones > 7):
			semitones -= 12

		return semitones

	#######################
	# Getters and Setters #
	#######################
		
	def setSemitones(self, p_semitones):
		self.semitones = p_semitones
	def setNumeral(self, p_numeral):
		self.numeral = p_numeral
		
	def getSemitones(self):
		return self.semitones
	def getNumeral(self):
		return self.numeral