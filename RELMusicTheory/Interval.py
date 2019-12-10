import re

# Class Name: Interval
# Parameters: p_semitones (Number of Semitones in interval), p_numeral (numeral representation), p_accidental (sharp/flat)

class Interval:

	unaltered_intervals = []
	accidentals = []

	def __init__(self, p_semitones, p_numeral):
		self.semitones = p_semitones
		self.numeral = p_numeral

	def __str__(self):
		return self.getAccidental() + str(self.getNumeral())

	def __repr__(self):
		return str(self)

	def __hash__(self):
		return hash((self.semitones, self.numeral))

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

	def simplify(self):
		return Interval(self.getSimpleSemitones(), self.getSimpleNumeral())

	def getSimpleNumeral(self):
		numeral = self.getNumeral()
		while (numeral > 7):
			numeral -= 7

		return numeral

	def getSimpleSemitones(self):
		semitones = self.getSemitones()
		while (semitones > 11):
			semitones -= 12

		return semitones

	##########################
	# Representation Methods #
	##########################

	def getAccidental(self):
		default_semitones = Interval.multiplySemitoneList(Interval.unaltered_intervals, 20)[self.getNumeral() - 1]
		accidental = (self.getSemitones() - default_semitones)

		if (accidental < 0):
			return Interval.accidentals[-1] * abs(accidental)
		elif (accidental > 0):
			return Interval.accidentals[1] * abs(accidental)
		else:
			return Interval.accidentals[0]

	##########################
	# Transformation Methods #
	##########################

	def transform(self, p_accidental):

		try:
			new_semitones = self.getSemitones() + list(Interval.accidentals.keys())[list(Interval.accidentals.values()).index(p_accidental)]
			new_numeral = self.getNumeral()

			return Interval(new_semitones, new_numeral)
			
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
		regex = "[" + str([item for item in Interval.accidentals.values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1] + "]"
		accidentals = re.findall(re.compile(regex), p_string)
		semitones = intervals[numeral - 1]

		if (len(accidentals) != 0):
			accidental = accidentals[0]
			semitones = semitones + list(Interval.accidentals.keys())[list(Interval.accidentals.values()).index(accidental)]

		return Interval(semitones, numeral)

	@staticmethod
	def generateIntervalList(p_unaltered_intervals):
		result = []
		degree_count = 1

		for i in range(max(p_unaltered_intervals) + 1):
			if i not in p_unaltered_intervals:
				result.append((Interval(i, degree_count - 1), Interval(i, degree_count)))
			else:
				result.append((Interval(i, degree_count),))
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

	#################
	# Sugar Methods #
	#################

	def getIdenticalIntervals(self):
		return Interval.generateIntervalList(Interval.unaltered_intervals)[self.getSimpleSemitones()]

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