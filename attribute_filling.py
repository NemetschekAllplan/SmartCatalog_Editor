#!/usr/bin/python3
# -*- coding: utf-8 -*

import os

from PyQt5.Qt import *

from allplan_manage import AllplanDatas, AllplanPaths
from attribute_335 import WidgetApercu, picture_loading
from history_manage import AttributeModifyData
from main_datas import attribute_setting_file, user_guid
from structure_widget import WidgetStructure
from tools import ValidatorInt, move_widget_ss_bouton, get_look_combobox, application_title
from tools import set_appareance_button, browser_file
from ui_attribute_filling import Ui_AttributeFilling


class AttributeFilling(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict, str)

    def __init__(self, smartcatalog):
        super().__init__()

        # Chargement du widget + setup
        self.ui = Ui_AttributeFilling()
        self.ui.setupUi(self)

        self.asc = smartcatalog

        self.widget_popup = WidgetStructure(self.asc)
        self.widget_popup.remp_modif.connect(self.popup_enregitrer)

        self.allplan: AllplanDatas = self.asc.allplan

        self.type_element = "type_remplissage"
        self.row_index = 0

        if self.allplan.allplan_paths is None:
            self.design_std_path = ""
        else:
            self.design_std_path = f"{self.allplan.allplan_paths.std_path}Design\\"

        self.design_prj_path = f"{self.allplan.catalog_user_path}design\\"

        self.qs_118 = QStandardItem()

        self.qs_111_ind = QStandardItem()
        self.qs_111_val = QStandardItem()

        self.qs_252_ind = QStandardItem()
        self.qs_252_val = QStandardItem()

        self.qs_336 = QStandardItem()

        self.listwidgetitem = QListWidgetItem()

        # ---------------------------------------
        # hachurage
        # ---------------------------------------

        self.filtre_hachurage = QSortFilterProxyModel()
        self.filtre_hachurage.setSourceModel(self.allplan.model_haching)
        self.filtre_hachurage.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_hachurage.setFilterKeyColumn(1)

        self.ui.hachurage.setModel(self.allplan.model_haching)
        self.ui.hachurage.setModelColumn(1)

        self.qcompleter_hachurage = self.ui.hachurage.completer()
        self.qcompleter_hachurage.setModel(self.filtre_hachurage)
        self.qcompleter_hachurage.setCompletionColumn(1)
        self.qcompleter_hachurage.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.qcompleter_hachurage.setCaseSensitivity(Qt.CaseInsensitive)
        self.qcompleter_hachurage.popup().setIconSize(QSize(200, 18))

        self.ui.hachurage.setCompleter(self.qcompleter_hachurage)
        self.ui.hachurage.setValidator(ValidatorInt())

        self.ui.chb_hachurage.clicked.connect(self.chb_hachurage_clic)
        self.ui.hachurage.lineEdit().textEdited.connect(self.filtre_hachurage.setFilterFixedString)

        self.ui.hachurage.currentIndexChanged.connect(self.verification_datas_hachurage)

        self.ui.hachurage.installEventFilter(self)

        get_look_combobox(self.ui.hachurage)

        # ---------------------------------------
        # Pattern
        # ---------------------------------------

        self.filtre_motif = QSortFilterProxyModel()
        self.filtre_motif.setSourceModel(self.allplan.model_pattern)
        self.filtre_motif.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_motif.setFilterKeyColumn(1)

        self.ui.motif.setModel(self.allplan.model_pattern)
        self.ui.motif.setModelColumn(1)

        self.qcompleter_motif = self.ui.motif.completer()
        self.qcompleter_motif.setModel(self.filtre_motif)
        self.qcompleter_motif.setCompletionColumn(1)
        self.qcompleter_motif.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.qcompleter_motif.setCaseSensitivity(Qt.CaseInsensitive)
        self.qcompleter_motif.popup().setIconSize(QSize(200, 18))

        self.ui.motif.setCompleter(self.qcompleter_motif)
        self.ui.motif.setValidator(ValidatorInt())

        self.ui.chb_motif.clicked.connect(self.chb_motif_clic)
        self.ui.motif.lineEdit().textEdited.connect(self.filtre_motif.setFilterFixedString)

        self.ui.motif.currentIndexChanged.connect(self.verification_datas_motif)

        self.ui.motif.installEventFilter(self)

        get_look_combobox(self.ui.motif)

        # ---------------------------------------
        # Color
        # ---------------------------------------

        self.filtre_couleur = QSortFilterProxyModel()
        self.filtre_couleur.setSourceModel(self.allplan.model_color)
        self.filtre_couleur.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_couleur.setFilterKeyColumn(1)

        self.ui.couleur.setModel(self.allplan.model_color)
        self.ui.couleur.setModelColumn(1)

        self.ui.couleur.view().setIconSize(QSize(200, 18))
        self.ui.couleur.setIconSize(QSize(200, 18))

        self.qcompleter_couleur = self.ui.couleur.completer()
        self.qcompleter_couleur.setModel(self.filtre_couleur)
        self.qcompleter_couleur.setCompletionColumn(1)
        self.qcompleter_couleur.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.qcompleter_couleur.setCaseSensitivity(Qt.CaseInsensitive)
        self.qcompleter_couleur.popup().setIconSize(QSize(200, 18))

        self.ui.couleur.setCompleter(self.qcompleter_couleur)
        self.ui.couleur.setValidator(ValidatorInt())

        self.ui.chb_couleur.clicked.connect(self.chb_couleur_clic)
        self.ui.couleur.lineEdit().textEdited.connect(self.filtre_couleur.setFilterFixedString)

        self.ui.couleur.currentIndexChanged.connect(self.verification_datas_couleur)

        self.ui.couleur.installEventFilter(self)

        get_look_combobox(self.ui.couleur)

        # ---------------------------------------
        # surface d'images
        # ---------------------------------------

        self.ui.browser_bt.clicked.connect(self.parcourir_surface)

        self.ui.chb_surface.clicked.connect(self.chb_surface_clic)

        set_appareance_button(self.ui.browser_bt)

        self.ui.surface.installEventFilter(self)

        self.ui.preview_bt.clicked.connect(self.afficher_apercu)

        # ---------------------------------------
        # style de surface
        # ---------------------------------------

        self.filtre_style = QSortFilterProxyModel()
        self.filtre_style.setSourceModel(self.allplan.model_style)
        self.filtre_style.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_style.setFilterKeyColumn(1)

        self.ui.style.setModel(self.allplan.model_style)
        self.ui.style.setModelColumn(1)

        self.qcompleter_style = self.ui.style.completer()
        self.qcompleter_style.setModel(self.filtre_style)
        self.qcompleter_style.setCompletionColumn(1)
        self.qcompleter_style.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.qcompleter_style.setCaseSensitivity(Qt.CaseInsensitive)
        self.qcompleter_style.popup().setIconSize(QSize(200, 18))

        self.ui.style.setCompleter(self.qcompleter_style)

        self.ui.chb_style.clicked.connect(self.chb_style_clic)

        set_appareance_button(self.ui.bt_option)
        self.ui.bt_option.clicked.connect(self.afficher_choix_surface)

        self.ui.style.lineEdit().textEdited.connect(self.filtre_style.setFilterFixedString)

        self.ui.style.currentIndexChanged.connect(self.verification_datas_style)

        self.ui.style.installEventFilter(self)
        self.ui.chb_surface.installEventFilter(self)

        get_look_combobox(self.ui.style)

        self.titre_couleur_2 = QLineEdit()

        self.ui.line_118.installEventFilter(self)
        self.ui.line_hatching.installEventFilter(self)
        self.ui.line_pattern.installEventFilter(self)
        self.ui.line_color.installEventFilter(self)
        self.ui.line_picture.installEventFilter(self)
        self.ui.line_style.installEventFilter(self)

    def chargement(self, row_index: int):

        self.row_index = row_index

        val_118 = self.qs_118.text()
        val_111_val = self.qs_111_val.text()
        val_111_ind = self.qs_111_ind.text()
        val_252_ind = self.qs_252_ind.text()
        val_336 = self.qs_336.text()

        self.charger_icone()

        # numero_identification
        self.ui.numero_identification.setText(val_118)

        # Hachurage
        if val_118 == "1":

            self.ui.chb_hachurage.setChecked(True)

            self.ui.hachurage.setCurrentText(val_111_val)
            self.ui.numero_hachurage.setText(val_111_ind)

            couleur = self.qs_252_ind.text()

            if couleur != "-1" and couleur != "":
                self.ui.chb_couleur.setChecked(True)

                val_252_int = int(val_252_ind) + 1
                self.ui.couleur.setCurrentIndex(val_252_int)
                self.ui.numero_couleur.setText(val_252_ind)

            self.chb_change()
            return

        # Motif
        if val_118 == "2":

            self.ui.chb_motif.setChecked(True)

            self.ui.motif.setCurrentText(val_111_val)
            self.ui.numero_motif.setText(val_111_ind)

            couleur = self.qs_252_ind.text()

            if couleur != "-1" and couleur != "":
                self.ui.chb_couleur.setChecked(True)

                val_252_int = int(val_252_ind) + 1
                self.ui.couleur.setCurrentIndex(val_252_int)
                self.ui.numero_couleur.setText(val_252_ind)

            self.chb_change()
            return

        # Couleur
        if val_118 == "3":
            self.ui.chb_couleur.setChecked(True)
            self.chb_change()

            val_111_ind_int2 = int(val_111_ind) + 1

            self.ui.couleur.setCurrentIndex(val_111_ind_int2)
            self.ui.numero_couleur.setText(val_111_ind)

            return

        # Surface
        if val_118 == "6":
            self.ui.chb_surface.setChecked(True)
            self.chb_change()

            self.ui.surface.setText(val_336)
            return

        # Style
        if val_118 == "5":
            self.ui.chb_style.setChecked(True)
            self.chb_change()

            self.ui.style.setCurrentText(val_111_val)
            self.ui.numero_style.setText(val_111_ind)
            return

        self.chb_change()

    @staticmethod
    def a___________________changement_type______():
        pass

    def aucun_clic(self):

        qs_parent = self.qs_118.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_filling -- aucun_clic -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_filling -- aucun_clic -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_filling -- aucun_clic -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = list()
        value_dict = dict()

        # ------------- 118

        value_current_118 = self.qs_118.text()
        value_new_118 = "0"

        self.qs_118.setText(value_new_118)
        self.ui.numero_identification.setText(value_new_118)

        attribute_data.append(AttributeModifyData(number_current="118", value_new=value_current_118))

        value_dict["118"] = [value_current_118, value_new_118]

        # ------------- 111

        value_current_111 = self.qs_111_val.text()
        value_new_111 = ""

        value_index_current_111 = self.qs_111_ind.text()
        value_index_new_111 = "-1"

        self.qs_111_val.setText(value_new_111)
        self.qs_111_ind.setText(value_index_new_111)

        attribute_data.append(AttributeModifyData(number_current="111",
                                                  value_new=value_current_111,
                                                  value_index_new=value_index_current_111))

        value_dict["111"] = [value_current_111, value_new_111]

        # ------------- 252

        value_current_252 = self.qs_252_val.text()
        value_new_252 = ""

        value_index_current_252 = self.qs_252_ind.text()
        value_index_new_252 = "-1"

        self.qs_252_val.setText(value_new_252)
        self.qs_252_ind.setText(value_index_new_252)

        attribute_data.append(AttributeModifyData(number_current="252",
                                                  value_new=value_current_252,
                                                  value_index_new=value_index_current_252))

        value_dict["252"] = [value_current_252, value_new_252]

        # ------------- 336

        value_current_336 = self.qs_336.text()
        value_new_336 = ""

        self.qs_336.setText(value_new_336)

        attribute_data.append(AttributeModifyData(number_current="336", value_new=value_current_336))

        value_dict["336"] = [value_current_336, value_new_336]

        # ------------- signal

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                           self.tr("Groupe Remplissage"))

    def chb_hachurage_clic(self):

        if not self.ui.chb_hachurage.isVisible():
            return

        checked = self.ui.chb_hachurage.isChecked()
        couleur = self.ui.chb_couleur.isChecked()

        # Motif
        self.ui.chb_motif.setChecked(False)

        # Couleur
        self.ui.chb_couleur.setChecked(couleur)

        # Surface
        self.ui.chb_surface.setChecked(False)

        # Style
        self.ui.chb_style.setChecked(False)

        # Tous
        self.chb_change()

        # Attributs
        if not checked:
            self.aucun_clic()
            return

        qs_parent = self.qs_118.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_filling -- chb_hachurage_clic -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_filling -- chb_hachurage_clic -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_filling -- chb_hachurage_clic -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = list()
        value_dict = dict()

        # ------------- 118

        value_current_118 = self.qs_118.text()
        value_new_118 = "1"

        self.qs_118.setText(value_new_118)
        self.ui.numero_identification.setText(value_new_118)

        attribute_data.append(AttributeModifyData(number_current="118", value_new=value_current_118))

        value_dict["118"] = [value_current_118, value_new_118]

        # ------------- 111

        value_current_111 = self.qs_111_val.text()
        value_new_111 = self.ui.hachurage.currentText()

        value_index_current_111 = self.qs_111_ind.text()
        value_index_new_111 = self.ui.numero_hachurage.text()

        self.qs_111_val.setText(value_new_111)
        self.qs_111_ind.setText(value_index_new_111)

        attribute_data.append(AttributeModifyData(number_current="111",
                                                  value_new=value_current_111,
                                                  value_index_new=value_index_current_111))

        value_dict["111"] = [value_current_111, value_new_111]

        # ------------- 252

        value_current_252 = self.qs_252_val.text()
        value_index_current_252 = self.qs_252_ind.text()

        if couleur:

            value_new_252 = self.ui.couleur.currentText()
            value_index_new_252 = self.ui.numero_couleur.text()

        else:

            value_new_252 = ""
            value_index_new_252 = "-1"

        self.qs_252_val.setText(value_new_252)
        self.qs_252_ind.setText(value_index_new_252)

        attribute_data.append(AttributeModifyData(number_current="252",
                                                  value_new=value_current_252,
                                                  value_index_new=value_index_current_252))

        value_dict["252"] = [value_current_252, value_new_252]

        # ------------- 336

        value_current_336 = self.qs_336.text()
        value_new_336 = ""

        self.qs_336.setText(value_new_336)

        attribute_data.append(AttributeModifyData(number_current="336", value_new=value_current_336))

        value_dict["336"] = [value_current_336, value_new_336]

        # ------------- signal

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                           self.tr("Groupe Remplissage"))

        # -------------

        self.ui.hachurage.setFocus()

    def chb_motif_clic(self):

        if not self.ui.chb_motif.isVisible():
            return

        checked = self.ui.chb_motif.isChecked()
        couleur = self.ui.chb_couleur.isChecked()

        # Hachurage
        self.ui.chb_hachurage.setChecked(False)

        # Couleur
        self.ui.chb_couleur.setChecked(couleur)

        # Surface
        self.ui.chb_surface.setChecked(False)

        # Style
        self.ui.chb_style.setChecked(False)

        # Tous
        self.chb_change()

        # Attributs
        if not checked:
            self.aucun_clic()
            return

        qs_parent = self.qs_118.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_filling -- chb_motif_clic -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_filling -- chb_motif_clic -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_filling -- chb_motif_clic -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = list()
        value_dict = dict()

        # ------------- 118

        value_current_118 = self.qs_118.text()
        value_new_118 = "2"

        self.qs_118.setText(value_new_118)
        self.ui.numero_identification.setText(value_new_118)

        attribute_data.append(AttributeModifyData(number_current="118", value_new=value_current_118))

        value_dict["118"] = [value_current_118, value_new_118]

        # ------------- 111

        value_current_111 = self.qs_111_val.text()
        value_new_111 = self.ui.motif.currentText()

        value_index_current_111 = self.qs_111_ind.text()
        value_index_new_111 = self.ui.numero_motif.text()

        self.qs_111_val.setText(value_new_111)
        self.qs_111_ind.setText(value_index_new_111)

        attribute_data.append(AttributeModifyData(number_current="111",
                                                  value_new=value_current_111,
                                                  value_index_new=value_index_current_111))

        value_dict["111"] = [value_current_111, value_new_111]

        # ------------- 252

        value_current_252 = self.qs_252_val.text()
        value_index_current_252 = self.qs_252_ind.text()

        if couleur:

            value_new_252 = self.ui.couleur.currentText()
            value_index_new_252 = self.ui.numero_couleur.text()

        else:

            value_new_252 = ""
            value_index_new_252 = "-1"

        self.qs_252_val.setText(value_new_252)
        self.qs_252_ind.setText(value_index_new_252)

        attribute_data.append(AttributeModifyData(number_current="252",
                                                  value_new=value_current_252,
                                                  value_index_new=value_index_current_252))

        value_dict["252"] = [value_current_252, value_new_252]

        # ------------- 336

        value_current_336 = self.qs_336.text()
        value_new_336 = ""

        self.qs_336.setText(value_new_336)

        attribute_data.append(AttributeModifyData(number_current="336", value_new=value_current_336))

        value_dict["336"] = [value_current_336, value_new_336]

        # ------------- signal

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                           self.tr("Groupe Remplissage"))

        # -------------

        self.ui.motif.setFocus()

    def chb_couleur_clic(self):

        if not self.ui.chb_couleur.isVisible():
            return

        checked = self.ui.chb_couleur.isChecked()

        hachurage = self.ui.chb_hachurage.isChecked()
        motif = self.ui.chb_motif.isChecked()

        # Surface
        self.ui.chb_surface.setChecked(False)

        # Style
        self.ui.chb_style.setChecked(False)

        # Tous
        self.chb_change()

        # -------------

        qs_parent = self.qs_118.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_filling -- chb_couleur_clic -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_filling -- chb_couleur_clic -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_filling -- chb_couleur_clic -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = list()
        value_dict = dict()

        # --------------------------------
        # Attributs hachurage + couleur
        # --------------------------------

        if hachurage and checked:
            # ------------- 118

            value_current_118 = self.qs_118.text()
            value_new_118 = "1"

            self.qs_118.setText(value_new_118)
            self.ui.numero_identification.setText(value_new_118)

            attribute_data.append(AttributeModifyData(number_current="118", value_new=value_current_118))

            value_dict["118"] = [value_current_118, value_new_118]

            # ------------- 111

            value_current_111 = self.qs_111_val.text()
            value_new_111 = self.ui.hachurage.currentText()

            value_index_current_111 = self.qs_111_ind.text()
            value_index_new_111 = self.ui.numero_hachurage.text()

            self.qs_111_val.setText(value_new_111)
            self.qs_111_ind.setText(value_index_new_111)

            attribute_data.append(AttributeModifyData(number_current="111",
                                                      value_new=value_current_111,
                                                      value_index_new=value_index_current_111))

            value_dict["111"] = [value_current_111, value_new_111]

            # ------------- 252

            value_current_252 = self.qs_252_val.text()
            value_new_252 = self.ui.couleur.currentText()

            value_index_current_252 = self.qs_252_ind.text()
            value_index_new_252 = self.ui.numero_couleur.text()

            self.qs_252_val.setText(value_new_252)
            self.qs_252_ind.setText(value_index_new_252)

            attribute_data.append(AttributeModifyData(number_current="252",
                                                      value_new=value_current_252,
                                                      value_index_new=value_index_current_252))

            value_dict["252"] = [value_current_252, value_new_252]

            # ------------- 336

            value_current_336 = self.qs_336.text()
            value_new_336 = ""

            self.qs_336.setText(value_new_336)

            attribute_data.append(AttributeModifyData(number_current="336", value_new=value_current_336))

            value_dict["336"] = [value_current_336, value_new_336]

            # ------------- signal

            self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                               self.tr("Groupe Remplissage"))

            # -------------

            self.ui.couleur.setFocus()
            return

        # --------------------------------
        # Attributs motif + couleur
        # --------------------------------

        if motif and checked:
            # ------------- 118

            value_current_118 = self.qs_118.text()
            value_new_118 = "2"

            self.qs_118.setText(value_new_118)
            self.ui.numero_identification.setText(value_new_118)

            attribute_data.append(AttributeModifyData(number_current="118", value_new=value_current_118))

            value_dict["118"] = [value_current_118, value_new_118]

            # ------------- 111

            value_current_111 = self.qs_111_val.text()
            value_new_111 = self.ui.motif.currentText()

            value_index_current_111 = self.qs_111_ind.text()
            value_index_new_111 = self.ui.numero_motif.text()

            self.qs_111_val.setText(value_new_111)
            self.qs_111_ind.setText(value_index_new_111)

            attribute_data.append(AttributeModifyData(number_current="111",
                                                      value_new=value_current_111,
                                                      value_index_new=value_index_current_111))

            value_dict["111"] = [value_current_111, value_new_111]

            # ------------- 252

            value_current_252 = self.qs_252_val.text()
            value_new_252 = self.ui.numero_couleur.text()

            value_index_current_252 = self.qs_252_ind.text()
            value_index_new_252 = self.ui.numero_couleur.text()

            self.qs_252_val.setText(value_new_252)
            self.qs_252_ind.setText(value_index_new_252)

            attribute_data.append(AttributeModifyData(number_current="252",
                                                      value_new=value_current_252,
                                                      value_index_new=value_index_current_252))

            value_dict["252"] = [value_current_252, value_new_252]

            # ------------- 336

            value_current_336 = self.qs_336.text()
            value_new_336 = ""

            self.qs_336.setText(value_new_336)

            attribute_data.append(AttributeModifyData(number_current="336", value_new=value_current_336))

            value_dict["336"] = [value_current_336, value_new_336]

            # ------------- signal

            self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                               self.tr("Groupe Remplissage"))

            # -------------

            self.ui.couleur.setFocus()
            return

        # --------------------------------
        # Attributs couleur seul
        # --------------------------------

        if checked:
            # ------------- 118

            value_current_118 = self.qs_118.text()
            value_new_118 = "3"

            self.qs_118.setText(value_new_118)
            self.ui.numero_identification.setText(value_new_118)

            attribute_data.append(AttributeModifyData(number_current="118", value_new=value_current_118))

            value_dict["118"] = [value_current_118, value_new_118]

            # ------------- 111

            value_current_111 = self.qs_111_val.text()
            value_new_111 = self.ui.couleur.currentText()

            value_index_current_111 = self.qs_111_ind.text()
            value_index_new_111 = self.ui.numero_couleur.text()

            self.qs_111_val.setText(value_new_111)
            self.qs_111_ind.setText(value_index_new_111)

            attribute_data.append(AttributeModifyData(number_current="111",
                                                      value_new=value_current_111,
                                                      value_index_new=value_index_current_111))

            value_dict["111"] = [value_current_111, value_new_111]

            # ------------- 252

            value_current_252 = self.qs_252_val.text()
            value_new_252 = ""

            value_index_current_252 = self.qs_252_ind.text()
            value_index_new_252 = "-1"

            self.qs_252_val.setText(value_new_252)
            self.qs_252_ind.setText(value_index_new_252)

            attribute_data.append(AttributeModifyData(number_current="252",
                                                      value_new=value_current_252,
                                                      value_index_new=value_index_current_252))

            value_dict["252"] = [value_current_252, value_new_252]

            # ------------- 336

            value_current_336 = self.qs_336.text()
            value_new_336 = ""

            self.qs_336.setText(value_new_336)

            attribute_data.append(AttributeModifyData(number_current="336", value_new=value_current_336))

            value_dict["336"] = [value_current_336, value_new_336]

            # ------------- signal

            self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                               self.tr("Groupe Remplissage"))

            self.ui.couleur.setFocus()
            return

        self.aucun_clic()

    def chb_surface_clic(self):

        if not self.ui.chb_surface.isVisible():
            return

        checked = self.ui.chb_surface.isChecked()

        if not checked:
            self.aucun_clic()
            return

        # Hachurage
        self.ui.chb_hachurage.setChecked(False)

        # Motif
        self.ui.chb_motif.setChecked(False)

        # Couleur
        self.ui.chb_couleur.setChecked(False)

        # Style
        self.ui.chb_style.setChecked(False)

        # Tous
        self.chb_change()

        # Attributs
        if not checked:
            self.aucun_clic()
            return

        # -------------

        qs_parent = self.qs_118.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_filling -- chb_surface_clic -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_filling -- chb_surface_clic -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_filling -- chb_surface_clic -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = list()
        value_dict = dict()

        # ------------- 118

        value_current_118 = self.qs_118.text()
        value_new_118 = "6"

        self.qs_118.setText(value_new_118)
        self.ui.numero_identification.setText(value_new_118)

        attribute_data.append(AttributeModifyData(number_current="118", value_new=value_current_118))

        value_dict["118"] = [value_current_118, value_new_118]

        # ------------- 111

        value_current_111 = self.qs_111_val.text()
        value_new_111 = ""

        value_index_current_111 = self.qs_111_ind.text()
        value_index_new_111 = "-1"

        self.qs_111_val.setText(value_new_111)
        self.qs_111_ind.setText(value_index_new_111)

        attribute_data.append(AttributeModifyData(number_current="111",
                                                  value_new=value_current_111,
                                                  value_index_new=value_index_current_111))

        value_dict["111"] = [value_current_111, value_new_111]

        # ------------- 252

        value_current_252 = self.qs_252_val.text()
        value_new_252 = ""

        value_index_current_252 = self.qs_252_ind.text()
        value_index_new_252 = "-1"

        self.qs_252_val.setText(value_new_252)
        self.qs_252_ind.setText(value_index_new_252)

        attribute_data.append(AttributeModifyData(number_current="252",
                                                  value_new=value_current_252,
                                                  value_index_new=value_index_current_252))

        value_dict["252"] = [value_current_252, value_new_252]

        # ------------- 336

        value_current_336 = self.qs_336.text()
        value_new_336 = self.ui.surface.text()

        self.qs_336.setText(value_new_336)

        attribute_data.append(AttributeModifyData(number_current="336", value_new=value_current_336))

        value_dict["336"] = [value_current_336, value_new_336]

        # ------------- signal

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                           self.tr("Groupe Remplissage"))

        # -------------

        self.ui.browser_bt.setFocus()

    def chb_style_clic(self):

        if not self.ui.chb_style.isVisible():
            return

        checked = self.ui.chb_style.isChecked()

        # Hachurage
        self.ui.chb_hachurage.setChecked(False)

        # Motif
        self.ui.chb_motif.setChecked(False)

        # Couleur
        self.ui.chb_couleur.setChecked(False)

        # Surface
        self.ui.chb_surface.setChecked(False)

        # Style
        self.ui.style.setEnabled(checked)

        # Tous
        self.chb_change()

        # Attributs
        if not checked:
            self.aucun_clic()
            return

        # -------------

        qs_parent = self.qs_118.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_filling -- chb_surface_clic -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_filling -- chb_surface_clic -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_filling -- chb_surface_clic -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = list()
        value_dict = dict()

        # ------------- 118

        value_current_118 = self.qs_118.text()
        value_new_118 = "5"

        self.qs_118.setText(value_new_118)
        self.ui.numero_identification.setText(value_new_118)

        attribute_data.append(AttributeModifyData(number_current="118", value_new=value_current_118))

        value_dict["118"] = [value_current_118, value_new_118]

        # ------------- 111

        value_current_111 = self.qs_111_val.text()
        value_new_111 = self.ui.style.currentText()

        value_index_current_111 = self.qs_111_ind.text()
        value_index_new_111 = self.ui.numero_style.text()

        self.qs_111_val.setText(value_new_111)
        self.qs_111_ind.setText(value_index_new_111)

        attribute_data.append(AttributeModifyData(number_current="111",
                                                  value_new=value_current_111,
                                                  value_index_new=value_index_current_111))

        value_dict["111"] = [value_current_111, value_new_111]

        # ------------- 252

        value_current_252 = self.qs_252_val.text()
        value_new_252 = ""

        value_index_current_252 = self.qs_252_ind.text()
        value_index_new_252 = "-1"

        self.qs_252_val.setText(value_new_252)
        self.qs_252_ind.setText(value_index_new_252)

        attribute_data.append(AttributeModifyData(number_current="252",
                                                  value_new=value_current_252,
                                                  value_index_new=value_index_current_252))

        value_dict["252"] = [value_current_252, value_new_252]

        # ------------- 336

        value_current_336 = self.qs_336.text()
        value_new_336 = ""

        self.qs_336.setText(value_new_336)

        attribute_data.append(AttributeModifyData(number_current="336", value_new=value_current_336))

        value_dict["336"] = [value_current_336, value_new_336]

        # ------------- signal

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                           self.tr("Groupe Remplissage"))

        # -------------

        self.ui.style.setFocus()

    def chb_change(self):

        # ----- 118 -----
        row_index = self.row_index

        self.ui.line_118.setStyleSheet(f"QWidget#line_118 {self.get_color_row(row_index=row_index)}")
        row_index += 1

        # ----- hatching -----

        hatching = self.ui.chb_hachurage.isChecked()

        self.ui.line_hatching.setVisible(hatching)

        if hatching:
            self.ui.line_hatching.setStyleSheet(f"QWidget#line_hatching {self.get_color_row(row_index=row_index)}")
            row_index += 1

        # ----- pattern -----

        pattern = self.ui.chb_motif.isChecked()

        self.ui.line_pattern.setVisible(pattern)

        if pattern:
            self.ui.line_pattern.setStyleSheet(f"QWidget#line_pattern {self.get_color_row(row_index=row_index)}")
            row_index += 1

        # ----- color -----

        color = self.ui.chb_couleur.isChecked()

        self.ui.line_color.setVisible(color)

        if color:
            self.ui.line_color.setStyleSheet(f"QWidget#line_color {self.get_color_row(row_index=row_index)}")
            row_index += 1

        # ----- surface -----

        surface = self.ui.chb_surface.isChecked()

        self.ui.line_picture.setVisible(surface)

        if surface:
            self.ui.line_picture.setStyleSheet(f"QWidget#line_picture {self.get_color_row(row_index=row_index)}")
            row_index += 1

        # ----- style -----

        style = self.ui.chb_style.isChecked()

        self.ui.line_style.setVisible(style)

        if style:
            self.ui.line_style.setStyleSheet(f"QWidget#line_style {self.get_color_row(row_index=row_index)}")
            row_index += 1

        # ----- text -----

        if color and (hatching or pattern):
            self.ui.num_attr_couleur.setText("252")
            self.ui.titre_couleur.setText(self.titre_couleur_2.text())

        elif color:
            self.ui.num_attr_couleur.setText("111")
            self.ui.titre_couleur.setText(self.ui.titre_hachurage.text())

        # ----- text -----

        if self.listwidgetitem is None:
            return

        self.listwidgetitem.setSizeHint(self.sizeHint())

    @staticmethod
    def get_color_row(row_index: int) -> str:
        pass

        # if row_index % 2 == 0:
        #     return "{background-color: #fff}"
        # return "{background-color: #e9e7e3}"

    @staticmethod
    def a___________________surface______():
        pass

    def parcourir_surface(self):

        self.asc.formula_widget_close()

        path_current = self.design_prj_path
        filename = ""

        if self.ui.surface.text() != "":

            valeur_actuelle = self.ui.surface.text().replace("\\\\", "\\")
            dossier_texture = os.path.dirname(valeur_actuelle)

            filename = os.path.basename(valeur_actuelle)

            full_path_prj = self.design_prj_path + dossier_texture + "\\"
            full_path_std = self.design_std_path + dossier_texture + "\\"

            if os.path.exists(full_path_prj):
                path_current = full_path_prj

            elif os.path.exists(full_path_std):
                path_current = full_path_std

        a = self.tr("Fichier")
        b = self.tr("Fichier image")

        datas_filters = {b: [".jpg", ".jff", ".jtf", ".jpeg", ".tif", ".tga", ".bmp", ".mac",
                             ".msp", ".pcd", ".pct", ".pcx", ".png", ".psd", ".ras", ".wmf"],
                         f"{a} JPEG": [".jpg", ".jff", ".jtf", ".jpeg"],
                         f"{a} TIF": [".tif"],
                         f"{a} TGA": [".tga"],
                         f"{a} BMP": [".bmp"],
                         f"{a} MAC": [".mac"],
                         f"{a} MSP": [".msp"],
                         f"{a} PCD": [".pcd"],
                         f"{a} PCT": [".pct"],
                         f"{a} PCX": [".pcx"],
                         f"{a} PNG": [".png"],
                         f"{a} PSD": [".psd"],
                         f"{a} RAS": [".ras"],
                         f"{a} WMF": [".wmf"],
                         self.tr("Tous les fichiers"): [".*"]}

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [self.allplan.allplan_paths.std_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.tmp_path]

            if self.allplan.catalog_user_path != self.allplan.allplan_paths.std_design_path:

                design = f"{self.allplan.catalog_user_path}Design\\"

                if os.path.exists(design):
                    shortcuts_list.append(design)

        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[attribute_setting_file, "path_bitmap_area"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters=datas_filters,
                                 current_path=path_current,
                                 default_path="",
                                 file_name=filename,
                                 use_setting_first=False)

        if file_path == "":
            return

        surface_path_lower = file_path.lower()

        if surface_path_lower.startswith(self.design_prj_path.lower()):
            file_path = file_path[len(self.design_prj_path):]

        elif surface_path_lower.startswith(self.design_std_path.lower()):
            file_path = file_path[len(self.design_std_path):]

        file_path = file_path.replace("\\\\", "\\")

        file_path = file_path.replace("\\", "\\\\")

        self.ui.surface.setText(file_path)
        self.mise_a_jour_surface()
        self.charger_icone()

    def mise_a_jour_surface(self):

        value_current = self.qs_336.text()

        value_new = self.ui.surface.text()

        if value_current == value_new:
            return

        if not self.ui.surface.isVisible():
            return

        self.qs_336.setText(value_new)

        # -------------

        qs_parent = self.qs_118.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_filling -- mise_a_jour_surface -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_filling -- mise_a_jour_surface -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_filling -- mise_a_jour_surface -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = [AttributeModifyData(number_current="336", value_new=value_current)]
        value_dict = {"336": [value_current, value_new]}

        # -------------

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, "")

    def afficher_apercu(self):

        self.asc.formula_widget_close()

        chemin = self.recherche_chemin_actuel()

        if chemin == "":
            return

        widget_popup = WidgetApercu(self, chemin)

        widget_popup.show()

        move_widget_ss_bouton(self.ui.preview_bt, widget_popup)

    def recherche_chemin_actuel(self) -> str:
        chemin = self.ui.surface.text()
        return self.recherche_chemin(chemin)

    def recherche_chemin(self, chemin: str) -> str:

        chemin_prj = f"{self.design_prj_path}{chemin}"
        chemin_std = f"{self.design_std_path}{chemin}"

        if chemin == "":
            return ""

        chemin = chemin.replace("\\\\", "\\")

        if os.path.exists(chemin):
            return chemin

        if os.path.exists(chemin_prj):
            return chemin_prj

        if os.path.exists(chemin_std):
            return chemin_std

        return ""

    def charger_icone(self):

        chemin = self.recherche_chemin_actuel()

        if chemin == "":
            self.ui.preview_bt.setVisible(False)
            return

        self.ui.preview_bt.setVisible(True)

        icon = QIcon(picture_loading(chemin))
        self.ui.preview_bt.setIcon(icon)

    @staticmethod
    def a___________________popup______():
        pass

    def afficher_choix_surface(self):

        self.asc.formula_widget_close()

        if not self.ui.chb_style.isChecked():
            return

        self.widget_popup.widget_structure_show(current_mode="remp",
                                                current_model=self.allplan.model_style_view,
                                                current_combo_model=self.ui.style.model(),
                                                curennt_index=self.ui.numero_style.text())

    def popup_enregitrer(self, numero: str, valeur: str):

        if valeur == "Aucun":
            valeur = ""

        self.ui.numero_style.setText(numero)
        self.ui.style.setCurrentText(valeur)

        self.verification_datas_style()

    @staticmethod
    def a___________________datas______():
        pass

    def verification_datas_hachurage(self):

        if self.ui.hachurage.view().isVisible():
            return

        self.verification_datas(widget_combo=self.ui.hachurage,
                                widget_index=self.ui.numero_hachurage,
                                nb_caractere=3)

    def verification_datas_motif(self):
        self.verification_datas(widget_combo=self.ui.motif,
                                widget_index=self.ui.numero_motif,
                                nb_caractere=3)

    def verification_datas_couleur(self):
        if self.qs_118.text() == "3":

            self.verification_datas(widget_combo=self.ui.couleur,
                                    widget_index=self.ui.numero_couleur)

        else:

            self.verification_datas(widget_combo=self.ui.couleur,
                                    widget_index=self.ui.numero_couleur,
                                    attribut_252=True)

    def verification_datas_style(self):
        self.verification_datas(widget_combo=self.ui.style,
                                widget_index=self.ui.numero_style)

    def verification_datas(self, widget_combo: QComboBox, widget_index: QLabel, attribut_252=False, nb_caractere=-1):

        if not attribut_252:
            qs_val = self.qs_111_val
            qs_ind = self.qs_111_ind
            numero = "111"
        else:
            qs_val = self.qs_252_val
            qs_ind = self.qs_252_ind
            numero = "252"

        texte = widget_combo.currentText()
        index_row = widget_combo.currentIndex()

        if index_row == -1 or texte == "":
            widget_combo.blockSignals(True)
            widget_combo.setCurrentText("")
            widget_index.setText("-1")
            widget_combo.blockSignals(False)

            self.mise_a_jour(qs_val=qs_val,
                             qs_ind=qs_ind,
                             number_current=numero,
                             widget_combo=widget_combo,
                             widget_index=widget_index)
            return

        if nb_caractere != -1:
            if len(texte) < nb_caractere:
                try:
                    texte = texte.zfill(nb_caractere)
                except Exception:
                    pass

        recherche = widget_combo.findText(texte, Qt.MatchExactly)

        if recherche == -1:
            widget_combo.blockSignals(True)
            widget_combo.setCurrentText(qs_val.text())
            widget_index.setText(qs_ind.text())
            widget_combo.blockSignals(False)

            return

        if recherche != index_row:
            numero_element = widget_combo.model().index(recherche, 0).data(Qt.DisplayRole)

        else:
            numero_element = widget_combo.model().index(index_row, 0).data(Qt.DisplayRole)

        widget_index.setText(numero_element)

        self.mise_a_jour(qs_val=qs_val,
                         qs_ind=qs_ind,
                         number_current=numero,
                         widget_combo=widget_combo,
                         widget_index=widget_index)

    def mise_a_jour(self, qs_val: QStandardItem, qs_ind: QStandardItem,
                    number_current: str, widget_combo: QComboBox, widget_index: QLabel):

        value_current = qs_val.text()
        value_new = widget_combo.currentText()

        value_index_current = qs_ind.text()
        value_index_new = widget_index.text()

        if value_current == value_new and value_index_current == value_index_new:
            return

        if not widget_combo.isVisible():
            return

        qs_val.setText(value_new)
        qs_ind.setText(value_index_new)

        # -------------

        qs_parent = self.qs_118.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_filling -- mise_a_jour -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_filling -- mise_a_jour -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_filling -- mise_a_jour -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = [AttributeModifyData(number_current=number_current,
                                              value_new=value_current,
                                              value_index_new=value_index_current)]

        value_dict = {number_current: [value_current, value_new]}

        # -------------

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, "")

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj in [self.ui.line_118, self.ui.line_hatching, self.ui.line_pattern, self.ui.line_color,
                   self.ui.line_picture, self.ui.line_style]:

            if event.type() == QEvent.FocusIn:

                self.ui.line_118.setStyleSheet("")
                self.ui.line_hatching.setStyleSheet("")
                self.ui.line_pattern.setStyleSheet("")
                self.ui.line_picture.setStyleSheet("")
                self.ui.line_style.setStyleSheet("")

            elif event.type() == QEvent.FocusOut:
                self.chb_change()

            return super().eventFilter(obj, event)

        if obj == self.ui.hachurage:

            if event.type() == QEvent.FocusOut:
                self.verification_datas_hachurage()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:

                if not self.ui.hachurage.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            event: QEvent.KeyPress

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

            return super().eventFilter(obj, event)

        if obj == self.ui.motif:

            if event.type() == QEvent.FocusOut:
                self.verification_datas_motif()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.motif.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            event: QEvent.KeyPress

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

            return super().eventFilter(obj, event)

        if obj == self.ui.couleur:

            if event.type() == QEvent.FocusOut:
                self.verification_datas_couleur()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.couleur.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            event: QEvent.KeyPress

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

            return super().eventFilter(obj, event)

        if obj == self.ui.surface and self.ui.surface.isEnabled():

            if event.type() == QEvent.MouseButtonDblClick:
                self.parcourir_surface()

            return super().eventFilter(obj, event)

        if obj == self.ui.style:

            if event.type() == QEvent.FocusOut:
                self.verification_datas_style()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.style.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            event: QEvent.KeyPress

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

            return super().eventFilter(obj, event)

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
