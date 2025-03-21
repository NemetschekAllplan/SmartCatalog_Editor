#!/usr/bin/python3
# -*- coding: utf-8 -*
import glob
import io
import json
import os.path
import platform
import shutil
import subprocess
import urllib.request
import webbrowser
from collections import OrderedDict, Counter
from datetime import datetime
from io import BytesIO
from typing import Union

import clr
import openpyxl
import requests
from ftfy import fix_text
from lxml import etree
from send2trash import send2trash

from main_datas import *
from translation_manage import get_favorites_allplan_dict
from ui_message import Ui_Message

try:

    # noinspection PyUnresolvedReferences
    clr.AddReference("System.Windows.Forms")

    # noinspection PyUnresolvedReferences
    from System.Windows.Forms import OpenFileDialog, SaveFileDialog, FileDialogCustomPlace, DialogResult

    load_ok = True

except Exception as error2:
    print(f"browser -- get_common_dialog_path -- {error2}")
    load_ok = False

invalid_chars = ("<", ">", ":", '"', "/", "\\", "|", "?", "*")

invalides_mots = ("CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7",
                  "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9")

menu_ht_ligne = 24
menu_ht_widget = 20
taille_police = 10
taille_police_menu = 10


def a___________________validateurs_______________():
    pass


class ValidatorModel(QValidator):

    def __init__(self, model, column_index=0):
        QValidator.__init__(self)
        self.model: QStandardItemModel = model
        self.column_index = column_index

    def validate(self, p_str: str, p_int: int):

        # Si ce que l'utilisateur a tapé est exactement un élément de la liste, alors c'est 100 % acceptable
        recherche = self.model.findItems(p_str, Qt.MatchExactly, self.column_index)

        if len(recherche) == 1:
            return QValidator.Acceptable, p_str, p_int

        # Si c'est le début d'au moins 1 élément de la liste, c'est Intermediate (probablement
        # acceptable + tard, mais pas encore certain)
        try:
            recherche = self.model.findItems(p_str, Qt.MatchContains, self.column_index)

            if len(recherche) > 0:
                return QValidator.Intermediate, p_str, p_int

        except IndexError:
            return QValidator.Invalid, p_str, -1

        except AttributeError:
            return QValidator.Invalid, p_str, -1

        # Si c'est ni acceptable, ni intermediate, c'est invalide...
        return QValidator.Invalid, p_str, -1

    def fixup(self, p_str):
        pass


class ValidatorInt(QValidator):

    def __init__(self, min_val=None, max_val=None):
        super().__init__()

        self.liste = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]

        if isinstance(min_val, int):
            self.min_val = min_val
        else:
            self.min_val = None

        if isinstance(max_val, int):
            self.max_val = max_val
        else:
            self.max_val = None

    def validate(self, p_str, p_int):

        if p_int == 0:
            return QValidator.Acceptable, p_str, p_int

        # Si ce que l'utilisateur a tapé est exactement un élément de la liste, alors c'est 100 % acceptable
        try:
            if p_str[p_int - 1] in self.liste:

                if self.min_val is None and self.max_val is None:
                    return QValidator.Acceptable, p_str, p_int

                value_int = int(p_str)

                if self.min_val is not None:

                    if value_int < self.min_val:
                        return QValidator.Invalid, p_str, -1

                if self.max_val is not None:

                    if value_int > self.max_val:
                        return QValidator.Invalid, p_str, -1

                return QValidator.Acceptable, p_str, p_int

        except IndexError:
            print("IndexError")
            return QValidator.Invalid, p_str, -1
        except AttributeError:
            print("AttributeError")
            return QValidator.Invalid, p_str, -1
        except ValueError:
            print("ValueError")
            return QValidator.Invalid, p_str, -1

        # Si c'est ni acceptable, ni intermediate, c'est invalide...
        return QValidator.Invalid, p_str, -1

    def fixup(self, p_str):
        pass


class ValidatorDouble(QValidator):

    def __init__(self, min_val=None, max_val=None):
        super().__init__()
        self.liste = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ",", ".", "-"]

        if isinstance(min_val, int):
            self.min_val = min_val
        else:
            self.min_val = None

        if isinstance(max_val, int):
            self.max_val = max_val
        else:
            self.max_val = None

    def validate(self, p_str: str, p_int: int):
        if p_int == 0:
            return QValidator.Acceptable, p_str, p_int

        # Si ce que l'utilisateur a tapé est exactement un élément de la liste, alors c'est 100 % acceptable
        try:
            if p_str[p_int - 1] in self.liste:

                # Vérification qu'une seule virgule exite
                if p_str.count(",") + p_str.count(".") > 1:
                    return QValidator.Invalid, p_str, -1

                if self.min_val is None and self.max_val is None:
                    return QValidator.Acceptable, p_str, p_int

                p_str_format = p_str.replace(",", ".")

                value_int = float(p_str_format)

                if self.min_val is not None:

                    if value_int < self.min_val:
                        return QValidator.Invalid, p_str, -1

                if self.max_val is not None:

                    if value_int > self.max_val:
                        return QValidator.Invalid, p_str, -1

                return QValidator.Acceptable, p_str, p_int

        except IndexError:
            return QValidator.Invalid, p_str, -1

        except AttributeError:
            return QValidator.Invalid, p_str, -1

        except ValueError:
            return QValidator.Invalid, p_str, -1

        # Si c'est ni acceptable, ni intermediate, c'est invalide...
        return QValidator.Invalid, p_str, -1

    def fixup(self, p_str):
        pass


class ValidatorDate(QValidator):

    def __init__(self):
        super().__init__()
        self.liste = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/"]

    def validate(self, p_str: str, p_int: int):

        if p_int == 0:
            return QValidator.Acceptable, p_str, p_int

        # Si ce que l'utilisateur a tapé est exactement un élément de la liste, alors c'est 100 % acceptable
        try:
            if p_str[p_int - 1] in self.liste:
                return QValidator.Acceptable, p_str, p_int
        except IndexError:
            return QValidator.Invalid, p_str, -1

        except AttributeError:
            return QValidator.Invalid, p_str, -1

        # Si c'est ni acceptable, ni intermediate, c'est invalide...
        return QValidator.Invalid, p_str, -1

    def fixup(self, p_str):
        pass


def a___________________menu_______________():
    pass


class MyContextMenu(QMenu):
    help_request = pyqtSignal(str)

    def __init__(self, title="", qicon=None, tooltips_visible=True, tooltips="", short_link=""):
        super().__init__()

        self.menu_ht_line = 24

        self.tooltips_visible = tooltips_visible

        current_font = self.font()
        current_font.setPointSize(taille_police_menu)
        self.setFont(current_font)

        changer_apparence_selection(widget=self)

        if isinstance(title, str) and title != "":
            self.setTitle(title)

        if isinstance(qicon, QIcon):
            self.setIcon(qicon)

        if isinstance(tooltips, bool):
            self.setToolTipsVisible(tooltips_visible)
        else:
            self.setToolTipsVisible(True)

        if isinstance(tooltips, str) and tooltips != "":
            self.setToolTip(tooltips)

        if isinstance(short_link, str) and short_link != "":
            self.setWhatsThis(short_link)

    def add_title(self, title: str, short_link="") -> QAction:

        action_widget = QWidgetAction(self)
        action_widget.setEnabled(False)
        action_widget.setIconVisibleInMenu(False)

        if not title.startswith("<b>"):
            title = f"<b> ---  {title}  --- "
        else:
            title = f" ---  {title}  --- "

        label = QLabel(title)

        font_w = label.font()
        font_w.setPointSize(taille_police_menu)
        label.setFont(font_w)

        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(self.menu_ht_line)
        label.setMinimumWidth(300)

        label.setStyleSheet("background: #BAD0E7; color: #4D4D4D; border: 1px solid #C4C4C4")

        action_widget.setDefaultWidget(label)

        if isinstance(short_link, str) and short_link != "":
            action_widget.setWhatsThis(short_link)

        self.addAction(action_widget)

        return action_widget

    def add_action(self, qicon=None, title="", action=None, tooltips="", objectname="", short_link="") -> QAction:

        if isinstance(qicon, QIcon):

            if action is not None:
                new_action = self.addAction(qicon, title, action)
            else:
                new_action = self.addAction(qicon, title)

        else:

            if action is not None:
                new_action = self.addAction(title, action)
            else:
                new_action = self.addAction(title)

        if isinstance(tooltips, str) and tooltips != "":
            new_action.setToolTip(tooltips)

        elif self.tooltips_visible:
            new_action.setToolTip(title)

        if isinstance(objectname, str) and objectname != "":
            new_action.setObjectName(objectname)

        if isinstance(short_link, str) and short_link != "":
            new_action.setWhatsThis(short_link)

        return new_action

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.key() != Qt.Key_F1:
            return

        position_cursor = QCursor().pos()

        try:

            local_pos = self.mapFromGlobal(position_cursor)

            action = self.actionAt(local_pos)

        except Exception as error:
            print(f"tools -- MyContextMenu -- keyPressEvent -- error : {error}")
            return

        if not isinstance(action, QAction):
            print(f"tools -- MyContextMenu -- keyPressEvent -- not isinstance(widget, QPushButton)")
            return

        short_link = action.whatsThis()

        if short_link == "":
            short_link = self.whatsThis()

            if self.whatsThis() == "":
                return

        self.help_request.emit(short_link)

    @staticmethod
    def a___________________end______():
        pass


def a___________________message_______________():
    pass


