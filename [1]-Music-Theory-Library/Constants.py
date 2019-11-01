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

# Heptatonic Scales
major = [P1, M2, M3, P4, P5, M6, M7]
minor = [P1, M2, m3, P4, P5, m6, m7]
melodicMinor = [P1, M2, m3, P4, P5, M6, m7]
harmonicMinor = [P1, M2, m3, P4, P5, m6, M7]

# Tonal Systems
TONES = {
    "western": ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
}