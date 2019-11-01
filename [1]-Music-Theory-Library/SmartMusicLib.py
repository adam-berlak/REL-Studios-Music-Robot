import random
import sys

# Constants

# Configuration
System = "western"

# Class Name: Interval
# Parameters: p_semitones (Number of Semitones in interval), p_numeral (numeral representation), p_accidental (sharp/flat)
class Interval:
	def __init__(self, p_semitones, p_numeral, p_accidental=""):
		self.semitones = p_semitones
		self.numeral = p_numeral
		self.accidental = p_accidental
	def __str__(self):
		return str(self.getNumeral()) + self.getAccidental()
	def __eq__(self, p_other):
		return self.getSemitones() == p_other.getSemitones()
		
	def setSemitones(self, p_semitones):
		self.semitones = p_semitones
	def setNumeral(self, p_numeral):
		self.numeral = p_numeral
	def setAccidental(self, p_accidental):
		self.accidental = p_accidental
	def setAccidental(self, p_accidental):
		self.accidental = p_accidental
		
	def getSemitones(self):
		return self.semitones
	def getNumeral(self):
		return self.numeral
	def getAccidental(self):
		return self.accidental
	def getAccidental(self):
		return self.accidental

# Internal Class Name: Scale
# Parameters: p_tonic_note (The tonic note the scale will be built off of), p_intervals (the interval pattern of the scale)
# Info: A scale object requires a tonic tone and an interval pattern
# Method getDegree: Retrieves the nth degree in the scale
# Method getDegreeByInterval: Retrieves the degree that is a certain interval from the tonic
class Scale:
	def __init__(self, p_tonic_note, p_intervals):
		self.tonic_note = p_tonic_note
		self.intervals = p_intervals
		self.degrees = []
        
		for i in range(len(p_intervals)):
			self.degrees.append(_Degree(self.intervals[i], self))

		for degree in self.getDegrees():
			note = (TONES.get(System)*2)[TONES.get(System).index(self.getTonicNote()) + degree.distanceFromClosest(self.getDegree(1))]
			degree.setNote(note)
		
		self.setParentDegree = None
	def __str__(self):
		result = "[ "
		for degree in self.getDegrees():
			result = result + degree.__str__() + " "
		return result + "]"
	def __eq__(self, p_other):
		return (self.getIntervals() == p_other.getIntervals()) and (self.getTonicNote() == p_other.getTonicNote())
	def __getitem__(self, p_index):
		return self.getDegrees()[p_index - 1]
	
	def getDegree(self, p_index):
		return self.getDegrees()[p_index - 1]		
	def getDegreeByInterval(self, p_interval):
		for degree in self.getDegrees():
			if (degree.getInterval() == p_interval):
				return degree
			return None
   
	def getIntervals(self):
		return self.intervals
	def getDegrees(self):
		return self.degrees
	def getTonicNote(self):
		return self.tonic_note
	def getParentDegree(self):
		return self.parent_degree

	def setIntervals(self, p_intervals):
		self.intervals = p_intervals
	def setDegrees(self, p_degrees):
		self.degrees = p_degrees
	def setTonicNote(self, p_tonic_note):
		self.tonic_note = p_tonic_note
	def setParentDegree(self, p_parent_degree):
		self.parent_degree = p_parent_degree
			
