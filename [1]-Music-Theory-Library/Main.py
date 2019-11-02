# TODO:
# Add try-catch statements of invalid inputs
# Add full support for add-sub for all classes
# Support #/b notes and assign accidentals correctly
# Print Roman Numerals

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
	G7 = DDorianScale[4].buildChord()
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

if __name__ == "__main__":
	main()