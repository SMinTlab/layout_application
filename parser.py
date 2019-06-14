import sys
import re

class Parser:
    ignore_list = []
    substitute_list = []

    def __init__(self):
        pass

    def add_ignore(self,ignore_range):
        if len(ignore_range) is not 2:
            raise Exception("Wrong expression.")
        self.ignore_list.append(ignore_range)

    def add_substitute(self,substitute_pair):
        if len(substitute_pair) is not 2:
            raise Exception("Wrong expression.")
        self.substitute_list.append(substitute_pair)

    def parse(self,text):
        for ig in self.ignore_list:
            str = "{}.*?{}".format(ig[0],ig[1])
            pat = re.compile(str)
            text = re.sub(pat,"",text)
        for sub in self.substitute_list:
            text = re.sub(sub[0],sub[1],text)
        return text

def main(path):
    ruby = ["《", "》"]
    for_printer = ["[", "]"]
    eol_to_space = ["\n", " "]
    with open(path) as f:
        s = f.read()
    print("input\n{}".format(s))
    parser = Parser()
    try:
        parser.add_ignore(ruby)
        parser.add_ignore(for_printer)
        parser.add_substitute(eol_to_space)
    except Exception as e:
        print(e)
        sys.exit(1)
    ps = parser.parse(s)
    print("parsed\n{}".format(ps))

if __name__ == "__main__":
    main(sys.argv[1])
