from Interval import *
from Tone import *
from ScalesDictionary import *

# Configuration System
DEFAULT_SYSTEM = "western"

ACCIDENTAL_LIMIT = 2

TONE_NAMES = {
        "western": ["C", None, "D", None, "E", "F", None, "G", None, "A", None, "B"],
        "german": ["C", None, "D", None, "E", "F", None, "G", None, "A", None, "H"],
        "dutch": ["C", None, "D", None, "E", "F", None, "G", None, "A", None, "B"],
        "japanese": ["ha", None, "ni", None, "ho", "he", None, "to", None, "i", None, "ro"],
        "chinese": ["C", None, "D", None, "E", "F", None, "G", None, "A", None, "B"],
        "arabic": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"],
        "italian": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"],
        "french": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"],
        "spanish": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"],
        "portuguese": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"],
        "russian": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"],
        "romanian": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"],
        "dutch/belgium": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"],
        "greek": ["Do", None, "Re", None, "Mi", "Fa", None, "Sol", None, "la", None, "Si"]}

# Configuration Interval Spectrum Systems
INTERVAL_SPECTRUM = {"western": {1: "D", 2: "S", 3: "N", 4: "M", 5: "P", 6: "T", 7: "P", 8: "M", 9: "N", 10: "S", 11: "D"}}

# Configuration Cardinality Systems
CARDINALITY = {"western": {1: "monotonic", 2: "ditonic", 3: "tritonic", 4: "tetratonic", 5: "pentatonic", 6: "hexatonic", 7: "heptatonic", 8: "octatonic", 12: "chromatic"}}

# Configure Unaltered Intervals
UNALTERED_INTERVALS = {"western": [0, 2, 4, 5, 7, 9, 11]}

# Configure Notation Systems
ACCIDENTALS = {
        "western": {-1: "b", 0: "", 1: "#"},
        "german": {-1: "es", 0: "", 1: "is"},
        "dutch": {-1: "mol", 0: "", 1: "kruis"},
        "japanese": {-1: "hen", 0: "", 1: "ei"},
        "chinese": {-1: "jiang", 0: "", 1: "sheng"},
        "arabic": {-1: "bemol", 0: "", 1: "diez"},
        "italian": {-1: "bemolle", 0: "", 1: "diesis"},
        "french": {-1: "bemol", 0: "", 1: "diese"},
        "spanish": {-1: "bemol", 0: "", 1: "sostenido"},
        "portuguese": {-1: "bemol", 0: "", 1: "sustenido"},
        "russian": {-1: "bemol", 0: "", 1: "diez"},
        "romanian": {-1: "mol", 0: "", 1: "kruis"},
        "dutch/belgium": {-1: "mol", 0: "", 1: "kruis"},
        "greek": {-1: "hyphesis", 0: "", 1: "diesis"}}

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

# Configuration Heptatonic Scales Constants
major = [P1, M2, M3, P4, P5, M6, M7]
minor = [P1, M2, m3, P4, P5, m6, m7]
melodicMinor = [P1, M2, m3, P4, P5, M6, M7]
harmonicMinor = [P1, M2, m3, P4, P5, m6, M7]
neopolitanMajor = [P1, m2, m3, P4, P5, M6, M7]

# Configuration Chord Quality Systems
CHORD_QUALITIES = {
        "western": {
                ("major", "maj", "M", "Δ"): [P1, M3, P5, M7, M9, P11, M13],
                ("minor", "min", "m", "-"): [P1, m3, P5, m7, M9, P11, m13],
                ("dominant", "dom", "\"", "\""): [P1, M3, P5, m7, M9, P11, M13],
                ("half-diminished", "half-dim", "ø", "ø"): [P1, m3, dim5, m7, m9, P11, m13],
                ("augmented", "aug", "+", "+"): [P1, M3, aug5, M7, aug9, aug11.transform("#"), P15],
                ("diminished", "dim", "o", "o"): [P1, m3, dim5, m7.transform("b"), P8, m10, dim12]},
        "german": {
                ("dur"): [P1, M3, P5, M7, M9, P11, M13],
                ("moll"): [P1, m3, P5, m7, M9, P11, m13]},
        "dutch": { 
                ("groot"): [P1, M3, P5, M7, M9, P11, M13],
                ("klien"): [P1, m3, P5, m7, M9, P11, m13]},
        "japanese": { 
                ("chōchō"): [P1, M3, P5, M7, M9, P11, M13],
                ("tanchō"): [P1, m3, P5, m7, M9, P11, m13]},
        "chinese": { 
                ("dà diào"): [P1, M3, P5, M7, M9, P11, M13],
                ("xiǎo diào"): [P1, m3, P5, m7, M9, P11, m13]},
        "korean": { 
                ("jangjo"): [P1, M3, P5, M7, M9, P11, M13],
                ("danjo"): [P1, m3, P5, m7, M9, P11, m13]},
        "arabic": { 
                ("major"): [P1, M3, P5, M7, M9, P11, M13],
                ("minor"): [P1, m3, P5, m7, M9, P11, m13]},
        "Italian": { 
                ("maggiore"): [P1, M3, P5, M7, M9, P11, M13],
                ("minore"): [P1, m3, P5, m7, M9, P11, m13]},
        "french": { 
                ("majeur"): [P1, M3, P5, M7, M9, P11, M13],
                ("mineur"): [P1, m3, P5, m7, M9, P11, m13]},
        "spanish": { 
                ("mayor"): [P1, M3, P5, M7, M9, P11, M13],
                ("menor"): [P1, m3, P5, m7, M9, P11, m13]},
        "portuguese": { 
                ("maior"): [P1, M3, P5, M7, M9, P11, M13],
                ("menor"): [P1, m3, P5, m7, M9, P11, m13]},
        "russian": { 
                ("мажор"): [P1, M3, P5, M7, M9, P11, M13],
                ("минор"): [P1, m3, P5, m7, M9, P11, m13]},
        "romanian": { 
                ("major"): [P1, M3, P5, M7, M9, P11, M13],
                ("minor"): [P1, m3, P5, m7, M9, P11, m13]},
        "greek": { 
                ("μείζονα"): [P1, M3, P5, M7, M9, P11, M13],
                ("ελάσσονα"): [P1, m3, P5, m7, M9, P11, m13]}}

# Configuration Scale Degree Naming Systems
SCALE_DEGREE_NAMES = {"western": {P1: "tonic", m2: "supertonic", M2: "supertonic", m3: "mediant", M3: "mediant", P4: "subdominant", P5: "dominant", m6: "submediant", M6: "submediant", m7: "subtonic", M7: "leading tone"}}

# Configuration Resolution Rules
def circleOfFifths(p_chord):
	return p_chord - 5
def circleOfFourths(p_chord):
	return p_chord - 4

