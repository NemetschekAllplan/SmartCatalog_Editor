# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_room.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Room(object):
    def setupUi(self, Room):
        Room.setObjectName("Room")
        Room.setWindowModality(QtCore.Qt.ApplicationModal)
        Room.resize(600, 850)
        Room.setMinimumSize(QtCore.QSize(600, 850))
        Room.setMaximumSize(QtCore.QSize(600, 850))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/room.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Room.setWindowIcon(icon)
        Room.setStyleSheet("QWidget#Room {background:#FFFFFF}")
        self.gridLayout_3 = QtWidgets.QGridLayout(Room)
        self.gridLayout_3.setContentsMargins(0, -1, 0, 0)
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 3, 1, 1)
        self.fond = QtWidgets.QWidget(Room)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.bt_enregistrer = QtWidgets.QPushButton(self.fond)
        self.bt_enregistrer.setMinimumSize(QtCore.QSize(120, 24))
        self.bt_enregistrer.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_enregistrer.setFont(font)
        self.bt_enregistrer.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.bt_enregistrer.setIconSize(QtCore.QSize(18, 18))
        self.bt_enregistrer.setObjectName("bt_enregistrer")
        self.horizontalLayout_2.addWidget(self.bt_enregistrer)
        self.bt_quitter = QtWidgets.QPushButton(self.fond)
        self.bt_quitter.setMinimumSize(QtCore.QSize(120, 24))
        self.bt_quitter.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_quitter.setFont(font)
        self.bt_quitter.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.bt_quitter.setIconSize(QtCore.QSize(18, 18))
        self.bt_quitter.setObjectName("bt_quitter")
        self.horizontalLayout_2.addWidget(self.bt_quitter)
        self.gridLayout_3.addWidget(self.fond, 3, 0, 1, 4)
        self.sh = QtWidgets.QGroupBox(Room)
        self.sh.setMinimumSize(QtCore.QSize(0, 100))
        self.sh.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.sh.setFont(font)
        self.sh.setStyleSheet("QGroupBox {border: 1px solid silver; margin: 15px 0px 5px 0; }  \n"
"QGroupBox::title {subcontrol-origin: margin; left: 7px; padding: 7px 0px 10px 0px; }")
        self.sh.setObjectName("sh")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.sh)
        self.gridLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bt_233 = QtWidgets.QPushButton(self.sh)
        self.bt_233.setMinimumSize(QtCore.QSize(120, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_233.setFont(font)
        self.bt_233.setStyleSheet("QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(227, 236, 246, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(227, 236, 246, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}")
        self.bt_233.setObjectName("bt_233")
        self.gridLayout_2.addWidget(self.bt_233, 0, 2, 1, 1)
        self.titre_233 = QtWidgets.QLabel(self.sh)
        self.titre_233.setMinimumSize(QtCore.QSize(250, 24))
        self.titre_233.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.titre_233.setFont(font)
        self.titre_233.setObjectName("titre_233")
        self.gridLayout_2.addWidget(self.titre_233, 0, 0, 1, 1)
        self.valeur_233 = QtWidgets.QComboBox(self.sh)
        self.valeur_233.setMinimumSize(QtCore.QSize(0, 24))
        self.valeur_233.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.valeur_233.setFont(font)
        self.valeur_233.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.valeur_233.setEditable(True)
        self.valeur_233.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.valeur_233.setObjectName("valeur_233")
        self.gridLayout_2.addWidget(self.valeur_233, 0, 1, 1, 1)
        self.titre_264 = QtWidgets.QLabel(self.sh)
        self.titre_264.setMinimumSize(QtCore.QSize(250, 24))
        self.titre_264.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.titre_264.setFont(font)
        self.titre_264.setObjectName("titre_264")
        self.gridLayout_2.addWidget(self.titre_264, 1, 0, 1, 1)
        self.valeur_264 = QtWidgets.QLineEdit(self.sh)
        self.valeur_264.setMinimumSize(QtCore.QSize(0, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.valeur_264.setFont(font)
        self.valeur_264.setObjectName("valeur_264")
        self.gridLayout_2.addWidget(self.valeur_264, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.sh, 1, 1, 1, 2)
        self.din277 = QtWidgets.QGroupBox(Room)
        self.din277.setMinimumSize(QtCore.QSize(0, 163))
        self.din277.setMaximumSize(QtCore.QSize(16777215, 163))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.din277.setFont(font)
        self.din277.setStyleSheet("QGroupBox {border: 1px solid silver; margin: 15px 0px 5px 0; }  \n"
"QGroupBox::title {subcontrol-origin: margin; left: 7px; padding: 7px 0px 10px 0px; }")
        self.din277.setObjectName("din277")
        self.gridLayout = QtWidgets.QGridLayout(self.din277)
        self.gridLayout.setContentsMargins(-1, 15, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.valeur_266 = QtWidgets.QLineEdit(self.din277)
        self.valeur_266.setMinimumSize(QtCore.QSize(0, 24))
        self.valeur_266.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.valeur_266.setFont(font)
        self.valeur_266.setObjectName("valeur_266")
        self.gridLayout.addWidget(self.valeur_266, 3, 1, 1, 1)
        self.valeur_235 = QtWidgets.QComboBox(self.din277)
        self.valeur_235.setMinimumSize(QtCore.QSize(0, 24))
        self.valeur_235.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.valeur_235.setFont(font)
        self.valeur_235.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.valeur_235.setEditable(True)
        self.valeur_235.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.valeur_235.setObjectName("valeur_235")
        self.gridLayout.addWidget(self.valeur_235, 1, 1, 1, 1)
        self.valeur_231 = QtWidgets.QComboBox(self.din277)
        self.valeur_231.setMinimumSize(QtCore.QSize(0, 24))
        self.valeur_231.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.valeur_231.setFont(font)
        self.valeur_231.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.valeur_231.setEditable(True)
        self.valeur_231.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.valeur_231.setObjectName("valeur_231")
        self.gridLayout.addWidget(self.valeur_231, 0, 1, 1, 1)
        self.titre_235 = QtWidgets.QLabel(self.din277)
        self.titre_235.setMinimumSize(QtCore.QSize(250, 0))
        self.titre_235.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.titre_235.setFont(font)
        self.titre_235.setObjectName("titre_235")
        self.gridLayout.addWidget(self.titre_235, 1, 0, 1, 1)
        self.bt_231 = QtWidgets.QPushButton(self.din277)
        self.bt_231.setMinimumSize(QtCore.QSize(120, 24))
        self.bt_231.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_231.setFont(font)
        self.bt_231.setStyleSheet("QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(227, 236, 246, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(227, 236, 246, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}")
        self.bt_231.setObjectName("bt_231")
        self.gridLayout.addWidget(self.bt_231, 0, 2, 1, 1)
        self.bt_235 = QtWidgets.QPushButton(self.din277)
        self.bt_235.setMinimumSize(QtCore.QSize(120, 24))
        self.bt_235.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_235.setFont(font)
        self.bt_235.setStyleSheet("QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(227, 236, 246, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(227, 236, 246, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}")
        self.bt_235.setObjectName("bt_235")
        self.gridLayout.addWidget(self.bt_235, 1, 2, 1, 1)
        self.titre_232 = QtWidgets.QLabel(self.din277)
        self.titre_232.setMinimumSize(QtCore.QSize(250, 24))
        self.titre_232.setMaximumSize(QtCore.QSize(250, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.titre_232.setFont(font)
        self.titre_232.setObjectName("titre_232")
        self.gridLayout.addWidget(self.titre_232, 2, 0, 1, 1)
        self.bt_232 = QtWidgets.QPushButton(self.din277)
        self.bt_232.setMinimumSize(QtCore.QSize(120, 24))
        self.bt_232.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.bt_232.setFont(font)
        self.bt_232.setStyleSheet("QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(227, 236, 246, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(227, 236, 246, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}")
        self.bt_232.setObjectName("bt_232")
        self.gridLayout.addWidget(self.bt_232, 2, 2, 1, 1)
        self.titre_266 = QtWidgets.QLabel(self.din277)
        self.titre_266.setMinimumSize(QtCore.QSize(250, 24))
        self.titre_266.setMaximumSize(QtCore.QSize(250, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.titre_266.setFont(font)
        self.titre_266.setObjectName("titre_266")
        self.gridLayout.addWidget(self.titre_266, 3, 0, 1, 1)
        self.valeur_232 = QtWidgets.QComboBox(self.din277)
        self.valeur_232.setMinimumSize(QtCore.QSize(0, 24))
        self.valeur_232.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.valeur_232.setFont(font)
        self.valeur_232.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.valeur_232.setEditable(True)
        self.valeur_232.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.valeur_232.setObjectName("valeur_232")
        self.gridLayout.addWidget(self.valeur_232, 2, 1, 1, 1)
        self.titre_231 = QtWidgets.QLabel(self.din277)
        self.titre_231.setMinimumSize(QtCore.QSize(250, 24))
        self.titre_231.setMaximumSize(QtCore.QSize(250, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.titre_231.setFont(font)
        self.titre_231.setObjectName("titre_231")
        self.gridLayout.addWidget(self.titre_231, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.din277, 0, 1, 1, 2)
        self.selection = QtWidgets.QGroupBox(Room)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.selection.setFont(font)
        self.selection.setStyleSheet("QGroupBox {background-image: url(:/Images/room_schema.png) ;border: 1px solid silver; margin: 15px 0px 5px 0; }  \n"
"QGroupBox::title {subcontrol-origin: margin; left: 7px; padding: 7px 0px 10px 0px; }")
        self.selection.setObjectName("selection")
        self.bt_hall = QtWidgets.QPushButton(self.selection)
        self.bt_hall.setGeometry(QtCore.QRect(380, 350, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_hall.setFont(font)
        self.bt_hall.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_hall.setFlat(True)
        self.bt_hall.setObjectName("bt_hall")
        self.bt_aeration = QtWidgets.QPushButton(self.selection)
        self.bt_aeration.setGeometry(QtCore.QRect(380, 430, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bt_aeration.setFont(font)
        self.bt_aeration.setStyleSheet("QPushButton:pressed { border: none }")
        self.bt_aeration.setFlat(True)
        self.bt_aeration.setObjectName("bt_aeration")
        self.bt_balcon_2 = QtWidgets.QPushButton(self.selection)
        self.bt_balcon_2.setGeometry(QtCore.QRect(40, 270, 91, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_balcon_2.setFont(font)
        self.bt_balcon_2.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_balcon_2.setFlat(True)
        self.bt_balcon_2.setObjectName("bt_balcon_2")
        self.bt_couloir = QtWidgets.QPushButton(self.selection)
        self.bt_couloir.setGeometry(QtCore.QRect(130, 350, 241, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_couloir.setFont(font)
        self.bt_couloir.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_couloir.setFlat(True)
        self.bt_couloir.setObjectName("bt_couloir")
        self.bt_sejour = QtWidgets.QPushButton(self.selection)
        self.bt_sejour.setGeometry(QtCore.QRect(130, 190, 241, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_sejour.setFont(font)
        self.bt_sejour.setAutoFillBackground(False)
        self.bt_sejour.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_sejour.setFlat(True)
        self.bt_sejour.setObjectName("bt_sejour")
        self.bt_bain = QtWidgets.QPushButton(self.selection)
        self.bt_bain.setGeometry(QtCore.QRect(170, 100, 91, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_bain.setFont(font)
        self.bt_bain.setStyleSheet("QPushButton {padding-top: 41px; padding-right: 10px; text-align: right }\n"
"QPushButton:pressed { border: none; padding-right: 11px }")
        self.bt_bain.setText("")
        self.bt_bain.setFlat(True)
        self.bt_bain.setObjectName("bt_bain")
        self.bt_debarras = QtWidgets.QPushButton(self.selection)
        self.bt_debarras.setGeometry(QtCore.QRect(270, 80, 101, 101))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_debarras.setFont(font)
        self.bt_debarras.setStyleSheet("QPushButton {padding-top: 61px; }\n"
"QPushButton:pressed { border: none; }")
        self.bt_debarras.setText("")
        self.bt_debarras.setFlat(True)
        self.bt_debarras.setObjectName("bt_debarras")
        self.bt_cour = QtWidgets.QPushButton(self.selection)
        self.bt_cour.setGeometry(QtCore.QRect(490, 430, 81, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bt_cour.setFont(font)
        self.bt_cour.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_cour.setFlat(True)
        self.bt_cour.setObjectName("bt_cour")
        self.bt_comble = QtWidgets.QPushButton(self.selection)
        self.bt_comble.setGeometry(QtCore.QRect(380, 100, 91, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_comble.setFont(font)
        self.bt_comble.setStyleSheet("QPushButton {padding-top: 41px; padding-left: 3px; text-align: left }\n"
"QPushButton:pressed { border: none; padding-left: 4px }")
        self.bt_comble.setText("")
        self.bt_comble.setFlat(True)
        self.bt_comble.setObjectName("bt_comble")
        self.bt_balcon_1 = QtWidgets.QPushButton(self.selection)
        self.bt_balcon_1.setGeometry(QtCore.QRect(40, 190, 91, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_balcon_1.setFont(font)
        self.bt_balcon_1.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_balcon_1.setFlat(True)
        self.bt_balcon_1.setObjectName("bt_balcon_1")
        self.bt_loggias = QtWidgets.QPushButton(self.selection)
        self.bt_loggias.setGeometry(QtCore.QRect(380, 190, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_loggias.setFont(font)
        self.bt_loggias.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_loggias.setFlat(True)
        self.bt_loggias.setObjectName("bt_loggias")
        self.bt_chauffage = QtWidgets.QPushButton(self.selection)
        self.bt_chauffage.setGeometry(QtCore.QRect(130, 430, 241, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_chauffage.setFont(font)
        self.bt_chauffage.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_chauffage.setFlat(True)
        self.bt_chauffage.setObjectName("bt_chauffage")
        self.bt_escalier = QtWidgets.QPushButton(self.selection)
        self.bt_escalier.setGeometry(QtCore.QRect(40, 430, 91, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_escalier.setFont(font)
        self.bt_escalier.setStyleSheet("QPushButton {padding-top: 21px; }\n"
"QPushButton:pressed { border: none; }")
        self.bt_escalier.setText("")
        self.bt_escalier.setFlat(True)
        self.bt_escalier.setObjectName("bt_escalier")
        self.bt_bureau = QtWidgets.QPushButton(self.selection)
        self.bt_bureau.setGeometry(QtCore.QRect(130, 270, 241, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_bureau.setFont(font)
        self.bt_bureau.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_bureau.setFlat(True)
        self.bt_bureau.setObjectName("bt_bureau")
        self.bt_air_frais = QtWidgets.QPushButton(self.selection)
        self.bt_air_frais.setGeometry(QtCore.QRect(380, 270, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.bt_air_frais.setFont(font)
        self.bt_air_frais.setStyleSheet("QPushButton:pressed { border: none; }")
        self.bt_air_frais.setFlat(True)
        self.bt_air_frais.setObjectName("bt_air_frais")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.selection)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 231, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.favoris_layer = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.favoris_layer.setContentsMargins(0, 0, 0, 0)
        self.favoris_layer.setObjectName("favoris_layer")
        self.valeur_fav = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.valeur_fav.setMinimumSize(QtCore.QSize(0, 30))
        self.valeur_fav.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.valeur_fav.setFont(font)
        self.valeur_fav.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.valeur_fav.setEditable(True)
        self.valeur_fav.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.valeur_fav.setObjectName("valeur_fav")
        self.favoris_layer.addWidget(self.valeur_fav)
        self.bt_renommer = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.bt_renommer.setMinimumSize(QtCore.QSize(30, 30))
        self.bt_renommer.setMaximumSize(QtCore.QSize(30, 30))
        self.bt_renommer.setStyleSheet("QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(227, 236, 246, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(227, 236, 246, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}")
        self.bt_renommer.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/rename.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_renommer.setIcon(icon1)
        self.bt_renommer.setIconSize(QtCore.QSize(18, 18))
        self.bt_renommer.setObjectName("bt_renommer")
        self.favoris_layer.addWidget(self.bt_renommer)
        self.bt_ajouter = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.bt_ajouter.setMinimumSize(QtCore.QSize(30, 30))
        self.bt_ajouter.setMaximumSize(QtCore.QSize(30, 30))
        self.bt_ajouter.setStyleSheet("QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(227, 236, 246, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(227, 236, 246, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}")
        self.bt_ajouter.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_ajouter.setIcon(icon2)
        self.bt_ajouter.setIconSize(QtCore.QSize(18, 18))
        self.bt_ajouter.setObjectName("bt_ajouter")
        self.favoris_layer.addWidget(self.bt_ajouter)
        self.bt_supprimer = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.bt_supprimer.setMinimumSize(QtCore.QSize(30, 30))
        self.bt_supprimer.setMaximumSize(QtCore.QSize(30, 30))
        self.bt_supprimer.setStyleSheet("QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(227, 236, 246, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(227, 236, 246, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid rgb(192, 192, 192)\n"
"}")
        self.bt_supprimer.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Images/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_supprimer.setIcon(icon3)
        self.bt_supprimer.setIconSize(QtCore.QSize(18, 18))
        self.bt_supprimer.setObjectName("bt_supprimer")
        self.favoris_layer.addWidget(self.bt_supprimer)
        self.gridLayout_3.addWidget(self.selection, 2, 1, 1, 2)

        self.retranslateUi(Room)
        QtCore.QMetaObject.connectSlotsByName(Room)
        Room.setTabOrder(self.valeur_231, self.bt_231)
        Room.setTabOrder(self.bt_231, self.valeur_235)
        Room.setTabOrder(self.valeur_235, self.bt_235)
        Room.setTabOrder(self.bt_235, self.valeur_232)
        Room.setTabOrder(self.valeur_232, self.bt_232)
        Room.setTabOrder(self.bt_232, self.valeur_266)
        Room.setTabOrder(self.valeur_266, self.valeur_233)
        Room.setTabOrder(self.valeur_233, self.bt_233)
        Room.setTabOrder(self.bt_233, self.valeur_264)
        Room.setTabOrder(self.valeur_264, self.valeur_fav)
        Room.setTabOrder(self.valeur_fav, self.bt_renommer)
        Room.setTabOrder(self.bt_renommer, self.bt_ajouter)
        Room.setTabOrder(self.bt_ajouter, self.bt_supprimer)
        Room.setTabOrder(self.bt_supprimer, self.bt_bain)
        Room.setTabOrder(self.bt_bain, self.bt_debarras)
        Room.setTabOrder(self.bt_debarras, self.bt_comble)
        Room.setTabOrder(self.bt_comble, self.bt_balcon_1)
        Room.setTabOrder(self.bt_balcon_1, self.bt_sejour)
        Room.setTabOrder(self.bt_sejour, self.bt_loggias)
        Room.setTabOrder(self.bt_loggias, self.bt_balcon_2)
        Room.setTabOrder(self.bt_balcon_2, self.bt_bureau)
        Room.setTabOrder(self.bt_bureau, self.bt_air_frais)
        Room.setTabOrder(self.bt_air_frais, self.bt_couloir)
        Room.setTabOrder(self.bt_couloir, self.bt_hall)
        Room.setTabOrder(self.bt_hall, self.bt_escalier)
        Room.setTabOrder(self.bt_escalier, self.bt_chauffage)
        Room.setTabOrder(self.bt_chauffage, self.bt_aeration)
        Room.setTabOrder(self.bt_aeration, self.bt_cour)

    def retranslateUi(self, Room):
        _translate = QtCore.QCoreApplication.translate
        Room.setWindowTitle(_translate("Room", "Pièce"))
        self.bt_enregistrer.setText(_translate("Room", " Enregistrer"))
        self.bt_quitter.setText(_translate("Room", " Annuler"))
        self.sh.setTitle(_translate("Room", "Attributs surface habitable"))
        self.bt_233.setText(_translate("Room", "Type de surface ..."))
        self.titre_233.setToolTip(_translate("Room", "Attribut 233"))
        self.titre_233.setText(_translate("Room", "Type de surface de base"))
        self.titre_264.setToolTip(_translate("Room", "attribut 264"))
        self.titre_264.setText(_translate("Room", "Facteur pour calcul de la surface habitable"))
        self.din277.setTitle(_translate("Room", "Attribut DIN277"))
        self.titre_235.setToolTip(_translate("Room", "Attribut 235"))
        self.titre_235.setText(_translate("Room", "Utilisation"))
        self.bt_231.setText(_translate("Room", "Pourtour ..."))
        self.bt_235.setText(_translate("Room", "Utilisation ..."))
        self.titre_232.setToolTip(_translate("Room", "Attribut 232"))
        self.titre_232.setText(_translate("Room", "Type de surface Din277"))
        self.bt_232.setText(_translate("Room", "Type de surface ..."))
        self.titre_266.setToolTip(_translate("Room", "Attribut 266"))
        self.titre_266.setText(_translate("Room", "Facteur DIN277"))
        self.titre_231.setToolTip(_translate("Room", "Attribut 231"))
        self.titre_231.setText(_translate("Room", "Pourtour de la salle"))
        self.selection.setTitle(_translate("Room", "Sélection rapide attributs"))
        self.valeur_fav.setToolTip(_translate("Room", "Liste de vos favoris"))
        self.bt_renommer.setToolTip(_translate("Room", "Renommer ce favori"))
        self.bt_ajouter.setToolTip(_translate("Room", "Ajouter ou mettre à jour un favoris avec la configuration actuelle"))
        self.bt_supprimer.setToolTip(_translate("Room", "Supprimer ce favoris"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Room = QtWidgets.QWidget()
    ui = Ui_Room()
    ui.setupUi(Room)
    Room.show()
    sys.exit(app.exec_())
