#!/usr/bin/python3
# -*- coding: utf-8 -*


from catalog_manage import *
from formula_favorite import FormulaFavorite
from tools import find_global_point, set_appareance_button, MyContextMenu
from tools import set_appearance_number, set_appearence_type, recherche_image, settings_save
from ui_attribute_formula import Ui_AttributeFormula


class AttributeFormula(QWidget):
    formula_changed = pyqtSignal()
    formula_corrected = pyqtSignal(Attribute, str, str)
    attribute_changed_signal = pyqtSignal(str, list, str, dict)

    def __init__(self, asc, qs_value: MyQstandardItem, attribute_obj: AttributeDatas, listwidgetitem: QListWidgetItem):
        super().__init__()

        # ---------------------------------------
        # Interface
        # ---------------------------------------

        self.ui = Ui_AttributeFormula()
        self.ui.setupUi(self)

        set_appareance_button(self.ui.formula_editor_bt)
        set_appareance_button(self.ui.formula_verification_bt)
        set_appareance_button(self.ui.formula_color_bt)
        set_appareance_button(self.ui.formula_favorite_bt)

        # ----------------------------------

        if isinstance(attribute_obj, AttributeDatas):

            self.ui.num_attrib.setText(attribute_obj.number)

            self.ui.name_attrib.setText(attribute_obj.name)
            self.ui.name_attrib.setToolTip(attribute_obj.tooltips)

            self.attrib_option = attribute_obj.option

        else:

            self.attrib_option = code_attr_str

        # ---------------------------------------
        # Variables
        # ---------------------------------------

        self.asc = asc

        self.allplan: AllplanDatas = self.asc.allplan
        self.catalogue: CatalogDatas = self.asc.catalog

        self.user_attribute = False

        self.max_row = 7
        self.adjust_height_active = False
        self.adjust_height_action = False

        self.listwidgetitem = listwidgetitem

        self.search_error_active = False

        # ---------------------------------------
        # CREATEUR DE FORMULES
        # ---------------------------------------

        self.widget_creation_formule = self.asc.formula_editor_widget

        self.widget_creation_formule.modif_formule.connect(self.retour_widget_formule)
        self.widget_creation_formule.close_event.connect(self.fermeture_formule)

        self.widget_formule_visible = False

        # ---------------------------------------
        # FAVORIS DE FORMULES
        # ---------------------------------------

        self.widget_formula_fav: FormulaFavorite = self.asc.formula_fav_widget

        # ---------------------------------------
        # QPlainText formule
        # ---------------------------------------

        self.ui.value_attrib.chargement(self.allplan)

        # ---------------------------------------
        # Bouton couleur
        # ---------------------------------------

        self.ui.formula_color_bt.clicked.connect(self.catalogue.change_highlighter)
        self.catalogue.formula_color_change_signal.connect(self.ui.value_attrib.change_highlighter_action)

        self.catalogue.formula_size_change_signal.connect(self.ui.value_attrib.setsize)

        # ---------------------------------------
        # Bouton favoris
        # ---------------------------------------

        self.ui.formula_favorite_bt.clicked.connect(self.formule_menu)
        self.ui.formula_favorite_bt.customContextMenuRequested.connect(self.formule_menu)

        # ---------------------------------------
        # chargement datas
        # ---------------------------------------

        self.qs_value = qs_value

        self.ui.value_attrib.setPlainText(self.qs_value.text())
        self.ui.value_attrib.size_change.connect(self.adjust_height)

        # ---------------------------------------
        # ATTRIBUT FORMULE - SIGNAUX
        # ---------------------------------------

        self.ui.value_attrib.textChanged.connect(self.text_changed)
        self.ui.value_attrib.editingFinished.connect(self.mise_a_jour)

        # ---------------------------------------
        # Editeur de formule
        # ---------------------------------------

        self.ui.formula_editor_bt.clicked.connect(self.ouvrir_createur_formule)

        # ---------------------------------------

    @staticmethod
    def a___________________formula_loading______():
        pass

    def chargement(self, search_error_active: bool):

        self.search_error_active = search_error_active

        set_appearance_number(self.ui.num_attrib)
        set_appearence_type(self.ui.type_attrib, self.attrib_option)

        if self.ui.num_attrib.toolTip() == self.tr("Attribut utilisateur"):
            self.ui.value_attrib.setReadOnly(True)
            self.ui.formula_editor_bt.setEnabled(False)
            self.ui.formula_verification_bt.setToolTip(self.tr("Formule à modifier directement depuis Allplan"))

            self.ui.value_attrib.setStyleSheet("background-color: Lightgrey")

            self.user_attribute = True

        self.ui.formula_verification_bt.verification(texte=self.ui.value_attrib.toPlainText(), allplan=self.allplan)
        self.count_nb_chars()

        self.adjust_height()

    @staticmethod
    def a___________________changement______():
        pass

    def text_changed(self):

        if self.widget_formule_visible:
            return

        self.ui.value_attrib.blockSignals(True)

        # self.ui.value_attrib.formula_format_check()

        # ---------------------------------------
        # GESTION DE L'ICONE DE VERIF FORMULE
        # ---------------------------------------

        self.ui.formula_verification_bt.verification(texte=self.ui.value_attrib.toPlainText(),
                                                     allplan=self.allplan)

        if self.ui.formula_verification_bt.isvalid:
            self.ui.value_attrib.setStyleSheet("QPlainTextEdit{border: 1px solid #8f8f91; "
                                               "border-right-width: 0px; "
                                               "padding-left: 5px; "
                                               "padding-right: 5px; "
                                               "padding-top: 1px; "
                                               "padding-bottom: 1px; "
                                               "border-top-left-radius: 5px; "
                                               "border-bottom-left-radius: 5px; "
                                               "background-color: #FFFFFF; }")

        else:
            self.ui.value_attrib.setStyleSheet("QPlainTextEdit{border: 2px solid orange; "
                                               "padding-left: 4px; "
                                               "padding-right: 3px; "
                                               "padding-top: 0px; "
                                               "padding-bottom: 0px; "
                                               "border-top-left-radius: 5px; "
                                               "border-bottom-left-radius: 5px; "
                                               "background-color: #FFFFFF; }")

        # ---------------------------------------
        # GESTION DU TOOLTIP DE LA LINEEDIT
        # ---------------------------------------

        message_actuel = self.qs_value.data(user_formule_ok)
        message_futur = self.ui.formula_verification_bt.toolTip()

        if message_futur == self.tr("C'est tout bon!"):
            message_futur = ""

        if message_actuel != message_futur and isinstance(self.qs_value, Attribute):

            self.qs_value.setData(message_futur, user_formule_ok)

        if message_futur == "" and self.search_error_active:

            self.formula_corrected.emit(self.qs_value, self.ui.num_attrib.text(), self.ui.value_attrib.toPlainText())

            self.mise_a_jour()

            self.formula_changed.emit()

            self.ui.value_attrib.autocompletion.hide()

        self.count_nb_chars()

        self.ui.value_attrib.blockSignals(False)

        self.adjust_height()

    def count_nb_chars(self):

        nb_char = len(self.ui.value_attrib.toPlainText())

        if nb_char < 2:
            a = self.tr("caractère")
            self.ui.nb_char.setText(f'{nb_char} {a}')
        else:
            a = self.tr("caractères")
            self.ui.nb_char.setText(f'{nb_char} {a}')

    def mise_a_jour(self):

        value_current = self.qs_value.text()
        value_new = self.ui.value_attrib.toPlainText()

        if value_current == value_new:
            return

        # -------------

        self.qs_value.setText(value_new)

        # -------------

        number_current = self.ui.num_attrib.text()

        value_dict = {number_current: [value_current, value_new]}

        # -------------

        qs_parent = self.qs_value.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("formula_attribute -- mise_a_jour -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("formula_attribute -- mise_a_jour -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("formula_attribute -- mise_a_jour -- not isinstance(parent_name, str)")
            return

        # -------------

        data = AttributeModifyData(number_current=number_current, value_new=value_current)

        attribute_data = [data]

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict)

    @staticmethod
    def a___________________lineedit_height______():
        pass

    def adjust_height(self):

        self.adjust_height_action = True

        if self.adjust_height_active:
            self.adjust_height_action = False
            return

        font = self.ui.value_attrib.document().defaultFont()
        fontmetrics = QFontMetrics(font)
        espace = fontmetrics.lineSpacing()
        border = 9

        row_count = round(self.ui.value_attrib.document().size().height())

        if row_count <= self.max_row:

            if self.ui.value_attrib.verticalScrollBarPolicy() != Qt.ScrollBarAlwaysOff:
                self.ui.value_attrib.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.ui.value_attrib.verticalScrollBar().setValue(0)

        else:

            row_count = self.max_row

            self.ui.value_attrib.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # ------------------------------

        height_plaintext = (row_count * espace) + border

        if height_plaintext < 100:
            height_plaintext = 100

        height_widget = height_plaintext + 14

        # ------------------------------

        self.ui.value_attrib.setFixedHeight(height_plaintext)

        self.update()

        label_height = (height_plaintext - self.ui.formula_editor_bt.height() -
                        self.ui.formula_verification_bt.height())

        self.ui.nb_char.setFixedHeight(label_height)

        # ------------------------------

        try:

            self.listwidgetitem.setSizeHint(QSize(self.width(), height_widget))

        except Exception:
            pass

        self.adjust_height_action = False

    def adjust_width(self):

        if not self.isVisible():
            return

        self.adjustSize()

    @staticmethod
    def a___________________gestion_createur_formule______():
        pass

    def ouvrir_createur_formule(self):

        self.asc.formula_widget_close()

        self.set_buttons_enable(False)

        self.widget_creation_formule.show_formula(value_widget=self.ui.value_attrib,
                                                  parent_actuel=self.asc,
                                                  number=self.ui.num_attrib.text(),
                                                  bt_favoris=True)

        self.widget_formule_visible = True

    def fermeture_formule(self):
        self.ui.value_attrib.autocompletion.hide()
        self.widget_formule_visible = False
        self.set_buttons_enable(True)

    def retour_widget_formule(self, value_widget: QPlainTextEdit, formule: str, position_cursor: int):

        if value_widget != self.ui.value_attrib:
            return

        self.ui.value_attrib.setPlainText(formule)
        self.mise_a_jour()

        self.ui.value_attrib.setFocus()

        cursor = self.ui.value_attrib.textCursor()
        cursor.setPosition(position_cursor, QTextCursor.MoveAnchor)
        self.ui.value_attrib.setTextCursor(cursor)

        self.set_buttons_enable(True)

    def set_buttons_enable(self, enable: bool):

        self.ui.value_attrib.setEnabled(enable)
        self.ui.formula_editor_bt.setEnabled(enable)
        self.ui.formula_verification_bt.setEnabled(enable)
        self.ui.formula_color_bt.setEnabled(enable)
        self.ui.formula_favorite_bt.setEnabled(enable)

    @staticmethod
    def a___________________favoris______():
        pass

    def formule_menu(self):

        self.asc.formula_widget_close()

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            self.afficher_widget_favoris()
            return

        menu = MyContextMenu(tooltips_visible=False)

        menu.add_title(title=self.tr("Favoris Formule"))

        menu.add_action(qicon=get_icon(formula_favorite_icon),
                        title=self.tr("Ouvrir le gestionnaire de vos favoris"),
                        action=self.afficher_widget_favoris)

        menu.addSeparator()

        datas = settings_read(formula_fav_config_file)

        if len(datas) == 0:
            datas = self.widget_formula_fav.formula_initialization()

        liste_qmenu = list()

        a = self.tr("Enregistrer cette formule dans")

        for family_title, family_datas in datas.items():

            family_datas: dict

            family_icon = family_datas.get("icon", "")

            family_icon = recherche_image(image_name=family_icon, image_default="attribute_model_show.svg")

            item = MyContextMenu(title=family_title, qicon=get_icon(family_icon), tooltips_visible=False)

            item.add_action(qicon=get_icon(save_icon),
                            title=f"{a} '{family_title}'",
                            action=lambda val=family_title: self.formule_ajouter_favoris(val))

            if self.user_attribute:
                liste_qmenu.append(item)
                continue

            family_formulas: dict = family_datas.get("formulas", dict())

            for formula_name, formula in family_formulas.items():
                item.add_action(qicon=get_icon(family_icon),
                                title=formula_name,
                                action=lambda val=formula: self.formule_ajouter(val),
                                tooltips=self.allplan.traduction_formule_allplan(formula))

            liste_qmenu.append(item)

        for item in liste_qmenu:
            menu.addMenu(item)

        menu.exec_(find_global_point(self.ui.formula_favorite_bt))

    def afficher_widget_favoris(self):
        self.widget_formula_fav.formula_fav_personnaliser(parent_actuel=self.asc)

    def formule_ajouter(self, formule: str):
        self.ui.value_attrib.setPlainText(formule)
        self.mise_a_jour()

    def formule_ajouter_favoris(self, nom_onglet: str):

        formula = self.ui.value_attrib.toPlainText()

        formula_name = self.save_config_add_item(nom_onglet=nom_onglet,
                                                 formula=formula)

        if formula_name == "":
            return

        a = self.tr("La formule a bien été ajoutée à vos favoris")
        b = self.tr("Voulez-vous ouvrir le gestionnaire de favoris de formules")

        if msg(titre=application_title,
               message=f"{a}.\n{b} ?",
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               defaut_bouton=QMessageBox.Ok,
               icone_question=True) == QMessageBox.Ok:
            self.widget_formula_fav.formula_fav_personnaliser(parent_actuel=self.asc,
                                                              nom_onglet=nom_onglet,
                                                              formula_name=formula_name)

    def save_config_add_item(self, nom_onglet: str, formula: str) -> str:

        datas_elements = settings_read(formula_fav_config_file)

        if not isinstance(datas_elements, dict):
            print("formula_favorite -- save_config_add_item -- not isinstance(datas_elements, dict)")
            return ""

        formula_titles_list = list()
        datas_current_formula = None

        for tab_name, datas_tab in datas_elements.items():

            if not isinstance(datas_tab, dict):
                print("formula_favorite -- save_config_add_item -- not isinstance(datas_tab, dict)")
                continue

            if "formulas" not in datas_tab:
                print("formula_favorite -- save_config_add_item -- formulas not in datas_tab")
                continue

            datas_formula = datas_tab["formulas"]

            if not isinstance(datas_formula, dict):
                print("formula_favorite -- save_config_add_item -- not isinstance(datas_formula, dict)")
                continue

            formula_titles_list.extend(list(datas_formula))

            if tab_name == nom_onglet:
                datas_current_formula = datas_formula

        if not isinstance(datas_current_formula, dict):
            print("formula_favorite -- save_config_add_item -- not isinstance(datas_current_formula, dict)")
            return ""

        formula_name = self.tr("Formule")
        formula_name = f"{formula_name} 01"

        if len(formula_titles_list) != 0:
            formula_name = find_new_title(base_title=formula_name, titles_list=formula_titles_list)

        datas_current_formula[formula_name] = formula

        settings_save(formula_fav_config_file, datas_elements)

        return formula_name

    @staticmethod
    def a___________________event______():
        pass

    def resizeEvent(self, event):

        super().resizeEvent(event)

        if not self.isVisible():
            return

        if not self.adjust_height_action:
            self.adjust_height()

    # def eventFilter(self, obj: QWidget, event: QEvent):
    #
    #     if obj != self.ui.value_attrib:
    #         return super().eventFilter(obj, event)
    #
    #     if event.type() != QEvent.FocusOut:
    #         return super().eventFilter(obj, event)
    #
    #     self.mise_a_jour()
    #     return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
