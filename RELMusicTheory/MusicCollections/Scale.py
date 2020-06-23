import re
import collections
import itertools
import statistics

from Configuration import *
from HelperMethods import *

from MusicCollections.IntervalList import *
from MusicCollections.IntervalListUtilities import *
from Components.IPitchedObject import * 
from IMusicObject import *

class Scale(IntervalList, IMusicObject):

	def __init__(self, p_item_1, p_item_2 = None, p_type_dict = {}):

		if isinstance(p_item_1, Scale): 
			self.tonic_tone = p_item_1[1].getTone()
			self.intervals = p_item_1.getIntervals()
			self.parent_item = p_item_1.getParentDegree()
			self.type_dict = p_type_dict 

		elif isinstance(p_item_1, list) and len(p_item_1) > 0 and isinstance(p_item_1[0], Tone): 
			self.tonic_tone = p_item_1[0]
			self.intervals = IntervalListUtilities.tonesToPitchClass(p_item_1)
			self.parent_item = None
			self.type_dict = p_type_dict

		elif isinstance(p_item_2, list) and len(p_item_2) > 0 and isinstance(p_item_2[0], Interval):
			self.tonic_tone = p_item_1.getTone() if isinstance(p_item_1, Scale.Degree) else p_item_1
			self.intervals = p_item_2
			self.parent_item = p_item_1 if isinstance(p_item_1, Scale.Degree) else None
			self.type_dict = p_type_dict
		
		elif isinstance(p_item_2, list) and len(p_item_2) > 0 and isinstance(p_item_2[0], int):
			self.tonic_tone = p_item_1.getTone() if isinstance(p_item_1, Scale.Degree) else p_item_1
			self.intervals = IntervalListUtilities.scaleStepsToPitchClass(p_item_2)
			self.parent_item = p_item_1 if isinstance(p_item_1, Scale.Degree) else None
			self.type_dict = p_type_dict

		elif isinstance(p_item_2, int):
			self.tonic_tone = p_item_1.getTone() if isinstance(p_item_1, Scale.Degree) else p_item_1
			self.intervals = IntervalListUtilities.decimalToPitchClass(p_item_2)
			self.parent_item = p_item_1 if isinstance(p_item_1, Scale.Degree) else None
			self.type_dict = p_type_dict

		else: print("Error: Cannot build Scale object with these parameters")

		self.buildComponents()

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

	def getName(self): return scale_names[IntervalListUtilities.pitchClassToDecimal([item.getInterval() for item in self.getIncludedDegrees()])]
	def getModeNames(self): return [(self + (item + 1)).getName() for item in range(len(self.getIntervals()))]

	#################
	# Sugar Methods #
	#################

	def getRelativeScale(self, p_experimental = True, p_reflection_point = 5):
		if (p_experimental and IntervalListUtilities.isDistinct(self.getIntervals()) and self.__contains__(p_reflection_point)): 
			parallel_scale = self.getParallelScale(True, p_reflection_point)
			relative_modes = [mode for mode in self.getModes() if mode.getIntervals() == parallel_scale.getIntervals()]
			if (len(relative_modes) > 0): return relative_modes[0]
			else: 
				print("Error: Scale has no reflection axis, relative Scale could not be found")
				return -1
		else: 
			if (self.__getitem__(1).buildPitchClass(2, 3) == [P1, m3]): return (self.sub(6))
			elif (self.__getitem__(1).buildPitchClass(2, 3) == [P1, M3]): return (self.add(6))		
			else: return self

	def getParallelScale(self, p_experimental = True, p_reflection_point = 5):
		if (p_experimental and IntervalListUtilities.isDistinct(self.getIntervals()) and self.__contains__(p_reflection_point)): 
			return self.getNegativeScale(p_reflection_point)[-p_reflection_point].buildScale()
		else: 
			if (self.__getitem__(1).buildPitchClass(2, 3) == [P1, m3]): return self.__getitem__(1).buildScaleWithIntervals((self.sub(6)).getIntervals())
			elif (self.__getitem__(1).buildPitchClass(2, 3) == [P1, M3]): return self.__getitem__(1).buildScaleWithIntervals((self.add(6)).getIntervals())
			else: return self

	def getNegativeScale(self, p_reflection_point = 5): 
		if (IntervalListUtilities.isDistinct(self.getIntervals()) and self.__contains__(p_reflection_point)): 
			new_reference_point = self.__getitem__(p_reflection_point).findInParent() if self.getParentDegree() is not None else self.__getitem__(p_reflection_point).getTone()
			new_scale = Scale(new_reference_point, IntervalListUtilities.scaleStepsToPitchClass(IntervalListUtilities.pitchClassToScaleSteps(self.__getitem__(p_reflection_point).getParentScale()[1].buildPitchClass())[::-1]))
			return new_scale
		else: 
			print("Error: Unable to get Negative of Scale")
			return -1

	def transpose(self, p_interval): return (self.add(p_interval))
	def rotate(self): return (self.transpose(2))
	def getModes(self): return [self + integer for integer in range(1, len(self.getIntervals()) + 1)]
	def getTonic(self): return self.__getitem__(1)

	###################
	# Wrapper Methods #
	###################

	def getParentScale(self): return self.getParentIntervalList()
	def getDegreeByInterval(self, p_interval): return self.getItemByInterval(p_interval)
	def getDegreeByNumeral(self, p_numeral): return self.getItemByNumeral(p_numeral)

	######################################################
	# Methods for ally calculating scale properties #
	######################################################

	def getHemitonia(self): return self.countIntervals(1)
	def getTritonia(self): return self.countIntervals(6)
	def getCardinality(self, p_system = DEFAULT_SYSTEM): return CARDINALITY[p_system][len(self.getDegrees())]
	def hasCohemitonia(self): return (len(self.getCohemitonic()) != 0)
	def isPrime(self): return (self.getPrimeMode() == self)

	def countIntervals(self, p_interval_size):

		try:
			counter = 0
			next_scale = self

			for i in range(len(self.getIntervals())):
				if (p_interval_size in next_scale.getSemitones()): counter = counter + 1
				next_scale = next_scale.rotate()

			if (p_interval_size == 6): counter = counter / 2
			return counter

		except: print("Error: Failed to count intervals for scale: " + str(self))

	def getImperfections(self):

		try:
			counter = 0

			for degree in self.getDegrees(): 
				if (P5 not in degree.buildPitchClass()): counter = counter + 1

			return counter

		except: print("Error: Failed to get imperfections for scale: " + str(self))
	
	def getRotationalSymmetry(self):

		try:
			parent_pitch_class = self.pitchClassToScaleSteps(self.getIntervals())
			result = []

			for degree in self.getDegrees():
				if (degree == self[1]): continue
				child_pitch_class = IntervalListUtilities.pitchClassToScaleSteps(degree.buildPitchClass())
				if (parent_pitch_class == child_pitch_class): result.append(degree.getPosition())

			return result

		except: print("Error: Failed to get rotational symmetry for scale: " + str(self))

	def getReflectionAxes(self):

		try:
			result = []

			for degree in self.getDegrees():
				scale_steps = IntervalListUtilities.pitchClassToScaleSteps(degree.buildPitchClass())
				if (scale_steps == scale_steps[::-1]): result.append(degree.getPosition())

			return result 

		except: print("Error: Failed to get reflection axes for scale: " + str(self))

	def getIntervalVector(self, p_system = DEFAULT_SYSTEM):

		try: 
			all_intervals = []
			for degree in self.getDegrees(): all_intervals = all_intervals + degree.buildPitchClass()[1:]
			all_pitch_classes = []

			for interval in all_intervals:
				semitones = interval.getSemitones()
				if (semitones > 11): semitones = semitones - 12
				all_pitch_classes.append(INTERVAL_SPECTRUM[p_system][semitones])

			counter = collections.Counter(all_pitch_classes)
			result = {}
			for key in counter.keys(): result[key] = int(counter[key]/2)
			return result

		except: print("Error: Failed to retrieve interval vector for scale: " + str(self))

	def isChiral(self, p_intervals):

		try:
			reflection_scale_steps = IntervalListUtilities.pitchClassToScaleSteps(p_intervals)[::-1]
			result = []

			for rotation_ammount in len(p_intervals):
				rotation_pitch_class = IntervalListUtilities.invertStatic(p_intervals, rotation_ammount + 1)
				rotation_scale_steps = IntervalListUtilities.pitchClassToScaleSteps(rotation_pitch_class)
				if (rotation_scale_steps == reflection_scale_steps): return False

			return True

		except: print("Error: Failed to check chirality for scale: " + str(self))

	def getCohemitonic(self, p_intervals):

		try:
			result = []
			scale_steps = IntervalListUtilities.pitchClassToScaleSteps(p_intervals) * 2

			for i in range(int(len(scale_steps) / 2)):
				if (scale_steps[i] == 1 and scale_steps[i + 1] == 1): result.append(i + 1)

			return result

		except: print("Error: Failed to retrieve cohemitonic tone")

	def getPrimeMode(self, p_consider_negative_modes = False):

		try: 
			min_count = 1000

			for degree in self.getDegrees():
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
				
			return prime_mode

		except: print("Error: Failed to get prime mode of scale: " + str(self))

	#################
	# Sugar Methods #
	#################

	def getIncludedDegrees(self): return [item for item in self.getDegrees() if not item.isOmitted()]
	def getDiatonicDegrees(self): return [item for item in self.getDegrees() if not item.isChromatic()]

	##############################
	# Overridable Business Logic #
	##############################

	def buildComponents(self):
		self.items = []

		for i in range(len(self.intervals)): 
			self.items.append(type(self).Degree(self.intervals[i], self, **self.type_dict[self.intervals[i]] if self.intervals[i] in self.type_dict.keys() else {}))

	def getAttributes(self):
		return {
			"p_type_dict": self.getTypeDict()
		}

	#######################
	# Getters and Setters #
	#######################
   
	def getDegrees(self): return self.items
	def getTonicTone(self): return self.tonic_tone
	def getParentDegree(self): return self.parent_item
	def getTypeDict(self): return self.type_dict
	
	class Degree(IntervalList.Item):
		
		def __init__(self, p_interval, p_parent_scale, p_chromatic = False, p_omitted = False):
			super().__init__(p_interval, p_parent_scale)
			self.chromatic = p_chromatic
			self.omitted = p_omitted

		def add_BL(self, p_other):
			if isinstance(p_other, int):	
				if abs(p_other) == 1: return self
				return self.next_BL().add_BL((p_other - 1) if not self.next_BL().isChromatic() else p_other) if p_other > 0 else self.previous_BL().add_BL((p_other + 1) if not self.previous_BL().isChromatic() else p_other)

			if isinstance(p_other, Interval):
				if abs(p_other) == P1: return self
				new_interval = self.getInterval() + p_other

				if new_interval < P1:
					return (self.getParentIntervalList().sub_BL(P8))[self.getPosition()] - (p_other - P8)
				
				if new_interval >= self.getParentIntervalList().getIntervals()[-1].roof():
					return (self.getParentIntervalList().add_BL(P8))[self.getPosition()] + (p_other - P8)

				if new_interval not in self.getParentIntervalList():
					return self.getParentIntervalList().addInterval(new_interval, {"p_chromatic": True}).getItemByInterval(new_interval)
				
				else: return self.getParentIntervalList().getItemByInterval(new_interval)
			else: return super().add_BL(p_other)
		
		################################
		# Methods concerned with names #
		################################

		def getName(self, p_system = DEFAULT_SYSTEM): return SCALE_DEGREE_NAMES[p_system][self.getInterval()]

		######################################################
		# Methods concerned with operations on scale degrees #
		######################################################

		def buildScale(self):
			new_scale = Scale(self, self.buildPitchClass())
			return new_scale

		def buildScaleWithIntervals_BL(self, p_intervals):
			new_scale = Scale(self, p_intervals)
			return new_scale

		###################
		# Wrapper Methods #
		###################

		def buildScaleWithIntervals(self, p_intervals): return self.buildScaleWithIntervals_BL(p_intervals)
		def getParentScale(self): return self.getParentIntervalList()

		#######################
		# Getters and Setters #
		#######################

		def isChromatic(self): return self.chromatic
		def isOmitted(self): return self.omitted
		