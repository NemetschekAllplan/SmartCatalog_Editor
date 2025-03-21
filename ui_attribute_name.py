# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_attribute_name.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AttributeName(object):
    def setupUi(self, AttributeName):
        AttributeName.setObjectName("AttributeName")
        AttributeName.resize(750, 40)
        AttributeName.setMinimumSize(QtCore.QSize(575, 40))
        AttributeName.setMaximumSize(QtCore.QSize(16777215, 40))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(AttributeName)
        self.horizontalLayout_3.setContentsMargins(15, 2, 15, 2)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.icon_folder = QtWidgets.QPushButton(AttributeName)
        self.icon_folder.setMinimumSize(QtCore.QSize(50, 26))
        self.icon_folder.setMaximumSize(QtCore.QSize(50, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.icon_folder.setFont(font)
        self.icon_folder.setFocusPolicy(QtCore.Qt.NoFocus)
        self.icon_folder.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.icon_folder.setStyleSheet("QPushButton{border: 2px solid #416596; border-radius: 5px ; background-color: #ffeebf; color: #416596 }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"")
        self.icon_folder.setIconSize(QtCore.QSize(20, 20))
        self.icon_folder.setObjectName("icon_folder")
        self.horizontalLayout_3.addWidget(self.icon_folder)
        self.name_attrib = QtWidgets.QLabel(AttributeName)
        self.name_attrib.setMinimumSize(QtCore.QSize(240, 26))
        self.name_attrib.setMaximumSize(QtCore.QSize(240, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.name_attrib.setFont(font)
        self.name_attrib.setObjectName("name_attrib")
        self.horizontalLayout_3.addWidget(self.name_attrib)
        self.type_attrib = QtWidgets.QLabel(AttributeName)
        self.type_attrib.setMinimumSize(QtCore.QSize(40, 26))
        self.type_attrib.setMaximumSize(QtCore.QSize(40, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.type_attrib.setFont(font)
        self.type_attrib.setStyleSheet("QLabel{color: grey; }")
        self.type_attrib.setText("ABC")
        self.type_attrib.setAlignment(QtCore.Qt.AlignCenter)
        self.type_attrib.setObjectName("type_attrib")
        self.horizontalLayout_3.addWidget(self.type_attrib)
        self.name_layer = QtWidgets.QHBoxLayout()
        self.name_layer.setSpacing(0)
        self.name_layer.setObjectName("name_layer")
        self.value_attrib = QtWidgets.QLineEdit(AttributeName)
        self.value_attrib.setMinimumSize(QtCore.QSize(100, 26))
        self.value_attrib.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.value_attrib.setFont(font)
        self.value_attrib.setStyleSheet("QLineEdit{padding-left: 5px; border: 1px solid #8f8f91; border-right-width: 0px; border-top-left-radius:5px; border-bottom-left-radius: 5px; }")
        self.value_attrib.setObjectName("value_attrib")
        self.name_layer.addWidget(self.value_attrib)
        self.verification_bt = QtWidgets.QPushButton(AttributeName)
        self.verification_bt.setMinimumSize(QtCore.QSize(40, 26))
        self.verification_bt.setMaximumSize(QtCore.QSize(40, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.verification_bt.setFont(font)
        self.verification_bt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verification_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-left-width: 0px; padding-left: 1px; border-right-width: 0px; padding-right: 1px; background-color:#FFFFFF; }\n"
"QPushButton:hover{border-left-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{border-left-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.verification_bt.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/test_verifier.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.verification_bt.setIcon(icon)
        self.verification_bt.setIconSize(QtCore.QSize(16, 16))
        self.verification_bt.setFlat(True)
        self.verification_bt.setObjectName("verification_bt")
        self.name_layer.addWidget(self.verification_bt)
        self.formatting_bt = QtWidgets.QPushButton(AttributeName)
        self.formatting_bt.setMinimumSize(QtCore.QSize(40, 26))
        self.formatting_bt.setMaximumSize(QtCore.QSize(40, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.formatting_bt.setFont(font)
        self.formatting_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-left-width: 0px; padding-left: 1px;  border-top-right-radius: 5px ; border-bottom-right-radius: 5px; background-color:#FFFFFF; }\n"
"QPushButton:hover{border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.formatting_bt.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/format.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.formatting_bt.setIcon(icon1)
        self.formatting_bt.setIconSize(QtCore.QSize(16, 16))
        self.formatting_bt.setFlat(True)
        self.formatting_bt.setObjectName("formatting_bt")
        self.name_layer.addWidget(self.formatting_bt)
        self.horizontalLayout_3.addLayout(self.name_layer)

        self.retranslateUi(AttributeName)
        QtCore.QMetaObject.connectSlotsByName(AttributeName)

    def retranslateUi(self, AttributeName):
        _translate = QtCore.QCoreApplication.translate
        self.icon_folder.setToolTip(_translate("AttributeName", "Choisir un icone"))
        self.name_attrib.setText(_translate("AttributeName", "Titre "))
        self.type_attrib.setToolTip(_translate("AttributeName", "Texte"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AttributeName = QtWidgets.QWidget()
    ui = Ui_AttributeName()
    ui.setupUi(AttributeName)
    AttributeName.show()
    sys.exit(app.exec_())
