class Log:
    data = None
    example_num = 5
    splitter = ','
    omit = '...'

    def __init__(self,time,text):
        self.data = {'time':time, 'text':text}

    def __str__(self):
        ret = ''
        for k in self.data:
            item = ''
            if k == 'text' and len(self.data[k])>self.example_num:
                for i in range(self.example_num):
                    item+=str(self.data[k])[i]
                item+=self.omit
            else:
                item+=str(self.data[k])
            item+=self.splitter
            ret+=item
        ret = ret[:-len(self.splitter)]
        return ret

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    l = []
    l.append(Log(0,'long_test'))
    l.append(Log(0,'test'))
    print(l)
