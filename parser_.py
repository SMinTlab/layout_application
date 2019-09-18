import sys
import re
import MeCab

class Token():
    words = None
    postags = None
    clause_index = None

    def __init__(self, text, dep_num):
        self.words = []
        self.postags = []
        self.clause_index = []
        mecab = MeCab.Tagger('-d C:\PROGRA~1\MeCab\dic\mecab-ipadic-neologd')
        #mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        mecab.parse('')
        node = mecab.parseToNode(text)
        while node:
            word = node.surface
            self.words.append(word)
            pos = node.feature.split(',')[0]
            self.postags.append(pos)
            print("{} {}".format(word, pos))
            node = node.next
        i = 0
        while i in range(len(self.postags)):
            if self.postags[i] == Parser.prefix:
                clause = []
                j = 0
                while self.postags[i+j] in Parser.prefix:
                    clause.append(i+j)
                    j += 1
                k = 0
                while self.postags[i+j+k] in Parser.dependents and k < dep_num:
                    clause.append(i+j+k)
                    k += 1
                if k == 0:
                    print("Wrong structure found.")
                    c = ""
                    p = ""
                    for idx in range(i-10,i+j+1):
                        c += self.words[idx]+" "
                        p += self.postags[idx]+" "
                    print("{}({})".format(c,p))
                    #sys.exit(1)
                l = 0
                while self.postags[i+j+k+l] in Parser.suffix or self.postags[i+j+k+l] in Parser.independents:
                    clause.append(i+j+k+l)
                    l += 1
                self.clause_index.append(clause)
                i += j + k + l - 1
            elif self.postags[i] in Parser.dependents:
                clause = []
                j = 0
                while self.postags[i+j] in Parser.dependents and j < dep_num:
                    clause.append(i+j)
                    j += 1
                k = 0
                while self.postags[i+j+k] in Parser.suffix or self.postags[i+j+k] in Parser.independents:
                    clause.append(i+j+k)
                    k += 1
                self.clause_index.append(clause)
                i += j + k - 1
            else:
                print("ignored {}: {}({})".format(i,self.words[i],self.postags[i]))
            i += 1

class Parser:
    ignore_list = None
    substitute_list = None
    dependents = frozenset(["名詞","動詞","形容詞","連体詞","副詞", "感動詞","フィラー","接続詞"])
    independents = frozenset(["助詞","助動詞","記号"])
    prefix = "接頭詞"
    suffix = frozenset(["接尾詞"])

    def __init__(self):
        self.ignore_list = []
        self.substitute_list = []

    def add_ignore(self,ignore_range):
        if len(ignore_range) is not 2:
            raise Exception("Wrong expression.")
        self.ignore_list.append(ignore_range)

    def add_substitute(self,substitute_pair):
        if len(substitute_pair) is not 2:
            raise Exception("Wrong expression.")
        self.substitute_list.append(substitute_pair)

    def parse(self,text,dep_num):
        for ig in self.ignore_list:
            pat_str = "{}.*?{}".format(ig[0],ig[1])
            pat = re.compile(pat_str)
            text = re.sub(pat,"",text)
        for sub in self.substitute_list:
            text = re.sub(sub[0],sub[1],text)
        print(text)
        token = Token(text,dep_num)
        #print(token.clause_index)
        for clause in token.clause_index:
            c = ""
            p = ""
            for i in clause:
                c += token.words[i]
                c += " "
                p += token.postags[i]
                p += " "
            if len(c)/2 > 0:
                print("{}({})".format(c, p))
        return token

def main(path):
    ruby = ["《", "》"]
    for_printer1 = ["[", "]"]
    for_printer2 = ["［","］"]
    #eol_to_space = ["\n", " "]
    with open(path) as f:
        s = f.read()
    #print("input\n{}".format(s))
    parser = Parser()
    try:
        parser.add_ignore(ruby)
        parser.add_ignore(for_printer1)
        parser.add_ignore(for_printer2)
        #parser.add_substitute(eol_to_space)
    except Exception as e:
        print(e)
        sys.exit(1)
    s.strip()
    ps = parser.parse(s,sys.maxsize)
    #print("parsed\n{}".format(ps))

if __name__ == "__main__":
    main(sys.argv[1])
