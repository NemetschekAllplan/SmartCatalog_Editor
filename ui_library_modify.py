# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_library_modify.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LibraryModify(object):
    def setupUi(self, LibraryModify):
        LibraryModify.setObjectName("LibraryModify")
        LibraryModify.setWindowModality(QtCore.Qt.ApplicationModal)
        LibraryModify.resize(450, 201)
        LibraryModify.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LibraryModify.setWindowIcon(icon)
        LibraryModify.setStyleSheet("QWidget#LibraryModify {background-color: #FFFFFF; }")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(LibraryModify)
        self.verticalLayout_3.setContentsMargins(-1, 6, -1, -1)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(9)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.path_text = QtWidgets.QLabel(LibraryModify)
        self.path_text.setMinimumSize(QtCore.QSize(0, 30))
        self.path_text.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.path_text.setFont(font)
        self.path_text.setStyleSheet("QLabel{padding-right: 10px}")
        self.path_text.setObjectName("path_text")
        self.horizontalLayout_5.addWidget(self.path_text)
        self.file_radio = QtWidgets.QRadioButton(LibraryModify)
        self.file_radio.setMinimumSize(QtCore.QSize(0, 30))
        self.file_radio.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.file_radio.setFont(font)
        self.file_radio.setChecked(True)
        self.file_radio.setObjectName("file_radio")
        self.horizontalLayout_5.addWidget(self.file_radio)
        self.url_radio = QtWidgets.QRadioButton(LibraryModify)
        self.url_radio.setMinimumSize(QtCore.QSize(0, 30))
        self.url_radio.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.url_radio.setFont(font)
        self.url_radio.setText("URL")
        self.url_radio.setObjectName("url_radio")
        self.horizontalLayout_5.addWidget(self.url_radio)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.path = QtWidgets.QLineEdit(LibraryModify)
        self.path.setMinimumSize(QtCore.QSize(0, 30))
        self.path.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.path.setFont(font)
        self.path.setStyleSheet("QLineEdit{padding-left: 5px; border: 1px solid #8f8f91; border-right-width: 0px; border-top-left-radius:5px; border-bottom-left-radius: 5px; }")
        self.path.setReadOnly(True)
        self.path.setObjectName("path")
        self.horizontalLayout_2.addWidget(self.path)
        self.browser = QtWidgets.QPushButton(LibraryModify)
        self.browser.setMinimumSize(QtCore.QSize(30, 30))
        self.browser.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.browser.setFont(font)
        self.browser.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-top-right-radius:5px ; border-bottom-right-radius:5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.browser.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/browse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browser.setIcon(icon1)
        self.browser.setIconSize(QtCore.QSize(20, 20))
        self.browser.setObjectName("browser")
        self.horizontalLayout_2.addWidget(self.browser)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_text = QtWidgets.QLabel(LibraryModify)
        self.title_text.setMinimumSize(QtCore.QSize(0, 30))
        self.title_text.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.title_text.setFont(font)
        self.title_text.setObjectName("title_text")
        self.verticalLayout_2.addWidget(self.title_text)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title = QtWidgets.QLineEdit(LibraryModify)
        self.title.setMinimumSize(QtCore.QSize(0, 30))
        self.title.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.title.setFont(font)
        self.title.setStyleSheet("QLineEdit{padding-left: 5px; border: 1px solid #8f8f91; border-right-width: 0px; border-top-left-radius:5px; border-bottom-left-radius: 5px; }")
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)
        self.format_bt = QtWidgets.QPushButton(LibraryModify)
        self.format_bt.setMinimumSize(QtCore.QSize(30, 30))
        self.format_bt.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.format_bt.setFont(font)
        self.format_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-left-width: 0px; padding-left: 1px; border-right-width: 0px; padding-right: 1px; background-color:#FFFFFF; }\n"
"QPushButton:hover{border-left-width: 1px; padding-left: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{border-left-width: 1px; padding-left: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/format.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.format_bt.setIcon(icon2)
        self.format_bt.setIconSize(QtCore.QSize(16, 16))
        self.format_bt.setFlat(True)
        self.format_bt.setObjectName("format_bt")
        self.horizontalLayout.addWidget(self.format_bt)
        self.verification = QtWidgets.QPushButton(LibraryModify)
        self.verification.setMinimumSize(QtCore.QSize(30, 30))
        self.verification.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.verification.setFont(font)
        self.verification.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-top-right-radius:5px ; border-bottom-right-radius:5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.verification.setText("")
        self.verification.setIconSize(QtCore.QSize(20, 20))
        self.verification.setObjectName("verification")
        self.horizontalLayout.addWidget(self.verification)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.ok = QtWidgets.QPushButton(LibraryModify)
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
        self.quit = QtWidgets.QPushButton(LibraryModify)
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
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(LibraryModify)
        QtCore.QMetaObject.connectSlotsByName(LibraryModify)
        LibraryModify.setTabOrder(self.file_radio, self.url_radio)
        LibraryModify.setTabOrder(self.url_radio, self.path)
        LibraryModify.setTabOrder(self.path, self.browser)
        LibraryModify.setTabOrder(self.browser, self.title)
        LibraryModify.setTabOrder(self.title, self.format_bt)
        LibraryModify.setTabOrder(self.format_bt, self.verification)
        LibraryModify.setTabOrder(self.verification, self.ok)
        LibraryModify.setTabOrder(self.ok, self.quit)

    def retranslateUi(self, LibraryModify):
        _translate = QtCore.QCoreApplication.translate
        self.path_text.setText(_translate("LibraryModify", "Chemin"))
        self.file_radio.setText(_translate("LibraryModify", "Fichier"))
        self.title_text.setText(_translate("LibraryModify", "Titre"))
        self.ok.setText(_translate("LibraryModify", "Valider"))
        self.quit.setText(_translate("LibraryModify", "Annuler"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LibraryModify = QtWidgets.QWidget()
    ui = Ui_LibraryModify()
    ui.setupUi(LibraryModify)
    LibraryModify.show()
    sys.exit(app.exec_())