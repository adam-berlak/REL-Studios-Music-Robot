import unittest

from Scale import *
from Chord import *
from Configuration import *

class TestScaleMethods(unittest.TestCase):

    def test_interval_arithmetic(self):
        self.assertEqual(str(P1 + M3), "3")     # Adding to P1 does not change Interval
        self.assertEqual(str(m2 + M3), "4")     # Adding two positive Intervals produces correct result
        self.assertEqual(str(M3 - M3), "1")     # Subtracting Interval by itself produces P1
        self.assertEqual(str(M3 - P4), "-b2")   # Subtracting an Interval from a smaller Interval produces correct result
        self.assertEqual(str(M3 - -m2), "4")    # Subtracting negative Interval produces correct result
        self.assertEqual(str(-M3 - m2), "-4")   # Subtracting two negative Intervals produces correct result
        self.assertEqual(str(-M3 + M3), "1")    # Adding Interval to its opposite produces P1
        self.assertEqual(str(-M3 + P4), "b2")   # Adding larger positive Interval to negative Interval produces correct result
        self.assertEqual(str(-P1 + P4), "4")    # Negative P1 works correctly

        self.assertEqual(str(abs(P1)), "1")     # Absolute value works correctly on positive P1
        self.assertEqual(str(abs(-P1)), "1")    # Absolute value works correctly on negative P1
        self.assertEqual(str(abs(m2)), "b2")    # Absolute value works correctly on positive Interval
        self.assertEqual(str(abs(-m2)), "b2")   # Absolute value works correctly on negative Interval

    def test_degree_arithmetic(self):
        self.assertEqual(str(Scale(C, major)[1] + M2), "D")
        self.assertEqual(str((Scale(C, major)[1] + M2).getParentScale()), "<C, D, E, F, G, A, B>")
        self.assertEqual(str(Scale(C, major)[1] + m2), "Db")
        self.assertEqual(str((Scale(C, major)[1] + m2).getParentScale()), "<C, Db, E, F, G, A, B>")
        self.assertEqual(str(Scale(C, major)[1] + P8), "C")
        self.assertEqual(str((Scale(C, major)[1] + P8).getParentScale()), "<C, D, E, F, G, A, B>")
        self.assertEqual(str(Scale(C, major)[1] - m2), "B")
        self.assertEqual(str((Scale(C, major)[1] - m2).getParentScale()), "<C, D, E, F, G, A, B>")
        self.assertEqual(str(Scale(C, major)[1] - M2), "Bb")
        self.assertEqual(str((Scale(C, major)[1] - M2).getParentScale()), "<C, D, E, F, G, A, Bb>")

        self.assertEqual(str(Scale(C, diminished)[1] + M2), "D")
        self.assertEqual(str((Scale(C, diminished)[1] + M2).getParentScale()), "<C, D, Eb, F, Gb, Ab, A, B>")
        self.assertEqual(str(Scale(C, diminished)[1] + m2), "Db")
        self.assertEqual(str((Scale(C, diminished)[1] + m2).getParentScale()), "<C, Db, D, Eb, F, Gb, Ab, A, B>")
        
    def test_scale_creation(self):
        self.assertEqual(str(Scale(C_flat, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[Cb, Db, Eb, Fb, Gb, Ab, Bb]")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[C, D, E, F, G, A, B]")
        self.assertEqual(str(Scale(C_sharp, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[C#, D#, E#, F#, G#, A#, B#]")
        self.assertEqual(str(Scale(D_flat, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[Db, Eb, F, Gb, Ab, Bb, C]")
        self.assertEqual(str(Scale(D, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[D, E, F#, G, A, B, C#]")
        self.assertEqual(str(Scale(D_sharp, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[D#, E#, F##, G#, A#, B#, C##]")
        self.assertEqual(str(Scale(E_flat, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[Eb, F, G, Ab, Bb, C, D]")
        self.assertEqual(str(Scale(E, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[E, F#, G#, A, B, C#, D#]")
        self.assertEqual(str(Scale(E_sharp, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[E#, F##, G##, A#, B#, C##, D##]")
        self.assertEqual(str(Scale(F_flat, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[Fb, Gb, Ab, Bbb, Cb, Db, Eb]")
        self.assertEqual(str(Scale(F, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[F, G, A, Bb, C, D, E]")
        self.assertEqual(str(Scale(F_sharp, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[F#, G#, A#, B, C#, D#, E#]")
        self.assertEqual(str(Scale(G_flat, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[Gb, Ab, Bb, Cb, Db, Eb, F]")
        self.assertEqual(str(Scale(G, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[G, A, B, C, D, E, F#]")
        self.assertEqual(str(Scale(G_sharp, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[G#, A#, B#, C#, D#, E#, F##]")
        self.assertEqual(str(Scale(A_flat, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[Ab, Bb, C, Db, Eb, F, G]")
        self.assertEqual(str(Scale(A, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[A, B, C#, D, E, F#, G#]")
        self.assertEqual(str(Scale(A_sharp, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[A#, B#, C##, D#, E#, F##, G##]")
        self.assertEqual(str(Scale(B_flat, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[Bb, C, D, Eb, F, G, A]")
        self.assertEqual(str(Scale(B, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[B, C#, D#, E, F#, G#, A#]")
        self.assertEqual(str(Scale(B_sharp, [P1, M2, M3, P4, P5, M6, M7]).printTones()), "[B#, C##, D##, E#, F##, G##, A##]")

    def test_scale_size(self):
        self.assertEqual(str(Scale(C, [P1]).printTones()), "[C]")
        self.assertEqual(str(Scale(C, [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7]).printTones()), "[C, Db, D, Eb, E, F, F#, G, Ab, A, Bb, B]")

    def test_scale_indexing(self):
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].getTone()), "C")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[7].getTone()), "B")

    def test_scale_next_previous(self):
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].previous().getTone()), "B")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[7].next().getTone()), "C")

    def test_scale_arithmetic(self):
        self.assertEqual(str((Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1] - 2).getTone()), "B")
        self.assertEqual(str((Scale(C, [P1, M2, M3, P4, P5, M6, M7])[7] + 2).getTone()), "C")

        self.assertEqual(str((Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1] - 16).getTone()), "B")
        self.assertEqual(str((Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1] + 16).getTone()), "D")

        self.assertEqual(str((Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1] - m2).getTone()), "B")
        self.assertEqual(str((Scale(C, [P1, M2, M3, P4, P5, M6, M7])[7] + m2).getTone()), "C")

        self.assertEqual(str((Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1] - m9).getTone()), "B")
        self.assertEqual(str((Scale(C, [P1, M2, M3, P4, P5, M6, M7])[7] + m9).getTone()), "C")

    def test_scale_contains(self):
        self.assertEqual(C in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(C_sharp in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), False)

        self.assertEqual(M2 in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(M9 in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(dim5 in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), False)

        self.assertEqual([P1, M3, P5] in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual([P1, M3, M9] in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual([P1, M3, dim5, P5] in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), False)

        self.assertEqual(Scale(C, [P1, M2, M3, P4, P5, M6]) in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(Scale(C, [P1, M2, M3, P4, P5, m6, M6, M7]) in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), False)

        self.assertEqual(Chord(C, Chord.stringToPitchClass("maj7")) in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(Chord(C, Chord.stringToPitchClass("maj9b5")) in Scale(C, [P1, M2, M3, P4, P5, M6, M7]), False)

    def test_scale_derived_attributes(self):
        self.assertEqual(Scale.pitchClassToScaleSteps([P1, M2, M3, P4, P5, M6, M7]), [2, 2, 1, 2, 2, 2, 1])
        self.assertEqual(Scale.pitchClassToScaleSteps([P1, M3, P5]), [4, 3, 5])

        self.assertEqual(Scale.scaleStepsToPitchClass([2, 2, 1, 2, 2, 2, 1]), [P1, M2, M3, P4, P5, M6, M7])
        self.assertEqual(Scale.scaleStepsToPitchClass([4, 3, 5]), [P1, M3, P5])
        # self.assertEqual(Scale.scaleStepsToPitchClass([4, 3, 5, 2]), [P1, M3, P5, M9])

    def test_build_chord(self):
        # self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 0).printTones()), "[]")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 1).printTones()), "[C]")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7).printTones()), "[C, E, G, B, D, F, A]")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 8).printTones()), "[C, E, G, B, D, F, A, C]")

        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 1).printTones()), "[C, C, C, C, C, C, C]")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 2).printTones()), "[C, D, E, F, G, A, B]")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 7).printTones()), "[C, B, A, G, F, E, D]")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 8, 7).printTones()), "[C, B, A, G, F, E, D, C]")
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 8).printTones()), "[C, C, C, C, C, C, C]")

    def test_string_to_pitch_class(self):
        self.assertEqual(str(Chord.stringToPitchClass("maj7")), "[1, 3, 5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("majmaj7")), "[1, 3, 5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("maj7b5")), "[1, 3, b5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("maj7b3b5")), "[1, b3, b5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj5")), "[1, b3, 5]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7")), "[1, b3, 5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7b7")), "[1, b3, 5, b7]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7b9")), "[1, b3, 5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7no5")), "[1, b3, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7no5sus2")), "[1, 2, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("mindom7")), "[1, b3, 5, b7]")
        self.assertEqual(str(Chord.stringToPitchClass("domdom7")), "[1, 3, 5, b7]")
        self.assertEqual(str(Chord.stringToPitchClass("Mo11")), "[1, 3, 5, bb7, 9, 11]")

    def test_print_quality(self):
        self.assertEqual(str(Chord(C, [P1, M3, M7]).getQuality()), "M7no5")
        self.assertEqual(str(Chord(C, [P1, m3, M7]).getQuality()), "mM7no5")
        self.assertEqual(str(Chord(C, [P1, m3, P4, M7]).getQuality()), "mM7add4no5")
        self.assertEqual(str(Chord(C, [P1, m3, aug4, M7]).getQuality()), "mM7add#4no5")
        self.assertEqual(str(Chord(C, [P1, P4, M7]).getQuality()), "M7sus4no5")
        self.assertEqual(str(Chord(C, [P1, aug4, M7]).getQuality()), "M7sus#4no5")
        self.assertEqual(str(Chord(C, [P1, M3, P5, m7]).getQuality()), "\"7")
        self.assertEqual(str(Chord(C, [P1, M3, dim5, m7]).getQuality()), "\"7b5")

        # Test all Chord Qualities
        self.assertEqual(str(Chord(C, [P1, M3, P5, M7, M9, P11, M13]).getQuality()), "M13")
        self.assertEqual(str(Chord(C, [P1, m3, P5, m7, M9, P11, M13]).getQuality()), "m13") 
        self.assertEqual(str(Chord(C, [P1, M3, P5, m7, M9, P11, M13]).getQuality()), "\"13")
        self.assertEqual(str(Chord(C, [P1, m3, dim5, m7, M9, P11, M13]).getQuality()), "ø13")
        self.assertEqual(str(Chord(C, [P1, m3, dim5, m7.transform("b"), M9, P11]).getQuality()), "o11")
        self.assertEqual(str(Chord(C, [P1, M3, aug5, m7, M9, P11, M13]).getQuality()), "+13")

        # Test compound Chord Qualities
        self.assertEqual(str(Chord(C, [P1, m3, P5, M7, M9, P11, M13]).getQuality()), "mM13")
        self.assertEqual(str(Chord(C, [P1, m3, dim5, M7, M9, P11, M13]).getQuality()), "øM13")
        self.assertEqual(str(Chord(C, [P1, M3, P5, m7.transform("b"), M9, P11]).getQuality()), "Mo11")

        # Test no keyword
        self.assertEqual(str(Chord(C, [P1, P5, M7, M9, P11, M13]).getQuality()), "M13no3")
        self.assertEqual(str(Chord(C, [P1, M3, M7, M9, P11, M13]).getQuality()), "M13no5")
        self.assertEqual(str(Chord(C, [P1, M3, P5, M9, P11, M13]).getQuality()), "M13no7")
        # self.assertEqual(str(Chord(C, [P1, m3, m7.transform("b"), M9, P11]).getQuality()), "øM13nob5")
        self.assertEqual(str(Chord(C, [P1, m3, dim5, M9, P11, M13]).getQuality()), "øM13no7")

    def test_scale_properties(self):
        self.assertEqual(Scale(C, major).getHemitonia(), 2)
        self.assertEqual(Scale(C, major).getTritonia(), 1)
        self.assertEqual(Scale(C, major).countIntervals(2), 5)
        self.assertEqual(Scale(C, major).countIntervals(3), 4)
        self.assertEqual(Scale(C, major).getCardinality(), "heptatonic")
        self.assertEqual(Scale(C, major).isPrime(), False)
        self.assertEqual(Scale(C, major).getImperfections(), 1)
        self.assertEqual(Scale(C, major).getRotationalSymmetry(), [])
        self.assertEqual(Scale(C, major).getReflectionAxes(), [2])
        self.assertEqual(Scale(C, major).getIntervalVector(), "S(5)M(3)P(6)N(4)D(2)T(1)")
        self.assertEqual(Scale(C, major).isChiral(), False)
        self.assertEqual(Scale(C, major).getCohemitonic(), [])
        self.assertEqual(Scale(C, major).getPrimeMode(), "7")

if __name__ == '__main__':
    unittest.main()