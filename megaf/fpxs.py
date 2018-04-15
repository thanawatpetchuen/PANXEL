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



class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # fig.tight_layout()

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
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

    def update_figure(self, df):
        # Get DataFrame and plot
        self.axes.cla()
        df.plot(kind="bar", ax=self.axes)
        hh = self.axes.get_ylim()[1]
        for i in self.axes.patches:
            print(i.get_y())
            self.axes.text(i.get_width()/20+i.get_x(), i.get_height()+hh*0.01, "{:.2f}".format(i.get_height()))
        self.draw()

    def update_bu(self, df):
            # Get DataFrame and plot
        self.axes.cla()
        df.plot(kind="bar", ax=self.axes)
        self.fig.tight_layout()
        hh = self.axes.get_ylim()[1]
        for i in self.axes.patches:
            print(i.get_y())
            self.axes.text(i.get_width()/20+i.get_x(), i.get_height()+hh*0.01, "{:.2f}".format(i.get_height()))
        self.draw()

class CheckComboBox(QtWidgets.QComboBox):
    # Check-able Combo Box Re-implement
    def addItem(self, item):
        # Add single check-able item
        super(CheckComboBox, self).addItem(item)
        item = self.model().item(self.count()-1,0)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)

    def addItems(self, items):
        # Add multiple check-able item
        for item in items:
            super(CheckComboBox, self).addItem(item)
            item = self.model().item(self.count()-1, 0)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            # item.pressed.connect(self.hand/lePress)

    def itemChecked(self, index):
        # Check if item has checked at index
        item = self.model().item(index, 0)
        return item.checkState() == QtCore.Qt.Checked

    def getItemChecked(self):
        # Get all items that checked
        self.checked =[]
        for i in range(self.count()):
            # print(i)
            item = self.model().item(i)
            if item.checkState() == QtCore.Qt.Checked:
                self.checked.append(item.text())

        return self.checked

    def handlePress(self, index):
        print(index)

