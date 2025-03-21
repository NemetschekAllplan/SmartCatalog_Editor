#!/usr/bin/python3
# -*- coding: utf-8 -*


from allplan_manage import *
from attribute_add import AttributesWidget, NumericSortProxyModel
from catalog_manage import CatalogDatas
from tools import get_look_tableview, move_window_tool, recherche_image, get_look_combobox, qm_check, find_new_title
from tools import help_open_link
from tools import taille_police_menu, find_global_point, settings_save, MyContextMenu
from translation_manage import get_code_langue
from ui_finishing import Ui_Finishing
from ui_formula import Ui_Formula
from ui_formula_tool import Ui_WidgetFormulaTool

col_obj_code = 0
col_obj_formula = 1


class Formula(QWidget):
    modif_formule = pyqtSignal(QPlainTextEdit, str, int)
    close_event = pyqtSignal()

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # Interface
        # ---------------------------------------

        self.ui = Ui_Formula()
        self.ui.setupUi(self)

        # ---------------------------------------
        # Variables
        # ---------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.allplan: AllplanDatas = self.asc.allplan
        self.catalogue: CatalogDatas = self.asc.catalog

        self.number = ""
        self.formule_originale = ""

        self.value_widget = QPlainTextEdit()

        # ---------------------------------------
        # Settings
        # ---------------------------------------

        formula_set = settings_read(formula_setting_file)

        self.ismaximized_on = formula_set.get("ismaximized_on", False)
        self.resize(formula_set.get("width", 800), formula_set.get("height", 600))

        # ---------------------------------------
        # FAVORIS DE FORMULES
        # ---------------------------------------

        self.widget_formula_fav = self.asc.formula_fav_widget

        # ---------------------------------------
        # WIDGET - SECOND OEUVRE
        # ---------------------------------------

        self.widget_second_oeuvre = Finishing(self.asc)
        self.widget_second_oeuvre.finishing_formula_add.connect(self.formula_add_text)

        # ---------------------------------------
        # WIDGET - Functions
        # ---------------------------------------

        self.widget_function = FormulaTool(self.asc, current_mod="function")
        self.widget_function.add_formula.connect(self.formula_add_text)

        # ---------------------------------------
        # WIDGET - Objet
        # ---------------------------------------

        self.widget_objet = FormulaTool(self.asc, current_mod="object")
        self.widget_objet.add_formula.connect(self.formula_add_text)

        # ---------------------------------------
        # WIDGET - Métier
        # ---------------------------------------

        self.widget_metier = FormulaTool(self.asc, current_mod="trade")
        self.widget_metier.add_formula.connect(self.formula_add_text)

        # ---------------------------------------
        # WIDGET - Favoris
        # ---------------------------------------

        self.ui.bt_favoris.clicked.connect(self.formule_menu)
        self.ui.bt_favoris.customContextMenuRequested.connect(self.formule_menu)

        # ---------------------------------------
        # WIDGET - ATTRIBUT
        # ---------------------------------------

        self.widget_attribut: AttributesWidget = self.asc.attributes_widget
        self.widget_attribut.formula_creator_signal.connect(self.formula_add_text)

        # ---------------------------------------
        # QPlainText formule
        # ---------------------------------------

        self.ui.valeur_attr.chargement(self.allplan)
        self.ui.valeur_attr.textChanged.connect(self.changement)

        # ---------------------------------------
        # Bouton couleur
        # ---------------------------------------

        self.ui.bt_formule_couleur.clicked.connect(self.catalogue.change_highlighter)
        self.catalogue.formula_color_change_signal.connect(self.ui.valeur_attr.change_highlighter_action)

        self.ui.valeur_attr.size_change.connect(self.catalogue.formula_size_change_signal.emit)
        self.catalogue.formula_size_change_signal.connect(self.ui.valeur_attr.setsize)
        self.catalogue.formula_size_change_signal.connect(self.translate_formula_change_size)

        # ---------------------------------------
        # SIGNAUX - REFERENCE
        # ---------------------------------------

        self.ui.attribute_add.clicked.connect(self.attribute_show_clicked)

        self.ui.function.clicked.connect(self.function_menu_show)

        self.ui.operator_bt.clicked.connect(self.operator_menu_show)

        self.ui.finishing.clicked.connect(self.finish_show_clicked)

        self.ui.object.clicked.connect(self.object_show_clicked)

        self.ui.trade.clicked.connect(self.trade_show_clicked)

        self.ui.help.clicked.connect(self.bt_aide)
        self.ui.help.customContextMenuRequested.connect(self.bt_aide)

        # ---------------------------------------
        # SIGNAUX - BOUTONS
        # ---------------------------------------

        self.ui.ok.clicked.connect(self.formula_save)
        self.ui.quit.clicked.connect(self.close)

        font = self.ui.formule_convertie.font()
        font.setPointSize(taille_police_menu)
        self.ui.formule_convertie.setFont(font)

    def show_formula(self, value_widget: QPlainTextEdit, parent_actuel: QWidget, number="", bt_favoris=False):

        if not isinstance(value_widget, QPlainTextEdit) or not isinstance(parent_actuel, QWidget):
            print("formula -- Formula -- show_formula -- param is wrong")
            return

        if self.asc.library_widget.isVisible():
            self.asc.library_widget.close()

        self.value_widget = value_widget

        if number != "":
            self.setWindowModality(Qt.WindowModal)
        else:
            self.setWindowModality(Qt.ApplicationModal)

        self.number = number

        self.formule_originale = value_widget.toPlainText()

        position_cursor = value_widget.textCursor().position()

        self.ui.valeur_attr.setPlainText(self.formule_originale)

        self.changement()

        self.ui.valeur_attr.setFocus()

        cursor = self.ui.valeur_attr.textCursor()
        cursor.setPosition(position_cursor, QTextCursor.MoveAnchor)
        self.ui.valeur_attr.setTextCursor(cursor)

        self.ui.bt_favoris.setEnabled(bt_favoris)

        move_window_tool(widget_parent=parent_actuel, widget_current=self)

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

        if not self.isActiveWindow():
            self.raise_()

    def changement(self):

        formula = self.ui.valeur_attr.toPlainText()

        self.ui.bt_verif.verification(texte=formula, allplan=self.allplan)

        if self.ui.bt_verif.isvalid:

            self.ui.valeur_attr.setStyleSheet("QPlainTextEdit{border: 1px solid #8f8f91; "
                                              "border-right-width: 0px; "
                                              "padding-left: 5px; "
                                              "padding-right: 5px; "
                                              "padding-top: 1px; "
                                              "padding-bottom: 1px; "
                                              "border-top-left-radius: 5px; "
                                              "border-bottom-left-radius: 5px; "
                                              "background-color: #FFFFFF; }")

        else:

            self.ui.valeur_attr.setStyleSheet("QPlainTextEdit{border: 2px solid orange; "
                                              "padding-left: 4px; "
                                              "padding-right: 3px; "
                                              "padding-top: 0px; "
                                              "padding-bottom: 0px; "
                                              "border-top-left-radius: 5px; "
                                              "border-bottom-left-radius: 5px; "
                                              "background-color: #FFFFFF; }")

        formula_converted = self.allplan.traduction_formule_allplan(formula=formula, format_on=False)

        self.ui.formule_convertie.setText(formula_converted)

        self.translate_formula_change_size(self.ui.valeur_attr.currentsize)

        nb_char = len(formula)

        if nb_char < 2:
            a = self.tr("caractère")
            self.ui.nb_char.setText(f'{nb_char} {a}')
        else:
            a = self.tr("caractères")
            self.ui.nb_char.setText(f'{nb_char} {a}')

    @staticmethod
    def a___________________selection_changed_______________():
        pass

    def formula_selection_changed(self) -> str:

        if not self.isVisible():
            return ""

        self.formula_save_ask(close_action=False)
        return self.number

    @staticmethod
    def a___________________fermeture_______________():
        pass

    def formula_save(self):

        position = self.ui.valeur_attr.textCursor().position()

        self.close()

        self.modif_formule.emit(self.value_widget, self.ui.valeur_attr.toPlainText(), position)

    def formula_save_ask(self, close_action=False):

        formula = self.ui.valeur_attr.toPlainText()

        if formula == self.formule_originale:
            if close_action:
                self.close()
            return

        self.raise_()

        if msg(titre=application_title,
               message=self.tr("Voulez-vous enregistrer les modifications?"),
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               defaut_bouton=QMessageBox.Ok,
               icone_question=True) != QMessageBox.Ok:
            return

        position = self.ui.valeur_attr.textCursor().position()

        if close_action:
            self.close()

        self.modif_formule.emit(self.value_widget, formula, position)
        self.formule_originale = formula

    @staticmethod
    def a___________________favoris______():
        pass

    def formule_menu(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            self.afficher_widget_favoris()
            return

        menu = MyContextMenu()

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

            item = MyContextMenu(title=family_title, qicon=get_icon(family_icon))

            item.add_action(qicon=get_icon(save_icon),
                            title=f"{a} '{family_title}'",
                            action=lambda val=family_title: self.formule_ajouter_favoris(val))

            family_formulas: dict = family_datas.get("formulas", dict())

            for formula_name, formula in family_formulas.items():
                item.add_action(qicon=get_icon(family_icon),
                                title=formula_name,
                                action=lambda val=formula: self.formule_ajouter(val),
                                tooltips=self.allplan.traduction_formule_allplan(formula))

            liste_qmenu.append(item)

        for item in liste_qmenu:
            menu.addMenu(item)

        menu.exec_(find_global_point(self.ui.bt_favoris))

    def formule_ajouter(self, formule: str):
        self.ui.valeur_attr.setPlainText(formule)

    def afficher_widget_favoris(self):

        formule_actuelle = self.ui.valeur_attr.toPlainText()

        if formule_actuelle != self.formule_originale:
            reponse = msg(titre=self.windowTitle(),
                          message=self.tr("Voulez-vous enregistrer les modifications?"),
                          type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                          defaut_bouton=QMessageBox.Ok,
                          icone_sauvegarde=True)

            if reponse == QMessageBox.Cancel:
                return

            if reponse == QMessageBox.Ok:
                self.widget_formula_fav.formula_fav_show(parent_actuel=self)
                self.formula_save()
                return

        self.close()

        self.widget_formula_fav.formula_fav_personnaliser(parent_actuel=self.asc)

    def formule_ajouter_favoris(self, nom_onglet: str):

        formula = self.ui.valeur_attr.toPlainText()
        #
        # self.widget_formula_fav.favoris_fav_model_add(nom_onglet=nom_onglet,
        #                                               formula_name="",
        #                                               formula=formula,
        #                                               save=True)

        formula_name = self.save_config_add_item(nom_onglet=nom_onglet,
                                                 formula=formula)

        if formula_name == "":
            return

        a = self.tr("La formule a bien été ajoutée à vos favoris")
        b = self.tr("Voulez-vous ouvrir le gestionnaire de favoris de formules")

        # if msg(titre=self.windowTitle(),
        #        message=f"{a}.\n{b} ?",
        #        type_bouton=QMessageBox.Ok | QMessageBox.No,
        #        defaut_bouton=QMessageBox.Ok,
        #        icone_question=True) == QMessageBox.Ok:
        #     self.widget_formula_fav.formula_fav_personnaliser(parent_actuel=self.asc,
        #                                                       nom_onglet=nom_onglet)

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
    def a___________________attribute_______________():
        pass

    def attribute_show_clicked(self):
        self.widget_attribut.attribute_show(current_mod="Formula", current_widget=self)

    @staticmethod
    def a___________________function_______________():
        pass

    def function_menu_show(self):

        menu = MyContextMenu()

        menu.add_title(title=self.tr("Fonctions"))

        menu.add_action(qicon=get_icon(function_icon),
                        title=self.tr("Ouvrir l'aide"),
                        action=self.function_show)

        menu.addSeparator()

        function_list = self.widget_function.tool_get_function_list()

        categories_dict = dict()

        for sub_list in function_list:

            if not isinstance(sub_list, list):
                continue

            if len(sub_list) != 4:
                continue

            category = sub_list[3]

            if not isinstance(category, str):
                continue

            if category not in categories_dict:
                sub_menu = MyContextMenu(title=category, qicon=get_icon(help_icon))

                categories_dict[category] = sub_menu
            else:
                sub_menu = categories_dict[category]

            if not isinstance(sub_menu, MyContextMenu):
                continue

            sub_menu.add_action(title=sub_list[0],
                                action=lambda x=sub_list[0]: self.formula_add_text(x),
                                tooltips=f"{sub_list[1]}\n{sub_list[2]}")

        for sub_menu in categories_dict.values():
            menu.addMenu(sub_menu)

        menu.exec_(find_global_point(self.ui.function))

    def function_show(self):

        move_window_tool(widget_parent=self, widget_current=self.widget_function)
        self.widget_function.tool_show()

    @staticmethod
    def a___________________operator_______________():
        pass

    def operator_menu_show(self):

        menu = MyContextMenu(tooltips=False)

        menu.add_title(title=self.tr("Opérateur"))

        for text in ['_IF_(', '_ELSE_(', '_ELSE__IF_(', "|", '&', "!", "=", "<", "<=", ">", ">=", "<>"]:

            if text == "&":
                title = "&&"
            else:
                title = text

            menu.add_action(qicon=get_icon(help_icon),
                            title=title,
                            action=lambda a=text: self.formula_add_text(a))

        menu.exec_(find_global_point(self.ui.operator_bt))

    @staticmethod
    def a___________________finish_______________():
        pass

    def finish_show_clicked(self):

        move_window_tool(widget_parent=self, widget_current=self.widget_second_oeuvre)
        self.widget_second_oeuvre.show_finish()

    @staticmethod
    def a___________________object_______________():
        pass

    def object_show_clicked(self):

        move_window_tool(widget_parent=self, widget_current=self.widget_objet)
        self.widget_objet.tool_show()

    @staticmethod
    def a___________________trade_______________():
        pass

    def trade_show_clicked(self):

        move_window_tool(widget_parent=self, widget_current=self.widget_metier)
        self.widget_metier.tool_show()

    @staticmethod
    def a___________________add_text_______________():
        pass

    def formula_add_text(self, valeur: str):
        """Permet d'ajouter l'attribut selectionné"""

        self.ui.valeur_attr.insertPlainText(valeur)
        self.ui.valeur_attr.setFocus()

    def bt_aide(self):
        """bt_aide"""

        code_langue = get_code_langue(langue=self.asc.langue)

        version_allplan = self.allplan.version_allplan_current

        lien = f"https://help.allplan.com/Allplan/{version_allplan}-0/{code_langue}/Allplan/index.htm#10058_1.htm"
        lien2 = f"https://help.allplan.com/Allplan/{version_allplan}-0/{code_langue}/Allplan/index.htm#9899.htm"
        lien3 = f"https://help.allplan.com/Allplan/{version_allplan}-0/{code_langue}/Allplan/index.htm#74158.htm"

        menu = MyContextMenu()

        menu.add_title(title=self.tr("Aide"))

        menu.add_action(qicon=get_icon(help_icon),
                        title=self.tr("Fonctions"),
                        action=lambda: help_open_link(full_link=lien))

        menu.add_action(qicon=get_icon(help_icon),
                        title=self.tr("Attribut"),
                        action=lambda: help_open_link(full_link=lien2))

        menu.add_action(qicon=get_icon(help_icon),
                        title=self.tr("Portes, Fenêtre"),
                        action=lambda: help_open_link(full_link=lien3))

        menu.exec_(find_global_point(self.ui.help))

    def afficher_message(self):

        tooltip = self.ui.bt_verif.toolTip()

        if tooltip == self.tr("C'est tout bon!"):

            msg(titre=self.windowTitle(),
                message=self.tr("Cette formule paraît correcte !"),
                icone_valide=True)

        else:
            msg(titre=self.windowTitle(),
                message=f"{tooltip}",
                icone_critique=True)

    def translate_formula_change_size(self, current_size: int):

        current_font = self.ui.formule_convertie.font()
        current_font.setPointSize(current_size)
        self.ui.formule_convertie.setFont(current_font)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    def changeEvent(self, event: QEvent):

        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.ismaximized_on = True

            else:
                self.ismaximized_on = False
                move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent):

        datas_config = settings_read(file_name=formula_setting_file)

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True
            else:
                datas_config["height"] = self.size().height()
                datas_config["width"] = self.size().width()
                datas_config["ismaximized_on"] = False

        else:

            datas_config["height"] = self.size().height()
            datas_config["width"] = self.size().width()
            datas_config["ismaximized_on"] = False

        settings_save(file_name=formula_setting_file, config_datas=datas_config)

        self.close_event.emit()

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class Finishing(QWidget):
    finishing_formula_add = pyqtSignal(str)

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # BOITE DE DIALOGUE
        # ---------------------------------------

        self.ui = Ui_Finishing()
        self.ui.setupUi(self)

        # ---------------------------------------
        # Variables
        # ---------------------------------------

        self.floor_index = 0
        self.baseboard_index = 1
        self.vsurface_index = 2
        self.ceiling_index = 3
        self.material_index = 4

        self.no_layer_list = [self.baseboard_index, self.material_index]

        # ---------------------------------------
        # PARENT
        # ---------------------------------------

        self.asc = asc
        self.allplan: AllplanDatas = self.asc.allplan

        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        # ---------------------------------------
        # WIDGET ATTRIBUTE
        # ---------------------------------------

        self.widget_attribute: AttributesWidget = self.asc.attributes_widget
        self.widget_attribute.finishing_signal.connect(self.finishing_attribute_added)

        # ---------------------------------------
        # SIGNAUX - FINISHING
        # ---------------------------------------

        get_look_combobox(self.ui.finishing)

        self.ui.help.clicked.connect(self.finishing_help_show)

        # ---------------------------------------
        # SIGNAUX - ATTRIBUTE
        # ---------------------------------------

        self.finishing_model = QStandardItemModel()

        # ---------------------------------------
        # Filter
        # ---------------------------------------

        self.finishing_filter = NumericSortProxyModel(column_number=1)
        self.finishing_filter.setSourceModel(self.finishing_model)
        self.finishing_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.finishing_filter.setSortLocaleAware(True)

        # ---------------------------------------
        # SETTINGS
        # ---------------------------------------

        formula_setting = settings_read(formula_setting_file)

        finishing_select = formula_setting.get("finishing_select", 0)

        if not isinstance(finishing_select, int):
            finishing_select = 0

        self.ui.finishing.setCurrentIndex(finishing_select)
        self.finishing_type_changed()

        # ---------------------------------------

        attribute_select = formula_setting.get("finishing_attribute_select", "209")

        if not isinstance(attribute_select, str):
            attribute_select = "209"

        self.attribute_number = attribute_select

        # ---------------------------------------

        layer_list = formula_setting.get("finishing_layer_select", ["0"])

        self.finishing_load_layer_list(layer_list=layer_list)

        # ---------------------------------------
        # Finishing type
        # ---------------------------------------

        self.ui.finishing.currentIndexChanged.connect(self.finishing_type_changed)

        # ---------------------------------------
        # Attribute
        # ---------------------------------------

        get_look_combobox(self.ui.attribute)

        self.ui.attribute_add.clicked.connect(self.finishing_attribute_show)

        # ---------------------------------------
        # SIGNAUX - COUCHES
        # ---------------------------------------

        self.ui.layer_01.clicked.connect(self.layer_number)
        self.ui.layer_02.clicked.connect(self.layer_number)
        self.ui.layer_03.clicked.connect(self.layer_number)
        self.ui.layer_04.clicked.connect(self.layer_number)
        self.ui.layer_05.clicked.connect(self.layer_number)
        self.ui.layer_06.clicked.connect(self.layer_number)
        self.ui.layer_07.clicked.connect(self.layer_number)
        self.ui.layer_08.clicked.connect(self.layer_number)
        self.ui.layer_09.clicked.connect(self.layer_number)
        self.ui.layer_10.clicked.connect(self.layer_number)

        self.ui.layer_upper.clicked.connect(self.layer_upper)

        self.ui.layer_all.clicked.connect(self.layer_all)

        # ---------------------------------------
        # SIGNAUX - BOUTONS
        # ---------------------------------------

        self.ui.ok.clicked.connect(self.finishing_save)
        self.ui.quit.clicked.connect(self.close)

    def show_finish(self):

        self.finishing_load_model(current_number=self.attribute_number)

        self.adjustSize()

        self.show()

    def finishing_load_model(self, current_number=""):

        self.finishing_model.clear()

        attributes_list = list()

        for number_str in self.allplan.formula_favorite_list:

            if number_str in attributes_list:
                continue

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):
                continue

            if attribute_obj.name == "":
                continue

            attributes_list.append(number_str)

            qs_name = QStandardItem(get_icon(attribute_icon), attribute_obj.name)
            qs_name.setToolTip(number_str)

            qm_number = QStandardItem(number_str)
            qm_number.setToolTip(attribute_obj.name)

            self.finishing_model.appendRow([qs_name, qm_number])

        self.finishing_filter.setSourceModel(self.finishing_model)

        self.finishing_filter.sort(0, Qt.AscendingOrder)

        self.ui.attribute.setModel(self.finishing_filter)

        if current_number == "":
            return

        current_row = self.attribute_number_find_index_by(number=current_number)

        self.ui.attribute.setCurrentIndex(current_row)

    def finishing_load_layer_list(self, layer_list: list):

        if not isinstance(layer_list, list):
            layer_list = ["0"]

        for number in layer_list:

            if not isinstance(number, str):
                self.ui.layer_upper.setChecked(True)
                self.layer_upper()
                return

            if number == "0":
                self.ui.layer_upper.setChecked(True)
                self.layer_upper()
                return

            if number == "-1":
                self.ui.layer_all.setChecked(True)
                self.layer_all()
                return

            if number == "1":
                self.ui.layer_01.setChecked(True)
                continue

            if number == "2":
                self.ui.layer_02.setChecked(True)
                continue

            if number == "3":
                self.ui.layer_03.setChecked(True)
                continue

            if number == "4":
                self.ui.layer_04.setChecked(True)
                continue

            if number == "5":
                self.ui.layer_05.setChecked(True)
                continue

            if number == "6":
                self.ui.layer_06.setChecked(True)
                continue

            if number == "7":
                self.ui.layer_07.setChecked(True)
                continue

            if number == "8":
                self.ui.layer_08.setChecked(True)
                continue

            if number == "9":
                self.ui.layer_09.setChecked(True)
                continue

            if number == "10":
                self.ui.layer_10.setChecked(True)
                continue

        self.layer_number()

    @staticmethod
    def a___________________help_______________():
        pass

    def finishing_help_show(self):

        part1 = self.tr("Remarques sur le second-œuvre")
        part2 = self.tr("En cas de sélection de plusieurs couches, celles-ci sont additionnées ou "
                        "listées de manière alphanumérique (caractère séparateur '/')")

        msg(titre=self.windowTitle(),
            message=f"{part1}\n{part2}")

    @staticmethod
    def a___________________finishing_type_______________():
        pass

    def finishing_type_changed(self):

        current_index = self.ui.finishing.currentIndex()

        layer_enable = current_index not in self.no_layer_list

        self.ui.layer_01.setEnabled(layer_enable)
        self.ui.layer_02.setEnabled(layer_enable)
        self.ui.layer_03.setEnabled(layer_enable)
        self.ui.layer_04.setEnabled(layer_enable)
        self.ui.layer_05.setEnabled(layer_enable)
        self.ui.layer_06.setEnabled(layer_enable)
        self.ui.layer_07.setEnabled(layer_enable)
        self.ui.layer_08.setEnabled(layer_enable)
        self.ui.layer_09.setEnabled(layer_enable)
        self.ui.layer_10.setEnabled(layer_enable)
        self.ui.layer_all.setEnabled(layer_enable)
        self.ui.layer_upper.setEnabled(layer_enable)

    @staticmethod
    def a___________________attribute_______________():
        pass

    def finishing_attribute_show(self):

        move_window_tool(widget_parent=self, widget_current=self.widget_attribute)

        self.widget_attribute.attribute_show(current_mod="Finishing", current_widget=self)

    def finishing_attribute_added(self, numero_attribut):

        self.finishing_load_model(current_number=numero_attribut)

    @staticmethod
    def a___________________layer_______________():
        pass

    def layer_number(self):
        """bt_1"""

        self.ui.layer_upper.setChecked(False)

        if self.ui.layer_01.isChecked() and \
                self.ui.layer_02.isChecked() and \
                self.ui.layer_03.isChecked() and \
                self.ui.layer_04.isChecked() and \
                self.ui.layer_05.isChecked() and \
                self.ui.layer_06.isChecked() and \
                self.ui.layer_07.isChecked() and \
                self.ui.layer_08.isChecked() and \
                self.ui.layer_09.isChecked() and \
                self.ui.layer_10.isChecked():

            self.ui.layer_all.setChecked(True)
        else:
            self.ui.layer_all.setChecked(False)

    def layer_upper(self):

        self.ui.layer_all.setChecked(False)
        self.ui.layer_01.setChecked(False)
        self.ui.layer_02.setChecked(False)
        self.ui.layer_03.setChecked(False)
        self.ui.layer_04.setChecked(False)
        self.ui.layer_05.setChecked(False)
        self.ui.layer_06.setChecked(False)
        self.ui.layer_07.setChecked(False)
        self.ui.layer_08.setChecked(False)
        self.ui.layer_09.setChecked(False)
        self.ui.layer_10.setChecked(False)

    def layer_all(self):

        status = self.ui.layer_all.isChecked()

        if status:
            self.ui.layer_01.setChecked(True)
            self.ui.layer_02.setChecked(True)
            self.ui.layer_03.setChecked(True)
            self.ui.layer_04.setChecked(True)
            self.ui.layer_05.setChecked(True)
            self.ui.layer_06.setChecked(True)
            self.ui.layer_07.setChecked(True)
            self.ui.layer_08.setChecked(True)
            self.ui.layer_09.setChecked(True)
            self.ui.layer_10.setChecked(True)
            self.ui.layer_upper.setChecked(False)

    @staticmethod
    def a___________________tool_______________():
        pass

    def attribute_number_find_index_by(self, number: str) -> int:

        search_start = self.finishing_filter.index(0, 0)

        search_index = self.finishing_filter.match(search_start, Qt.ToolTipRole, number, 1, Qt.MatchExactly)

        if len(search_index) == 0:
            return -1

        qm_name = search_index[0]

        if not qm_check(qm_name):
            return -1

        current_row = qm_name.row()

        return current_row

    @staticmethod
    def a___________________save_______________():
        pass

    def finishing_save(self):

        if self.ui.finishing.currentIndex() == self.floor_index:
            formula = "Obj_Floor("

        elif self.ui.finishing.currentIndex() == self.baseboard_index:
            formula = "Obj_Baseboard("

        elif self.ui.finishing.currentIndex() == self.vsurface_index:
            formula = "Obj_VSurface("

        elif self.ui.finishing.currentIndex() == self.ceiling_index:
            formula = "Obj_Ceiling("

        elif self.ui.finishing.currentIndex() == self.material_index:
            formula = "Obj_Material("

        else:
            return

        attribute_index = self.ui.attribute.currentIndex()

        qm_number = self.finishing_filter.index(attribute_index, 1)

        if not qm_check(qm_number):
            return

        attribute_number = qm_number.data()

        if not isinstance(attribute_number, str) or attribute_number == "":
            return

        formula += f"@{attribute_number}@"

        if self.ui.finishing.currentIndex() in self.no_layer_list:
            formula += ";1)"

            self.finishing_formula_add.emit(formula)

            self.close()

            return

        if self.ui.layer_upper.isChecked():
            formula += " ;0)"

        else:

            if self.ui.layer_01.isChecked():
                formula += " ;1"

            if self.ui.layer_02.isChecked():
                formula += " ;2"

            if self.ui.layer_03.isChecked():
                formula += " ;3"

            if self.ui.layer_04.isChecked():
                formula += " ;4"

            if self.ui.layer_05.isChecked():
                formula += " ;5"

            if self.ui.layer_06.isChecked():
                formula += " ;6"

            if self.ui.layer_07.isChecked():
                formula += " ;7"

            if self.ui.layer_08.isChecked():
                formula += " ;8"

            if self.ui.layer_09.isChecked():
                formula += " ;9"

            if self.ui.layer_10.isChecked():
                formula += " ;10"

            formula += ")"

        self.finishing_formula_add.emit(formula)

        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):

        formula_setting = settings_read(file_name=formula_setting_file)

        # ---------------------------------------

        finishing_index = self.ui.finishing.currentIndex()

        formula_setting["finishing_select"] = finishing_index

        # ---------------------------------------

        attribute_index = self.ui.attribute.currentIndex()

        qm_number = self.finishing_filter.index(attribute_index, 1)

        if qm_check(qm_number):

            attribute_number = qm_number.data()

            if isinstance(attribute_number, str) and attribute_number != "":
                formula_setting["finishing_attribute_select"] = attribute_number

                self.attribute_number = qm_number.data()

        # ---------------------------------------
        if self.ui.layer_all.isChecked():
            formula_setting["finishing_layer_select"] = ["-1"]

        elif self.ui.layer_upper.isChecked():
            formula_setting["finishing_layer_select"] = ["0"]

        else:

            layer_list = list()

            if self.ui.layer_01.isChecked():
                layer_list.append("1")

            if self.ui.layer_02.isChecked():
                layer_list.append("2")

            if self.ui.layer_03.isChecked():
                layer_list.append("3")

            if self.ui.layer_04.isChecked():
                layer_list.append("4")

            if self.ui.layer_05.isChecked():
                layer_list.append("5")

            if self.ui.layer_06.isChecked():
                layer_list.append("6")

            if self.ui.layer_07.isChecked():
                layer_list.append("7")

            if self.ui.layer_08.isChecked():
                layer_list.append("8")

            if self.ui.layer_09.isChecked():
                layer_list.append("9")

            if self.ui.layer_10.isChecked():
                layer_list.append("10")

            formula_setting["finishing_layer_select"] = layer_list

        # ---------------------------------------

        settings_save(file_name=formula_setting_file, config_datas=formula_setting)

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class FormulaTool(QWidget):
    add_formula = pyqtSignal(str)

    def __init__(self, asc, current_mod: str):
        super().__init__()

        # ---------------------------------------
        # BOITE DE DIALOGUE
        # ---------------------------------------

        self.asc = asc
        self.allplan: AllplanDatas = self.asc.allplan

        self.ui = Ui_WidgetFormulaTool()
        self.ui.setupUi(self)

        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        # ---------------------------------------
        # Model
        # ---------------------------------------

        self.tool_model = QStandardItemModel()
        self.current_mod = current_mod

        # ---------------------------------------
        # Filter
        # ---------------------------------------

        self.tool_filter = NumericSortProxyModel(column_number=1)
        self.tool_filter.setSourceModel(self.tool_model)
        self.tool_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.tool_filter.setSortLocaleAware(True)

        # ---------------------------------------
        # Table
        # ---------------------------------------

        self.ui.table.setModel(self.tool_filter)

        self.ui.table.doubleClicked.connect(self.tool_add_formula_action)

        self.ui.table.selectionModel().selectionChanged.connect(self.tool_manage_add_button)

        self.ui.table.setCurrentIndex(self.tool_filter.index(0, col_obj_code))

        get_look_tableview(self.ui.table)

        if current_mod == "object":
            self.tool_load_object_model()
            self.setWindowTitle(self.tr('Objet'))
            self.asc.langue_change.connect(self.tool_load_object_model)

        elif current_mod == "trade":
            self.setWindowTitle(self.tr('Métier'))
            self.tool_load_trade_model()
            self.asc.langue_change.connect(self.tool_load_trade_model)

        elif current_mod == "function":
            self.setWindowTitle(self.tr('Fonctions'))
            self.tool_load_function_model()
            self.tool_filter.setFilterKeyColumn(1)
            self.asc.langue_change.connect(self.tool_load_function_model)

        # ---------------------------------------
        # SETTINGS
        # ---------------------------------------

        formula_setting = settings_read(formula_setting_file)

        width = formula_setting.get(f"{current_mod}_width", 500)

        if not isinstance(width, int):
            width = 500

        height = formula_setting.get(f"{current_mod}_height", 500)

        if not isinstance(height, int):
            height = 500

        self.resize(width, height)

        # ---------------------------------------

        ismaximized_on = formula_setting.get(f"{current_mod}_ismaximized_on", False)

        if not isinstance(ismaximized_on, bool):
            self.ismaximized_on = False
        else:
            self.ismaximized_on = ismaximized_on

        # ---------------------------------------

        header = self.ui.table.horizontalHeader()

        if header is not None:

            order = formula_setting.get(f"{current_mod}_order", 0)

            if not isinstance(order, int):
                order = 0

            order_col = formula_setting.get(f"{current_mod}_order_col", 0)

            if not isinstance(order_col, int):
                order_col = 0

            header.setSortIndicator(order_col, order)
            self.ui.table.sortByColumn(order_col, order)

        # ---------------------------------------

        current_txt = formula_setting.get(f"{current_mod}_select", "")

        if isinstance(current_txt, str) and current_txt != "" and self.tool_filter.rowCount() != 0:

            search_start = self.tool_filter.index(0, 0)

            search = self.tool_filter.match(search_start, Qt.DisplayRole, current_txt, 1, Qt.MatchExactly)

            if len(search) != 0:
                qm_new = search[0]

                if qm_check(qm_new):
                    self.ui.table.setCurrentIndex(qm_new)

                    self.ui.table.scrollTo(qm_new, QAbstractItemView.PositionAtCenter)

        # ---------------------------------------
        # Search
        # ---------------------------------------

        self.ui.search.textChanged.connect(self.tool_search_manage)
        self.ui.search_clear.clicked.connect(self.ui.search.clear)

        # ---------------------------------------
        # SIGNAUX - BOUTONS
        # ---------------------------------------

        self.ui.ok.clicked.connect(self.tool_add_formula)
        self.ui.quit.clicked.connect(self.close)

    @staticmethod
    def a___________________loading______():
        pass

    def tool_load_object_model(self):

        objects_list = self.allplan.get_object_datas()

        if len(objects_list) == 0:
            print("formula -- tool_load_object_model -- len(objects_list) == 0")
            return

        self.tool_model.clear()

        self.tool_model.setHorizontalHeaderLabels([self.tr("Nom objet"), self.tr("Formule")])

        for code, number_int in objects_list:
            formula = f"@OBJ@={number_int}"

            qs_formula = QStandardItem(formula)
            qs_formula.setData(number_int, user_data_type)

            self.tool_model.appendRow([QStandardItem(code), qs_formula])

            self.allplan.model_autocompletion.appendRow([QStandardItem(f"@OBJ@={code}"),
                                                         QStandardItem(formula)])

        self.tool_header_manage()

    def tool_load_trade_model(self):

        self.tool_model.clear()

        self.tool_model.setHorizontalHeaderLabels([self.tr("Code"), self.tr("Formule")])

        attribute_obj = self.allplan.attributes_dict.get("209")

        if not isinstance(attribute_obj, AttributeDatas):
            return

        if not isinstance(attribute_obj.enumeration, QStandardItemModel):
            return

        for index_item in range(attribute_obj.enumeration.rowCount()):

            qs_index = attribute_obj.enumeration.index(index_item, 0)
            qs_trade = attribute_obj.enumeration.index(index_item, 1)

            number = qs_index.data()
            code = qs_trade.data()

            if code == "":
                continue

            try:
                number_int = int(number)
            except Exception:
                print("formula -- FormulaTool -- tool_load_trade_model -- bad number")
                continue

            formula = f"@209@={number_int}"

            qs_formula = QStandardItem(formula)
            qs_formula.setData(number_int, user_data_type)

            self.tool_model.appendRow([QStandardItem(code), qs_formula])

        self.tool_header_manage()

    def tool_get_function_list(self) -> list:

        txt_math = self.tr("Mathématiques Générales")
        txt_geom = self.tr("Trigonométrie")
        txt_conv = self.tr("Unités et Conversion d'Angles")
        txt_data = self.tr("Analyse de Données et Texte")
        txt_obj_ = self.tr("Fonctions Obj_")
        txt_precast = "PRECAST"
        txt_other = self.tr("Autres")

        functions = [
            ['ABS', self.tr("Valeur absolue"), "ABS(x)", txt_math],
            ['SQRT', self.tr("Racine carrée"), "SQRT(x)", txt_math],
            ['SQR', self.tr("Nombre de carrés"), "SQR(x)", txt_math],
            ['PI', "3.14", "PI", txt_math],
            ['LN', self.tr("Logarithme népérien (base e)"), "LN(x)", txt_math],
            ['LOG', self.tr("Logarithme népérien (base 10)"), "LOG(x)", txt_math],
            ['RCP', "1/x", "RCP(x)", txt_math],
            ['EXP', self.tr("Fonction exponentielle de base e"), "EXP(x)", txt_math],
            ['SGN', self.tr("Détermine signe -> retourne 1 si >0 | 0 si égal à 0 | -1 si <0"), "SGN(x)", txt_math],
            ['SIN', self.tr("Fonction trigonométrique sinus"), "SIN(x)", txt_geom],
            ['COS', self.tr("Fonction trigonométrique cosinus"), "COS(x)", txt_geom],
            ['TAN', self.tr("Fonction trigonométrique tangente"), "TAN(x)", txt_geom],
            ['ASIN', self.tr("Renvoie l’arcsinus ou le sinus inverse d’un nombre"), "ASIN(x)", txt_geom],
            ['ACOS', self.tr("Renvoie l’arccosinus, ou inverse du cosinus d’un nombre"), "ACOS(x)", txt_geom],
            ['ATAN', self.tr("Renvoie l’arctangente ou la tangente inverse d’un nombre"), "ATAN(x)", txt_geom],
            ['SINH', self.tr("Renvoie le sinus hyperbolique inverse d’un nombre"), "SINH(x)", txt_geom],
            ['COSH', self.tr("Renvoie le cosinus hyperbolique inverse d’un nombre"), "COSH(x)", txt_geom],
            ['TANH', self.tr("Renvoie la tangente hyperbolique inverse d’un nombre"), "TANH(x)", txt_geom],
            ['NINT', self.tr("Arrondit à l'entier le plus proche"), "NINT(1,55) =>2", txt_math],
            ['INT', self.tr("Arrondit à la valeur entière inférieure"), "INT(1,55) =>1", txt_math],
            ['CEIL', self.tr("Arrondit à la valeur entière supérieure"), "CEIL(1,55) =>2", txt_math],
            ['GRA', self.tr("Mesure d'arc en degré"), "GRA(x)", txt_conv],
            ['RAD', self.tr("Degré en mesure d'arc"), "RAD(x)", txt_conv],
            ['GON', self.tr("Mesure d'arc en grade"), "GON(x)", txt_conv],
            ['RAG', self.tr("Grade en mesure d'arc"), "RAG(x)", txt_conv],
            ['AVG', self.tr("Moyenne de 10 arguments (au plus) séparés par des points-virgules"),
             "AVG(1;3) =>2", txt_math],

            ['MIN', self.tr("Minimum de 10 arguments (au plus) séparés par des points-virgules"),
             "MIN(1;3) =>1", txt_math],

            ['MAX', self.tr("Maximum de 10 arguments au plus séparés par des points-virgules"),
             "MAX(1;3) =>3", txt_math],

            ['FLAG', self.tr("Analyse binaire"), "FLAG(x; 1)", txt_data],

            ['ROUND',
             self.tr("Arrondissement d'une valeur numérique quelconque au nombre de dix décimales spécifiées"),
             "ROUND(1.13333;2) =>1,13", txt_math],

            ['ELE', self.tr("Filtre plusieurs valeurs numériques d'un attribut et retourne à 0 ou 1."),
             "ELE(@221@;0,115;0,24;0,365)", txt_data],

            ['VALUE', self.tr("Détermine des valeurs quelconques à partir de textes"),
             self.tr('STR_TEST = "Ma maison a 6 chambres et 2 salles de bains" --> '
                     'VALUE(STR_TEST;1) + VALUE(STR_TEST;2) => 8'), txt_data],

            ['MID',
             self.tr("Renvoie un nombre donné de caractères d'une chaîne de caractères à partir d'un point donné"),
             self.tr('MID("Ma maison a 6 chambres et 2 salles de bains" ; 13 ; 10) => 6 chambres'), txt_data],

            ['FORMAT', self.tr("Permet d'obtenir la sortie formatée de valeurs"),
             'FORMAT("B/H=%.2f / %.2f"; @220@; @222@)', txt_data],

            ['PARENT', self.tr("Permet d'obtenir la valeur de l'attribut du parent de l'objet"),
             "PARENT(@507@)", txt_other],

            ['CHILD', self.tr("Permet d'obtenir la valeur de l'attribut de l'enfant de l'objet"),
             "CHILD(@507@)", txt_other],

            ['Obj_Floor',
             self.tr("Evalue la formule sur toutes les surfaces de sol adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Floor(@229@; 1]", txt_obj_],

            ['Obj_Ceiling',
             self.tr("Evalue la formule sur toutes les surfaces de plafond adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Ceiling(@229@; 1]", txt_obj_],

            ['Obj_VSurface',
             self.tr("Evalue la formule sur toutes les faces verticales adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_VSurface(@229@; 1]", txt_obj_],

            ['Obj_Baseboard',
             self.tr("Evalue la formule sur toutes les plinthes adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Baseboard(@220@; 1]", txt_obj_],

            ['Obj_Material',
             self.tr("Evalue la formule sur tous les matériaux adjacents et additionne "
                     "ou concatène avec '/'"),
             "Obj_Material(@229@]", txt_obj_],

            ['Obj_WindowOpening',
             self.tr("Evalue la formule sur toutes les ouvertures adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_WindowOpening(@229@]", txt_obj_],

            ['Obj_FrenchWindowOpening',
             self.tr("Evalue la formule sur toutes les ouvertures adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_FrenchWindowOpening(@229@]", txt_obj_],

            ['Obj_Roof_Opening',
             self.tr("Evalue la formule sur toutes les ouvertures de toit adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Roof_Opening(@229@]", txt_obj_],

            ['Obj_DoorOpening',
             self.tr("Evalue la formule sur toutes les ouvertures de porte adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_DoorOpening(@229@]", txt_obj_],

            ['Obj_Niche',
             self.tr("Evalue la formule sur toutes les niches adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Niche(@229@]", txt_obj_],

            ['Obj_Wall',
             self.tr("Evalue la formule sur tous les murs adjacents et additionne "
                     "ou concatène avec '/'"),
             "Obj_Wall(@229@]", txt_obj_],

            ['Obj_Room',
             self.tr("Evalue la formule sur toutes les pièces adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Room(@229@]", txt_obj_],

            ['Obj_Column',
             self.tr("Evalue la formule sur tous les poteaux adjacents et additionne "
                     "ou concatène avec '/'"),
             "Obj_Column(@229@]", txt_obj_],

            ['Obj_WindowSmartSymbol',
             self.tr("Evalue la formule sur toutes les macros de fenêtre adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_WindowSmartSymbol(@229@]", txt_obj_],

            ['Obj_DoorSmartSymbol',
             self.tr("Evalue la formule sur toutes les macros de porte adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_DoorSmartSymbol(@229@]", txt_obj_],

            ['Obj_RoofWindow',
             self.tr("Evalue la formule sur toutes les fenêtres de toit adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_RoofWindow(@229@]", txt_obj_],

            ['Obj_Window',
             self.tr("Evalue la formule sur toutes les fenêtres adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Window(@229@]", txt_obj_],

            ['Obj_Door',
             self.tr("Evalue la formule sur toutes les portes adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Door(@229@]", txt_obj_],

            ['Obj_Roof',
             self.tr("Evalue la formule sur toutes les toitures adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_Roof(@229@]", txt_obj_],

            ['Obj_RoofLayer',
             self.tr("Evalue la formule sur toutes les couches de toitures adjacentes et additionne "
                     "ou concatène avec '/'"),
             "Obj_RoofLayer(@229@]", txt_obj_],

            ['TOPOLOGY',
             self.tr("Evalue la formule sur l'objet topologique souhaité"),
             "Type = 'Site', 'Building', 'Story' \nTOPOLOGY('Building', @507@)", txt_other],

            ['PARENTPRECAST', self.tr("[PRECAST] Permet d'obtenir les éléments PARENT d'une armature."),
             "PARENTPRECAST (@1877@)", txt_precast],

            ['IMPRRE', "[PRECAST]", self.tr("IMPRRE(@attribut@; valeur_1; valeur_2; valeur_x)"), txt_precast],

            ['FIXTURECOUNT', self.tr(
                "[PRECAST] Permet d'obtenir combien de pièces portant un nom "
                "spécifique sont incluses dans un élément préfabriqué."),
             'FIXTURECOUNT(@1332@; "Halox")', txt_precast],

            ['GROUP',
             self.tr("Renvoie le texte correspondant à partir de groupes dont la valeur (plage) correspont au nombre."),
             'GROUP("1-4:A ; 5-8:B" ;@1013@)', txt_precast],

            ['OPENINGMACROCOUNT', self.tr("Nombre de macros d'ouverture (optionnel avec condition."),
             'OPENINGMACROCOUNT(@507@;"Holzab")', txt_precast],

            ['TOTAL', self.tr("Permet de faire la somme de plusieurs valeurs"), "TOTAL(@210@)", txt_other]

        ]
        return functions

    def tool_load_function_model(self):

        functions = self.tool_get_function_list()

        self.tool_model.clear()

        self.tool_model.setHorizontalHeaderLabels([self.tr("Fonctions"), self.tr("Usage"), ""])

        for title, usage, example, _ in functions:
            qs_function = QStandardItem("")
            qs_function.setToolTip(example)

            self.tool_model.appendRow([QStandardItem(title), QStandardItem(usage), qs_function])

        self.tool_header_manage()

    def tool_header_manage(self):

        header = self.ui.table.horizontalHeader()

        if header is not None:

            header.sortIndicatorChanged.connect(self.tool_scroll)

            if self.current_mod == "function":

                header.setSectionResizeMode(col_obj_code, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(col_obj_formula, QHeaderView.Stretch)
                header.resizeSection(2, 40)

            else:

                header.setSectionResizeMode(col_obj_code, QHeaderView.Stretch)
                header.setSectionResizeMode(col_obj_formula, QHeaderView.Stretch)

            if header.height() != 24:
                header.setFixedHeight(24)

    def tool_buttons_refresh(self):

        row_count = self.tool_filter.rowCount()

        for item_index in range(row_count):

            qm_filtre = self.tool_filter.index(item_index, 2)

            if not qm_check(qm_filtre):
                print("library -- FormulaTool -- tool_buttons_refresh -- not qm_check(qm_filtre)")
                continue

            self.tool_button_creation(qm_filter=qm_filtre)

    def tool_scroll(self):

        qm_filter_current = self.ui.table.currentIndex()

        if not qm_check(qm_filter_current):
            return

        self.ui.table.scrollTo(qm_filter_current, QAbstractItemView.PositionAtCenter)

    @staticmethod
    def a___________________library_buttons___________________():
        pass

    def tool_button_creation(self, qm_filter: QModelIndex):

        button = QPushButton(get_icon(help_icon), "")
        button.setFlat(True)
        button.setIconSize(QSize(20, 20))

        button.clicked.connect(self.tool_show_help)

        self.ui.table.setIndexWidget(qm_filter, button)

    def tool_show_help(self):

        qm_current = self.ui.table.currentIndex()

        if not qm_check(qm_current):
            return

        column = qm_current.column()

        if column == 2:

            example = qm_current.data(Qt.ToolTipRole)

            if isinstance(example, str) and example != "":
                msg(titre=self.windowTitle(),
                    message=example)

            return

        qm_current = self.tool_filter.index(qm_current.row(), 2)

        if not qm_check(qm_current):
            return

        example = qm_current.data(Qt.ToolTipRole)

        if isinstance(example, str) and example != "":
            msg(titre=self.windowTitle(),
                message=example)

    @staticmethod
    def a___________________show______():
        pass

    def tool_show(self):

        qm_current = self.ui.table.currentIndex()

        if not qm_check(qm_current):
            self.ui.table.setCurrentIndex(self.tool_filter.index(0, 0))

        if self.current_mod == "function":
            self.tool_buttons_refresh()

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

    @staticmethod
    def a___________________search______():
        pass

    def tool_search_manage(self, current_txt: str):

        if current_txt == "":
            self.ui.search.setStyleSheet("QLineEdit{border: 1px solid #8f8f91; "
                                         "border-right-width: 0px; border-top-left-radius: 5px; "
                                         "border-bottom-left-radius: 5px; padding-left: 5px; }")
        else:
            self.ui.search.setStyleSheet("QLineEdit{border: 2px solid orange; "
                                         "border-right-width: 0px; border-top-left-radius: 5px; "
                                         "border-bottom-left-radius: 5px; padding-left: 4px; }")

        old_selection = self.tool_find_current_name()

        if self.current_mod != "function":

            try:
                int(current_txt)
                self.tool_filter.setFilterKeyColumn(1)
            except Exception:
                self.tool_filter.setFilterKeyColumn(0)

        self.tool_filter.setFilterRegExp(current_txt)

        if self.tool_filter.rowCount() == 0:

            if self.tool_filter.filterKeyColumn() == 0:
                self.tool_filter.setFilterKeyColumn(1)
            else:
                self.tool_filter.setFilterKeyColumn(0)

            if self.tool_filter.rowCount() == 0:
                return

        qm_current = self.ui.table.currentIndex()

        if not qm_check(qm_current):

            qm_current = self.tool_filter.index(0, 0)

            if old_selection != "":

                search = self.tool_filter.match(qm_current, Qt.DisplayRole, old_selection, 1, Qt.MatchExactly)

                if len(search) != 0:
                    qm_new = search[0]

                    if qm_check(qm_new):
                        qm_current = qm_new

            self.ui.table.setCurrentIndex(qm_current)

        self.tool_buttons_refresh()

        self.ui.table.scrollTo(qm_current, QAbstractItemView.PositionAtCenter)

        self.ui.search.setFocus()

    @staticmethod
    def a___________________manage_button______():
        pass

    def tool_manage_add_button(self):
        selection_list = self.ui.table.selectionModel().selectedRows(0)
        self.ui.ok.setEnabled(len(selection_list) != 0)

    @staticmethod
    def a___________________add______():
        pass

    def tool_add_formula(self):

        selection_list = self.ui.table.selectionModel().selectedRows(0)

        if len(selection_list) == 0:
            return

        qm: QModelIndex = selection_list[0]

        if not qm_check(qm):
            print("formula -- FormulaTool -- tool_add_formula -- not qm_check(qm)")
            return

        self.tool_add_formula_action(qm=qm)

    def tool_add_formula_action(self, qm: QModelIndex):

        row_index = qm.row()

        if self.current_mod == "function":

            qm_formula = self.tool_filter.index(row_index, 0)

            if not qm_check(qm_formula):
                print("formula -- FormulaTool -- tool_add_formula_action -- not qm_check(qm_formula)")
                return

            formula = qm_formula.data()

            if formula == "":
                return

            formula += f"("

        else:

            qm_formula = self.tool_filter.index(row_index, col_obj_formula)

            if not qm_check(qm_formula):
                print("formula -- FormulaTool -- tool_add_formula_action -- not qm_check(qm_formula)")
                return

            formula = qm_formula.data()

        self.close()
        self.add_formula.emit(formula)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.ismaximized_on = True

            else:
                self.ismaximized_on = False
                move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent):

        formula_setting = settings_read(file_name=formula_setting_file)

        formula_setting[f"{self.current_mod}_ismaximized_on"] = self.isMaximized()

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                formula_setting[f"{self.current_mod}_height"] = screen.height()
                formula_setting[f"{self.current_mod}_width"] = screen.width()

            else:

                formula_setting[f"{self.current_mod}_height"] = self.size().height()
                formula_setting[f"{self.current_mod}_width"] = self.size().width()

        else:

            formula_setting[f"{self.current_mod}_height"] = self.size().height()
            formula_setting[f"{self.current_mod}_width"] = self.size().width()

        # ---------------------------------------

        header = self.ui.table.horizontalHeader()

        if header is not None:
            formula_setting[f"{self.current_mod}_order"] = header.sortIndicatorOrder()
            formula_setting[f"{self.current_mod}_order_col"] = header.sortIndicatorSection()

        # ---------------------------------------

        current_name = self.tool_find_current_name()

        formula_setting[f"{self.current_mod}_select"] = current_name

        settings_save(file_name=formula_setting_file, config_datas=formula_setting)

        super().closeEvent(event)

    def tool_find_current_name(self):

        qm_index = self.ui.table.currentIndex()

        if not qm_check(qm_index):
            return ""

        if qm_index.column() == 0:
            current_name = qm_index.data()

            if current_name is not None:
                return current_name

            return ""

        qm_index = self.tool_filter.index(qm_index.row(), 0)

        if not qm_check(qm_index):
            return ""

        current_name = qm_index.data()

        if current_name is not None:
            return current_name

        return ""

    @staticmethod
    def a___________________end______():
        pass
