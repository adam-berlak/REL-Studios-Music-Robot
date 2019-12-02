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

# STRETCH GOAL: Get parallel key of scale
# STRETCH GOAL: Get Negative Harmony of a Chord
# STRETCH GOAL: Add full support for sub for all classes
# STRETCH GOAL: Add support for chord inversions and sus notes
# STRETCH GOAL: Create a Scale.Dictionary.py file for holding thousands of Scale definitions

# IMPORTANT: Add try-catch statements of invalid inputs
# IMPORTANT: Move unaltered_intervals dictionary into constants
# IMPORTANT: Using buildWithIntervals method should change the parent scale of the resulting scale object if it includes intervals not in the parent, but only if the scale object is a chord
# IMPORTANT: Add support for stringToInterval in interval class
# IMPORTANT: Add support for sus chords in stringToPitchClass method
# IMPORTANT: Fix issue with using Dominant as extension in printQuality()

import random
import sys

from Scale import *
from Chord import *
from Keyboard import *
from Constants import *

def main():
	# Create a C Major Scale
	CMajorScale = Scale("C", major)
	print("The C Major Scale is: " + CMajorScale)

	Eb = CMajorScale[1] + m3
	print("The first degree of the C Major Scale + m3 is: " + Eb)

	print("The major scale converted to Decimal is: " + str(Scale.pitchClassToDecimal([P1, M2, M3, P4, P5, M6, M7])))

	print("The string dom7sus9no5b5 produces the pitch class " + str(Chord.stringToPitchClass("dom7sus9no5b5")))

	result = CMajorScale[1] - 4
	print("The root of the major scale - 4 is " + result)

	print(Chord("C", Chord.stringToPitchClass("maj7"))[2].buildPitchClass(2))
	print(CMajorScale[1].build(Chord)[2].buildPitchClass(2))

	# Build a scale off of a scale degree
	DDorianScale = CMajorScale[2].buildScale()
	print("The D Dorian Scale is: " + DDorianScale)

	# Build a chord off of a scale degree
	G9 = DDorianScale[4].build(Chord)
	print("The G Dominant chord is: " + G9)

	print("Converting the string #3 to an interval produces: " + Interval.stringToInterval("#3"))

	print("G7 with a flat third is: " + G9[2].transform("b", Chord))

	print("The roman numeral notation of the G9 chord is " + G9.printNumeralWithContext(True, 2))

	# Resolve the chord using a specific rule
	CM7 = G9.resolveChord(circleOfFifths)
	print("The result of resolving G9 is: " + CM7)

	# Find the relative chord of a chord
	Em7 = G9.getRelativeChord()
	print("The relative chord of G9 is Em7: " + Em7)

	# Get secondary dominant of a chord
	D7 = G9.getSecondaryDominant()
	print("The secondary dominant of G9 is D7: " + D7)

	# Transpose a scale up by semitones
	DMajorScale = CMajorScale + M2
	print("The D Major Scale is: " + DMajorScale)

	# Print the quality of a subset of a chord
	print("The chord resulting from subsetting G9 by 2-5 are: " + G9[2:4])

	# Properly print quality of a chord with accidentals
	Bhalfdim9 = CMajorScale[7].build(Chord)
	print("The quality of the 7th chord of the C major scale is: " + Bhalfdim9.printQuality())

	# Properly assign notes to non-major heptatonic scales
	AMelodicMinor = Scale("A", melodicMinor)
	print("The A Melodic Minor Scale is: " + AMelodicMinor)

	# Build a chord on a non-major heptatonic scale
	AM11b3 = AMelodicMinor[1].build(Chord)
	print("The first chord of the melodic minor scale is: " + AM11b3)

	# Properly print the quality of non-major diatonic chord
	print("The quality of this chord is: " + AM11b3.printQuality())

	# Print Roman Numerals with the Correct quality
	print("The jazz numeral notation of the 6th chord of A minor, with 7 notes is: " + Scale("A", minor)[6].build(Chord, 7).printNumeral(True, 2))

	print(CMajorScale[1].buildWithIntervals(Chord, Chord.stringToPitchClass("half-dimmaj7")).getParentDegree().getParentScale())

	# Get properties of scale
	print("The number of imperfections in the C Major Scale is: " + str(CMajorScale.getImperfections()))
	print("The reflection axes of the C Major scale are: " + str(CMajorScale.getReflectionAxes()))

	# Build non-heptatonic scales
	CChromaticScale = Scale("C", [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7])
	print("The Chromatic Scale is: " + CChromaticScale)

	# build a chord on the chromatic scale
	chord = CChromaticScale[1].build(Chord, 5)
	print("the quality of the first chord in the C chromatic scale is: " + chord.printQuality() + chord)

	print(Chord.stringToPitchClass("half-dimmaj7"))

	# Build chord on non-heptatonic scales
	CDimScale = Scale("C", [P1, M2, m3, P4, aug4, m6, M6, M7])
	print("The first chord of the C Diminished Scale is: " + CDimScale[1].build(Chord))

	# build a chord on the c dim scale
	chord = CDimScale[1].build(Chord, 5)
	print("the quality of the first chord in the C Dim scale is: " + chord.printQuality() + chord)

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