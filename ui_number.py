# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_number.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Number(object):
    def setupUi(self, Number):
        Number.setObjectName("Number")
        Number.setWindowModality(QtCore.Qt.WindowModal)
        Number.resize(500, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Number.setWindowIcon(icon)
        Number.setStyleSheet("QWidget#Number{background-color: #FFFFFF; }")
        self.gridLayout = QtWidgets.QGridLayout(Number)
        self.gridLayout.setContentsMargins(0, -1, 0, 0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.fond = QtWidgets.QWidget(Number)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.bt_valider = QtWidgets.QPushButton(self.fond)
        self.bt_valider.setMinimumSize(QtCore.QSize(120, 24))
        self.bt_valider.setMaximumSize(QtCore.QSize(120, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_valider.setFont(font)
        self.bt_valider.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.bt_valider.setIconSize(QtCore.QSize(18, 18))
        self.bt_valider.setObjectName("bt_valider")
        self.horizontalLayout_3.addWidget(self.bt_valider)
        self.bt_quitter = QtWidgets.QPushButton(self.fond)
        self.bt_quitter.setMinimumSize(QtCore.QSize(120, 24))
        self.bt_quitter.setMaximumSize(QtCore.QSize(120, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_quitter.setFont(font)
        self.bt_quitter.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.bt_quitter.setIconSize(QtCore.QSize(18, 18))
        self.bt_quitter.setObjectName("bt_quitter")
        self.horizontalLayout_3.addWidget(self.bt_quitter)
        spacerItem1 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.gridLayout.addWidget(self.fond, 3, 0, 1, 4)
        spacerItem2 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 0, 1, 1)
        self.verticalWidget = QtWidgets.QWidget(Number)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ele_type_title = QtWidgets.QLabel(self.verticalWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ele_type_title.setFont(font)
        self.ele_type_title.setObjectName("ele_type_title")
        self.verticalLayout.addWidget(self.ele_type_title)
        self.spin = QtWidgets.QSpinBox(self.verticalWidget)
        self.spin.setMinimumSize(QtCore.QSize(0, 30))
        self.spin.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.spin.setFont(font)
        self.spin.setStyleSheet("QSpinBox {padding-left: 5px; border: 1px solid #8f8f91; border-radius:5px; }\n"
"\n"
"QSpinBox::up-button {width: 22px; image: url(:/Images/spin_up.svg); border-left: 1px solid #8f8f91; border-top-right-radius:5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QSpinBox::up-button:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QSpinBox::up-button:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"\n"
"\n"
"QSpinBox::down-button {width: 22px; image: url(:/Images/spin_down.svg); border-left: 1px solid #8f8f91; border-top: 1px solid #8f8f91;  border-bottom-right-radius:5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QSpinBox::down-button:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QSpinBox::down-button:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"")
        self.spin.setMinimum(1)
        self.spin.setObjectName("spin")
        self.verticalLayout.addWidget(self.spin)
        self.gridLayout.addWidget(self.verticalWidget, 0, 1, 1, 1)
        self.verticalWidget_2 = QtWidgets.QWidget(Number)
        self.verticalWidget_2.setObjectName("verticalWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ele_type_title_2 = QtWidgets.QLabel(self.verticalWidget_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ele_type_title_2.setFont(font)
        self.ele_type_title_2.setObjectName("ele_type_title_2")
        self.verticalLayout_2.addWidget(self.ele_type_title_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.description_chk = QtWidgets.QCheckBox(self.verticalWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description_chk.sizePolicy().hasHeightForWidth())
        self.description_chk.setSizePolicy(sizePolicy)
        self.description_chk.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.description_chk.setFont(font)
        self.description_chk.setStyleSheet("QCheckBox {padding-left: 5px; padding-right: 5px; border: 1px solid #8f8f91; border-bottom-width: 0px; border-right-width: 0px; border-top-left-radius:5px;background-color: #DBE4EE;  }\n"
"")
        self.description_chk.setObjectName("description_chk")
        self.gridLayout_2.addWidget(self.description_chk, 0, 0, 1, 1)
        self.separator = QtWidgets.QLineEdit(self.verticalWidget_2)
        self.separator.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.separator.setFont(font)
        self.separator.setStyleSheet("QLineEdit {padding-left: 5px; border: 1px solid #8f8f91; border-bottom-width: 0px; border-top-right-radius:5px; background-color: #DBE4EE }\n"
"")
        self.separator.setText("|")
        self.separator.setMaxLength(1)
        self.separator.setAlignment(QtCore.Qt.AlignCenter)
        self.separator.setObjectName("separator")
        self.gridLayout_2.addWidget(self.separator, 0, 1, 1, 1)
        self.titles = QtWidgets.QPlainTextEdit(self.verticalWidget_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.titles.setFont(font)
        self.titles.setStyleSheet("QPlainTextEdit{border: 1px solid #8f8f91; padding: 5px; padding-right: 5px; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px; background-color: #FFFFFF; }")
        self.titles.setTabChangesFocus(True)
        self.titles.setObjectName("liste_titres")
        self.gridLayout_2.addWidget(self.titles, 1, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout.addWidget(self.verticalWidget_2, 1, 1, 1, 1)

        self.retranslateUi(Number)
        QtCore.QMetaObject.connectSlotsByName(Number)
        Number.setTabOrder(self.spin, self.description_chk)
        Number.setTabOrder(self.description_chk, self.separator)
        Number.setTabOrder(self.separator, self.titles)
        Number.setTabOrder(self.titles, self.bt_valider)
        Number.setTabOrder(self.bt_valider, self.bt_quitter)

    def retranslateUi(self, Number):
        _translate = QtCore.QCoreApplication.translate
        Number.setWindowTitle(_translate("Number", "Ajout multiple"))
        self.bt_valider.setToolTip(_translate("Number", "Valider"))
        self.bt_valider.setText(_translate("Number", "Valider"))
        self.bt_quitter.setToolTip(_translate("Number", "Annuler"))
        self.bt_quitter.setText(_translate("Number", "Annuler"))
        self.ele_type_title.setText(_translate("Number", "Nombre"))
        self.ele_type_title_2.setText(_translate("Number", "Titres & Description"))
        self.description_chk.setText(_translate("Number", "Avec description -> Séparateur :"))
        self.separator.setPlaceholderText(_translate("Number", "Séparateur"))
        self.titles.setPlaceholderText(_translate("Number", "Ici, vous pouvez écrire les titres dès maintenant"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Number = QtWidgets.QWidget()
    ui = Ui_Number()
    ui.setupUi(Number)
    Number.show()
    sys.exit(app.exec_())
