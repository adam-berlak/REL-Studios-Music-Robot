from Scale import *

class Chord(Scale):
	
	def __init__(self, p_tone, p_pitch_class):
		super().__init__(p_tone, p_pitch_class)
		self.parent_chord = self.rearrangeIntervalsAsThirds(p_pitch_class)

	#####################################
	# Methods concerning class behavior #
	#####################################

	def __getitem__(self, p_other):
		
		if (isinstance(p_other, slice)):
			new_interval_list = super(Chord._Degree, self[p_other.start]).buildPitchClass()
			new_chord = self[p_other.start].findInParent().buildWithIntervals(Chord, new_interval_list[:p_other.stop])

			return new_chord
		else:
			return self.getDegrees()[p_other - 1]

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):

		if (self.getParentDegree() != None):

			if (isinstance(p_other, Interval)):
				return (self.getParentDegree() + p_other).buildWithIntervals(Chord, self.getIntervals())

			if (isinstance(p_other, int)):
				return (self.getParentDegree() + p_other).buildWithGenericIntervals(Chord, self.getNumerals())

			if (isinstance(p_other, str)):
				return str(self) + p_other
		else:
			return super().__add__(p_other)

	def __radd__(self, p_other):

		if (isinstance(p_other, str)):
			return p_other + str(self)

	def __sub__(self, p_other):

		if (self.getParentDegree() != None):

			if (isinstance(p_other, Interval)):
				return (self.getParentDegree() - p_other).buildWithIntervals(Chord, self.getIntervals())

			if (isinstance(p_other, int)):
				return (self.getParentDegree() - p_other).buildWithGenericIntervals(Chord, self.getNumerals())
		else:
			return super().__sub__(p_other)
		
	######################################################
	# Methods concerning string representaton of a chord #
	######################################################

	def getParentChordQuality(self, style = 2, p_system = DEFAULT_SYSTEM):

		try: 
			# Arrange parent chord intervals as thirds
			chord_intervals = Chord.rearrangeIntervalsAsThirds(self.getIntervals())

			# Keep track of all possible bass triad names
			triad_qualities = []

			# Loop through all naming conventions for bass triads
			for key in CHORD_QUALITIES[p_system].keys():

				# If bass triad in dictionary matches bass triad in parent chord add its name to the list
				if (all(elem in chord_intervals[:2] for elem in CHORD_QUALITIES[p_system][key][:2]) or chord_intervals[1] == None):
					triad_qualities.append(key)

			# Retrieve extensions of parent chord
			extensions = chord_intervals[2:]
			smallest_difference = 1000
			accidentals = ""

			# Keep track of all possible extension names
			possible_extensions = []

			# Loop through all naming conventions for extensions
			for key in CHORD_QUALITIES[p_system].keys():

				# Counters
				temp_chord_quality_extensions = CHORD_QUALITIES[p_system][key][2:]
				temp_accidentals = ""
				count = 0
				i = 0

				# Loop through all the chord intervals
				while(i < len(extensions)):

					# Check if chord interval is not None object
					if (extensions[i]):

						# Check if interval does not match with interval in dictionary
						if (extensions[i] != temp_chord_quality_extensions[i]):
							count = count + 1

							# Add the extension to the list of accidentals if it is altered
							if (extensions[i] != temp_chord_quality_extensions[i]):
								temp_accidentals = temp_accidentals + extensions[i]

					# If chord interval is None object indicate that the chord is missing this interval
					else:
						temp_accidentals = temp_accidentals + OMISSION_NOTATION[p_system] + str((((2 + i) + 1) * 2) - 1)

					i = i + 1

				# Check if the current match is the closest to the parent chords pitch class
				if (count < smallest_difference):
					closest_match = key
					smallest_difference = count
					accidentals = temp_accidentals
					possible_extensions = []
					possible_extensions.append((key, temp_accidentals))

				elif (count == smallest_difference):
					possible_extensions.append((key, temp_accidentals))
			
			# Keep track of all valid names for the chord
			possible_qualities = []

			# Loop through all the possible naming conventions for the extensions of this chord
			for extensions_quality_and_accidentals in possible_extensions:

				# Loop through all the possible naming conventions for the bass triad of this chord
				for final_triad_quality in triad_qualities:
					final_extensions_quality = extensions_quality_and_accidentals[0]

					# If the bass triad and the extensions have the same quality null out the extensions quality for the final string
					if (final_triad_quality[0] == final_extensions_quality[0]):
						final_extensions_quality = ("", "", "")

						# Append the following to the possible names of the chord
						possible_qualities.append(final_triad_quality[style] + final_extensions_quality[style] + str(max([x.getNumeral() for x in chord_intervals if x])) + extensions_quality_and_accidentals[1])

					# If the bass triad and the extensions dont have the same quality the only valid extension qualities are Major and Minor (In order to prevent using Dominant or other extension qualities)
					elif (("major" in final_extensions_quality[0]) or ("minor" in final_extensions_quality[0])):

						# Append the following to the possible names of the chord
						possible_qualities.append(final_triad_quality[style] + final_extensions_quality[style] + str(max([x.getNumeral() for x in chord_intervals if x])) + extensions_quality_and_accidentals[1])
			
			# Return the shortest name
			return min(possible_qualities, key=len)

		except: 
			print("Error: Failed to create string represention of the chord")

	def getQuality(self, p_system = DEFAULT_SYSTEM):

		parent_chord_quality = self.getParentChordQuality()

		# Get quality of chord for bass triad and extensions
		regex = (("(" + str([item for representations in CHORD_QUALITIES[p_system] for item in representations]).replace('\'', "").replace(" ", "").replace(',', "|").replace('+', "\+")[1:][:-1] + ")") * 2) + "*(\d+)"
		quality_contents = re.search(re.compile(regex), parent_chord_quality)

		bass_triad_quality = quality_contents.group(1)
		extensions_quality = quality_contents.group(2)

		if (extensions_quality == None):
			extensions_quality = bass_triad_quality

		# Get actually highest numeral in Chord
		extensions_numeral = max([item.getNumeral() for item in self.getIntervals()])

		# RegEx no and altered intervals in parent chord quality and only include those below highest numeral
		modifications = []

		accidentals_regex = str([item for item in ACCIDENTALS[p_system].values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1]
		interval_regex = "[" + accidentals_regex + "]\d+"
		altered_intervals = re.findall(re.compile(interval_regex), parent_chord_quality)

		for altered_interval in altered_intervals:

			if (Interval.stringToInterval(altered_interval).getNumeral() <= int(extensions_numeral)):
				modifications.append((altered_interval, Interval.stringToInterval(altered_interval).getNumeral()))

		interval_regex_optional_accidental = "[" + accidentals_regex + "]*\d+"
		regex = OMISSION_NOTATION[p_system] + interval_regex_optional_accidental
		omitted_intervals = re.findall(re.compile(regex), parent_chord_quality)

		for omitted_interval in omitted_intervals:

			interval_string = re.findall(re.compile(interval_regex_optional_accidental), str(omitted_interval))[0]

			if (Interval.stringToInterval(interval_string).getNumeral() <= int(extensions_numeral)):
				modifications.append((omitted_interval, Interval.stringToInterval(interval_string).getNumeral()))

		# Loop through tones and if not a third make it a sus
		for interval in self.getIntervals():

			if (((interval.getNumeral() - 1) % 2) != 0):
				string_form = "sus" + str(interval)
				modifications.append((string_form, interval.getNumeral()))

		# Add all the alterations to the quality by order of numeral
		modifications = sorted(modifications, key=lambda x: x[1])

		modifications_string = ""

		for modification in modifications:
			modifications_string = modifications_string + modification[0]

		if (bass_triad_quality == extensions_quality):
			return bass_triad_quality + str(extensions_numeral) + modifications_string
		else:
			return bass_triad_quality + extensions_quality + str(extensions_numeral) + modifications_string

	def printNumeral(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):

		# Convert numeral integer into roman numeral
		numeral = intToRoman(self.getParentDegree().getInterval().getNumeral())

		# Check quality of triad built on this degree, and change numeral to lower if minor     
		if (self[1:2].getIntervals() == [P1, m3]):
			numeral = numeral.lower()

		# Obtain the accidental of the associated interval
		accidental = self.getParentDegree().getInterval().getAccidental()

		# If parent scale is based off a degree of another scale, print the following degree as a secondary chord
		secondary_information = ""

		if (p_with_quality == True):
			return accidental + numeral + self.getParentChordQuality(p_style, p_system)

		return accidental + numeral

	def printNumeralWithContext(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):

		# Check if chord is a Secondary Chord
		if (self.getParentScale().getParentDegree() != None):
			secondary_information = "\\" + self.getParentScale().getParentDegree().build(Chord).printNumeral()

		return self.printNumeral(p_with_quality, p_style, p_system) + secondary_information

	def getFiguredBass(self):
		return self.getFirstInversion().printNumeral(False) + Chord.pitchClassToFiguredBass(self.getIntervals())

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
	def stringToPitchClass(p_quality, p_system = DEFAULT_SYSTEM):

		# Search input string for the qualities and numeral
		regex = (("(" + str([item for representations in CHORD_QUALITIES[p_system] for item in representations]).replace('\'', "").replace(" ", "").replace(',', "|").replace('+', "\+")[1:][:-1] + ")") * 2) + "*(\d+)"
		quality_contents = re.search(re.compile(regex), p_quality)

		bass_triad_quality = quality_contents.group(1)
		extensions_quality = quality_contents.group(2)
		extensions_numeral = quality_contents.group(3)

		if (extensions_quality == None):
			extensions_quality = bass_triad_quality

		# Obtain accidental components via RegEx
		accidentals_regex = str([item for item in ACCIDENTALS[p_system].values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1]
		interval_regex = "[" + accidentals_regex + "]\d+"
		altered_intervals = re.findall(re.compile(interval_regex), p_quality)

		# Loop through each chord types names and find the matching type
		for quality_tuple in CHORD_QUALITIES[p_system].keys():

			if (bass_triad_quality != ""):

				# Copy types pitch class
				if bass_triad_quality in quality_tuple:
					bass_triad_pitch_class = CHORD_QUALITIES[p_system][quality_tuple][:]

			# Copy types pitch class
			if extensions_quality in quality_tuple:
				extensions_pitch_class = CHORD_QUALITIES[p_system][quality_tuple][:]

		# Return result with bass_triad_pitch class if it is defined
		if (bass_triad_pitch_class != ""):
			result = (bass_triad_pitch_class[:2] + extensions_pitch_class[2:])[:int((int(extensions_numeral) + 1) / 2)]
		else:
			result = extensions_pitch_class[:int((int(extensions_numeral) + 1) / 2)]

		# Loop through all altered intervals and apply them to the pitch class set
		for altered_interval in altered_intervals:
			accidental = altered_interval[0]
			number = re.findall(r'\d+', altered_interval)[0]
			match = [item for item in result if item.getNumeral() == int(number)]

			if (len(match) != 0):
				interval_to_be_altered = match[0]
				result[extensions_pitch_class.index(interval_to_be_altered)] = Interval.stringToInterval(str(altered_interval))

		# Obtain sus components via RegEx
		interval_regex_optional_accidental = "[" + accidentals_regex + "]*\d+"
		regex = SUSPENDED_NOTATION[p_system] + interval_regex_optional_accidental
		sus_intervals = re.findall(re.compile(regex), p_quality)
		list_of_sus_intervals = []

		# Create a list of suspended intervals
		for sus_interval in sus_intervals:
			interval = str(re.findall(re.compile(interval_regex_optional_accidental), str(sus_interval)))
			list_of_sus_intervals.append(Interval.stringToInterval(interval))

		result = result + list_of_sus_intervals
		result.sort(key=lambda x: x.getSemitones())

		# Obtain no components via RegEx
		regex = OMISSION_NOTATION[p_system] + interval_regex_optional_accidental
		omitted_intervals = re.findall(re.compile(regex), p_quality)

		# Remove every interval within omitted intervals from result
		for omitted_interval in omitted_intervals:
			interval_string = str(re.findall(re.compile(interval_regex_optional_accidental), str(omitted_interval)))
			interval = Interval.stringToInterval(interval_string)

			if (interval in result):
				result.pop(result.index(interval))

		return result

	@staticmethod
	def pitchClassToFiguredBass(p_pitch_class, p_slice = 2):
		new_pitch_class = p_pitch_class[::-1]

		string = ""

		for numeral in [item.getNumeral() for item in new_pitch_class][:p_slice]:
			string = string + str(numeral) + "/"

		return string[:-1]

	##########################
	# Transformation methods #
	##########################

	def transformChordTo(self, p_intervals):
		return self.getParentDegree().buildWithIntervals(Chord, p_intervals)

	def invert(self, p_inversion_number):
		new_chord = super(Chord._Degree, super(Chord, self).__getitem__(p_inversion_number)).build(Chord, len(self.getIntervals()), 2)
		new_chord.setParentDegree(super(type(self[1]), self[1]).__add__(p_inversion_number).findInParent())

		return new_chord

	def getFirstInversion(self):

		previous = self
		smallest_inversion = self
		min_none_count = len([item for item in Chord.rearrangeIntervalsAsThirds(self.getIntervals()) if item == None])

		for i in range(len(self.getIntervals())):
			temp_chord = previous.invert(2)
			intervals = Chord.rearrangeIntervalsAsThirds(temp_chord.getIntervals())
			temp_count = len([item for item in intervals if item == None])

			if (temp_count < min_none_count):
				smallest_inversion = temp_chord
				min_none_count = temp_count

			previous = temp_chord

		return smallest_inversion

	def getParallelChord(self, p_rotation = 6):

		try:
			if (self.getParentScale() != None):

				parallel_scale = self.getParentScale()[1].buildScaleWithIntervals((self.getParentScale() + p_rotation).getIntervals())
				parallel_chord = parallel_scale[self[1].getPositionInParent()].buildWithGenericIntervals(Chord, self.getNumerals())

				return parallel_chord
			else:
				print("Error: Unable to get parallel of Chord that does not have a Parent Scale")

		except:
			print("Error: Failed to get parallel Chord")

	def getRelativeChord(self, p_rotation = 6):

		try:
			if (self.getParentScale() != None):

				relative_scale = self.getParentScale() + p_rotation
				relative_chord = relative_scale[self[1].getPositionInParent()].buildWithGenericIntervals(Chord, self.getNumerals())

				return relative_chord

			else:
				print("Error: Unable to get relative of Chord that does not have a Parent Scale")

		except:
			print("Error: Failed to get relative Chord")

	def getSecondaryDominant(self):
		return (self.getParentDegree().buildScale()[1] + P5).buildWithIntervals(Chord, [P1, M3, P5, m7])

	def resolveChord(self, p_voice_leading_rules = circleOfFifths):
		return p_voice_leading_rules(self)

	#################
	# Sugar Methods #
	#################

	def next(self):
		return (self.getParentDegree().next()).buildWithGenericIntervals(Chord, self.getNumerals())

	def previous(self):
		return (self.getParentDegree().previous()).buildWithGenericIntervals(Chord, self.getNumerals())

	def getParentChord(self):
		new_interval_list = [item for item in Chord.rearrangeIntervalsAsThirds(self.getIntervals()) if item != None]

		return (self.getParentDegree().buildWithIntervals(Chord, new_interval_list))

	##################################
	# Overridden Methods and Classes #
	##################################

	def setParentDegree(self, p_degree):
		self.parent_degree = self.configureParentDegree(p_degree)

	def configureParentDegree(self, p_degree):
		result_scale = p_degree.getParentScale()

		for degree in self.getDegrees():
			interval_in_parent = (p_degree.getInterval() + degree.getInterval())

			if (interval_in_parent.getNumeral() > max([item.getNumeral() for item in result_scale.getIntervals()])):
				interval_in_parent = interval_in_parent.simplify()

			if (interval_in_parent not in result_scale and not result_scale.isDistinct()):
				result_scale = result_scale.addInterval(interval_in_parent)

			elif (interval_in_parent not in result_scale and result_scale.isDistinct()):
				result_scale = result_scale.replaceAtNumeralWith(interval_in_parent.getNumeral(), interval_in_parent)

		return result_scale.getDegreeByInterval(p_degree.getInterval())

	class _Degree(Scale._Degree):

		def build(self, object_type, p_num_tones = 4, p_leap_size = 3, *args):
			if (self.getParentScale().getParentDegree() != None):
				return self.findInParent().build(object_type, p_num_tones, p_leap_size, *args)
			else:
				return super().build(object_type, p_num_tones, p_leap_size, *args)

		def buildWithIntervals(self, object_type, p_pitch_class, *args):
			if (self.getParentScale().getParentDegree() != None):
				return self.findInParent().buildWithIntervals(object_type, p_pitch_class, *args)
			else:
				return super().buildWithIntervals(object_type, p_pitch_class, *args)

		def buildWithGenericIntervals(self, object_type, p_generic_intervals, *args):
			if (self.getParentScale().getParentDegree() != None):
				return self.findInParent().buildWithGenericIntervals(object_type, p_generic_intervals, *args)
			else:
				return super().buildWithGenericIntervals(object_type, p_generic_intervals, *args)

		def buildScale(self):
			if (self.getParentScale().getParentDegree() != None):
				return self.findInParent().buildScale()
			else:
				return super().buildScale()

		def buildScaleWithIntervals(self, p_intervals):
			if (self.getParentScale().getParentDegree() != None):
				return self.findInParent().buildScaleWithIntervals(p_intervals)
			else:
				return super().buildScaleWithIntervals(p_intervals)

		def buildPitchClass(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM):
			if (self.getParentScale().getParentDegree() != None):
				return self.findInParent().buildPitchClass(p_num_tones, p_leap_size, p_system)
			else:
				return super().buildPitchClass(p_num_tones, p_leap_size, p_system)

		def next(self):
			if (self.getParentScale().getParentDegree() != None):
				return self.findInParent().next()
			else:
				return super().next()

		def previous(self):
			if (self.getParentScale().getParentDegree() != None):
				return self.findInParent().previous()
			else:
				return super().previous()

		def transform(self, p_accidental, p_system = DEFAULT_SYSTEM):
			new_object = super().transform(p_accidental, p_system)
				
			if (self.getParentScale().getParentDegree() != None):
				new_parent = self.findInParent().transform(p_accidental, p_system)
				new_object.setParentDegree(new_parent.getDegreeByInterval(self.getParentScale().getParentDegree().getInterval()))

			return new_object