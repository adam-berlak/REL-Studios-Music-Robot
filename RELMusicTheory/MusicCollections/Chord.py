import itertools

from MusicCollections.Scale import *
from MusicCollections.IntervalList import *
from IMusicObject import *

class Chord(IntervalList, IMusicObject):
	
	def __init__(self,  
				p_item_1, 
				p_item_2 = None, 
				p_root = None, 
				p_bass_triad_quality = None,
				p_extensions_quality = None, 
				p_fixed_invert = None, 
				p_modulate_parent = False, 
				p_type_dict = {}): 
		
		if isinstance(p_item_1, Scale):	
			self.intervals = p_item_1.getIntervals()
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None else self.intervals[-1].roof()	
			self.bass_triad_quality = Chord.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Bass Triad Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_bass_triad_quality
			self.extensions_quality = Chord.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Extensions Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_extensions_quality
			self.parent_item = self.configureParentItem(p_item_1[1], self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getTone()
			self.root = p_root if p_root is not None else self.parent_item + IntervalListUtilities.findRoot(self.intervals)
		
		elif isinstance(p_item_1, list) and len(p_item_1) != 0 and (isinstance(p_item_1[0], IPitchedObject) or isinstance(p_item_1[0], Tone)):
			self.intervals = [item - p_item_1[0] for item in p_item_1]	
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None else self.intervals[-1].roof()	
			self.bass_triad_quality = Chord.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Bass Triad Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_bass_triad_quality
			self.extensions_quality = Chord.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Extensions Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_extensions_quality
			self.parent_item = self.configureParentItem(Scale(p_item_1, Chord.identifyParentScale(self.bass_triad_quality, self.extensions_quality))[1], self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getTone()
			self.root = p_root if p_root is not None else self.parent_item + IntervalListUtilities.findRoot(self.intervals)
		
		elif isinstance(p_item_1, Scale.Degree) and isinstance(p_item_2, list) and len(p_item_2) != 0 and (isinstance(p_item_2[0], int) or isinstance(p_item_2[0], Interval)):
			self.intervals = p_item_2 
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None else self.intervals[-1].roof()	
			self.bass_triad_quality = Chord.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Bass Triad Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_bass_triad_quality
			self.extensions_quality = Chord.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Extensions Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_extensions_quality
			self.parent_item = self.configureParentItem(p_item_1, self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getTone()
			self.root = p_root if p_root is not None else self.parent_item + IntervalListUtilities.findRoot(self.intervals)

		elif isinstance(p_item_1, IPitchedObject) and isinstance(p_item_2, list) and len(p_item_2) != 0 and (isinstance(p_item_2[0], int) or isinstance(p_item_2[0], Interval)):
			self.intervals = p_item_2 	
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None else self.intervals[-1].roof()	   
			self.bass_triad_quality = Chord.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Bass Triad Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_bass_triad_quality
			self.extensions_quality = Chord.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Extensions Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_extensions_quality
			self.parent_item = self.configureParentItem(Scale(p_item_1, Chord.identifyParentScale(self.bass_triad_quality, self.extensions_quality))[1], self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getTone()
			self.root = p_root if p_root is not None else self.parent_item + IntervalListUtilities.findRoot(self.intervals)
		
		elif isinstance(p_item_1, IPitchedObject) and isinstance(p_item_2, str):
			self.intervals = Chord.stringToPitchClass(p_item_2)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None else self.intervals[-1].roof()					
			self.bass_triad_quality = Chord.stringQualityToData(p_item_2)["Bass Triad Quality"]
			self.extensions_quality = Chord.stringQualityToData(p_item_2)["Extensions Quality"]
			self.parent_item = self.configureParentItem(Scale(p_item_1, Chord.identifyParentScale(self.bass_triad_quality, self.extensions_quality))[1], self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getTone()
			self.root = self.parent_item

		elif isinstance(p_item_1, Scale.Item) and isinstance(p_item_2, str):
			self.intervals = Chord.stringToPitchClass(p_item_2)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None else self.intervals[-1].roof()					
			self.bass_triad_quality = Chord.stringQualityToData(p_item_2)["Bass Triad Quality"]
			self.extensions_quality = Chord.stringQualityToData(p_item_2)["Extensions Quality"]
			self.parent_item = self.configureParentItem(p_item_1, self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getTone()
			self.root = self.parent_item
	
		else: 
			print("Error: Cannot build Chord object with these Parameters")
			return

		self.buildComponents()

	#####################################
	# Methods concerning class behavior #
	#####################################

	def __getitem__(self, p_index): 

		if isinstance(p_index, tuple):
			items = [self.getitem_BL(1).__add__(item) for item in p_index]
			result = items[0]

			for item in items[1:]:
				result += item

			return result
		
		elif isinstance(p_index, int): return self.getItems()[0].__add__(p_index)

		else: return super().__getitem__(p_index)

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):
		if (self.getParentItem() != None and (isinstance(p_other, int) or isinstance(p_other, Interval))):
			if (isinstance(p_other, Interval)): return (self.getParentItem() + p_other).build(Chord, self.getIntervals())
			if (isinstance(p_other, int)): return (self.getParentItem() + p_other).build(Chord, self.getNumerals())

		else: return super().__add__(p_other)

	def __sub__(self, p_other):
		if (isinstance(p_other, Interval)): self + (-p_other)
		if (isinstance(p_other, int)): self + (-p_other)	
		else: return super().__sub__(p_other)
	
	def __radd__(self, p_other):
		if (isinstance(p_other, str)): return p_other + str(self)

	###########################
	# Playable Object Methods #
	###########################

	def __play__(self):
		return

	def __toMidiData__(self): 
		try: return self.getTones()
		except: print("Error: Unable to convert object to midi data as it does not contain playable objects")
		
	################################
	# Methods concerned with names #
	################################

	@staticmethod
	def intervalsToQuality(p_intervals, p_bass_triad_quality = None, p_extensions_quality = None, p_system = DEFAULT_SYSTEM):
		bass_triad_qualities = Chord.evaluateQualityAssignments(p_intervals, slice(None, 3, None), p_bass_triad_quality, p_system)
		extensions_qualities = Chord.evaluateQualityAssignments(p_intervals, slice(3, None, None), p_extensions_quality, p_system)
		possible_qualities = []

		for extensions_quality_data in extensions_qualities:
			for triad_quality_data in bass_triad_qualities:

				data = {
					"Bass Triad Quality": triad_quality_data["Quality"], 
					"Bass Triad Accidentals": triad_quality_data["Accidentals"], 
					"Bass Triad Omissions": [item for item in triad_quality_data["Omissions"] if item[1].getNumeral() < max([x.getNumeral() for x in p_intervals if x])],
					"Extensions Quality": extensions_quality_data["Quality"],                 
					"Extensions Accidentals" : extensions_quality_data["Accidentals"], 
					"Extensions Omissions": [item for item in extensions_quality_data["Omissions"] if item[1].getNumeral() < max([x.getNumeral() for x in p_intervals if x])],
					"Extensions Size": max([x.getNumeral() for x in p_intervals if x])
				}

				evaluation = triad_quality_data["Evaluation"] + extensions_quality_data["Evaluation"]
				possible_qualities.append((data, evaluation))

		return min(possible_qualities, key=lambda x: x[1])[0]

	def getParentChordQualityData(self, p_system = DEFAULT_SYSTEM):
		return Chord.intervalsToQuality(self.getParentChord().getIntervals(), self.getBassTriadQuality(), self.getExtensionsQuality(), p_system)

	def getParentChordQuality(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		data = self.getParentChordQualityData(p_system)
		modifications = data["Bass Triad Accidentals"] + data["Bass Triad Omissions"] + data["Extensions Accidentals"] + data["Extensions Omissions"]
		modifications.sort(key=lambda x: x[1].getNumeral())
		return data["Bass Triad Quality"][p_style] + (data["Extensions Quality"][p_style] if data["Bass Triad Quality"] != data["Extensions Quality"] else "") + str(data["Extensions Size"]) + (''.join([item[0] + str(item[1]) for item in modifications]))

	def getQualityData(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		parent_chord_quality_data = self.getParentChordQualityData(p_system)
		temp_first_inversion_intervals = self.getRootPosition().getIntervals()
		add = []
		sus = []

		for interval in temp_first_inversion_intervals:
			if (not (interval.getNumeral() - 1) % 2) == 0:
				if (interval.getNumeral() in [2, 4]) and (3 not in [item.getNumeral() for item in temp_first_inversion_intervals]): sus.append((SUSPENDED_NOTATION[p_system], interval))
				else: add.append((ADDITION_NOTATION[p_system], interval))

		parent_chord_quality_data["Added"] = add
		parent_chord_quality_data["Suspended"] = sus

		return parent_chord_quality_data

	def getQuality(self, p_style = 2, p_system = DEFAULT_SYSTEM):
		data = self.getQualityData(p_style, p_system)
		modifications = data["Bass Triad Accidentals"] + data["Bass Triad Omissions"] + data["Extensions Accidentals"] + data["Extensions Omissions"] + data["Added"] + data["Suspended"]
		modifications.sort(key=lambda x: x[1].getNumeral())
		return data["Bass Triad Quality"][p_style] + (data["Extensions Quality"][p_style] if data["Bass Triad Quality"] != data["Extensions Quality"] else "") + str(data["Extensions Size"]) + (''.join([item[0] + str(item[1]) for item in modifications]))

	@staticmethod
	def evaluateQualityAssignments(p_chord_intervals, p_slice, p_quality = None, p_system = DEFAULT_SYSTEM):
		chord_qualities = []
		in_qualities = [item for item in CHORD_QUALITIES[p_system].keys() if p_quality in item] if p_quality is not None else CHORD_QUALITIES[p_system].keys() 

		for key in in_qualities:
			temp_in_chord_intervals = p_chord_intervals[p_slice]
			temp_chord_quality_chord = [item for item in CHORD_QUALITIES[p_system][key] if item is not None][p_slice]

			evaluation = 0
			temp_accidentals = []
			omitted_intervals = []

			for interval in temp_chord_quality_chord:
				if (interval.getNumeral() not in [item.getNumeral() for item in temp_in_chord_intervals]): 
					omitted_intervals += [(OMISSION_NOTATION[p_system], interval)]
					evaluation += 1
				else:
					for item in [item for item in temp_in_chord_intervals if item.getNumeral() == interval.getNumeral()]:
						if (item != interval):
							temp_accidentals += [("", item)]
							evaluation += 1

			chord_qualities.append({
					"Quality": key, 
					"Accidentals": temp_accidentals, 
					"Omissions": omitted_intervals, 
					"Evaluation": evaluation}
				)

		return chord_qualities

	@staticmethod
	def stringQualityToData(p_quality, p_system = DEFAULT_SYSTEM):
		regex = (("(" + str([item for representations in CHORD_QUALITIES[p_system] for item in representations]).replace('\'', "").replace(" ", "").replace(',', "|").replace('+', "\+")[1:][:-1] + ")") * 2) + "*(\d+)"
		quality_contents = re.search(re.compile(regex), p_quality)

		bass_triad_quality = quality_contents.group(1)
		extensions_quality = quality_contents.group(2)
		extensions_numeral = quality_contents.group(3)

		extensions_quality = bass_triad_quality if extensions_quality is None else extensions_quality

		regex_accidentals = str([item for item in ACCIDENTALS[p_system].values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1]
		regex_optional_accidentals = "[" + regex_accidentals + "]*\d+"

		regex_alt = "[" + regex_accidentals + "]\d+"
		altered_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_alt), p_quality)]

		regex_sus = SUSPENDED_NOTATION[p_system] + regex_optional_accidentals
		sus_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_sus), p_quality)]

		regex_add = ADDITION_NOTATION[p_system] + regex_optional_accidentals
		add_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_add), p_quality)]

		regex_omit = OMISSION_NOTATION[p_system] + regex_optional_accidentals
		omitted_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_omit), p_quality)]

		data = {
				"Bass Triad Quality": bass_triad_quality, 
				"Bass Triad Accidentals": [item for item in altered_intervals if item.getNumeral() <= 5], 
				"Bass Triad Added": [item for item in add_intervals if item.getNumeral() <= 5],
				"Bass Triad Omissions": [item for item in omitted_intervals if item.getNumeral() <= 5], 
				"Extensions Quality": extensions_quality,                 
				"Extensions Accidentals" : [item for item in altered_intervals if item.getNumeral() > 5], 
				"Extensions Added" : [item for item in add_intervals if item.getNumeral() > 5], 
				"Extensions Omissions": [item for item in omitted_intervals if item.getNumeral() > 5], 
				"Suspended" : sus_intervals, 
				"Extensions Size": extensions_numeral
			}

		return data

	@staticmethod
	def stringToPitchClass(p_quality, p_system = DEFAULT_SYSTEM):
		data = Chord.stringQualityToData(p_quality, p_system)

		bass_triad_quality = data["Bass Triad Quality"]
		extensions_quality = data["Extensions Quality"]
		list_of_alt_intervals = data["Bass Triad Accidentals"] + data["Extensions Accidentals"]
		list_of_sus_intervals = data["Suspended"]
		list_of_add_intervals = data["Bass Triad Added"] + data["Extensions Added"]
		list_of_omi_intervals = data["Bass Triad Omissions"] + data["Extensions Omissions"]
		extensions_numeral = data["Extensions Size"]

		for quality_tuple in CHORD_QUALITIES[p_system].keys():
			if bass_triad_quality in quality_tuple: bass_triad_pitch_class = CHORD_QUALITIES[p_system][quality_tuple][:3]
			if extensions_quality in quality_tuple: extensions_pitch_class = CHORD_QUALITIES[p_system][quality_tuple][3:]

		result = (bass_triad_pitch_class + extensions_pitch_class)[:int((int(extensions_numeral) + 1) / 2)]

		for altered_interval in list_of_alt_intervals:
			match = [item for item in result if item.getNumeral() == altered_interval.getNumeral()]
			if len(match) != 0: result[result.index(match[0])] = altered_interval

		result = result + list_of_sus_intervals
		if (len(list_of_sus_intervals) > 0 and 3 in [item.getNumeral() for item in result]): result.pop(result.index([item for item in result if item.getNumeral() == 3][0]))

		result = result + list_of_add_intervals
		result.sort(key=lambda x: x.getSemitones())
		
		for omitted_interval in list_of_omi_intervals:
			if omitted_interval in result: result.pop(result.index(omitted_interval)) 

		return result

	@staticmethod
	def identifyParentScale(p_bass_triad_quality, p_extensions_quality):
		result_scale = [item for item in IntervalListUtilities.simplifyIntervals(Chord.stringToPitchClassFast(p_bass_triad_quality)) if item.getNumeral() in (1, 3, 5)]
		result_scale += [item for item in IntervalListUtilities.simplifyIntervals(Chord.stringToPitchClassFast(p_extensions_quality)) if item.getNumeral() in (2, 4, 6, 7)]
		return IntervalListUtilities.sortIntervals(result_scale)

	@staticmethod
	def stringToPitchClassFast(p_quality):
		results = [item for item in CHORD_QUALITIES[DEFAULT_SYSTEM].keys() if p_quality in item]
		return [item for item in CHORD_QUALITIES[DEFAULT_SYSTEM][results[0]] if item is not None] if len(results) > 0 else None

	def getNumeral(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):
		return self.getRoot().getNumeral() + self.getParentChordQuality(p_style, p_system) if p_with_quality else self.getRoot().getNumeral()

	def getNumeralWithContext(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):
		secondary_information = "\\" + self.getParentIntervalList().getParentItem().build(Chord).getNumeral() if self.getParentIntervalList().getParentItem() is not None else ""
		return self.getNumeral(p_with_quality, p_style, p_system) + secondary_information

	def getFiguredBass(self, p_slice = -1): 
		return self.getParentChord().getNumeral(False) + " " + self.pitchClassToFiguredBass(p_slice)

	def getAllInversions(self):
		return [self.invert(item) for item in range(len(self.getIntervals()))]

	def pitchClassToFiguredBass(self, p_slice):
		temp_chord = self.invert(1)

		for temp_chord in self.getAllInversions():
			if (temp_chord.getIntervals()[::-1][:p_slice] == self.getIntervals()[::-1][:p_slice] and p_slice != len(self.getIntervals())): return self.pitchClassToFiguredBass(p_slice + 1)
			temp_chord = temp_chord.invert(1)

		string = ""
		if (p_slice == -1): p_slice == 1
		for numeral in [item.getNumeral() for item in self.getIntervals()[::-1]][:p_slice]: string = string + str(numeral) + "/"

		return string[:-1]		

	##########################
	# Transformation methods #
	##########################

	def getParentChord(self):
		new_chord = self.getRootPosition().buildOnThirds()
		return new_chord

	def transformChordTo(self, p_intervals):
		new_chord = Chord(self.getParentItem(), p_intervals)
		return new_chord

	def getParallelChord(self, p_reflection_point = 5):
		parallel_scale = self.getParentIntervalList().getParallelScale(p_reflection_point)
		new_chord = parallel_scale[self[1].getPositionInParent()].build(Chord, self.getNumerals())
		return new_chord

	def getRelativeChord(self, p_reflection_point = 5):
		relative_scale = self.getParentIntervalList().getRelativeScale(p_reflection_point)
		new_chord = relative_scale[self[1].getPositionInParent()].build(Chord, self.getNumerals())
		return new_chord

	def getNegativeChord(self, p_reflection_point = 5):
		parent_chord = self.getRootPosition().buildOnThirds()
		generic_intervals_inverted = [item.getNumeral() for item in IntervalListUtilities.scaleStepsToPitchClass(IntervalListUtilities.pitchClassToScaleSteps(self.getIntervals())[:-1][::-1] + [1])]
		root = self.getParentIntervalList().getNegativeScale(p_reflection_point)[-parent_chord[1].getPositionInParent()] - ((2 * self.getInversion()) + 1) - generic_intervals_inverted[-1]
		new_chord = root.build(Chord, generic_intervals_inverted)
		return new_chord

	########################
	# Common Functionality #
	########################

	def resolveChord(self, p_system = DEFAULT_SYSTEM):
		return self.resolveChordInto((self.getRootPosition().buildOnThirds() + RESOLUTION_SYSTEM[p_system])[1:4])

	def resolveChordInto(self, p_next_chord, p_system = DEFAULT_SYSTEM):
		resolution_list = []

		for item in self.getParts():
			possible_motion = item.getMotionToClosestItem(p_next_chord)
			resolution_list.append(possible_motion)

		all_combinations = list(itertools.product(*resolution_list))
		possible_chords = []

		for combination in all_combinations:
			new_chord = self
			new_chord_size = len(new_chord.getIntervals())
			index = 1

			for move in combination:
				new_chord = super(type(new_chord), new_chord).__getitem__(index).move(move)

				if (len(new_chord.getIntervals()) != new_chord_size): 
					new_chord_size = len(new_chord.getIntervals())
					continue

				index += 1

			possible_chords.append(new_chord)

		min_chord = None
		min_chord_count = 1000
		max_chord_size = 0

		for chord in possible_chords:
			temp_chord_count = chord.getItemRepetitionCount()
			temp_chord_size = len(chord.getIntervals())

			if (temp_chord_count < min_chord_count or (temp_chord_count == min_chord_count and temp_chord_size > max_chord_size)):
				min_chord = chord
				min_chord_count = temp_chord_count
				max_chord_size = temp_chord_size

		return min_chord

	def getPossibleParentScales(self, p_cardinality = 7, p_distinct = True):
		scale_list = {}

		for i in range(4096):

			if (len([item for item in str('{0:012b}'.format(i)) if item == '1']) == p_cardinality):
				new_scale = Scale(self[1].getTone(), IntervalListUtilities.decimalToPitchClass(i))

				if (IntervalListUtilities.isDistinct(new_scale.getIntervals()) == p_distinct and self in new_scale): 
					scale_list[new_scale.getName()] = new_scale

		return scale_list

	def invert(self, p_inversion_number = 1):
		if p_inversion_number == 0: return self
		temp_new_chord = Chord(super().__getitem__(int(2*(p_inversion_number/abs(p_inversion_number)))).findInParent(), IntervalListUtilities.invertStatic(self.getIntervals(), (p_inversion_number/abs(p_inversion_number)), self.getFixedInvert()), self.getRoot(), self.getBassTriadQuality(), self.getExtensionsQuality(), self.getFixedInvert())
		new_chord = temp_new_chord.invert(p_inversion_number - (p_inversion_number/abs(p_inversion_number))) if abs(p_inversion_number) != 1 else temp_new_chord
		return new_chord

	def getInversion(self):

		if not self.isRootless():
			result = len(self.getParts()) - ([item for item in self.getParts() if item.getTone().getTone() == self.getRoot().getTone().getTone()][0].getPosition() - 1)
			return result if result != len(self.getParts()) else 0

		else: 
			print("Failed to retrieve inversion of Chord as the Chord is rootless")
			return 0

	def isRootless(self):
		return not self.getRoot().getTone().getTone() in [item.getTone() for item in self.getTones()]

	def getRootPosition(self):
		new_chord = self.invert(-self.getInversion())
		return new_chord

	def getSecondaryDominant(self):
		root = (self.getParentItem().buildScale()[1] + 5)
		new_chord = root.build(Chord, [P1, M3, P5, m7], p_args = {"p_root": root, "p_bass_triad_quality": "dom", "p_extensions_quality": "dom", "p_modulate_parent": True})
		return new_chord

	def getSecondarySubDominant(self):
		root = (self.getParentItem().buildScale()[1] + 2)
		new_chord = root.build(Chord, [1, 3, 5, 7], p_args = {"p_root": root})
		return new_chord

	def getSecondaryTonic(self):
		root = (self.getParentItem().buildScale()[1] + 1)
		new_chord = root.build(Chord, [1, 3, 5], p_args = {"p_root": root})
		return new_chord

	def getSecondaryNeopolitan(self):
		new_chord.getSecondarySubDominant()[1].transform("b")
		return new_chord

	def getSecondaryAugmentedSix(self):
		new_chord = self.getSecondaryDominant().getSecondaryTritoneSubstitution()
		return new_chord

	def getSecondaryTritoneSubstitution(self):
		new_chord = self.getSecondaryDominant()[3].transform("b")
		return new_chord

	#################
	# Sugar Methods #
	#################

	def getItemRepetitionCount(self): 
		result = 0

		for interval in self.getIntervals():
			repeats = len([item for item in self.getIntervals() if item.simplify().getSemitones() == interval.simplify().getSemitones()])
			if (repeats > 1): result = result + repeats

		return result

	def buildOnThirds(self):
		new_intervals = [item for item in IntervalListUtilities.rearrangeIntervalsAsThirds(self.getIntervals()) if item != None]
		new_chord = Chord(self.getParentItem(), new_intervals, **self.getAttributes())
		return new_chord

	def simplify(self):
		new_intervals = [item.simplify() for item in self.getIntervals()]
		new_intervals.sort(key=lambda x: x.getSemitones())
		new_chord = Chord(self.getParentItem(), new_intervals, **self.getAttributes())
		return new_chord

	def next(self):
		new_chord = (self[1].next()).build(Chord, self.getNumerals(), p_args = {"p_root": self.getRoot() + 1})
		return new_chord

	def previous(self):
		new_chord = (self[1].previous()).build(Chord, self.getNumerals(), p_args = {"p_root": self.getRoot() - 1})
		return new_chord

	##############################
	# Overridable Business Logic #
	##############################

	def addInterval_BL(self, p_interval, p_attributes = {}):
		new_pitch_class = self.getIntervals()[:]

		if p_interval not in new_pitch_class:
			new_pitch_class.append(p_interval)
			new_pitch_class.sort(key=lambda x: x.getSemitones())
			
		new_reference_point = self.getParentItem() if self.getParentItem() is not None else self.getitem_BL(1).getTone()
		new_scale = type(self)(new_reference_point, new_pitch_class, **self.getAttributes(), p_type_dict = {p_interval: p_attributes})
		return new_scale

	def buildComponents(self):
		self.items = []
		
		for i in range(len(self.intervals)): 
			self.items.append(type(self).Part(self.intervals[i], self))

	def getAttributes(self):
		return {
			"p_root": self.getRoot(),
			"p_bass_triad_quality": self.getBassTriadQuality(),
			"p_extensions_quality": self.getExtensionsQuality()
		}

	#################
	# Configuration #
	#################

	def setParentItem(self, p_item): 
		if (p_item == None): return
		self.parent_item = self.configureParentItem(p_item, self.getIntervals())

	def configureParentItem(self, p_item, p_intervals, p_modulate_parent = False):
		result_scale = p_item.getParentIntervalList()
		root_altered = False

		for interval in p_intervals:
			interval_in_parent = (p_item.getInterval() + interval)
			interval_in_parent = interval_in_parent.simplify()

			if (interval_in_parent not in result_scale):
				if (p_modulate_parent and IntervalListUtilities.isDistinct(p_intervals)):
					if (interval_in_parent.getNumeral() == 1):
						root_altered = True
						alteration = interval_in_parent.getAccidental()
					result_scale = result_scale.replaceAtNumeralWith(interval_in_parent.getNumeral(), interval_in_parent)
				else: result_scale = result_scale.addInterval(interval_in_parent, p_attributes = {"p_chromatic": True})
					
		if (root_altered): return result_scale.getItemByNumeral(p_item.getInterval().getNumeral())
		return result_scale.getItemByInterval(p_item.getInterval())

	#######################
	# Getters and Setters #
	#######################

	def getParts(self): return self.items
	def getFixedInvert(self): return self.fixed_invert
	def getRoot(self): return self.root
	def getBassTriadQuality(self): return self.bass_triad_quality
	def getExtensionsQuality(self): return self.extensions_quality

	class Part(IntervalList.Item):

		##############################
		# Overridden Wrapper Methods #
		##############################
		
		def __add__(self, p_other):

			if isinstance(p_other, int):
				if abs(p_other) == 1: return self
				new_interval = (self.findInParent() + p_other) - self.getParentIntervalList().getItems()[0].findInParent()

				if (new_interval < P1):
					return (self.getParentIntervalList().sub_BL(P8))[self.getPosition()] - (p_other - 7)

				if (new_interval >= self.getParentIntervalList().getIntervals()[-1].roof()):
					return (self.getParentIntervalList().add_BL(P8)).getItems()[self.getPosition() - 1] + (p_other - 7)
				
				if new_interval not in self.getParentIntervalList().getIntervals(): 
					return self.getParentIntervalList().addInterval(new_interval).getItemByInterval(new_interval)

				else: return self.getParentIntervalList().getItemByInterval(new_interval)
			else: return super().__add__(p_other)

		def next(self):
			return self.findInParent().next()

		def previous(self):
			return self.findInParent().previous()
		
		def build_BL(self, object_type, p_num_tones = 4, p_leap_size = 3, p_args = {}):
			return self.findInParent().build(object_type, p_num_tones, p_leap_size, p_args)

		def buildScale_BL(self):
			return self.findInParent().buildScale()

		def buildScaleWithIntervals_BL(self, p_intervals):
			return self.findInParent().buildScaleWithIntervals(p_intervals)

		def buildPitchClass_BL(self, p_num_tones = -1, p_leap_size = 2, p_system = DEFAULT_SYSTEM):
			return self.findInParent().buildPitchClass(p_num_tones, p_leap_size, p_system)

		###############
		# New Methods #
		###############

		def isNonHarmonic(self):
			return self.findInParentChord().getInterval().getNumeral() > 7

		def findInParentChord(self):
			temp_delta_to_root = self.getParentIntervalList().getRoot() - self.getParentIntervalList().getParentItem() 
			temp_intervals = IntervalListUtilities.scaleIntervalsByOrder([temp_delta_to_root, self.getInterval()])
			temp_intervals = IntervalListUtilities.normalizeIntervals(temp_intervals)
			temp_intervals = IntervalListUtilities.buildOnThirdsStatic(temp_intervals)
			return self.getParentIntervalList().getParentChord()[1] + temp_intervals[-1]

		def transform(self, p_accidental):
			new_object = super().transform(p_accidental)

			if (self.getParentIntervalList().getParentItem() != None):
				new_parent_item = self.findInParent().transform(p_accidental)
				new_object.setParentItem(new_parent_item[self.getParentIntervalList()[1].findInParent().getPosition()])

			return new_object

		def move(self, p_interval):
			new_chord = (self + p_interval).build(Chord, 1, p_args = self.getParentIntervalList().getAttributes())

			if (self.getPosition() != 1): 
				new_chord_start = self.getParentIntervalList().getitem_BL(slice(1, self.getPosition() - 1, None))
				if (new_chord_start.getitem_BL(len(new_chord_start.getIntervals())).getTone() != new_chord[1].getTone()): new_chord = new_chord_start + new_chord
				else: new_chord = new_chord_start
				
			if (self.getPosition() != len(self.getParentIntervalList().getIntervals())): 
				new_chord_end = self.getParentIntervalList().getitem_BL(slice(self.getPosition() + 1, len(self.getParentIntervalList().getIntervals()), None))
				if (new_chord_end[1].getTone() != new_chord.getitem_BL(len(new_chord.getIntervals())).getTone()): new_chord = new_chord + new_chord_end
				else: new_chord = new_chord.getitem_BL(slice(1, len(new_chord.getIntervals()) - 1, None)) + new_chord_end if len(new_chord.getIntervals()) > 1 else new_chord_end
				
			return new_chord

		def getMotionToClosestItem(self, p_next_chord):
			min_positive_distance = min([(tone.getTone() - self.getTone().getTone()).simplify() for tone in p_next_chord.getTones()])
			min_negative_distance = min([(self.getTone().getTone() - tone.getTone()).simplify() for tone in p_next_chord.getTones()])
			return [min_positive_distance, -min_negative_distance]