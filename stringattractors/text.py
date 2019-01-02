from typing import Optional, Sequence
from .lz77 import LZ77


class Text:
    '''
    string attractors を持つ文字列
    '''
    __slots__ = ['text', 'attractor_list']

    def __init__(self, text: str, attractor_list: Optional[Sequence[int]] = None) -> None:
        '''
        :param text: 文字列
        :param attractor_list: string attractors
        '''
        if attractor_list is None:
            attractor_list = LZ77(text).attractor_list

        self.text = text
        self.attractor_list = attractor_list

    @property
    def marked_text(self) -> str:
        '''
        :return: string attractor の位置を [] で囲んだ文字列
        '''
        return ''.join([
            f'[{ch}]' if position in self.attractor_list else ch
            for position, ch in enumerate(self.text)
        ])

    def is_string_attractors(self) -> bool:
        '''
        :return: string attracgtors の要件を満たしているかどうか
        '''
        return all([
            self.make_coordinate(self.text[begin:end])
            for begin in range(len(self.text))
            for end in range(begin + 1, len(self.text) + 1)
        ])

    def make_coordinate(self, query: str) -> Optional['Coordinate']:
        '''
        :param query: クエリ文字列
        :return: クエリにマッチし、かつ string attractor を含む部分文字列の位置
        '''
        position = -1
        while True:
            try:
                position = self.text.index(query, position + 1)
            except ValueError:
                return None
            for attractor in self.attractor_list:
                if attractor in range(position, position + len(query)):
                    return Coordinate(attractor, attractor - position)


class Coordinate:
    '''
    文字列上の位置を string atteactor と
    string attractor までのオフセットで表現したもの
    '''
    __slots__ = ['attractor', 'offset']

    def __init__(self, attractor: int, offset: int) -> None:
        '''
        :param attractor: string attractor
        :param offset: string attractor までのオフセット
        '''
        self.attractor = attractor
        self.offset = offset

    @property
    def position(self) -> int:
        '''
        :return: 文字列上の位置
        '''
        return self.attractor - self.offset
