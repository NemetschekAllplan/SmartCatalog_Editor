# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_formula_favorite_modify.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormulaFavoriteModify(object):
    def setupUi(self, FormulaFavoriteModify):
        FormulaFavoriteModify.setObjectName("FormulaFavoriteModify")
        FormulaFavoriteModify.resize(350, 79)
        FormulaFavoriteModify.setWindowTitle("Form")
        FormulaFavoriteModify.setStyleSheet("QWidget#FormulaFavoriteModify {background-color: #F8F8F8; }")
        self.verticalLayout = QtWidgets.QVBoxLayout(FormulaFavoriteModify)
        self.verticalLayout.setContentsMargins(-1, 6, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.icone = QtWidgets.QPushButton(FormulaFavoriteModify)
        self.icone.setEnabled(True)
        self.icone.setMinimumSize(QtCore.QSize(30, 30))
        self.icone.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.icone.setFont(font)
        self.icone.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.icone.setText("")
        self.icone.setIconSize(QtCore.QSize(18, 18))
        self.icone.setObjectName("icone")
        self.horizontalLayout_2.addWidget(self.icone)
        self.icone_clear = QtWidgets.QPushButton(FormulaFavoriteModify)
        self.icone_clear.setMinimumSize(QtCore.QSize(30, 30))
        self.icone_clear.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.icone_clear.setFont(font)
        self.icone_clear.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.icone_clear.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/none.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icone_clear.setIcon(icon)
        self.icone_clear.setIconSize(QtCore.QSize(18, 18))
        self.icone_clear.setObjectName("icone_clear")
        self.horizontalLayout_2.addWidget(self.icone_clear)
        self.onglet_texte = QtWidgets.QLineEdit(FormulaFavoriteModify)
        self.onglet_texte.setMinimumSize(QtCore.QSize(0, 30))
        self.onglet_texte.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.onglet_texte.setFont(font)
        self.onglet_texte.setStyleSheet("QLineEdit{padding-left: 5px; border: 1px solid #8f8f91; border-radius:5px; }")
        self.onglet_texte.setAlignment(QtCore.Qt.AlignCenter)
        self.onglet_texte.setObjectName("onglet_texte")
        self.horizontalLayout_2.addWidget(self.onglet_texte)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.bt_enregistrer = QtWidgets.QPushButton(FormulaFavoriteModify)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_enregistrer.sizePolicy().hasHeightForWidth())
        self.bt_enregistrer.setSizePolicy(sizePolicy)
        self.bt_enregistrer.setMinimumSize(QtCore.QSize(100, 0))
        self.bt_enregistrer.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_enregistrer.setFont(font)
        self.bt_enregistrer.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.bt_enregistrer.setObjectName("bt_enregistrer")
        self.horizontalLayout_3.addWidget(self.bt_enregistrer)
        self.bt_quitter = QtWidgets.QPushButton(FormulaFavoriteModify)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_quitter.sizePolicy().hasHeightForWidth())
        self.bt_quitter.setSizePolicy(sizePolicy)
        self.bt_quitter.setMinimumSize(QtCore.QSize(100, 24))
        self.bt_quitter.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_quitter.setFont(font)
        self.bt_quitter.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.bt_quitter.setObjectName("bt_quitter")
        self.horizontalLayout_3.addWidget(self.bt_quitter)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(FormulaFavoriteModify)
        QtCore.QMetaObject.connectSlotsByName(FormulaFavoriteModify)
        FormulaFavoriteModify.setTabOrder(self.icone, self.icone_clear)
        FormulaFavoriteModify.setTabOrder(self.icone_clear, self.onglet_texte)
        FormulaFavoriteModify.setTabOrder(self.onglet_texte, self.bt_enregistrer)
        FormulaFavoriteModify.setTabOrder(self.bt_enregistrer, self.bt_quitter)

    def retranslateUi(self, FormulaFavoriteModify):
        _translate = QtCore.QCoreApplication.translate
        self.icone.setToolTip(_translate("FormulaFavoriteModify", "Choisir un icone"))
        self.icone_clear.setToolTip(_translate("FormulaFavoriteModify", "Supprimer l\'icône"))
        self.bt_enregistrer.setText(_translate("FormulaFavoriteModify", "Enregistrer"))
        self.bt_quitter.setText(_translate("FormulaFavoriteModify", "Annuler"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormulaFavoriteModify = QtWidgets.QWidget()
    ui = Ui_FormulaFavoriteModify()
    ui.setupUi(FormulaFavoriteModify)
    FormulaFavoriteModify.show()
    sys.exit(app.exec_())