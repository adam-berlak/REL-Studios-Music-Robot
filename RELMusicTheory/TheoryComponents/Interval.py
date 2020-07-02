import re

class Interval:

	unaltered_intervals = []
	accidentals = []

	def __init__(self, p_semitones, p_numeral):
		self.semitones = p_semitones
		self.numeral = p_numeral

	def __str__(self): 
		prefix = ""
		if (self.getNumeral() < 0): prefix = "-"
		return prefix + abs(self).getAccidental() + str(abs(self).getNumeral())

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
		return (self.getNumeral() > p_other.getNumeral())

	def __lt__(self, p_other): 
		return (self.getNumeral() < p_other.getNumeral())

	def __ge__(self, p_other): 
		return (self > p_other) or (self.getNumeral() == p_other.getNumeral())

	def __le__(self, p_other): 
		return (self < p_other) or (self.getNumeral() == p_other.getNumeral())

	##############
	# Arithmetic #
	##############

	def __abs__(self):
		return Interval(abs(self.getSemitones()), abs(self.getNumeral()))

	def __neg__(self):
		return Interval(-self.getSemitones(), -self.getNumeral())

	def __add__(self, p_other):
		if (isinstance(p_other, Interval)): 
			if (p_other < Interval(0, 0)): return self - abs(p_other)
			elif (self < Interval(0, 0)): return p_other - abs(self)
			else: return Interval(self.getSemitones() + p_other.getSemitones(), self.getNumeral() + p_other.getNumeral() - 1)

		if (isinstance(p_other, int)): 
			if (p_other == 1): return self
			return self.next().__add__(p_other - 1)

		if (isinstance(p_other, str)): 
			return str(self) + p_other

	def __radd__(self, p_other):
		if (isinstance(p_other, str)): 
			return p_other + str(self)

	def __sub__(self, p_other):
		if (isinstance(p_other, Interval)): 
			if (p_other < Interval(0, 0)): return self + abs(p_other)
			elif (self > Interval(0, 0) and p_other > self): return Interval(self.getSemitones() - p_other.getSemitones(), self.getNumeral() - (p_other.getNumeral() + 1))
			else: return Interval(self.getSemitones() - p_other.getSemitones(), (self.getNumeral() + 1) - p_other.getNumeral())

	def __mul__(self, p_other):
		if (isinstance(p_other, int)): 
			return Interval(self.getSemitones() * p_other, ((self.getNumeral() * p_other) - (1 * (p_other - 1))))

	##########################
	# Representation Methods #
	##########################

	def getAccidental(self):

		try:
			accidental = self.getAccidentalAsSemitones()
			if (accidental < 0): return Interval.accidentals[-1] * abs(accidental)
			elif (accidental > 0): return Interval.accidentals[1] * abs(accidental)
			else: return Interval.accidentals[0]

		except: print("Error: Failed to print accidental")

	def getAccidentalAsSemitones(self):
		default_semitones = Interval.multiplySemitoneList(Interval.unaltered_intervals, 20)[self.getNumeral() - 1]
		return (self.getSemitones() - default_semitones)

	##########################
	# Transformation Methods #
	##########################

	@staticmethod
	def stringToAccidental(p_accidental):
		return list(Interval.accidentals.keys())[list(Interval.accidentals.values()).index(p_accidental)]

	def transform(self, p_accidental):
		if isinstance(p_accidental, str): 
			new_semitones = self.getSemitones() + Interval.stringToAccidental(p_accidental)
			return Interval(new_semitones, self.getNumeral())

		elif isinstance(p_accidental, int): 
			return Interval(self.getSemitones() + p_accidental, self.getNumeral())

	##################
	# STATIC Methods #
	##################

	@staticmethod
	def stringToInterval(p_string):

		try:
			intervals = Interval.multiplySemitoneList(Interval.unaltered_intervals, 20)
			numeral = int(re.findall(r'\d+', p_string)[0])
			regex = "[" + str([item for item in Interval.accidentals.values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1] + "]"
			accidentals = re.findall(re.compile(regex), p_string)
			semitones = intervals[numeral - 1]

			if (len(accidentals) != 0):
				accidental = accidentals[0]
				semitones = semitones + list(Interval.accidentals.keys())[list(Interval.accidentals.values()).index(accidental)]

			return Interval(semitones, numeral)
		
		except: print("Error: Failed to convert string: " + p_string + "to an Interval")

	@staticmethod
	def getPossibleIntervals(p_semitones):
		previous_list = Interval.generateIntervalList(Interval.unaltered_intervals)
		octaves = 1

		while(len(previous_list) <= p_semitones):
			temp_list = previous_list[:]
			for intervals in previous_list[:12]: temp_list.append([item + (Interval(12, 8) * octaves) for item in intervals])
			previous_list = temp_list[:]
			octaves += 1

		return previous_list[p_semitones]

	@staticmethod
	def generateIntervalList(p_unaltered_intervals):

		try: 
			result = []
			degree_count = 1

			for i in range(max(p_unaltered_intervals) + 1):
				if i not in p_unaltered_intervals: result.append([Interval(i, degree_count - 1), Interval(i, degree_count)])
				else:
					result.append([Interval(i, degree_count)])
					degree_count = degree_count + 1

			return result

		except: print("Error: Failed to generate interval list")

	@staticmethod
	def multiplySemitoneList(p_semitone_list, p_multiplier):

		try:
			result = p_semitone_list[:]

			for i in range(1, p_multiplier):

				for semitones in p_semitone_list:
					new_semitones = semitones + (12 * i)
					result.append(new_semitones)

			return result
		
		except: print("Error: Failed to mulitply semitone list")

	@staticmethod
	def multiplyPitchClass(p_pitch_class, p_multiplier):

		try:
			result = p_pitch_class

			for i in range(1, p_multiplier):

				for interval in p_pitch_class:
					new_interval = Interval(interval.getSemitones() + (12 * i), interval.getNumeral() + (7 * i))
					result.append(new_interval)

			return result

		except: print("Error: Failed to mulitply pitch class")

	#################
	# Sugar Methods #
	#################

	def getOctaveRange(self): 
		if self < Interval(0, 0): return -int(abs(self.getSemitones()) / 12) - 1
		return int(self.getSemitones() / 12)

	def getIdenticalIntervals(self): 
		return Interval.getPossibleIntervals(self.getSemitones())
	
	def roof(self): 
		if (self < Interval(0, 0)): return -abs(self).floor()
		return self + (Interval(12, 8) - self.simplify())

	def floor(self): 
		if (self < Interval(0, 0)): return -abs(self).roof()
		return self - (self.simplify())

	def simplify(self): 
		return Interval(Interval.getSimpleSemitones(self.getSemitones()), Interval.getSimpleNumeral(self.getNumeral()))

	def next(self):
		if (self.getNumeral() == len(Interval.unaltered_intervals)): 
			new_interval = Interval(Interval.unaltered_intervals[0] + self.getAccidentalAsSemitones(), 1)
			shift = Interval(12, 8) * (self.getOctaveRange() + 1)
		else:
			new_interval = Interval(Interval.unaltered_intervals[(self.simplify().getNumeral() - 1) + 1] + self.getAccidentalAsSemitones(), self.simplify().getNumeral() + 1)
			shift = Interval(12, 8) * self.getOctaveRange()

		return new_interval + shift

	@staticmethod
	def getSimpleNumeral(p_numeral):
		while (p_numeral > 7): p_numeral -= 7
		while (p_numeral < 1): p_numeral += 7
		return p_numeral

	@staticmethod
	def getSimpleSemitones(p_semitones):
		while (p_semitones > 11): p_semitones -= 12
		while (p_semitones < 0): p_semitones += 12
		return p_semitones

	#######################
	# Getters and Setters #
	#######################
		
	def setSemitones(self, p_semitones): self.semitones = p_semitones
	def setNumeral(self, p_numeral): self.numeral = p_numeral
		
	def getSemitones(self): return self.semitones
	def getNumeral(self): return self.numeral