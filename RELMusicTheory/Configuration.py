from Interval import *
from Tone import *
from ScalesDictionary import *

# Configuration System
DEFAULT_SYSTEM = "western"

ACCIDENTAL_LIMIT = 2

DEGREE_SIMPLE_REPRESENTATION = True

TONE_NAMES = {"western": ["C", None, "D", None, "E", "F", None, "G", None, "A", None, "B"]}

# Configuration Interval Spectrum Systems
INTERVAL_SPECTRUM = {"western": {1: "D", 2: "S", 3: "N", 4: "M", 5: "P", 6: "T", 7: "P", 8: "M", 9: "N", 10: "S", 11: "D"}}

# Configuration Cardinality Systems
CARDINALITY = {"western": {1: "monotonic", 2: "ditonic", 3: "tritonic", 4: "tetratonic", 5: "pentatonic", 6: "hexatonic", 7: "heptatonic", 8: "octatonic", 12: "chromatic"}}

# Configure Unaltered Intervals
UNALTERED_INTERVALS = {"western": [0, 2, 4, 5, 7, 9, 11]}

# Configure Voice Leading for Chords
HARMONIC_VOICE_LEADING = {"western": {1: 1, 2: 1, 3: -2, 4: -2}}

# Configure Notation Systems
ACCIDENTALS = {"western": {-1: "b", 0: "", 1: "#"}}

SUSPENDED_NOTATION = {"western": "sus"}

OMISSION_NOTATION = {"western": "no"}

Interval.unaltered_intervals = UNALTERED_INTERVALS["western"]
Interval.accidentals = ACCIDENTALS["western"]

Tone.tone_names = TONE_NAMES["western"]
Tone.accidentals = ACCIDENTALS["western"]

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

# Configuration Tone Constants
C = Tone("C")
D = Tone("D")
E = Tone("E")
F = Tone("F")
G = Tone("G")
A = Tone("A")
B = Tone("B")

C_flat = Tone("C", -1)
D_flat = Tone("D", -1)
E_flat = Tone("E", -1)
F_flat = Tone("F", -1)
G_flat = Tone("G", -1)
A_flat = Tone("A", -1)
B_flat = Tone("B", -1)

C_sharp = Tone("C", 1)
D_sharp = Tone("D", 1)
E_sharp = Tone("E", 1)
F_sharp = Tone("F", 1)
G_sharp = Tone("G", 1)
A_sharp = Tone("A", 1)
B_sharp = Tone("B", 1)

# Configuration Chord Quality Systems
CHORD_QUALITIES = {"western": {
                ("major", "maj", "M", "Δ"): [P1, M3, P5, M7, M9, P11, M13],
                ("minor", "min", "m", "-"): [P1, m3, P5, m7, M9, P11, m13],
                ("dominant", "dom", "\"", "\""): [P1, M3, P5, m7, M9, P11, M13],
                ("half-diminished", "half-dim", "ø", "ø"): [P1, m3, dim5, m7, m9, P11, m13],
                ("augmented", "aug", "+", "+"): [P1, M3, aug5, M7, aug9, aug11.transform("#"), P15],
                ("diminished", "dim", "o", "o"): [P1, m3, dim5, m7.transform("b"), P8, m10, dim12]}}

# Configuration Scale Degree Naming Systems
SCALE_DEGREE_NAMES = {"western": {P1: "tonic", m2: "supertonic", M2: "supertonic", m3: "mediant", M3: "mediant", P4: "subdominant", P5: "dominant", m6: "submediant", M6: "submediant", m7: "subtonic", M7: "leading tone"}}
