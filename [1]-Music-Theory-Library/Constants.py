from Interval import Interval

# Configuration
System = "western"

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

# Chord Quality Systems
Chord_Qualities = {
    "western": {
        ("major", "maj", "M"): [P1, M3, P5, M7, M9, P11, M13],
        ("minor", "min", "m"): [P1, m3, P5, m7, M9, P11, m13],
        ("dominant", "dom", ""): [P1, M3, P5, m7, M9, P11, M13]
    }
}
'''
class ScaleDescriptor:
    def __init__(self, p_intervals, p_mode_names, p_cardinality, p_pitch_class_set, p_forte_number, p_rotational_symmetry, p_reflection_axes, p_palindromic, p_chirality, p_hemitonia, p_cohemitonia, p_imperfections, p_modes, p_prime_mode):
        self.intervals = p_intervals
        self.mode_names = p_mode_names
        self.cardinality = p_cardinality
        self.pitch_class_set = p_pitch_class_set
        self.forte_number = p_forte_number
        self.rotational_symmetry = p_rotational_symmetry
        self.reflection_axes = p_reflection_axes
        self.palindromic = p_palindromic
        self.chirality = p_chirality
        self.hemitonia = p_hemitonia
        self.cohemitonia = p_cohemitonia
        self.imperfections = p_imperfections
        self.modes = p_modes
        self.prime_mode = p_prime_mode

# Scale Quality Systems
Scale_Qualities = {
    "western": {
        ("major", ): ScaleDescriptor([P1, M2, M3, P4, P5, M6, M7], [("major", "lonian"), ("dorian",), ("phrygian",), ("lydian",), ("myxolydian",), ("minor", "aeolian"), ("locrian",)], (7,"heptatonic"), [0,2,4,5,7,9,11], "7-35", "none", 2, "no", "no", (2,"dihemitonic"), (0,"ancohemitonic"), 1, 6, 7),
        ("melodic minor", ): ScaleDescriptor([P1, M2, m3, P4, P5, M6, M7], [("melodic minor",), ("dorian flat 2",), ("lydian augmented",), ("acoustic",), ("major-minor",), ("minor locrian",), ("superlocrian",)]),
        ("harmonic minor", ): ScaleDescriptor([P1, M2, m3, P4, P5, m6, M7], [("harmonic minor",)("locrian natural 6",)("major augmented",)("lydian augmented",)("phrygian dominant",)("aeolian harmonic",)("ultralociran",)]),
        ("neopolitan major", ): ScaleDescriptor([P1, m2, m3, P4, P5, M6, M7], [("neopolitan major",)("leading whole-tone",)("aeroptian",)("lydian minor",)("major locrian",)("storian",)("leading whole-tone inverse",)]),
        ("neopolitan minor", ): ScaleDescriptor([P1, m2, m3, P4, P5, m6, M7], [("neopolitan minor",)("mela citrambari",)("lagian",)("minor romani",)("asian (a)",)("mela sulini",)("porian",)])
    }
}
'''
# Tonal Systems
TONES = {
    "western": [("B#", "C", "Dbb"), ("B##", "C#", "Db"), ("C##", "D", "Ebb"), ("D#", "Eb", "Fbb"), ("D##", "E", "Fb"), ("E#", "F", "Gbb"), ("E##", "F#", "Gb"), ("F##", "G", "Abb"), ("G#", "Ab", "Bbbb"), ("G##", "A", "Bbb"), ("A#", "Bb", "Cbb"), ("A##", "B", "Cb")]
}

# Heptatonic Scales
major = [P1, M2, M3, P4, P5, M6, M7]
minor = [P1, M2, m3, P4, P5, m6, m7]
melodicMinor = [P1, M2, m3, P4, P5, M6, M7]
harmonicMinor = [P1, M2, m3, P4, P5, m6, M7]
neopolitanMajor = [P1, m2, m3, P4, P5, M6, M7]

# Resolution Rules
def circleOfFifths(p_chord):
	return p_chord + 3
def circleOfFourths(p_chord):
	return p_chord + 4