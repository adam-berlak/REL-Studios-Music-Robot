Unaltered_Intervals = {
	"western": [0, 2, 4, 5, 7, 9, 11]
}

accidentals = {
	"western": {
		"b": -1,
		"bb": -2,
		"#": +1, 
		"##": +2
	}
}

# Class Name: Interval
# Parameters: p_semitones (Number of Semitones in interval), p_numeral (numeral representation), p_accidental (sharp/flat)

class Interval:
	def __init__(self, p_semitones, p_numeral):
		self.semitones = p_semitones
		self.numeral = p_numeral

	def __str__(self):
		return self.getAccidental() + str(self.getNumeral())

	def __repr__(self):
		return str(self)

	##############
	# Comparison #
	##############

	def __eq__(self, p_other):
		return (type(self) == type(p_other)) and ((self.getSemitones() == p_other.getSemitones()) and (self.getNumeral() == p_other.getNumeral()))

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
			return str(self) + p_other

	def __radd__(self, p_other):
		if (isinstance(p_other, str)):
			return p_other + str(self)

	def __sub__(self, p_other):
		if (isinstance(p_other, Interval)):
			return Interval(self.getSemitones() - p_other.getSemitones(), (self.getNumeral() + 1) - p_other.getNumeral())

	def __mul__(self, p_other):
		if (isinstance(p_other, int)):
			return Interval(self.getSemitones() * p_other, ((self.getNumeral() + 1) * p_other) - p_other)

	##################
	# Helper Methods #
	##################

	def getOctaveRange(self):
		return int(self.getSemitones() / 12)

	def transform(self, p_accidental):

		try:
			new_semitones = self.getSemitones() + accidentals["western"][p_accidental]
			interval_list = self.generateIntervalList(self.multiplySemitoneList(Unaltered_Intervals["western"], 20))
			interval = [item for item in interval_list[new_semitones] if self.getNumeral() == item.getNumeral()][0]

			return interval
		except:
			print("Error: Trying to apply " + p_accidental + " to " + str(self) + "")

			return self

	def generateIntervalList(self, p_unaltered_intervals):
		result = []
		degree_count = 1

		for i in range(max(p_unaltered_intervals) + 1):
			if i not in p_unaltered_intervals:
				result.append((Interval(i, degree_count - 1), Interval(i, degree_count)))
			else:
				result.append((Interval(i, degree_count), ""))
				degree_count = degree_count + 1

		return result

	def multiplySemitoneList(self, p_semitone_list, p_multiplier):
		result = p_semitone_list[:]
		for i in range(1, p_multiplier):
			for semitones in p_semitone_list:
				new_semitones = semitones + (12 * i)
				result.append(new_semitones)

		return result

	def multiplyPitchClass(self, p_pitch_class, p_multiplier):
		result = p_pitch_class
		for i in range(1, p_multiplier):
			for interval in p_pitch_class:
				new_interval = Interval(interval.getSemitones() + (12 * i), interval.getNumeral() + (7 * i))
				result.append(new_interval)

		return result

	def getIdenticalIntervals(self):
		return self.generateIntervalList(Unaltered_Intervals["western"])[self.getMinSemitones()]

	def getAccidental(self):
		default_semitones = Unaltered_Intervals["western"][self.getMinNumeral() - 1]

		if (self.getMinSemitones() < default_semitones):
			return "b"
		elif (self.getMinSemitones() > default_semitones):
			return "#"

		return ""

	def minimize(self):
		return Interval(self.getMinSemitones(), self.getMinNumeral())

	def getMinNumeral(self):
		numeral = self.getNumeral()
		while (numeral > 7):
			numeral -= 7

		return numeral

	def getMinSemitones(self):
		semitones = self.getSemitones()
		while (semitones > 11):
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