from Interval import *

# Configuration System
DEFAULT_SYSTEM = "western"

# Variables #

# Configuration Interval Constants
P1 = Interval(0, 1)
M2 = Interval(2, 2)
M3 = Interval(4, 3)
P4 = Interval(5, 4)
P5 = Interval(7, 5)
M6 = Interval(9, 6)
M7 = Interval(11, 7)
P8 = Interval(12, 8)
M9 = Interval(14, 9)
M10 = Interval(16, 10)
P11 = Interval(17, 11)
P12 = Interval(19, 12)
M13 = Interval(21, 13)
M14 = Interval(23, 14)
P15 = Interval(24, 15)

m2 = Interval(1, 2)
m3 = Interval(3, 3)
dim5 = Interval(6, 5)
m6 = Interval(8, 6)
m7 = Interval(10, 7)
m9 = Interval(13, 9)
m10 = Interval(15, 10)
dim12 = Interval(18, 12)
m13 = Interval(20, 13)
m14 = Interval(22, 14)

aug2 = Interval(3, 2)
aug4 = Interval(6, 4)
aug5 = Interval(8, 5)
aug6 = Interval(10, 6)
aug7 = Interval(12, 7)
aug9 = Interval(15, 9)
aug11 = Interval(18, 11)
aug12 = Interval(20, 12)
aug13 = Interval(22, 13)
aug14 = Interval(24, 14)

# Configuration Heptatonic Scales Constants
major = [P1, M2, M3, P4, P5, M6, M7]
minor = [P1, M2, m3, P4, P5, m6, m7]
melodicMinor = [P1, M2, m3, P4, P5, M6, M7]
harmonicMinor = [P1, M2, m3, P4, P5, m6, M7]
neopolitanMajor = [P1, m2, m3, P4, P5, M6, M7]

# Configuration Tonal Systems
TONES = {
    "western": [("B#", "C", "Dbb"), ("B##", "C#", "Db"), ("C##", "D", "Ebb"), ("D#", "Eb", "Fbb"), ("D##", "E", "Fb"), ("E#", "F", "Gbb"), ("E##", "F#", "Gb"), ("F##", "G", "Abb"), ("G#", "Ab", "Bbbb"), ("G##", "A", "Bbb"), ("A#", "Bb", "Cbb"), ("A##", "B", "Cb")]
}

# Configuration Interval Spectrum Systems
Interval_Spectrum = {
    "western": {
        1: "D",
        2: "S",
        3: "N",
        4: "M",
        5: "P",
        6: "T",
        7: "P",
        8: "M",
        9: "N",
        10: "S",
        11: "D"
    }
}
'''
# Configuration Scale Degree Naming Systems
scale_degree_names = {
    "western": {
        (P1,): "tonic",
        (m2, M2): "supertonic",
        (m3, M3): "mediant",
        (P4,): "subdominant",
        (P5,): "dominant",
        (m6, M6): "submediant",
        (m7,): "subtonic",
        (M7,): "leading tone"
    }
}
'''
# Configuration Cardinality Systems
cardinality = {
    "western": {
        1: "monotonic",
        2: "ditonic",
        3: "tritonic",
        4: "tetratonic",
        5: "pentatonic",
        6: "hexatonic",
        7: "heptatonic", 
        8: "octatonic",
        12: "chromatic"
    }
}

# Configuration Chord Quality Systems
Chord_Qualities = {
    "western": {
        ("major", "maj", "M"): [P1, M3, P5, M7, M9, P11, M13],
        ("minor", "min", "m"): [P1, m3, P5, m7, M9, P11, m13],
        ("dominant", "dom", ""): [P1, M3, P5, m7, M9, P11, M13],
	("half-diminished", "half-dim", "ø"): [P1, m3, dim5, m7, m9, P11, m13]
	("augmented", "aug", "+"): [P1, M3, aug5, M7, aug9, P12, None], # Fix issue with index being out of range
    }
}

# Configuration Scale Nameing Systems
Scales = {
    "western": {
        "major": ([P1, M2, M3, P4, P5, M6, M7], ["ionian", "dorian", "phrygian", "lydian", "myxolydian", "aeolian", "locrian"])
    }
}

# Configuration Resolution Rules
def circleOfFifths(p_chord):
	return p_chord + 4
def circleOfFourths(p_chord):
	return p_chord + 5
