import sys
import unittest

sys.path.append("../..")
from src.server.gender import Gender


class TestGender(unittest.TestCase):
    def test_male(self):
        self.assertEqual(Gender.MALE.value, 1)
        self.assertEqual(Gender.MALE.name, "MALE")

    def test_female(self):
        self.assertEqual(Gender.FEMALE.value, 2)
        self.assertEqual(Gender.FEMALE.name, "FEMALE")


if __name__ == "__main__":
    unittest.main()
