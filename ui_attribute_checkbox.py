# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_attribute_checkbox.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AttributeCheckbox(object):
    def setupUi(self, AttributeCheckbox):
        AttributeCheckbox.setObjectName("AttributeCheckbox")
        AttributeCheckbox.resize(750, 40)
        AttributeCheckbox.setMinimumSize(QtCore.QSize(575, 40))
        AttributeCheckbox.setMaximumSize(QtCore.QSize(16777215, 40))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(AttributeCheckbox)
        self.horizontalLayout_3.setContentsMargins(15, 2, 15, 2)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.num_attrib = QtWidgets.QLabel(AttributeCheckbox)
        self.num_attrib.setMinimumSize(QtCore.QSize(50, 26))
        self.num_attrib.setMaximumSize(QtCore.QSize(50, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.num_attrib.setFont(font)
        self.num_attrib.setAlignment(QtCore.Qt.AlignCenter)
        self.num_attrib.setObjectName("num_attrib")
        self.horizontalLayout_3.addWidget(self.num_attrib)
        self.name_attrib = QtWidgets.QLabel(AttributeCheckbox)
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
        self.type_attrib = QtWidgets.QLabel(AttributeCheckbox)
        self.type_attrib.setMinimumSize(QtCore.QSize(40, 26))
        self.type_attrib.setMaximumSize(QtCore.QSize(40, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.type_attrib.setFont(font)
        self.type_attrib.setStyleSheet("QLabel{color: grey; }")
        self.type_attrib.setText("123")
        self.type_attrib.setAlignment(QtCore.Qt.AlignCenter)
        self.type_attrib.setObjectName("type_attrib")
        self.horizontalLayout_3.addWidget(self.type_attrib)
        self.value_attrib = QtWidgets.QCheckBox(AttributeCheckbox)
        self.value_attrib.setMinimumSize(QtCore.QSize(100, 26))
        self.value_attrib.setMaximumSize(QtCore.QSize(16777215, 26))
        self.value_attrib.setText("")
        self.value_attrib.setObjectName("value_attrib")
        self.horizontalLayout_3.addWidget(self.value_attrib)

        self.retranslateUi(AttributeCheckbox)
        QtCore.QMetaObject.connectSlotsByName(AttributeCheckbox)

    def retranslateUi(self, AttributeCheckbox):
        _translate = QtCore.QCoreApplication.translate
        self.type_attrib.setToolTip(_translate("AttributeCheckbox", "Nombre entier"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AttributeCheckbox = QtWidgets.QWidget()
    ui = Ui_AttributeCheckbox()
    ui.setupUi(AttributeCheckbox)
    AttributeCheckbox.show()
    sys.exit(app.exec_())
