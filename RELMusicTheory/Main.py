# TODO:
# COMPLETED: Support #/b notes and assign accidentals correctly
# COMPLETED: Print Roman Numerals
# COMPLETED: Support Non-heptatonic Scales
# COMPLETED: Find solution to multiplying scale for chords to support degrees of > 12 Semitone intervals :: Solution: Chord inherits from scale, it is a scale object but has additional methods like resolve etc. but it also has its own degrees
# COMPLETED: fix building chords with skips greater or less than three
# COMPLETED: Fix notation for non-triadic chords
# COMPLETED: Fix Numeral Addition
# COMPLETED: Remove reliance on Interval objects, instead use semitones as is, interval objects only required for printing and interfacing
# COMPLETED: Automate creation of Interval objects within Scale so that it is always accurate, and have a fixed amount of intervals available for interfacing
# COMPLETED: Add support for subtraction, find better way of looping through degrees IE cycle
# COMPLETED: Fix arithmetic with degrees such that adding a generic interval includes the principle degree, IE C + 3 = E as opposed to F
# COMPLETED: Fix stringToPitchClass
# COMPLETED: Move unaltered_intervals dictionary into constants
# COMPLETED: Add support for stringToInterval in interval class
# COMPLETED: Using buildWithIntervals method should change the parent scale of the resulting scale object if it includes intervals not in the parent, but only if the scale object is a chord
# COMPLETED: Fix Degree addition problem
# COMPLETED: Add support for sus chords in stringToPitchClass method
# COMPLETED: Create a Scale.Dictionary.py file for holding thousands of Scale definitions
# COMPLETED: Create simplify method for Tone and change minimize to simplify in Interval
# COMPLETED: Add full support for sub for Tone class
# COMPLETED: Fix [Interval] in Scale method. It should check each rotation of the Scale
# COMPLETED: Add support for buildWithGenericIntervals
# COMPLETED: If you call a super method in chord, and that super method uses a method thats overridden super is ineffective (Check if class is a subclass)
# COMPLETED: If you build a chord on a Scale Degree that contains Tones not in the principle degree, they should ONLY be added if parent scale degree are not distinct, otherwise they should be transformed
# COMPLETED: All Degree objects should have a parent degree when a parent degree is established for the Root Degree *Added findInParent method*
# COMPLETED: Simplify invert method
# COMPLETED: Created getParallelChord() and transformChordTo() methods
# COMPLETED: Adding a specific interval to a scale degree should not add a new interval to the scale unless it is not distinct
# COMPLETED: Fixed getSecondaryDominant()
# COMPLETED: Get Numeral should return only the numeral
# COMPLETED: getFirstInversion() is not consistant *Checks if duplicates of same number of Nones are found, in which case we just return self*

# LONG-TERM GOAL: Create and fix issues in UnitTest
# LONG-TERM GOAL: Add try-catch statements of invalid inputs 

# NEW FEATURES: Should be able to get a version of an interval with minimal accidentals IE: bb4 = b3
# NEW FEATURES: Change name for the Tone class within the Keyboard object to Key, allow it to play sounds
# NEW FEATURES: Get parallel key of scale
# NEW FEATURES: Get Negative Harmony of a Chord
# NEW FEATURES: Add support for chord inversions and sus notes in printQuality()
# NEW FEATURES: Support voice leading rules in configuration

# BUGS TO FIX: In Chord, for all methods that access parentDegree perfom a check
# BUGS TO FIX: Add limitations on getFirstInversion() and getInversion() so that it doesnt loop forever
# BUGS TO FIX: Fix sub and addition
# BUGS TO FIX: Remove hardcoded chord quality names from Chord class
# BUGS TO FIX: If you build a Chord on a Chord degree with specific intervals how does it behave
# BUGS TO FIX: Check if sub-setting Chords and rotating/added maintains the parent degree
# BUGS TO FIX: Diminished and Augmented chords arent neccissarily built on Thirds so I need to find a new way to identify qualities
# BUGS TO FIX: Retrieving numeral relative to parent should go down the chain of all parents

import random
import sys

from Scale import *
from Chord import *
from Configuration import *

