# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_choices.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Choices(object):
    def setupUi(self, Choices):
        Choices.setObjectName("Choices")
        Choices.setWindowModality(QtCore.Qt.ApplicationModal)
        Choices.resize(500, 225)
        Choices.setMinimumSize(QtCore.QSize(500, 225))
        Choices.setMaximumSize(QtCore.QSize(500, 225))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Choices.setWindowIcon(icon)
        Choices.setStyleSheet("QWidget#Choices {background:#FFFFFF}")
        self.gridLayout = QtWidgets.QGridLayout(Choices)
        self.gridLayout.setContentsMargins(0, -1, 0, 0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(6, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.search_in_widget = QtWidgets.QWidget(Choices)
        self.search_in_widget.setObjectName("search_in_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.search_in_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QtWidgets.QLabel(self.search_in_widget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setWhatsThis("")
        self.title.setText("Title")
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title)
        self.choices_table = QtWidgets.QTableView(self.search_in_widget)
        self.choices_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.choices_table.setAlternatingRowColors(True)
        self.choices_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.choices_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.choices_table.setObjectName("choices_table")
        self.choices_table.horizontalHeader().setVisible(False)
        self.choices_table.horizontalHeader().setStretchLastSection(True)
        self.choices_table.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.choices_table)
        self.gridLayout.addWidget(self.search_in_widget, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(6, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.fond = QtWidgets.QWidget(Choices)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.ok = QtWidgets.QPushButton(self.fond)
        self.ok.setMinimumSize(QtCore.QSize(120, 24))
        self.ok.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.ok.setFont(font)
        self.ok.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.ok.setShortcut("Ctrl+S")
        self.ok.setObjectName("ok")
        self.horizontalLayout_3.addWidget(self.ok)
        self.quit = QtWidgets.QPushButton(self.fond)
        self.quit.setMinimumSize(QtCore.QSize(120, 24))
        self.quit.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.quit.setFont(font)
        self.quit.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.quit.setShortcut("Esc")
        self.quit.setObjectName("quit")
        self.horizontalLayout_3.addWidget(self.quit)
        spacerItem3 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addWidget(self.fond, 1, 0, 1, 3)

        self.retranslateUi(Choices)
        QtCore.QMetaObject.connectSlotsByName(Choices)

    def retranslateUi(self, Choices):
        _translate = QtCore.QCoreApplication.translate
        self.ok.setText(_translate("Choices", "Valider"))
        self.quit.setText(_translate("Choices", "Annuler"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Choices = QtWidgets.QWidget()
    ui = Ui_Choices()
    ui.setupUi(Choices)
    Choices.show()
    sys.exit(app.exec_())
