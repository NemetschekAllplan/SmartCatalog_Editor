# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_room_favorite_modify.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RoomFavoriteModify(object):
    def setupUi(self, RoomFavoriteModify):
        RoomFavoriteModify.setObjectName("RoomFavoriteModify")
        RoomFavoriteModify.setWindowModality(QtCore.Qt.ApplicationModal)
        RoomFavoriteModify.resize(300, 82)
        RoomFavoriteModify.setMaximumSize(QtCore.QSize(300, 82))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        RoomFavoriteModify.setWindowIcon(icon)
        RoomFavoriteModify.setStyleSheet("QWidget#RoomFavoriteModify {background-color: #FFFFFF; }")
        self.gridLayout = QtWidgets.QGridLayout(RoomFavoriteModify)
        self.gridLayout.setContentsMargins(0, -1, 0, 0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.title_layer_1 = QtWidgets.QHBoxLayout()
        self.title_layer_1.setSpacing(0)
        self.title_layer_1.setObjectName("title_layer_1")
        self.favorite_name = QtWidgets.QLineEdit(RoomFavoriteModify)
        self.favorite_name.setMinimumSize(QtCore.QSize(0, 30))
        self.favorite_name.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.favorite_name.setFont(font)
        self.favorite_name.setStyleSheet("QLineEdit{padding-left: 5px; border: 1px solid #8f8f91; border-right-width: 0px; border-top-left-radius:5px; border-bottom-left-radius: 5px; }")
        self.favorite_name.setMaxLength(27)
        self.favorite_name.setObjectName("favorite_name")
        self.title_layer_1.addWidget(self.favorite_name)
        self.format_bt = QtWidgets.QPushButton(RoomFavoriteModify)
        self.format_bt.setMinimumSize(QtCore.QSize(30, 30))
        self.format_bt.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.format_bt.setFont(font)
        self.format_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-left-width: 0px; padding-left: 1px; border-right-width: 0px; padding-right: 1px; background-color:#FFFFFF; }\n"
"QPushButton:hover{border-left-width: 1px; padding-left: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{border-left-width: 1px; padding-left: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/format.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.format_bt.setIcon(icon1)
        self.format_bt.setIconSize(QtCore.QSize(16, 16))
        self.format_bt.setFlat(True)
        self.format_bt.setObjectName("format_bt")
        self.title_layer_1.addWidget(self.format_bt)
        self.verification = QtWidgets.QPushButton(RoomFavoriteModify)
        self.verification.setMinimumSize(QtCore.QSize(30, 30))
        self.verification.setMaximumSize(QtCore.QSize(30, 30))
        self.verification.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-top-right-radius:5px ; border-bottom-right-radius:5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.verification.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/valid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.verification.setIcon(icon2)
        self.verification.setIconSize(QtCore.QSize(20, 20))
        self.verification.setObjectName("verification")
        self.title_layer_1.addWidget(self.verification)
        self.gridLayout.addLayout(self.title_layer_1, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.ok = QtWidgets.QPushButton(RoomFavoriteModify)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ok.sizePolicy().hasHeightForWidth())
        self.ok.setSizePolicy(sizePolicy)
        self.ok.setMinimumSize(QtCore.QSize(100, 0))
        self.ok.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.ok.setFont(font)
        self.ok.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.ok.setObjectName("ok")
        self.horizontalLayout_3.addWidget(self.ok)
        self.quit = QtWidgets.QPushButton(RoomFavoriteModify)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quit.sizePolicy().hasHeightForWidth())
        self.quit.setSizePolicy(sizePolicy)
        self.quit.setMinimumSize(QtCore.QSize(100, 24))
        self.quit.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.quit.setFont(font)
        self.quit.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.quit.setObjectName("quit")
        self.horizontalLayout_3.addWidget(self.quit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.retranslateUi(RoomFavoriteModify)
        QtCore.QMetaObject.connectSlotsByName(RoomFavoriteModify)

    def retranslateUi(self, RoomFavoriteModify):
        _translate = QtCore.QCoreApplication.translate
        RoomFavoriteModify.setWindowTitle(_translate("RoomFavoriteModify", "Définir nom du favoris"))
        self.ok.setText(_translate("RoomFavoriteModify", "Valider"))
        self.quit.setText(_translate("RoomFavoriteModify", "Annuler"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RoomFavoriteModify = QtWidgets.QWidget()
    ui = Ui_RoomFavoriteModify()
    ui.setupUi(RoomFavoriteModify)
    RoomFavoriteModify.show()
    sys.exit(app.exec_())
