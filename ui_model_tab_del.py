# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_model_tab_del.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ModelTabDel(object):
    def setupUi(self, ModelTabDel):
        ModelTabDel.setObjectName("ModelTabDel")
        ModelTabDel.resize(316, 80)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 248, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 248, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 248, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 248, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        ModelTabDel.setPalette(palette)
        ModelTabDel.setWindowTitle("Form")
        ModelTabDel.setStyleSheet("QWidget#ModelModify {border: 1px solid #8f8f91}")
        self.verticalLayout = QtWidgets.QVBoxLayout(ModelTabDel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titre = QtWidgets.QLabel(ModelTabDel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.titre.setFont(font)
        self.titre.setObjectName("titre")
        self.verticalLayout.addWidget(self.titre)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bt_supprimer = QtWidgets.QPushButton(ModelTabDel)
        self.bt_supprimer.setMinimumSize(QtCore.QSize(100, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_supprimer.setFont(font)
        self.bt_supprimer.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.bt_supprimer.setIconSize(QtCore.QSize(20, 20))
        self.bt_supprimer.setObjectName("bt_supprimer")
        self.horizontalLayout.addWidget(self.bt_supprimer)
        self.bt_annuler = QtWidgets.QPushButton(ModelTabDel)
        self.bt_annuler.setMinimumSize(QtCore.QSize(100, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_annuler.setFont(font)
        self.bt_annuler.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.bt_annuler.setIconSize(QtCore.QSize(20, 20))
        self.bt_annuler.setShortcut("Del")
        self.bt_annuler.setObjectName("bt_annuler")
        self.horizontalLayout.addWidget(self.bt_annuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ModelTabDel)
        QtCore.QMetaObject.connectSlotsByName(ModelTabDel)

    def retranslateUi(self, ModelTabDel):
        _translate = QtCore.QCoreApplication.translate
        self.titre.setText(_translate("ModelTabDel", "Voulez-vous vraiment supprimer l\'onglet?"))
        self.bt_supprimer.setText(_translate("ModelTabDel", "Supprimer"))
        self.bt_annuler.setText(_translate("ModelTabDel", "Annuler"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ModelTabDel = QtWidgets.QWidget()
    ui = Ui_ModelTabDel()
    ui.setupUi(ModelTabDel)
    ModelTabDel.show()
    sys.exit(app.exec_())
