import collections

class martinLuther:
    def __init__(self):
        self.file = 'martin.txt'
        self.words = []

    def readFile(self):
        self.f = open(self.file, 'r')
        self.raw_text = self.f.readlines()
        i = 0
        for row in self.raw_text:
            eachRow = row.split(" ")
            for row2 in eachRow:
                # print(row2)
                if row2 == 'ring!\n':
                    print(row2)
                row2.replace("\n", '')
                row2.replace(",", '')
                row2.replace(".", '')
                row2.replace("!", '')
                # if row2 == 'ring':
                #     print(row2)

                # print(row2, "After")
                self.words.append(row2)


    def wordCount(self, n):
        newWord = [word.replace(",", '') for word in self.words]
        newWord = [word.replace("!", '') for word in newWord]
        newWords = [word.replace(".", '') for word in newWord]
        newWords = [word.replace('\n', '') for  word in newWords]
        a = collections.Counter(newWords).most_common(n)
        print(a)
        # for item in a:
        #     print(item)

if __name__ == '__main__':
    ml = martinLuther()
    ml.readFile()
    ml.wordCount(15)