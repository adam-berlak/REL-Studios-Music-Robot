import re

# Class Name: Interval
# Parameters: p_semitones (Number of Semitones in interval), p_numeral (numeral representation), p_accidental (sharp/flat)

class Interval:

	unaltered_intervals = [0, 2, 4, 5, 7, 9, 11]

	accidentals = {"b": -1, "bb": -2, "#": 1, "##": 2}

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

	###########################
	# Properties of Intervals #
	###########################

	def getOctaveRange(self):
		return int(self.getSemitones() / 12)

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

	##########################
	# Representation Methods #
	##########################

	def getAccidental(self):
		default_semitones = Interval.unaltered_intervals[self.getMinNumeral() - 1]

		for key in Interval.accidentals.keys():
			if (Interval.accidentals[key] == (self.getMinSemitones() - default_semitones)):
				return key

		return ""

	##########################
	# Transformation Methods #
	##########################

	def transform(self, p_accidental):

		try:
			new_semitones = self.getSemitones() + Interval.accidentals[p_accidental]
			interval_list = Interval.generateIntervalList(Interval.multiplySemitoneList(Interval.unaltered_intervals, 20))
			interval = [item for item in interval_list[new_semitones] if self.getNumeral() == item.getNumeral()][0]

			return interval
			
		except:
			print("Error: Trying to apply " + p_accidental + " to " + str(self) + "")

			return self

	##################
	# STATIC Methods #
	##################

	@staticmethod
	def stringToInterval(p_string):
		intervals = Interval.multiplySemitoneList(Interval.unaltered_intervals, 20)
		numeral = int(re.findall(r'\d+', p_string)[0])
		accidentals = re.findall(r'[#,b]', p_string)
		semitones = intervals[numeral - 1]

		if (len(accidentals) != 0):
			accidental = accidentals[0]
			semitones = semitones + Interval.accidentals[accidental]

		return Interval(semitones, numeral)

	@staticmethod
	def generateIntervalList(p_unaltered_intervals):
		result = []
		degree_count = 1

		for i in range(max(p_unaltered_intervals) + 1):
			if i not in p_unaltered_intervals:
				result.append((Interval(i, degree_count - 1), Interval(i, degree_count)))
			else:
				result.append((Interval(i, degree_count), ""))
				degree_count = degree_count + 1

		return result

	@staticmethod
	def multiplySemitoneList(p_semitone_list, p_multiplier):
		result = p_semitone_list[:]

		for i in range(1, p_multiplier):

			for semitones in p_semitone_list:
				new_semitones = semitones + (12 * i)
				result.append(new_semitones)

		return result

	@staticmethod
	def multiplyPitchClass(p_pitch_class, p_multiplier):
		result = p_pitch_class

		for i in range(1, p_multiplier):

			for interval in p_pitch_class:
				new_interval = Interval(interval.getSemitones() + (12 * i), interval.getNumeral() + (7 * i))
				result.append(new_interval)

		return result

	####################
	# Courtesy Methods #
	####################

	def getIdenticalIntervals(self):
		return Interval.generateIntervalList(Interval.unaltered_intervals)[self.getMinSemitones()]

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