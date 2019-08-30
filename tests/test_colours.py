import unittest

from simplequi._colours import get_colour


class TestColours(unittest.TestCase):
    """Test cases to exercise the _colours module

    Exercises internal functions but only uses external get_colour api"""

    def test_rgb(self):
        """Test valid and invalid rgb strings"""
        data = [
            ('rgb(0, 255, 255)', (0, 255, 255, 255)),
            ('rgb(20%, 45%, 83.2%)', (51, 115, 212, 255)),
            ('rgb(, , )', (0, 255, 255, 255)),
            ('rgb(, , )', (0, 255, 255, 255)),
            ('rgb(, , )', (0, 255, 255, 255)),
            ('rgb(, , )', (0, 255, 255, 255)),
        ]
        for inp, out in data:
            self.assertTupleEqual(get_colour(inp).getRgb(), out)

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
