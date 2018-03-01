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

        # Create subset of data and sort
        data_ss = self.data[xs+ys]
        data = data_ss.sort_values(ys, ascending=[False])

        # Create pivot table to plot
        ddss = data.head(20).pivot_table(index=xs)
        print(ddss)

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