class WidgetMessage(QDialog):

    def __init__(self):
        super().__init__()

        # Chargement de l'interface
        self.ui = Ui_Message()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.ui.bt_oui.clicked.connect(self.bouton_oui_clicked)
        self.ui.bt_non.clicked.connect(self.bouton_non_clicked)
        self.ui.bt_save.clicked.connect(self.bouton_save_clicked)
        self.ui.bt_annuler.clicked.connect(self.bouton_annuler_clicked)

        self.deplier_actif = False
        self.avec_checkbox = False
        self.save = False

        self.reponse = None
        self.check = False

        self.ht_defaut = 104
        self.ht_chk = 123
        self.ht_details_chk = 126
        self.ht_details = 225

        self.resize(QSize(300, self.ht_defaut))

        self.ui.bt_deplier.clicked.connect(self.gestion_deplier)

        self.ui.copy.clicked.connect(self.message_copy)
        self.ui.save.clicked.connect(self.message_save)

    def show_message(self, title: str, message: str, infos="",
                     type_bouton=None, defaut_bouton=None,
                     bt_oui=str(), bt_non=str(), bt_annuler=True,
                     icone_question=False, icone_avertissement=False, icone_critique=False, icone_valide=False,
                     icone_sauvegarde=False, icone_lock=False, icone_ouvrir=False,
                     details=None, txt_save=str(), afficher_details=False):
        """
        Permet d'afficher un message
        :param title: Titre de la fenêtre
        :param message: Message à afficher
        :param infos: Checkbox pour ne plus afficher -> nom de l'élément dans la base de registre
        :param type_bouton: Défini le type de bouton :
                            QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel | QMessageBox.Save)

        :param defaut_bouton: Défini le bouton par défaut à selectionner
        :param bt_oui: Texte du bouton oui -> QMessageBox.Ok
        :param bt_non: Texte du bouton non -> QMessageBox.No
        :param bt_annuler: (obsolète)
        :param icone_question: Permet d'afficher l'icône de question
        :param icone_avertissement: Permet d'afficher l'icône de l'avertissement
        :param icone_critique: Permet d'afficher l'icône d'une erreur critique
        :param icone_valide: Permet d'afficher l'icône pour la validation (OK)
        :param icone_sauvegarde: Permet d'affciher l'icône de sauvegarde
        :param icone_lock: Permet d'affciher l'icône de sauvegarde
        :param icone_ouvrir: Permet d'afficher l'icône ouvrir
        :param details: Permet d'afficher plus de détails
        :param txt_save: Permet d'afficher et de modifier le texte -> QMessageBox.Save
        :param afficher_details: Bool permettant d'afficher ou masquer les détails (défaut false)
        :return: None
        """

        # Gestion du titre
        self.setWindowTitle(title)

        # Gestion du message
        self.ui.message.setText(message)
        # Gestion icône
        self.gestion_icone(icone_question,
                           icone_avertissement,
                           icone_critique,
                           icone_valide,
                           icone_sauvegarde,
                           icone_lock,
                           icone_ouvrir)

        # Gestion boutons
        self.gestions_boutons(type_bouton, defaut_bouton, bt_oui, bt_non, bt_annuler, txt_save)

        # Gestion checkbox
        self.gestion_checkbox(infos)

        # Géstion détails
        self.gestion_details(details, not afficher_details)

        self.exec()

    def gestion_icone(self, icone_question: bool, icone_avertissement: bool, icone_critique: bool, icone_valide,
                      icone_sauvegarde: bool, icone_lock: bool, icone_ouvrir: bool):
        """
        Permet de gérer les icônes
        :param icone_question: Permet d'afficher l'icône de question
        :param icone_avertissement: Permet d'afficher l'icône de l'avertissement
        :param icone_critique: Permet d'afficher l'icône d'une erreur critique
        :param icone_valide: Permet d'afficher l'icône pour la validation (OK)
        :param icone_sauvegarde: Permet d'affciher l'icône de sauvegarde
        :param icone_lock: Permet d'affciher l'icône cadenas
        :param icone_ouvrir: Permet d'afficher l'icône Ouvrir
        :return: None
        """

        image = information_icon

        if icone_question:
            image = help_icon

        elif icone_avertissement:
            image = warning_icon

        elif icone_critique:
            image = error_icon

        elif icone_valide:
            image = valid_icon

        elif icone_sauvegarde:
            image = save_icon

        elif icone_lock:
            image = lock_icon

        elif icone_ouvrir:
            image = open_icon

        self.ui.icon.setIcon(get_icon(image))

    def gestions_boutons(self, type_bouton=None, defaut_bouton=None,
                         bt_oui=str(), bt_non=str(), bt_annuler=True, txt_save=str()):

        """
        Permet de gérer les textes et l'affichage des boutons
        :param type_bouton: Défini le type de bouton
        :param defaut_bouton: Défini le bouton par défaut à selectionner
        :param bt_oui: Texte du bouton oui -> QMessageBox.Ok
        :param bt_non: Texte du bouton non -> QMessageBox.No
        :param bt_annuler: Permet de cacher le bouton annuler -> QMessageBox.Cancel
        :param txt_save: Permet de changer le nom save -> QMessageBox.Save
        :return: None
        """

        if type_bouton is not None:

            # Bouton seul (4)
            if type_bouton == QMessageBox.No:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_save.setVisible(False)

            elif type_bouton == QMessageBox.Save:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_non.setVisible(False)
                self.ui.bt_annuler.setVisible(False)

            elif type_bouton == QMessageBox.Cancel:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_non.setVisible(False)
                self.ui.bt_save.setVisible(False)

            # Bouton OK (3)
            elif type_bouton == QMessageBox.Ok | QMessageBox.No:
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_save.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.Save:
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_non.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.Cancel:
                self.ui.bt_non.setVisible(False)
                self.ui.bt_save.setVisible(False)

            # Bouton non (2)
            elif type_bouton == QMessageBox.No | QMessageBox.Save:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_annuler.setVisible(False)

            elif type_bouton == QMessageBox.No | QMessageBox.Cancel:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_save.setVisible(False)

            # Bouton save (1)
            elif type_bouton == QMessageBox.Save | QMessageBox.Cancel:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_non.setVisible(False)

            # Bouton triple
            elif type_bouton == QMessageBox.Ok | QMessageBox.Save | QMessageBox.Cancel:
                self.ui.bt_non.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.No | QMessageBox.Save:
                self.ui.bt_annuler.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel:
                self.ui.bt_save.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.Save | QMessageBox.Cancel:
                self.ui.bt_non.setVisible(False)

            elif type_bouton == QMessageBox.No | QMessageBox.Save | QMessageBox.Cancel:
                self.ui.bt_oui.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.No | QMessageBox.Save | QMessageBox.Cancel:
                pass

            else:
                self.ui.bt_non.setVisible(False)
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_oui.setText("OK")

        else:

            if (bt_oui == "" or bt_oui == "Ok") and bt_non == "" and txt_save == "":
                self.ui.bt_non.setVisible(False)
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_oui.setText("OK")

        self.ui.bt_oui.setFocus()

        if defaut_bouton is not None:

            if defaut_bouton == QMessageBox.No:
                self.ui.bt_non.setFocus()

            elif defaut_bouton == QMessageBox.Save:
                self.ui.bt_save.setFocus()

            elif defaut_bouton == QMessageBox.Cancel:
                self.ui.bt_annuler.setFocus()

        if bt_oui != "":
            self.ui.bt_oui.setText(f" {bt_oui} ")

        if bt_non != "":
            self.ui.bt_non.setText(f" {bt_non} ")

        if txt_save != "":
            self.ui.bt_save.setVisible(True)
            self.ui.bt_save.setText(f" {txt_save} ")

        else:
            self.ui.bt_save.setVisible(False)

        if not bt_annuler:
            pass

        self.sizeHint()

    def gestion_checkbox(self, infos: str):
        """
        Permet de gérer l'affichage de la checkbox
        :param infos: Checkbox pour ne plus afficher -> nom de l'élément dans la base de registre
        :return: None
        """

        if infos == "":
            self.ui.infos_widget.setVisible(False)
            return

        self.avec_checkbox = True

    def gestion_details(self, details, afficher_details):
        """
        Permet de gérer l'affichage du détail
        :param details: Permet d'afficher plus de détails
        :param afficher_details: Permet d'afficher plus de détails
        :return:
        """

        texte = ""

        if isinstance(details, list):

            nb_caractere = 3

            try:
                nb_items = str(len(details))
                nb_caractere = len(nb_items)

            except ValueError:
                pass

            for index_item in range(len(details)):

                try:

                    index_str = str(index_item)
                    index_str = index_str.zfill(nb_caractere)

                except ValueError:
                    index_str = f"{index_item}"

                texte += f"{index_str} ==> {details[index_item]}\n"

        elif isinstance(details, dict):

            for key in details.keys():
                texte += f"{key} ==> {details[key]}\n"

        else:

            texte = details

        self.deplier_actif = afficher_details

        if details is None or details == "":
            self.ui.bt_deplier.setVisible(False)
            self.ui.details_widget.setVisible(False)

            self.ui.details.clear()

            self.deplier_actif = False

            return

        self.ui.bt_deplier.setVisible(True)

        self.ui.details.setText(f"{texte}")

        self.gestion_deplier()

    def gestion_deplier(self):
        """
        Permet de gérer l'affichage de l'icône pour déplier et replier les détails
        :return: None
        """

        self.deplier_actif = not self.deplier_actif

        self.setMaximumHeight(16777215)
        self.ui.details_widget.setVisible(self.deplier_actif)

        if self.deplier_actif:
            self.ui.bt_deplier.setIcon(get_icon(detail_hide_icon))

            height = self.ui.message_widget.height()

            if height < 40:
                height = 40

            self.ui.message_widget.setMaximumHeight(height)
            return

        self.ui.bt_deplier.setIcon(get_icon(detail_show_icon))

        self.ui.message_widget.setMaximumHeight(16777215)

        self.adjustSize()

        self.resize(self.width(), 0)
        self.setMaximumHeight(self.height())

    def bouton_oui_clicked(self):
        """
        Permet de mettre en mémoire la réponse de l'utilisateur = OK
        :return: None
        """
        self.save = True
        self.reponse = QMessageBox.Ok
        self.check = self.ui.checkbox.isChecked()
        # print(f"bouton_ok_clicked -- checkbox == {self.ui.checkbox.isChecked()}")
        self.close()

    def bouton_non_clicked(self):
        """
        Permet de mettre en mémoire la réponse de l'utilisateur = No
        :return:None
        """

        self.save = True
        self.reponse = QMessageBox.No
        self.check = self.ui.checkbox.isChecked()

        # print(f"bouton_no_clicked -- checkbox == {self.ui.checkbox.isChecked()}")
        self.close()

    def message_copy(self):

        text = self.ui.details.toPlainText()

        if not isinstance(text, str):
            return

        QApplication.clipboard().setText(text)

    def message_save(self):

        shortcuts_list = [asc_export_path]

        a = QCoreApplication.translate("tools", "Fichier")

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 datas_filters={f"{a} TXT": [".txt"]},
                                 registry=[app_setting_file, "path_export"],
                                 shortcuts_list=shortcuts_list,
                                 current_path=asc_export_path,
                                 default_path="",
                                 use_setting_first=True,
                                 use_save=True)

        if file_path == "":
            return

        text = self.ui.details.toPlainText()

        if not isinstance(text, str):
            return

        try:
            with open(file_path, "w", encoding="UTF-8") as file:
                file.write(text)

        except Exception as error:
            print(f"message -- WidgetMessage -- message_save -- error : {error}")

    def bouton_annuler_clicked(self):
        """
        Permet de mettre en mémoire la réponse de l'utilisateur = Cancel
        :return: None
        """

        self.save = True
        self.reponse = QMessageBox.Cancel
        self.check = self.ui.checkbox.isChecked()

        # print(f"bouton_cancel_clicked -- checkbox == {self.ui.checkbox.isChecked()}")

        self.close()

    def bouton_save_clicked(self):
        """
        Permet de mettre en mémoire la réponse de l'utilisateur = Save
        :return: None
        """

        self.save = True
        self.reponse = QMessageBox.Save
        self.check = self.ui.checkbox.isChecked()

        # print(f"bouton_cancel_clicked -- checkbox == {self.ui.checkbox.isChecked()}")

        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if not self.save:
            self.reponse = QMessageBox.Cancel
            self.check = False

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


def a___________________browser_______________():
    pass


def browser_file(parent: QObject, title: str, datas_filters: dict, registry: list, shortcuts_list: list,
                 current_path="", default_path="",
                 file_name="", use_setting_first=True, use_save=False) -> str:
    """

    :param parent: Objet parent
    :param title: Title of dialog
    :param datas_filters:  {"Images" : [".png", ".jpg"], "Pdf" : [".pdf"]}
    :param registry: [file_setting_name, setting_name]
    :param shortcuts_list: shortcut paths list
    :param current_path: current_path
    :param default_path: default_path
    :param file_name: file_name
    :param use_setting_first: True = searh in the registry + current + default // False = current + registry + default
    :param use_save: bool : False = for select file // True = For save file
    :return: Path of select file or empty text
    """

    if not isinstance(title, str) or not isinstance(current_path, str) or not isinstance(default_path, str):
        print(f"browser -- browser_file -- not isinstance(title, str)")
        return ""

    if not isinstance(datas_filters, dict) or not isinstance(registry, list) or not isinstance(shortcuts_list, list):
        print(f"browser -- browser_file -- not isinstance(title, str)")
        return ""

    if not isinstance(file_name, str) or not isinstance(use_setting_first, bool) or not isinstance(use_save, bool):
        print(f"browser -- browser_file -- not isinstance(file_name, str)")
        return ""

    current_folder = find_folder_path(current_path)

    default_folder = find_folder_path(default_path)

    if len(registry) != 2:
        settings_folder = default_folder
    else:
        settings_folder = settings_get(file_name=registry[0], info_name=registry[1])

        if settings_folder is None:
            settings_folder = default_folder

    target_folder = ""

    if not use_setting_first:

        if current_folder != "" and current_folder != "\\" and os.path.exists(current_folder):

            target_folder = f"{current_folder}{file_name}"

        else:

            if settings_folder != "" and settings_folder != "\\" and os.path.exists(settings_folder):

                target_folder = f"{settings_folder}{file_name}"

            else:

                if default_folder != "" and default_folder != "\\" and os.path.exists(default_folder):
                    target_folder = f"{default_folder}{file_name}"

    else:

        if settings_folder != "" and settings_folder != "\\" and os.path.exists(settings_folder):

            target_folder = f"{settings_folder}{file_name}"

        else:

            if current_folder != "" and current_folder != "\\" and os.path.exists(current_folder):

                target_folder = f"{current_folder}{file_name}"

            else:

                if default_folder != "" and default_folder != "\\" and os.path.exists(default_folder):
                    target_folder = f"{default_folder}{file_name}"

    if load_ok == "":

        file_path = browser_file_classic(parent=parent,
                                         title=title,
                                         datas_filters=datas_filters,
                                         target_folder=target_folder,
                                         use_save=use_save)
    else:

        file_path = browser_file_new(title=title,
                                     datas_filters=datas_filters,
                                     shortcuts_list=shortcuts_list,
                                     target_folder=target_folder,
                                     use_save=use_save)

    if file_name == file_path:
        return ""

    if file_path == "":
        return ""

    folder_current = find_folder_path(file_path)

    if folder_current != "" and folder_current != "\\":
        if len(registry) == 2:
            settings_save_value(file_name=registry[0], key_name=registry[1], value=folder_current)

    file_path: str = file_path.replace("/", "\\")

    return file_path

    # if accepter_tous:
    #     return chemin_fichier
    #
    # if use_save:
    #
    #     if len(liste_extensions) == 0:
    #         return chemin_fichier
    #
    #     extension_actuelle = liste_extensions[0]
    #
    #     if chemin_fichier.endswith(extension_actuelle):
    #         return chemin_fichier
    #
    #     chemin_fichier += extension_actuelle
    #     return chemin_fichier
    #
    # for extension in liste_extensions:
    #
    #     extension: str
    #     fichier_upper = chemin_fichier.upper()
    #
    #     if fichier_upper.endswith(extension.upper()):
    #         return chemin_fichier
    #
    # afficher_message(titre=parent.tr("Erreur extension de fichier"),
    #                  message=parent.tr("L'extension du fichier est non valide !"),
    #                  icone_avertissement=True)
    #
    # return ""


def browser_file_classic(parent: QObject, title: str, datas_filters: dict, target_folder: str, use_save=False) -> str:
    extensions_list = list()
    filters_list = list()

    for filter_title, extensions in datas_filters.items():

        for extension in extensions:

            if extension == ".*":
                extensions_list.clear()
                break

            if extension in extensions_list:
                continue

            extensions_list.append(extension)

        extensions: list
        extension_str = f'*{" *".join(extensions)}'
        filters_list.append(f'{filter_title} ({extension_str})')

    filter_str = ";;".join(filters_list)

    if not use_save:

        file_path, _filter = QFileDialog.getOpenFileName(parent=parent,
                                                         caption=title,
                                                         directory=target_folder,
                                                         filter=filter_str)
    else:

        file_path, _filter = QFileDialog.getSaveFileName(parent=parent,
                                                         caption=title,
                                                         directory=target_folder,
                                                         filter=filter_str)

    if not isinstance(file_path, str):
        return ""

    if file_path == "":
        return ""

    return file_path


def browser_file_new(title: str, datas_filters: dict, shortcuts_list: list, target_folder: str, use_save=False) -> str:
    filter_extensions = list()

    for title_filter, extensions in datas_filters.items():

        if not isinstance(extensions, list):
            print(f"browser -- browser_file2 -- not isinstance(extensions, list)")
            continue

        filter_extensions.append(f"{title_filter} (*{';*'.join(extensions)})|*{';*'.join(extensions)}")

    filters = "|".join(filter_extensions)

    # ------------------------------------------
    try:

        if use_save:
            dlg = SaveFileDialog()
        else:
            dlg = OpenFileDialog()

        dlg.CheckFileExists = not use_save

        dlg.Title = title
        dlg.Filter = filters

        dlg.InitialDirectory = find_folder_path(file_path=target_folder)

        dlg.FileName = find_filename(file_path=target_folder, with_ext=True)

        for path in shortcuts_list:
            dlg.CustomPlaces.Add(FileDialogCustomPlace(path))

        result = dlg.ShowDialog()

        if result == DialogResult.Cancel:
            return ""

        filename = dlg.FileName

        if not isinstance(filename, str):
            return ""

        return filename

    except Exception as error:
        print(f"browser -- browser_file2 -- error : {error}")
        return ""


def a___________________formatages_______________():
    pass


