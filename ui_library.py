# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_library.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Library(object):
    def setupUi(self, Library):
        Library.setObjectName("Library")
        Library.setWindowModality(QtCore.Qt.WindowModal)
        Library.resize(857, 727)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        Library.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Library.setWindowIcon(icon)
        Library.setStyleSheet("QWidget#Library {background-color: #FFFFFF; }")
        self.gridLayout_3 = QtWidgets.QGridLayout(Library)
        self.gridLayout_3.setContentsMargins(0, -1, 0, 0)
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setVerticalSpacing(10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.librairies_tabs = QtWidgets.QTabWidget(Library)
        self.librairies_tabs.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.librairies_tabs.setObjectName("librairies_tabs")
        self.gridLayout_3.addWidget(self.librairies_tabs, 0, 0, 1, 1)

        self.retranslateUi(Library)
        QtCore.QMetaObject.connectSlotsByName(Library)

    def retranslateUi(self, Library):
        _translate = QtCore.QCoreApplication.translate
        Library.setWindowTitle(_translate("Library", "Bible externe"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Library = QtWidgets.QWidget()
    ui = Ui_Library()
    ui.setupUi(Library)
    Library.show()
    sys.exit(app.exec_())
