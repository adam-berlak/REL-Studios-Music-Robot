import itertools

from TheoryCollections.Scale import *
from TheoryCollections.IntervalList import *
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
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()
			self.bass_triad_quality = IntervalListUtilities.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Bass Triad Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_bass_triad_quality
			self.extensions_quality = IntervalListUtilities.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Extensions Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_extensions_quality
			self.parent_item = self.configureParentItem(p_item_1.getItems()[0], self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getReferencePoint_BL()
			self.root = p_root if p_root is not None else self.parent_item.add_BL(IntervalListUtilities.findRoot(self.intervals))
		
		elif isinstance(p_item_1, list) and len(p_item_1) > 0 and (isinstance(p_item_1[0], IPitchedObject) or isinstance(p_item_1[0], Tone)):
			self.intervals = [item - p_item_1[0] for item in p_item_1]	
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()
			self.bass_triad_quality = IntervalListUtilities.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Bass Triad Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_bass_triad_quality
			self.extensions_quality = IntervalListUtilities.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Extensions Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_extensions_quality
			self.parent_item = self.configureParentItem(Scale(p_item_1, IntervalListUtilities.identifyParentScale(self.bass_triad_quality, self.extensions_quality)).getItems()[0], self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getReferencePoint_BL()
			self.root = p_root if p_root is not None else self.parent_item.add_BL(IntervalListUtilities.findRoot(self.intervals))
		
		elif isinstance(p_item_1, Scale.Degree) and isinstance(p_item_2, list) and len(p_item_2) > 0 and (isinstance(p_item_2[0], int) or isinstance(p_item_2[0], Interval)):
			self.intervals = p_item_2 
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()
			self.bass_triad_quality = IntervalListUtilities.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Bass Triad Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_bass_triad_quality
			self.extensions_quality = IntervalListUtilities.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Extensions Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_extensions_quality
			self.parent_item = self.configureParentItem(p_item_1, self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getReferencePoint_BL()
			self.root = p_root if p_root is not None else self.parent_item.add_BL(IntervalListUtilities.findRoot(self.intervals))

		elif isinstance(p_item_1, IPitchedObject) and isinstance(p_item_2, list) and len(p_item_2) > 0 and (isinstance(p_item_2[0], int) or isinstance(p_item_2[0], Interval)):
			self.intervals = p_item_2 	
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()
			self.bass_triad_quality = IntervalListUtilities.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Bass Triad Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_bass_triad_quality
			self.extensions_quality = IntervalListUtilities.intervalsToQuality(IntervalListUtilities.getParentChordStatic(self.intervals))["Extensions Quality"][2] if (p_bass_triad_quality is None or p_extensions_quality is None) else p_extensions_quality
			self.parent_item = self.configureParentItem(Scale(p_item_1, IntervalListUtilities.identifyParentScale(self.bass_triad_quality, self.extensions_quality)).getItems()[0], self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getReferencePoint_BL()
			self.root = p_root if p_root is not None else self.parent_item.add_BL(IntervalListUtilities.findRoot(self.intervals))
		
		elif isinstance(p_item_1, IPitchedObject) and isinstance(p_item_2, str):
			self.intervals = IntervalListUtilities.stringToPitchClass(p_item_2)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()
			self.bass_triad_quality = IntervalListUtilities.stringQualityToData(p_item_2)["Bass Triad Quality"]
			self.extensions_quality = IntervalListUtilities.stringQualityToData(p_item_2)["Extensions Quality"]
			self.parent_item = self.configureParentItem(Scale(p_item_1, IntervalListUtilities.identifyParentScale(self.bass_triad_quality, self.extensions_quality)).getItems()[0], self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getReferencePoint_BL()
			self.root = self.parent_item

		elif isinstance(p_item_1, Scale.Item) and isinstance(p_item_2, str):
			self.intervals = IntervalListUtilities.stringToPitchClass(p_item_2)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()
			self.bass_triad_quality = IntervalListUtilities.stringQualityToData(p_item_2)["Bass Triad Quality"]
			self.extensions_quality = IntervalListUtilities.stringQualityToData(p_item_2)["Extensions Quality"]
			self.parent_item = self.configureParentItem(p_item_1, self.intervals, p_modulate_parent)
			self.tonic_tone = self.parent_item.getReferencePoint_BL()
			self.root = self.parent_item
	
		else: 
			print("Error: Cannot build Chord object with these Parameters")
			return

		self.buildItems()

	#####################################
	# Methods concerning class behavior #
	#####################################

	def __getitem__(self, p_index): 
		if isinstance(p_index, tuple):
			items = [self.getItems()[0].__add__(item) for item in p_index]
			result = items[0]

			for item in items[1:]:
				result = result.add_BL(item)

			return result
		
		elif isinstance(p_index, int): 
			return self.getItems()[0].__add__(p_index)

		else: return super().__getitem__(p_index)

	##############
	# Arithmetic #
	##############

	def __add__(self, p_other):
		if (isinstance(p_other, int)): 
			return (self.getParentItem().add_BL(p_other)).build(Chord, self.getNumerals())

		if (isinstance(p_other, Interval)): 
			return (self.getParentItem().add_BL(p_other)).build(Chord, self.getIntervals())

		else: return super().add_BL(p_other)

	def __sub__(self, p_other):
		if (isinstance(p_other, Interval)): 
			self.__add__(-p_other)

		if (isinstance(p_other, int)): 
			self.__add__(-p_other)	
			
		else: return super().sub_BL(p_other)
	
	def __radd__(self, p_other):
		if (isinstance(p_other, str)): 
			return p_other + str(self)

	###########################
	# Playable Object Methods #
	###########################

	def __play__(self):
		return

	def __toMidiData__(self): 
		try: return self.getItems()
		except: print("Error: Unable to convert object to midi data as it does not contain playable objects")
		
	################################
	# Methods concerned with names #
	################################

	def getParentChordQualityData(self, p_system = DEFAULT_SYSTEM):
		return IntervalListUtilities.intervalsToQuality(self.getParentChord().getIntervals(), self.getBassTriadQuality(), self.getExtensionsQuality(), p_system)

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

	def getNumeral(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):
		return self.getRoot().getNumeral() + self.getParentChordQuality(p_style, p_system) if p_with_quality else self.getRoot().getNumeral()

	def getNumeralWithContext(self, p_with_quality = False, p_style = 2, p_system = DEFAULT_SYSTEM):
		secondary_information = "\\" + self.getParentIntervalList().getParentItem().build(Chord).getNumeral() if self.getParentIntervalList().getParentItem() is not None else ""
		return self.getNumeral(p_with_quality, p_style, p_system) + secondary_information

	def getFiguredBass(self, p_slice = -1): 
		return self.getParentChord().getNumeral(False) + " " + self.pitchClassToFiguredBass(p_slice)

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
		new_chord = parallel_scale.getitem_BL(self.getItems()[0].getPositionInParent()).build(Chord, self.getNumerals())
		return new_chord

	def getRelativeChord(self, p_reflection_point = 5):
		relative_scale = self.getParentIntervalList().getRelativeScale(p_reflection_point)
		new_chord = relative_scale.getitem_BL(self.getItems()[0].getPositionInParent()).build(Chord, self.getNumerals())
		return new_chord

	def getNegativeChord(self, p_reflection_point = 5):
		parent_chord = self.getRootPosition().buildOnThirds()
		generic_intervals_inverted = [item.getNumeral() for item in IntervalListUtilities.scaleStepsToPitchClass(IntervalListUtilities.pitchClassToScaleSteps(self.getIntervals())[:-1][::-1] + [1])]
		root = self.getParentIntervalList().getNegativeScale(p_reflection_point)[-parent_chord.getItems()[0].getPositionInParent()] - ((2 * self.getInversion()) + 1) - generic_intervals_inverted[-1]
		new_chord = root.build(Chord, generic_intervals_inverted)
		return new_chord

	########################
	# Common Functionality #
	########################

	def resolveChord(self, p_system = DEFAULT_SYSTEM):
		return self.resolveChordInto((self.getRootPosition().buildOnThirds() + RESOLUTION_SYSTEM[p_system]).getitem_BL(slice(1, 4, None)))

	def resolveChordInto(self, p_next_chord, p_system = DEFAULT_SYSTEM):
		resolution_list = []

		for item in self.getItems():
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
			temp_chord_count = IntervalListUtilities.getItemRepetitionCount(chord.getIntervals())
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
				new_scale = Scale(self.getItems()[0].getReferencePoint_BL(), IntervalListUtilities.decimalToPitchClass(i))

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
			result = len(self.getParts()) - ([item for item in self.getItems() if item.getReferencePoint_BL().getTone() == self.getRoot().getReferencePoint_BL().getTone()][0].getPosition() - 1)
			return result if result != len(self.getItems()) else 0

		else: 
			print("Failed to retrieve inversion of Chord as the Chord is rootless")
			return 0

	def isRootless(self):
		return not self.getRoot().getReferencePoint_BL().getTone() in [item.getTone() for item in self.getReferencePoints_BL()]

	def getRootPosition(self):
		new_chord = self.invert(-self.getInversion())
		return new_chord

	def getSecondaryDominant(self):
		new_root = (self.getParentItem().buildScale().getItems()[0].add_BL(5))
		new_chord = new_root.build(Chord, [P1, M3, P5, m7], p_args = {"p_root": new_root, "p_bass_triad_quality": "dom", "p_extensions_quality": "dom", "p_modulate_parent": True})
		return new_chord

	def getSecondarySubDominant(self):
		new_root = (self.getParentItem().buildScale().getItems()[0].add_BL(2))
		new_chord = new_root.build(Chord, [1, 3, 5, 7], p_args = {"p_root": new_root})
		return new_chord

	def getSecondaryTonic(self):
		new_root = (self.getParentItem().buildScale().getItems()[0].add_BL(1))
		new_chord = new_root.build(Chord, [1, 3, 5], p_args = {"p_root": new_root})
		return new_chord

	def getSecondaryNeopolitan(self):
		new_chord.getSecondarySubDominant().getItems()[0].transform(-1)
		return new_chord

	def getSecondaryAugmentedSix(self):
		new_chord = self.getSecondaryDominant().getSecondaryTritoneSubstitution()
		return new_chord

	def getSecondaryTritoneSubstitution(self):
		new_chord = self.getSecondaryDominant().getitem_BL(3).transform(-1)
		return new_chord

	#################
	# Sugar Methods #
	#################

	def getAllInversions(self):
		return [self.invert(item) for item in range(len(self.getIntervals()))]

	def buildOnThirds(self):
		new_intervals = [item for item in IntervalListUtilities.rearrangeIntervalsAsThirds(self.getIntervals()) if item != None]
		new_chord = Chord(self.getParentItem(), new_intervals, **self.getAttributes())
		return new_chord

	def simplify(self):
		new_intervals = IntervalListUtilities.simplify(self.getIntervals())
		new_chord = Chord(self.getParentItem(), new_intervals, **self.getAttributes())
		return new_chord

	def next(self):
		new_chord = (self.getItems()[0].next()).build(Chord, self.getNumerals(), p_args = {"p_root": self.getRoot().__add__(1)})
		return new_chord

	def previous(self):
		new_chord = (self.getItems()[0].previous()).build(Chord, self.getNumerals(), p_args = {"p_root": self.getRoot().__sub__(1)})
		return new_chord

	##############################
	# Overridable Business Logic #
	##############################

	def buildItems(self):
		self.items = []
		
		for i in range(len(self.intervals)): 
			self.items.append(type(self).Part(self.intervals[i], self))

	def getAttributes(self):
		return {
			"p_type_dict": self.getTypeDict(),
			"p_root": self.getRoot(),
			"p_bass_triad_quality": self.getBassTriadQuality(),
			"p_extensions_quality": self.getExtensionsQuality()
		}

	#################
	# Configuration #
	#################

	def setParentItem(self, p_item): 
		if p_item == None: return
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

	###################
	# Wrapper Methods #
	###################

	def getParts(self): 
		return self.getItems()

	def getParentDegree(self): 
		return self.getParentItem()

	def setParts(self, p_parts):
		self.setItems(p_parts)

	def setParentDegree(self, p_parent_item):
		self.setParentItem(p_parent_item)

	def getParentScale(self): 
		return self.getParentIntervalList_BL()

	def getPartByInterval(self, p_interval): 
		return self.getItemByInterval_BL(p_interval)

	def getPartByNumeral(self, p_numeral): 
		return self.getItemByNumeral_BL(p_numeral)
    
	#######################
	# Getters and Setters #
	#######################

	def getFixedInvert(self): return self.fixed_invert
	def getRoot(self): return self.root
	def getBassTriadQuality(self): return self.bass_triad_quality
	def getExtensionsQuality(self): return self.extensions_quality

	class Part(IntervalList.Item):

		def __init__(self, p_interval, p_parent_scale, p_position_in_parent_voice = None, p_parent_voice = None):
			super().__init__(p_interval, p_parent_scale)
			self.position_in_parent_voice = p_position_in_parent_voice
			self.parent_voice = p_parent_voice

		#################
		# Voice Methods #
		#################

		def resolveVoice(self):
			new_part = self.nextInVoice()
			if new_part is None: return
			return new_part if new_part.getReferencePoint() != self.getReferencePoint() else new_part.nextInVoice()

		def nextInVoice(self):
			new_index = self.getPositionInParentVoice() + 1

			if new_index >= len(self.getParentVoice().getParts()):
				print("Error: No subsequent part found")
				return None

			new_part = self.getParentVoice().getParts(new_index)
			return new_index

		##############################
		# Overridden Wrapper Methods #
		##############################

		def __getattr__(self, p_attr):
			return getattr(self.findInParent(), p_attr)
		
		def __add__(self, p_other):
			if isinstance(p_other, int):
				if abs(p_other) == 1: return self
				new_interval = (self.findInParent().add_BL(p_other)).sub_BL(self.getParentIntervalList().getItems()[0].findInParent())

				if new_interval not in self.getParentIntervalList().getIntervals(): 
					return self.getParentIntervalList().addInterval(new_interval).getItemByInterval(new_interval if new_interval >= P1 else P1)

				else: return self.getParentIntervalList().getItemByInterval(new_interval)

			if isinstance(p_other, Interval):
				if abs(p_other) == P1: return self
				new_interval = self.getInterval() + p_other

				if new_interval not in self.getParentIntervalList().getIntervals():
					return self.getParentIntervalList().addInterval(new_interval).getItemByInterval(new_interval if new_interval >= P1 else P1)
				
				else: return self.getParentIntervalList().getItemByInterval(new_interval)
			else: return super().add_BL(p_other)

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

		###################
		# Wrapper Methods #
		###################

		def getParentChord(self): 
			return self.getParentIntervalList()

		###############
		# New Methods #
		###############

		def isNonHarmonic(self):
			return self.findInParentChord().getInterval().getNumeral() > 7

		def findInParentChord(self):
			temp_delta_to_root = self.getParentIntervalList().getRoot().sub_BL(self.getParentIntervalList().getParentItem())
			temp_intervals = IntervalListUtilities.scaleIntervalsByOrder([temp_delta_to_root, self.getInterval()])
			temp_intervals = IntervalListUtilities.normalizeIntervals(temp_intervals)
			temp_intervals = IntervalListUtilities.buildOnThirdsStatic(temp_intervals)
			return self.getParentIntervalList().getParentChord().getItems()[0].add_BL(temp_intervals[-1])

		def move(self, p_interval):
			new_chord = (self.__add__(p_interval)).build(Chord, 1, p_args = self.getParentIntervalList().getAttributes())

			if (self.getPosition() != 1): 
				new_chord_start = self.getParentIntervalList().getitem_BL(slice(1, self.getPosition() - 1, None))
				if (new_chord_start.getitem_BL(len(new_chord_start.getIntervals())).getReferencePoint_BL() != new_chord.getItems()[0].getReferencePoint_BL()): new_chord = new_chord_start.add_BL(new_chord)
				else: new_chord = new_chord_start
				
			if (self.getPosition() != len(self.getParentIntervalList().getIntervals())): 
				new_chord_end = self.getParentIntervalList().getitem_BL(slice(self.getPosition() + 1, len(self.getParentIntervalList().getIntervals()), None))
				if (new_chord_end.getItems()[0].getReferencePoint_BL() != new_chord.getitem_BL(len(new_chord.getIntervals())).getReferencePoint_BL()): new_chord = new_chord.add_BL(new_chord_end)
				else: new_chord = new_chord.getitem_BL(slice(1, len(new_chord.getIntervals()) - 1, None)).add_BL(new_chord_end) if len(new_chord.getIntervals()) > 1 else new_chord_end
				
			return new_chord

		def getMotionToClosestItem(self, p_next_chord):
			min_positive_distance = min([(tone.getTone() - self.getReferencePoint_BL().getTone()).simplify() for tone in p_next_chord.getReferencePoints_BL()])
			min_negative_distance = min([(self.getReferencePoint_BL().getTone() - tone.getTone()).simplify() for tone in p_next_chord.getReferencePoints_BL()])
			return [min_positive_distance, -min_negative_distance]

		#######################
		# Getters and Setters #
		#######################

		def getPositionInParentVoice(self): return self.parent_voice
		def getParentVoice(self): return self.parent_voice

		def setParentVoice(self, p_position_in_parent_voice, p_parent_voice):
			self.position_in_parent_voice = p_position_in_parent_voice
			self.parent_voice = p_parent_voice