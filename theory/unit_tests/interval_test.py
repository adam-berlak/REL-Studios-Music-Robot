import unittest
from interval import Interval

class test_Interval(unittest.TestCase):

    def test_add_BL_unison(self):

    def test_add_BL_add_positives(self):

    def test_add_BL_add_negatives(self):

    def test_add_BL_positive_axis_change(self):

    def test_add_BL_negative_axis_change(self):

    # Testing __neg__() method
    self.assertEqual(str(-P1), "-1")
    self.assertEqual(str(-dim1), "-b1")
    self.assertEqual(str(-aug1), "-#1")

    # Testing general arithmetic
    self.assertEqual(str(P1 + M3), "3")     # Adding to P1 does not change Interval
    self.assertEqual(str(m2 + M3), "4")     # Adding two positive Intervals produces correct result
    self.assertEqual(str(M3 - M3), "1")     # Subtracting Interval by itself produces P1
    self.assertEqual(str(M3 - P4), "-b2")   # Subtracting an Interval from a smaller Interval produces correct result

    # Testing arithmetic with negative Intervals
    self.assertEqual(str(M3 - -m2), "4")    # Subtracting negative Interval produces correct result
    self.assertEqual(str(-M3 - m2), "-4")   # Subtracting two negative Intervals produces correct result
    self.assertEqual(str(-M3 + M3), "1")    # Adding Interval to its opposite produces P1
    self.assertEqual(str(-M3 + P4), "b2")   # Adding larger positive Interval to negative Interval produces correct result
    self.assertEqual(str(-P1 + P4), "4")    # Negative P1 works correctly

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