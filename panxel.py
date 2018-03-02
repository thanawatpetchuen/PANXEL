import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
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
        self.app.addLabelOptionBox("X:", [], row=1, column=0)
        self.app.addLabelOptionBox("Y:", [], row=1, column=1)
        self.app.setSticky("new")
        self.app.addButton("Go", self.plot, row=2, rowspan=0)
        self.app.stopLabelFrame()

        # Label Frame "Plotting"
        self.app.startLabelFrame("Plotting", row=3, rowspan=5)
        self.app.setSticky("ew")
        self.app.addLabel("Graph")
        self.app.stopLabelFrame()
        self.file = ''

    def select_file(self, btn=None):
        # Select File
        file = self.app.openBox("Select file")
        if file != '':
            self.file = file
            data_file = "global.xlsx"
            self.data = pd.read_excel(data_file)
            self.grouppredict()



    def plot(self, btn=None):
        # Plot pandas graph

        # Get option box both x, y
        self.x = self.app.getOptionBox("X:")
        self.y = self.app.getOptionBox("Y:")
        # print(self.x,self.y)

        # Create subset of data and sort
        data_ss = self.data[[self.x, self.y]]
        print(data_ss, "Data ss1")
        data = data_ss.sort_values([self.y], ascending=[False])
        print(data, "Data 1")
        # Create pivot table to plot
        ddss = data.nlargest(20,[self.y])
        print(ddss, "Daya ss2")

        # Start LabelFrame to plot
        self.app.openLabelFrame("Plotting")
        self.app.removeLabel('Graph')
        self.app.addPandasplot("pd1", ddss, width=200)
        self.app.stopLabelFrame()
        plt.show()
        print("Plot!")

    def run(self):
        self.app.go()
        self.app.setLabelFrameHeight("Setting", 2)

    def grouppredict(self):
        if is_numeric_dtype(self.data.keys):
            self.app.changeOptionBox("Y:", self.data.keys())
        if is_string_dtype(self.data.keys):
            self.app.changeOptionBox("X:", self.data.keys())
        else:
            pass


if __name__ == '__main__':
    px = panxel()
    px.run()