def date_formatting(date_texte: str) -> str:
    lg = settings_get(app_setting_file, "language")

    if "/" not in date_texte:
        if len(date_texte) >= 6:

            if lg != "FR":

                mois = date_texte[:2]
                jour = date_texte[2:4]
                annee = date_texte[4:]

                date_texte = f'{mois}/{jour}/{annee}'

            else:
                jour = date_texte[:2]
                mois = date_texte[2:4]
                annee = date_texte[4:]

                date_texte = f'{jour}/{mois}/{annee}'

    if date_texte.count("/") != 2:
        afficher_message(titre=application_title,
                         message=QCoreApplication.translate("tools", "Le nombre de ' / ' n'est pas correct, désolé!"),
                         icone_avertissement=True)
        return ""

    liste_datas = date_texte.split('/')

    jour = f'{liste_datas[0].zfill(2)}'
    mois = f'{liste_datas[1].zfill(2)}'
    annee = liste_datas[2]

    try:
        jour_int = int(jour)
        mois_int = int(mois)
        annee_int = int(annee)
    except Exception:
        return ""

    if jour_int == 0:
        afficher_message(titre=application_title,
                         message=QCoreApplication.translate("tools",
                                                            "Le numéro du jour est non valide (égale à 0), désolé!"),
                         icone_avertissement=True)
        return ""

    if mois_int == 0:
        afficher_message(titre=application_title,
                         message=QCoreApplication.translate("tools",
                                                            "Le numéro du mois est non valide (égale à 0), désolé!"),
                         icone_avertissement=True)
        return ""

    if mois_int > 12:
        if jour_int <= 12:
            jour = f'{liste_datas[1].zfill(2)}'
            mois = f'{liste_datas[0].zfill(2)}'
            jour_int = int(jour)
            mois_int = int(mois)
        else:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate(
                                 "tools",
                                 "Le numéro du mois est non valide (supérieur à 12), désolé!"),
                             icone_avertissement=True)
            return ""

    mois_31 = [1, 3, 5, 7, 8, 10, 12]
    mois_30 = [4, 6, 9, 11]

    if mois_int in mois_31:
        if jour_int > 31:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate(
                                 "tools", "Le numéro du jour est non valide (supérieur à 31), désolé!"),
                             icone_avertissement=True)
            return ""

    elif mois_int in mois_30:
        if jour_int > 30:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate(
                                 "tools", "Le numéro du jour est non valide (supérieur à 30), désolé!"),
                             icone_avertissement=True)
            return ""

    else:
        if jour_int > 29:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate(
                                 "tools", "Le numéro du jour est non valide (supérieur à 29), désolé!"),
                             icone_avertissement=True)
            return ""

    if len(annee) == 2:

        cet_annee = int(QDate.currentDate().year())

        if annee_int > cet_annee - 2000:
            annee = f'19{annee}'
        else:
            annee = f'20{annee}'

    if lg != "FR":
        date_formatter = f'{mois}/{jour}/{annee}'
    else:
        date_formatter = f'{jour}/{mois}/{annee}'

    return date_formatter


def format_float_value(value: str, allplan_version: str):
    """
    Permet de convertir les textes contenant des numéros de type float
    :param value: numéro à convertir
    :return: numéro converti
    :rtype: str
    """

    if value == "":
        return value

    try:

        value_tps = value.replace(",", ".")
        value_float = float(value_tps)
        value_tps = f"{value_float:.3f}"

        if "2022" in allplan_version or "2023" in allplan_version:
            value_tps = value_tps.replace(".", ",")

        return value_tps

    except ValueError:

        print("formater_numero_decimal -- le formatage a échoué")
        return value


def recherche_position_parentheses(formule: str) -> list:
    """
    recherche les position des parenthèses ouvrantes et fermantes
    :param formule:
    :return:
    """
    stack = []
    parentheses_indices = []

    for idx, char in enumerate(formule):
        if char == "(":
            stack.append(idx)
        elif char == ")":
            if stack:
                open_idx = stack.pop()
                parentheses_indices.append((open_idx, idx))

    return parentheses_indices


def recherche_couleur(index_couleur: int) -> QColor:
    unique_value = (index_couleur * 123456789) % 16777215  # 16777215 est le nombre maximum pour RVB

    red = (unique_value >> 16) & 0xFF
    green = (unique_value >> 8) & 0xFF
    blue = unique_value & 0xFF

    return QColor(red, green, blue)


def find_new_title(base_title: str, titles_list: list):
    titles_list = [nom.upper() for nom in titles_list if isinstance(nom, str)]

    if base_title.upper() not in titles_list:
        return base_title

    try:

        match_fin = re.search(r"(\d+)$", base_title)

        if match_fin:

            last_group = match_fin.group(1)

            for numero in range(1, 99):

                incremented_group = str(int(last_group) + numero)

                # Calculer le nombre de zéros à ajouter pour maintenir la même longueur
                num_zeros_to_add = len(last_group) - len(incremented_group)

                if num_zeros_to_add > 0:
                    incremented_group = "0" * num_zeros_to_add + incremented_group

                # Remplacer le dernier groupe de chiffres par le nouveau dans le texte
                titre_temp = re.sub(r"\d+$", incremented_group, base_title)

                if titre_temp.upper() not in titles_list:
                    return titre_temp

    except Exception as erreur:
        print(f"tools -- find_new_title -- end -- {erreur}")
        pass

    num = 1
    valeur = base_title

    while True:

        # Vérification que le nom n'est pas dans la liste des noms interdits
        if valeur.upper() in titles_list:

            # Définition du nouveau nom
            valeur = f"{base_title} - {num}"

            # Tant que le nouveau nom est dans la liste des numéros interdit, création d'un nouveau nom +1
            num += 1

        # Si le nom n'est plus dans la liste des noms interdits
        else:
            return valeur


def a___________________conversions_______________():
    pass


def convertir_bytes(text_byte: bytes):
    if isinstance(text_byte, str):
        return text_byte.strip()

    if isinstance(text_byte, (int | float)):
        return text_byte

    if text_byte is None:
        return ""

    if not isinstance(text_byte, bytes):
        print(f"tools -- convertir_bytes -- not isinstance(texte_byte, bytes)")
        return ""

    try:
        text = text_byte.decode('cp1252', errors='ignore')

        text = text.strip()

    except Exception as error:
        print(f"tools -- convertir_bytes -- error : {error}")
        return ""

    return text


def a___________________verifications_______________():
    pass


def verification_catalogue_correct(file_path: str, message=True) -> str:
    content = read_file_to_text(file_path=file_path)

    if len(content) == 0:
        if message:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate("tools", "Le fichier semble être vide, désolé"),
                             icone_critique=True)
        return ""

    if "<AllplanCatalog" not in content:
        if message:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate(
                                 "tools", "Le fichier ne semble pas être un Catalogue, désolé"),
                             icone_critique=True)
        return ""

    if "<PositionDef>" not in content:
        return "XML_O"

    return "XML"


def catalog_name_is_correct(catalog_name: str) -> str:
    if catalog_name == "":
        return QCoreApplication.translate("tools", "Vous ne pouvez pas laisser le titre vide.")

    if catalog_name == "test":
        return QCoreApplication.translate("tools", "Ce titre est protégé.")

    if catalog_name in invalides_mots:
        a = QCoreApplication.translate("tools", "fait parti des noms de fichiers interdits dans Windows")
        return f"{catalog_name} {a}"

    for chars in invalid_chars:
        if chars in catalog_name:
            a = QCoreApplication.translate("tools", "le caractère")
            c = QCoreApplication.translate("tools", "fait parti des caractères interdits dans Windows")
            return f"{a} '{chars}' {c}"

    if len(catalog_name) > 27:
        return QCoreApplication.translate("tools", "Le nom de catalogue ne doit pas dépassé 27 caractères")

    return "Ok"


def catalog_xml_region(current_language="EN") -> str:
    if current_language == "EN":
        return "GB"
    return current_language


# def catalog_xml_version(allplan_version: str) -> str:
#     return "1.0"
# if allplan_version == "2025":
#     return "1.1"
#
# return "1.0"


def catalog_xml_date(current_language="EN", date_complet_modif=None) -> str:
    if date_complet_modif is None:
        date_complet_modif = datetime.now()

    if current_language == "FR":
        date_modif = date_complet_modif.strftime("%d-%m-%Y - %H:%M:%S")
    else:
        date_modif = date_complet_modif.strftime("%m-%d-%Y - %I:%M:%S %p")

    return date_modif


def catalog_xml_find_all(element, tag: str, parameter: str, value: str) -> list:
    try:
        if '"' in value and "'" in value:
            parts = value.split('"')
            value = 'concat("' + '", \'"\', "'.join(parts) + '")'
        elif '"' in value:
            value = f"'{value}'"
        else:
            value = f'"{value}"'

        search = element.findall(f'{tag}[@{parameter}={value}]')

        return search

    except SyntaxError:
        pass

    try:

        search = element.xpath(f'{tag}[@{parameter}={value}]')

    except Exception as error:
        print(f"tools -- catalog_xml_find_all - error : {error}")
        return list()

    return search


def convertir_nom_fichier_correct(nom_fichier: str) -> str:
    """Permet de vérifier si le nom du fichier est correct
    :param nom_fichier: Nom du fichier à analyser
    :return: nom fichier correct
    """

    if nom_fichier in invalides_mots:
        return f"{nom_fichier}_"

    # Vérification si le nom du fichier est correct
    for chars in invalid_chars:
        nom_fichier = nom_fichier.replace(chars, " ")

    nom_fichier = nom_fichier.strip()

    return nom_fichier


def validation_fichier_xml(fichier_a_analyser, afficher_msg=True):
    if not os.path.exists(fichier_a_analyser):
        return None

    try:

        tree = etree.parse(fichier_a_analyser)

    except etree.XMLSyntaxError as error:

        if afficher_msg:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate("tools", "Une erreur a été détecté dans le fichier"),
                             icone_critique=True,
                             details=error)

        return None

    except etree.DocumentInvalid as error:

        if afficher_msg:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate("tools", "Une erreur a été détecté dans le fichier"),
                             icone_critique=True,
                             details=error)

        return None

    except OSError as error:

        if afficher_msg:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate("tools", "Le fichier est inaccessible"),
                             icone_critique=True,
                             details=error)

        return None

    except:

        if afficher_msg:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate("tools", "Une erreur a été détecté dans le fichier"),
                             icone_critique=True)
        return None

    else:

        return tree


def get_value_is_valid(xml_element: etree._Element) -> bool:
    if not isinstance(xml_element, etree._Element):
        return False

    texte = xml_element.text

    return texte is not None


def verification_nom_catalogue(chemin_actuel: str):
    """
    Vérification du chemin du fichier
    :param chemin_actuel: chemin_actuel
    :return: nom complet
    """

    chemin_actuel = chemin_actuel.replace("/", "\\")

    nom_fichier = os.path.basename(chemin_actuel)
    chemin = os.path.dirname(chemin_actuel)

    if not chemin.endswith("\\"):
        chemin += "\\"

    nb_char = len(nom_fichier)

    if nb_char <= 31:
        return chemin_actuel

    afficher_message(titre=application_title,
                     message=QCoreApplication.translate(
                         "tools", "Le nombre de caractères du fichier ne peut pas dépacer 27 caractères,"
                                  "le nom du fichier a été rogné."),
                     icone_avertissement=True)

    nom_fichier_ss_ext = nom_fichier[:-4]

    nom_fichier = nom_fichier_ss_ext[:27]

    return f"{chemin}{nom_fichier}.xml"


def verification_projet(prj_folder_path: str) -> bool:
    conf_file_path = f"{prj_folder_path}project.cfg"

    if not os.path.exists(conf_file_path):
        return False

    content = read_file_to_text(file_path=conf_file_path)

    nb_std = 0

    for texte in ['STIFT=STD', 'MUSTER=STD', 'LAYER=STD', 'ASW=STD', 'ATTR=STD']:
        nb_std += texte in content

    return nb_std == 5


def recherche_catalogue_prj(prj_folder: str) -> str:
    conf_file_path = f"{prj_folder}project.cfg"

    if not os.path.exists(conf_file_path):
        return ""

    lines_list = read_file_to_list(file_path=conf_file_path)

    try:

        for texte in lines_list:

            if texte.startswith("XML_CATALOG_NAME"):
                nom_cat = texte.replace("XML_CATALOG_NAME=", "").replace("\n", "")

                return nom_cat

        return ""

    except Exception:
        return ""


def qm_check(qm: QModelIndex) -> bool:
    if not isinstance(qm, QModelIndex):
        return False
    return qm.isValid()


def get_real_path_of_apn_file(file_path: str, prj_path: str, is_cat_folder=False, show_msg=True) -> str:
    """

    :param file_path: Chemin du fichier APN ou PRJ
    :param prj_path: Chemin du dossier prj dans lequel rechercher
    :param is_cat_folder: renvoyer le chemin du dossier SmartCatalog
    :param show_msg: Show avertissement message
    :return: le chemin du dossier PRJ ou SmartCatalog
    """

    file_name = os.path.basename(file_path)

    if file_path.endswith(".prj"):
        extension = ".prj"
        file_name = file_name.replace(extension, "")
        path_file_prj = file_path

    elif file_path.endswith(".apn"):
        extension = ".apn"
        file_name = file_name.replace(extension, "")
        path_file_prj = f"{prj_path}{file_name}.prj"
    else:
        print("outils -- recherche_chemin_projet_apn -- erreur : extension non reconnue")
        return ""

    if not os.path.exists(file_path):

        if show_msg:
            a = QCoreApplication.translate("tools", "Le fichier '.prj' n'existe pas dans le dossier PRJ")
            b = QCoreApplication.translate("tools", "Vous devez créer une liaison du projet dans Allplan")
            c = QCoreApplication.translate("tools", "Fichier")
            d = QCoreApplication.translate("tools", "Gestion de ressources avancés")
            e = QCoreApplication.translate("tools", "Mes projets")
            f = QCoreApplication.translate("tools", "clic droit")
            g = QCoreApplication.translate("tools", "lier un projet existant")

            afficher_message(titre=application_title,
                             message=f"{a}.\n{b} :\n{c} -> {d} -> \n{e} -> {f} -> {g}",
                             icone_avertissement=True)

            print("outils -- recherche_chemin_projet_apn -- erreur : Fichier non lié")

        return ""

    datas_config_apn: list = read_file_to_list(file_path=path_file_prj)

    if len(datas_config_apn) == 0:
        print("outils -- recherche_chemin_projet_apn -- erreur : Fichier vide")
        return ""

    if len(datas_config_apn) < 3:
        print("outils -- recherche_chemin_projet_apn -- erreur : Fichier non valide")
        return ""

    chemin_tmp: str = datas_config_apn[0]
    chemin_tmp = chemin_tmp.replace("\n", "")

    if not chemin_tmp.endswith("\\"):
        chemin_tmp += "\\"

    chemin_tmp_prj = f"{chemin_tmp}{file_name}.prj\\"

    if not os.path.exists(chemin_tmp_prj):
        print("outils -- recherche_chemin_projet_apn -- erreur : projet inexistant")

        afficher_message(titre=application_title,
                         message=QCoreApplication.translate(
                             "tools", "Le projet n'existe pas dans le dossier temporaire d'Allplan."),
                         icone_avertissement=True)

        return ""

    if not is_cat_folder:
        return chemin_tmp_prj

    chemin_dossier_prj_cat = f"{chemin_tmp_prj}Xml\\SmartCatalog\\"

    if not os.path.exists(chemin_dossier_prj_cat):
        return ""

    nom_catalogue = recherche_catalogue_prj(chemin_tmp_prj)

    if nom_catalogue == "":
        afficher_message(titre=application_title,
                         message=QCoreApplication.translate(
                             "tools", "Aucun catalogue n'est actuellement assigné à ce projet."),
                         icone_avertissement=True)

        return ""

    chemin_fichier_cat = f"{chemin_dossier_prj_cat}{nom_catalogue}.xml"

    if not os.path.exists(chemin_fichier_cat):
        afficher_message(titre=application_title,
                         message=QCoreApplication.translate(
                             "tools", "le catalogue assigné à ce projet n'a pas été trouvé"),
                         icone_avertissement=True)
        return ""

    return chemin_fichier_cat


