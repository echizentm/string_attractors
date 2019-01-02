import unittest
from stringattractors.lz77 import LZ77


class TestLZ77(unittest.TestCase):
    def test_get(self):
        text = 'CDABCCDABCCA'

        lz77 = LZ77(text)
        self.assertEqual(lz77.attractor_list, [0, 1, 2, 3, 4, 9, 10, 11])
        self.assertEqual(lz77.factorize(), ['C', 'D', 'A', 'B', 'C', 'CDABC', 'C', 'A'])
        self.assertEqual(lz77.decode(), text)


if __name__ == '__main__':
    unittest.main()
