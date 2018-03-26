# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\asd.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_file = "global.xlsx"
# data = pd.read_excel(data_file)
#
# datak = data.keys()
datak = ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
       'Customer ID', 'Customer Name', 'Segment', 'Postal Code', 'City',
       'State', 'Country', 'Region', 'Market', 'Product ID', 'Category',
       'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount',
       'Profit', 'Shipping Cost', 'Order Priority']
print(datak)

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def __init__(self, df):
        MyMplCanvas.__init__(self)
        self.df = df

    def compute_initial_figure(self):
        self.df.plot(kind="bar", ax=self.axes)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        pass
        # self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self, df):
        self.axes.cla()
        df.plot(kind="bar", ax=self.axes)
        self.draw()


class ListS(QtWidgets.QListWidget):
    def __init__(self, title, parent, who, a, b, c, d):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)

        # self.setGeometry(QtCore.QRect(170, 20, 401, 31))
        self.setGeometry(QtCore.QRect(a, b, c, d))
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setAlternatingRowColors(True)
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setViewMode(QtWidgets.QListView.ListMode)
        if who == 'dimension':
            self.setStyleSheet("QListWidget::item {"
         "border-style: outset;"
         "border-width:1px;"
         "border-color:black;"
         "background-color: rgb(51, 204, 51);"
        "border-radius:70px;}"
      "QListWidget::item:selected {"
         "background-color: rgb(40, 164, 40);"
      "}")
        else:
            self.setStyleSheet("QListWidget::item {"
         "border-style: outset;"
         "border-width:1px;"
         "border-color:black;"
         "background-color: rgb(102, 153, 255);"
        "border-radius:70px;}"
      "QListWidget::item:selected {"
         "background-color: rgb(0, 85, 255)"
      "}")
        self.setObjectName(title)

        self.dimension =[]
        self.measurement =[]

    def currentItemChanged(self, QListWidgetItem, QListWidgetItem_1):
        print("ASD")

    # def dragEnterEvent(self, e):
    #     if e.mimeData().hasFormat('text/plain'):
    #         e.ignore()
    #     else:
    #         print("ASDss")
    #         e.acccept()


    def _addItem(self, name):
        self.addItem(name)
        print("ASd")


    def dropEvent(self, QDropEvent):
        # self.addItem(QDropEvent.mimeData())
        mdd = QDropEvent.mimeData()

        if(QDropEvent.mimeData().hasFormat('application/x-qabstractitemmodeldatalist')):
            QDropEvent.accept()
            # QDropEvent.setDropAction(QtCore.Qt.MoveAction)
            name = QDropEvent.mimeData().data('application/x-qabstractitemmodeldatalist')
            # mm = QtCore.QTextCodec.availableCodecs(name)

            namees = name.data().decode('utf-8')
            itemname = "".join(i for i in namees if i.isalpha() or i == '-' or i == ' ')
            print(itemname)

            self.dimension.append(itemname)
            self.addItem(itemname)


        # print(QDropEvent.dropAction())
        # self._addItem(QDropEvent.source().text())
        # print(self.addItem("asd"))
        # items = []
        # for i in range(self.listWidget.count()):
        #     items.append(self.listWidget.item(i))
        # labels = [i.text() for i in items]
        # print(labels)
        # QDropEvent.accept()
        # QDropEvent.acceptProposedAction()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(778, 526)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 771, 501))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(680, 420, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 420, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.clickOnMe)

        self.listWidget = ListS("listWidget", self.tab, "dimension", 170, 20, 401, 31)

        self.listWidget_2 = QtWidgets.QListWidget(self.tab)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 20, 161, 171))
        self.listWidget_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_2.setObjectName("listWidget_2")
        for item in datak:
            items = QtWidgets.QListWidgetItem(item)
            self.listWidget_2.addItem(items)
        self.listWidget_3 = QtWidgets.QListWidget(self.tab)
        self.listWidget_3.setGeometry(QtCore.QRect(0, 210, 161, 201))
        self.listWidget_3.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_3.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_3.setObjectName("listWidget_3")
        for item in datak:
            items = QtWidgets.QListWidgetItem(item)
            self.listWidget_3.addItem(items)

        self.listWidget_4 = ListS("listWidget", self.tab, "measurement", 170, 60, 401, 31)

        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(0, 0, 161, 20))
        self.label.setStyleSheet("background-color:rgb(175, 254, 255);\n"
"alternate-background-color: rgb(169, 247, 255);")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(0, 190, 161, 20))
        self.label_3.setStyleSheet("background-color:rgb(175, 254, 255);\n"
"alternate-background-color: rgb(169, 247, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setGeometry(QtCore.QRect(170, 100, 411, 311))
        self.widget.setObjectName("widget")

        l = QtWidgets.QVBoxLayout(self.widget)
        self.sc = MyDynamicMplCanvas(self.tab, width=10, height=2, dpi=100)
        l.addWidget(self.sc)

        self.listWidget_5 = QtWidgets.QHBoxLayout(self.tab)
        self.listWidget_5.setGeometry(QtCore.QRect(590, 20, 171, 111))
        self.listWidget_5.setObjectName("listWidget_5")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(590, 0, 171, 16))
        self.label_2.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(590, 20, 161, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 420, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        # self.frame = QtWidgets.QFrame(self.verticalLayoutWidget)
        # self.frame.setStyleSheet("background-color: rgb(198, 255, 203);")
        # self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame.setObjectName("frame")
        # self.verticalLayout.addWidget(self.frame)
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.listWidget.raise_()
        self.listWidget_2.raise_()
        self.listWidget_3.raise_()
        self.listWidget_4.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.widget.raise_()
        self.label_2.raise_()
        self.verticalLayoutWidget.raise_()
        self.pushButton_3.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 778, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuOption = QtWidgets.QMenu(self.menubar)
        self.menuOption.setObjectName("menuOption")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menu.addAction(self.actionOpen)
        self.menuOption.addSeparator()
        self.menuOption.addSeparator()
        self.menuOption.addSeparator()
        self.menuOption.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuOption.menuAction())

        self.time_count = False

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PANXEL"))
        self.pushButton.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_2.setText(_translate("MainWindow", "OK"))
        self.pushButton_3.setText(_translate("MainWindow", "Refresh"))
        self.label.setText(_translate("MainWindow", "                  Dimention"))
        self.label_3.setText(_translate("MainWindow", "              Measurements"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.menuOption.setTitle(_translate("MainWindow", "Option"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))

    def clickOnMe(self):
        data_file = "global.xlsx"

        if not self.time_count:
            self.data = pd.read_excel(data_file)
                    # self.time_count = 0

            datak = self.data.keys()
            print(datak)

            dim = self.listWidget.dimension
            meas = self.listWidget_4.dimension


            for item in dim:
                combobox = QtWidgets.QComboBox()
                combobox.setObjectName("combobox>{}".format(item))
                print("combobox>{}".format(item))
                combobox.addItems(self.data[item].unique())
            #
                self.verticalLayout.addWidget(combobox)

            print(dim, "Dimension")
            print(meas, "Measurement")

            # data_ss = data[['Country', 'Category', 'Sales']]
            data_ss = self.data[dim+meas]
            # data_sss = data_ss.loc[data_ss['Country'] == "Italy"]
            # data_cat = data_sss.loc[data_sss['Category'].isin(['Technology'])]
            # sum_cat = data_sss.groupby('Category')['Sales'].sum()

            pdf = self.data.pivot_table(index=['Country', 'Category'], values=['Sales'], aggfunc=np.sum)

            # data_sorted = data_ss.sort_values(['Sales'], ascending=False)
            # datas = data_sss.sort_values(['Sales'], ascending=[False])
            # ddss = data_sss.pivot_table(index=['Category'])

            # print(data_ss)
            # print(data_sss)
            # print(sum_cat)
            # print(data['Country'].unique())
            # print(pdf)

            # pdf.head().plot.bar()
            # plt.show()
            self.sc.update_figure(pdf.head())
            self.time_count = True
        else:
            print("SEY")
            # self.first_time = False
            dim = self.listWidget.dimension
            meas = self.listWidget_4.dimension

            self.dim_dict = {}

            # child = self.tab.findChild(QtWidgets.QComboBox, "combobox>Country")
            # print(child.currentText())
            for item in dim:
                child = self.tab.findChild(QtWidgets.QComboBox, "combobox>{}".format(item))
                # child = QtCore.Qt.FindDirectChildrenOnly(QtWidgets.QComboBox, "combobox>{}".format(item))
                # child = QtWidgets.QComboBox.objectName()
                self.dim_dict["combobox>{}".format(item)] = child.currentText()

            print(self.dim_dict)

            data_ss = self.data[dim+meas]
            data_sss = data_ss.loc[data_ss[dim[0]] == self.dim_dict['combobox>Country']]

            self.sc.update_figure(data_sss)
            # data_cat = data_sss.loc[data_sss['Category'].isin(['Technology'])]
            # sum_cat = data_sss.groupby('Category')['Sales'].sum()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

