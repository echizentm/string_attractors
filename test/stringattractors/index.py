import unittest
from stringattractors.index import Index
from stringattractors.text import Text


class TestIndex(unittest.TestCase):
    def test_get(self):
        index = Index()
        text = Text('CDABCCDABCCA', [3, 6, 10, 11])

        index.make(text)
        for position, ch in enumerate(text.text):
            self.assertEqual(index.get(position), ch)


if __name__ == '__main__':
    unittest.main()
