import unittest
from interval import Interval

class test_Interval(unittest.TestCase):

    def test_add_BL_unison(self):
        self.assertEqual(P1.add_BL(M3), M3)

    def test_add_BL_positive_flat_unision(self):
        self.assertEqual(P1.add_BL(dim1), dim1)

    def test_add_BL_negative_flat_unision(self):
        self.assertEqual(P1.add_BL(-dim1), aug1)

    def test_add_BL_positive_aug_unision(self):
        self.assertEqual(P1.add_BL(aug1), aug1)

    def test_add_BL_negative_aug_unision(self):
        self.assertEqual(P1.add_BL(-aug1), dim1)

    def test_add_BL_net_positive(self):
        self.assertEqual(M3.add_BL(-M3), P1)

    def test_add_BL_net_negative(self):
        self.assertEqual((-M3).add_BL(M3), P1)

    def test_add_BL_add_positives(self):
        self.assertEqual(M3.add_BL(M3), P5)

    def test_add_BL_add_negatives(self):
        self.assertEqual((-M3).add_BL(-M3), -P5)

    def test_add_BL_add_positive_negative(self):
        self.assertEqual(M3.add_BL(-M2), M2)

    def test_add_BL_positive_axis_change(self):
        self.assertEqual(M3.add_BL(-P4), -dim2)

    def test_add_BL_negative_axis_change(self):
        self.assertEqual((-M3).add_BL(P4), dim2)

    def test_add_BL_compound(self):
        self.assertEqual((M3).add_BL(P8), M10)

    # Testing __neg__() method
    self.assertEqual(str(-P1), "-1")
    self.assertEqual(str(-dim1), "-b1")
    self.assertEqual(str(-aug1), "-#1")

    # Testing arithmetic with negative Intervals
    self.assertEqual(str(M3 - -m2), "4")    # Subtracting negative Interval produces correct result
    self.assertEqual(str(-M3 - m2), "-4")   # Subtracting two negative Intervals produces correct result
    self.assertEqual(str(-M3 + P4), "b2")   # Adding larger positive Interval to negative Interval produces correct result

    # Testing outlier cases with altered P1 Intervals
    self.assertEqual(str(M3 + dim1), "b3")
    self.assertEqual(str(M3 - dim1), "#3")
    self.assertEqual(str(M3 + aug1), "#3")
    self.assertEqual(str(M3 - aug1), "b3")

    # Testing __abs__() method
    self.assertEqual(str(abs(P1)), "1")     # Absolute value works correctly on positive P1
    self.assertEqual(str(abs(-P1)), "1")    # Absolute value works correctly on negative P1
    self.assertEqual(str(abs(m2)), "b2")    # Absolute value works correctly on positive Interval
    self.assertEqual(str(abs(-m2)), "b2")   # Absolute value works correctly on negative Interval
    #self.assertEqual(str(abs(dim1)), "b1")  # Absolute value works correctly on diminished P1
    #self.assertEqual(str(abs(-dim1)), "b1") # Absolute value works correctly on diminished P1
    #self.assertEqual(str(abs(aug1)), "#1")  # Absolute value works correctly on augmented P1
    #self.assertEqual(str(abs(-aug1)), "#1") # Absolute value works correctly on augmented P1

    # Testing __mul__() method
    self.assertEqual(str(abs(P1 * P1)), "1")