"""
A Sentence as a sequence of words.
"""
import re
import reprlib

RE_WORD  = re.compile('\w+')

class Sentence(object):

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    # def __getitem__(self, index):
    #     return self.words[index]

    def __iter__(self):
        for word in self.words:
            yield word
        # return

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return "{sentence}".format(sentence=reprlib.repr(self.text))

if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s)
    for word in s:
        print(word)
    # print(s[0])
