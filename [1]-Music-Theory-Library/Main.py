import random
import sys

def main():
	print("Hello World")
	# Testing
	CMajorScale = Scale("C#", harmonicMinor)
	print(CMajorScale)
	DDorianScale = CMajorScale[2].buildScale()
	# CMajorScale.setParentDegree("E")
	# G7 = DDorianScale.getDegree(4).buildChord()
	# CM7 = G7.resolveChord()

if __name__ == "__main__":
	main()