from PyQt5 import QtGui, QtCore, QtWidgets
import sys, os

# subclass
class CheckableComboBox(QtWidgets.QComboBox):
    # once there is a checkState set, it is rendered
    # here we assume default Unchecked
    def addItem(self, item):
        super(CheckableComboBox, self).addItem(item)
        item = self.model().item(self.count()-1,0)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        item.view().pressed.connect(self.handlePress)

    def addItems(self, items):
        for item in items:
            super(CheckableComboBox, self).addItem(item)
            item = self.model().item(self.count()-1,0)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.view().pressed.connect(self.handlePress)

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

    def handlePress(self, index):
        print(index)

def clik():
    print("Clicked!")
    cc = ComboBox.getItemCheked()
    print(cc)
    # for i in range(ComboBox.count()):
    #     print(i)
    #     item = ComboBox.itemChecked(i)
    #     print(item)


# the basic main()
app = QtWidgets.QApplication(sys.argv)
dialog = QtWidgets.QMainWindow()
mainWidget = QtWidgets.QWidget()
dialog.setCentralWidget(mainWidget)
ComboBox = CheckableComboBox(mainWidget)
botton = QtWidgets.QPushButton(mainWidget)
botton.setGeometry(100, 100, 50, 20)
botton.setText("Click Me!")
botton.clicked.connect(clik)
for i in range(6):
    ComboBox.addItem("Combobox Item " + str(i))

dialog.show()
sys.exit(app.exec_())
