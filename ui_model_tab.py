# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_model_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ModelTab(object):
    def setupUi(self, ModelTab):
        ModelTab.setObjectName("ModelTab")
        ModelTab.resize(800, 396)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        ModelTab.setPalette(palette)
        ModelTab.setAcceptDrops(True)
        ModelTab.setStyleSheet("QWidget#ModelTab{background-color: #FFFFFF; }")
        self.gridLayout = QtWidgets.QGridLayout(ModelTab)
        self.gridLayout.setContentsMargins(15, 15, 15, 0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.liste_items = QtWidgets.QTableView(ModelTab)
        self.liste_items.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.liste_items.setStyleSheet("QHeaderView {background-color: #d8e9e8}")
        self.liste_items.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.liste_items.setAlternatingRowColors(True)
        self.liste_items.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.liste_items.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.liste_items.setSortingEnabled(True)
        self.liste_items.setObjectName("liste_items")
        self.liste_items.horizontalHeader().setStretchLastSection(True)
        self.liste_items.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.liste_items, 1, 0, 1, 4)
        self.actionbar = QtWidgets.QWidget(ModelTab)
        self.actionbar.setMinimumSize(QtCore.QSize(0, 71))
        self.actionbar.setMaximumSize(QtCore.QSize(16777215, 71))
        self.actionbar.setStyleSheet("QWidget#actionbar { border:1px solid #B2B2B2}")
        self.actionbar.setObjectName("actionbar")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.actionbar)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bt_attributs = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_attributs.sizePolicy().hasHeightForWidth())
        self.bt_attributs.setSizePolicy(sizePolicy)
        self.bt_attributs.setMinimumSize(QtCore.QSize(40, 0))
        self.bt_attributs.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.bt_attributs.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/attribute_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_attributs.setIcon(icon)
        self.bt_attributs.setIconSize(QtCore.QSize(24, 24))
        self.bt_attributs.setFlat(True)
        self.bt_attributs.setObjectName("bt_attributs")
        self.gridLayout_2.addWidget(self.bt_attributs, 0, 2, 1, 1)
        self.bt_supprimer = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_supprimer.sizePolicy().hasHeightForWidth())
        self.bt_supprimer.setSizePolicy(sizePolicy)
        self.bt_supprimer.setMinimumSize(QtCore.QSize(40, 0))
        self.bt_supprimer.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px;  border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px;  border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.bt_supprimer.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_supprimer.setIcon(icon1)
        self.bt_supprimer.setIconSize(QtCore.QSize(24, 24))
        self.bt_supprimer.setShortcut("Del")
        self.bt_supprimer.setFlat(True)
        self.bt_supprimer.setObjectName("bt_supprimer")
        self.gridLayout_2.addWidget(self.bt_supprimer, 0, 3, 1, 1)
        self.copy_bt = QtWidgets.QPushButton(self.actionbar)
        self.copy_bt.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_bt.sizePolicy().hasHeightForWidth())
        self.copy_bt.setSizePolicy(sizePolicy)
        self.copy_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.copy_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px;  border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px;  border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/copy.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy_bt.setIcon(icon2)
        self.copy_bt.setIconSize(QtCore.QSize(24, 24))
        self.copy_bt.setShortcut("Ctrl+C")
        self.copy_bt.setFlat(True)
        self.copy_bt.setObjectName("copy_bt")
        self.gridLayout_2.addWidget(self.copy_bt, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(6, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 8, 1, 1)
        self.titre_import = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_import.sizePolicy().hasHeightForWidth())
        self.titre_import.setSizePolicy(sizePolicy)
        self.titre_import.setMinimumSize(QtCore.QSize(0, 16))
        self.titre_import.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.titre_import.setFont(font)
        self.titre_import.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.titre_import.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_import.setObjectName("titre_import")
        self.gridLayout_2.addWidget(self.titre_import, 1, 6, 1, 2)
        self.bt_importer = QtWidgets.QPushButton(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_importer.sizePolicy().hasHeightForWidth())
        self.bt_importer.setSizePolicy(sizePolicy)
        self.bt_importer.setMinimumSize(QtCore.QSize(40, 0))
        self.bt_importer.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; padding-top: 1px; padding-right: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-right-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.bt_importer.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Images/favorite_open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_importer.setIcon(icon3)
        self.bt_importer.setIconSize(QtCore.QSize(22, 22))
        self.bt_importer.setFlat(True)
        self.bt_importer.setObjectName("bt_importer")
        self.gridLayout_2.addWidget(self.bt_importer, 0, 6, 1, 1)
        self.bt_exporter = QtWidgets.QPushButton(self.actionbar)
        self.bt_exporter.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_exporter.sizePolicy().hasHeightForWidth())
        self.bt_exporter.setSizePolicy(sizePolicy)
        self.bt_exporter.setMinimumSize(QtCore.QSize(40, 0))
        self.bt_exporter.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        self.bt_exporter.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Images/favorite_save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_exporter.setIcon(icon4)
        self.bt_exporter.setIconSize(QtCore.QSize(24, 24))
        self.bt_exporter.setFlat(True)
        self.bt_exporter.setObjectName("bt_exporter")
        self.gridLayout_2.addWidget(self.bt_exporter, 0, 7, 1, 1)
        self.paste_bt = QtWidgets.QPushButton(self.actionbar)
        self.paste_bt.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paste_bt.sizePolicy().hasHeightForWidth())
        self.paste_bt.setSizePolicy(sizePolicy)
        self.paste_bt.setMinimumSize(QtCore.QSize(40, 0))
        self.paste_bt.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.paste_bt.setStyleSheet("QPushButton{border: 0px solid #B2B2B2; border-right-width: 1px; padding-top: 1px; padding-left: 1px; }\n"
"QPushButton:hover{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }\n"
"QPushButton:pressed{border-top-width: 1px; border-left-width: 1px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Images/paste.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.paste_bt.setIcon(icon5)
        self.paste_bt.setIconSize(QtCore.QSize(24, 24))
        self.paste_bt.setShortcut("Ctrl+V")
        self.paste_bt.setFlat(True)
        self.paste_bt.setObjectName("paste_bt")
        self.gridLayout_2.addWidget(self.paste_bt, 0, 5, 1, 1)
        self.titre_edition = QtWidgets.QLabel(self.actionbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_edition.sizePolicy().hasHeightForWidth())
        self.titre_edition.setSizePolicy(sizePolicy)
        self.titre_edition.setMinimumSize(QtCore.QSize(0, 16))
        self.titre_edition.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.titre_edition.setFont(font)
        self.titre_edition.setStyleSheet("QLabel{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.titre_edition.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_edition.setObjectName("titre_edition")
        self.gridLayout_2.addWidget(self.titre_edition, 1, 2, 1, 4)
        self.end_title = QtWidgets.QWidget(self.actionbar)
        self.end_title.setStyleSheet("QWidget#end_title{color: #4D4D4D; border:1px solid #B2B2B2; border-top: 0px; border-left: 0px; background: #BAD0E7; padding-left: 5px; padding-right: 5px; }")
        self.end_title.setObjectName("end_title")
        self.gridLayout_2.addWidget(self.end_title, 1, 8, 1, 1)
        self.gridLayout.addWidget(self.actionbar, 0, 0, 1, 4)

        self.retranslateUi(ModelTab)
        QtCore.QMetaObject.connectSlotsByName(ModelTab)
        ModelTab.setTabOrder(self.liste_items, self.bt_attributs)
        ModelTab.setTabOrder(self.bt_attributs, self.bt_supprimer)
        ModelTab.setTabOrder(self.bt_supprimer, self.copy_bt)
        ModelTab.setTabOrder(self.copy_bt, self.paste_bt)
        ModelTab.setTabOrder(self.paste_bt, self.bt_importer)
        ModelTab.setTabOrder(self.bt_importer, self.bt_exporter)

    def retranslateUi(self, ModelTab):
        _translate = QtCore.QCoreApplication.translate
        self.bt_attributs.setToolTip(_translate("ModelTab", "Ajouter attribut"))
        self.bt_supprimer.setToolTip(_translate("ModelTab", "Supprimer attribut"))
        self.copy_bt.setToolTip(_translate("ModelTab", "Copier (CTRL + C)"))
        self.titre_import.setText(_translate("ModelTab", "Favoris"))
        self.bt_importer.setToolTip(_translate("ModelTab", "Charger favoris"))
        self.bt_exporter.setToolTip(_translate("ModelTab", "Enregistrer favoris"))
        self.paste_bt.setToolTip(_translate("ModelTab", "Coller (CTRL+ V)"))
        self.titre_edition.setText(_translate("ModelTab", "Édition"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ModelTab = QtWidgets.QWidget()
    ui = Ui_ModelTab()
    ui.setupUi(ModelTab)
    ModelTab.show()
    sys.exit(app.exec_())
