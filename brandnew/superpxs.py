# Form implementation generated from reading ui file '.\asd.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import pyqtgraph.widgets.MatplotlibWidget as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
# import random
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from PandasModel import PandasModel
import hashlib
import time
from difflib import SequenceMatcher
import resources
import atexit
import random
import os

class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # fig.tight_layout()

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        scale = 1.1
        zp = ZoomPan()
        self.fig.tight_layout()
        figZoom = zp.zoom_factory(self.axes, base_scale=scale)
        figPan = zp.pan_factory(self.axes)
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
    def saveFigure(self):
        self.fig.savefig("11.png")

    def update_figure(self, df):
        # Get DataFrame and plot
        self.axes.cla()
        df.plot(kind="bar", ax=self.axes)
        axesHeight = self.axes.get_ylim()[1]
        for i in self.axes.patches:
            print(i.get_y())
            self.axes.text(i.get_width()/20+i.get_x(), i.get_height()+axesHeight*0.01, "{:.2f}".format(i.get_height()))
        self.draw()
        self.fig.tight_layout()

    def update_bu(self, df):
            # Get DataFrame and plot
        self.axes.cla()
        df.plot(kind="bar", ax=self.axes)
        self.fig.tight_layout()
        axesHeight = self.axes.get_ylim()[1]
        for i in self.axes.patches:
            print(i.get_y())
            self.axes.text(i.get_width()/20+i.get_x(), i.get_height()+axesHeight*0.01, "{:.2f}".format(i.get_height()))
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

            # Get original key and compare if namees exist or similar.
            name = QDropEvent.mimeData().data('application/x-qabstractitemmodeldatalist')
            namees = name.data().decode('ascii')



            # print(namees, "NAMEESS")
            itemname = "".join(i for i in namees if i.isalpha() or i == '-' or i == ' ' or i == ':' or i == '(' or i == ')')
            # print(itemname)

            if self.who == 'dimension':
                self.dim = self.widget.dimdata.keys()
                # print("I'm Dimension", self.dim)
                for item in self.dim:
                    print(SequenceMatcher(None, itemname, item).ratio())
                    if SequenceMatcher(None, itemname, item).ratio() >= 0.92:
                        # print(itemname, '==', item)
                        itemname = item
            else:
                self.meas = self.widget.mesudata.keys()
                for item in self.meas:
                    # print(SequenceMatcher(None, itemname, item).ratio())
                    if SequenceMatcher(None, itemname, item).ratio() >= 0.92:
                        # print(itemname, '==', item)
                        itemname = item

            self.dimension.append(itemname)
            self.addItem(itemname)

            item = self.getItem()
            try:
                self.widget.addCombobox(items=item, who=self.who)
            except:
                print("=======FROM Add Combobox=======")
                print(sys.exc_info()[0], sys.exc_info()[1])
                print("===============================")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1269, 690)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
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
        # self.sc = MyDynamicMplCanvas(self.tab, width=10, height=2, dpi=100)
        # self.toolbar = NavigationToolbar(self.sc, self.tab)
        # l.addWidget(self.toolbar)
        # l.addWidget(self.sc)


        ##########
        # Plot
        self.plotWidget = pg.PlotWidget(name="Plot1")
        l.addWidget(self.plotWidget)
        ##########

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
        self.pushButton_5 = QtWidgets.QPushButton(self.tab)
        self.pushButton_5.setGeometry(QtCore.QRect(1120, 175, 81, 71))
        self.pushButton_5.setMaximumSize(QtCore.QSize(261, 251))
        self.pushButton_5.setStyleSheet("background-image: url(:/1.png);\n"
                                        "\n"
                                        "background-color: rgb(255, 255, 255);")
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        # self.pushButton_6 = QtWidgets.QPushButton(self.tab)
        # self.pushButton_6.setGeometry(QtCore.QRect(1120, 280, 81, 71))
        # self.pushButton_6.setMaximumSize(QtCore.QSize(261, 251))
        # self.pushButton_6.setStyleSheet("background-image: url(:/2.png);\n"
        #                                 "\n"
        #                                 "background-color: rgb(255, 255, 255);")
        # self.pushButton_6.setText("")
        # self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(1120, 275, 81, 71))
        self.pushButton_7.setMaximumSize(QtCore.QSize(261, 251))
        self.pushButton_7.setStyleSheet("background-image: url(:/3.png);\n"
                                        "\n"
                                        "background-color: rgb(255, 255, 255);")
        self.pushButton_7.setText("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab)
        self.pushButton_8.setGeometry(QtCore.QRect(1120, 375, 81, 71))
        self.pushButton_8.setMaximumSize(QtCore.QSize(261, 251))
        self.pushButton_8.setStyleSheet("background-image: url(:/line-graphic-81x71.png);\n"
                                        "\n"
                                        "background-color: rgb(255, 255, 255);")
        self.pushButton_8.setText("")
        self.pushButton_8.setObjectName("pushButton_8")

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
        self.tableView.setObjectName("tableView")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        ############################################33
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1269, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menu.addAction(self.actionOpen)
        self.menubar.addAction(self.menu.menuAction())
        ############################################################3
        # QtWidgets.QShortcut()
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.actionSave)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+O"), self.tab)
        self.shortcut.activated.connect(self.openFile)
        #########################################################
        self.time_count = False
        self.dimSelected = []
        self.measSelected = []
        self.filterSelected = []
        self.filter = {}
        self.combo_option = {}
        self.graph_selected = ''
        self.legend = None

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PANXEL"))
        self.pushButton.setText(_translate("MainWindow", "Clear"))
        self.pushButton_2.setText(_translate("MainWindow", "OK"))
        self.pushButton_3.setText(_translate("MainWindow", "Refresh"))
        self.pushButton_4.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_4.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.pushButton_3.clicked.connect(self.opClearLayout)
        self.pushButton.clicked.connect(self.clearandclean)
        self.pushButton_2.clicked.connect(self.plot)
        self.label_4.setText(_translate("MainWindow", "      Dimensions"))
        self.label_9.setText(_translate("MainWindow", "   Measurements"))
        self.label.setText(_translate("MainWindow", "                  Dimension"))
        self.label_3.setText(_translate("MainWindow", "              Measurements"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        # self.menuOption.setTitle(_translate("MainWindow", "Option"))
        self.actionOpen.setText(_translate("MainWindow", "Open      [Ctrl+O]"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.save)
        self.pushButton_5.clicked.connect(lambda select: self.graph_type('Bar'))
        self.pushButton_7.clicked.connect(lambda select: self.graph_type('Line'))
        self.pushButton_8.clicked.connect(lambda select: self.graph_type('Scatter'))
        # self.actionSave_Fugure_as.triggered.connect(self.sc.saveFigure)

    def graph_type(self, type):
        # Type : Bar, Line, Scatter
        self.graph_selected = type
        self.statusbar.showMessage("Graph: {}".format(self.graph_selected))
        print(self.graph_selected)

    def save(self):
        self.datadimfile = '{}_datadim'.format(self.filePath)
        self.dimfile = open(self.datadimfile, 'w+')
        self.dimsaved = []
        print((self.listWidget_2.count()))
        for i in range(self.listWidget_2.count()):
            self.dimsaved.append(self.listWidget_2.item(i).text())
        for q in range(self.listWidget.count()):
            self.dimsaved.append(self.listWidget.item(q).text())
        for i in self.dimsaved:
            # print(i)
            self.dimfile.write(i+ '\n')
        self.dimfile.close()
        # self.write_mearec()

        # print(self.dimsaved)
        # print("Save!!!!!!!!")

        self.datameafile = '{}_datamea'.format(self.filePath)
        self.meafile = open(self.datameafile, 'w+')
        self.measaved = []
        for j in range(self.listWidget_3.count()):
            self.measaved.append(self.listWidget_3.item(j).text())
        for w in range(self.listWidget_4.count()):
            self.measaved.append(self.listWidget_4.item(w).text())
            # meafile.write(self.listWidget_3.item(j).text() + '\n')
        for j in self.measaved:
            self.meafile.write(j + '\n')
        self.meafile.close()

        print(self.measaved)


    def write_dimrec(self):
        for i in self.dimsaved:
            self.dimfile.write(i + '\n')

    def write_mearec(self):
        for j in self.measaved:
            self.meafile.write(j + '\n')


    def addCombobox(self, who, items, option=None):
        # Add Combobox
        if who == 'measurement':
                pass
        else:
            if self.verticalLayout.count() >= 1:
                # print("More than 1")
                self.clearLayout()
                if option is not None:
                    # On changed
                    # print("On changed")
                    ordered_dict = self.orderData(option)
                else:
                    ordered_dict = self.orderData(items)
                # print(ordered_dict, "from More than 1")
                for item in items:
                    try:
                        if item in self.timedata:
                            # print("In timedata")
                            dateStart = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
                            dateStart.setCalendarPopup(True)
                            dateStop = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
                            dateStop.setCalendarPopup(True)
                            dateStart.setObjectName("datepicker_start>{}".format(item))
                            dateStop.setObjectName("datepicker_stop>{}".format(item))
                            dateType = QtWidgets.QComboBox()
                            dateType.addItems(['Daily', 'Monthly', 'Yearly'])
                            dateType.setObjectName("datetype>{}".format(item))
                            self.verticalLayout.addWidget(dateStart)
                            self.verticalLayout.addWidget(dateStop)
                            self.verticalLayout.addWidget(dateType)
                        else:
                            combobox = CheckComboBox()
                            combobox.setObjectName("combobox>{}".format(item))
                            # print("combobox>{}".format(item), "from Try")
                            combobox.addItem(item)
                            combobox.addItems(ordered_dict[item])
                            combobox.currentTextChanged.connect(self.on_combobox_changed)
                            self.verticalLayout.addWidget(combobox)
                    except:
                        if item in self.timedata:
                            # print("In timedata")
                            # datePopup = QtWidgets.QCalendarWidget
                            # datePopup.set
                            dateStart = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
                            dateStart.setCalendarPopup(True)
                            dateStop = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
                            dateStop.setCalendarPopup(True)
                            dateStart.setObjectName("datepicker_start>{}".format(item))
                            dateStop.setObjectName("datepicker_stop>{}".format(item))
                            dateType = QtWidgets.QComboBox()
                            dateType.addItems(['Daily', 'Monthly', 'Yearly'])
                            dateType.setObjectName("datetype>{}".format(item))
                            self.verticalLayout.addWidget(dateStart)
                            self.verticalLayout.addWidget(dateStop)
                            self.verticalLayout.addWidget(dateType)
                        else:
                            combobox = CheckComboBox()
                            combobox.setObjectName("combobox>{}".format(item))
                            # print("combobox>{}".format(item), "from Except")
                            combobox.addItem(item)
                            combobox.addItems(self.widget.data[item])
                            combobox.currentTextChanged.connect(self.on_combobox_changed)
                            self.verticalLayout.addWidget(combobox)
                            # print("Pass from Except")
            else:
                # First time
                # print("First time")
                # print(items, "itemsss")



                for item in items:
                    # print(item)
                    if item in self.timedata:
                        # print("In timedata")
                        dateStart = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
                        dateStart.setCalendarPopup(True)
                        dateStop = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
                        dateStop.setCalendarPopup(True)
                        dateStart.setObjectName("datepicker_start>{}".format(item))
                        dateStop.setObjectName("datepicker_stop>{}".format(item))
                        dateType = QtWidgets.QComboBox()
                        dateType.addItems(['Daily', 'Monthly', 'Yearly'])
                        dateType.setObjectName("datetype>{}".format(item))
                        self.verticalLayout.addWidget(dateStart)
                        self.verticalLayout.addWidget(dateStop)
                        self.verticalLayout.addWidget(dateType)
                    else:
                        try:
                            # print(type(item), "!From else!")
                            # print(self.data[item].unique())
                            dataunique = self.data[item].unique()
                            combobox = CheckComboBox()
                            combobox.setObjectName("combobox>{}".format(item))
                            # print("combobox>{}".format(item), "from First time")
                            combobox.addItem(item)
                            combobox.addItems([item for item in dataunique if isinstance(item, str)])
                            combobox.setObjectName("combobox>{}".format(item))
                            combobox.currentTextChanged.connect(self.on_combobox_changed)
                            self.verticalLayout.addWidget(combobox)
                            # print("add complete")
                        except:
                            print("=======FROM Inner Combobox=======")
                            print(sys.exc_info()[0], sys.exc_info()[1])
                            print("=================================")

    def orderData(self, items, option=None):
        # Ordering Data from use as combobox OPTION
        # print("Ordering Data")
        currentData = items
        ordered = self.data
        ordered_dict = {}
        i = 0
        for item in currentData:
            # print(item, "iter from orderData")
            try:
                if option is not None:
                    child = option
                else:
                    child = self.tab.findChild(QtWidgets.QComboBox, "combobox>{}".format(item)).currentText()
                # print(child, item, "child from orderData")
                if child == item:
                    # print("Child == Item")
                    dataunique = ordered[item].unique()
                    ordered_dict[item] = [item for item in dataunique if isinstance(item, str)]
                else:
                    # print("Child !!!!!==== Item")
                    if i >= 1:
                        pass
                    else:
                        ordered = ordered.loc[self.widget.data[item] == child]
                    dataunique = ordered[item].unique()
                    ordered_dict[item] = [item for item in dataunique if isinstance(item, str)]
                    i += 1
            except:
                # print("Not have!")
                dataunique = ordered[item].unique()
                ordered_dict[item] = ordered[item].unique()
                ordered_dict[item] = [item for item in dataunique if isinstance(item, str)]

        # print("Going to return ordered_dict")
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
            # print(item, "OPCLEAR")
            if item in self.timedata:
                print("=======Opclear======")
                print(item)
                # print("In timedata")
                dateStart = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
                dateStart.setCalendarPopup(True)
                dateStop = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
                dateStop.setCalendarPopup(True)
                dateStart.setObjectName("datepicker_start>{}".format(item))
                dateStop.setObjectName("datepicker_stop>{}".format(item))
                dateType = QtWidgets.QComboBox()
                dateType.addItems(['Daily', 'Monthly', 'Yearly'])
                dateType.setObjectName('datetype>{}'.format(item))
                self.verticalLayout.addWidget(dateStart)
                self.verticalLayout.addWidget(dateStop)
                self.verticalLayout.addWidget(dateType)
            else:
                combobox = CheckComboBox()
                combobox.setObjectName("combobox>{}".format(item))
                # print("combobox>{}".format(item))
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
                # print(item.text())
            return True
        return self.eventFilter(source, event)

    def thaitoarab(self, num):
        ll = ''
        for i in num:
            if i == '๐':
                ll += '0'
            elif i == '๑':
                ll += '1'
            elif i == '๒':
                ll += '2'
            elif i == '๓':
                ll += '3'
            elif i == '๔':
                ll += '4'
            elif i == '๕':
                ll += '5'
            elif i == '๖':
                ll += '6'
            elif i == '๗':
                ll += '7'
            elif i == '๘':
                ll += '8'
            elif i == '๙':
                ll += '9'
            else:
                ll += '/'

        # print(ll)
        return ll



    def write_datadim(self):
        self.datadimfile = '{}_datadim'.format(self.filePath)
        # print(self.datadimfile)
        dimfile = open(self.datadimfile, 'w+')
        for i in self.dimdata:
            dimfile.write(i+"\n")
        dimfile.close()

    def write_datamea(self):
        self.datameafile = '{}_datamea'.format(self.filePath)
        meafile = open(self.datameafile, 'w+')
        for j in self.mesudata:
            meafile.write(j+"\n")
        meafile.close()

    def write_datetime(self):
        self.datatime = '{}_datetime'.format(self.filePath)
        timefile = open(self.datatime, 'w+')
        for i in self.timedata:
            timefile.write(i + '\n')
        timefile.close()

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
        self.datajson = self.data.reset_index().to_json(orient = 'records', date_format = 'iso')
        # print('12345678910')
        # print(self.datajson)
        self.dataJsonfile = '{}_Json.txt'.format(self.filePath)
        jsonfile = open(self.dataJsonfile, 'w+')
        jsonfile.write(self.datajson)

    def md5(self):
        # Write new md5
        if self.filePath != '':
            # print("Yes md5")
            self.file_database = "plogs.txt"
            self.database = open(self.file_database, 'a')
            self.hashmd5 = hashlib.md5(open(self.filePath, 'rb').read()).hexdigest()
            self.database.write(self.hashmd5 + " " + time.strftime("%H:%M:%S") + " " + time.strftime("%d/%m/%Y") + "\n")

    def checkEmpty(self):
        self.dataJsonfile = '{}_Json.txt'.format(self.filePath)
        self.readJson = open(self.dataJsonfile, 'r+')
        return os.stat(self.dataJsonfile).st_size == 0

    def checkExist(self):
        self.dataJsonfile = '{}_Json.txt'.format(self.filePath)
        # print(os.path.isfile(self.dataJsonfile))
        # print("Newdeaasdasdasdwdasdwdasdasdawdawdasdwdsdwdasdwdasdwdasd")
        return os.path.exists(self.dataJsonfile)

    def clearListWidget(self):
        if self.listWidget_2.count() != 0:
            # print(self.listWidget_2.count())
            self.filterSelected = []
            self.filter = {}
            self.dimSelected = []
            self.measSelected = []
            self.clearLayout()
            self.listWidget.clear()
            self.listWidget_2.clear()
            self.listWidget_3.clear()
            self.listWidget_4.clear()
            self.plotWidget.clear()
            self.plotWidget.clearPlots()
            try:
                self.legend.scene().removeItem(self.legend)
            except:
                pass
            self.dimdata = self.data.select_dtypes(include=['object', np.datetime64])
            self.mesudata = self.data._get_numeric_data()
            # self.tabWidget.clear()

    def openFile(self):
        self.filePath = str(QtWidgets.QFileDialog.getOpenFileName()[0])
        # dim = []
        # mea = []
        # progessbar1 = Ui_Form(self)
        # print(self.dr)
        # _translate = QtCore.QCoreApplication.translate
        # _translate = QtCore.QCoreApplication.translate
        # file = self.app.openBox("Select file")
        self.md5()
        if self.filePath != '':
            if not self.checkmd5():
                try:
                    self.clearListWidget()
                    # print('1st')
                    self.data_file = self.filePath
                    self.data = pd.read_excel(self.data_file)
                    try:
                        self.write_json()
                        # print('Newdeathnote')
                    except:
                        errorDetect = sys.exc_info()[0]
                        errorDetect2 = sys.exc_info()[1]
                        print(errorDetect, errorDetect2, sys.exc_info())
                    self.database.close()
                    self.dimdata = self.data.select_dtypes(include=['object', np.datetime64])
                    self.timedata = self.data.select_dtypes(include=[np.datetime64]).keys()
                    # print('timedata', self.timedata)
                    self.write_datetime()
                    self.mesudata = self.data._get_numeric_data()
                    # print("Date Column is ", self.timedata)
                    if list(self.timedata) != []:
                        # print("YESSSSSSSSSSSSSSSSSS")
                        # If data have time column
                        # Convert those column to pandas datetime
                        for item in self.timedata:
                            # print(item, "in in")
                            self.data[item] = pd.to_datetime(self.data[item])

                            self.data['Month>{}'.format(item)] = self.data[item].dt.month
                            self.data['Year>{}'.format(item)] = self.data[item].dt.year
                            # print('Month>{}'.format(item))
                            # print('Year>{}'.format(item))

                    # print("SELF ADD LIST WIDGET")
                    self.add_listwidget()
                    self.setTab2()
                    self.write_datadim()
                    # print('Newdea')
                    self.write_datamea()
                    # print('newdeathnote132222')

                except:
                    errorDetect = sys.exc_info()[0]
                    errorDetect2 = sys.exc_info()[1]
                    print(errorDetect, errorDetect2, sys.exc_info())

            elif self.checkExist() and self.checkmd5():
                # print('2th')
                self.dataJsonfile = '{}_Json.txt'.format(self.filePath)
                self.datadimfile = '{}_datadim'.format(self.filePath)
                self.datameafile = '{}_datamea'.format(self.filePath)
                self.datatime = '{}_datetime'.format(self.filePath)
                self.readjsondata = open(self.dataJsonfile, 'r+')
                self.readdatadim = open(self.datadimfile, 'r+')
                self.readdatamea = open(self.datameafile, 'r+')
                self.readtime = open(self.datatime, 'r+')
                rdimdata = self.readdatadim.readlines()
                rmeadata = self.readdatamea.readlines()
                rtimedata = self.readtime.readlines()
                self.dimlist = [x.strip() for x in rdimdata]
                self.mealist = [x.strip() for x in rmeadata]
                self.timelist = [x.strip() for x in rtimedata]
                # print(self.dimlist)
                # print(self.mealist)
                self.add_listwidget2()
                self.readpd = pd.read_json(self.readjsondata, orient= 'records', convert_dates= self.timelist)
                # print(type(self.readpd))
                # print(self.readpd.head())
                self.data = self.readpd
                # self.mesudata = self.mealist
                # self.dimdata = self.dimlist
                self.mesudata = self.data._get_numeric_data()
                self.dimdata = self.data.select_dtypes(include=['object', np.datetime64])
                # self.data = pd.read_excel(self.dr)
                self.timedata = self.data.select_dtypes(include=[np.datetime64]).keys()
                # print("Date Column is ", self.timedata)
                if not list(self.timedata):
                    # If data have time column
                    # Convert those column to pandas datetime
                    for item in self.timedata:
                        # print(item)
                        self.data[item] = pd.to_datetime(self.data[item])
                self.setTab2()
                # self.add_listwidget2()
            else:
                self.clearListWidget()
                # print('1st')
                self.data_file = self.filePath
                # print("new")
                self.data = pd.read_excel(self.data_file)
                # print("new")
                try:
                    self.write_json()
                    # print('Newdeathnote')
                except:
                    errorDetect = sys.exc_info()[0]
                    errorDetect2 = sys.exc_info()[1]
                    print(errorDetect, errorDetect2, sys.exc_info())
                self.database.close()
                # print(self.data)
                self.dimdata = self.data.select_dtypes(include=['object', np.datetime64])
                self.timedata = self.data.select_dtypes(include=[np.datetime64]).keys()
                # print('timedata', self.timedata)
                self.write_datetime()
                self.mesudata = self.data._get_numeric_data()
                # print("Date Column is ", self.timedata)
                if not list(self.timedata):
                    # If data have time column
                    # Convert those column to pandas datetime
                    for item in self.timedata:
                        print(item)
                        self.data[item] = pd.to_datetime(self.data[item])

                self.add_listwidget()
                self.setTab2()
                self.write_datadim()
                # print('Newdea')
                self.write_datamea()
                # print('newdeathnote132222')

        else:
            pass

    def setTab2(self):
        modelPandas = PandasModel(self.data)
        print(modelPandas)
        self.cleanTable = self.tableView.setModel(modelPandas)

    def add_listwidget(self):
        for i in self.dimdata.keys():
            # print(i)
            item = QtWidgets.QListWidgetItem(i)
            self.listWidget_2.addItem(item)
            # print()
            # print(QtCore.QCoreApplication.processEvents(pd.read_excel(data_file)))
        for j in self.mesudata.keys():
            item = QtWidgets.QListWidgetItem(j)
            self.listWidget_3.addItem(item)
            # print("another1")

    def add_listwidget2(self):
        for i in self.dimlist:
            # print(i)
            item = QtWidgets.QListWidgetItem(i)
            self.listWidget_2.addItem(item)
            # print()
            # print(QtCore.QCoreApplication.processEvents(pd.read_excel(data_file)))
        for j in self.mealist:
            item = QtWidgets.QListWidgetItem(j)
            self.listWidget_3.addItem(item)
            # print("another1")

    def getOpcode(self, type, temp, istime=False):
        # get a DYNAMIC Op Code for using filter
        # print("Type: ", type)
        # print(u'{}'.format(temp[0]))
        # print("istime: ", istime)

        operations = '(myData2["{}"] == "{}")'

        operationsTimes = "(myData2['{type}'] >= '{start}') & (myData2['{type}'] <= '{stop}')"
        operationsTimes2 = "(myData2['{type}'] == '{start}')"
        operationsCode = []
        opeations_Time = ''
        if istime:
            # If data set is time-order
            temp_start = time.strptime(temp[0], '%d/%m/%Y')
            temp_stop = time.strptime(temp[1], '%d/%m/%Y')
            # print("Today: ", QtCore.QDate.currentDate())
            # print(time.strftime('%Y-%m-%d', tes))
            temp_start = time.strftime('%Y-%m-%d', temp_start)
            temp_stop = time.strftime('%Y-%m-%d', temp_stop)
            print(temp_start, temp_stop, "START_STOP")
            if temp_start == temp_stop:
                opeations_Time = operationsTimes2.format(type=type, start=temp_start)
            else:
                opeations_Time = operationsTimes.format(type=type, start=temp_start, stop=temp_stop)
        else:
            for item in temp:
                operationsCode.append(operations.format(type, item))

        # To join each opcode together
        opeartionsCode_cooked = ' | '.join(operationsCode)
        # opcode_cook_time = ''.join(opeations_Time)
        # result = opeartionsCode_cooked + opcode_cook_time
        # print(result)
        if istime:
            return opeations_Time
        else:
            return opeartionsCode_cooked

    def updateTable(self):
        # print('updeated')
        self.updateData = PandasModel(self.data3)
        self.tableView.setModel(self.updateData)

    def plot(self):
        # Plotting the graph
        try:
            if self.graph_selected == '':
                self.statusbar.showMessage("Please select Graph type!")
            else:
                self.refresh()
                myDimensions = self.dimSelected
                myMeasurements = self.measSelected
                myFilterSelected = self.filterSelected
                myFilter = self.filter
                # dataForPlot = self.data[myDimensions + myMeasurements]
                dataForPlot = self.data

                # print("From plot: (myFilterSelected)", myFilterSelected)
                # print("From plot: (myFilter)", myFilter)
                #
                # print("Refresh PASS!")
                # If filter has not been selected
                count = 0
                for item in myFilterSelected:
                    if myFilter[item] == []:
                        count += 1
                if count == len(myFilterSelected):
                    # print("Nothing Selected!")
                    dataForPlot = dataForPlot.pivot_table(index=myDimensions, values=myMeasurements, aggfunc=np.sum)
                    # print(dataForPlot)
                else:
                    # At least one selected
                    myData2 = dataForPlot
                    operationsCodes = None
                    istime = False
                    time_temp = ''

                    for i in range(len(myFilterSelected)):
                        tempFilter = []
                        try:
                            for j in range(len(myFilter[myFilterSelected[i]])):
                                # Temp are items which selected by its own filter
                                if myFilterSelected[i] in self.timedata:
                                    # print(myFilter[myFilterSelected[i]], "TIMETEMPP")
                                    tempFilter = myFilter[myFilterSelected[i]]
                                else:
                                    tempFilter.append(myFilter[myFilterSelected[i]][j])
                            # print("This is TEMP: ", tempFilter)
                            if myFilterSelected[i] in self.timedata:
                                # print("TIME selected")
                                operationsCodes = self.getOpcode(myFilterSelected[i], tempFilter, istime=True)
                                time_temp = operationsCodes
                                istime = True
                            else:
                                operationsCodes = self.getOpcode(myFilterSelected[i], tempFilter)
                                myData2 = myData2[eval(operationsCodes)]
                            # print(operationsCodes)

                        except:
                            print("---Error occurred---")
                            errorDetect = sys.exc_info()[0]
                            errorDetect2 = sys.exc_info()[1]
                            print(errorDetect, errorDetect2)
                            print(sys.exc_info())

                    # print("Pre DaTa2")
                    # print(myData2[(myData2['Order Date'] >= '2014-11-11') & (myData2['Order Date'] <= '2014-11-12')])
                    if istime:
                        # print("IS TIME")
                        myData2 = myData2[eval(time_temp)]
                        # print(myData2)

                        for item in self.filterSelected:
                            if item in self.timedata:
                                print(item, "ISTIMM")
                                ch = self.tab.findChild(QtWidgets.QComboBox, "datetype>{}".format(item)).currentText()
                                if ch == 'Monthly':
                                    print("=======Monthly=======")
                                    print("=======Before=======")
                                    print(myDimensions)
                                    print("====================")
                                    for item2 in myDimensions:
                                        print("Checking(Monthly):", item, item2)
                                        if item in item2:
                                            print("DUP", item, item2)
                                            myDimensions.pop(myDimensions.index(item2))
                                            print("=======AFTER POP=======")
                                            print(myDimensions)
                                            print("=======================")
                                            # print("DUPLICLATE", item, item2)
                                            # if item == item2:
                                            #     my_temp = myDimensions.pop(myDimensions.index(item))
                                            #     my_temp2 = 'Nothh'
                                            # else:
                                            #     my_temp = myDimensions.pop(myDimensions.index(item))
                                            #     my_temp2 = myDimensions.pop(myDimensions.index(item2))
                                            # print(my_temp, my_temp2)
                                    try:
                                        for item2 in myDimensions:
                                            if item in item2:
                                                print('DUP Again', item, item2)
                                                myDimensions.pop(myDimensions.index(item2))
                                        myDimensions.pop(myDimensions.index(item))
                                    except:
                                        myDimensions.append("Month>{}".format(item))

                                    print("=======MYDIM MONTHLY=======")
                                    print(myDimensions)
                                    print("===========================")
                                    dataForPlot = myData2.pivot_table(index=myDimensions, values=myMeasurements, aggfunc=np.sum)
                                elif ch == 'Yearly':
                                    print("=======Yearly=======")
                                    print("=======Before=======")
                                    print(myDimensions)
                                    print("====================")
                                    for item2 in myDimensions:
                                        print("Checking(Yearly):", item, item2)
                                        if item in item2:
                                            print("DUP", item, item2)
                                            myDimensions.pop(myDimensions.index(item2))
                                            print("=======AFTER POP=======")
                                            print(myDimensions)
                                            print("=======================")
                                            # print("DUPLICLATE", item, item2)
                                            # if item == item2:
                                            #     my_temp = myDimensions.pop(myDimensions.index(item))
                                            #     my_temp2 = 'Nothh'
                                            # else:
                                            #     my_temp = myDimensions.pop(myDimensions.index(item))
                                            #     my_temp2 = myDimensions.pop(myDimensions.index(item2))
                                            # print(my_temp, my_temp2)
                                    try:
                                        for item2 in myDimensions:
                                            if item in item2:
                                                print('DUP Again', item, item2)
                                                myDimensions.pop(myDimensions.index(item2))
                                        myDimensions.pop(myDimensions.index(item))
                                    except:
                                        myDimensions.append("Year>{}".format(item))


                                    print("=======MYDIM YEARLY=======")
                                    print(myDimensions)
                                    print("==========================")
                                    dataForPlot = myData2.pivot_table(index=list(set(myDimensions)), values=myMeasurements, aggfunc=np.sum)
                                else:
                                    print("=======MYDIM DAILY=======")
                                    print(myDimensions)
                                    print("==========================")
                                    for item2 in myDimensions:
                                        print("Checking(Daily):", item, item2)
                                        if item in item2:
                                            print("DUP", item, item2)
                                            myDimensions.pop(myDimensions.index(item2))
                                            print("=======AFTER POP=======")
                                            print(myDimensions)
                                            print("=======================")
                                            # print("DUPLICLATE", item, item2)
                                            # if item == item2:
                                            #     my_temp = myDimensions.pop(myDimensions.index(item))
                                            #     my_temp2 = 'Nothh'
                                            # else:
                                            #     my_temp = myDimensions.pop(myDimensions.index(item))
                                            #     my_temp2 = myDimensions.pop(myDimensions.index(item2))
                                            # print(my_temp, my_temp2)
                                    try:
                                        for item2 in myDimensions:
                                            if item in item2:
                                                print('DUP Again', item, item2)
                                                myDimensions.pop(myDimensions.index(item2))
                                        myDimensions.pop(myDimensions.index(item))
                                    except:
                                        myDimensions.append(item)
                                    dataForPlot = myData2.pivot_table(index=myDimensions, values=myMeasurements, aggfunc=np.sum)

                    else:
                        # print('Mydata!!!!!!!!!!!!!!!!!!!', self.data3)
                        dataForPlot = myData2.pivot_table(index=myDimensions, values=myMeasurements, aggfunc=np.sum)

                print("Going to plot!")
                print(myDimensions)
                # mydata4 = dataForPlot.set_index(myDimensions, append=True).rename_axis([None, None, None]).squeeze().unstack()
                # print(mydata4)
                myFinaldata = dataForPlot
                self.data3 = myFinaldata.reset_index()
                myData2 = dataForPlot

                if self.graph_selected == 'Bar':
                    self.bar2(dataForPlot)
                    # self.plotWidget.autoRange()
                elif self.graph_selected == 'Line':
                    self.lineChart(dataForPlot)
                    # self.plotWidget.autoRange()
                elif self.graph_selected == 'Scatter':
                    self.scatterChart(dataForPlot)
                    # self.plotWidget.autoRange()
                # self.sc.update_figure(dataForPlot)
                # self.data3 = dataForPlot
                self.updateTable()
                # pltwid = pg.plot(title='new')
                # pltwid.plot(dataForPlot)
                print("Plot")

        except:
            print("-----From OUTSIDE-----")
            print(sys.exc_info()[0], sys.exc_info()[1])

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
            if item in self.timedata:
                date_start = self.tab.findChild(QtWidgets.QDateTimeEdit,
                                                'datepicker_start>{}'.format(item)).date().toString("d/M/yyyy")
                date_stop = self.tab.findChild(QtWidgets.QDateTimeEdit,
                                               'datepicker_stop>{}'.format(item)).date().toString("d/M/yyyy")
                self.filterSelected.append(item)
                self.filter[item] = [date_start, date_stop]
            else:
                print("I'm Here!")
                try:
                    commoboxChild = self.tab.findChild(CheckComboBox, "combobox>{}".format(item)).getItemChecked()
                    # print(commoboxChild, "CHIlddd")
                    if commoboxChild != item:
                        self.filterSelected.append(item)
                        self.filter[item] = commoboxChild
                except:
                    pass


        # Cast filterSelected to list without duplicate
        self.filterSelected = list(set(self.filterSelected))
        # print(self.filterSelected, "Filter Select")
        # print(self.filter, "Filter"
        # After refresh, getComboOptions
        result = self.getComboOptions()
        return result

    def getComboOptions(self):
        # Caution
        # Require refresh before you call this function
        print(self.data)
        print("=======Dimensional=======")
        Dimensional = self.dimSelected
        print(Dimensional)
        Measurementional = self.measSelected
        myFilterSelected = self.filterSelected
        myFilter = self.filter
        # print("Before myFilter")
        # print(Dimensional, Measurementional, Dimensional+Measurementional)
        print("=======myData2=======")
        myData2 = self.data[Dimensional + Measurementional]
        print(myData2)
        # print(myFilter, "MY FILTER")
        # print(myFilterSelected, "MY FILRERSELECTED")

        for i in range(len(myFilterSelected)):
            tempFilter = []
            try:
                if myFilterSelected[i] in self.timedata:
                    # print("PASS")
                    pass
                else:
                    for j in range(len(myFilter[myFilterSelected[i]])):
                        tempFilter.append(myFilter[myFilterSelected[i]][j])

                    # print("This is TEMPss: ", tempFilter)
                    operationsCode = self.getOpcode(myFilterSelected[i], tempFilter)
                    print("=======RopCode=======")
                    print(operationsCode)
                    myData2 = myData2[eval(operationsCode)]
            except:
                print("Error at getComboOptions occurred")

        for i, item in enumerate(Dimensional):
            dataunique = myData2[Dimensional[i]].unique()
            print("=======dataunique=======")
            print(dataunique)
            print("=======combooptino=======")
            print(self.combo_option)
            self.combo_option[item] = [item for item in dataunique if isinstance(item, str)]
            self.combo_option2 = {k: v for k, v in self.combo_option.items() if v and v[0]}
            print("=======combooptino22222=======")
            print(self.combo_option2)
        result = self.combo_option2
        print("=======Resut=======")
        print(result)
        return result

    def clearandclean(self):
        # Clear all temp and Add new combobox
        self.filterSelected = []
        self.filter = {}
        self.dimSelected = []
        self.measSelected = []
        # self.combo_option = []

        self.clearLayout()
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        self.listWidget_4.clear()

        self.setTab2()
        self.plotWidget.clear()
        self.plotWidget.clearPlots()
        self.plotWidget.getAxis('bottom').setTicks([])
        try:
            self.legend.scene().removeItem(self.legend)
        except:
            pass
        self.dimdata = self.data.select_dtypes(include=['object', np.datetime64])
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
            combobox.addItem(item)
            combobox.addItems(combo_option[item])
            combobox.currentTextChanged.connect(self.on_combobox_changed)
            self.verticalLayout.addWidget(combobox)

    def rand_color(self, n):
        '''Random n dist    inct color'''
        colors = []
        r = int(random.random() * 256)
        g = int(random.random() * 256)
        b = int(random.random() * 256)
        step = 256 / n
        for i in range(n):
            r += step
            g += step
            b += step
            r = int(r) % 256
            g = int(g) % 256
            b = int(b) % 256
            colors.append((r, g, b))
        return colors

    def lineChart2(self, df):
        '''Plot line chart in chart tab.'''
        dimensionsAxis = df.index.values
        # self.plotTable(dimensionsAxis)
        self.plotWidget.showGrid(x=False, y=False)
        measurementAxis = self.measSelected
        dimensionsAxis = df.index.values
        dimensionsAxis = list(enumerate(dimensionsAxis))
        self.plotWidget.clear()
        self.plotWidget.clearPlots()
        if self.legend != None:
            self.legend.scene().removeItem(self.legend)
        self.legend = self.plotWidget.addLegend()
        colors = self.rand_color(len(measurementAxis))
        for eachMeasurement, color in zip(measurementAxis, colors):
            x = df.shape[0]
            y = list(df[eachMeasurement])
            self.plotWidget.plot(x=np.arange(x), y=y, pen=color, symbol='x', symbolPen=color, name=eachMeasurement)
        self.plotWidget.getAxis('bottom').setTicks([dimensionsAxis])


    def scatterChart(self, df):
        '''Scatter chart in chart tab.'''
        self.plotWidget.showGrid(x=False, y=False)
        measurementAxis = self.measSelected
        dimensionsAxis = df.index.values
        dimensionsAxis = list(enumerate(dimensionsAxis))
        self.plotWidget.clear()
        self.plotWidget.clearPlots()
        if self.legend != None:
            self.legend = self.plotWidget.addLegend()
        else:
            try:
                self.legend.scene().removeItem(self.legend)
            except:
                print("=======ERROR=======")
                self.legend = self.plotWidget.addLegend()
                pass
        colors = self.rand_color(len(measurementAxis))
        y_Min = 0
        y_Max = 0
        for eachMeasurement, color in zip(measurementAxis, colors):
            x = df.shape[0]
            y = df[eachMeasurement]
            ymax = np.max(y)
            ymin = np.min(y)
            if ymax > y_Max:
                y_Max = ymax
            if ymin < y_Min:
                y_Min = ymin
            print("Y max: ", y_Max)
            print("Y min: ", y_Min)
            scatter = pg.ScatterPlotItem(size=10, pen=color, name=eachMeasurement)
            scatter.addPoints(x=np.arange(x), y=y)
            self.plotWidget.addItem(scatter)
            self.plotWidget.plot(name=eachMeasurement, pen=color)
        self.plotWidget.setLimits(yMin=y_Min, yMax=y_Max, xMin=0, xMax=df.shape[0])
        self.plotWidget.setMouseEnabled(x=True, y=False)
        self.plotWidget.setXRange(0, 10)
        self.plotWidget.getAxis('bottom').setTicks([dimensionsAxis])

    def lineChart(self, df):
        '''Plot line chart in chart tab.'''
        try:
            self.plotWidget.showGrid(x=False, y=False)
            measurementAxis = self.measSelected
            dimensionsAxis = df.index.values
            dimensionsAxis = list(enumerate(dimensionsAxis))
            print(dimensionsAxis)
            self.plotWidget.clear()
            self.plotWidget.clearPlots()
            if self.legend != None:
                self.legend = self.plotWidget.addLegend()
            else:
                try:
                    self.legend.scene().removeItem(self.legend)
                except:
                    print("=======ERROR=======")
                    self.legend = self.plotWidget.addLegend()
                    pass
            colors = self.rand_color(len(measurementAxis))
            print("Going to loop")
            y_Min = 0
            y_Max = 0
            for eachMeasurement, color in zip(measurementAxis, colors):
                print(eachMeasurement)
                x = df.shape[0]
                y = list(df[eachMeasurement])
                ymax = np.max(y)
                ymin = np.min(y)
                if ymax > y_Max:
                    y_Max = ymax
                if ymin < y_Min:
                    y_Min = ymin
                print("Y max: ", y_Max)
                print("Y min: ", y_Min)
                self.plotWidget.plot(x=np.arange(x), y=y, pen=color, symbol='x', symbolPen=color, name=eachMeasurement)
                print("---Pass---")
            print("=======Here=======")
            self.plotWidget.setLimits(yMin=y_Min, yMax=y_Max, xMin=0, xMax=df.shape[0])
            self.plotWidget.setMouseEnabled(x=True, y=False)
            self.plotWidget.setXRange(0, 10)
            self.plotWidget.getAxis('bottom').setTicks([dimensionsAxis])

        except:
            print("=======From Line Chart=======")
            print(sys.exc_info()[0], sys.exc_info()[1])
            print("=============================")


    def bar2(self, df):
        print("=======Bar Chart=======")
        dimensionsAxis = df.index.values
        self.plotWidget.showGrid(x=False, y=False)
        measurementAxis = self.measSelected
        dimensionsAxis = df.index.values
        dimensionsAxis = list(enumerate(dimensionsAxis))
        self.plotWidget.clear()
        self.plotWidget.clearPlots()
        colors = self.rand_color(len(measurementAxis))
        if self.legend != None:
            self.legend = self.plotWidget.addLegend()
        else:
            try:
                self.legend.scene().removeItem(self.legend)
            except:
                print("=======ERROR=======")
                self.legend = self.plotWidget.addLegend()
                pass
        y_Min = 0
        y_Max = 0
        for eachMeasurement, color in zip(measurementAxis, colors):
            x = df.shape[0]
            y = df[eachMeasurement]
            ymax = np.max(y)
            ymin = np.min(y)
            if ymax > y_Max:
                y_Max = ymax
            if ymin < y_Min:
                y_Min = ymin
            print("Y max: ", y_Max)
            print("Y min: ", y_Min)
            barChart = pg.BarGraphItem(x=np.arange(x), height=y, width=0.5, brush=color)
            self.plotWidget.addItem(barChart)
            self.plotWidget.plot(name=eachMeasurement, pen=color)

        self.plotWidget.setLimits(yMin=y_Min, yMax=y_Max, xMax=df.shape[0])
        self.plotWidget.setMouseEnabled(x=True, y=False)
        self.plotWidget.setXRange(0, 10)
        print("Set Limit: yMin: {}, yMax: {}".format(y_Min, y_Max))
        self.plotWidget.getAxis('bottom').setTicks([dimensionsAxis])


    def get_range(self):
        print(self.plotWidget.viewRange())
        print(self.plotWidget.viewRect())

    def barChart(self, df):
        '''Plot bar chart in chart tab.'''
        try:
            dimensionsAxis = df.index.values
            self.plotWidget.showGrid(x=False, y=False)
            measurementAxis = list(self.iterFlatten(df.values.astype(float).tolist()))
            dimensionsAxis = list(map(str, df.index.values))
            dimensionsAxis = list(enumerate(dimensionsAxis))
            print(dimensionsAxis)
            print(measurementAxis)
            self.plotWidget.clear()
            self.plotWidget.clearPlots()
            vals = np.linspace(0,1,256)
            np.random.shuffle(vals)
            self.plotWidget.addLegend()
            n = len(self.measSelected)
            lm = len(measurementAxis)
            barChart = pg.BarGraphItem(x=np.arange(lm), height=measurementAxis, width=0.5, brush='r')
            self.plotWidget.addItem(barChart)
            self.plotWidget.getAxis('bottom').setTicks([dimensionsAxis])
        except:
            print("=======From Bar Plot=======")
            print(sys.exc_info()[0], sys.exc_info()[1])
            print("===========================")

    def iterFlatten(self, root):
        if isinstance(root, (list, tuple)):
            for element in root:
                for e in self.iterFlatten(element):
                    yield e
        else:
            yield root

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    atexit.register(ui.save)
    sys.exit(app.exec_())
