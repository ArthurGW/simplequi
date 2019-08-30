import unittest

from simplequi._colours import get_colour


class TestColours(unittest.TestCase):
    """Test cases to exercise the _colours module

    Exercises internal functions but only uses external get_colour api"""

    def assertTupleAlmostEqual(self, t1, t2, msg='', dp=3):
        """Fuzzy comparer for tuples with floating point entries"""

        for ind, vals in enumerate(zip(t1, t2)):
            v1, v2 = vals
            v1 = round(v1, dp)
            v2 = round(v2, dp)
            if v1 != v2:
                # Mismatching entry found: use normal tuple exception for nice error formatting
                self.assertTupleEqual(t1, t2)

    def test_rgb(self):
        """Test valid and invalid rgb strings"""
        data = [
            ('rgb(0, 255, 255)', (0., 1., 1., 1.)),
            ('rgb(20%, 45%, 83.2%)', (0.2, 0.45, 0.832, 1.)),
            ('rgb(25.5, 25.5, 51.00)', (0.1, 0.1, 0.2, 1.)),
        ]

        bad_data = [
            'rgb(, , )',
            'rgb(300, 123.2, 233)',
            'rgb(120%, 99%, 30%)',
        ]

        for inp, out in data:
            self.assertTupleAlmostEqual(get_colour(inp).getRgbF(), out)

        for inp in bad_data:
            self.assertRaises(ValueError, lambda: get_colour(inp))

    def test_rgba(self):
        """Test valid and invalid rgba strings"""
        self.fail('not implemented')

    def test_hsl(self):
        """Test valid and invalid hsl strings"""
        self.fail('not implemented')

    def test_hsla(self):
        """Test valid and invalid hsla strings"""
        self.fail('not implemented')

    def test_hex(self):
        """Test valid and invalid hex strings"""
        self.fail('not implemented')

    def test_named_colours(self):
        """Test named colours"""
        self.fail('not implemented')

    def test_invalid_names(self):
        """Test invalid colour strings not covered by other cases"""
        self.fail('not implemented')


if __name__ == '__main__':
    unittest.main()
