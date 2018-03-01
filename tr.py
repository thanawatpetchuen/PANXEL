from appJar import *
import pandas as pd

class tr:
    def __init__(self):
        self.app = gui("TR", "500x500")

        data_file = "global.xlsx"
        self.data = pd.read_excel(data_file)
        dlist = self.data.keys()
        print(len(dlist))
        print(dlist[23])
        self.app.addLabelTickOptionBox("P", dlist)
        self.app.addButton("Click me ", self.gettick)
        self.app.startLabelFrame("data")
        ic = 0
        for r in range(len(dlist)):
            for c in range(6):
                if ic == len(dlist):
                    break
                else:
                    self.app.addLabel("b{}{}".format(r, c), dlist[ic], row=r, column=c)
                    ic += 1
        self.app.stopLabelFrame()

    def gettick(self, btn=None):
        gt = self.app.getOptionBox("P")
        foodict = [k for k, v in gt.items() if v]

        print(foodict)

    def run(self):
        self.app.go()


if __name__ == '__main__':
    tt = tr()
    tt.run()
