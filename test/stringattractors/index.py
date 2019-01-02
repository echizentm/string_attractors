import itertools
import unittest
from stringattractors.index import Index
from stringattractors.text import Text


class TestIndex(unittest.TestCase):
    def test_get(self):
        raw_text_list = [
            'CDABCCDABCCA',
            'abracadabra',
            'みるみるミルキィ',
            'ケアルケアルラケアルダケアルガケアルジャ',
            '働きたくない私は働きたくない私の働きたくない気持ちを大切にして働きたくない',
        ]
        alpha_list = [1, 2, 3, 4, 5]

        for raw_text, alpha in itertools.product(raw_text_list, alpha_list):
            text = Text(raw_text)
            index = Index(alpha=alpha)

            index.make(text)
            for position, ch in enumerate(text.text):
                self.assertEqual(index.get(position), ch)


if __name__ == '__main__':
    unittest.main()
