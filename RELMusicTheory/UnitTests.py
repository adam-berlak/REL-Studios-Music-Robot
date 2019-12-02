import unittest

from Scale import *
from Chord import *

class TestScaleMethods(unittest.TestCase):

    def test_scale_creation(self):
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])), "[C, D, E, F, G, A, B]")
        self.assertEqual(str(Scale("C#", [P1, M2, M3, P4, P5, M6, M7])), "[C#, D#, E#, F#, G#, A#, B#]")
        self.assertEqual(str(Scale("Db", [P1, M2, M3, P4, P5, M6, M7])), "[Db, Eb, F, Gb, Ab, Bb, C]")
        self.assertEqual(str(Scale("D", [P1, M2, M3, P4, P5, M6, M7])), "[D, E, F#, G, A, B, C#]")
        self.assertEqual(str(Scale("D#", [P1, M2, M3, P4, P5, M6, M7])), "[D#, E#, F##, G#, A#, B#, C##]")
        self.assertEqual(str(Scale("Eb", [P1, M2, M3, P4, P5, M6, M7])), "[Eb, F, G, Ab, Bb, C, D]")
        self.assertEqual(str(Scale("E", [P1, M2, M3, P4, P5, M6, M7])), "[E, F#, G#, A, B, C#, D#]")
        self.assertEqual(str(Scale("E#", [P1, M2, M3, P4, P5, M6, M7])), "[E#, F##, G##, A#, B#, C##, D##]")
        self.assertEqual(str(Scale("F", [P1, M2, M3, P4, P5, M6, M7])), "[F, G, A, Bb, C, D, E]")
        self.assertEqual(str(Scale("F#", [P1, M2, M3, P4, P5, M6, M7])), "[F#, G#, A#, B, C#, D#, E#]")
        self.assertEqual(str(Scale("Gb", [P1, M2, M3, P4, P5, M6, M7])), "[Gb, Ab, Bb, Cb, Db, Eb, F]")
        self.assertEqual(str(Scale("G", [P1, M2, M3, P4, P5, M6, M7])), "[G, A, B, C, D, E, F#]")
        self.assertEqual(str(Scale("G#", [P1, M2, M3, P4, P5, M6, M7])), "[G#, A#, B#, C#, D#, E#, F##]")
        self.assertEqual(str(Scale("Ab", [P1, M2, M3, P4, P5, M6, M7])), "[Ab, Bb, C, Db, Eb, F, G]")
        self.assertEqual(str(Scale("A", [P1, M2, M3, P4, P5, M6, M7])), "[A, B, C#, D, E, F#, G#]")
        self.assertEqual(str(Scale("A#", [P1, M2, M3, P4, P5, M6, M7])), "[A#, B#, C##, D#, E#, F##, G##]")
        self.assertEqual(str(Scale("Bb", [P1, M2, M3, P4, P5, M6, M7])), "[Bb, C, D, Eb, F, G, A]")
        self.assertEqual(str(Scale("B", [P1, M2, M3, P4, P5, M6, M7])), "[B, C#, D#, E, F#, G#, A#]")
        self.assertEqual(str(Scale("B#", [P1, M2, M3, P4, P5, M6, M7])), "[B#, C##, D##, E#, F##, G##, A##]")
        self.assertEqual(str(Scale("Cb", [P1, M2, M3, P4, P5, M6, M7])), "[Cb, Db, Eb, Fb, Gb, Ab, Bb]")

    def test_scale_size(self):
        self.assertEqual(str(Scale("C", [P1])), "[C]")
        self.assertEqual(str(Scale("C", [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7])), "[C, Db, D, Eb, E, F, F#, G, Ab, A, Bb, B]")

    def test_scale_indexing(self):
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1]), "C")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[7]), "B")

    def test_scale_next_previous(self):
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].previous()), "B")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[7].next()), "C")

    def test_scale_arithmetic(self):
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1] - 2), "B")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[7] + 2), "C")

        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1] - 16), "B")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1] + 16), "D")

        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1] - m2), "B")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[7] + m2), "C")

        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1] - m9), "B")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[7] + m9), "C")

    def test_scale_contains(self):
        self.assertEqual("C" in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual("C#" in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), False)

        self.assertEqual(M2 in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(M9 in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(dim5 in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), False)

        self.assertEqual([P1, M3, P5] in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual([P1, M3, M9] in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual([P1, M3, dim5, P5] in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), False)

        self.assertEqual(Scale("C", [P1, M2, M3, P4, P5, M6]) in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(Scale("C", [P1, M2, M3, P4, P5, m6, M6, M7]) in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), False)

        self.assertEqual(Chord("C", Chord.stringToPitchClass("maj7")) in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), True)
        self.assertEqual(Chord("C", Chord.stringToPitchClass("maj9b5")) in Scale("C", [P1, M2, M3, P4, P5, M6, M7]), False)

    def test_pitch_class_to_scale_steps(self):
        self.assertEqual(Scale.pitchClassToScaleSteps([P1, M2, M3, P4, P5, M6, M7]), [2, 2, 1, 2, 2, 2, 1])
        self.assertEqual(Scale.pitchClassToScaleSteps([P1, M3, P5]), [4, 3, 5])

    def test_build_chord(self):
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 0)), "]")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 1)), "[C]")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7)), "[C, E, G, B, D, F, A]")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 8)), "[C, E, G, B, D, F, A, C]")

        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 1)), "[C, C, C, C, C, C, C]")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 2)), "[C, D, E, F, G, A, B]")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 7)), "[C, B, A, G, F, E, D]")
        self.assertEqual(str(Scale("C", [P1, M2, M3, P4, P5, M6, M7])[1].build(Chord, 7, 8)), "[C, B, A, G, F, E, D, C]")

    def test_string_to_pitch_class(self):
        self.assertEqual(str(Chord.stringToPitchClass("maj7")), "[1, 3, 5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("maj7b5")), "[1, 3, b5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj5")), "[1, b3, 5]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7")), "[1, b3, 5, 7]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7b7")), "[1, b3, 5, b7]")
        self.assertEqual(str(Chord.stringToPitchClass("minmaj7b9")), "[1, b3, 5, 7]")



if __name__ == '__main__':
    unittest.main()