#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from main_datas import get_icon
from main_datas import paste_icon
from ui_message_children import Ui_MessageChildren
from ui_message_existing import Ui_MessageExisting
from ui_message_location import Ui_MessageLocation


class LoadingSplash(QSplashScreen):

    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.setObjectName("loading")
        self.resize(400, 74)

        self.setStyleSheet("QWidget#loading {border: 1px solid #8f8f91; background-color: #FFFFFF; }")

        layout = QVBoxLayout(self)

        self.titre = QLabel()
        font = self.titre.font()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        self.titre.setFont(font)
        self.titre.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.titre)

        progress = QProgressBar()
        progress.setStyleSheet("QProgressBar{border: 1px solid #8f8f91; border-radius:5px;}")

        progress.setMaximum(0)
        progress.setMinimum(0)

        layout.addWidget(progress)

    def launch_show(self, titre: str):
        self.titre.setText(titre)

        self.show()
        self.showMessage("")
        self.setFocus()

    @staticmethod
    def a___________________end______():
        pass


class MessageExisting(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MessageExisting()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.ui.update.clicked.connect(self.update_clicked)
        self.ui.replace.clicked.connect(self.replace_clicked)
        self.ui.duplicate.clicked.connect(self.duplicate_clicked)
        self.ui.quit.clicked.connect(self.quit_clicked)

        txt1 = self.tr("l'élément et ses enfants")
        txt2 = self.tr("Les enfants et les attributs non présents dans le presse-papier")

        bt_maj_txt1 = self.tr("Mettre à jour")
        bt_maj_txt2 = self.tr("ne sont pas supprimés")

        self.ui.update.setToolTip(f"<p style='white-space:pre'><center>{bt_maj_txt1} {txt1} :\n\n"
                                  f"<b>{txt2} <u>{bt_maj_txt2} !")

        bt_remp_txt1 = self.tr("Remplacer")
        bt_remp_txt2 = self.tr("sont supprimés")

        self.ui.replace.setToolTip(f"<p style='white-space:pre'><center>{bt_remp_txt1} {txt1} :\n\n"
                                   f"<b>{txt2} <u>{bt_remp_txt2} !")

        self.reponse = ""

    def show_message_existing(self, message: str, bt_update="", bt_replace="", bt_duplicate="",
                              chk_all=True, checkbox_index=0, checkbox_total=0, checkbox_tooltips="",
                              details=None, default_bouton="bt_maj"):

        texte_chk = self.tr("Appliquer aux éléments suivants")

        self.ui.message.setText(message)

        self.ui.update.setText(f" {bt_update}")
        self.ui.replace.setText(f" {bt_replace}")
        self.ui.duplicate.setText(f" {bt_duplicate}")

        if checkbox_total == 1:
            self.ui.chk_all.setChecked(False)
        else:
            self.ui.chk_all.setChecked(chk_all)

        if checkbox_total == 1 or (checkbox_index == checkbox_total):
            self.ui.chk_all.setEnabled(False)
        else:
            self.ui.chk_all.setEnabled(True)

        if checkbox_total != 1:
            self.ui.chk_all.setText(f"{texte_chk} ({checkbox_index}/{checkbox_total})")
        else:
            self.ui.chk_all.setText(texte_chk)

        self.ui.chk_all.setToolTip(checkbox_tooltips)

        if details is not None:
            texte = "\n".join(details)
            self.ui.details.setText(texte)

        if default_bouton == "bt_maj":
            self.ui.update.setFocus()

        elif default_bouton == "bt_dupliquer":
            self.ui.duplicate.setFocus()

        else:
            self.ui.replace.setFocus()

        self.ui.duplicate.setIcon(get_icon(paste_icon))

        self.exec()

    def update_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.YesAll
        else:
            self.reponse = QMessageBox.Yes

        self.close()

    def replace_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.SaveAll
        else:
            self.reponse = QMessageBox.Save

        self.close()

    def duplicate_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.NoAll
        else:
            self.reponse = QMessageBox.No

        self.close()

    def quit_clicked(self):

        self.reponse = QMessageBox.Cancel
        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.reponse == "":
            self.reponse = QMessageBox.Cancel

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class MessageChildren(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MessageChildren()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.ui.ok.clicked.connect(self.yes_clicked)
        self.ui.no.clicked.connect(self.no_clicked)
        self.ui.quit.clicked.connect(self.quit_clicked)

        self.reponse = ""

    def show_message_children(self, message: str, bt_ok="", bt_no="", chk_all=True,
                              checkbox_index=0, checkbox_total=0, checkbox_tooltips="",
                              details=None, default_bouton="ok"):

        text_chk = self.tr("Appliquer aux éléments suivants")

        self.ui.message.setText(message)

        self.ui.ok.setText(bt_ok)
        self.ui.no.setText(bt_no)

        if checkbox_total == 1:
            self.ui.chk_all.setChecked(False)
        else:
            self.ui.chk_all.setChecked(chk_all)

        if checkbox_total == 1 or (checkbox_index == checkbox_total):
            self.ui.chk_all.setEnabled(False)
        else:
            self.ui.chk_all.setEnabled(True)

        if checkbox_total != 1:
            self.ui.chk_all.setText(f"{text_chk} ({checkbox_index}/{checkbox_total})")

        self.ui.chk_all.setToolTip(checkbox_tooltips)

        if details is not None:
            text = "\n".join(details)
            self.ui.details.setText(text)

        if default_bouton == "ok":
            self.ui.ok.setFocus()
        else:
            self.ui.no.setFocus()

        self.exec()

    def yes_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.YesAll
        else:
            self.reponse = QMessageBox.Yes

        self.close()

    def no_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.NoAll
        else:
            self.reponse = QMessageBox.No

        self.close()

    def quit_clicked(self):

        self.reponse = QMessageBox.Cancel
        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.reponse == "":
            self.reponse = QMessageBox.Cancel

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class MessageLocation(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MessageLocation()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.ui.tree.doubleClicked.connect(self.ok_clicked)
        self.ui.ok.clicked.connect(self.ok_clicked)

        self.ui.quit.clicked.connect(self.close)

        self.ui.tree.expandAll()

        self.child_txt = ""
        self.parent_txt = ""

        self.reponse = QMessageBox.Cancel

    def show_message_location(self, message: str,
                              parent_txt="", parent_type="",
                              child_txt="", child_type=""):

        self.ui.message.setText(message)

        self.parent_txt = parent_txt
        self.child_txt = child_txt

        self.ui.tree.topLevelItem(0).setText(0, parent_txt)
        self.ui.tree.topLevelItem(0).setIcon(0, get_icon(f":/Images/{parent_type}.png"))

        a = self.tr("Ajouter dans")
        b = self.tr("Frère")
        c = self.tr("Sera frère de")
        d = self.tr("Ajouter après")
        e = self.tr("Enfant")
        f = self.tr("Sera enfant de")
        g = self.tr("Ajouter comme 1er enfant")

        self.ui.tree.topLevelItem(0).child(1).setText(0, f"{a} '{parent_txt}' ({b})")
        self.ui.tree.topLevelItem(0).child(1).setToolTip(0, f"{c} '{parent_txt}' --> "
                                                            f"{d} '{child_txt}'")

        self.ui.tree.topLevelItem(0).child(0).setText(0, child_txt)
        self.ui.tree.topLevelItem(0).child(0).setIcon(0, get_icon(f":/Images/{child_type}.png"))

        self.ui.tree.topLevelItem(0).child(0).child(0).setText(0, f"{a} '{child_txt}' ({e})")
        self.ui.tree.topLevelItem(0).child(0).child(0).setToolTip(0, f"{f} '{child_txt}' --> {g}")

        self.ui.tree.setCurrentItem(self.ui.tree.topLevelItem(0).child(0).child(0))

        self.exec()

    def ok_clicked(self):

        current_item = self.ui.tree.currentItem()

        if current_item is None:
            return None

        current_text = current_item.toolTip(0)

        if self.tr("Sera enfant de") in current_text:
            self.reponse = QMessageBox.Yes
        else:
            self.reponse = QMessageBox.No

        self.close()

    @staticmethod
    def a___________________end______():
        pass