class ListS(QtWidgets.QListWidget):
    # QListWidget Re-implement for overwriting Drop Event
    def __init__(self, title, parent, widget, who, a, b, c, d):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.who = who
        self.widget = widget
        self.setGeometry(QtCore.QRect(a, b, c, d))
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setAlternatingRowColors(True)
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setViewMode(QtWidgets.QListView.ListMode)
        self.itemDoubleClicked.connect(self.menuItemClicked)

        # Color for item setting
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

        # Private Variable
        self.dimension = []
        self.measurement = []
        self.dimension_changed = []

    def _addItem(self, name):
        self.addItem(name)
        print("ASd")

    def menuItemClicked(self):
        print("Asd")

    def getItem(self):
        # Get all items in ListS
        items = []
        for item in range(self.count()):
            items.append(self.item(item).text())
        return items

    def dropEvent(self, QDropEvent):
        # Overwriting old dropEvent for catch data before trigger functions

        mdd = QDropEvent.mimeData()

        # application/x-qabstractitemmodeldatalist == QWidgets.QListWidgetItem
        if QDropEvent.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            # Accpet drop if item is QListWidgetItem
            QDropEvent.accept()

            name = QDropEvent.mimeData().data('application/x-qabstractitemmodeldatalist')
            namees = name.data().decode('utf-8')
            itemname = "".join(i for i in namees if i.isalpha() or i == '-' or i == ' ')
            print(itemname)

            self.dimension.append(itemname)
            self.addItem(itemname)

            item = self.getItem()
            self.widget.addCombobox(items=item, who=self.who)

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
        # self.pushButton_2.clicked.connect(self.clickOnMe)

        self.listWidget = ListS("listWidget", self.tab, self, "dimension", 170, 20, 401, 31)

        self.listWidget_2 = QtWidgets.QListWidget(self.tab)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 20, 161, 171))
        self.listWidget_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_3 = QtWidgets.QListWidget(self.tab)
        self.listWidget_3.setGeometry(QtCore.QRect(0, 210, 161, 201))
        self.listWidget_3.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_3.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_3.setObjectName("listWidget_3")

        self.listWidget_4 = ListS("listWidget", self.tab, self, "measurement", 170, 60, 401, 31)

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

        # Box layout for Plot frame
        l = QtWidgets.QVBoxLayout(self.widget)
        self.sc = MyDynamicMplCanvas(self.tab, width=10, height=2, dpi=100)
        l.addWidget(self.sc)

        # Box layout for Combobox
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
        # QtWidgets.QShortcut()
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+O"), self.tab)
        self.shortcut.activated.connect(self.openFile)

        self.time_count = False
        self.dimSelected = []
        self.measSelected = []
        self.filterSelected = []
        self.filter = {}
        self.combo_option = {}

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PANXEL"))
        self.pushButton.setText(_translate("MainWindow", "Clear"))
        self.pushButton_2.setText(_translate("MainWindow", "OK"))
        self.pushButton_3.setText(_translate("MainWindow", "Refresh"))
        self.pushButton_3.clicked.connect(self.opClearLayout)
        self.pushButton.clicked.connect(self.clearandclean)
        self.pushButton_2.clicked.connect(self.plot)
        self.label.setText(_translate("MainWindow", "                  Dimension"))
        self.label_3.setText(_translate("MainWindow", "              Measurements"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.menuOption.setTitle(_translate("MainWindow", "Option"))
        self.actionOpen.setText(_translate("MainWindow", "Open      [Ctrl+O]"))
        self.actionOpen.triggered.connect(self.openFile)

    def addCombobox(self, who, items, option=None):
        # Add Combobox
        if who == 'measurement':
                pass
        else:
            if self.verticalLayout.count() >= 1:
                print("More than 1")
                self.clearLayout()
                if option is not None:
                    # On changed
                    print("On changed")
                    ordered_dict = self.orderData(option)
                else:
                    ordered_dict = self.orderData(items)
                print(ordered_dict, "from More than 1")
                for item in items:
                    try:
                        combobox = CheckComboBox()
                        combobox.setObjectName("combobox>{}".format(item))
                        print("combobox>{}".format(item))
                        combobox.addItem(item)
                        combobox.addItems(ordered_dict[item])
                        combobox.currentTextChanged.connect(self.on_combobox_changed)
                        self.verticalLayout.addWidget(combobox)
                    except:
                        combobox = CheckComboBox()
                        combobox.setObjectName("combobox>{}".format(item))
                        print("combobox>{}".format(item))
                        combobox.addItem(item)
                        combobox.addItems(self.widget.data[item])
                        combobox.currentTextChanged.connect(self.on_combobox_changed)
                        self.verticalLayout.addWidget(combobox)
            else:
                # First time
                print("First time")
                print(items, "itemsss")
                for item in items:
                    print(item)
                    combobox = CheckComboBox()
                    combobox.setObjectName("combobox>{}".format(item))
                    print("combobox>{}".format(item))
                    combobox.addItem(item)
                    combobox.addItems(self.data[item].unique())
                    combobox.setObjectName("combobox>{}".format(item))
                    combobox.currentTextChanged.connect(self.on_combobox_changed)
                    self.verticalLayout.addWidget(combobox)
                    print("add complete")

    def orderData(self, items, option=None):
        # Ordering Data from use as combobox OPTION
        print("Ordering Data")
        currentData = items
        ordered = self.data
        ordered_dict = {}
        i = 0
        for item in currentData:
            print(item, "iter from orderData")
            try:
                if option is not None:
                    child = option
                else:
                    child = self.tab.findChild(QtWidgets.QComboBox, "combobox>{}".format(item)).currentText()
                print(child, item, "child from orderData")
                if child == item:
                    print("Child == Item")
                    ordered_dict[item] = ordered[item].unique()
                else:
                    print("Child !!!!!==== Item")
                    if i >= 1:
                        pass
                    else:
                        ordered = ordered.loc[self.widget.data[item] == child]
                    ordered_dict[item] = ordered[item].unique()
                    i += 1
            except:
                print("Not have!")
                ordered_dict[item] = ordered[item].unique()

        print("Going to return ordered_dict")
        return ordered_dict

    def clearLayout(self, option=None):
        # To clear layout
        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().deleteLater()

    def opClearLayout(self):
        # Integrated clear layout function
        combo_option = self.refresh()
        self.clearLayout()

        for item in combo_option.keys():
            combobox = CheckComboBox()
            combobox.setObjectName("combobox>{}".format(item))
            print("combobox>{}".format(item))
            combobox.addItem(item)
            combobox.addItems(combo_option[item])
            combobox.currentTextChanged.connect(self.on_combobox_changed)
            self.verticalLayout.addWidget(combobox)

    def eventFilter(self, source, event):
        if(event.type() == QtCore.QEvent.ContextMenu and
        source is self.listWidget):
            menu = QtWidgets.QMenu()
            menu.addAction("Filter...")
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item.text())
            return True
        return self.eventFilter(source, event)

    def openFile(self):
        # Open dialog and select the directory of file
        self.dr = str(QtWidgets.QFileDialog.getOpenFileName()[0])
        print(self.dr)
        _translate = QtCore.QCoreApplication.translate
        if self.dr != '':

            data_file = self.dr
            self.data = pd.read_excel(data_file)
            self.dimdata = self.data.select_dtypes(include=['object'])
            self.mesudata = self.data._get_numeric_data()
            for i in self.dimdata.keys():
                item = QtWidgets.QListWidgetItem(i)
                self.listWidget_2.addItem(item)
            for j in self.mesudata.keys():
                item = QtWidgets.QListWidgetItem(j)
                self.listWidget_3.addItem(item)

    def getOpcode(self, type, temp):
        print("Type: ", type)
        print(temp)

        op = '(myData2["{}"] == "{}")'
        opcode_raw = []
        for item in temp:
            opcode_raw.append(op.format(type, item))

        opcode_cook = ' | '.join(opcode_raw)
        # print(opcode_cook)
        return opcode_cook

    def plot(self):
        # Plotting the graph
        self.refresh()
        myDim = self.dimSelected
        myMeas = self.measSelected
        myFilterSelected = self.filterSelected
        myFilter = self.filter
        myData = self.data[myDim + myMeas]

        print("From plot: (myFilterSelected)", myFilterSelected)
        print("From plot: (myFilter)", myFilter)



        # If filter has not been selected
        count = 0
        for item in myFilterSelected:
            if myFilter[item] == []:
                count += 1
        if count == len(myFilterSelected):
        # if myFilterSelected == [] or myFilter == {}:
            print("Nothing Selected!")
            myData = myData.pivot_table(index=myDim, values=myMeas, aggfunc=np.sum)
            print(myData)
        else:
            myData2 = myData
            opCode = None

            for i in range(len(myFilterSelected)):
                temp = []
                try:
                    for j in range(len(myFilter[myFilterSelected[i]])):
                        temp.append(myFilter[myFilterSelected[i]][j])
                    print("This is TEMP: ", temp)
                    opCode = self.getOpcode(myFilterSelected[i], temp)
                    print(opCode)
                    myData2 = myData2[eval(opCode)]
                except:
                    print("---Error occurred---")

            print(myData2)
            myData = myData2.pivot_table(index=myDim, values=myMeas, aggfunc=np.sum)

        print("Going to plot!")
        self.sc.update_figure(myData)
        print("Plot")

    def refresh(self):
        # Refresh the variable and use for combo option
        for i in range(self.listWidget.count()):
            self.dimSelected.append(self.listWidget.item(i).text())
        self.dimSelected = list(set(self.dimSelected))

        for i in range(self.listWidget_4.count()):
            self.measSelected.append(self.listWidget_4.item(i).text())
        self.measSelected = list(set(self.measSelected))

        print(list(set(self.dimSelected)), "Selected Dimension")
        print(list(set(self.measSelected)), "Selected Measurement")

        for item in self.dimSelected:
            child = self.tab.findChild(CheckComboBox, "combobox>{}".format(item)).getItemChecked()
            # print(child, "CHIlddd")
            if child != item:
                self.filterSelected.append(item)
                self.filter[item] = child

        # Cast filterSelected to list without duplicate
        self.filterSelected = list(set(self.filterSelected))

        print(self.filterSelected, "Filter Select")
        print(self.filter, "Filter")

        # After refresh, getComboOptions
        result = self.getComboOptions()
        return result

    def getComboOptions(self):
        # Caution
        # Require refresh before you call this function
        myDim = self.dimSelected
        myMeas = self.measSelected
        myFilterSelected = self.filterSelected
        myFilter = self.filter
        myData2 = self.data[myDim + myMeas]
        print(myFilter, "MY FILTER")
        print(myFilterSelected, "MY FILRERSELECTED")

        for i in range(len(myFilterSelected)):
            temp = []
            try:
                for j in range(len(myFilter[myFilterSelected[i]])):
                    temp.append(myFilter[myFilterSelected[i]][j])

                print("This is TEMPss: ", temp)
                opCode = self.getOpcode(myFilterSelected[i], temp)
                print(opCode)
                myData2 = myData2[eval(opCode)]
            except:
                print("Error at getComboOptions occurred")

        print("Pass Stage 1")
        for i, item in enumerate(myDim):
            self.combo_option[item] = myData2[myDim[i]].unique()
        print("Pass Stage 2")
        result = self.combo_option
        print("This is RESULT: ", result)
        # print(self.combo_option)
        return result

    def clearandclean(self):
        # Clear all temp and Add new combobox
        self.filterSelected = []
        self.filter = {}
        self.dimSelected = []
        self.measSelected = []

        self.clearLayout()
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        self.listWidget_4.clear()

        self.sc.axes.cla()
        self.sc.draw()

        self.dimdata = self.data.select_dtypes(include=['object'])
        self.mesudata = self.data._get_numeric_data()
        for i in self.dimdata.keys():
            item = QtWidgets.QListWidgetItem(i)
            self.listWidget_2.addItem(item)
        for j in self.mesudata.keys():
            item = QtWidgets.QListWidgetItem(j)
            self.listWidget_3.addItem(item)

    def on_combobox_changed(self, value):
        # If Combobox changed do

        # Refresh for get a fresh combo box option
        combo_option = self.refresh()

        # Clear layout to add a new combobox
        self.clearLayout()
        for item in combo_option.keys():
            combobox = CheckComboBox()
            combobox.setObjectName("combobox>{}".format(item))
            print("combobox>{}".format(item))
            combobox.addItem(item)
            combobox.addItems(combo_option[item])
            combobox.currentTextChanged.connect(self.on_combobox_changed)
            self.verticalLayout.addWidget(combobox)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

