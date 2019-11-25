from Scale import *

class Chord(Scale):
	def __init__(self, p_tone, p_pitch_class):
		super().__init__(p_tone, p_pitch_class)
		self.parent_chord = p_pitch_class

	#####################################
	# Methods concerning class behavior #
	#####################################

	def __getitem__(self, p_other):
		
		if (isinstance(p_other, slice)):
			new_interval_list = self[p_other.start].buildPitchClass()
			new_chord = self.findDegreeInParent(self[p_other.start]).buildWithIntervals(Chord, new_interval_list[:-(len(new_interval_list) - (p_other.stop - 1))])
			return new_chord
		else:
			return self.getDegrees()[p_other - 1]

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):

		if (isinstance(p_other, str)):
			return str(self) + p_other

		if (isinstance(p_other, int)):
			return self.getParentDegree().__add__(p_other).build(Chord)

	def __radd__(self, p_other):

		if (isinstance(p_other, str)):
			return p_other + str(self)

		if (isinstance(p_other, int)):
			return self.getParentDegree().__add__(p_other).build(Chord)

	def __sub__(self, p_other):

		if (isinstance(p_other, int)):
			return self.getParentDegree().__sub__(p_other).build(Chord)
		
	######################################################
	# Methods concerning string representaton of a chord #
	######################################################

	def printQuality(self, p_system = DEFAULT_SYSTEM, style = 2):
		try: 
			chord_intervals = Chord.rearrangeIntervalsAsThirds(self.getIntervals())

			# Counters
			smallest_difference = 1000
			accidentals = ""

			# Loop through all known chord qualities
			for key in Chord_Qualities[p_system].keys():

				# Counters
				temp_accidentals = ""
				count = 0
				i = 0

				# Loop through all the chord intervals
				while(i < len(chord_intervals)):

					# Check if chord interval is not None object
					if (chord_intervals[i]):

						# Check if interval does not match with interval in dictionary
						if (chord_intervals[i] != Chord_Qualities[p_system][key][i]):
							count = count + 1

							# Add a flat if the interval of the parent chord is smaller than the dictionary interval
							if (chord_intervals[i] < Chord_Qualities[p_system][key][i]):
								temp_accidentals = temp_accidentals + "b" + str(((i + 1) * 2) - 1)

							# Otherwise add a sharp
							else:
								temp_accidentals = temp_accidentals + "#" + str(((i + 1) * 2) - 1)
					else:
						temp_accidentals = temp_accidentals + "(omit" + str(((i + 1) * 2) - 1) + ")"

					i = i + 1

				# Check if the current match is the closest to the parent chords pitch class
				if (count < smallest_difference):
					closest_match = key
					smallest_difference = count
					accidentals = temp_accidentals

			return closest_match[style] + str(max([x.getNumeral() for x in chord_intervals if x])) + accidentals

		except: 
			print("Error: Failed to create string represention of the chord")

	def printNumeral(self, p_system = DEFAULT_SYSTEM):
		numeral = intToRoman(self.getParentDegree().getInterval().getNumeral())

		if (self[1:3].printQuality(p_system, 0) == "minor3"):
			numeral = numeral.lower()

		accidental = self.getParentDegree().getInterval().getAccidental()

		secondary_information = ""
		if (self.getParentDegree().getParentScale().getParentDegree() != None):
			secondary_information = self.getParentDegree().getParentScale().getParentDegree().build(Chord).printNumeral() + "/"

		return  secondary_information + accidental + numeral

	def jazzNumeralNotation(self, p_system = DEFAULT_SYSTEM):
		return self.printNumeral(p_system) + self.printQuality(p_system) 

	'''
	def invert(self, p_inversion_number):
		result = []

		for degree in self.getDegrees():
			result.append(degree.getInterval())

		for i in range(p_inversion_number):
			result = result[1:].append(result[0] + P8 * (result[-1].getOctaveRange() + 1))
	'''

	##################
	# Static Methods #
	##################

	@staticmethod
	def rearrangeIntervalsAsThirds(p_pitch_class, p_system = DEFAULT_SYSTEM):
		try: 
			new_interval_list = []

			# Loop through all degrees in the chord
			for interval in p_pitch_class:
				possible_intervals = []

				# If the interval cannot be built on a sequence of thirds and it is less than 12 semitones large add 12
				if (((interval.getNumeral() - 1) % 2) != 0 and interval < P8):
					new_interval = interval + P8

				# If the interval cannot be built on a sequence of thirds and it is greater than 12 semitones large subtract 12
				elif ((interval.getNumeral() - 1) % 2 != 0 and interval > P8):
					new_interval = interval

					# subtract 12 until interval semitones is below 12
					while (new_interval > P8):
						new_interval -= P8
				else:
					new_interval = interval

				new_interval_list.append(new_interval)

			# Sort the new interval list by number of semitones in the intervals
			new_interval_list.sort(key=lambda x: x.getSemitones())

			# Counters
			previous_numeral = -1
			i = 0

			# Loop through the new interval list
			while (i < len(new_interval_list)):

				# If the previous degrees of the chard is missing place Nones in their position
				if (new_interval_list[i].getNumeral() - previous_numeral != 2):
					difference = new_interval_list[i].getNumeral() - previous_numeral

					# for all missing degrees do the following
					for j in range(int((difference - 2)/2)):
						new_interval_list.insert(i, None)
						i = i + 1

				previous_numeral = new_interval_list[i].getNumeral()
				i = i + 1

			return new_interval_list
		
		except:
			print("Error: Failed to rearrange intervals of parent chord as thirds")

	@staticmethod
	def stringToPitchClass(p_root_tone, p_quality, p_system = DEFAULT_SYSTEM):
		altered_intervals = re.findall(r'[b,#]\d+', p_quality)
		quality = re.search('(^[a-zA-Z]+)\d', p_quality).group(1)
		chord_size = re.search('^[a-zA-Z]+(\d).*', p_quality).group(1)

		for quality_tuple in Chord_Qualities[p_system].keys():

			if quality in quality_tuple:
				pitch_class = Chord_Qualities[p_system][quality_tuple][:]

		for altered_interval in altered_intervals:
			accidental = altered_interval[0]
			number = re.findall(r'\d+', altered_interval)[0]

			altered_interval = [item for item in pitch_class if item.getNumeral() == int(number)][0]
			pitch_class[pitch_class.index(altered_interval)] = altered_interval.transform(accidental)

		return pitch_class

		@staticmethod
		def pitchClassToFiguredBass(p_pitch_class, p_slice):
			new_pitch_class = p_pitch_class.reverse()[:-1]
			return [item.getNumeral() for item in new_pitch_class][:p_slice]

	###########################################################
	# Methods concerning harmonic movement and transformation #
	###########################################################

	def addInterval(self, p_interval):
		new_pitch_class = self.getIntervals()[:]
		new_pitch_class.append(p_interval)
		new_pitch_class.sort(key=lambda x: x.getNumeral())
		new_chord = Chord(self.getTonic().getTone(), new_pitch_class)
		return new_chord

	def resolveChord(self, p_voice_leading_rules = circleOfFifths):
		return p_voice_leading_rules(self)

	def getRelativeChord(self):
		return self - 3

	def getSecondaryDominant(self):
		return self.getParentDegree().buildScaleWithIntervals(major)[5].build(Chord)

	#######################
	# Getters and Setters #
	#######################

	def getRoot(self):
		return self.getParentDegree()
	def getParentChord(self):
		return self.parent_chord
	def getLeapSize(self):
		return self.leap_size

	def setParentChord(self, p_parent_chord):
		self.parent_chord = p_parent_chord
	def setLeapSize(self, p_leap_size):
		self.leap_size = p_leap_size

	# TODO 
	# def transformChordTo(self, p_intervals):
	# def getParallelChord(self):