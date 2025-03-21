# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_ktlg.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Ktlg(object):
    def setupUi(self, Ktlg):
        Ktlg.setObjectName("Ktlg")
        Ktlg.setWindowModality(QtCore.Qt.ApplicationModal)
        Ktlg.resize(712, 603)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Ktlg.setWindowIcon(icon)
        Ktlg.setStyleSheet("QWidget#Ktlg {background:#FFFFFF}")
        self.gridLayout = QtWidgets.QGridLayout(Ktlg)
        self.gridLayout.setContentsMargins(0, 9, 0, 0)
        self.gridLayout.setHorizontalSpacing(9)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(9, 270, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(9, 270, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.actionbar = QtWidgets.QWidget(Ktlg)
        self.actionbar.setMinimumSize(QtCore.QSize(0, 71))
        self.actionbar.setMaximumSize(QtCore.QSize(16777215, 71))
        self.actionbar.setStyleSheet("QWidget#actionbar { border:1px solid #B2B2B2}")
        self.actionbar.setObjectName("actionbar")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.actionbar)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.default_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.default_bt.sizePolicy().hasHeightForWidth())
        self.default_bt.setSizePolicy(sizePolicy)
        self.default_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.default_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-left: 1px; padding-right: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; border-right-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.default_bt.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/reset.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.default_bt.setIcon(icon1)
        self.default_bt.setIconSize(QtCore.QSize(24, 24))
        self.default_bt.setFlat(True)
        self.default_bt.setObjectName("default_bt")
        self.gridLayout_2.addWidget(self.default_bt, 0, 5, 1, 1)
        self.current_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_bt.sizePolicy().hasHeightForWidth())
        self.current_bt.setSizePolicy(sizePolicy)
        self.current_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.current_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.current_bt.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/catalog.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.current_bt.setIcon(icon2)
        self.current_bt.setIconSize(QtCore.QSize(24, 24))
        self.current_bt.setFlat(True)
        self.current_bt.setObjectName("current_bt")
        self.gridLayout_2.addWidget(self.current_bt, 0, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 10, 1, 1)
        self.select_title = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_title.sizePolicy().hasHeightForWidth())
        self.select_title.setSizePolicy(sizePolicy)
        self.select_title.setMinimumSize(QtCore.QSize(0, 16))
        self.select_title.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.select_title.setFont(font)
        self.select_title.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.select_title.setAlignment(QtCore.Qt.AlignCenter)
        self.select_title.setObjectName("select_title")
        self.gridLayout_2.addWidget(self.select_title, 1, 2, 1, 2)
        self.browser_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browser_bt.sizePolicy().hasHeightForWidth())
        self.browser_bt.setSizePolicy(sizePolicy)
        self.browser_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.browser_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.browser_bt.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Images/browse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browser_bt.setIcon(icon3)
        self.browser_bt.setIconSize(QtCore.QSize(24, 24))
        self.browser_bt.setFlat(True)
        self.browser_bt.setObjectName("browser_bt")
        self.gridLayout_2.addWidget(self.browser_bt, 0, 6, 1, 1)
        self.select_none_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_none_bt.sizePolicy().hasHeightForWidth())
        self.select_none_bt.setSizePolicy(sizePolicy)
        self.select_none_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.select_none_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.select_none_bt.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Images/select_none.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_none_bt.setIcon(icon4)
        self.select_none_bt.setIconSize(QtCore.QSize(24, 24))
        self.select_none_bt.setFlat(True)
        self.select_none_bt.setObjectName("select_none_bt")
        self.gridLayout_2.addWidget(self.select_none_bt, 0, 3, 1, 1)
        self.save_favorite_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_favorite_bt.sizePolicy().hasHeightForWidth())
        self.save_favorite_bt.setSizePolicy(sizePolicy)
        self.save_favorite_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.save_favorite_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.save_favorite_bt.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Images/favorite_save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_favorite_bt.setIcon(icon5)
        self.save_favorite_bt.setIconSize(QtCore.QSize(22, 22))
        self.save_favorite_bt.setFlat(True)
        self.save_favorite_bt.setObjectName("save_favorite_bt")
        self.gridLayout_2.addWidget(self.save_favorite_bt, 0, 1, 1, 1)
        self.end_title = QtWidgets.QWidget(self.actionbar)
        self.end_title.setStyleSheet("QWidget#end_title{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.end_title.setObjectName("end_title")
        self.gridLayout_2.addWidget(self.end_title, 1, 10, 1, 1)
        self.select_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_bt.sizePolicy().hasHeightForWidth())
        self.select_bt.setSizePolicy(sizePolicy)
        self.select_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.select_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.select_bt.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Images/select_all.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_bt.setIcon(icon6)
        self.select_bt.setIconSize(QtCore.QSize(24, 24))
        self.select_bt.setFlat(True)
        self.select_bt.setObjectName("select_bt")
        self.gridLayout_2.addWidget(self.select_bt, 0, 2, 1, 1)
        self.open_favorite_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_favorite_bt.sizePolicy().hasHeightForWidth())
        self.open_favorite_bt.setSizePolicy(sizePolicy)
        self.open_favorite_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.open_favorite_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.open_favorite_bt.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Images/favorite_open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_favorite_bt.setIcon(icon7)
        self.open_favorite_bt.setIconSize(QtCore.QSize(24, 24))
        self.open_favorite_bt.setFlat(True)
        self.open_favorite_bt.setObjectName("open_favorite_bt")
        self.gridLayout_2.addWidget(self.open_favorite_bt, 0, 0, 1, 1)
        self.favorite_title = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.favorite_title.sizePolicy().hasHeightForWidth())
        self.favorite_title.setSizePolicy(sizePolicy)
        self.favorite_title.setMinimumSize(QtCore.QSize(0, 16))
        self.favorite_title.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.favorite_title.setFont(font)
        self.favorite_title.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.favorite_title.setAlignment(QtCore.Qt.AlignCenter)
        self.favorite_title.setObjectName("favorite_title")
        self.gridLayout_2.addWidget(self.favorite_title, 1, 0, 1, 2)
        self.options_title = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.options_title.sizePolicy().hasHeightForWidth())
        self.options_title.setSizePolicy(sizePolicy)
        self.options_title.setMinimumSize(QtCore.QSize(0, 16))
        self.options_title.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.options_title.setFont(font)
        self.options_title.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.options_title.setAlignment(QtCore.Qt.AlignCenter)
        self.options_title.setObjectName("options_title")
        self.gridLayout_2.addWidget(self.options_title, 1, 4, 1, 3)
        self.tools_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tools_bt.sizePolicy().hasHeightForWidth())
        self.tools_bt.setSizePolicy(sizePolicy)
        self.tools_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.tools_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; padding-top: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; padding-top: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.tools_bt.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Images/tool.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tools_bt.setIcon(icon8)
        self.tools_bt.setIconSize(QtCore.QSize(24, 24))
        self.tools_bt.setFlat(True)
        self.tools_bt.setObjectName("tools_bt")
        self.gridLayout_2.addWidget(self.tools_bt, 0, 7, 1, 1)
        self.tools_title = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tools_title.sizePolicy().hasHeightForWidth())
        self.tools_title.setSizePolicy(sizePolicy)
        self.tools_title.setMinimumSize(QtCore.QSize(80, 16))
        self.tools_title.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.tools_title.setFont(font)
        self.tools_title.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.tools_title.setAlignment(QtCore.Qt.AlignCenter)
        self.tools_title.setObjectName("tools_title")
        self.gridLayout_2.addWidget(self.tools_title, 1, 7, 1, 1)
        self.gridLayout.addWidget(self.actionbar, 0, 1, 1, 2)
        self.fond = QtWidgets.QWidget(Ktlg)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.save_bt = QtWidgets.QPushButton(self.fond)
        self.save_bt.setEnabled(False)
        self.save_bt.setMinimumSize(QtCore.QSize(100, 24))
        self.save_bt.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.save_bt.setFont(font)
        self.save_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7)}\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC)}\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8)}")
        self.save_bt.setShortcut("Ctrl+S")
        self.save_bt.setObjectName("save_bt")
        self.horizontalLayout_3.addWidget(self.save_bt)
        self.quit_bt = QtWidgets.QPushButton(self.fond)
        self.quit_bt.setMinimumSize(QtCore.QSize(100, 24))
        self.quit_bt.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.quit_bt.setFont(font)
        self.quit_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7)}\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC)}\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8)}")
        self.quit_bt.setShortcut("Ctrl+F4")
        self.quit_bt.setObjectName("quit_bt")
        self.horizontalLayout_3.addWidget(self.quit_bt)
        spacerItem4 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.gridLayout.addWidget(self.fond, 2, 0, 1, 4)
        self.ktlg_view = QtWidgets.QTreeView(Ktlg)
        self.ktlg_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ktlg_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ktlg_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ktlg_view.setIconSize(QtCore.QSize(20, 20))
        self.ktlg_view.setObjectName("ktlg_view")
        self.gridLayout.addWidget(self.ktlg_view, 1, 1, 1, 2)

        self.retranslateUi(Ktlg)
        QtCore.QMetaObject.connectSlotsByName(Ktlg)
        Ktlg.setTabOrder(self.open_favorite_bt, self.save_favorite_bt)
        Ktlg.setTabOrder(self.save_favorite_bt, self.select_bt)
        Ktlg.setTabOrder(self.select_bt, self.select_none_bt)
        Ktlg.setTabOrder(self.select_none_bt, self.current_bt)
        Ktlg.setTabOrder(self.current_bt, self.default_bt)
        Ktlg.setTabOrder(self.default_bt, self.browser_bt)
        Ktlg.setTabOrder(self.browser_bt, self.tools_bt)
        Ktlg.setTabOrder(self.tools_bt, self.ktlg_view)
        Ktlg.setTabOrder(self.ktlg_view, self.save_bt)
        Ktlg.setTabOrder(self.save_bt, self.quit_bt)

    def retranslateUi(self, Ktlg):
        _translate = QtCore.QCoreApplication.translate
        self.default_bt.setToolTip(_translate("Ktlg", "Mettre les paramètres par défaut"))
        self.current_bt.setToolTip(_translate("Ktlg", "Définir ce catalogue"))
        self.select_title.setText(_translate("Ktlg", "Sélection"))
        self.browser_bt.setToolTip(_translate("Ktlg", "Parcourir"))
        self.select_none_bt.setToolTip(_translate("Ktlg", "Désélectionner"))
        self.save_favorite_bt.setToolTip(_translate("Ktlg", "Enregistrer favoris"))
        self.open_favorite_bt.setToolTip(_translate("Ktlg", "Importer favoris"))
        self.favorite_title.setText(_translate("Ktlg", "Favoris"))
        self.options_title.setText(_translate("Ktlg", "Édition"))
        self.tools_bt.setToolTip(_translate("Ktlg", "Outils"))
        self.tools_title.setText(_translate("Ktlg", "Outils"))
        self.save_bt.setText(_translate("Ktlg", "Enregistrer"))
        self.quit_bt.setText(_translate("Ktlg", "Quitter"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Ktlg = QtWidgets.QWidget()
    ui = Ui_Ktlg()
    ui.setupUi(Ktlg)
    Ktlg.show()
    sys.exit(app.exec_())
