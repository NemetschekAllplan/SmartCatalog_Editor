# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_library_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LibraryTab(object):
    def setupUi(self, LibraryTab):
        LibraryTab.setObjectName("LibraryTab")
        LibraryTab.resize(1011, 726)
        LibraryTab.setAcceptDrops(True)
        LibraryTab.setWindowTitle("Form")
        self.gridLayout_2 = QtWidgets.QGridLayout(LibraryTab)
        self.gridLayout_2.setContentsMargins(0, -1, 0, 0)
        self.gridLayout_2.setVerticalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bible_splitter = QtWidgets.QSplitter(LibraryTab)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bible_splitter.setFont(font)
        self.bible_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.bible_splitter.setHandleWidth(10)
        self.bible_splitter.setChildrenCollapsible(False)
        self.bible_splitter.setObjectName("bible_splitter")
        self.hierarchy = Hierarchy(self.bible_splitter)
        self.hierarchy.setMinimumSize(QtCore.QSize(450, 0))
        self.hierarchy.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.hierarchy.setStyleSheet("")
        self.hierarchy.setLineWidth(9)
        self.hierarchy.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.hierarchy.setTabKeyNavigation(True)
        self.hierarchy.setDragEnabled(True)
        self.hierarchy.setAlternatingRowColors(True)
        self.hierarchy.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.hierarchy.setIconSize(QtCore.QSize(20, 20))
        self.hierarchy.setAnimated(True)
        self.hierarchy.setExpandsOnDoubleClick(False)
        self.hierarchy.setObjectName("hierarchy")
        self.library_details = QtWidgets.QTableView(self.bible_splitter)
        self.library_details.setMinimumSize(QtCore.QSize(450, 0))
        self.library_details.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.library_details.setStyleSheet("QHeaderView {background-color: #d8e9e8}")
        self.library_details.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.library_details.setAlternatingRowColors(True)
        self.library_details.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.library_details.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.library_details.setObjectName("library_details")
        self.library_details.horizontalHeader().setStretchLastSection(True)
        self.library_details.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.bible_splitter, 1, 1, 1, 1)
        self.fond = QtWidgets.QWidget(LibraryTab)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background-color: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.add_possibilities_title = QtWidgets.QLabel(self.fond)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.add_possibilities_title.setFont(font)
        self.add_possibilities_title.setStyleSheet("")
        self.add_possibilities_title.setObjectName("add_possibilities_title")
        self.horizontalLayout_3.addWidget(self.add_possibilities_title)
        self.label_2 = QtWidgets.QLabel(self.fond)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setText(":")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.folder = QtWidgets.QPushButton(self.fond)
        self.folder.setMinimumSize(QtCore.QSize(30, 24))
        self.folder.setMaximumSize(QtCore.QSize(30, 24))
        self.folder.setFocusPolicy(QtCore.Qt.NoFocus)
        self.folder.setStyleSheet("QPushButton{border: 0px}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folder.setIcon(icon)
        self.folder.setIconSize(QtCore.QSize(20, 20))
        self.folder.setChecked(False)
        self.folder.setObjectName("folder")
        self.horizontalLayout_3.addWidget(self.folder)
        self.material = QtWidgets.QPushButton(self.fond)
        self.material.setMinimumSize(QtCore.QSize(30, 24))
        self.material.setMaximumSize(QtCore.QSize(30, 24))
        self.material.setFocusPolicy(QtCore.Qt.NoFocus)
        self.material.setStyleSheet("QPushButton{border: 0px}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/material.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.material.setIcon(icon1)
        self.material.setIconSize(QtCore.QSize(20, 20))
        self.material.setObjectName("material")
        self.horizontalLayout_3.addWidget(self.material)
        self.component = QtWidgets.QPushButton(self.fond)
        self.component.setMinimumSize(QtCore.QSize(30, 24))
        self.component.setMaximumSize(QtCore.QSize(30, 24))
        self.component.setFocusPolicy(QtCore.Qt.NoFocus)
        self.component.setStyleSheet("QPushButton{border: 0px}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/component.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.component.setIcon(icon2)
        self.component.setIconSize(QtCore.QSize(20, 20))
        self.component.setObjectName("component")
        self.horizontalLayout_3.addWidget(self.component)
        self.link = QtWidgets.QPushButton(self.fond)
        self.link.setMinimumSize(QtCore.QSize(30, 24))
        self.link.setMaximumSize(QtCore.QSize(30, 24))
        self.link.setFocusPolicy(QtCore.Qt.NoFocus)
        self.link.setStyleSheet("QPushButton{border: 0px}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Images/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.link.setIcon(icon3)
        self.link.setIconSize(QtCore.QSize(20, 20))
        self.link.setObjectName("link")
        self.horizontalLayout_3.addWidget(self.link)
        self.attribute = QtWidgets.QPushButton(self.fond)
        self.attribute.setMinimumSize(QtCore.QSize(30, 24))
        self.attribute.setMaximumSize(QtCore.QSize(30, 24))
        self.attribute.setFocusPolicy(QtCore.Qt.NoFocus)
        self.attribute.setStyleSheet("QPushButton{border: 0px}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Images/attribute.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.attribute.setIcon(icon4)
        self.attribute.setIconSize(QtCore.QSize(20, 20))
        self.attribute.setObjectName("attribute")
        self.horizontalLayout_3.addWidget(self.attribute)
        self.none = QtWidgets.QPushButton(self.fond)
        self.none.setMinimumSize(QtCore.QSize(30, 24))
        self.none.setMaximumSize(QtCore.QSize(30, 24))
        self.none.setFocusPolicy(QtCore.Qt.NoFocus)
        self.none.setStyleSheet("QPushButton{border: 0px}")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Images/none.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.none.setIcon(icon5)
        self.none.setIconSize(QtCore.QSize(20, 20))
        self.none.setObjectName("none")
        self.horizontalLayout_3.addWidget(self.none)
        spacerItem1 = QtWidgets.QSpacerItem(157, 50, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
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
        spacerItem2 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout_2.addWidget(self.fond, 2, 0, 1, 3)
        spacerItem3 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 0, 1, 1)
        self.actionbar = QtWidgets.QWidget(LibraryTab)
        self.actionbar.setMinimumSize(QtCore.QSize(0, 71))
        self.actionbar.setMaximumSize(QtCore.QSize(16777215, 71))
        self.actionbar.setStyleSheet("QWidget#actionbar { border:1px solid #B2B2B2}")
        self.actionbar.setObjectName("actionbar")
        self.gridLayout = QtWidgets.QGridLayout(self.actionbar)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.library_refresh_title = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.library_refresh_title.sizePolicy().hasHeightForWidth())
        self.library_refresh_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.library_refresh_title.setFont(font)
        self.library_refresh_title.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.library_refresh_title.setAlignment(QtCore.Qt.AlignCenter)
        self.library_refresh_title.setObjectName("library_refresh_title")
        self.gridLayout.addWidget(self.library_refresh_title, 1, 1, 1, 1)
        self.library_collapse_all = QtWidgets.QPushButton(self.actionbar)
        self.library_collapse_all.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.library_collapse_all.sizePolicy().hasHeightForWidth())
        self.library_collapse_all.setSizePolicy(sizePolicy)
        self.library_collapse_all.setMinimumSize(QtCore.QSize(40, 0))
        self.library_collapse_all.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.library_collapse_all.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Images/collapse_all.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.library_collapse_all.setIcon(icon6)
        self.library_collapse_all.setIconSize(QtCore.QSize(24, 24))
        self.library_collapse_all.setShortcut("F4")
        self.library_collapse_all.setFlat(True)
        self.library_collapse_all.setObjectName("library_collapse_all")
        self.gridLayout.addWidget(self.library_collapse_all, 0, 3, 1, 1)
        self.library_expand_all = QtWidgets.QPushButton(self.actionbar)
        self.library_expand_all.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.library_expand_all.sizePolicy().hasHeightForWidth())
        self.library_expand_all.setSizePolicy(sizePolicy)
        self.library_expand_all.setMinimumSize(QtCore.QSize(40, 0))
        self.library_expand_all.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.library_expand_all.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Images/expand_all.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.library_expand_all.setIcon(icon7)
        self.library_expand_all.setIconSize(QtCore.QSize(24, 24))
        self.library_expand_all.setShortcut("F3")
        self.library_expand_all.setFlat(True)
        self.library_expand_all.setObjectName("library_expand_all")
        self.gridLayout.addWidget(self.library_expand_all, 0, 2, 1, 1)
        self.library_refresh = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.library_refresh.sizePolicy().hasHeightForWidth())
        self.library_refresh.setSizePolicy(sizePolicy)
        self.library_refresh.setMinimumSize(QtCore.QSize(80, 0))
        self.library_refresh.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.library_refresh.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Images/reset.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.library_refresh.setIcon(icon8)
        self.library_refresh.setIconSize(QtCore.QSize(24, 24))
        self.library_refresh.setShortcut("F5")
        self.library_refresh.setFlat(True)
        self.library_refresh.setObjectName("library_refresh")
        self.gridLayout.addWidget(self.library_refresh, 0, 1, 1, 1)
        self.library_expand_title = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.library_expand_title.sizePolicy().hasHeightForWidth())
        self.library_expand_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.library_expand_title.setFont(font)
        self.library_expand_title.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.library_expand_title.setAlignment(QtCore.Qt.AlignCenter)
        self.library_expand_title.setObjectName("library_expand_title")
        self.gridLayout.addWidget(self.library_expand_title, 1, 2, 1, 2)
        self.library_search_title = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.library_search_title.sizePolicy().hasHeightForWidth())
        self.library_search_title.setSizePolicy(sizePolicy)
        self.library_search_title.setMinimumSize(QtCore.QSize(255, 16))
        self.library_search_title.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.library_search_title.setFont(font)
        self.library_search_title.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.library_search_title.setAlignment(QtCore.Qt.AlignCenter)
        self.library_search_title.setObjectName("library_search_title")
        self.gridLayout.addWidget(self.library_search_title, 1, 6, 1, 1)
        self.search_widget = QtWidgets.QWidget(self.actionbar)
        self.search_widget.setStyleSheet("QWidget#search_widget{border-right: 1px solid #B2B2B2;}")
        self.search_widget.setObjectName("search_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.search_widget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(15, 0, 15, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.search_line = QtWidgets.QLineEdit(self.search_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_line.sizePolicy().hasHeightForWidth())
        self.search_line.setSizePolicy(sizePolicy)
        self.search_line.setMinimumSize(QtCore.QSize(300, 30))
        self.search_line.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.search_line.setFont(font)
        self.search_line.setStyleSheet("QLineEdit{border: 1px solid #8f8f91; border-radius: 5px; padding-left: 5px; }")
        self.search_line.setObjectName("search_line")
        self.horizontalLayout.addWidget(self.search_line)
        self.search_bt = QtWidgets.QPushButton(self.search_widget)
        self.search_bt.setMinimumSize(QtCore.QSize(40, 30))
        self.search_bt.setMaximumSize(QtCore.QSize(40, 30))
        self.search_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/Images/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_bt.setIcon(icon9)
        self.search_bt.setIconSize(QtCore.QSize(20, 20))
        self.search_bt.setCheckable(True)
        self.search_bt.setObjectName("search_bt")
        self.horizontalLayout.addWidget(self.search_bt)
        self.gridLayout.addWidget(self.search_widget, 0, 6, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 10, 1, 1)
        self.library_synchro = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.library_synchro.sizePolicy().hasHeightForWidth())
        self.library_synchro.setSizePolicy(sizePolicy)
        self.library_synchro.setMinimumSize(QtCore.QSize(80, 0))
        self.library_synchro.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.library_synchro.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/Images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.library_synchro.setIcon(icon10)
        self.library_synchro.setIconSize(QtCore.QSize(24, 24))
        self.library_synchro.setShortcut("F5")
        self.library_synchro.setFlat(True)
        self.library_synchro.setObjectName("library_synchro")
        self.gridLayout.addWidget(self.library_synchro, 0, 4, 1, 1)
        self.library_synchro_title = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.library_synchro_title.sizePolicy().hasHeightForWidth())
        self.library_synchro_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.library_synchro_title.setFont(font)
        self.library_synchro_title.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.library_synchro_title.setAlignment(QtCore.Qt.AlignCenter)
        self.library_synchro_title.setObjectName("library_synchro_title")
        self.gridLayout.addWidget(self.library_synchro_title, 1, 4, 1, 1)
        self.end_title = QtWidgets.QWidget(self.actionbar)
        self.end_title.setStyleSheet("QWidget#end_title{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.end_title.setObjectName("end_title")
        self.gridLayout.addWidget(self.end_title, 1, 10, 1, 1)
        self.gridLayout_2.addWidget(self.actionbar, 0, 1, 1, 1)

        self.retranslateUi(LibraryTab)
        QtCore.QMetaObject.connectSlotsByName(LibraryTab)
        LibraryTab.setTabOrder(self.library_refresh, self.library_expand_all)
        LibraryTab.setTabOrder(self.library_expand_all, self.library_collapse_all)
        LibraryTab.setTabOrder(self.library_collapse_all, self.library_synchro)
        LibraryTab.setTabOrder(self.library_synchro, self.search_line)
        LibraryTab.setTabOrder(self.search_line, self.search_bt)
        LibraryTab.setTabOrder(self.search_bt, self.hierarchy)
        LibraryTab.setTabOrder(self.hierarchy, self.library_details)
        LibraryTab.setTabOrder(self.library_details, self.ok)
        LibraryTab.setTabOrder(self.ok, self.quit)

    def retranslateUi(self, LibraryTab):
        _translate = QtCore.QCoreApplication.translate
        self.add_possibilities_title.setText(_translate("LibraryTab", "Ajout possible"))
        self.folder.setToolTip(_translate("LibraryTab", "Dossier"))
        self.material.setToolTip(_translate("LibraryTab", "Ouvrage"))
        self.component.setToolTip(_translate("LibraryTab", "Composant"))
        self.link.setToolTip(_translate("LibraryTab", "Attribut"))
        self.attribute.setToolTip(_translate("LibraryTab", "Attribut"))
        self.none.setToolTip(_translate("LibraryTab", "Aucun ajout possible"))
        self.ok.setText(_translate("LibraryTab", "Ajouter"))
        self.quit.setText(_translate("LibraryTab", "Quitter"))
        self.library_refresh_title.setText(_translate("LibraryTab", "Rafraichir"))
        self.library_collapse_all.setToolTip(_translate("LibraryTab", "Replier tous les éléments"))
        self.library_expand_all.setToolTip(_translate("LibraryTab", "Déplier tous les éléments"))
        self.library_expand_title.setText(_translate("LibraryTab", "Affichage"))
        self.library_search_title.setText(_translate("LibraryTab", "Recherche"))
        self.search_line.setPlaceholderText(_translate("LibraryTab", "Rechercher"))
        self.search_bt.setToolTip(_translate("LibraryTab", "Lancer la recherche"))
        self.library_synchro_title.setText(_translate("LibraryTab", "Synchroniser"))
from hierarchy import Hierarchy
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LibraryTab = QtWidgets.QWidget()
    ui = Ui_LibraryTab()
    ui.setupUi(LibraryTab)
    LibraryTab.show()
    sys.exit(app.exec_())
