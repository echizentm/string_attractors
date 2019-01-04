import unittest
from stringattractors.index import Index
from stringattractors.text import Text


class TestIndex(unittest.TestCase):
    def test_get(self):
        raw_text_list = [
            'CDABCCDABCCA',
            'aaaaaaaabbbbbbbb',
            'abracadabra',
            'みるみるミルキィ',
            'ケアルケアルラケアルダケアルガケアルジャ',
            '働きたくない私は働きたくない私の働きたくない気持ちを大切にして働きたくない',
        ]

        for raw_text in raw_text_list:
            text = Text(raw_text)
            index = Index()

            index.make(text)
            for position, ch in enumerate(text.text):
                self.assertEqual(index.get(position), ch)


if __name__ == '__main__':
    unittest.main()
