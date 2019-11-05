# TODO:
# Add try-catch statements of invalid inputs
# Add full support for add-sub for all classes
# Support #/b notes and assign accidentals correctly : Completed
# Get parallel key of scale
# Get Negative Harmony of a Chord
# Print Roman Numerals
# Fix Numeral Addition
# Find solution to multiplying scale for chords to support degrees of > 12 Semitone intervals :: Solution: Chord inherits from scale, it is a scale object but has additional methods like resolve etc. but it also has its own degrees

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
	G7 = DDorianScale[4].buildChord(4)
	print("The G Dominant Chord is: " + G7)

	# Resolve the chord using a specific rule
	CM7 = G7.resolveChord(circleOfFifths)
	print("The result of resolving G7 is: " + CM7)

	# Find the relative chord of a chord
	Em7 = G7.getRelativeChord()
	print("The relative chord of G7 is Em7: " + Em7)

	# Get secondary dominant of a chord
	D7 = G7.getSecondaryDominant()
	print("The secondary dominant of G7 is D7: " + D7)

	# Transpose a scale up by semitones
	DMajorScale = CMajorScale + 2
	print("The D Major Scale is: " + DMajorScale)

	# Print the quality of a chord
	print(G7[1:5].printQuality())

	# Properly print quality of a chord with accidentals
	Bhalfdim9 = CMajorScale[7].buildChord()
	print(Bhalfdim9.printQuality())

	# Properly assign notes to non-major heptatonic scales
	AMelodicMinor = Scale("A", melodicMinor)
	print("The A Melodic Minor Scale is: " + AMelodicMinor)

	# Build a chord on a non-major heptatonic scale
	AChord = AMelodicMinor[1].buildChord(6)
	print("The A Melodic Minor 7 Chord is: " + AChord)

	# Properly print the quality of non-major diatonic chord
	print("The A Melodic Minor 11 Chord Quality is is: " + AChord.printQuality())

	# Print Roman Numerals with the Correct quality
	print(Scale("A", minor)[6].buildChord(7).jazzNumeralNotation())

	print(CMajorScale.getImperfections())

	print(CMajorScale.getReflectionAxes())

if __name__ == "__main__":
	main()