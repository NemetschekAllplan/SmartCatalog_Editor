# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_formula.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Formula(object):
    def setupUi(self, Formula):
        Formula.setObjectName("Formula")
        Formula.setWindowModality(QtCore.Qt.WindowModal)
        Formula.resize(500, 525)
        Formula.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        Formula.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Formula.setWindowIcon(icon)
        Formula.setStyleSheet("QWidget#Formula{background-color: #FFFFFF}")
        self.gridLayout = QtWidgets.QGridLayout(Formula)
        self.gridLayout.setContentsMargins(0, -1, 0, 0)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.actionbar = QtWidgets.QWidget(Formula)
        self.actionbar.setMinimumSize(QtCore.QSize(0, 71))
        self.actionbar.setMaximumSize(QtCore.QSize(16777215, 71))
        self.actionbar.setStyleSheet("QWidget#actionbar { border:1px solid #B2B2B2}")
        self.actionbar.setObjectName("actionbar")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.actionbar)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.titre_favoris = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_favoris.sizePolicy().hasHeightForWidth())
        self.titre_favoris.setSizePolicy(sizePolicy)
        self.titre_favoris.setMinimumSize(QtCore.QSize(0, 16))
        self.titre_favoris.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.titre_favoris.setFont(font)
        self.titre_favoris.setStyleSheet("color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; background: #BAD0E7;")
        self.titre_favoris.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_favoris.setObjectName("titre_favoris")
        self.gridLayout_2.addWidget(self.titre_favoris, 1, 2, 1, 6)
        self.help = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help.sizePolicy().hasHeightForWidth())
        self.help.setSizePolicy(sizePolicy)
        self.help.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.help.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; padding-top: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; padding-top: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.help.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help.setIcon(icon1)
        self.help.setIconSize(QtCore.QSize(24, 24))
        self.help.setShortcut("F1")
        self.help.setFlat(True)
        self.help.setObjectName("help")
        self.gridLayout_2.addWidget(self.help, 0, 8, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 9, 1, 1)
        self.trade = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trade.sizePolicy().hasHeightForWidth())
        self.trade.setSizePolicy(sizePolicy)
        self.trade.setMinimumSize(QtCore.QSize(40, 0))
        self.trade.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.trade.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/formula_trade.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trade.setIcon(icon2)
        self.trade.setIconSize(QtCore.QSize(24, 24))
        self.trade.setFlat(True)
        self.trade.setObjectName("trade")
        self.gridLayout_2.addWidget(self.trade, 0, 7, 1, 1)
        self.attribute_add = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attribute_add.sizePolicy().hasHeightForWidth())
        self.attribute_add.setSizePolicy(sizePolicy)
        self.attribute_add.setMinimumSize(QtCore.QSize(40, 0))
        self.attribute_add.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.attribute_add.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Images/attribute_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.attribute_add.setIcon(icon3)
        self.attribute_add.setIconSize(QtCore.QSize(24, 24))
        self.attribute_add.setFlat(True)
        self.attribute_add.setObjectName("attribute_add")
        self.gridLayout_2.addWidget(self.attribute_add, 0, 2, 1, 1)
        self.titre_r_fin = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_r_fin.sizePolicy().hasHeightForWidth())
        self.titre_r_fin.setSizePolicy(sizePolicy)
        self.titre_r_fin.setStyleSheet("color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; ")
        self.titre_r_fin.setText("")
        self.titre_r_fin.setObjectName("titre_r_fin")
        self.gridLayout_2.addWidget(self.titre_r_fin, 1, 9, 1, 1)
        self.titre_selection = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_selection.sizePolicy().hasHeightForWidth())
        self.titre_selection.setSizePolicy(sizePolicy)
        self.titre_selection.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.titre_selection.setFont(font)
        self.titre_selection.setStyleSheet("color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; ")
        self.titre_selection.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_selection.setObjectName("titre_selection")
        self.gridLayout_2.addWidget(self.titre_selection, 1, 8, 1, 1)
        self.object = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.object.sizePolicy().hasHeightForWidth())
        self.object.setSizePolicy(sizePolicy)
        self.object.setMinimumSize(QtCore.QSize(40, 0))
        self.object.setStatusTip("")
        self.object.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px}\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.object.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Images/formula_object.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.object.setIcon(icon4)
        self.object.setIconSize(QtCore.QSize(24, 24))
        self.object.setFlat(True)
        self.object.setObjectName("object")
        self.gridLayout_2.addWidget(self.object, 0, 6, 1, 1)
        self.function = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.function.sizePolicy().hasHeightForWidth())
        self.function.setSizePolicy(sizePolicy)
        self.function.setMinimumSize(QtCore.QSize(40, 0))
        self.function.setMaximumSize(QtCore.QSize(105, 16777215))
        self.function.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.function.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px}\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.function.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Images/function.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.function.setIcon(icon5)
        self.function.setIconSize(QtCore.QSize(23, 23))
        self.function.setFlat(True)
        self.function.setObjectName("function")
        self.gridLayout_2.addWidget(self.function, 0, 3, 1, 1)
        self.finishing = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finishing.sizePolicy().hasHeightForWidth())
        self.finishing.setSizePolicy(sizePolicy)
        self.finishing.setMinimumSize(QtCore.QSize(40, 0))
        self.finishing.setMaximumSize(QtCore.QSize(105, 16777215))
        self.finishing.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px}\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.finishing.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Images/formula_finish.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.finishing.setIcon(icon6)
        self.finishing.setIconSize(QtCore.QSize(24, 24))
        self.finishing.setFlat(True)
        self.finishing.setObjectName("finishing")
        self.gridLayout_2.addWidget(self.finishing, 0, 5, 1, 1)
        self.operator_bt = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operator_bt.sizePolicy().hasHeightForWidth())
        self.operator_bt.setSizePolicy(sizePolicy)
        self.operator_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.operator_bt.setMaximumSize(QtCore.QSize(105, 16777215))
        self.operator_bt.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.operator_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px}\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px;  padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.operator_bt.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Images/operator.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.operator_bt.setIcon(icon7)
        self.operator_bt.setIconSize(QtCore.QSize(24, 24))
        self.operator_bt.setFlat(True)
        self.operator_bt.setObjectName("operator_bt")
        self.gridLayout_2.addWidget(self.operator_bt, 0, 4, 1, 1)
        self.gridLayout.addWidget(self.actionbar, 0, 1, 1, 1)
        self.formule_convertie = QtWidgets.QTextBrowser(Formula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formule_convertie.sizePolicy().hasHeightForWidth())
        self.formule_convertie.setSizePolicy(sizePolicy)
        self.formule_convertie.setMinimumSize(QtCore.QSize(0, 175))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.formule_convertie.setFont(font)
        self.formule_convertie.setFocusPolicy(QtCore.Qt.NoFocus)
        self.formule_convertie.setStyleSheet("QTextBrowser{border: 1px solid #8f8f91; border-radius: 5px; padding-left: 5px; background-color: #ececec; color: #a0a0a0; }")
        self.formule_convertie.setObjectName("formule_convertie")
        self.gridLayout.addWidget(self.formule_convertie, 2, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.spacer = QtWidgets.QLabel(Formula)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.spacer.setFont(font)
        self.spacer.setStyleSheet("QLabel{border: 1px solid #8f8f91; border-top-width: 0px; border-left-width: 0px; border-bottom-right-radius: 5px; background-color: #FFFFFF; }")
        self.spacer.setText("")
        self.spacer.setAlignment(QtCore.Qt.AlignCenter)
        self.spacer.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.spacer.setObjectName("spacer")
        self.gridLayout_3.addWidget(self.spacer, 5, 1, 1, 3)
        self.bt_verif = BoutonVerif(Formula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_verif.sizePolicy().hasHeightForWidth())
        self.bt_verif.setSizePolicy(sizePolicy)
        self.bt_verif.setMinimumSize(QtCore.QSize(40, 40))
        self.bt_verif.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.bt_verif.setFont(font)
        self.bt_verif.setStyleSheet("QPushButton{border: 0px solid #8f8f91; border-right-width: 1px; padding-bottom: 1px; padding-top: 1px; padding-left: 1px; background-color: #FFFFFF; }\n"
"QPushButton:hover{border-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{border-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Images/valid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_verif.setIcon(icon8)
        self.bt_verif.setIconSize(QtCore.QSize(18, 18))
        self.bt_verif.setFlat(True)
        self.bt_verif.setObjectName("bt_verif")
        self.gridLayout_3.addWidget(self.bt_verif, 3, 2, 1, 1)
        self.bt_formule_couleur = QtWidgets.QPushButton(Formula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_formule_couleur.sizePolicy().hasHeightForWidth())
        self.bt_formule_couleur.setSizePolicy(sizePolicy)
        self.bt_formule_couleur.setMinimumSize(QtCore.QSize(40, 40))
        self.bt_formule_couleur.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.bt_formule_couleur.setFont(font)
        self.bt_formule_couleur.setStyleSheet("QPushButton{border: 0px solid #8f8f91; border-right-width: 1px; padding-bottom: 1px; padding-top: 1px; padding-left: 1px; background-color: #FFFFFF; }\n"
"QPushButton:hover{border-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{border-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/Images/brackets_color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_formule_couleur.setIcon(icon9)
        self.bt_formule_couleur.setIconSize(QtCore.QSize(18, 18))
        self.bt_formule_couleur.setChecked(False)
        self.bt_formule_couleur.setFlat(True)
        self.bt_formule_couleur.setObjectName("bt_formule_couleur")
        self.gridLayout_3.addWidget(self.bt_formule_couleur, 4, 2, 1, 1)
        self.bt_favoris = QtWidgets.QPushButton(Formula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_favoris.sizePolicy().hasHeightForWidth())
        self.bt_favoris.setSizePolicy(sizePolicy)
        self.bt_favoris.setMinimumSize(QtCore.QSize(40, 40))
        self.bt_favoris.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.bt_favoris.setFont(font)
        self.bt_favoris.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.bt_favoris.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-left-width: 0px; padding-left: 1px; ; border-bottom-width: 0px; padding-bottom: 1px; border-top-right-radius: 5px; background-color: #FFFFFF; }\n"
"QPushButton:hover{border-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{border-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/Images/formula_favorite.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_favoris.setIcon(icon10)
        self.bt_favoris.setIconSize(QtCore.QSize(18, 18))
        self.bt_favoris.setFlat(True)
        self.bt_favoris.setObjectName("bt_favoris")
        self.gridLayout_3.addWidget(self.bt_favoris, 2, 2, 1, 1)
        self.valeur_attr = TextFormule(Formula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valeur_attr.sizePolicy().hasHeightForWidth())
        self.valeur_attr.setSizePolicy(sizePolicy)
        self.valeur_attr.setMinimumSize(QtCore.QSize(0, 175))
        self.valeur_attr.setStyleSheet("QPlainTextEdit{border: 1px solid #8f8f91; border-right-width: 0px; padding-left: 5px; padding-right: 5px; padding-top: 1px; padding-bottom: 1px; border-top-left-radius: 5px; border-bottom-left-radius: 5px; background-color: #FFFFFF; }")
        self.valeur_attr.setTabChangesFocus(True)
        self.valeur_attr.setObjectName("valeur_attr")
        self.gridLayout_3.addWidget(self.valeur_attr, 2, 0, 4, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 1, 1, 1)
        self.fond = QtWidgets.QWidget(Formula)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background-color: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.nb_char = QtWidgets.QLabel(self.fond)
        self.nb_char.setMinimumSize(QtCore.QSize(0, 24))
        self.nb_char.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.nb_char.setFont(font)
        self.nb_char.setText("")
        self.nb_char.setObjectName("nb_char")
        self.horizontalLayout_4.addWidget(self.nb_char)
        spacerItem2 = QtWidgets.QSpacerItem(157, 50, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
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
        self.horizontalLayout_4.addWidget(self.ok)
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
        self.horizontalLayout_4.addWidget(self.quit)
        spacerItem3 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.gridLayout.addWidget(self.fond, 3, 0, 1, 3)
        spacerItem4 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 2, 1, 1)

        self.retranslateUi(Formula)
        QtCore.QMetaObject.connectSlotsByName(Formula)
        Formula.setTabOrder(self.attribute_add, self.function)
        Formula.setTabOrder(self.function, self.operator_bt)
        Formula.setTabOrder(self.operator_bt, self.finishing)
        Formula.setTabOrder(self.finishing, self.object)
        Formula.setTabOrder(self.object, self.trade)
        Formula.setTabOrder(self.trade, self.help)
        Formula.setTabOrder(self.help, self.valeur_attr)
        Formula.setTabOrder(self.valeur_attr, self.bt_favoris)
        Formula.setTabOrder(self.bt_favoris, self.bt_verif)
        Formula.setTabOrder(self.bt_verif, self.bt_formule_couleur)
        Formula.setTabOrder(self.bt_formule_couleur, self.ok)
        Formula.setTabOrder(self.ok, self.quit)

    def retranslateUi(self, Formula):
        _translate = QtCore.QCoreApplication.translate
        Formula.setWindowTitle(_translate("Formula", "Créer votre formule"))
        self.titre_favoris.setText(_translate("Formula", "Ajouter"))
        self.help.setToolTip(_translate("Formula", "Afficher Aide"))
        self.trade.setToolTip(_translate("Formula", "Métier"))
        self.attribute_add.setToolTip(_translate("Formula", "Ajouter attribut"))
        self.titre_selection.setText(_translate("Formula", "Aide"))
        self.object.setToolTip(_translate("Formula", "Objet"))
        self.function.setToolTip(_translate("Formula", "Fonctions"))
        self.finishing.setToolTip(_translate("Formula", "Second-Œuvre"))
        self.operator_bt.setToolTip(_translate("Formula", "Fonctions"))
        self.bt_formule_couleur.setToolTip(_translate("Formula", "Coloriser les couples de parenthèses"))
        self.bt_favoris.setToolTip(_translate("Formula", "Ouvrir les favoris"))
        self.ok.setText(_translate("Formula", "Valider"))
        self.quit.setText(_translate("Formula", "Quitter"))
from formula_manage import BoutonVerif, TextFormule
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Formula = QtWidgets.QWidget()
    ui = Ui_Formula()
    ui.setupUi(Formula)
    Formula.show()
    sys.exit(app.exec_())