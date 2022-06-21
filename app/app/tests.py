
"""
Sample tests
"""

from django.test import SimpleTestCase

from app import calc


class CalcTest(SimpleTestCase):
    """Test for cal. module"""

    def test_add(self):
        """Test for add function"""
        result = calc.add(1, 2)
        self.assertEqual(result, 3)

    def test_subtract_numbers(self):
        """Test for subtract function"""
        result = calc.subtract(1, 2)
        self.assertEqual(result, -1)