# Internal Class Name: _Degree
# Parameters: p_interval (Interval associated with the degree), p_parent_scale (scale associated with scale degree)
# Info: The degree object is part of the scale object, you cannot create a scale degree without a scale
# Method distanceFromClosest: Finds the smallest distance from this degree note to another degree note within the scale
# Method distanceFromNext: Finds the distance to the next repetition of a scale degree note
# Method buildChord: Builds and returns a chord on the current scale degree givin a number of notes and the leap between each note in the chord
# Method buildScale: Builds and returns a scale on the current scale degree based off the parent scale
# Method buildScaleWithIntervals: Builds and returns a scale on the current scale degree based off an scale parameter		
class _Degree:
	def __init__(self, p_interval, p_parent_scale):
		self.interval = p_interval
		self.parent_scale = p_parent_scale
	def __eq__(self, p_other):
		return (self.getInterval() == p_other.getInterval()) and (self.getNote() == p_other.getNote())
	def __str__(self):
		return self.getNote()
	def __add__(self, p_other):
		return (self.getParentScale().getDegrees()*2)[self.getParentScale().getDegrees().index(self) + p_other]

	def distanceFromClosest(self, p_other):
		return abs(self.getInterval().getSemitones() - p_other.getInterval().getSemitones())
	def distanceFromNext(self, p_other):
		result = self.getInterval().getSemitones() - p_other.getInterval().getSemitones()
		while (result > 0):
			result -= 12
		return abs(result)

	def buildChord(self, p_num_notes = 4, p_leap_size = 2):
		parent_degrees = self.getParentScale().getIntervals() * 3
		chord_intervals = [P1]
		i = parent_degrees.index(self) + p_leap_size
		while (i < 24):
			chord_intervals.append(Intervals[self.distanceFromNext(parent_degrees[i])])
			i = i + p_leap_size
		child_chord = Chord(chord_intervals)
		child_chord.setParentDegree(self)
		return child_chord
	def buildScale(self):
		parent_degrees = self.getParentScale().getDegrees() * 2
		child_intervals = [P1]
		i = parent_degrees.index(self) + 1
		while (parent_degrees[i] != self):
			child_intervals.append(Intervals[self.distanceFromNext(parent_degrees[i])])
			i = i + 1
		child_scale = Scale(self.getNote(), child_intervals)
		# child_scale.setParentDegree(self)
		return child_scale
	def buildScaleWithIntervals(self, p_intervals):
		new_scale = Scale(self.getNote(), p_intervals)
		new_scale.setParentDegree(self)
		return new_scale
	
	def getNote(self):
		return self.note
	def getInterval(self):
		return self.interval
	def getParentScale(self):
		return self.parent_scale

	def setNote(self, p_note):
		self.note = p_note
	def setInterval(self, p_interval):
		self.interval = p_interval
	def setParentScale(self, p_parent_scale):
		self.parent_scale = p_parent_scale

def circleOfFifths(p_chord):
	return p_chord + 5
def circleOfFourths(p_chord):
	return p_chord + 4

class Chord:
	def __init__(self, p_intervals):
		self.intervals = p_intervals
	def __add__(self, p_other):
		return self.getParentDegree().__add__(p_other).buildChord()
		
	def resolveChord(self, p_voice_leading_rules = circleOfFifths):
		return p_voice_leading_rules(self)
	def getRelativeChord(self):
		return self - 2
	# def transformChordTo(self, p_intervals):
	# def getParallelChord(self):

	def getIntervals(self):
		return self.intervals
	def getParentDegree(self):
		return self.parent_degree

	def setIntervals(self, p_intervals):
		self.intervals = p_intervals
	def setParentDegree(self, p_degree):
		self.parent_degree = p_parent_degree

def main():
	print("Hello World")

if __name__ == "__main__":
	main()

# Intervals
P1 = Interval(0, 1)
P4 = Interval(5, 4)
P5 = Interval(7, 5)
P8 = Interval(12, 8)
P11 = Interval(17, 11)
P12 = Interval(19, 12)
P15 = Interval(24, 15)

m2 = Interval(1, 2, "b")
m3 = Interval(3, 3, "b")
m6 = Interval(8, 6, "b")
m7 = Interval(10, 7, "b")
m9 = Interval(13, 9, "b")
m10 = Interval(15, 10, "b")
m13 = Interval(20, 13, "b")
m14 = Interval(22, 14, "b")

M2 = Interval(2, 2)
M3 = Interval(4, 3)
M6 = Interval(9, 6)
M7 = Interval(11, 7)
M9 = Interval(14, 9)
M10 = Interval(16, 10)
M13 = Interval(21, 13)
M14 = Interval(23, 14)

aug4 = Interval(6, 4, "#")
aug11 = Interval(18, 11, "#")

Intervals = [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7, P8, m9, M9, m10, M10, P11, aug11, P12, m13, M13, m14, M14, P15]

# Heptatonic Scales
major = [P1, M2, M3, P4, P5, M6, M7]
minor = [P1, M2, m3, P4, P5, m6, m7]
melodicMinor = [P1, M2, m3, P4, P5, M6, m7]
harmonicMinor = [P1, M2, m3, P4, P5, m6, M7]

# Tonal Systems
TONES = {
    "western": ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
}

# Testing
CMajorScale = Scale("C#", harmonicMinor)
print(CMajorScale)
DDorianScale = CMajorScale[2].buildScale()
# CMajorScale.setParentDegree("E")
# G7 = DDorianScale.getDegree(4).buildChord()
# CM7 = G7.resolveChord()