def get_project_use(prj_path: str) -> list:
    prj_lists = list()

    if not os.path.exists(prj_path):
        print("allplan_manage -- get_project_use -- not os.path.exists(prj_path)")
        return prj_lists

    lck_list = glob.glob(f"{prj_path}*.lck")

    if len(lck_list) == 0:
        return prj_lists

    prj_numbers_list = list()

    for path in lck_list:

        prj_number = find_filename(path)

        if not prj_number.startswith("n"):
            print("allplan_manage -- get_project_use -- not prj_number.startswith(n)")
            continue

        prj_number = prj_number.replace("n", "")

        if len(prj_number) != 7:
            print("allplan_manage -- get_project_use -- len(prj_number) != 7")
            continue

        if not prj_number.isnumeric():
            print("allplan_manage -- get_project_use -- not prj_number.isnumeric()")
            continue

        if prj_number in prj_numbers_list:
            print("allplan_manage -- get_project_use -- prj_number in prj_numbers_list")
            continue

        try:
            os.rename(path, path)
            print("allplan_manage -- get_project_use -- This file isn't used")
            continue

        except Exception:
            prj_numbers_list.append(prj_number)

    return prj_numbers_list


def a___________________recherche_______________():
    pass


def recherche_chemin_bcm():
    """
    Permet de récupérer le chemin de BCM
    :return: Chemin de BCM
    :rtype: str
    """

    bcm_setting_path = settings_get(library_setting_file, "path_bcm")

    if bcm_setting_path != "" and os.path.exists(bcm_setting_path):
        return bcm_setting_path

    allright_file_path = "C:\\Windows\\Allright.ini"

    if not os.path.exists(allright_file_path):
        return ""

    lines_list = read_file_to_list(file_path=allright_file_path)

    for ligne in lines_list:

        if "PrjDir=" in ligne:
            bcm_setting_path = ligne.replace("PrjDir=", "").strip()

            if os.path.exists(bcm_setting_path):
                return bcm_setting_path

    return ""


def read_file_to_text(file_path: str) -> str:
    """
        Read file and return contents
        :param file_path: file path
        :return: full contents
        :rtype: str
        """

    if not os.path.exists(file_path):
        print(f"outils -- read_file_to_text == not os.path.exists(file_path)")
        return ""

    bom1 = "ÿþ"
    bom2 = "\ufeff"

    try:
        with open(file_path, "r", errors='ignore') as fichier:
            results = fix_text(fichier.read())

            if not isinstance(results, str):
                return ""

            if results.startswith(bom1):
                results = results.replace(bom1, "", 1)

            if results.startswith(bom2):
                results = results.replace(bom2, "", 1)

            return results

    except Exception as erreur:

        print(f"outils -- read_file_to_text == {erreur}")

        return ""


def read_file_to_list(file_path: str, duplicates=True, list_sorted=False) -> list:
    """
        Read file and parse. return list of all lines
        :param file_path: file_path
        :return: list of all lines
        :rtype: list
        """

    if not os.path.exists(file_path):
        print(f"outils -- read_file_to_list == not os.path.exists(file_path)")
        return list()

    results = read_file_to_text(file_path=file_path)

    if results == "":
        return list()

    if "\n" not in results:
        return [results]

    try:

        lines_list = results.split("\n")

    except Exception as erreur:

        print(f"outils -- read_file_to_list == {erreur}")

        return list()

    if not duplicates:
        lines_list = list(set(lines_list))

    if list_sorted:
        lines_list.sort()

    return lines_list


def a___________________chargements_______________():
    pass


def settings_verifications() -> None:
    for file_name in settings_names.keys():

        if os.path.exists(f"{asc_settings_path}{file_name}.ini"):
            continue

        if file_name == cat_list_file or file_name == unit_list_file:
            settings_save(file_name, settings_names.get(file_name, list()))
            continue

        settings_save(file_name, settings_names.get(file_name, dict()))

    # -------------------------------
    # Romms config
    # -------------------------------

    for langue in translation_room.keys():

        if os.path.exists(f"{asc_settings_path}{room_config_file}_{langue.lower()}.ini"):
            continue

        if langue not in dict_langues:
            room_file = f"{room_config_file}_en"
        else:
            room_file = f"{room_config_file}_{langue}"

        room_config = get_room_defaut_dict(langue=langue)

        if not isinstance(room_config, dict):
            print("tools -- settings_conversion -- langue not in room_config_files")
            continue

        if len(room_config) != translation_room_count:
            print("tools -- settings_conversion -- langue not in room_config_files")
            continue

        settings_save(room_file, room_config)


def settings_read(file_name: str) -> dict:
    json_file_path = f"{asc_settings_path}{file_name}.ini"

    default_dict = settings_names.get(file_name, dict())

    if not isinstance(default_dict, dict):
        return dict()

    default_dict = dict(default_dict)

    if not os.path.exists(json_file_path):
        return default_dict

    try:

        with open(json_file_path, 'r', encoding="Utf-8") as file:

            config: dict = json.load(file)

    except Exception as erreur:
        print(f"outils -- lecture_settings -- {erreur}")
        return default_dict

    if not isinstance(config, dict):
        print(f"outils -- lecture_settings -- not isinstance(config, dict)")
        return default_dict

    for key, value in config.items():

        if key not in default_dict:
            default_dict[key] = value
            continue

        value_default = default_dict.get(key)

        if not isinstance(value, type(value_default)):
            continue

        default_dict[key] = value

    return default_dict


def settings_list(file_name: str, ele_add=None, ele_del=None) -> list:
    json_file_path = f"{asc_settings_path}{file_name}.ini"

    try:

        with open(json_file_path, 'r', encoding="Utf-8") as file:

            config: list = json.load(file)

    except Exception as erreur:
        print(f"outils -- lecture_settings -- {erreur}")
        return list()

    if not isinstance(config, list):
        return list()

    if ele_add is not None:

        if ele_add in config:
            return config

        config.append(ele_add)
        settings_save(file_name, config)
        return config

    if ele_del is not None:

        if ele_del not in config:
            return config

        config.remove(ele_del)
        settings_save(file_name, config)
        return config

    return config


def settings_get(file_name: str, info_name):
    config = settings_read(file_name)
    return config.get(info_name, None)


def settings_save(file_name: str, config_datas: Union[dict, tuple, list]) -> bool:
    json_file_path = f"{asc_settings_path}{file_name}.ini"

    if asc_settings_path == "" or file_name == "":
        return False

    if os.path.exists(json_file_path):
        make_backup(chemin_dossier=asc_settings_path, fichier=file_name, extension=".ini",
                    dossier_sauvegarde=f"{asc_settings_path}backup\\", nouveau=False, nb_sauvegardes=5)

    try:

        with open(json_file_path, 'w', encoding="Utf-8") as file:

            json.dump(config_datas, file, ensure_ascii=False, indent=2)

            return True

    except Exception as error:
        print(f"outils -- settings_save -- {error}")
        return False


def settings_save_value(file_name: str, key_name: str, value):
    datas = settings_read(file_name)

    if key_name not in datas:
        return

    datas[key_name] = value

    settings_save(file_name, datas)


def a___________________model_______________():
    pass


def model_verification(liste_contenus: list, detail: bool) -> list:
    liste_numero = list()

    for numero in liste_contenus:

        try:
            numero = str(int(numero))
        except Exception:
            pass

        if numero in liste_numero:
            continue

        liste_numero.append(numero)

        if detail:
            if numero in attribute_val_default_layer:
                for key in attribute_val_default_layer:
                    if key not in liste_numero:
                        liste_numero.append(key)

            elif numero in attribute_val_default_fill:
                for key in attribute_val_default_fill:
                    if key not in liste_numero:
                        liste_numero.append(key)

            elif numero in attribute_val_default_room:
                for key in attribute_val_default_room:
                    if key not in liste_numero:
                        liste_numero.append(key)
    try:
        liste_numero.sort(key=int)
    except Exception:
        return list()

    liste_finale = [numero for numero in liste_attributs_ordre if numero in liste_numero]
    liste_finale += [numero for numero in liste_numero if numero not in liste_finale]

    return liste_finale


def a___________________favorite_______________():
    pass


def favorites_import_verification(file_path: str) -> bool:
    if not isinstance(file_path, str):
        return False

    if not file_path.lower().endswith(".csv"):
        return False

    if not os.path.exists(file_path):
        return False

    contenu = load_csv(file_path)

    liste_contenus = convert_list_attribute_number(contenu)

    return len(liste_contenus) != 0


def convert_list_attribute_number(number_list: list) -> list:
    number_list_new = list()

    if not isinstance(number_list, list):
        return number_list_new

    if len(number_list) == 0:
        return number_list_new

    for number in number_list:

        try:
            number = str(int(number))
        except Exception:
            continue

        if number in number_list_new:
            continue

        if len(number) > 5:
            continue

        number_list_new.append(number)

    number_list_new.sort(key=int)

    return number_list_new


def a___________________csv_______________():
    pass


def load_csv(csv_file_path: str, duplicate=False) -> list:
    """
    Permet de charger les fichiers des attributs que j'ai créé
    :param csv_file_path: chemin de fichier
    :param duplicate: accepter les doublons (bool)
    :return: Liste des attributs de la famille
    :rtype: list
    """

    content = read_file_to_text(file_path=csv_file_path)

    if content == "":
        return list()

    if "," in content:
        content_splitted = content.split(", ")

        if duplicate:
            return content_splitted

        content_splitted = list(OrderedDict.fromkeys(content))
        return content_splitted

    if len(content) > 0:
        return [content]

    return list()


def a___________________zt_______________():
    pass


def read_zt_file(file_path: str, title_datas: dict) -> bool:
    if not os.path.exists(file_path):
        return False

    content = read_file_to_text(file_path=file_path)

    matches = re.findall(r"(?<!-)\b(\d+):(\D+)", content)

    if len(matches) == 0:
        return False

    for number_str, desc in matches:

        if not isinstance(number_str, str) or not isinstance(desc, str):
            print("tools -- read_zt_file -- not isinstance(number_str, str)")
            continue

        # --------------

        desc = desc.strip()

        if desc == "":
            continue

        # --------------

        try:
            number_int = int(number_str)
        except Exception:
            print("tools -- read_zt_file -- not number_str.isnumeric()")
            continue

        if number_int < 1 or number_int > 999:
            continue

        # --------------

        number_str = number_str.zfill(3)

        title_datas[f"{number_int}"] = f"{number_str} -- {desc}"

    return True


def a___________________gestion_infos_catalogue_______________():
    pass


def get_catalog_setting_folder(catalog_folder: str) -> str:
    """
    Find the path of the catalog settings folder. if old folder -> rename / if not exist -> create
    :param catalog_folder: path of the catalog
    :return: catalog_settings_folder (str)
    """

    # Define the path of the settings folder
    catalog_settings_folder = f"{catalog_folder}ASC_settings\\"

    # if the path exist -> return the path -> Ok
    if os.path.exists(catalog_settings_folder):
        return catalog_settings_folder

    # Define the old folder
    catalog_settings_folder_old = f"{catalog_folder}Sauvegarde_affichage\\"

    if not os.path.exists(catalog_folder):

        try:

            os.mkdir(catalog_folder)
            os.mkdir(catalog_settings_folder)

        except Exception as error:
            print(f"tool -- get_catalog_setting_folder -- erreur création dossier SmartCatalog --> {error}")
            return ""

        return catalog_settings_folder

    # if the path existe -> try rename it -> return the path -> Ok
    if os.path.exists(catalog_settings_folder_old):

        try:

            os.rename(catalog_settings_folder_old, catalog_settings_folder)

            return catalog_settings_folder

        except Exception as error:

            print(f"tool -- get_catalog_setting_folder -- erreur renommer dossier --> {error}")

            return ""

    # if the folder doesn't existe, try create -> return the path -> Ok
    try:

        os.mkdir(catalog_settings_folder)

        return catalog_settings_folder

    except Exception as error:

        print(f"tool -- get_catalog_setting_folder -- erreur création dossier --> {error}")

        return ""


