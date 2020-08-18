import re
import collections
import itertools
import statistics

from Configuration import *
from TheoryCollections.IntervalList import *
from TheoryCollections.IntervalListUtilities import *
from TheoryComponents.IPitchedObject import * 
from IMusicObject import *

class Scale(IntervalList, IMusicObject):

	def __init__(self, 
		p_item_1, 
		p_item_2 = None, 
		p_unaltered_intervals = [], 
		p_type_dict = {}, 
		p_sublist = False, 
		p_altered = True,
		p_fixed_invert = None):

		if issubclass(type(p_item_1), IntervalList):	
			self.tonic_tone = p_item_1.getItems()[0].getReferencePoint_BL()
			self.intervals = p_item_1.getIntervals()
			self.parent_item = p_item_1.getParentItem() if p_item_1.getParentItem() is not None else None
			self.type_dict = IntervalListUtilities.getUnalteredIntervalsTypeDict(self.intervals, p_item_1.getAttributes()["p_type_dict"] if p_type_dict == {} and type(self) == type(p_item_1) else p_type_dict)
			self.sublist = p_sublist
			self.altered = p_altered
			self.unaltered_intervals = IntervalListUtilities.deriveUnalteredIntervalsFromParent(self.parent_item) if self.sublist else IntervalListUtilities.getValidUnalteredIntervals(self.intervals, p_unaltered_intervals)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()

		elif isinstance(p_item_1, list) and len(p_item_1) > 0 and (isinstance(p_item_1[0], IPitchedObject) or isinstance(p_item_1[0], Tone)): 
			self.tonic_tone = Key(p_item_1[0], 4) if isinstance(p_item_1[0], Tone) else p_item_1[0]
			self.intervals = IntervalListUtilities.tonesToPitchClass(p_item_1)
			self.parent_item = None
			self.type_dict = p_type_dict
			self.sublist = p_sublist
			self.altered = p_altered
			self.unaltered_intervals = IntervalListUtilities.deriveUnalteredIntervalsFromParent(self.parent_item) if self.sublist else IntervalListUtilities.getValidUnalteredIntervals(self.intervals, p_unaltered_intervals)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()

		elif isinstance(p_item_2, list) and len(p_item_2) > 0 and isinstance(p_item_2[0], Interval):
			self.tonic_tone = p_item_1.getReferencePoint_BL() if isinstance(p_item_1, Scale.Degree) else (Key(p_item_1, 4) if isinstance(p_item_1, Tone) else p_item_1)
			self.intervals = p_item_2
			self.parent_item = self.configureParentItem(p_item_1, self.intervals) if isinstance(p_item_1, Scale.Degree) else None
			self.type_dict = p_type_dict
			self.sublist = p_sublist
			self.altered = p_altered
			self.unaltered_intervals = IntervalListUtilities.deriveUnalteredIntervalsFromParent(self.parent_item) if self.sublist else IntervalListUtilities.getValidUnalteredIntervals(self.intervals, p_unaltered_intervals)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()
		
		elif isinstance(p_item_2, list) and len(p_item_2) > 0 and isinstance(p_item_2[0], int):
			self.tonic_tone = p_item_1.getReferencePoint_BL() if isinstance(p_item_1, Scale.Degree) else (Key(p_item_1, 4) if isinstance(p_item_1, Tone) else p_item_1)
			self.intervals = IntervalListUtilities.scaleStepsToPitchClass(p_item_2)
			self.parent_item = self.configureParentItem(p_item_1, self.intervals) if isinstance(p_item_1, Scale.Degree) else None
			self.type_dict = p_type_dict
			self.sublist = p_sublist
			self.altered = p_altered
			self.unaltered_intervals = IntervalListUtilities.deriveUnalteredIntervalsFromParent(self.parent_item) if self.sublist else IntervalListUtilities.getValidUnalteredIntervals(self.intervals, p_unaltered_intervals)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()

		elif isinstance(p_item_2, int):
			self.tonic_tone = p_item_1.getReferencePoint_BL() if isinstance(p_item_1, Scale.Degree) else (Key(p_item_1, 4) if isinstance(p_item_1, Tone) else p_item_1)
			self.intervals = IntervalListUtilities.decimalToPitchClass(p_item_2)
			self.parent_item = self.configureParentItem(p_item_1, self.intervals) if isinstance(p_item_1, Scale.Degree) else None
			self.type_dict = p_type_dict
			self.sublist = p_sublist
			self.altered = p_altered
			self.unaltered_intervals = IntervalListUtilities.deriveUnalteredIntervalsFromParent(self.parent_item) if self.sublist else IntervalListUtilities.getValidUnalteredIntervals(self.intervals, p_unaltered_intervals)
			self.fixed_invert = p_fixed_invert if p_fixed_invert is not None and p_fixed_invert > self.intervals[-1] else self.intervals[-1].roof()

		else: print("Error: Cannot build Scale object with these parameters")

		self.buildItems()

	def str_BL(self):
		result = "<" + type(self).__name__ + " "
		#for item in self.getIncludedDegrees(): result += str(item) + ", "
		for item in self.getDegrees(): result += str(item) + ", "
		return result[:-2] + ">"

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

	def getName(self): 
		return scale_names[IntervalListUtilities.pitchClassToDecimal([item.getInterval() for item in self.getIncludedDegrees()])]

	def getModeNames(self): 
		return [(self.add_BL(item + 1)).getName() for item in range(len(self.getIntervals()))]

	#################
	# Sugar Methods #
	#################

	def getRelativeScale(self, p_experimental = True, p_reflection_point = 5):
		parallel_scale = self.getParallelScale(True, p_reflection_point)
		relative_modes = [mode for mode in self.getModes() if mode.getIntervals() == parallel_scale.getIntervals()]

		if (len(relative_modes) > 0): 
			return relative_modes[0]
		else: 
			print("Error: Scale has no reflection axis, relative Scale could not be found")
			return -1

	def getParallelScale(self, p_experimental = True, p_reflection_point = 5): 
		new_reference_point = self.getNegativeScale().getItems()[0].add_BL(-p_reflection_point)
		new_scale = new_reference_point.build_BL(type(self), p_ignore_parent = True, p_ignore_altered = False, p_preserve_parent = True, p_sublist = True)
		return new_scale

	def getNegativeScale(self, p_reflection_point = 5): 
		new_intervals = IntervalListUtilities.invertIntervals(self.getIntervals())

		if self.getParentItem() is not None:
			parent_interval_list = self.getParentItem().getParentIntervalList()
			new_reference_point = parent_interval_list.getParallelScale().getItems()[self.getParentItem().getPosition() - 1].add_BL(p_reflection_point)

		else: new_reference_point = self.getitem_BL(p_reflection_point).getReferencePoint_BL()	

		new_attributes = self.getAttributes()
		new_attributes["p_type_dict"] = IntervalListUtilities.intervalsToTypeDict(new_intervals)
		new_attributes["p_unaltered_intervals"] = IntervalListUtilities.invertIntervals(self.getUnalteredIntervals())
		new_scale = Scale(new_reference_point, new_intervals, **new_attributes)
		return new_scale
	'''
	def rotate(self, p_other = 2, p_ignore_parent = None, p_cascade_args = False, p_ignore_altered = True, p_remove_temp = True):
		new_reference_point = self.getItems()[0].add_BL(p_other, p_ignore_parent, p_cascade_args, p_ignore_altered, p_remove_temp)
		new_scale = new_reference_point.build_BL(type(self), -1, 2, p_ignore_parent = True, p_ignore_altered = False, p_preserve_parent = True)
		return new_scale
	'''
	def getModes(self): 
		return [self.rotate_BL(integer) for integer in range(1, len(self.getIntervals()) + 1)]

	def getTonic(self): 
		return self.getItems()[0]

	######################################################
	# Methods for ally calculating scale properties #
	######################################################

	def getHemitonia(self): 
		return self.countIntervals(1)
		
	def getTritonia(self): 
		return self.countIntervals(6)

	def getCardinality(self, p_system = DEFAULT_SYSTEM): 
		return CARDINALITY[p_system][len(self.getItems())]

	def hasCohemitonia(self): 
		return (len(self.getCohemitonic()) != 0)

	def isPrime(self): 
		return (self.getPrimeMode() == self)

	def countIntervals(self, p_interval_size):
		counter = 0
		next_scale = self

		for i in range(len(self.getIntervals())):
			if (p_interval_size in next_scale.getSemitones()): counter = counter + 1
			next_scale = next_scale.rotate()

		if (p_interval_size == 6): counter = counter / 2
		return counter

	def getImperfections(self):
		counter = 0

		for degree in self.getItems(): 
			if (P5 not in degree.buildPitchClass()): counter = counter + 1

		return counter
	
	def getRotationalSymmetry(self):
		parent_pitch_class = self.pitchClassToScaleSteps(self.getIntervals())
		result = []

		for degree in self.getItems():
			if (degree == self.getItems()[0]): continue
			child_pitch_class = IntervalListUtilities.pitchClassToScaleSteps(degree.buildPitchClass())
			if (parent_pitch_class == child_pitch_class): result.append(degree.getPosition())

		return result

	def getReflectionAxes(self):
		result = []

		for degree in self.getItems():
			scale_steps = IntervalListUtilities.pitchClassToScaleSteps(degree.buildPitchClass())
			if (scale_steps == scale_steps[::-1]): result.append(degree.getPosition())

		return result 

	def getIntervalVector(self, p_system = DEFAULT_SYSTEM):
		all_intervals = []
		for degree in self.getItems(): all_intervals = all_intervals + degree.buildPitchClass()[1:]
		all_pitch_classes = []

		for interval in all_intervals:
			semitones = interval.getSemitones()
			if (semitones > 11): semitones = semitones - 12
			all_pitch_classes.append(INTERVAL_SPECTRUM[p_system][semitones])

		counter = collections.Counter(all_pitch_classes)
		result = {}
		for key in counter.keys(): result[key] = int(counter[key]/2)
		return result

	def isChiral(self, p_intervals):
		reflection_scale_steps = IntervalListUtilities.pitchClassToScaleSteps(p_intervals)[::-1]
		result = []

		for rotation_ammount in len(p_intervals):
			rotation_pitch_class = IntervalListUtilities.invertStatic(p_intervals, rotation_ammount + 1)
			rotation_scale_steps = IntervalListUtilities.pitchClassToScaleSteps(rotation_pitch_class)
			if (rotation_scale_steps == reflection_scale_steps): return False

		return True

	def getCohemitonic(self, p_intervals):
		result = []
		scale_steps = IntervalListUtilities.pitchClassToScaleSteps(p_intervals) * 2

		for i in range(int(len(scale_steps) / 2)):
			if (scale_steps[i] == 1 and scale_steps[i + 1] == 1): result.append(i + 1)

		return result

	def getPrimeMode(self, p_consider_negative_modes = False):
		min_count = 1000

		for degree in self.getItems():
			new_scale = degree.buildScale()
			temp_sum = sum([item.getSemitones() for item in new_scale.getIntervals()])

			if (temp_sum < min_count):
				prime_mode = new_scale
				min_count = temp_sum
			
			if (p_consider_negative_modes):
				new_scale = new_scale.getNegative()
				temp_sum = sum([item.getSemitones() for item in new_scale.getIntervals()])

				if (temp_sum < min_count):
					prime_mode = new_scale
					min_count = temp_sum

	###################
	# Wrapper Methods #
	###################

	def getParentScale(self): 
		return self.getParentIntervalList_BL()

	def getDegreeByInterval(self, p_interval): 
		return self.getItemByInterval_BL(p_interval)

	def getDegreeByNumeral(self, p_numeral): 
		return self.getItemByNumeral_BL(p_numeral)

	def getDegrees(self): 
		return self.getItems()

	def getParentDegree(self): 
		return self.getParentItem()

	def setDegrees(self, p_degrees):
		self.setItems(p_degrees)

	def setParentDegree(self, p_parent_degree):
		self.setItems(p_parent_degree)

	#################
	# Sugar Methods #
	#################

	def getIncludedDegrees(self): 
		return [item for item in self.getItems() if not item.isOmitted()]

	def getDiatonicDegrees(self): 
		return [item for item in self.getItems() if not item.isChromatic()]

	##############################
	# Overridable Business Logic #
	##############################

	def buildItems(self):
		self.items = []

		for i in range(len(self.intervals)): 
			self.items.append(type(self).Degree(self.intervals[i], self, **self.type_dict[self.intervals[i]] if self.intervals[i] in self.type_dict.keys() else {}))
	
	class Degree(IntervalList.Item):
		
		################################
		# Methods concerned with names #
		################################

		def getName(self, p_system = DEFAULT_SYSTEM): 
			return SCALE_DEGREE_NAMES[p_system][self.getInterval()]

		######################################################
		# Methods concerned with operations on scale degrees #
		######################################################

		def buildScale_BL(self):
			new_scale = self.build_BL(Scale)
			return new_scale

		def buildScaleWithIntervals_BL(self, p_intervals):
			new_scale = Scale(self, p_intervals)
			return new_scale

		###################
		# Wrapper Methods #
		###################

		def isChromatic(self): 
			return self.isAltered()

		def buildScale(self):
			return self.buildScale_BL()

		def buildScaleWithIntervals(self, p_intervals): 
			return self.buildScaleWithIntervals_BL(p_intervals)

		def getParentScale(self): 
			return self.getParentIntervalList()
		