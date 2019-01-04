import unittest
from stringattractors.text import Text


class TestText(unittest.TestCase):
    def test_attractor_list(self):
        text = Text('CDABCCDABCCA')
        self.assertEqual(text.attractor_list, [0, 1, 2, 3, 4, 9, 10, 11])

    def test_marked_text(self):
        text = Text('CDABCCDABCCA', [3, 6, 10, 11])
        self.assertEqual(text.marked_text, 'CDA[B]CC[D]ABC[C][A]')

    def test_is_string_attractors(self):
        text = Text('CDABCCDABCCA', [3, 6, 10, 11])
        self.assertTrue(text.is_string_attractors())

        text = Text('CDABCCDABCCA', [3, 6, 10])
        self.assertFalse(text.is_string_attractors())

    def test_make_coordinate(self):
        text = Text('CDABCCDABCCA', [3, 6, 10, 11])

        coordinate = text.make_coordinate('ABC')
        self.assertEqual(coordinate.attractor, 3)
        self.assertEqual(coordinate.offset, 1)
        self.assertEqual(coordinate.position, 2)

        self.assertIsNone(text.make_coordinate('ABD'))


if __name__ == '__main__':
    unittest.main()
