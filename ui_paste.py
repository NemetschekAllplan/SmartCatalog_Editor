# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_paste.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Paste(object):
    def setupUi(self, Paste):
        Paste.setObjectName("Paste")
        Paste.resize(375, 300)
        Paste.setWindowTitle("Form")
        self.gridLayout = QtWidgets.QGridLayout(Paste)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.tree = QtWidgets.QTreeView(Paste)
        self.tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tree.setTabKeyNavigation(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setIconSize(QtCore.QSize(20, 20))
        self.tree.setAnimated(True)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.setObjectName("tree")
        self.tree.header().setVisible(False)
        self.tree.header().setDefaultSectionSize(35)
        self.gridLayout.addWidget(self.tree, 0, 0, 1, 1)

        self.retranslateUi(Paste)
        QtCore.QMetaObject.connectSlotsByName(Paste)

    def retranslateUi(self, Paste):
        pass
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Paste = QtWidgets.QWidget()
    ui = Ui_Paste()
    ui.setupUi(Paste)
    Paste.show()
    sys.exit(app.exec_())