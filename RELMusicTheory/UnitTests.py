import unittest

from Scale import *
from Chord import *
from Configuration import *

class TestScaleMethods(unittest.TestCase):

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
        self.assertEqual(Scale.scaleStepsToPitchClass([4, 3, 5, 2]), [P1, M3, P5, M9])

    def test_build_chord(self):
        self.assertEqual(str(Scale(C, [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 0).printTones()), "[]")
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
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7no5sus2")), "[1, 2, b3, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("mindom7")), "[1, b3, 5, b7]")
        self.assertEqual(str(Chord.stringToPitchClass("domdom7")), "[1, 3, 5, b7]")

if __name__ == '__main__':
    unittest.main()