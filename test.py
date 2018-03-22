import pandas as pd
from appJar import *
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


class panxel:
    def __init__(self):
        self.app = gui("PANXEL", "660x720")

        # Label Frame "Setting"
        self.app.startLabelFrame("Setting", row=0)
        self.app.setPadding(20)
        self.app.setStretch("both")
        self.app.setSticky("new")
        self.app.addMenuList("File", ["Open..."], self.select_file)
        self.app.addLabelTickOptionBox("X:", [], row=1, column=0)
        self.app.addLabelTickOptionBox("Y:", [], row=1, column=1)
        self.app.setSticky("new")
        self.app.addButton("Go", self.plot, row=2, rowspan=0)
        self.app.stopLabelFrame()

        # Label Frame "Plotting"
        self.app.startLabelFrame("Plotting", row=3, rowspan=5)
        self.app.setSticky("ew")
        self.app.addLabel("Graph")
        self.app.stopLabelFrame()

        self.file = ''
        self.plot_count = False
        self.addOp = False
        self.list_optionbox = []
        self.current_row = 2

    def select_file(self, btn=None):
        # Select File
        file = self.app.openBox("Select file")
        if file != '':
            self.file = file
            data_file = "global.xlsx"
            self.data = pd.read_excel(data_file)
            self.app.changeOptionBox("X:", self.data.keys())
            self.app.changeOptionBox("Y:", self.data.keys())


    def plot(self, btn=None):
        # Plot pandas graph

        # Get option box both x, y
        x = self.app.getOptionBox("X:")
        y = self.app.getOptionBox("Y:")
        xs = [k for k, v in x.items() if v]
        ys = [k for k, v in y.items() if v]

        print("X: ", xs)
        print("Y: ", ys)

        if self.addOp:
            select_stack = []
            getall = self.app.getAllOptionBoxes()
            for item in self.list_optionbox:
                select_stack.append(getall[item])
            print("ASD", select_stack)
        else:
            for item in xs:
                self.app.addOptionBox("Select {}".format(item), self.data[item].unique(), row=self.current_row)
                self.list_optionbox.append("Select {}".format(item))
                self.current_row += 1
                self.addOp = True
            data_ss = self.data[xs + ys]
            data = data_ss.sort_values(ys, ascending=[False])
            ddss = data.head(20).pivot_table(index=xs)
            self.__plot(ddss)

        # if xs == ['Country']:
        #     if self.addOp:
        #         select = self.app.getOptionBox("Select s")
        #         data_ss = self.data[xs+ys]
        #         self.data_ss = data_ss.loc[data_ss[xs[0]] == select]
        #         self.data_sorted = self.data_ss.sort_values(ys, ascending=[False])
        #         ddss = self.data_sorted.head(20)
        #         self.__plot(ddss)
        #     else:
        #         self.app.addOptionBox("Select s", self.data[xs[0]].unique(), row=2)
        #         self.addOp = True
        #         data_ss = self.data[xs + ys]
        #         data = data_ss.sort_values(ys, ascending=[False])
        #         ddss = data.head(20).pivot_table(index=xs)
        #         self.__plot(ddss)
        #
        # # Create subset of data and sort
        # else:
        #     data_ss = self.data[xs + ys]
        #     data = data_ss.sort_values(ys, ascending=[False])
        #     ddss = data.head(20).pivot_table(index=xs)
        #     self.__plot(ddss)





        # Create pivot table to plot

        # print(ddss)
        #
        # # Start LabelFrame to plot
        # self.app.openLabelFrame("Plotting")
        # if self.plot_count:
        #     print("2 time")
        #     self.app.updatePandas("pd1", ddss)
        # else:
        #     self.app.removeLabel('Graph')
        #     self.app.addPandasplot("pd1", data_ss.head(), width=200)
        #     self.app.stopLabelFrame()
        #     plt.show()
        #     self.plot_count = True
        #     print("1 time")
        #     print("Plot!")

    def __plot(self, ddss):
        # Start LabelFrame to plot
        self.app.openLabelFrame("Plotting")
        if self.plot_count:
            print("2 time")
            self.app.updatePandas("pd1", ddss)
        else:
            self.app.removeLabel('Graph')
            self.app.addPandasplot("pd1", ddss, width=200)
            self.app.stopLabelFrame()
            plt.show()
            self.plot_count = True
            print("1 time")
            print("Plot!")
    def run(self):
        self.app.go()
        self.app.setLabelFrameHeight("Setting", 2)


if __name__ == '__main__':
    px = panxel()
    px.run()
