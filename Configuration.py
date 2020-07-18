from TheoryComponents.Interval import Interval
from TheoryComponents.Tone import Tone
from TheoryComponents.Key import Key
from TheoryComponents.Note import Note
from TheoryCollections.ScalesDictionary import *

# Configuration System
DEFAULT_SYSTEM = "western"

ACCIDENTAL_LIMIT = 1

DEGREE_SIMPLE_REPRESENTATION = False

# Configuration Unaltered Tones
UNALTERED_TONES = {
    0: "C",
    2: "D",
    4: "E",
    5: "F",
    7: "G",
    9: "A",
    11: "B"
}

UNALTERED_INTERVALS = {"western": list(UNALTERED_TONES.keys())}
TONE_NAMES = {"western": [UNALTERED_TONES[item] if item in UNALTERED_TONES.keys() else None for item in range(0, 12)]}

# Configuration Interval Spectrum Systems
INTERVAL_SPECTRUM = {"western": {1: "D", 2: "S", 3: "N", 4: "M", 5: "P", 6: "T", 7: "P", 8: "M", 9: "N", 10: "S", 11: "D"}}

# Configuration Cardinality Systems
CARDINALITY = {"western": {1: "monotonic", 2: "ditonic", 3: "tritonic", 4: "tetratonic", 5: "pentatonic", 6: "hexatonic", 7: "heptatonic", 8: "octatonic", 12: "chromatic"}}

RESOLUTION_SYSTEM = {"western": -5}

# Configure Notation Systems
ACCIDENTALS = {"western": {-1: "b", 0: "", 1: "#"}}
SUSPENDED_NOTATION = {"western": "sus"}
ADDITION_NOTATION = {"western": "add"}
OMISSION_NOTATION = {"western": "no"}

RHYTHM_TREE = {"western": {1: "Semi-breve", 
                            2: "minim", 
                            4: "crotchet", 
                            8: "quaver", 
                            16: "semi-quaver", 
                            32: "demi-semi-quaver"}}

Interval.unaltered_intervals = UNALTERED_INTERVALS[DEFAULT_SYSTEM]
Interval.accidentals = ACCIDENTALS[DEFAULT_SYSTEM]

Tone.accidental_limit = ACCIDENTAL_LIMIT
Tone.tone_names = TONE_NAMES[DEFAULT_SYSTEM]
Tone.accidentals = ACCIDENTALS[DEFAULT_SYSTEM]

# Configuration Note Constants Systems
TIME_DIVISION = 480

Note.time_division = TIME_DIVISION
Note.rhythm_tree = RHYTHM_TREE[DEFAULT_SYSTEM]

# Variables #

# Configuration note length constants
whole_note = 1
half_note = 2
quarter_note = 4
eighth_note = 8
sixteenth_note = 16

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

dim1 = Interval(-1, 1)
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

aug1 = Interval(1, 1)
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

# Configuration Chord Quality Systems
CHORD_QUALITIES = {"western": {
                ("major", "maj", "M", "Δ"):                [P1, M3, P5, M7, M9, P11, M13],
                ("minor", "min", "m", "-"):                [P1, m3, P5, m7, M9, P11, M13],
                ("dominant", "dom", "\"", "\""):           [P1, M3, P5, m7, M9, P11, M13],
                ("half-diminished", "half-dim", "ø", "ø"): [P1, m3, dim5, m7, M9, P11, M13],
                ("augmented", "aug", "+", "+"):            [P1, M3, aug5, m7, M9, P11, M13],
                ("diminished", "dim", "o", "o"):           [P1, m3, dim5, m7.transform("b"), M9, P11, None]}}

# Configuration Scale Degree Naming Systems
SCALE_DEGREE_NAMES = {"western": {P1: "tonic", m2: "supertonic", M2: "supertonic", m3: "mediant", M3: "mediant", P4: "subdominant", P5: "dominant", m6: "submediant", M6: "submediant", m7: "subtonic", M7: "leading tone"}}

# Configuration Tone Constants
C = Tone(TONE_NAMES[DEFAULT_SYSTEM][0])
D = Tone(TONE_NAMES[DEFAULT_SYSTEM][2])
E = Tone(TONE_NAMES[DEFAULT_SYSTEM][4])
F = Tone(TONE_NAMES[DEFAULT_SYSTEM][5])
G = Tone(TONE_NAMES[DEFAULT_SYSTEM][7])
A = Tone(TONE_NAMES[DEFAULT_SYSTEM][9])
B = Tone(TONE_NAMES[DEFAULT_SYSTEM][11])

C_flat = Tone(TONE_NAMES[DEFAULT_SYSTEM][0], -1)
D_flat = Tone(TONE_NAMES[DEFAULT_SYSTEM][2], -1)
E_flat = Tone(TONE_NAMES[DEFAULT_SYSTEM][4], -1)
F_flat = Tone(TONE_NAMES[DEFAULT_SYSTEM][5], -1)
G_flat = Tone(TONE_NAMES[DEFAULT_SYSTEM][7], -1)
A_flat = Tone(TONE_NAMES[DEFAULT_SYSTEM][9], -1)
B_flat = Tone(TONE_NAMES[DEFAULT_SYSTEM][11], -1)

C_sharp = Tone(TONE_NAMES[DEFAULT_SYSTEM][0], 1)
D_sharp = Tone(TONE_NAMES[DEFAULT_SYSTEM][2], 1)
E_sharp = Tone(TONE_NAMES[DEFAULT_SYSTEM][4], 1)
F_sharp = Tone(TONE_NAMES[DEFAULT_SYSTEM][5], 1)
G_sharp = Tone(TONE_NAMES[DEFAULT_SYSTEM][7], 1)
A_sharp = Tone(TONE_NAMES[DEFAULT_SYSTEM][9], 1)
B_sharp = Tone(TONE_NAMES[DEFAULT_SYSTEM][11], 1)

# Configuration Key Constants
keyboard_tones = [C_flat, C, C_sharp, D_flat, D, D_sharp, E_flat, E, E_sharp, F_flat, F, F_sharp, G_flat, G, G_sharp, A_flat, A, A_sharp, B_flat, B, B_sharp]
Key.start_point = C

Keyboard = {}

for i in range(12):

    for tone in keyboard_tones: 

        temp_accidental = ''
        if (tone.getAccidental() == 1): temp_accidental = '_sharp'
        if (tone.getAccidental() == -1): temp_accidental = '_flat'

        globals()[tone.getToneName() + temp_accidental + str(i)] = Key(tone, i)

# Functions
def toMidiData(p_playable_object):
    return p_playable_object.__toMidiData__()

def play(p_playable_object):
    return p_playable_object.__play__()