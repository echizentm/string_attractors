from typing import List, Optional, Tuple


class LZ77:
    '''
    LZ77 によって圧縮された文字列
    '''
    __slots__ = ['directive_list']

    def __init__(self, text: str) -> None:
        '''
        :param text: 圧縮する文字列
        '''
        self.directive_list = self._make_directive_list(text)

    @property
    def attractor_list(self) -> List[int]:
        '''
        :return: string attractor のリスト
        '''
        index = -1
        attractor_list = []
        for begin, end, ch in self.directive_list:
            index += end - begin
            attractor_list.append(index)
        return attractor_list

    def factorize(self) -> List[str]:
        '''
        :return: 元のテキストを factor のリストにしたもの
        '''
        text = ''
        factor_list = []
        for begin, end, ch in self.directive_list:
            factor = ch if ch else text[begin:end]
            factor_list.append(factor)
            text += factor
        return factor_list

    def decode(self) -> str:
        '''
        :return: 元のテキストを復元したもの
        '''
        return ''.join(self.factorize())

    def _make_directive_list(self, text: str) -> List[Tuple[int, int, Optional[str]]]:
        directive_list: List[Tuple[int, int, Optional[str]]] = []
        begin = 0
        while begin < len(text):
            index = begin
            subtext = text[begin]
            ch: Optional[str] = text[begin]
            for end in range(begin + 1, len(text) + 1):
                new_subtext = text[begin:end]
                new_index = text.find(new_subtext)
                if new_index == -1 or new_index + len(new_subtext) > begin:
                    break

                index = new_index
                subtext = new_subtext
                ch = None

            directive_list.append((index, index + len(subtext), ch))
            begin += len(subtext)

        return directive_list