def get_catalog_setting_path_file(catalog_settings_folder: str, catalog_name: str) -> str:
    """
    find the path of the file CatalogName_path.ini. if old path -> rename
    :param catalog_settings_folder: path of the settings folder
    :param catalog_name: the name of catalog
    :return: catalog_setting_path_file (str)
    """

    # Define the path of the file :  CatalogName_path.ini
    catalog_setting_path_file = f"{catalog_settings_folder}{catalog_name}_path.ini"

    # if the path existe -> return path -> Ok
    if os.path.exists(catalog_setting_path_file):
        return catalog_setting_path_file

    # if the setting folder doesn't existe -> error
    if not os.path.exists(catalog_settings_folder):
        return ""

    # if the name of catalog is empty -> error
    if not catalog_name:
        return ""

    # -----------------------
    # Define the old path
    # -----------------------

    catalog_setting_path_file_old = f"{catalog_settings_folder}chemin_{catalog_name}.ini"

    # if the old path existe -> try renamme it -> return the path -> Ok
    if os.path.exists(catalog_setting_path_file_old):
        try:

            os.rename(catalog_setting_path_file_old, catalog_setting_path_file)

        except Exception as erreur:
            print(f"catalog_manage -- charger_fichier_ini -- erreur renommer dossier --> {erreur}")
            return ""

    # -----------------------
    # Define the old path (backup)
    # -----------------------

    catalog_setting_path_file_old = f"{catalog_settings_folder}chemin_{catalog_name}.bak"

    # if the old path existe -> try renamme it -> return the path -> Ok
    if os.path.exists(catalog_setting_path_file_old):
        try:

            os.rename(catalog_setting_path_file_old, f"{catalog_settings_folder}{catalog_name}_path.bak")

        except Exception:
            pass

    # return the path -> Ok
    return catalog_setting_path_file


def get_catalog_setting_display_file(catalog_settings_folder: str, catalog_name: str) -> str:
    """

    :param catalog_settings_folder:
    :param catalog_name:
    :return:
    """

    # Define the path of the file :  CatalogName_display.ini
    catalog_setting_display_file = f"{catalog_settings_folder}{catalog_name}_display.xml"

    # if the path existe -> return path -> Ok
    if os.path.exists(catalog_setting_display_file):
        return catalog_setting_display_file

    # if the setting folder doesn't existe -> error
    if not os.path.exists(catalog_settings_folder):
        return ""

    # if the name of catalog is empty -> error
    if not catalog_name:
        return ""

    # -----------------------
    # Define the old path
    # -----------------------

    catalog_setting_display_file_old = f"{catalog_settings_folder}affichage_{catalog_name}.xml"

    # if the old path existe -> try renamme it -> return the path -> Ok
    if os.path.exists(catalog_setting_display_file_old):
        try:

            os.rename(catalog_setting_display_file_old, catalog_setting_display_file)

        except Exception as erreur:
            print(f"tool -- catalog_display_find_path -- erreur renommer fichier --> {erreur}")
            return ""

    # -----------------------
    # Define the old path (backup)
    # -----------------------

    catalog_setting_display_file_old = f"{catalog_settings_folder}affichage_{catalog_name}.bak"

    # if the old path existe -> try renamme it -> return the path -> Ok
    if os.path.exists(catalog_setting_display_file_old):
        try:

            os.rename(catalog_setting_display_file_old, f"{catalog_settings_folder}affichage_{catalog_name}.bak")

        except Exception:
            pass

    # return the path -> Ok
    return catalog_setting_display_file


def a___________________catalog_setting_file_paths_______________():
    pass


def read_catalog_paths_file(catalog_setting_path_file: str,
                            folder_std: str,
                            folder_prj: str,
                            allplan_version_default: str,
                            allplan_version_list: list) -> dict:
    """
    read / convert / create (if not exist) the catalog setting file : CatalogName_path.ini
    :param catalog_setting_path_file: The path of the catalog settings file
    :param folder_std: The path of the user data folder
    :param folder_prj: the path of prj folder
    :param allplan_version_default: The Allplan version to use
    :param allplan_version_list: List of installed versions

    :return: dict["user_data_path", "allplan_version"]
    """

    user_data_path = folder_std
    allplan_version = allplan_version_default
    attribute_default = attribute_default_base

    # ----------

    # if catalog_setting_path_file is empty -> return default
    if catalog_setting_path_file == "":
        return {"user_data_path": user_data_path,
                "allplan_version": allplan_version,
                "attribute_default": attribute_default}

    # ----------

    # The file doesn't existe -> creation setting + return default
    if not os.path.exists(catalog_setting_path_file):
        write_catalog_paths_file(catalog_setting_path_file=catalog_setting_path_file,
                                 user_data_path=user_data_path,
                                 allplan_version=allplan_version,
                                 attribute_default=attribute_default)
        return {"user_data_path": user_data_path,
                "allplan_version": allplan_version,
                "attribute_default": attribute_default}

    try:

        # ----------------
        # Load json file
        # ----------------

        with open(catalog_setting_path_file, "r", encoding="utf-8") as file:

            lines_list = json.load(file)

            if isinstance(lines_list, dict):

                # define new path
                user_data_path = check_user_datas_path(user_data_path=lines_list.get("user_data_path", ""),
                                                       folder_std=folder_std,
                                                       folder_prj=folder_prj)
                # ----------------
                # define new version

                version_allplan_new = lines_list.get("allplan_version", attribute_default_base)

                # ----------------

                # Check if version is installed
                if version_allplan_new in allplan_version_list:
                    allplan_version = version_allplan_new

                # ----------------

                attribute_default = attribut_default_obj.check_number(lines_list.get("attribute_default"))

                # ----------------

                return {"user_data_path": user_data_path,
                        "allplan_version": allplan_version,
                        "attribute_default": attribute_default}

    except Exception:
        pass

    lines_list = read_file_to_list(file_path=catalog_setting_path_file)

    # ----------

    # Check if len datas_new <2 -> creation new setting file + return default settings

    if len(lines_list) < 2:
        write_catalog_paths_file(catalog_setting_path_file=catalog_setting_path_file,
                                 user_data_path=user_data_path,
                                 allplan_version=allplan_version,
                                 attribute_default=attribute_default)

        return {"user_data_path": user_data_path,
                "allplan_version": allplan_version,
                "attribute_default": attribute_default}

    user_data_path = check_user_datas_path(user_data_path=lines_list[0].strip(),
                                           folder_std=folder_std,
                                           folder_prj=folder_prj)

    # ----------

    # define new version
    version_allplan_new = lines_list[1].strip()

    # ----------

    # Check if version is installed
    if version_allplan_new and version_allplan_new in allplan_version_list:
        # Remplace default value by new value
        allplan_version = version_allplan_new

    # ----------

    # Update file to json
    write_catalog_paths_file(catalog_setting_path_file=catalog_setting_path_file,
                             user_data_path=user_data_path,
                             allplan_version=allplan_version,
                             attribute_default=attribute_default)

    return {"user_data_path": user_data_path,
            "allplan_version": allplan_version,
            "attribute_default": attribute_default}


def check_user_datas_path(user_data_path: str, folder_std: str, folder_prj: str) -> str:
    """
    Check if the user datas path is valid.
    :param user_data_path: current path
    :param folder_std: the path of the STD folder
    :param folder_prj: the path of the PRJ folder
    :return: the path ot user datas (str)
    """

    # if the path exists and the path is a folder -> return path
    if os.path.exists(user_data_path) and os.path.isdir(user_data_path):
        return user_data_path

    # if STD in the path -> return the path of the STD folder
    if "\\STD\\" in user_data_path.upper():
        return folder_std

    # Try to find the name of prj. -> if error return the path of the STD folder
    try:
        prj_name = os.path.basename(os.path.normpath(user_data_path)).lower()

    except Exception:
        return folder_std

    # Check if the end of the project's name != ".prj" -> return the path of the STD folder
    if not prj_name.endswith(".prj"):
        return folder_prj

    # Define the new path in the current PRJ folder.
    prj_path = f"{folder_prj}{prj_name}"

    # if the new path not exist -> return the path of the STD folder
    if not os.path.exists(prj_path):
        return folder_std

    # Check if the path is a folder -> return the path
    if os.path.isdir(prj_path):
        return prj_path

    # Find the real path for the file ".prj" (apn)
    prj_path = get_real_path_of_apn_file(file_path=prj_path, prj_path=folder_prj, show_msg=False)

    # If success -> return the path
    if prj_path:
        return prj_path

    # No success -> return the path of the STD folder
    return folder_std


def write_catalog_paths_file(catalog_setting_path_file: str, user_data_path: str, allplan_version: str,
                             attribute_default: str) -> bool:
    if os.path.exists(catalog_setting_path_file):

        catalog_settings_folder = find_folder_path(catalog_setting_path_file)
        setting_filename = find_filename(catalog_setting_path_file)

        if catalog_settings_folder == "" or setting_filename == "":
            return False

        make_backup(chemin_dossier=catalog_settings_folder,
                    fichier=setting_filename,
                    extension=".ini",
                    dossier_sauvegarde=f"{catalog_settings_folder}backup\\",
                    nouveau=True)

    # --------------

    if not isinstance(user_data_path, str):
        print(f"tools -- write_catalog_paths_file -- not isinstance(user_data_path, str)")
        return False

    if not isinstance(allplan_version, str):
        print(f"tools -- write_catalog_paths_file -- not isinstance(allplan_version, str)")
        return False

    attribute_default = attribut_default_obj.check_number(number=attribute_default)

    datas = {"user_data_path": user_data_path,
             "allplan_version": allplan_version,
             "attribute_default": attribute_default}

    # --------------

    try:

        with open(catalog_setting_path_file, 'w', encoding="Utf-8") as file:

            json.dump(datas, file, ensure_ascii=False, indent=2)
            return True

    except Exception as error:
        print(f"outils -- write_catalog_paths_file -- {error}")
        return False


def a___________________gestion_apparence_______________():
    pass


def changer_selection_apparence(widget: QWidget):
    """Permet de changer l'apparence"""

    pal: QPalette = widget.palette()
    pal.setColor(QPalette.Inactive, QPalette.Highlight, pal.color(QPalette.Highlight))
    pal.setColor(QPalette.Inactive, QPalette.HighlightedText, pal.color(QPalette.HighlightedText))

    font = widget.font()
    font.setPointSize(taille_police)
    widget.setFont(font)

    widget.setPalette(pal)

    return pal


def changer_apparence_selection(widget: QWidget):
    """Permet de changer l'apparence"""

    pal: QPalette = widget.palette()
    pal.setColor(QPalette.Inactive, QPalette.Highlight, QColor("#BAD0E7"))
    pal.setColor(QPalette.Active, QPalette.Highlight, QColor("#BAD0E7"))
    pal.setColor(QPalette.Active, QPalette.HighlightedText, QColor("#000000"))
    widget.setPalette(pal)

    return


def get_look_widget(widget: QWidget):
    """Permet de changer l'apparence"""

    pal: QPalette = widget.palette()
    pal.setColor(QPalette.Inactive, QPalette.Highlight, pal.color(QPalette.Highlight))
    pal.setColor(QPalette.Inactive, QPalette.HighlightedText, pal.color(QPalette.HighlightedText))
    widget.setPalette(pal)

    changer_police(widget, taille_police)

    return pal


def get_look_tableview(widget: QWidget):
    """Permet de changer l'apparence"""
    changer_apparence_selection(widget)
    changer_police(widget, taille_police)
    return


def get_look_treeview(widget: QWidget):
    """Permet de changer l'apparence"""
    changer_apparence_selection(widget)
    changer_police(widget, taille_police)
    return


def changer_police(widget: QWidget, taille: int):
    font = widget.font()
    font.setFamily("Segoe UI")
    font.setPointSize(taille)
    widget.setFont(font)
    return


def qstandarditem_font(bold=False, italic=False):
    font = QStandardItem().font()
    font.setFamily("Segoe UI")
    font.setPointSize(taille_police)

    if bold:
        font.setBold(True)

    if italic:
        font.setItalic(True)

    return font


def get_look_qs(qs: QStandardItem, bold=False, italic=False):
    font = qs.font()
    font.setFamily("Segoe UI")
    font.setPointSize(taille_police)

    if bold:
        font.setBold(True)

    if italic:
        font.setItalic(True)

    qs.setFont(font)

    return qs


def selectionner_parentheses(widget: QPlainTextEdit):
    if isinstance(widget, QPlainTextEdit):
        cursor = widget.textCursor()
        texte_selectionner = cursor.selectedText()

    else:
        return

    if cursor.selectionStart() < cursor.position():
        deduction = -1
    else:
        deduction = 0

    position_actuelle = widget.textCursor().position() + deduction
    position_finale = -1

    format_txt_original = QTextCharFormat()
    format_txt_original.clearBackground()

    widget.blockSignals(True)

    cursor.select(QTextCursor.Document)
    cursor.setCharFormat(format_txt_original)

    cursor.setPosition(position_actuelle)
    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)

    widget.blockSignals(False)

    if texte_selectionner != "(" and texte_selectionner != ")":
        return

    parentheses_indices = recherche_position_parentheses(widget.toPlainText())

    if len(parentheses_indices) == 0:
        return

    for open_idx, close_idx in parentheses_indices:

        if position_actuelle != open_idx and position_actuelle != close_idx:
            continue

        if position_actuelle == open_idx:
            position_finale = close_idx
        else:
            position_finale = open_idx

        break

    if position_finale == -1 or position_actuelle == position_finale:
        return

    format_txt = QTextCharFormat()
    format_txt.setBackground(QColor(0, 120, 215))

    widget.blockSignals(True)

    cursor.setPosition(position_finale)

    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)

    cursor.mergeCharFormat(format_txt)

    cursor.setPosition(position_actuelle)

    widget.blockSignals(False)


def set_appareance_button(widget: QWidget):
    """Permet de changer l'apparence"""

    pal: QPalette = widget.palette()
    pal.setColor(QPalette.Active, QPalette.Highlight, QColor(Qt.darkBlue))
    widget.setPalette(pal)
    return


def get_look_combobox(widget: QComboBox):
    if not isinstance(widget, QComboBox):
        return

    pal = widget.palette()
    pal.setColor(QPalette.Inactive, QPalette.Highlight, QColor("#BAD0E7"))
    pal.setColor(QPalette.Active, QPalette.Highlight, QColor("#BAD0E7"))
    pal.setColor(QPalette.Active, QPalette.HighlightedText, QColor("#000000"))
    pal.setColor(QPalette.Active, QPalette.Background, QColor("#FFFFFF"))
    widget.setPalette(pal)

    lineedit = widget.lineEdit()

    if isinstance(lineedit, QLineEdit):
        font = lineedit.font()
        font.setFamily("Segoe UI")
        font.setPointSize(10)

        lineedit.setFont(font)

    view = widget.view()

    if isinstance(view, QListView):
        pal: QPalette = view.palette()
        pal.setColor(QPalette.Inactive, QPalette.Highlight, QColor("#BAD0E7"))
        pal.setColor(QPalette.Active, QPalette.Highlight, QColor("#BAD0E7"))
        pal.setColor(QPalette.Active, QPalette.HighlightedText, QColor("#000000"))
        pal.setColor(QPalette.Active, QPalette.Background, QColor("#FFFFFF"))
        view.setPalette(pal)


