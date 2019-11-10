# TODO:
# Support #/b notes and assign accidentals correctly : Completed
# Print Roman Numerals : Completed
# Support Non-heptatonic Scales : Completed
# Find solution to multiplying scale for chords to support degrees of > 12 Semitone intervals :: Solution: Chord inherits from scale, it is a scale object but has additional methods like resolve etc. but it also has its own degrees
# fix building chords with skips greater or less than three : Completed
# Fix Numeral Addition
# Fix notation for non-triadic chords 
# Get parallel key of scale
# Get Negative Harmony of a Chord
# Add try-catch statements of invalid inputs
# Add full support for add-sub for all classes
# Add support for chord inversions and sus notes

import random
import sys

from Scale import Scale
from Constants import *

def main():
	# Create a C Major Scale
	CMajorScale = Scale("C", major)
	print("The C Major Scale is: " + CMajorScale)

	# Build a scale off of a scale degree
	DDorianScale = CMajorScale[2].buildScale()
	print("The D Dorian Scale is: " + DDorianScale)

	# Build a chord off of a scale degree
	G9 = DDorianScale[4].buildChord(7, 6)
	print("The G Dominant chord is: " + G9)

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
	print("The chord resulting from subsetting G9 by 2-5 are: " + G9[2:5])

	# Properly print quality of a chord with accidentals
	Bhalfdim9 = CMajorScale[7].buildChord()
	print("The quality of the 7th chord of the C major scale is: " + Bhalfdim9.printQuality())

	# Properly assign notes to non-major heptatonic scales
	AMelodicMinor = Scale("A", melodicMinor)
	print("The A Melodic Minor Scale is: " + AMelodicMinor)

	# Build a chord on a non-major heptatonic scale
	AM11b3 = AMelodicMinor[1].buildChord(6)
	print("The first chord of the melodic minor scale is: " + AM11b3)

	# Properly print the quality of non-major diatonic chord
	print("The quality of this chord is: " + AM11b3.printQuality())

	# Print Roman Numerals with the Correct quality
	print("The jazz numeral notation of the 6th chord of A minor, with 7 notes is: " + Scale("A", minor)[6].buildChord(7).jazzNumeralNotation())

	# Get properties of scale
	print("The number of imperfections in the C Major Scale is: " + str(CMajorScale.getImperfections()))
	print("The reflection axes of the C Major scale are: " + str(CMajorScale.getReflectionAxes()))

	# Build non-heptatonic scales
	CChromaticScale = Scale("C", [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7])
	print("The Chromatic Scale is: " + CChromaticScale)

	# build a chord on the chromatic scale
	chord = CChromaticScale[1].buildChord(5)
	print("the quality of the first chord in the C chromatic scale is: " + chord.printQuality() + chord)

	# Build chord on non-heptatonic scales
	CDimScale = Scale("C", [P1, M2, m3, P4, aug4, m6, M6, M7])
	print("The first chord of the C Diminished Scale is: " + CDimScale[1].buildChord())

	# build a chord on the c dim scale
	chord = CDimScale[1].buildChord(5)
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