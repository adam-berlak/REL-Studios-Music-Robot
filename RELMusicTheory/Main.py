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
# COMPLETED: Fix negative intervals and avoid interval with 0 semitones and numerals
# COMPLETED: Fix numeral representation *Fixed, when calling super in invert, the recursive add/sub calls the subclass add and sub after one repeat*
# COMPLETED: Fix adding interval not in chord to chord without context
# COMPLETED: Might need to scale by order for gen intervals in move
# COMPLETED: Tone simplify should return a list of Tones with multiple simple names
# COMPLETED: Printing of negative Intervals
# COMPLETED: Diminished and Augmented chords arent neccissarily built on Thirds so I need to find a new way to identify qualities
# COMPLETED: scaleIntervalsByOrder() should be le and not lt. Also when you use move if new degree already exists in chord it should be removed
# COMPLETED: Support voice leading rules in configuration
# COMPLETED: Add support for chord inversions and sus notes in printQuality()
# COMPLETED: Get parallel key of scale
# COMPLETED: Printing quality of AmM7 is wrong
# COMPLETED: Need to fix scaleStepsToPitchClass so it doesnt include the Intervals array
# COMPLETED: getNegativeChord needs to use first inversion
# COMPLETED: Support invert for chords larger than M13
# COMPLETED: In distanceFromNext() check if it works with scales larger than 7 degrees
# COMPLETED: Resulting Chord from ResolveChord should use same accidentals as inputed chord
# COMPLETED: BUGS TO FIX: next() and previous() for Intervals with mutliple accidentals should work differently *Removed Next and Previous*

# LONG-TERM GOAL: Create and fix issues in UnitTest
# LONG-TERM GOAL: Add try-catch statements of invalid inputs 

# NEW FEATURES: Should be able to get a version of an interval with minimal accidentals IE: bb4 = b3
# NEW FEATURES: Change name for the Tone class within the Keyboard object to Key, allow it to play sounds

# BUGS TO FIX: Support decimal to pitch class in build
# BUGS TO FIX: Dont use contains for checking if interval in scale, because contains will rotate scale
# BUGS TO FIX: Transform should return degree instead of Scale or Chord
# BUGS TO FIX: Too many overrided methods in Chord, indexing should retrieve parent scale degree instead
# BUGS TO FIX: Transform should either take int or Accidental
# BUGS TO FIX: Override Interval add in Chord Degree
# BUGS TO FIX: Possibly fix slice for Chord
# BUGS TO FIX: Possibly change how findInParent returns self if no parent defined
# BUGS TO FIX: In Chord, for all methods that access parentDegree perfom a check
# BUGS TO FIX: Add limitations on getFirstInversion() and getInversion() so that it doesnt loop forever
# BUGS TO FIX: Fix sub and addition
# BUGS TO FIX: Remove hardcoded chord quality names from Chord class
# BUGS TO FIX: If you build a Chord on a Chord degree with specific intervals how does it behave
# BUGS TO FIX: Check if sub-setting Chords and rotating/added maintains the parent degree
# BUGS TO FIX: Retrieving numeral relative to parent should go down the chain of all parents

import random
import sys

from Scale import *
from Chord import *
from Configuration import *