def find_global_point(widget: QWidget) -> QPoint:
    global_point = widget.mapToGlobal(QPoint(0, 0))

    point = QPoint(global_point.x(), global_point.y() + widget.height())

    return point


def move_widget_ss_bouton(button: QWidget, widget: QWidget, left_force=False):
    # --------------------
    # Button's Information
    # --------------------

    button_position = button.mapToGlobal(QPoint(0, 0))

    button_width = button.width()
    buttom_height = button.height()

    button_pos_x = button_position.x()
    button_pos_y = button_position.y()

    button_end_x = button_pos_x + button_width
    button_end_y = button_pos_y + buttom_height

    # --------------------
    #  Widget's Information
    # --------------------

    widget_with = widget.width()
    widget_height = widget.height()

    # --------------------
    # Screen's information
    # --------------------

    screennumber = QApplication.desktop().screenNumber(button)
    screen: QRect = QApplication.desktop().availableGeometry(screennumber)

    screen_width = screen.width()
    screen_height = screen.height()

    screen_pos_x = screen.x()
    screen_pos_y = screen.y()

    screen_end_x = screen_pos_x + screen_width
    screen_end_y = screen_pos_y + screen_height

    # --------------------
    # Screen's information
    # --------------------

    popup_pos_x = button_pos_x
    popup_pos_y = button_end_y

    popup_end_x = popup_pos_x + widget_with
    popup_end_y = popup_pos_y + widget_height

    if popup_end_x > screen_end_x or left_force:
        popup_pos_x = button_end_x - widget_with

    if popup_end_y > screen_end_y:
        popup_pos_y = button_pos_y - widget_height

    widget.move(popup_pos_x, popup_pos_y)


def titre_menu_deroulant(parent, texte: str):
    """
    Permet de créer un titre dans le menu déroulant
    :param parent: parent
    :param texte: texte à afficher
    :return: QAction
    """

    action_widget = QWidgetAction(parent)
    action_widget.setEnabled(False)
    action_widget.setIconVisibleInMenu(False)

    if not texte.startswith("<b>"):
        texte = f"<b> ---  {texte}  --- "
    else:
        texte = f" ---  {texte}  --- "

    label = QLabel(texte)

    font_w = label.font()
    font_w.setPointSize(taille_police_menu)
    label.setFont(font_w)

    label.setAlignment(Qt.AlignCenter)
    label.setFixedHeight(menu_ht_ligne)
    label.setMinimumWidth(300)

    label.setStyleSheet("background: #CFD7DC; color: #4D4D4D; border: 1px solid #C4C4C4")

    action_widget.setDefaultWidget(label)

    return action_widget


def get_lastest_used(current_list: list):
    liste = list()

    for chemin in reversed(current_list):

        if chemin not in liste:
            liste.append(chemin)

        if len(liste) == 10:
            break

    liste.sort()
    return liste


def get_most_used(current_list: list):
    occurrences = Counter(current_list)

    chemins_tries = sorted(occurrences, key=occurrences.get, reverse=True)

    nombre_max_chemins = min(10, len(chemins_tries))

    chemins_plus_utilises = chemins_tries[:nombre_max_chemins]

    chemins_plus_utilises.sort()

    return chemins_plus_utilises


def get_image_dimensions(image_path, message=True):
    try:
        file_size = os.path.getsize(image_path)

        if file_size <= 10000:
            return True

        if message:
            a = QCoreApplication.translate("tools", "La taille de l'icône choisie est supérieure à 10 ko")
            b = QCoreApplication.translate("tools", "Veuillez choisir une icône plus petite")

            afficher_message(titre=application_title,
                             message=f"{a}.\n{b}.")
        return False

    except IOError:

        if message:
            afficher_message(titre=application_title,
                             message=QCoreApplication.translate(
                                 "tools", "La recherche du poids de l'image a échouée, désolé."))
        return False


def set_appearance_number(widget_numero: QLabel):
    numero_str = widget_numero.text()

    try:
        numero = int(numero_str)

        if 1999 < numero < 12000:
            widget_numero.setToolTip(QCoreApplication.translate("tools", "Attribut utilisateur"))

            widget_numero.setStyleSheet("QLabel{border: 2px solid #416596;"
                                        "border-radius: 5px; "
                                        "color: #416596;"
                                        "background-color:#c4ffc4;}")

            return

        if 55000 <= numero < 99000:
            widget_numero.setToolTip(QCoreApplication.translate("tools", "Attribut Import"))

            widget_numero.setStyleSheet("QLabel{border: 2px solid #416596;"
                                        "border-radius: 5px; "
                                        "color: #416596;"
                                        "background-color:#c4ffc4;}")

            return

        if numero >= 99000:
            widget_numero.setToolTip(QCoreApplication.translate("tools", "Attribut inconnu"))

            widget_numero.setStyleSheet("QLabel{border: 2px solid #416596;"
                                        "border-radius: 5px; "
                                        "color: #416596;"
                                        "background-color:#f0be82;}")

            return

    except ValueError:
        pass

    widget_numero.setToolTip(QCoreApplication.translate("tools", "Attribut Allplan"))

    widget_numero.setStyleSheet("QLabel{border: 2px solid #416596; border-radius: 5px; color: #416596}")


def set_appearence_type(bt_type: QPushButton, attrib_option: str):
    if "Nombre entier" in attrib_option:
        bt_type.setText("123")
        bt_type.setToolTip(QCoreApplication.translate("tools", "Nombre entier"))
        return

    if "Nombre décimal" in attrib_option:
        bt_type.setText("0,0")
        bt_type.setToolTip(QCoreApplication.translate("tools", "Nombre décimal"))
        return

    bt_type.setText("ABC")
    bt_type.setToolTip(QCoreApplication.translate("tools", "Texte"))


def move_window_tool(widget_parent: QWidget, widget_current: QWidget, always_center=False):
    if not isinstance(widget_parent, QWidget) or not isinstance(widget_current, QWidget):
        return False

    screennumber = QApplication.desktop().screenNumber(widget_parent)

    screen: QRect = QApplication.desktop().availableGeometry(screennumber)

    screenwidth, screenheight = screen.width(), screen.height()

    dialogwidth, dialogweight = widget_current.width(), widget_current.height()

    if dialogwidth > screenwidth and dialogweight > screenheight:
        widget_current.resize(int(screenwidth * 0.9), int(screenheight * 0.9))

    elif dialogwidth > screenwidth:
        widget_current.resize(int(screenwidth * 0.9), widget_current.height())

    elif dialogweight > screenheight:
        widget_current.resize(widget_current.width(), int(screenheight * 0.9))

    if hasattr(widget_current, 'ismaximized_on') and widget_current.ismaximized_on:
        widget_current.move(screen.x(), 0)
        return

    pos_x = widget_current.x()
    pos_x_end = widget_current.x() + widget_current.width()

    screen_x_fin = screen.x() + screen.width()

    pos_y = widget_current.y()
    pos_y_end = widget_current.y() + widget_current.height()

    screen_y_end = screen.y() + screen.height()

    if pos_x <= screen.x() or pos_x_end > screen_x_fin or pos_y <= screen.y() or pos_y_end > screen_y_end:
        qp = screen.center()
        qr = widget_current.frameGeometry()
        widget_current.move(QPoint(qp.x() - int(qr.width() / 2), qp.y() - int(qr.height() / 2)))
        return

    if always_center and widget_parent != widget_current:
        qr = widget_current.frameGeometry()
        qr.moveCenter(widget_parent.frameGeometry().center())
        widget_current.move(qr.topLeft())


def a___________________gestions_registre_______________():
    pass


