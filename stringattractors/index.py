import bisect
import math
from typing import List, Optional, Sequence
from .text import Coordinate, Text

PAD = '*'


class Index:
    '''
    文字列と、その string attractors から作られる
    任意の位置の文字を取得可能なインデックス
    '''
    __slots__ = [
        'alpha', 'tau',
        '_block_list_list', '_coordinate_list_list', '_last_block_str_list',
    ]

    def __init__(self, alpha: int = 1, tau: int = 2) -> None:
        '''
        :param alpha: ブロックがこのサイズになったらまるごと保存する
        :param tau: ブロックをいくつに分割するかを表すパラメータ
        '''
        if alpha < 1:
            raise Exception('alpha は1以上の整数を与えてください')
        if tau < 2:
            raise Exception('tau は2以上の整数を与えてください')

        self.alpha = alpha
        self.tau = tau
        self._block_list_list: List[List['Block']] = []
        self._coordinate_list_list: List[List[Optional[Coordinate]]] = []
        self._last_block_str_list: List[str] = []

    def make(self, text: Text) -> None:
        '''
        インデックスを作る

        :param text: string attractors つき文字列
        '''
        block_length = None
        while (block_length is None) or (block_length >= 2 * self.alpha):
            block_list = self._make_next_block_list(text, block_length)
            if len(block_list) == 0:
                raise Exception('ブロックが1つも作れませんでした')
            block_length = block_list[0].length
            coordinate_list = self._make_coordinate_list(text, block_list)
            block_str_list = self._make_block_str_list(text, block_list)

            self._block_list_list.append(block_list)
            self._coordinate_list_list.append(coordinate_list)
            self._last_block_str_list = block_str_list

    def get(self, position: int) -> str:
        '''
        :param position: 取得する位置
        :return: 指定した位置にある文字
        '''
        return self._get_recursive(position, 0)

    def _make_next_block_list(
        self, text: Text, block_length: Optional[int] = None
    ) -> List['Block']:
        if block_length is None:
            return self._make_first_block_list(text)

        next_block_length = math.ceil(block_length / self.tau)
        next_block_list: List['Block'] = []
        for attractor in text.attractor_list:
            # 論文では attractor は前半ブロックに含めていますが
            # 実装を綺麗にするために attractor を後半ブロックに含めます
            begin = attractor - next_block_length * self.tau
            end = attractor + next_block_length * self.tau
            next_block_list += [
                Block(begin, next_block_length)
                for begin in range(begin, end, next_block_length)
            ]
        return next_block_list

    def _make_first_block_list(self, text: Text) -> List['Block']:
        block_length = math.ceil(len(text.text) / len(text.attractor_list))
        return [
            Block(begin, block_length)
            for begin in range(0, len(text.text), block_length)
        ]

    def _make_coordinate_list(
        self, text: 'Text', block_list: Sequence['Block']
    ) -> List[Optional[Coordinate]]:
        return [self._make_coordinate(text, block) for block in block_list]

    def _make_coordinate(self, text: Text, block: 'Block') -> Optional[Coordinate]:
        if block.end <= 0:
            return None
        return text.make_coordinate(text.text[max(block.begin, 0):block.end])

    def _make_block_str_list(
        self, text: 'Text', block_list: Sequence['Block']
    ) -> List[str]:
        return [self._make_block_str(text, block) for block in block_list]

    def _make_block_str(self, text: Text, block: 'Block') -> str:
        return ''.join([
            text.text[position] if position >= 0 and position < len(text.text) else PAD
            for position in range(block.begin, block.end)
        ])

    def _get_recursive(self, position: int, level: int) -> str:
        block_position = self._get_block_position(position, level)

        block = self._block_list_list[level][block_position]
        block_str = self._last_block_str_list[block_position]
        coordinate = self._coordinate_list_list[level][block_position]
        if coordinate is None:
            raise Exception('coordinate が不正です')

        if level == len(self._block_list_list) - 1:
            return block_str[position - block.begin]

        offset = position - block.begin
        return self._get_recursive(coordinate.position + offset, level + 1)

    def _get_block_position(self, position: int, level: int) -> int:
        block_list = self._block_list_list[level]

        if level == 0:
            return bisect.bisect([block.end for block in block_list], position)

        # 1つの string attractor に対して 2 * tau 個のブロックが
        # 連続した位置に割り当てられています
        # この連続ブロック内では end は昇順になっています
        # 一方で連続ブロック同士は位置が重なっている可能性があります
        # なので最初に連続ブロックの全体の end に対して search を行い
        # その後、連続ブロック内で search するという2段階の search をします
        cons_block_num = 2 * self.tau

        block_position = bisect.bisect(
            [block.end for i, block in enumerate(block_list) if (i + 1) % cons_block_num == 0],
            position,
        ) * cons_block_num

        return bisect.bisect([
            block.end
            for block in block_list[block_position:block_position + cons_block_num]
        ], position) + block_position


class Block:
    '''
    文字列上の部分文字列(ブロック)を
    開始位置とブロックの長さで表現したもの
    '''
    __slots__ = ['begin', 'length']

    def __init__(self, begin: int, length: int) -> None:
        '''
        :param begin: ブロックの開始位置
        :param length: ブロックの長さ
        '''
        self.begin = begin
        self.length = length

    @property
    def end(self) -> int:
        '''
        :return: ブロックの終端位置
        '''
        return self.begin + self.length
