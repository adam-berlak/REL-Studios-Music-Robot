import itertools

from Scale import *

class Chord(Scale):
	
	def __init__(self, p_tone, p_item = -1): 

		if (isinstance(p_tone, Scale)):
			scale = p_tone
			p_tone = scale.getTonicTone()
			p_item = scale.getIntervals()

		elif (isinstance(p_item, str)): p_item = Chord.stringToPitchClass(p_item)

		super().__init__(p_tone, p_item)

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):

		if (self.getParentDegree() != None and (isinstance(p_other, int) or isinstance(p_other, Interval))):
			if (isinstance(p_other, Interval)): return (self.getParentDegree() + p_other).build(Chord, self.getIntervals())
			if (isinstance(p_other, int)): return (self.getParentDegree() + p_other).build(Chord, self.getNumerals())

		else: return super().__add__(p_other)

	def __sub__(self, p_other):

		if (self.getParentDegree() != None and (isinstance(p_other, int) or isinstance(p_other, Interval))):
			if (isinstance(p_other, Interval)): return (self.getParentDegree() - p_other).build(Chord, self.getIntervals())
			if (isinstance(p_other, int)): return (self.getParentDegree() - p_other).build(Chord, self.getNumerals())
			
		else: return super().__sub__(p_other)
	
	def __radd__(self, p_other):
		if (isinstance(p_other, str)): return p_other + str(self)
		
	################################
	# Methods concerned with names #
	################################

	def getParentChordQuality(self, p_style = 2, p_system = DEFAULT_SYSTEM):

		try: 
			chord_intervals = Chord.rearrangeIntervalsAsThirds(self.getIntervals())
			triad_qualities = Chord.getPossibleQualitiesOfSlice(chord_intervals, 0, 3, p_system)
			extension_qualities = Chord.getPossibleQualitiesOfSlice(chord_intervals, 3, len(chord_intervals), p_system)
			possible_qualities = []

			for extensions_quality_and_accidentals in extension_qualities:

				for triad_quality_and_accidentals in triad_qualities:
					final_triad_quality = triad_quality_and_accidentals[0]
					final_extensions_quality = extensions_quality_and_accidentals[0]

					if (final_triad_quality[0] == final_extensions_quality[0]):
						final_extensions_quality = ("", "", "", "")

					possible_qualities.append(final_triad_quality[p_style] + final_extensions_quality[p_style] + str(max([x.getNumeral() for x in chord_intervals if x])) + triad_quality_and_accidentals[1] + extensions_quality_and_accidentals[1])
			
			return min(possible_qualities, key=len)

		except: print("Error: Failed to get quality of parent chord for chord: " + str(self))

	def getQuality(self, p_style = 2, p_system = DEFAULT_SYSTEM):

		try:
			parent_chord_quality = self.getParentChordQuality(p_style, p_system)
			regex = (("(" + str([item for representations in CHORD_QUALITIES[p_system] for item in representations]).replace('\'', "").replace(" ", "").replace(',', "|").replace('+', "\+")[1:][:-1] + ")") * 2) + "*(\d+)"
			quality_contents = re.search(re.compile(regex), parent_chord_quality)

			bass_triad_quality = quality_contents.group(1)
			extensions_quality = quality_contents.group(2)

			if (extensions_quality == None): extensions_quality = ""

			extensions_numeral = max([item.getNumeral() for item in self.getIntervals()])

			accidentals_regex = str([item for item in ACCIDENTALS[p_system].values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1]
			interval_regex = "[" + accidentals_regex + "]+\d+"
			altered_intervals = re.findall(re.compile(interval_regex), parent_chord_quality)

			modifications = []

			for altered_interval in altered_intervals:
				if (Interval.stringToInterval(altered_interval).getNumeral() <= int(extensions_numeral)): modifications.append((altered_interval, Interval.stringToInterval(altered_interval).getNumeral()))

			interval_regex_optional_accidental = "[" + accidentals_regex + "]*\d+"
			regex = OMISSION_NOTATION[p_system] + interval_regex_optional_accidental
			omitted_intervals = re.findall(re.compile(regex), parent_chord_quality)

			for omitted_interval in omitted_intervals:
				interval_string = re.findall(re.compile(interval_regex_optional_accidental), str(omitted_interval))[0]
				my_quality = bass_triad_quality + extensions_quality + str(extensions_numeral)
				my_numeral = Interval.stringToInterval(interval_string).getNumeral()
				if (Interval.stringToInterval(interval_string).getNumeral() <= int(extensions_numeral)): modifications.append(("no" + str(Chord.stringToPitchClass(my_quality)[int(((my_numeral + 1) / 2) - 1)]), my_numeral))

			for interval in self.getIntervals():
				if ((interval.getNumeral() in [2, 4]) and (3 not in [item.getNumeral() for item in self.getIntervals()])): 
					modifications.append((str(SUSPENDED_NOTATION[p_system] + str(interval)), interval.getNumeral()))
					modifications.pop(modifications.index([item for item in modifications if item[1] == 3 and "no" in item[0]][0]))
				elif (((interval.getNumeral() - 1) % 2) != 0): modifications.append((str(ADDITION_NOTATION[p_system] + str(interval)), interval.getNumeral()))

			modifications = sorted(modifications, key=lambda x: x[1])
			modifications_string = ""

			for modification in modifications: modifications_string = modifications_string + modification[0]
			return bass_triad_quality + extensions_quality + str(extensions_numeral) + modifications_string

		except: print("Error: Failed to get quality of chord: " + str(self))

	def getNumeral(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):

		try:
			if (self.getParentDegree() != None):
				result = self.getParentDegree().getNumeral()
				if (p_with_quality == True): return result + self.getParentChordQuality(p_style, p_system)
				return result
				
			else: print("Error: Unable to retrieve numeral of Chord as there is not Parent Degree Assigned")
		
		except: print("Error: Failed to print numeral of chord: " + str(self))

	def getNumeralWithContext(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):

		try:
			if (self.getParentDegree() != None and self.getParentScale().getParentDegree() != None):
				secondary_information = "\\" + self.getParentScale().getParentDegree().build(Chord).getNumeral()
				return self.getNumeral(p_with_quality, p_style, p_system) + secondary_information

			else: print("Error: Unable to retrieve secondary information of Chord as there is not Parent Degree Assigned")
		
		except: print("Error: Failed to print numeral with context of chord: " + str(self))

	def getFiguredBass(self, p_slice = -1): 
		return self.getFirstInversion().getNumeral(False) + " " + self.pitchClassToFiguredBass(p_slice)

	def pitchClassToFiguredBass(self, p_slice):
		temp_chord = self.invert(1)

		while(temp_chord != self):
			if (temp_chord.getIntervals()[::-1][:p_slice] == self.getIntervals()[::-1][:p_slice] and p_slice != len(self.getIntervals())): return self.pitchClassToFiguredBass(p_slice + 1)
			temp_chord = temp_chord.invert(1)

		string = ""
		if (p_slice == -1): p_slice == 1
		for numeral in [item.getNumeral() for item in self.getIntervals()[::-1]][:p_slice]: string = string + str(numeral) + "/"

		return string[:-1]
			

	##########################
	# Transformation methods #
	##########################

	def transformChordTo(self, p_intervals):
		new_chord = Chord(self[1].getTone(), p_intervals)
		if (self.getParentDegree() != None): new_chord.setParentDegree(self.getParentDegree())
		return new_chord

	def getParallelChord(self):

		try:
			if (self.getParentDegree() != None):
				parallel_scale = self.getParentScale().getParallelScale()
				parallel_chord = parallel_scale[self[1].getPositionInParent()].build(Chord, self.getNumerals())
				return parallel_chord

			else: print("Error: Unable to get parallel of Chord that does not have a Parent Scale")

		except: print("Error: Failed to get parallel Chord")

	def getRelativeChord(self):

		try:
			if (self.getParentDegree() != None):
				relative_scale = self.getParentScale().getRelativeScale()
				relative_chord = relative_scale[self[1].getPositionInParent()].build(Chord, self.getNumerals())
				return relative_chord

			else: print("Error: Unable to get relative of Chord that does not have a Parent Scale")

		except: print("Error: Failed to get relative Chord")

	def getNegativeChord(self, p_axis_point = 3):

		try:
			first_inversion = self.getFirstInversion()
			generic_intervals_inverted = [item.getNumeral() for item in Scale.scaleStepsToPitchClass(Scale.pitchClassToScaleSteps(self.getIntervals())[:-1][::-1] + [1])]
			root = self.getParentScale().getNegativeScale(p_axis_point)[-first_inversion[1].getPositionInParent()] - ((2 * (self.getInversion() - 1)) + 1) - generic_intervals_inverted[-1]
			return root.build(Chord, generic_intervals_inverted)

		except: print("Error: Failed to get negative of chord: " + str(self))

	########################
	# Common Functionality #
	########################

	def resolveChord(self, p_system = DEFAULT_SYSTEM):
		try: return self.resolveChordInto((self.getFirstInversion() + RESOLUTION_SYSTEM[p_system])[1:4])
		except: print("Error: Failed to resolve Chords: " + str(self))

	def resolveChordInto(self, p_next_chord, p_system = DEFAULT_SYSTEM):
		resolution_list = []

		for degree in self.getDegrees():
			possible_motion = degree.getMotionToClosestDegree(p_next_chord)
			resolution_list.append(possible_motion)

		all_combinations = list(itertools.product(*resolution_list))
		possible_chords = []

		for combination in all_combinations:
			new_chord = self
			new_chord_size = len(new_chord.getIntervals())
			index = 1

			for move in combination:
				new_chord = new_chord[index].move(move)

				if (len(new_chord.getIntervals()) != new_chord_size): 
					new_chord_size = len(new_chord.getIntervals())
					continue

				index += 1

			possible_chords.append(new_chord)

		min_chord = None
		min_chord_count = 1000
		max_chord_size = 0

		for chord in possible_chords:
			temp_chord_count = chord.getDegreeRepetitionCount()
			temp_chord_size = len(chord.getIntervals())

			if (temp_chord_count < min_chord_count or (temp_chord_count == min_chord_count and temp_chord_size > max_chord_size)):
				min_chord = chord
				min_chord_count = temp_chord_count
				max_chord_size = temp_chord_size

		return min_chord

	def getPossibleParentScales(self, p_cardinality = 7, p_distinct = True):

		try:
			scale_list = {}

			for i in range(4096):
				if (len([item for item in str('{0:012b}'.format(i)) if item == '1']) == p_cardinality):
					new_scale = Scale(self[1].getTone(), Scale.decimalToPitchClass(i))
					if (new_scale.isDistinct() == p_distinct and self in new_scale): 
						scale_list[new_scale.getName()] = new_scale

			return scale_list
		
		except: print("Error: Failed to get possible Parent-Scales")

	def invert(self, p_inversion_number):

		try:
			new_chord = super(Chord._Degree, self[p_inversion_number + 1]).build(Chord, len(self.getIntervals()), 2)
			if (self.getParentDegree() != None): new_chord.setParentDegree(self[p_inversion_number + 1].findInParent())
			else: new_chord.parent_degree = None
			return new_chord

		except: print("Error: Failed to invert Chord: " + str(self) + " by " + str(p_inversion_number))

	def getInversion(self):

		try:
			next_inversion = self.getFirstInversion()
			counter = 1

			while(next_inversion.simplify() != self.simplify()):
				next_inversion = next_inversion.invert(1)
				counter = counter + 1

			return counter

		except: print("Error: Failed to get inversion number for Chord: " + str(self))

	def getFirstInversion(self):

		try:
			duplicates_found = False
			previous = self.buildOnThirds()
			smallest_inversion = previous
			min_interval_sum = sum([item.getSemitones() for item in smallest_inversion.getIntervals()])

			for i in range(len(self.getIntervals()) - 1):
				temp_chord = previous.invert(1).buildOnThirds()
				temp_interval_sum = sum([item.getSemitones() for item in temp_chord.getIntervals()])

				if (temp_interval_sum < min_interval_sum):
					duplicates_found = False
					smallest_inversion = temp_chord
					min_interval_sum = temp_interval_sum

				elif (temp_interval_sum == min_interval_sum): duplicates_found = True

				previous = temp_chord

			if (duplicates_found):
				print("Error: Failed to find first inversion as there are several possible candidates")
				return self

			return smallest_inversion

		except: print("Error: Failed to get first inversion of Chord: " + str(self))

	def getSecondaryDominant(self):
		if (self.getParentDegree() != None): return (self.getParentDegree().buildScale()[1] + P5).build(Chord, [P1, M3, P5, m7])
		else:
			self.setParentDegree(Scale(self[1].getTone(), [P1, M2, M3, P4, P5, M6, M7])[1])
			return (self.getParentDegree().buildScale()[1] + P5).build(Chord, [P1, M3, P5, m7])

	def getSecondarySubDominant(self):
		if (self.getParentDegree() != None): return (self.getParentDegree().buildScale()[1] + M2).build(Chord, [1, 3, 5, 7])
		else:
			self.setParentDegree(Scale(self[1].getTone(), [P1, M2, M3, P4, P5, M6, M7])[1])
			return (self.getParentDegree().buildScale()[1] + M2).build(Chord, [1, 3, 5, 7])

	def getSecondaryTonic(self):
		if (self.getParentDegree() != None): return (self.getParentDegree().buildScale()[1] + P1).build(Chord, [1, 3, 5])
		else:
			self.setParentDegree(Scale(self[1].getTone(), [P1, M2, M3, P4, P5, M6, M7])[1])
			return (self.getParentDegree().buildScale()[1] + P1).build(Chord, [1, 3, 5])

	def getSecondaryNeopolitan(self):
		if (self.getParentDegree() != None): return (self.getParentDegree().buildScale()[1] + M2).build(Chord, [1, 3, 5, 7])[1].transform("b")
		else:
			self.setParentDegree(Scale(self[1].getTone(), [P1, M2, M3, P4, P5, M6, M7])[1])
			return (self.getParentDegree().buildScale()[1] + M2).build(Chord, [1, 3, 5, 7])[1].transform("b")

	def getSecondaryAugmentedSix(self):
		if (self.getParentDegree() != None): return (self.getParentDegree().buildScale()[1] + P5).build(Chord, [P1, M3, P5, m7]).getSecondaryTritoneSubstitution()
		else:
			self.setParentDegree(Scale(self[1].getTone(), [P1, M2, M3, P4, P5, M6, M7])[1])
			return (self.getParentDegree().buildScale()[1] + P5).build(Chord, [P1, M3, P5, m7]).getSecondaryTritoneSubstitution()

	def getSecondaryTritoneSubstitution(self):
		if (self.getParentDegree() != None): return (self.getParentDegree().buildScale()[1] + P5).build(Chord, [P1, M3, P5, m7])[3].transform("b")
		else:
			self.setParentDegree(Scale(self[1].getTone(), [P1, M2, M3, P4, P5, M6, M7])[1])
			return (self.getParentDegree().buildScale()[1] + P5).build(Chord, [P1, M3, P5, m7])[3].transform("b")

	#################
	# Sugar Methods #
	#################

	def getDegreeRepetitionCount(self): 

		try:
			result = 0

			for interval in self.getIntervals():
				repeats = len([item for item in self.getIntervals() if item.simplify().getSemitones() == interval.simplify().getSemitones()])
				if (repeats > 1): result = result + repeats

			return result

		except: print("Error: Failed to count repeating intervals in: " + str(self))

	def buildOnThirds(self):

		try:
			new_chord = Chord(self[1].getTone(), [item for item in Chord.rearrangeIntervalsAsThirds(self.getIntervals()) if item != None])
			if (self.getParentDegree() != None): new_chord.setParentDegree(self.getParentDegree())
			return new_chord

		except: print("Error: Failed to build Chord: " + str(self) + " on thirds")

	def simplify(self):

		try:
			new_pitch_class = [item.simplify() for item in self.getIntervals()]
			new_pitch_class.sort(key=lambda x: x.getSemitones())
			new_chord = Chord(self[1].getTone(), new_pitch_class)
			if (self.getParentDegree() != None): new_chord.setParentDegree(self.getParentDegree())
			return new_chord

		except: print("Error: Failed to simplify intervals of Chord: " + str(self))

	def next(self):
		if (self.getParentDegree() != None): return (self[1].next()).build(Chord, self.getNumerals())
		else: return self.rotate()

	def previous(self):
		if (self.getParentDegree() != None): return (self[1].previous()).build(Chord, self.getNumerals())
		else: return self.rotate()

	##################
	# Static Methods #
	##################

	@staticmethod
	def fromString(p_quality, p_system = DEFAULT_SYSTEM): return Chord.stringToPitchClass(p_quality, p_system)

	@staticmethod
	def stringToPitchClass(p_quality, p_system = DEFAULT_SYSTEM):

		try:
			regex = (("(" + str([item for representations in CHORD_QUALITIES[p_system] for item in representations]).replace('\'', "").replace(" ", "").replace(',', "|").replace('+', "\+")[1:][:-1] + ")") * 2) + "*(\d+)"
			quality_contents = re.search(re.compile(regex), p_quality)

			bass_triad_quality = quality_contents.group(1)
			extensions_quality = quality_contents.group(2)
			extensions_numeral = quality_contents.group(3)

			if (extensions_quality == None):
				extensions_quality = bass_triad_quality

			accidentals_regex = str([item for item in ACCIDENTALS[p_system].values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1]
			interval_regex = "[" + accidentals_regex + "]\d+"
			altered_intervals = re.findall(re.compile(interval_regex), p_quality)

			for quality_tuple in CHORD_QUALITIES[p_system].keys():

				if (bass_triad_quality != ""):
					if bass_triad_quality in quality_tuple: bass_triad_pitch_class = CHORD_QUALITIES[p_system][quality_tuple][:]

				if extensions_quality in quality_tuple: extensions_pitch_class = CHORD_QUALITIES[p_system][quality_tuple][:]

			if (bass_triad_pitch_class != ""): result = (bass_triad_pitch_class[:3] + extensions_pitch_class[3:])[:int((int(extensions_numeral) + 1) / 2)]
			else: result = extensions_pitch_class[:int((int(extensions_numeral) + 1) / 2)]

			for altered_interval in altered_intervals:
				accidental = altered_interval[0]
				number = re.findall(r'\d+', altered_interval)[0]
				match = [item for item in result if item.getNumeral() == int(number)]

				if (len(match) != 0):
					interval_to_be_altered = match[0]
					result[extensions_pitch_class.index(interval_to_be_altered)] = Interval.stringToInterval(str(altered_interval))

			interval_regex_optional_accidental = "[" + accidentals_regex + "]*\d+"
			regex_sus = SUSPENDED_NOTATION[p_system] + interval_regex_optional_accidental
			sus_intervals = re.findall(re.compile(regex_sus), p_quality)
			list_of_sus_intervals = []

			for sus_interval in sus_intervals:
				interval = str(re.findall(re.compile(interval_regex_optional_accidental), str(sus_interval)))
				list_of_sus_intervals.append(Interval.stringToInterval(interval))

			result = result + list_of_sus_intervals
			if (len(list_of_sus_intervals) > 0 and 3 in [item.getNumeral() for item in result]): result.pop(result.index([item for item in result if item.getNumeral() == 3][0]))
			
			regex = ADDITION_NOTATION[p_system] + interval_regex_optional_accidental
			add_intervals = re.findall(re.compile(regex), p_quality)
			list_of_add_intervals = []

			for add_interval in add_intervals:
				interval = str(re.findall(re.compile(interval_regex_optional_accidental), str(add_interval)))
				list_of_add_intervals.append(Interval.stringToInterval(interval))

			result = result + list_of_add_intervals
			result.sort(key=lambda x: x.getSemitones())

			regex = OMISSION_NOTATION[p_system] + interval_regex_optional_accidental
			omitted_intervals = re.findall(re.compile(regex), p_quality)

			for omitted_interval in omitted_intervals:
				interval_string = str(re.findall(re.compile(interval_regex_optional_accidental), str(omitted_interval)))
				interval = Interval.stringToInterval(interval_string)

				if (interval in result): result.pop(result.index(interval))

			return result

		except: print("Error: Failed to convert string " + p_quality + " to pitch-class")

	@staticmethod
	def getPossibleQualitiesOfSlice(p_pitch_class, p_slice_start, p_slice_end, p_system = DEFAULT_SYSTEM):

		try:
			chord = p_pitch_class[p_slice_start:p_slice_end]
			chord_qualities = []

			for key in CHORD_QUALITIES[p_system].keys():
				temp_chord_quality_chord = CHORD_QUALITIES[p_system][key][p_slice_start:p_slice_end]
				temp_accidentals = ""
				exclude = False
				i = 0

				while(i < len(chord)):

					if (chord[i]):

						if (temp_chord_quality_chord[i] and (chord[i].getSemitones() > temp_chord_quality_chord[i].getSemitones()) and chord[i] in [P1, M3, P5, M7, M9, P11, M13]): exclude = True
						elif (chord[i] != temp_chord_quality_chord[i]): 
							temp_accidentals = temp_accidentals + chord[i]

					else:
						temp_accidentals = temp_accidentals + OMISSION_NOTATION[p_system] + str(temp_chord_quality_chord[i])
					i = i + 1

				if (not exclude): chord_qualities.append((key, temp_accidentals))

			return chord_qualities
		
		except: print("Error: Failed to get qualities of slice")

	@staticmethod
	def rearrangeIntervalsAsThirds(p_pitch_class, p_system = DEFAULT_SYSTEM):
		
		try: 
			new_interval_list = []

			for interval in p_pitch_class:
				possible_intervals = []

				if (((interval.getNumeral() - 1) % 2) != 0 and interval < P8): new_interval = interval + P8

				elif ((interval.getNumeral() - 1) % 2 != 0 and interval > P8 and interval < M13):
					new_interval = interval
					while (new_interval > P8): new_interval -= P8

				elif (interval > M13):
					new_interval = interval
					while (new_interval > M13 or ((new_interval.getNumeral() - 1) % 2) != 0): new_interval -= P8

				else:
					new_interval = interval

				if (new_interval != P8):
					new_interval_list.append(new_interval)

			new_interval_list.sort(key=lambda x: x.getSemitones())
			previous_numeral = -1
			i = 0

			while (i < len(new_interval_list)):

				if (new_interval_list[i].getNumeral() - previous_numeral != 2):
					difference = new_interval_list[i].getNumeral() - previous_numeral

					for j in range(int((difference - 2)/2)):
						new_interval_list.insert(i, None)
						i = i + 1

				previous_numeral = new_interval_list[i].getNumeral()
				i = i + 1

			return new_interval_list
		
		except: print("Error: Failed to rearrange intervals " + p_pitch_class + "as thirds")

	def getPitchClassByQuality(p_quality, p_system = DEFAULT_SYSTEM):

		for key in CHORD_QUALITIES[p_system].keys():
			if p_quality in key: return CHORD_QUALITIES[p_system][key]

		return None

	##################################
	# Overridden Methods and Classes #
	##################################

	def setParentDegree(self, p_degree): self.parent_degree = self.configureParentDegree(p_degree)

	def configureParentDegree(self, p_degree):
		result_scale = p_degree.getParentScale()
		root_altered = False

		for degree in self.getDegrees():

			interval_in_parent = (p_degree.getInterval() + degree.getInterval())
			if (interval_in_parent.getNumeral() > max([item.getNumeral() for item in result_scale.getIntervals()])): interval_in_parent = interval_in_parent.simplify()

			if (interval_in_parent not in result_scale):

				if (result_scale.isDistinct() and self.isDistinct()):

					if (interval_in_parent.getNumeral() == 1):
						root_altered = True
						alteration = interval_in_parent.getAccidental()

					result_scale = result_scale.replaceAtNumeralWith(interval_in_parent.getNumeral(), interval_in_parent)

				else: result_scale = result_scale.addInterval(interval_in_parent)

		if (root_altered): return result_scale.getDegreeByNumeral(p_degree.getInterval().getNumeral())
		return result_scale.getDegreeByInterval(p_degree.getInterval())

	class _Degree(Scale._Degree):

		def __add__(self, p_other):	
			if (self.getParentScale().getParentDegree() != None and (isinstance(p_other, int) or isinstance(p_other, Interval))): return self.findInParent() + p_other
			else: return super().__add__(p_other)

		def __sub__(self, p_other):
			if (self.getParentScale().getParentDegree() != None and (isinstance(p_other, int) or isinstance(p_other, Interval))): return self.findInParent() - p_other
			else: return super().__sub__(p_other)

		def build(self, object_type, p_num_tones = 4, p_leap_size = 3, *args):
			if (self.getParentScale().getParentDegree() != None): return self.findInParent().build(object_type, p_num_tones, p_leap_size, *args)
			else: return super().build(object_type, p_num_tones, p_leap_size, *args)

		def buildScale(self):
			if (self.getParentScale().getParentDegree() != None): return self.findInParent().buildScale()
			else: return super().buildScale()

		def buildScaleWithIntervals(self, p_intervals):
			if (self.getParentScale().getParentDegree() != None): return self.findInParent().buildScaleWithIntervals(p_intervals)
			else: return super().buildScaleWithIntervals(p_intervals)

		def buildPitchClass(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM):
			if (self.getParentScale().getParentDegree() != None): return self.findInParent().buildPitchClass(p_num_tones, p_leap_size, p_system)
			else: return super().buildPitchClass(p_num_tones, p_leap_size, p_system)

		def next(self):
			if (self.getParentScale().getParentDegree() != None): return self.findInParent().next()
			else: return super().next()

		def previous(self):
			if (self.getParentScale().getParentDegree() != None): return self.findInParent().previous()
			else: return super().previous()

		def transform(self, p_accidental):

			try: 
				new_object = super().transform(p_accidental)

				if (self.getParentScale().getParentDegree() != None):
					new_parent = self.findInParent().transform(p_accidental)
					new_object.setParentDegree(new_parent[self.getParentScale()[1].findInParent().getPosition()])

				return new_object

			except: print("Error: Failed to transform: " + str(self) + " by the accidental " + str(p_accidental))

		def move(self, p_interval):
			new_chord = (self + p_interval).build(Chord, 1)

			if (self.getPosition() != 1): 
				new_chord_start = self.getParentScale()[1:self.getPosition() - 1]
				if (new_chord_start[len(new_chord_start.getIntervals())].getTone() != new_chord[1].getTone()): new_chord = new_chord_start + new_chord
				else: new_chord = new_chord_start
				
			if (self.getPosition() != len(self.getParentScale().getIntervals())): 
				new_chord_end = self.getParentScale()[self.getPosition() + 1:len(self.getParentScale().getIntervals())]
				if (new_chord_end[1].getTone() != new_chord[len(new_chord.getIntervals())].getTone()): new_chord = new_chord + new_chord_end
				else: new_chord = new_chord[1:len(new_chord.getIntervals()) - 1] + new_chord_end
				
			return new_chord

		def getPositionInFirstInversion(self):

			try:
				first_inversion = self.getParentScale().getFirstInversion()
				for degree in first_inversion.getDegrees(): 
					if (degree.getInterval().simplify() == (first_inversion[self.getParentScale().getInversion()].getInterval() + self.getInterval()).simplify()): return degree.getPosition()

				return None
			
			except: print("Error: Failed to get the position of: " + str(self) + " in first inversion")

		def getMotionToClosestDegree(self, p_next_chord):
			min_positive_distance = min([(degree - self).simplify() for degree in p_next_chord.getDegrees()])
			min_negative_distance = min([(self - degree).simplify() for degree in p_next_chord.getDegrees()])
			return [min_positive_distance, -min_negative_distance]