def registry_find_value(path: str, name: str, key=winreg.HKEY_LOCAL_MACHINE) -> str:
    """
    find in regsitry
    :param path: path in registry
    :param name: name of key
    :return: value of name or ""
    """

    try:
        key = winreg.OpenKey(key, path)
        value, _ = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return value

    except Exception:
        pass

    except FileNotFoundError:
        pass

    # -----------------------------------------

    try:
        key = winreg.OpenKey(key, path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return value

    except Exception:
        pass

    except FileNotFoundError:
        pass

    # -----------------------------------------

    bitness = platform.architecture()[0]
    if bitness == '32bit':
        other_view_flag = winreg.KEY_WOW64_64KEY
    else:
        other_view_flag = winreg.KEY_WOW64_32KEY

    try:
        key = winreg.OpenKey(key, path, access=winreg.KEY_READ | other_view_flag)
        value, _ = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return value

    except Exception:
        return ""

    except FileNotFoundError:
        return ""


def convertir_langue(lg: str) -> str:
    if lg in language_title:
        return lg

    for language, title in language_title.items():

        if lg.upper() == language.upper():
            return language

        if lg.upper() == title.upper():
            return language

    return "EN"


def a___________________gestions_ouvrir_______________():
    pass


def open_file(file_path) -> bool:
    if file_path is None:
        print("tools -- open_file -- chemin_fichier is None")
        return False

    if not os.path.exists(file_path):
        a = QCoreApplication.translate("tools", "Le fichier")
        b = QCoreApplication.translate("tools", "n'existe pas, impossible de l'ouvrir, désolé")

        afficher_message(titre=application_name,
                         message=f"{a} {file_path} {b}")
        return False

    try:
        subprocess.Popen(['cmd', '/c', 'start', '', file_path], shell=True)
        return True

    except Exception as error:
        print(f"tools -- open_file -- error : {error}")
        return False


def open_folder(folder_path: str) -> bool:
    if folder_path is None:
        print("tools -- open_folder -- folder_path is None")
        return False

    if folder_path == "":
        afficher_message(titre=application_name,
                         message=QCoreApplication.translate(
                             "outils", "Aucun chemin défini."))
        return False

    if not os.path.exists(folder_path):
        a = QCoreApplication.translate("tools", "Le dossier")
        b = QCoreApplication.translate("tools", "n'existe pas, impossible de l'ouvrir, désolé")

        afficher_message(titre=application_name,
                         message=f"{a} : {folder_path} {b}",
                         details=f"folder_path : {folder_path}")
        return False

    if folder_path.endswith("\\"):
        folder_path = folder_path[:-1]

    subprocess.Popen(["explorer", folder_path])
    return True


def find_folder_path(file_path: str) -> str:
    if not isinstance(file_path, str):
        return ""

    try:
        if os.path.exists(file_path):

            if os.path.isfile(file_path):
                file_path: str = os.path.dirname(file_path)

        else:

            if not file_path.endswith("\\"):

                extensions = ['.xml', '.csv', '.xlsx', '.dbf', '.surf', '.png', ".jpg", ".jff", ".jtf", ".jpeg", ".tif",
                              ".tga", ".bmp", ".mac", ".msp", ".pcd", ".pct", ".pcx", ".png", ".psd", ".ras", ".wmf",
                              ".apn", ".kat", "fic"] + list(get_favorites_allplan_dict())

                for extension in extensions:
                    if file_path.endswith(extension):
                        file_path: str = os.path.dirname(file_path)
                        break

        file_path = file_path.replace("/", "\\")

        if not file_path.endswith("\\"):
            file_path += "\\"

        if file_path == "\\":
            return ""

        return file_path

    except Exception:
        return ""


def find_filename(file_path: str, with_ext=False) -> str:
    try:
        filename_with_extension = os.path.basename(file_path)

        if os.path.isdir(file_path):
            return ""

        if with_ext:
            return filename_with_extension

        filename_without_extension, _ = os.path.splitext(filename_with_extension)

        return filename_without_extension

    except Exception:
        return ""


# def browser_file(parent: QObject, title: str, datas_filters: dict, registry: list, current_path="", default_path="",
#                  file_name="", use_setting_first=True, use_save=False) -> str:
#     """
#
#     :param parent: Objet parent
#     :param title: Titre de la boite de dialogue
#     :param datas_filters: datas_filtre = {"Images" : [".png", ".jpg"], "Pdf" : [".pdf"]}
#     :param registry: Nom de l'élément dans la base de registre
#     :param current_path: chemin actuel de l'élément
#     :param default_path: chemin par défaut
#     :param file_name: nom_fichier
#     :param use_setting_first: "setting" = recherche dans le registre + actuel + défaut // actuel + setting + defaut ""
#     :param use_save: bool : pour choisir un fichier existant
#     :return: chemin du fichier ou ""
#     """
#
#     if not isinstance(current_path, str):
#         return ""
#
#     dossier_actuel = find_folder_path(current_path)
#
#     dossier_defaut = find_folder_path(default_path)
#
#     if len(registry) != 2:
#         dossier_settings = dossier_defaut
#     else:
#         dossier_settings = settings_get(registry[0], registry[1])
#
#         if dossier_settings is None:
#             dossier_settings = dossier_defaut
#
#     dossier_cible = ""
#
#     if not use_setting_first:
#
#         if dossier_actuel != "" and dossier_actuel != "\\" and os.path.exists(dossier_actuel):
#
#             dossier_cible = f"{dossier_actuel}{file_name}"
#
#         else:
#
#             if dossier_settings != "" and dossier_settings != "\\" and os.path.exists(dossier_settings):
#
#                 dossier_cible = f"{dossier_settings}{file_name}"
#
#             else:
#
#                 if dossier_defaut != "" and dossier_defaut != "\\" and os.path.exists(dossier_defaut):
#                     dossier_cible = f"{dossier_defaut}{file_name}"
#
#     else:
#
#         if dossier_settings != "" and dossier_settings != "\\" and os.path.exists(dossier_settings):
#
#             dossier_cible = f"{dossier_settings}{file_name}"
#
#         else:
#
#             if dossier_actuel != "" and dossier_actuel != "\\" and os.path.exists(dossier_actuel):
#
#                 dossier_cible = f"{dossier_actuel}{file_name}"
#
#             else:
#
#                 if dossier_defaut != "" and dossier_defaut != "\\" and os.path.exists(dossier_defaut):
#                     dossier_cible = f"{dossier_defaut}{file_name}"
#
#     liste_extensions = list()
#     les_filtres = list()
#
#     accepter_tous = False
#
#     for titre_filtre, extensions in datas_filters.items():
#
#         if not accepter_tous:
#
#             for extension in extensions:
#
#                 if extension == ".*":
#                     accepter_tous = True
#                     liste_extensions.clear()
#                     break
#
#                 if extension in liste_extensions:
#                     continue
#
#                 liste_extensions.append(extension)
#
#         extensions: list
#         ensemble = f'*{" *".join(extensions)}'
#         les_filtres.append(f'{titre_filtre} ({ensemble})')
#
#     filtre = ";;".join(les_filtres)
#
#     if not use_save:
#
#         chemin_fichier, _filter = QFileDialog.getOpenFileName(parent=parent,
#                                                               caption=title,
#                                                               directory=dossier_cible,
#                                                               filter=filtre)
#     else:
#
#         chemin_fichier, _filter = QFileDialog.getSaveFileName(parent=parent,
#                                                               caption=title,
#                                                               directory=dossier_cible,
#                                                               filter=filtre)
#     if chemin_fichier is None:
#         return ""
#
#     if chemin_fichier == "":
#         return ""
#
#     dossier_actuel = find_folder_path(chemin_fichier)
#
#     if dossier_actuel != "" and dossier_actuel != "\\":
#         if len(registry) == 2:
#             settings_save_value(registry[0], registry[1], dossier_actuel)
#
#     chemin_fichier: str = chemin_fichier.replace("/", "\\")
#
#     if accepter_tous:
#         return chemin_fichier
#
#     if use_save:
#
#         if len(liste_extensions) == 0:
#             return chemin_fichier
#
#         extension_actuelle = liste_extensions[0]
#
#         if chemin_fichier.endswith(extension_actuelle):
#             return chemin_fichier
#
#         chemin_fichier += extension_actuelle
#         return chemin_fichier
#
#     for extension in liste_extensions:
#
#         extension: str
#         fichier_upper = chemin_fichier.upper()
#
#         if fichier_upper.endswith(extension.upper()):
#             return chemin_fichier
#
#     afficher_message(titre=parent.tr("Erreur extension de fichier"),
#                      message=parent.tr("L'extension du fichier est non valide !"),
#                      icone_avertissement=True)
#
#     return ""


def parcourir_dossier(parent: QObject, title: str, registry: list, current="", default="",
                      use_setting_first=True) -> str:
    """

    :param parent: Objet parent
    :param title: Titre de la boite de dialogue
    :param registry: Nom de l'élément dans la base de registre
    :param current: chemin actuel de l'élément
    :param default: chemin par défaut
    :param use_setting_first: "setting" = recherche dans le registre + actuel + défaut // actuel + setting + defaut ""
    :return: chemin du fichier ou ""
    """

    if not isinstance(parent, QObject):
        parent = None

    dossier_actuel = find_folder_path(current)

    dossier_defaut = find_folder_path(default)

    if len(registry) != 2:
        dossier_settings = dossier_defaut
    else:
        dossier_settings = settings_get(registry[0], registry[1])

        if dossier_settings is None:
            dossier_settings = dossier_defaut

    dossier_cible = ""

    if not use_setting_first:

        if dossier_actuel != "" and dossier_actuel != "\\" and os.path.exists(dossier_actuel):

            dossier_cible = dossier_actuel

        else:

            if dossier_settings != "" and dossier_settings != "\\" and os.path.exists(dossier_settings):

                dossier_cible = dossier_settings

            else:

                if dossier_defaut != "" and dossier_defaut != "\\" and os.path.exists(dossier_defaut):
                    dossier_cible = dossier_defaut

    else:

        if dossier_settings != "" and dossier_settings != "\\" and os.path.exists(dossier_settings):

            dossier_cible = dossier_settings

        else:

            if dossier_actuel != "" and dossier_actuel != "\\" and os.path.exists(dossier_actuel):

                dossier_cible = dossier_actuel

            else:

                if dossier_defaut != "" and dossier_defaut != "\\" and os.path.exists(dossier_defaut):
                    dossier_cible = dossier_defaut

    dossier = QFileDialog.getExistingDirectory(parent=parent,
                                               caption=title,
                                               directory=dossier_cible)

    if dossier is None:
        return ""

    if dossier == "":
        return ""

    dossier_actuel = find_folder_path(dossier)

    if dossier_actuel != "" and dossier_actuel != "\\":
        if len(registry) == 2:
            settings_save_value(registry[0], registry[1], dossier_actuel)

    return dossier_actuel


def recherche_image(image_name: str, image_default: str):
    if not isinstance(image_name, str):
        if image_default != "":
            return f":/Images/{image_default}"
        return ""

    if image_name.startswith(":/Images/") and not QPixmap(image_name).isNull():
        return image_name

    if os.path.exists(image_name):
        return image_name

    if not QPixmap(f":/Images/{image_name}").isNull():
        return f":/Images/{image_name}"

    file = find_filename(image_name)
    image_default = image_default.lower()

    if file is None or file == "":
        if image_default != "":
            return f":/Images/{image_default}"
        return image_name

    if file in datas_icons:
        file = datas_icons[file]
        return f"{icons_path}{file}.png"

    icon_path = f"{icons_path}{file}.png"

    if os.path.exists(icon_path):
        return icon_path

    icon_path = f"{icons_path}{file}.jpg"

    if os.path.exists(icon_path):
        return icon_path

    icon_path = f"{icons_path}{file}.bmp"

    if os.path.exists(icon_path):
        return icon_path

    if image_default != "":
        return f":/Images/{image_default}.svg"
    return image_name


def customize_folder_name_apply(folder_path: str, display_name: str, hide=False) -> bool:
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("tools -- customize_folder_name_apply -- not os.path.exists(folder_path)")
        return False

    if folder_path.endswith("\\"):
        folder_path = folder_path.rstrip("\\")

    desktop_ini_path = os.path.join(folder_path, "desktop.ini")

    ini_content = f"""[.ShellClassInfo]
    LocalizedResourceName={display_name}
    IconResource={asc_exe_path},0"""

    try:

        with open(desktop_ini_path, "w", encoding="utf-8") as ini_file:
            ini_file.write(ini_content)

        # -------

        subprocess.run(["attrib", "+s", folder_path], check=True)

        # -------

        if not hide:
            return True

        subprocess.run(["attrib", "+h", "+s", desktop_ini_path], check=True)
        return True

    except Exception as error:
        print(f"tools -- customize_folder_name_apply -- error : {error}")

    return False


def customize_folder_name_remove(folder_path: str):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("tools -- customize_folder_name_remove -- not os.path.exists(folder_path)")
        return False

    if folder_path.endswith("\\"):
        folder_path = folder_path.rstrip("\\")

    desktop_ini_path = os.path.join(folder_path, "desktop.ini")

    try:

        subprocess.run(["attrib", "-s", folder_path], check=True)

        if os.path.exists(desktop_ini_path):
            subprocess.run(["attrib", "-s", "-h", desktop_ini_path], check=True)

            os.remove(desktop_ini_path)
            return True

    except Exception as error:
        print(f"tools -- customize_folder_name_remove -- error : {error}")

    return False


def a___________________affichage_messages_______________():
    pass


def afficher_message(titre: str, message: str, infos="", type_bouton=None, defaut_bouton=None,
                     perso=False, bt_ok=str(), bt_no=str(), bt_cancel=True,
                     icone_question=False, icone_avertissement=False, icone_critique=False, icone_valide=False,
                     icone_sauvegarde=False, icone_lock=False, icone_ouvrir=False,
                     details=None, txt_save=str(), afficher_details=False, infos_defaut=None):
    """
    :param titre: Titre de l'information
    :param message: message écrit
    :param infos: type d'infos
    :param type_bouton: QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel | QMessageBox.Save)
    :param defaut_bouton: défini le bouton par défaut
    :param perso: Permet de créer des boutons personnalisés
    :param bt_ok: Titre du bouton 1 => renvoi QMessageBox.Ok
    :param bt_no: Titre du bouton 2 => renvoi QMessageBox.No
    :param bt_cancel : (obsoléte)
    :param icone_question: Permet d'afficher l'Icône de question
    :param icone_avertissement: Permet d'afficher l'Icône de l'avertissement
    :param icone_critique: Permet d'afficher l'Icône d'une erreur critique
    :param icone_valide: Permet d'afficher l'Icône pour la validation (OK)
    :param icone_sauvegarde: Permet d'affciher l'Icône de sauvegarde
    :param icone_lock: Permet d'afficher l'Icône cadenas
    :param icone_ouvrir: Permet d'afficher l'Icône ouvrir
    :param details: Permet d'afficher plus de détails
    :param txt_save: Permet de changer le texte du bouton annuler => renvoi QMessageBox.Save
    :param afficher_details: Bool permettant d'afficher ou masquer les détails (défaut false)
    :param infos_defaut: Défini si la sauvegarde dans le registre est limité
    :return: renvoi la réponse au message affiché
    """

    print(message)

    # Définition du message
    msgbox = WidgetMessage()

    # Si le paramètre infos est saisi --> affichage de la checkbox + texte
    if infos:

        valeur_infos = settings_get(warning_setting_file, infos)

        # Si la valeur de l'infos dans la base de registre est vrai --> quitte
        if (valeur_infos is not None and
                (valeur_infos == QMessageBox.Ok or valeur_infos == QMessageBox.No or valeur_infos == QMessageBox.Save)):
            return valeur_infos

    if perso:
        pass

    msgbox.show_message(title=titre,
                        message=message,
                        infos=infos,
                        type_bouton=type_bouton,
                        defaut_bouton=defaut_bouton,
                        bt_oui=bt_ok,
                        bt_non=bt_no,
                        bt_annuler=bt_cancel,
                        icone_question=icone_question,
                        icone_avertissement=icone_avertissement,
                        icone_critique=icone_critique,
                        icone_valide=icone_valide,
                        icone_sauvegarde=icone_sauvegarde,
                        icone_lock=icone_lock,
                        icone_ouvrir=icone_ouvrir,
                        details=details,
                        txt_save=txt_save,
                        afficher_details=afficher_details)

    reponse = msgbox.reponse

    if infos and msgbox.check and reponse != QMessageBox.Cancel:

        if infos_defaut == QMessageBox.Ok or infos_defaut == QMessageBox.No or infos_defaut == QMessageBox.Save:
            settings_save_value(warning_setting_file, infos, infos_defaut)
        else:
            settings_save_value(warning_setting_file, infos, reponse)

    return reponse


def a___________________gestions_sauvegarde_______________():
    pass


def make_backup(chemin_dossier: str, fichier: str, extension: str, dossier_sauvegarde=None, nouveau=True,
                nb_sauvegardes=25):
    """ Permet sauvegarder un fichier
    :param chemin_dossier: chemin complet du fichier (c:\\...\\nom_fichier.db)
    :param fichier: Nom du fichier à sauvegarder
    :param extension: extension du fichier (.db)
    :param dossier_sauvegarde: chemin dans lequel le fichier va sauvegarder
    :param nouveau: Si True -> déplacement fichier, sinon copie fichier
    :param nb_sauvegardes: défini le nombre de sauvegardes (25 par défaut)
    :return: Si la sauvegarde a fonctionné correctement = True sinon False
    :rtype: bool
    """

    # Vérification que les valeurs ont été correctement entrée
    if chemin_dossier == "" or fichier == "" or extension == "":
        afficher_message(titre=application_title,
                         message=QCoreApplication.translate(
                             "tools", "Une erreur est survenue."),
                         icone_critique=True,
                         details=f"Missing data : \n"
                                 f"folder_path = {chemin_dossier}\n"
                                 f"file = {fichier}\n"
                                 f"extension = {extension}\n")
        return False

    try:

        zfill = len(str(nb_sauvegardes))

    except ValueError as error:
        afficher_message(titre=application_title,
                         message=QCoreApplication.translate(
                             "tools", "Une erreur est survenue."),
                         icone_critique=True,
                         details=f"{error}")
        return False

    # Vérifiaction si l'extension comporte bien un point
    if "." not in extension:
        extension = f".{extension}"

    # Vérification que le chemin comporte bien un \\ à la fin
    if not chemin_dossier.endswith("\\"):
        chemin_dossier += "\\"

    # Vérification si le chemin existe
    if not os.path.exists(chemin_dossier):
        afficher_message(titre=application_title,
                         message=QCoreApplication.translate(
                             "tools", "Une erreur est survenue."),
                         icone_critique=True,
                         details=f"Folder path not found : {chemin_dossier}")
        return False

    # verification fichier n'a pas l'extension
    if fichier.endswith(extension):
        fichier = fichier[:-len(extension)]

    # Définition du chemin complet
    chemin_fichier_original = f"{chemin_dossier}{fichier}{extension}"
    chemin_fichier_sauvegarde = f"{dossier_sauvegarde}{fichier}{extension}"

    if not os.path.exists(chemin_fichier_original):
        print("creation_sauvegarde --> Aucun fichier à sauvegarde")
        return True

    # Vérification qu'un dossier de sauvegarde a été donné
    if dossier_sauvegarde is not None:

        # Vérification que le chemin comporte bien un \\ à la fin
        if not dossier_sauvegarde.endswith("\\"):
            dossier_sauvegarde += "\\"

        # Vérification que le dossier de sauvegarde existe
        # Cas 1 - le dossier n'existe pas
        if not os.path.exists(dossier_sauvegarde):

            # Création du dossier
            try:
                os.mkdir(dossier_sauvegarde)

            except OSError as error:
                afficher_message(titre=application_title,
                                 message=QCoreApplication.translate(
                                     "tools", "La création du dossier de sauvegarde a échoué."),
                                 icone_critique=True,
                                 details=f"{error}")
                return False

    # --------------------------------
    # Recherche fichiers dans dossier de sauvegardes
    # --------------------------------

    liste_fichiers = os.listdir(dossier_sauvegarde)
    liste_fichiers_a_verifier = list()

    # --------------------------------
    # Recherche des fichiers à renommer
    # --------------------------------

    for fichier_analyser in liste_fichiers:

        if fichier_analyser.startswith(f"{fichier} - ") and fichier_analyser.endswith(extension):
            liste_fichiers_a_verifier.append(fichier_analyser)
            continue

        if fichier_analyser == f"{fichier}{extension}":
            liste_fichiers_a_verifier.insert(0, fichier_analyser)

    # --------------------------------
    # Suppression et renommage
    # --------------------------------

    nb_items = len(liste_fichiers_a_verifier)
    liste_suppression_erreurs = str()
    nb_supression_erreurs = 0

    liste_renommage_erreurs = str()
    nb_renommage_erreurs = 0

    continuer_renommage = True

    for index in reversed(range(nb_items)):

        fichier_analyser = liste_fichiers_a_verifier[index]

        # suppression
        if index >= nb_sauvegardes:

            chemin_fichier_sauvegarde_a_supprimer = f"{dossier_sauvegarde}{fichier_analyser}"

            try:

                send2trash(chemin_fichier_sauvegarde_a_supprimer)

            except OSError as error:

                nb_supression_erreurs += 1
                liste_suppression_erreurs += f"  - {error}\n"

        # renommage
        else:

            if not continuer_renommage:

                chemin_fichier_sauvegarde_avant_renommage = f"{dossier_sauvegarde}{fichier_analyser}"

                try:
                    send2trash(chemin_fichier_sauvegarde_avant_renommage)
                    continuer_renommage = True

                except OSError as error:

                    continuer_renommage = False
                    print(f"creation_sauvegarde -- send2trash({chemin_fichier_sauvegarde_avant_renommage}) -- {error}")

                continue

            index_str = str(index + 1).zfill(zfill)
            chemin_fichier_sauvegarde_avant_renommage = f"{dossier_sauvegarde}{fichier_analyser}"
            nouveau_nom = f"{fichier} - {index_str}{extension}"

            chemin_fichier_sauvegarde_apres_renommage = f"{dossier_sauvegarde}{nouveau_nom}"

            try:

                os.rename(chemin_fichier_sauvegarde_avant_renommage, chemin_fichier_sauvegarde_apres_renommage)

            except Exception as error:

                nb_renommage_erreurs += 1
                liste_renommage_erreurs += f"  - {error}\n"
                continuer_renommage = False

    # -------------------------------
    # Création des messages d'erreurs
    # -------------------------------
    message = ""

    if nb_renommage_erreurs == 1:
        message = f"Une erreur est survenue lors du renommage du fichier de sauvegarde : \n" \
                  f"{liste_renommage_erreurs}"

    elif nb_renommage_erreurs > 1:
        message = f"Des erreurs sont survenues lors du renommage des fichiers de sauvegardes : \n" \
                  f" {liste_renommage_erreurs}"

    if nb_supression_erreurs == 1:
        if message != "":
            message += "\n"

        message += f"Une erreur est survenue lors de la suppression du fichier de sauvegarde : \n" \
                   f"{liste_suppression_erreurs}"

    elif nb_supression_erreurs > 1:
        message += f"Des erreurs sont survenues lors de la suppression de la sauvegarde des fichier : \n" \
                   f" {liste_suppression_erreurs}"

    # --------------------------------
    # Copie du fichier dans le dossier sauvegarde
    # --------------------------------

    copie = True
    error = ""

    try:

        if nouveau:
            shutil.move(chemin_fichier_original, chemin_fichier_sauvegarde)

        else:
            shutil.copy(chemin_fichier_original, chemin_fichier_sauvegarde)

    except Exception as error:

        copie = False

        a = QCoreApplication.translate("tools", "Sauvegarde : le fichier original")
        b = QCoreApplication.translate("tools", "ne peut être déplacé vers le dossier de sauvegarde")
        c = QCoreApplication.translate("tools", "ne peut être copié vers le dossier de sauvegarde")

        if nouveau:

            message = f"{a} : {fichier}{extension} " \
                      f"{b} : \n  - {chemin_fichier_sauvegarde}\n" \
                      f" {message}"

        else:

            message = f"{a} : {fichier}{extension} " \
                      f" {c} : \n {chemin_fichier_sauvegarde}\n" \
                      f" {message}"

    # Affichage du message si la copie a échoué
    if message != "" and not copie:
        afficher_message(titre=application_title,
                         message=message,
                         icone_critique=True,
                         details=f"{error}")

    return copie


def a___________________gestions_presse_papier_______________():
    pass


def copy_to_clipboard(value: str, show_msg=False):
    """
    copier le nom de l'attribut sélectionné dans le presse-papier
    :param value: nom à copier
    :return: None
    """

    if not isinstance(value, str):
        return

    if value == "":
        return

    QApplication.clipboard().setText(value)

    if not show_msg:
        return

    txt = QCoreApplication.translate("tools", "est désormais dans votre presse-papier!")

    afficher_message(titre=f"{value} {txt}",
                     message=f"{value} {txt}")


def a___________________room_______________():
    pass


def get_room_defaut_dict(langue: str, allplan_version="2024") -> dict:
    final_dict = dict()

    if (langue not in translation_room or langue not in translation_231 or langue not in translation_232
            or langue not in translation_233 or langue not in translation_233):
        print("tools -- get_room_defaut_dict -- langue not in dict")

        return dict()

    datas_names = translation_room[langue]
    datas_231 = translation_231[langue]
    datas_232 = translation_232[langue]
    datas_233 = translation_233[langue]
    datas_235 = translation_235[langue]

    if (not isinstance(datas_names, list) or not isinstance(datas_231, list) or not isinstance(datas_232, list)
            or not isinstance(datas_233, list) or not isinstance(datas_235, list)):
        print("tools -- get_room_defaut_dict -- not isinstance(datas_xxx, list)")

        return final_dict

    count_names = len(datas_names)

    count_231 = len(datas_231)
    count_232 = len(datas_232)
    count_233 = len(datas_233)
    count_235 = len(datas_235)

    if (count_names != room_config_count or count_231 != translation_231_count or
            count_232 != translation_232_count or count_233 != translation_233_count
            or count_235 != translation_235_count):
        print("tools -- get_room_defaut_dict -- bad count")

        return final_dict

    for row_index, room_name in enumerate(datas_names):

        room_config = room_config_list[row_index]

        if not isinstance(room_config, list):
            print("tools -- get_room_defaut_dict -- not isinstance(room_config, list)")
            continue

        if len(room_config) != room_sub_config_count:
            print("tools -- get_room_defaut_dict -- len(room_config) != room_sub_config_count")
            continue

        index_231 = room_config[room_config_index_231]
        index_232 = room_config[room_config_index_232]
        index_233 = room_config[room_config_index_233]
        index_235 = room_config[room_config_index_235]
        int_264 = room_config[room_config_index_264]
        int_266 = room_config[room_config_index_266]

        if (not isinstance(index_231, int) or not isinstance(index_232, int) or not isinstance(index_233, int) or not
        isinstance(index_235, int) or not isinstance(int_264, float) or not isinstance(int_266, float)):
            print("tools -- get_room_defaut_dict -- not isinstance(index_2xx, int)")
            continue

        if index_231 >= count_231 or index_232 >= count_232 or index_233 >= count_233 or index_235 >= count_235:
            print("tools -- get_room_defaut_dict -- bad index")
            continue

        val_231 = datas_231[index_231]
        val_232 = datas_232[index_232]
        val_233 = datas_233[index_233]
        val_235 = datas_235[index_235]
        val_264 = format_float_value(value=f"{int_264}", allplan_version=allplan_version)
        val_266 = format_float_value(value=f"{int_266}", allplan_version=allplan_version)

        final_dict[room_name] = {"231": val_231, "232": val_232, "233": val_233, "235": val_235,
                                 "264": val_264, "266": val_266}

    return final_dict


def get_bdd_paths(shortcuts_list: list, short_list=False):
    config = settings_read(file_name=library_setting_file)

    if not isinstance(config, dict):
        return

        # -------------------

    path_cat = config.get("path_cat", "")

    if path_cat != "" and os.path.exists(path_cat) and path_cat not in shortcuts_list:
        shortcuts_list.append(path_cat)

    # -------------------

    path_alltop = config.get("path_alltop", "")

    if path_alltop != "" and os.path.exists(path_alltop) and path_alltop not in shortcuts_list:
        shortcuts_list.append(path_alltop)

    # -------------------

    path_bcm = config.get("path_bcm", "")

    if path_bcm != "" and os.path.exists(path_bcm) and path_bcm not in shortcuts_list:
        shortcuts_list.append(path_bcm)

    if short_list:
        return

    # -------------------

    path_excel = config.get("path_excel", "")

    if path_excel != "" and os.path.exists(path_excel) and path_excel not in shortcuts_list:
        shortcuts_list.append(path_excel)

    # -------------------

    path_favorites = config.get("path_favorites", "")

    if path_favorites != "" and os.path.exists(path_favorites) and path_favorites not in shortcuts_list:
        shortcuts_list.append(path_favorites)

    # -------------------

    path_gimi = config.get("path_gimi", "")

    if path_gimi != "" and os.path.exists(path_gimi) and path_gimi not in shortcuts_list:
        shortcuts_list.append(path_gimi)

    # -------------------

    path_kukat = config.get("path_kukat", "")

    if path_kukat != "" and os.path.exists(path_kukat) and path_kukat not in shortcuts_list:
        shortcuts_list.append(path_kukat)

    # -------------------

    path_kukat = config.get("path_open", "")

    if path_kukat != "" and os.path.exists(path_kukat) and path_kukat not in shortcuts_list:
        shortcuts_list.append(path_kukat)

    return


def a___________________help_______________():
    pass


def help_get_full_link(short_link: str, langue: str) -> str:
    if not isinstance(short_link, str) or not isinstance(langue, str):
        return ""

    short_link = short_link.upper().strip()

    if not short_link.startswith("ASC"):
        return ""

    if langue.upper() not in dict_langues:
        langue = "en_US"

    elif langue == "EN":
        langue = "en_US"

    else:
        langue = langue.lower()

    full_link = f"https://allplan.my.site.com/Customer/s/article/{short_link}?name={short_link}&language={langue}"

    return full_link


def help_get_short_link(full_link: str) -> str:
    if not isinstance(full_link, str):
        return ""

    if not full_link.startswith("https"):
        return ""

    short_link = full_link.replace("https://allplan.my.site.com/Customer/s/article/", "")

    if "?" not in short_link:
        return ""

    char_index = short_link.index("?")

    short_link = short_link[:char_index]

    if len(short_link) < 7:
        return ""

    return short_link


def help_open_link(full_link: str) -> None:
    try:

        webbrowser.open(url=full_link)

    except Exception as error:
        print(f"tools -- help_open_link -- error : {error}")


def help_modify_tooltips(widget: QWidget, short_link: str, help_text: str) -> None:
    if not help_mode:
        return

    if not isinstance(widget, QWidget) or not isinstance(short_link, str) or not isinstance(help_text, str):
        return

    tooltips = widget.toolTip()

    if tooltips == "" or short_link == "" or help_text == "":
        return

    short_link = short_link.upper()

    if not short_link.startswith("ASC") and not short_link.startswith("SPE"):
        return

    help_tooltips_extend = f'<br><br><img src="{help_icon}" width="14" height="14"><b> {help_text}'

    if help_tooltips_extend not in tooltips:
        widget.setToolTip(f"<p style='white-space:pre'>{tooltips}{help_tooltips_extend}")

    if short_link != widget.whatsThis() and not short_link.startswith("SPE"):
        widget.setWhatsThis(short_link)

    return


def help_pressed(widget_parent: QWidget) -> str:
    if not isinstance(widget_parent, QWidget):
        print(f"tools -- help_pressed -- not isinstance(widget_parent, QWidget)")
        return ""

    position_cursor = QCursor().pos()

    try:

        local_pos = widget_parent.mapFromGlobal(position_cursor)

        widget = widget_parent.childAt(local_pos)

    except Exception as error:
        print(f"tools -- help_pressed -- error : {error}")
        return ""

    if not isinstance(widget, QPushButton):
        print(f"tools -- help_pressed -- not isinstance(widget, QPushButton)")
        return ""

    short_link = widget.whatsThis()

    return short_link


def a___________________excel_______________():
    pass


def xml_load_root(file_path: str) -> etree._Element | None:
    if not isinstance(file_path, str):
        print("tools -- xml_load_root -- not isinstance(file_path, str)")
        return

    # -------------
    # Offline
    # -------------

    if not file_path.startswith("https"):

        if not os.path.exists(file_path):
            print(f"tools -- xml_load_root -- not os.path.exists(file_path)")
            return

        try:

            tree = etree.parse(file_path)
            root = tree.getroot()

            return root

        except Exception as error:
            print(f"convert_manage -- ConvertExtern -- run -- error : {error}")

        return

    # -------------
    # Online
    # -------------

    try:
        with urllib.request.urlopen(file_path) as response:

            xml = response.read().decode()

            if not isinstance(xml, str):
                print("tools -- xml_load_root -- not isinstance(xml, str)")
                return

            root = etree.fromstring(xml)
            return root

    except Exception as error:
        print(f"tools -- xml_load_root -- error : {error}")


def excel_load_workbook(file_path: str) -> openpyxl.Workbook | None:
    # -------------
    # Offline
    # -------------

    if not file_path.lower().startswith("https"):

        try:

            with open(file_path, "rb") as f:
                in_mem_file = io.BytesIO(f.read())

            workbook = openpyxl.load_workbook(in_mem_file, data_only=True, read_only=True)

            return workbook

        except Exception as error:
            print(f"tools -- excel_load_workbook -- error : {error}")

        return

    # -------------
    # Online
    # -------------

    try:

        response = requests.get(file_path, stream=True, verify=False)

    except Exception as error:
        print(f"tools -- excel_load_workbook -- error : {error}")
        return

    if not isinstance(response, requests.Response):
        print(f"tools -- excel_load_workbook -- not isinstance(response, Response)")
        return

    if response.status_code != 200:
        print(f"tools -- excel_load_workbook -- error : {response.status_code}")
        return

    try:
        file_data = BytesIO(response.content)

        workbook = openpyxl.load_workbook(file_data, data_only=True, read_only=True)

        return workbook

    except Exception as error:
        print(f"convert_manage -- ConvertExcel -- excel_load_workbook -- error 2 : {error}")

    return None


def a___________________end_______________():
    pass
