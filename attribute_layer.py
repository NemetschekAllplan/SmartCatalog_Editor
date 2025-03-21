#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from allplan_manage import AllplanDatas
from history_manage import AttributeModifyData
from main_datas import user_guid
from tools import ValidatorDouble, get_look_combobox
from tools import ValidatorInt
from tools import set_appareance_button, ValidatorModel
from ui_attribute_layer import Ui_AttributeLayer
from structure_widget import WidgetStructure


class AttributeLayer(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict, str)

    def __init__(self, asc):
        super().__init__()

        # Chargement du widget + setup
        self.ui = Ui_AttributeLayer()
        self.ui.setupUi(self)

        self.type_element = "type_ligne"

        self.row_index = 0

        self.asc = asc

        self.widget_popup = WidgetStructure(self.asc)
        self.widget_popup.layer_modif.connect(self.popup_enregitrer)

        self.allplan: AllplanDatas = self.asc.allplan

        self.qs_141_ind = QStandardItem()
        self.qs_141_val = QStandardItem()

        self.qs_349 = QStandardItem()

        self.qs_346_ind = QStandardItem()
        self.qs_346_val = QStandardItem()

        self.qs_345_ind = QStandardItem()
        self.qs_345_val = QStandardItem()

        self.qs_347_ind = QStandardItem()
        self.qs_347_val = QStandardItem()

        self.listwidgetitem = QListWidgetItem()

        self.model_layers_view = self.allplan.model_layers_view

        # ---------------------------------------
        # LAYER
        # ---------------------------------------

        self.filtre_layer = QSortFilterProxyModel()
        self.filtre_layer.setSourceModel(self.allplan.model_layers)
        self.filtre_layer.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_layer.setFilterKeyColumn(1)

        self.ui.value_141.setModel(self.allplan.model_layers)
        self.ui.value_141.setModelColumn(1)

        qcompleter_141 = self.ui.value_141.completer()
        qcompleter_141.setModel(self.filtre_layer)
        qcompleter_141.setCompletionColumn(1)
        qcompleter_141.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_141.setCaseSensitivity(Qt.CaseInsensitive)

        self.ui.value_141.setValidator(ValidatorModel(model=self.allplan.model_layers, column_index=1))

        self.ui.value_141.lineEdit().textEdited.connect(self.filtre_layer.setFilterFixedString)
        self.ui.value_141.currentIndexChanged.connect(self.changement_layer)

        get_look_combobox(self.ui.value_141)

        self.ui.value_141.installEventFilter(self)

        # ---------------------------------------
        # STYLE DE LIGNE
        # ---------------------------------------

        self.ui.value_349_stroke.clicked.connect(self.changement_chb)
        get_look_combobox(self.ui.value_349_stroke)

        self.ui.value_349_pen.clicked.connect(self.changement_chb)
        get_look_combobox(self.ui.value_349_pen)

        self.ui.value_349_color.clicked.connect(self.changement_chb)
        get_look_combobox(self.ui.value_349_color)

        # ---------------------------------------
        # EPAISSEUR
        # ---------------------------------------

        self.filtre_346 = QSortFilterProxyModel()
        self.filtre_346.setSourceModel(self.allplan.model_pen)
        self.filtre_346.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_346.setFilterKeyColumn(1)

        self.ui.value_346.setModel(self.allplan.model_pen)
        self.ui.value_346.setModelColumn(1)

        qcompleter_346 = self.ui.value_346.completer()
        qcompleter_346.setModel(self.filtre_346)
        qcompleter_346.setCompletionColumn(1)
        qcompleter_346.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_346.setCaseSensitivity(Qt.CaseInsensitive)
        qcompleter_346.popup().setIconSize(QSize(200, 18))

        self.ui.value_346.setValidator(ValidatorDouble())

        self.ui.value_346.lineEdit().textEdited.connect(self.filtre_346.setFilterFixedString)
        self.ui.value_346.currentIndexChanged.connect(self.changement_epaisseur)

        self.ui.value_346.installEventFilter(self)
        self.ui.value_346.lineEdit().installEventFilter(self)

        # ---------------------------------------
        # TYPE DE LIGNE
        # ---------------------------------------

        self.filtre_345 = QSortFilterProxyModel()
        self.filtre_345.setSourceModel(self.allplan.model_line)
        self.filtre_345.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_345.setFilterKeyColumn(1)

        self.ui.value_345.setModel(self.allplan.model_line)
        self.ui.value_345.setModelColumn(1)

        qcompleter_345 = self.ui.value_345.completer()
        qcompleter_345.setModel(self.filtre_345)
        qcompleter_345.setCompletionColumn(1)
        qcompleter_345.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_345.setCaseSensitivity(Qt.CaseInsensitive)
        qcompleter_345.popup().setIconSize(QSize(200, 18))

        self.ui.value_345.setValidator(ValidatorInt())

        self.ui.value_345.lineEdit().textEdited.connect(self.filtre_345.setFilterFixedString)
        self.ui.value_345.currentIndexChanged.connect(self.changement_type)

        self.ui.value_345.installEventFilter(self)
        self.ui.value_345.lineEdit().installEventFilter(self)

        # ---------------------------------------
        # COULEUR DE LIGNE
        # ---------------------------------------

        self.filtre_347 = QSortFilterProxyModel()
        self.filtre_347.setSourceModel(self.allplan.model_color)
        self.filtre_347.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_347.setFilterKeyColumn(1)

        self.ui.value_347.setModel(self.allplan.model_color)
        self.ui.value_347.setModelColumn(1)

        qcompleter_347 = self.ui.value_347.completer()
        qcompleter_347.setModel(self.filtre_347)
        qcompleter_347.setCompletionColumn(1)
        qcompleter_347.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_347.setCaseSensitivity(Qt.CaseInsensitive)
        qcompleter_347.popup().setIconSize(QSize(200, 18))

        self.ui.value_347.setValidator(ValidatorInt())

        self.ui.value_347.lineEdit().textEdited.connect(self.filtre_347.setFilterFixedString)
        self.ui.value_347.currentIndexChanged.connect(self.changement_couleur)

        self.ui.value_347.installEventFilter(self)
        self.ui.value_347.lineEdit().installEventFilter(self)

        # ---------------------------------------

        self.ui.lock_141.clicked.connect(self.afficher_choix_layer)
        set_appareance_button(self.ui.lock_141)

        # ---------------------------------------

        self.ui.line_141.installEventFilter(self)
        self.ui.line_349.installEventFilter(self)
        self.ui.line_346.installEventFilter(self)
        self.ui.line_345.installEventFilter(self)
        self.ui.line_347.installEventFilter(self)

    @staticmethod
    def a___________________chargement______():
        pass

    def chargement(self, row_index: int):

        self.row_index = row_index

        val_141_ind = self.qs_141_ind.text()
        val_141_val = self.qs_141_val.text()

        val_349 = self.qs_349.text()

        val_346_ind = self.qs_346_ind.text()
        val_346_val = self.qs_346_val.text()

        val_345_ind = self.qs_345_ind.text()
        val_345_val = self.qs_345_val.text()

        val_347_ind = self.qs_347_ind.text()
        val_347_val = self.qs_347_val.text()

        self.ui.index_141.setText(val_141_ind)

        index_141 = self.recherche_index(self.ui.value_141, val_141_val)
        self.ui.value_141.setCurrentIndex(index_141)

        self.ui.index_349.setText(val_349)

        self.ui.index_346.setText(val_346_ind)
        index_346 = self.recherche_index(self.ui.value_346, val_346_val)
        self.ui.value_346.setCurrentIndex(index_346)

        self.ui.index_345.setText(val_345_ind)
        index_345 = self.recherche_index(self.ui.value_345, val_345_val)
        self.ui.value_345.setCurrentIndex(index_345)

        self.ui.index_347.setText(val_347_ind)
        index_347 = self.recherche_index(self.ui.value_347, val_347_val)
        self.ui.value_347.setCurrentIndex(index_347)

        self.gestion_checkbox()
        self.chargement_style()

    @staticmethod
    def recherche_index(combo: QComboBox, texte: str) -> int:

        recherche = combo.findText(texte)

        return recherche

    def chargement_style(self):

        if self.ui.index_141.text() == "0":
            self.ui.value_349_stroke.setChecked(False)
            self.ui.value_349_pen.setChecked(False)
            self.ui.value_349_color.setChecked(False)
            self.changement_chb()
            return

        numero_style = self.ui.index_349.text()

        if numero_style == "1":
            self.ui.value_349_stroke.setChecked(True)
            self.ui.value_349_pen.setChecked(False)
            self.ui.value_349_color.setChecked(False)
            self.changement_chb()
            return

        if numero_style == "2":
            self.ui.value_349_stroke.setChecked(False)
            self.ui.value_349_pen.setChecked(True)
            self.ui.value_349_color.setChecked(False)
            self.changement_chb()
            return

        if numero_style == "3":
            self.ui.value_349_stroke.setChecked(True)
            self.ui.value_349_pen.setChecked(True)
            self.ui.value_349_color.setChecked(False)
            self.changement_chb()
            return

        if numero_style == "4":
            self.ui.value_349_stroke.setChecked(False)
            self.ui.value_349_pen.setChecked(False)
            self.ui.value_349_color.setChecked(True)
            self.changement_chb()
            return

        if numero_style == "5":
            self.ui.value_349_stroke.setChecked(True)
            self.ui.value_349_pen.setChecked(False)
            self.ui.value_349_color.setChecked(True)
            self.changement_chb()
            return

        if numero_style == "6":
            self.ui.value_349_stroke.setChecked(False)
            self.ui.value_349_pen.setChecked(True)
            self.ui.value_349_color.setChecked(True)
            self.changement_chb()
            return

        if numero_style == "7":
            self.ui.value_349_stroke.setChecked(True)
            self.ui.value_349_pen.setChecked(True)
            self.ui.value_349_color.setChecked(True)
            self.changement_chb()
            return

        self.ui.value_349_stroke.setChecked(False)
        self.ui.value_349_pen.setChecked(False)
        self.ui.value_349_color.setChecked(False)
        self.changement_chb()

    def gestion_checkbox(self):

        numero_layer = self.ui.index_141.text()
        status = numero_layer != "0"

        self.ui.line_349.setVisible(status)

        self.manage_row_color()

        if status:
            return

        self.ui.value_349_stroke.setChecked(False)
        self.ui.value_349_pen.setChecked(False)
        self.ui.value_349_color.setChecked(False)

        self.ui.index_349.setText("0")
        self.mise_a_jour_chb()

    def manage_row_color(self):

        row_index = self.row_index

        # ----- 141 -----

        self.ui.line_141.setStyleSheet(f"QWidget#line_141 {self.get_color_row(row_index=row_index)}")
        row_index += 1

        # ----- 349 -----

        if self.ui.index_141.text() != "0":
            self.ui.line_349.setStyleSheet(f"QWidget#line_349 {self.get_color_row(row_index=row_index)}")
            row_index += 1

        # ----- 346 -----

        if not self.ui.value_349_stroke.isChecked():
            self.ui.line_346.setStyleSheet(f"QWidget#line_346 {self.get_color_row(row_index=row_index)}")
            row_index += 1

        # ----- 345 -----

        if not self.ui.value_349_pen.isChecked():
            self.ui.line_345.setStyleSheet(f"QWidget#line_345 {self.get_color_row(row_index=row_index)}")
            row_index += 1

        # ----- 347 -----

        if not self.ui.value_349_color.isChecked():
            self.ui.line_347.setStyleSheet(f"QWidget#line_347 {self.get_color_row(row_index=row_index)}")
            row_index += 1

    @staticmethod
    def get_color_row(row_index: int) -> str:
        return

        # if row_index % 2 == 0:
        #     return "{background-color: #fff}"
        # return "{background-color: #e9e7e3}"

    @staticmethod
    def a___________________popup______():
        pass

    def afficher_choix_layer(self):

        self.asc.formula_widget_close()

        self.widget_popup.widget_structure_show(current_mode="layer",
                                                current_model=self.model_layers_view,
                                                current_combo_model=self.ui.value_141.model(),
                                                curennt_index=self.ui.index_141.text())

    def popup_enregitrer(self, numero: str, valeur: str):

        self.ui.index_141.setText(numero)
        self.ui.value_141.setCurrentText(valeur)

        self.changement_layer()

    @staticmethod
    def a___________________changement_chb______():
        pass

    def changement_chb(self):

        chb_plume = self.ui.value_349_stroke.isChecked()

        self.ui.line_346.setVisible(not chb_plume)

        chb_345 = self.ui.value_349_pen.isChecked()

        self.ui.line_345.setVisible(not chb_345)

        chb_coul = self.ui.value_349_color.isChecked()

        self.ui.line_347.setVisible(not chb_coul)

        self.manage_row_color()

        try:
            self.listwidgetitem.setSizeHint(self.sizeHint())
        except RuntimeError:
            pass

        if chb_plume and not chb_345 and not chb_coul:
            self.ui.index_349.setText("1")

        elif not chb_plume and chb_345 and not chb_coul:
            self.ui.index_349.setText("2")

        elif chb_plume and chb_345 and not chb_coul:
            self.ui.index_349.setText("3")

        elif not chb_plume and not chb_345 and chb_coul:
            self.ui.index_349.setText("4")

        elif chb_plume and not chb_345 and chb_coul:
            self.ui.index_349.setText("5")

        elif not chb_plume and chb_345 and chb_coul:
            self.ui.index_349.setText("6")

        elif chb_plume and chb_345 and chb_coul:
            self.ui.index_349.setText("7")
        else:

            self.ui.index_349.setText("0")

        self.mise_a_jour_chb()

    def mise_a_jour_chb(self):

        value_current = self.qs_349.text()
        value_new = self.ui.index_349.text()

        if value_current == value_new:
            return

        if not self.ui.index_349.isVisible():
            return

        self.qs_349.setText(value_new)

        numero_layer = self.ui.index_141.text()

        if numero_layer == 0:
            return

        # -------------

        qs_parent = self.qs_141_val.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_date -- date_update -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_date -- date_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_date -- date_update -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_type = self.tr("Groupe Layer")
        attribute_data = [AttributeModifyData(number_current="349", value_new=value_current)]
        value_dict = {"349": [value_current, value_new]}

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, attribute_type)

    @staticmethod
    def a___________________changement_combo______():
        pass

    def mise_a_jour(self, qs_val: QStandardItem, qs_ind: QStandardItem,
                    number_current: str, widget_combo: QComboBox, widget_index: QLabel):

        value_current = qs_val.text()
        value_new = widget_combo.currentText()

        value_index_current = qs_ind.text()
        value_index_new = widget_index.text()

        if value_current == value_new and value_index_current == value_index_new:
            return

        # -------------

        if not widget_combo.isVisible():
            return

        # -------------

        qs_val.setText(value_new)
        qs_ind.setText(value_index_new)

        # -------------

        qs_parent = self.qs_141_val.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_date -- date_update -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_date -- date_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_date -- date_update -- not isinstance(parent_name, str)")
            return

        # -------------

        data = AttributeModifyData(number_current=number_current,
                                   value_new=value_current,
                                   value_index_new=value_index_current,
                                   guid_desc=None)

        attribute_data = [data]

        # -------------

        value_dict = {number_current: [value_current, value_new]}

        # -------------

        attribute_type = self.tr("Groupe Layer")

        # -------------

        if number_current != "141":
            self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, attribute_type)
            return

        # -------------

        if value_index_new != "0":
            self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, attribute_type)
            return

        # -------------

        chb_style = self.ui.index_349.text()

        if chb_style == 0:
            self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, attribute_type)
            return

        # -------------

        value_current_349 = self.qs_349.text()

        value_dict["349"] = [value_current_349, "0"]

        data = AttributeModifyData(number_current="349",
                                   value_new=value_current_349)

        attribute_data.append(data)

        # -------------

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, attribute_type)

    @staticmethod
    def a___________________changement_donnees______():
        pass

    def verification_datas(self, qs_val: QStandardItem, qs_ind: QStandardItem,
                           numero: str, widget_combo: QComboBox, widget_index: QLabel,
                           nb_caractere=-1):

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
                    texte = texte.zfill(2)
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

    def changement_layer(self):

        self.verification_datas(qs_val=self.qs_141_val,
                                qs_ind=self.qs_141_ind,
                                numero="141",
                                widget_combo=self.ui.value_141,
                                widget_index=self.ui.index_141)

        self.gestion_checkbox()
        self.chargement_style()

        return

    def changement_epaisseur(self):

        self.verification_datas(qs_val=self.qs_346_val,
                                qs_ind=self.qs_346_ind,
                                numero="346",
                                widget_combo=self.ui.value_346,
                                widget_index=self.ui.index_346)

        return

    def changement_type(self):
        """Permet d'appliquer les modifications"""

        self.verification_datas(qs_val=self.qs_345_val,
                                qs_ind=self.qs_345_ind,
                                numero="345",
                                widget_combo=self.ui.value_345,
                                widget_index=self.ui.index_345,
                                nb_caractere=2)

        return

    def changement_couleur(self):

        self.verification_datas(qs_val=self.qs_347_val,
                                qs_ind=self.qs_347_ind,
                                numero="347",
                                widget_combo=self.ui.value_347,
                                widget_index=self.ui.index_347)

        return

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj in [self.ui.line_141, self.ui.line_349, self.ui.line_346, self.ui.line_345,
                   self.ui.line_347]:

            if event.type() == QEvent.FocusIn:

                self.ui.line_141.setStyleSheet("")
                self.ui.line_349.setStyleSheet("")
                self.ui.line_346.setStyleSheet("")
                self.ui.line_345.setStyleSheet("")
                self.ui.line_347.setStyleSheet("")

            elif event.type() == QEvent.FocusOut:
                self.manage_row_color()

            return super().eventFilter(obj, event)

        if obj == self.ui.value_141:

            if event.type() == QEvent.FocusOut:
                self.changement_layer()

                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.value_141.hasFocus():
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

        # -----------------------
        #  Epaisseur de traits
        # -----------------------

        elif obj == self.ui.value_346:

            if event.type() == QEvent.FocusOut:
                self.changement_epaisseur()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.value_346.hasFocus():
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

        elif obj == self.ui.value_346.lineEdit():

            if event.type() != QEvent.MouseButtonDblClick:
                return super().eventFilter(obj, event)

            if self.ui.value_346.isEnabled():
                return super().eventFilter(obj, event)

            self.ui.value_349_stroke.setChecked(False)
            self.changement_chb()

            self.ui.value_346.showPopup()

            return super().eventFilter(obj, event)

        # -----------------------
        #  Type de traits
        # -----------------------

        elif obj == self.ui.value_345:

            if event.type() == QEvent.FocusOut:
                self.changement_type()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.value_345.hasFocus():
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

        elif obj == self.ui.value_345.lineEdit():

            if event.type() != QEvent.MouseButtonDblClick:
                return super().eventFilter(obj, event)

            if self.ui.value_345.isEnabled():
                return super().eventFilter(obj, event)

            self.ui.value_349_pen.setChecked(False)
            self.changement_chb()

            self.ui.value_345.showPopup()

            return super().eventFilter(obj, event)

        # -----------------------
        #  Couleur de traits
        # -----------------------

        elif obj == self.ui.value_347:

            if event.type() == QEvent.FocusOut:
                self.changement_couleur()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.value_347.hasFocus():
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

        elif obj == self.ui.value_347.lineEdit():

            if event.type() != QEvent.MouseButtonDblClick:
                return super().eventFilter(obj, event)

            if self.ui.value_347.isEnabled():
                return super().eventFilter(obj, event)

            self.ui.value_349_color.setChecked(False)
            self.changement_chb()

            self.ui.value_347.showPopup()

            return super().eventFilter(obj, event)

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
