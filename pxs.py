# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\asd.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
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

class ListS(QtWidgets.QListWidget):
    def __init__(self, title, parent):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)

        self.setGeometry(QtCore.QRect(170, 20, 401, 31))
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setAlternatingRowColors(True)
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setViewMode(QtWidgets.QListView.ListMode)
        self.setObjectName(title)

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
        print(mdd)

        if(QDropEvent.mimeData().hasFormat('application/x-qabstractitemmodeldatalist')):
            QDropEvent.accept()
            # QDropEvent.setDropAction(QtCore.Qt.MoveAction)
            name = QDropEvent.mimeData().data('application/x-qabstractitemmodeldatalist')
            # mm = QtCore.QTextCodec.availableCodecs(name)

            print(type(name))
            namees = name.data().decode('utf-8')
            print(namees, "asdasd")
            itemname = "".join(i for i in namees if i.isalpha() or i == '-' or i == ' ')
            print(itemname)

            self.addItem(itemname)
            print(self.items())

            # print(b'{}'.format(str(name)[1:]))
            # items = QtWidgets.QListWidgetItem(name)
            # self.addItem(items)



        print(mdd.formats())
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

        # byta = QDropEvent.mimeData().data('application/x-qabstractitemmodeldatalist')
        # datae = self.decode_data(byta)

        # print(mdd)
        print("WA")

    def decode_data(self, bytearray):

        data = []
        item = {}

        ds = QtCore.QDataStream(bytearray)
        while not ds.atEnd():

            row = ds.readInt32()
            column = ds.readInt32()

            map_items = ds.readInt32()
            for i in range(map_items):

                key = ds.readInt32()

                value = QtCore.QVariant()
                ds >> value
                item[QtCore.Qt.ItemDataRole(key)] = value

            data.append(item)

        return data






class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(592, 517)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 581, 501))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setGeometry(QtCore.QRect(0, 440, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(260, 380, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 380, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.listWidget = ListS("listWidget", self.tab)

        self.listWidget_2 = QtWidgets.QListWidget(self.tab)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 20, 161, 171))
        self.listWidget_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        for item in datak:
            items = QtWidgets.QListWidgetItem(item)
            self.listWidget_2.addItem(items)
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_3 = QtWidgets.QListWidget(self.tab)
        self.listWidget_3.setGeometry(QtCore.QRect(0, 210, 161, 171))
        self.listWidget_3.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_3.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_3.setObjectName("listWidget_3")
        for item in datak:
            items = QtWidgets.QListWidgetItem(item)
            self.listWidget_3.addItem(items)
        self.listWidget_4 = QtWidgets.QListWidget(self.tab)
        self.listWidget_4.setGeometry(QtCore.QRect(170, 60, 401, 31))
        self.listWidget_4.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.listWidget_4.setAcceptDrops(True)
        self.listWidget_4.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_4.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_4.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_4.setObjectName("listWidget_4")
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
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setGeometry(QtCore.QRect(169, 99, 401, 281))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color:rgb(225, 225, 225)")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 592, 21))
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

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_2.setText(_translate("MainWindow", "OK"))
        self.label.setText(_translate("MainWindow", "                  Dimention"))
        self.label_3.setText(_translate("MainWindow", "              Measurements"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.menuOption.setTitle(_translate("MainWindow", "Option"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

