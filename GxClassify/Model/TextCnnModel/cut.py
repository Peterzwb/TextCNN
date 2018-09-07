import re
import jieba
import os
from Application import Application

class Cut(object):

    f = open(os.path.join(Application.base_dir, r'Model\TextCnnModel\user_dict\dict.txt'))
    jieba.load_userdict(f)
    patten = re.compile(r'[A-Za-z]+')

    @classmethod
    def cut(cls,s):

        result = jieba.lcut(s)

        return result

    @classmethod
    def cut_word(cls,s):

        y = []
        result = []

        for word in s:
            if cls.patten.match(word) !=  None:
                y.append(word)
            else:
                if len(y) > 0:
                    result.append(''.join(y))
                    y = []
                if word != ',':
                    result.append(word)

        return result



