import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QMenu, QWidget



class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.lbl = QtWidgets.QLabel("Ubuntu", self)

        self.combo = QtWidgets.QComboBox(self)
        self.combo.setContextMenuPolicy(Qt.CustomContextMenu)
        self.combo.customContextMenuRequested.connect(self.showMenu)
        self.combo.addItem("Ubuntu")
        self.combo.addItem("Mandriva")
        self.combo.addItem("Fedora")
        self.combo.addItem("Red Hat")
        self.combo.addItem("Gentoo")

        self.combo.move(50, 50)
        self.lbl.move(50, 150)

        self.combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QComboBox')
        self.show()

    def showMenu(self,pos):
        menu = QtWidgets.QMenu()
        clear_action = menu.addAction("Clear Selection")
        filter_action = menu.addAction("Filter...")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == clear_action:
            self.pp()
            self.combo.setCurrentIndex(0)
        elif action == filter_action:
            print("Filter")

    def pp(self):
        print("Yes")

    def onActivated(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()

def main():

    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()