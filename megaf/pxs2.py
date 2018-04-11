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
import hashlib
import time
from PandasModel import PandasModel

data_file = "global.xlsx"
# data = pd.read_excel(data_file)
#


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

class ListItem(QtWidgets.QListWidgetItem):
    def __init__(self, title):
        super().__init__(title)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.connect(self, QtCore.PYQT_SIGNAL("customContextMenuRequest(QPoint)"), self.showMenu)
        self.customContextMenuRequested.connect(self.showMenu)

class CheckComboBox(QtWidgets.QComboBox):
    def addItem(self, item):
        super(CheckComboBox, self).addItem(item)
        item = self.model().item(self.count()-1,0)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)

    def addItems(self, items):
        for item in items:
            super(CheckComboBox, self).addItem(item)
            item = self.model().item(self.count()-1,0)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

    def itemChecked(self, index):
        item = self.model().item(index, 0)
        return item.checkState() == QtCore.Qt.Checked

    def getItemCheked(self):
        self.checked =[]
        for i in range(self.count()):
            print(i)
            item = self.model().item(i)
            if item.checkState() == QtCore.Qt.Checked:
                self.checked.append(item.text())

        return self.checked

class ListS(QtWidgets.QListWidget):
    def __init__(self, title, parent, widget, who, a, b, c, d):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.who = who
        self.widget = widget
        # self.setGeometry(QtCore.QRect(170, 20, 401, 31))
        self.setGeometry(QtCore.QRect(a, b, c, d))
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setAlternatingRowColors(True)
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setViewMode(QtWidgets.QListView.ListMode)
        self.itemDoubleClicked.connect(self.menuItemClicked)
        # self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.connect(self, QtCore.PYQT_SIGNAL("customContextMenuRequest(QPoint)"), self.showMenu)
        # self.customContextMenuRequested.connect(self.showMenu)
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

        self.dimension_changed = []


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

    # def showMenu(self, pos):
    #     menu = QtWidgets.QMenu()
    #     # clear_action = menu.addAction("Clear Selection")
    #     filter_action = menu.addAction("Filter...")
    #
    #
    #     action = menu.exec_(self.mapToGlobal(pos))
    #     # action.connect(self.menuItemClicked)
    #     # if action == clear_action:
    #     #     self.pp()
    #     #     self.combo.setCurrentIndex(0)
    #     if action == filter_action:
    #         print("Filter")

    def menuItemClicked(self):
        print("Asd")

    def getItem(self):
        items = []
        for item in range(self.count()):
            items.append(self.item(item).text())
        return items

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
            item = QtWidgets.QListWidgetItem(itemname)
            # item.

            # if self.who == 'dimension':
            #     self.widget.fil

            self.addItem(itemname)

            self.addCom()
            self.addCombobox()

                # self.parent().
            # self.widget.parentCall()
            # print(type(self.parent().parent()))

    def addCom(self):
        combo_option = self.widget.getComboOptions()
        print(combo_option)

    def addCombobox(self, option=None):
        if self.who == 'measurement':
                pass
        else:
            if self.widget.verticalLayout.count() >= 1:
                print("More than 1")
                self.widget.clearLayout()
                if option is not None:
                    # On changed
                    print("On changed")
                    ordered_dict = self.orderData(option)
                else:
                    ordered_dict = self.orderData()
                print(ordered_dict, "from More than 1")
                for item in self.getItem():
                    try:
                        combobox = QtWidgets.QComboBox()
                        combobox.setObjectName("combobox>{}".format(item))
                        print("combobox>{}".format(item))
                        combobox.addItem(item)
                        combobox.addItems(ordered_dict[item])
                        combobox.currentTextChanged.connect(self.on_combobox_changed)
                        self.widget.verticalLayout.addWidget(combobox)
                    except:
                        combobox = QtWidgets.QComboBox()
                        combobox.setObjectName("combobox>{}".format(item))
                        print("combobox>{}".format(item))
                        combobox.addItem(item)
                        combobox.addItems(self.widget.data[item])
                        combobox.currentTextChanged.connect(self.on_combobox_changed)
                        self.widget.verticalLayout.addWidget(combobox)
            else:
                # First time
                print("First time")
                for item in self.getItem():
                    combobox = CheckComboBox()
                    combobox.setObjectName("combobox>{}".format(item))
                    print("combobox>{}".format(item))
                    combobox.addItem(item)
                    combobox.addItems(self.widget.data[item].unique())
                    combobox.setObjectName("combobox>{}".format(item))
                    combobox.currentTextChanged.connect(self.on_combobox_changed)
                    # cb = QtWidgets.QCheckBox("Test")
                    # self.widget.verticalLayout.addWidget(cb)

                    # combobox.currentTextChanged.connect(self.on_combobox_changed)
                    self.widget.verticalLayout.addWidget(combobox)
                    print("add complete")

    def showMenu(self, pos):
        menu = QtWidgets.QMenu()
        clear_action = menu.addAction("Clear Filter")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == clear_action:
            self.widget.clearLayout()
            self.addCombobox()

    def on_combobox_changed(self, value):
        # def whoCalls():
        #     print(value)
        combo_option = self.widget.refresh()
        print(combo_option)
        print(combo_option.keys())
        self.widget.clearLayout()
        for item in combo_option.keys():

            combobox = CheckComboBox()
            combobox.setObjectName("combobox>{}".format(item))
            print("combobox>{}".format(item))
            combobox.addItem(item)
            combobox.addItems(combo_option[item])
            combobox.currentTextChanged.connect(self.on_combobox_changed)
            # combobox.setContextMenuPolicy(QtWidgets.CustomContextMenu)
            # combobox.setContextMenuPolicy(QtWidgets.Qt.CustomContextMenu)
            # combobox.customContextMenuRequested.connect(self.showMenu)
            self.widget.verticalLayout.addWidget(combobox)
        # child = self.widget.tab.findChild(QtWidgets.QComboBox, "combobox>{}".format(myDim[0])).currentText()
        # print(child)

        # print("Combobox changed", self.who, value)
        # self.widget.clearLayout()
        # self.dimension_changed.append(value)
        # print(self.dimension_changed)
        #
        # self.addCombobox(value)
        #

    # def plot(self):
    #     for item in self.
    #     self.widget.tab.findChild(QtWidgets.Q)

    def checkDefault(self, item):
        check = self.widget.tab.findChild(QtWidgets.QComboBox, "combobox>{}".format(item))
        if check == item:
            return True
        else:
            return False

    def orderData(self, option=None):
        print("Ordering Data")
        currentData = self.getItem()
        ordered = self.widget.data
        ordered_dict = {}
        i = 0
        for item in currentData:
            print(item, "iter from orderData")
            try:
                if option is not None:
                    child = option
                else:
                    child = self.widget.tab.findChild(QtWidgets.QComboBox, "combobox>{}".format(item)).currentText()
                print(child, item, "child from orderData")
                if child == item:
                    print("Child == Item")
                    ordered_dict[item] = ordered[item].unique()
                else:
                    print("Child !!!!!==== Item")
                    if i >= 1:
                        pass
                    else:
                        # if option is not None:
                        #     ordered = ordered[item].unique()
                        # else:
                        ordered = ordered.loc[self.widget.data[item] == child]
                    # print(ordered, "--- ordered ")
                    ordered_dict[item] = ordered[item].unique()
                    i += 1
            except:
                print("Not have!")
                ordered_dict[item] = ordered[item].unique()
            # if self.checkDefault(item):
            #     ordered_dict[item] = ordered[item].unique()
            # else:


        print("Going to return ordered_dict")
        # print("ordered_dict: ", ordered_dict)
        return ordered_dict
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
        MainWindow.resize(1269, 682)
        # MainWindow.showMaximized()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        # self.tabWidget.setGeometry(QtCore.QRect(0, 0, 771, 501))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(1060, 580, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(970, 580, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        # self.pushButton_2.clicked.connect(self.clickOnMe)

        self.listWidget = ListS("listWidget", self.tab, self, "dimension", 460, 10, 411, 41)
        self.listWidget_2 = QtWidgets.QListWidget(self.tab)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 31, 160, 262))
        self.listWidget_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_2.setObjectName("listWidget_2")
        # for item in datak:
        #     items = QtWidgets.QListWidgetItem(item)
        #     self.listWidget_2.addItem(items)
        self.listWidget_3 = QtWidgets.QListWidget(self.tab)
        self.listWidget_3.setGeometry(QtCore.QRect(0, 330, 160, 281))
        self.listWidget_3.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_3.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_3.setObjectName("listWidget_3")
        # for item in datak:
        #     items = QtWidgets.QListWidgetItem(item)
        #     self.listWidget_3.addItem(items)

        self.listWidget_4 = ListS("listWidget", self.tab, self, "measurement", 460, 50, 411, 41)

        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(0, 0, 161, 31))
        self.label.setStyleSheet("background-color:rgb(175, 254, 255);\n"
"alternate-background-color: rgb(169, 247, 255);")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(0, 299, 161, 30))
        self.label_3.setStyleSheet("background-color:rgb(175, 254, 255);\n"
"alternate-background-color: rgb(169, 247, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setGeometry(QtCore.QRect(250, 120, 771, 381))
        self.widget.setObjectName("widget")

        l = QtWidgets.QVBoxLayout(self.widget)
        self.sc = MyDynamicMplCanvas(self.tab, width=10, height=2, dpi=100)
        l.addWidget(self.sc)

        self.listWidget_5 = QtWidgets.QHBoxLayout(self.tab)
        self.listWidget_5.setGeometry(QtCore.QRect(590, 20, 171, 111))
        self.listWidget_5.setObjectName("listWidget_5")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(1070, 20, 171, 16))
        self.label_2.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1070, 40, 171, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(880, 580, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        # self.pushButton_3.clicked.connect(self.getItem)
        # self.frame = QtWidgets.QFrame(self.verticalLayoutWidget)
        # self.frame.setStyleSheet("background-color: rgb(198, 255, 203);")
        # self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame.setObjectName("frame")
        # self.verticalLayout.addWidget(self.frame)
        ####################################################################
        self.pushButton_4 = QtWidgets.QPushButton(self.tab)
        self.pushButton_4.setGeometry(QtCore.QRect(1150, 580, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(360, 10, 91, 41))
        self.label_4.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.label_4.setObjectName("label_4")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(360, 50, 91, 41))
        self.label_9.setStyleSheet("background-color: rgb(186, 133, 200);")
        self.label_9.setObjectName("label_9")
        self.comboBoxForGraph = QtWidgets.QComboBox(self.tab)
        self.comboBoxForGraph.setGeometry(QtCore.QRect(250, 500, 141, 21))
        self.comboBoxForGraph.setObjectName("comboBoxForGraph")
        self.comboBoxForGraph.addItem("")
        self.comboBoxForGraph.addItem("")
        self.comboBoxForGraph.addItem("")
        self.comboBoxForGraph.addItem("")

        ####################################################################
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
        self.tableView = QtWidgets.QTableView(self.tab_2)
        # self.tableView = QtWidgets.QTableWidget(self.tab_2)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 1251, 621))
        # self.tableView.
        # self.tablewidget.setObjectName('tablewidget')
        # self.tableView.setObjectName("tableView")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1269, 21))
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

    def clearLayout(self, option=None):
        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().deleteLater()
        # def orderData(self, data):


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
        self.dr = str(QtWidgets.QFileDialog.getOpenFileName()[0])
        # dim = []
        # mea = []
        # progessbar1 = Ui_Form(self)
        print(self.dr)
        # _translate = QtCore.QCoreApplication.translate
        _translate = QtCore.QCoreApplication.translate
        # file = self.app.openBox("Select file")
        self.md5()
        if self.dr != '':
            if not self.checkmd5():
                print('1st')
                self.data_file = self.dr
                self.data = pd.read_excel(data_file)
                self.dimdata = self.data.select_dtypes(include=['object'])
                self.mesudata = self.data._get_numeric_data()
                self.add_listwidget()
                self.setTab2()
                self.write_datadim()
                self.write_datamea()
                self.write_json()
            else:
                print('2th')
                self.dataJsonfile = '{}_Json.txt'.format(self.dr)
                self.datadimfile = '{}_datadim'.format(self.dr)
                self.datameafile = '{}_datamea'.format(self.dr)
                self.readtable = open(self.dataJsonfile, 'r+')
                self.readdatadim = open(self.datadimfile, 'r+')
                self.readdatamea = open(self.datameafile, 'r+')

                rdimdata = self.readdatadim.readlines()
                rmeadata = self.readdatamea.readlines()
                self.dimlist = [x.strip() for x in rdimdata]
                self.mealist = [x.strip() for x in rmeadata]
                print(self.dimlist)
                print(self.mealist)
                self.add_listwidget2()
                self.readpd = pd.read_json(self.readtable, orient='records')
                print(type(self.readpd))
                # print(self.readpd.head())
                self.data = self.readpd
                self.setTab2()
                # self.add_listwidget2()
        else:
            pass
    def setTab2(self):
        model = PandasModel(self.data)
        print(model)
        self.tableView.setModel(model)

    def add_listwidget(self):
        for i in self.dimdata.keys():
            print(i)
            item = QtWidgets.QListWidgetItem(i)
            self.listWidget_2.addItem(item)
            print()
            # print(QtCore.QCoreApplication.processEvents(pd.read_excel(data_file)))
        for j in self.mesudata.keys():
            item = QtWidgets.QListWidgetItem(j)
            self.listWidget_3.addItem(item)
            print("another1")

    def add_listwidget2(self):
        for i in self.dimlist:
            print(i)
            item = QtWidgets.QListWidgetItem(i)
            self.listWidget_2.addItem(item)
            print()
            # print(QtCore.QCoreApplication.processEvents(pd.read_excel(data_file)))
        for j in self.mealist:
            item = QtWidgets.QListWidgetItem(j)
            self.listWidget_3.addItem(item)
            print("another1")

    def write_datadim(self):
        self.datadimfile = '{}_datadim'.format(self.dr)
        print(self.datadimfile)
        dimfile = open(self.datadimfile, 'w+')
        for i in self.dimdata:
            dimfile.write(i+"\n")
        dimfile.close()

    def write_datamea(self):
        self.datameafile = '{}_datamea'.format(self.dr)
        meafile = open(self.datameafile, 'w+')
        for j in self.mesudata:
            meafile.write(j+"\n")
        meafile.close()

    def checkmd5 (self):
        self.rdb = open(self.file_database, 'r')
        found = False
        for line in self.rdb:
            try:
                if self.hashmd5 in line:
                    return True
            except AttributeError:
                pass
        return False

    def write_json(self):
        self.datajson = self.data.reset_index().to_json(orient='records')
        # print(self.datajson)
        self.dataJsonfile = '{}_Json.txt'.format(self.dr)
        jsonfile = open(self.dataJsonfile, 'w+')
        jsonfile.write(self.datajson)
        jsonfile.close()

    def md5(self):
        # Write new md5
        print("Yes md5")
        self.file_database = "plogs.txt"
        self.database = open(self.file_database, 'a')
        self.hashmd5 = hashlib.md5(open(self.dr, 'rb').read()).hexdigest()
        self.database.write(self.hashmd5 + " " + time.strftime("%H:%M:%S") + " " + time.strftime("%d/%m/%Y") + "\n")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PANXEL"))
        self.pushButton.setText(_translate("MainWindow", "Clear Filter"))
        self.pushButton_2.setText(_translate("MainWindow", "OK"))
        self.pushButton_3.setText(_translate("MainWindow", "Refresh"))
        self.pushButton_4.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_4.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.pushButton_3.clicked.connect(self.refresh)
        self.pushButton.clicked.connect(self.clearFilter)
        self.pushButton_2.clicked.connect(self.plot)
        self.label_4.setText(_translate("MainWindow", "      Dimensions"))
        self.label_9.setText(_translate("MainWindow", "   Measurements"))
        self.comboBoxForGraph.setItemText(0, _translate("MainWindow", "Available Graph"))
        self.label.setText(_translate("MainWindow", "                  Dimension"))
        self.label_3.setText(_translate("MainWindow", "              Measurements"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.menuOption.setTitle(_translate("MainWindow", "Option"))
        self.actionOpen.setText(_translate("MainWindow", "Open      [Ctrl+O]"))
        self.actionOpen.triggered.connect(self.openFile)

    def plot(self):
        self.refresh()
        myDim = self.dimSelected
        myMeas = self.measSelected
        myFilterSelected = self.filterSelected
        myFilter = self.filter
        myData = self.data[myDim + myMeas]

        if myFilterSelected == [] or myFilter == {}:
            myData = myData.pivot_table(index=myDim, values=myMeas, aggfunc=np.sum)
        else:
            for i in range(len(myFilterSelected)):
                myData = myData.loc[myData[myFilterSelected[i]] == myFilter[myFilterSelected[i]]]
            myData = myData.pivot_table(index=myDim, values=myMeas, aggfunc=np.sum)

        self.sc.update_figure(myData)
        print("Plot")

    def refresh(self):
        for i in range(self.listWidget.count()):
            print(i)
            self.dimSelected.append(self.listWidget.item(i).text())
        self.dimSelected = list(set(self.dimSelected))

        for i in range(self.listWidget_4.count()):
            print(i)
            self.measSelected.append(self.listWidget_4.item(i).text())
        self.measSelected = list(set(self.measSelected))

        print(list(set(self.dimSelected)), "Selected Dimension")
        print(list(set(self.measSelected)), "Selected Measurement")

        for item in self.dimSelected:
            child = self.tab.findChild(QtWidgets.QComboBox, "combobox>{}".format(item)).currentText()
            if child != item:
                self.filterSelected.append(item)
                self.filter[item] = child
            print(child)
        self.filterSelected = list(set(self.filterSelected))

        print(self.filterSelected, "Filter Select")
        print(self.filter, "Filter")

        result = self.getComboOptions()
        return result

    def getComboOptions(self):
        myDim = self.dimSelected
        myMeas = self.measSelected
        myFilterSelected = self.filterSelected
        myFilter = self.filter
        myData = self.data[myDim + myMeas]

        for i in range(len(myFilterSelected)):
            myData = myData.loc[myData[myFilterSelected[i]] == myFilter[myFilterSelected[i]]]

        for i, item in enumerate(myDim):
            self.combo_option[item] = myData[myDim[i]].unique()

        result = self.combo_option
        # print(self.combo_option)
        return result

    def clearFilter(self):
        self.filterSelected = []
        self.filter = {}
        self.clearLayout()
        for item in self.dimSelected:
                    combobox = CheckComboBox()
                    combobox.setObjectName("combobox>{}".format(item))
                    print("combobox>{}".format(item))
                    combobox.addItem(item)
                    combobox.addItems(self.data[item].unique())
                    combobox.setObjectName("combobox>{}".format(item))
                    combobox.currentTextChanged.connect(self.on_combobox_changed)
                    self.verticalLayout.addWidget(combobox)
                    print("add complete")

    def on_combobox_changed(self, value):
        combo_option = self.plot()
        print(combo_option)
        print(combo_option.keys())
        self.clearLayout()
        for item in combo_option.keys():
            combobox = CheckComboBox()
            combobox.setObjectName("combobox>{}".format(item))
            print("combobox>{}".format(item))
            combobox.addItem(item)
            combobox.addItems(combo_option[item])
            combobox.currentTextChanged.connect(self.on_combobox_changed)
            self.verticalLayout.addWidget(combobox)

    def clickOnMe(self):
        data_file = "global.xlsx"

        if not self.time_count:
            # First Time

            datak = self.data.keys()
            print(datak)

            dim = self.listWidget.getItem()
            meas = self.listWidget_4.getItem()

            # Clear item in VerticalLayout
            for item in range(self.verticalLayout.count()):
                layout_item = self.verticalLayout.itemAt(item)
                self.verticalLayout.removeItem(layout_item)

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

            pdf = data_ss.pivot_table(index=dim, values=meas, aggfunc=np.sum)

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

            print(self.dim_dict)
            # print(self.dim_dict["combobox>{}".format(dim[0])])
            # data_q = self.data.loc[self.data[dim[0]] == self.dim_dict["combobox>{}".format(dim[0])]]
            # print(data_q)
            for item in dim:

                try:
                    child = self.tab.findChild(QtWidgets.QComboBox, "combobox>{}".format(item))
                    if child is not None:

                        pass
                    else:
                        combobox = QtWidgets.QComboBox()
                        combobox.setObjectName("combobox>{}".format(item))
                        print("combobox>{}".format(item))


                        # combobox.addItems(data_q[item].unique())
                #
                        # self.verticalLayout.addWidget(combobox)
                except:
                    pass

            print(dim, "dim")
            print(meas, "meas")

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
            pdf = data_ss.pivot_table(index=dim, values=meas, aggfunc=np.sum)

            self.sc.update_figure(pdf)
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