def main():

	print(Chord(C, [P1, M3, M7]).getQuality())

	print(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 8))

	print(Scale(C, [2, 2, 1, 2, 2, 2, 1]).getModeNames())

	# Create a C Major Scale
	CMajorScale = Scale(C, Scale.decimalToPitchClass(major))

	print("Got Here" + CMajorScale[1].build(Chord).getSecondaryAugmentedSix())

	print(Chord(C, [P1, m3, P5, m7])[2])

	print(CMajorScale.printTones())

	print(Scale.scaleIntervalsByOrder([P1, M3, P5, M7, M2, P4, m6]))

	print(CMajorScale[2].buildScale()[2].findInParent().getInterval())

	print(Scale(C, Scale.decimalToPitchClass(diminished_seventh)))

	print((CMajorScale[1].build(Chord)[1] + m3).getParentScale().getParentScale())
	
	CChromaticScale = Scale(G, [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7])

	print(CMajorScale[7] + CChromaticScale[3])

	print("result: " + Chord(C, [P1, M3, P5, M7])[2].build(Chord).getParentScale())

	Dorian = CMajorScale + 2
	print(CMajorScale[7].build(Chord).getSecondaryDominant())
	
	CM7 = CMajorScale[1].buildWithIntervals(Chord, [P1, M3, aug5, m7, m9, P11])
	print(CM7.getParentChordQuality())
	
	print(Scale(B, Scale.scaleStepsToPitchClass([2, 2, 1, 2, 2, 2, 1])))

	print(Tone("G", 3).simplify())

	print(Scale(C, [P1, m2, m3, M3, aug4, P5, M6, m7]).getModeNames())
	
	Eb = CMajorScale[1] + m3
	print("The first degree of the C Major Scale + m3 is: " + Eb)

	print("The major scale converted to Decimal is: " + str(Scale.pitchClassToDecimal([P1, M2, M3, P4, P5, M6, M7])))

	print("The string dom7sus9no5b5 produces the pitch class " + str(Chord.stringToPitchClass("dom7sus9no5b5")))
	
	result = CMajorScale[1] - 4
	print("The root of the major scale - 4 is " + result)

	print(Chord(C, Chord.stringToPitchClass("min7")).printTones())
	print(CMajorScale[1].build(Chord)[2].buildPitchClass(-1, 2))
	
	# Build a scale off of a scale degree
	DDorianScale = CMajorScale[2].buildScale()
	print("The D Dorian Scale is: " + DDorianScale.printTones())

	# Build a chord off of a scale degree
	G9 = DDorianScale[4].build(Chord)
	print("The G Dominant chord is: " + G9.printTones())

	print("Converting the string #3 to an interval produces: " + Interval.stringToInterval("#3"))

	print("G7 with a flat third is: " + G9[2].transform("b").printTones())

	print("The roman numeral notation of the G9 chord is " + G9.printNumeralWithContext(True, 2))

	# Resolve the chord using a specific rule
	# CM7 = G9.resolveChord(circleOfFifths)
	# print("The result of resolving G9 is: " + CM7)

	# Find the relative chord of a chord
	Em7 = G9.getRelativeChord()
	print("The relative chord of G9 is Em7: " + Em7.printTones())

	# Get secondary dominant of a chord
	D7 = G9.getSecondaryDominant()
	print("The secondary dominant of G9 is D7: " + D7.printTones())

	# Transpose a scale up by semitones
	DMajorScale = CMajorScale + M2
	print("The D Major Scale is: " + DMajorScale.printTones())

	# Print the quality of a subset of a chord
	print("The chord resulting from subsetting G9 by 2-5 are: " + G9[2:3].printTones())

	# Properly print quality of a chord with accidentals
	Bhalfdim9 = CMajorScale[7].build(Chord)
	print("The quality of the 7th chord of the C major scale is: " + Bhalfdim9.getParentChordQuality())

	# Properly assign notes to non-major heptatonic scales
	AMelodicMinor = Scale(A, Scale.decimalToPitchClass(melodic_minor_ascending))
	print("The A Melodic Minor Scale is: " + AMelodicMinor.printTones())

	# Build a chord on a non-major heptatonic scale
	AM11b3 = AMelodicMinor[1].build(Chord)
	print("The first chord of the melodic minor scale is: " + AM11b3.printTones())

	# Properly print the quality of non-major diatonic chord
	print("The quality of this chord is: " + AM11b3.getParentChordQuality())

	# Print Roman Numerals with the Correct quality
	print("The jazz numeral notation of the 6th chord of A minor, with 7 notes is: " + Scale(A, Scale.decimalToPitchClass(minor))[6].build(Chord, 7).printNumeral(True, 2))

	print(CMajorScale[1].buildWithIntervals(Chord, Chord.stringToPitchClass("half-dimmaj7")).getParentDegree().getParentScale().printTones())

	# Get properties of scale
	print("The number of imperfections in the C Major Scale is: " + str(CMajorScale.getImperfections()))
	print("The reflection axes of the C Major scale are: " + str(CMajorScale.getReflectionAxes()))

	# Build non-heptatonic scales
	CChromaticScale = Scale(C, [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7])
	print("The Chromatic Scale is: " + CChromaticScale.printTones())

	# build a chord on the chromatic scale
	chord = CChromaticScale[1].build(Chord, 5)
	print("the quality of the first chord in the C chromatic scale is: " + chord.getParentChordQuality() + chord)

	print(Chord.stringToPitchClass("half-dimmaj7"))

	# Build chord on non-heptatonic scales
	CDimScale = Scale(C, [P1, M2, m3, P4, dim5, m6, m7.transform("b"), M7])
	print("The first chord of the C Diminished Scale is: " + CDimScale[1].build(Chord).printTones())

	# build a chord on the c dim scale
	chord = CDimScale[1].build(Chord, 5)
	print("the quality of the first chord in the C Dim scale is: " + chord.getParentChordQuality() + chord)

	# Check if chord exists in a scale
	if G9 in CMajorScale:
		print("Check if G9 in C Major Scale: True")

	# Check if scale exists in a scale
	if DDorianScale in CMajorScale:
		print("Check if D Dorian Scale in C Major Scale: True")

	# Check if intervals exist in a scale
	if [P1, M3, P5] in CMajorScale:
		print("Check if [P1, M3, P5] in C Major Scale: True")


if __name__ == "__main__":
	main()