def main():

	# Ways to build a Scale object
	C_Major_Scale = Scale(C, major)
	C_M7 = C_Major_Scale[1].build(Chord, "maj7")

	C_Major_Scale_2 = Scale(C, [P1, M2, M3, P4, P5, M6, M7])
	C_Major_Scale_3 = Scale(C, [2, 2, 1, 2, 2, 2, 1])
	C_Major_Scale_4 = Scale([C, D, E, F, G, A, B])

	# Ways to build a Chord object with a Parent Scale
	C_M7 = C_Major_Scale[1].build(Chord, "maj7")
	C_M7_2 = C_Major_Scale[1].build(Chord, 4, 3)
	C_M7_3 = C_Major_Scale[1].build(Chord, [P1, M3, P5, M7])
	C_M7_4 = C_Major_Scale[1].build(Chord, [1, 3, 5, 7])
	C_M7_5 = (Chord(C_Major_Scale[1] + C_Major_Scale[3] + C_Major_Scale[5] + C_Major_Scale[7]))

	# Ways to build a Chord object without a Parent Scale
	C_M7_6 = Chord(C, [P1, M3, P5, M7])
	C_M7_7 = Chord(C, [4, 3, 4, 1])
	C_M7_8 = Chord([C, E, G, B])

	# Naming Conventions
	C_Major_Scale.getName()
	C_Major_Scale.getCardinality()
	C_Major_Scale.getModeNames()
	C_Major_Scale[1].getName()
	C_Major_Scale[1].getNumeral()
	(C_Major_Scale + 2).getName()
	
	C_M7.getQuality()
	C_M7.getFiguredBass()
	C_M7.getNumeral()

	# Arithmetic
	C_Major_Scale + 3
	C_Major_Scale + m3
	C_Major_Scale[1] + 3
	C_Major_Scale[1] + m3
	C_Major_Scale[1] + C_Major_Scale[3]
	C_Major_Scale[1:2] + C_Major_Scale[4]
	C_Major_Scale[1:2] + C_Major_Scale[4:7]

	C_Major_Scale[3] - C_Major_Scale[1]
	
	E - C
	C + m3
	P1 + m3

	# Chord Inversions and Sub-Setting
	C_64 = C_M7[1:3].invert(2)
	C_64.getInversion()
	C_64.getFiguredBass()
	C_75 = C_64.getFirstInversion()

	# Resolving Chords and Voice Leading
	F_643 = C_M7.resolveChord()
	F_643.getInversion()
	G_643 = C_M7.resolveChordInto(C_Major_Scale[5].build(Chord))
	G_643.getInversion()
	
	# Transformations
	C_M7.getRelativeChord()
	C_M7.getParallelChord()
	C_M7.getNegativeChord()

	# Finding alternative Scales
	#C_M7.getPossibleParentScales()

	# Secondary Chords
	D_m7 = C_M7 + 2
	D_m7.getSecondaryDominant()
	D_m7.getSecondarySubDominant()
	D_m7.getSecondaryTonic()
	D_m7.getSecondaryAugmentedSix()
	D_m7.getSecondaryTritoneSubstitution()

	# Complex Chord Building
	Chord(C, "mM11b5no9")
	Chord(C, "half-dim9sus4b9")


'''
	C_Minor_Scale = Scale(C, lydian)
	
	C_Diminished_Scale = Scale(C, diminished)
	C_Chromatic_Scale = Scale(C, chromatic)
	A_Minor_Scale = C_Major_Scale + 6
	
	A_Melodic_Minor = Scale(A, melodic_minor_ascending)

	test = Scale(C, diminished_seventh)
	print(test.getIntervals())
	
	Cdim7 = C_Diminished_Scale[1].build(Chord, [1, 3, 4, 6])
	Bm7b5 = C_Major_Scale[7].build(Chord)
	G7 = C_Major_Scale[5].build(Chord)
	CM7 = C_Major_Scale[1].build(Chord)
	FM7 = C_Major_Scale[1].build(Chord, [1, 3, 4, 7])

	AmM7 = A_Melodic_Minor[1].build(Chord)

	test_chord = C_Major_Scale[7].build(Chord, [1, 3, 5, 6, 7, 11])

	print(Cdim7.getNegativeChord())

	print(Chord([E, B, F, C, G]).invert(5).getIntervals())



	#print(C_Major_Scale[3].build(Chord, diminished_seventh))

	#print(Cdim7.getNegativeChord())

	# Create a C Major Scale
	CMajorScale = Scale(C, Scale.decimalToPitchClass(major))

	print("Got Here" + CMajorScale[1].build(Chord).getSecondaryAugmentedSix())

	print(Chord(C, [P1, m3, P5, m7])[2])

	print(CMajorScale.printTones())

	print(Scale.scaleIntervalsByOrder([P1, M3, P5, M7, M2, P4, m6]))

	print(CMajorScale[2].buildScale()[2].findInParent().getInterval())

	print(Scale(C, Scale.decimalToPitchClass(diminished_seventh)))

	print("herere" + (CMajorScale[1].build(Chord)[1] + m3).getParentScale())
	
	CChromaticScale = Scale(G, [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7])
	
	print(CMajorScale[7] + CChromaticScale[3])

	print("result: " + Chord(C, [P1, M3, P5, M7])[2].build(Chord).getParentScale())

	Dorian = CMajorScale + 2
	print(CMajorScale[7].build(Chord).getSecondaryDominant())
	
	CM7 = CMajorScale[1].build(Chord, [P1, M3, aug5, m7, m9, P11])
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

	print("The roman numeral notation of the G9 chord is " + G9.getNumeralWithContext(True, 2))

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
	print("The jazz numeral notation of the 6th chord of A minor, with 7 notes is: " + Scale(A, Scale.decimalToPitchClass(minor))[6].build(Chord, 7).getNumeral(True, 2))

	print(CMajorScale[1].build(Chord, Chord.stringToPitchClass("half-dimmaj7")).getParentDegree().getParentScale().printTones())

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
'''

if __name__ == "__main__":
	main()