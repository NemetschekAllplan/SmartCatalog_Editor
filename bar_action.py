#!/usr/bin/python3
# -*- coding: utf-8 -*

from attribute_add import AttributesWidget
from attributes_loader import *
from catalog_manage import *
from choices_widget import ChoicesWidget
from formula import Formula
from history import WidgetHistory
from library import Library
from link import LinkAdd, LinKAddAgain
from message import MessageLocation as MsgLocalication
from models import Models
from number_widget import WidgetNumber
from order_widget import OrderWidget
from paste_widget import WidgetPaste
from tools import afficher_message as msg, help_modify_tooltips
from tools import menu_ht_ligne, taille_police_menu, find_global_point, move_widget_ss_bouton, MyContextMenu
from tools import move_window_tool, settings_save
from ui_main_windows import Ui_MainWindow


class ActionBar(QObject):

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # Loading Tools
        # ---------------------------------------

        self.asc = asc
        self.ui: Ui_MainWindow = self.asc.ui
        self.hierarchy: Hierarchy = self.ui.hierarchy

        self.catalog: CatalogDatas = self.asc.catalog
        self.allplan: AllplanDatas = self.asc.allplan

        self.creation = self.allplan.creation

        self.formula_editor_widget: Formula = self.asc.formula_editor_widget

        # ======================================
        # Loading MENUS
        # ======================================

        self.material_menu = MyContextMenu(short_link=help_material_new)  # OK
        self.material_menu.help_request.connect(self.asc.help_request)

        self.component_menu = MyContextMenu(short_link=help_component_new)  # OK
        self.component_menu.help_request.connect(self.asc.help_request)

        self.attribute_menu = MyContextMenu(short_link=help_attribute_new)  # OK
        self.attribute_menu.help_request.connect(self.asc.help_request)

        self.hierarchy_menu = MyContextMenu()  # OK
        self.hierarchy_menu.help_request.connect(self.asc.help_request)
        self.hierarchy_menu.installEventFilter(self)

        self.detail_menu = MyContextMenu()  # OK
        self.detail_menu.help_request.connect(self.asc.help_request)
        self.detail_menu.installEventFilter(self)

        # ======================================
        # Loading WIDGETS
        # ======================================

        self.choices_widget = ChoicesWidget(asc=asc)
        self.choices_widget.save_modif_choice.connect(self.allplan.allplan_18358_choise_end)

        # ---------------------------------------
        # Loading attributes widget
        # ---------------------------------------

        self.attributes_widget: AttributesWidget = self.asc.attributes_widget
        self.attributes_widget.add_attributs.connect(self.attributs_ajouter_action)

        # ---------------------------------------
        # Loading attributes detail loader widget
        # ---------------------------------------

        self.attributes_detail_loader: AttributesDetailLoader = self.asc.attributes_detail_loader

        # ---------------------------------------
        # Loading Link widgets
        # ---------------------------------------

        self.link_creation_widget = LinkAdd(catalog=self.catalog, hierarchy=self.hierarchy)
        self.link_creation_widget.link_add_signal.connect(self.lien_ajouter_action)

        self.link_add_widget = LinKAddAgain()
        self.link_add_widget.link_open_signal.connect(self.link_add)
        self.link_add_widget.link_creation_signal.connect(self.lien_ajouter_action)

        self.asc.langue_change.connect(
            lambda main=self.link_add_widget: self.link_add_widget.ui.retranslateUi(main))

        # ---------------------------------------
        # Loading library widget
        # ---------------------------------------

        self.library_widget: Library = self.asc.library_widget

        # ---------------------------------------
        # Loading model widget
        # ---------------------------------------

        self.models_widget: Models = self.asc.models_widget

        # ---------------------------------------
        # Loading number widget
        # ---------------------------------------

        self.number_widget = WidgetNumber()
        self.asc.langue_change.connect(lambda main=self.number_widget: self.number_widget.ui.retranslateUi(main))

        self.number_widget.save_item.connect(self.item_ajouter_action)

        # ---------------------------------------
        # Loading paste widget
        # ---------------------------------------

        self.paste_widget = WidgetPaste(self.catalog)
        self.paste_widget.coller_menu.connect(self.hierarchie_bt_coller_action_list)

        # ---------------------------------------
        # Loading Undo widget
        # ---------------------------------------

        self.undo_widget = WidgetHistory(parent_actuel=self.asc, mode_current="undo")
        self.undo_widget.undo_selection_signal.connect(self.undo_action)

        self.redo_widget = WidgetHistory(parent_actuel=self.asc, mode_current="redo")
        self.redo_widget.redo_selection_signal.connect(self.redo_action)

        # ---------------------------------------
        # Loading Order widget
        # ---------------------------------------

        self.order_widget = OrderWidget(asc=asc)

        self.order_widget.order_edit_signal.connect(self.attributes_order_changed)

        if self.asc.attributes_order_custom:
            self.asc.attributes_order_list = self.order_widget.order_read_config()

        # ======================================
        # Loading UNDO/REDO SIGNALS
        # ======================================

        self.ui.undo_bt.clicked.connect(self.undo_button_pressed)
        self.ui.undo_bt.customContextMenuRequested.connect(self.undo_menu)

        self.ui.undo_list_bt.clicked.connect(self.undo_menu)
        self.ui.undo_list_bt.customContextMenuRequested.connect(self.undo_menu)

        self.ui.redo_bt.clicked.connect(self.redo_button_pressed)
        self.ui.redo_bt.customContextMenuRequested.connect(self.redo_menu)

        self.ui.redo_list_bt.clicked.connect(self.redo_menu)
        self.ui.redo_list_bt.customContextMenuRequested.connect(self.redo_menu)

        # ======================================
        # Loading ACTIONS BAR SIGNALS
        # ======================================

        # ---------------------------------------
        # Loading signals expand/collapse
        # ---------------------------------------

        self.ui.expand_all_bt.clicked.connect(self.expand_menu_show)

        help_modify_tooltips(widget=self.ui.expand_all_bt,
                             short_link=help_interface_hierarchy,
                             help_text=self.asc.help_tooltip)

        self.ui.collapse_all_bt.clicked.connect(self.collapse_menu_show)

        help_modify_tooltips(widget=self.ui.collapse_all_bt,
                             short_link=help_interface_hierarchy,
                             help_text=self.asc.help_tooltip)

        # ---------------------------------------
        # Loading_signals move
        # ---------------------------------------

        self.ui.move_up_bt.clicked.connect(self.monter)

        help_modify_tooltips(widget=self.ui.move_up_bt,
                             short_link=help_interface_hierarchy,
                             help_text=self.asc.help_tooltip)

        self.ui.move_down_bt.clicked.connect(self.descendre)

        help_modify_tooltips(widget=self.ui.move_down_bt,
                             short_link=help_interface_hierarchy,
                             help_text=self.asc.help_tooltip)

        # ---------------------------------------
        # Loading signal Folder
        # ---------------------------------------

        self.ui.folder_add_bt.clicked.connect(self.folder_add)

        help_modify_tooltips(widget=self.ui.folder_add_bt,
                             short_link=help_folder_new,
                             help_text=self.asc.help_tooltip)

        # ---------------------------------------
        # Loading signals Material
        # ---------------------------------------

        self.ui.material_add_bt.clicked.connect(self.material_add)

        help_modify_tooltips(widget=self.ui.material_add_bt,
                             short_link=help_material_new,
                             help_text=self.asc.help_tooltip)

        self.ui.material_list_bt.clicked.connect(self.material_menu_show)
        self.ui.material_list_bt.customContextMenuRequested.connect(self.material_menu_show)

        # ---------------------------------------
        # Loading signals Component
        # ---------------------------------------

        self.ui.component_add_bt.clicked.connect(self.component_add)

        help_modify_tooltips(widget=self.ui.component_add_bt,
                             short_link=help_component_new,
                             help_text=self.asc.help_tooltip)

        self.ui.component_list_bt.clicked.connect(self.component_menu_show)
        self.ui.component_list_bt.customContextMenuRequested.connect(self.component_menu_show)

        # ---------------------------------------
        # Loading signals Link
        # ---------------------------------------

        self.ui.link_add_bt.clicked.connect(self.link_add)

        help_modify_tooltips(widget=self.ui.link_add_bt,
                             short_link=help_link_new,
                             help_text=self.asc.help_tooltip)

        self.ui.link_list_bt.clicked.connect(self.link_menu_show)
        self.ui.link_list_bt.customContextMenuRequested.connect(self.link_menu_show)

        # ---------------------------------------
        # Loading signals Attribute
        # ---------------------------------------

        self.ui.attribute_add_bt.clicked.connect(self.attributs_ajouter)

        help_modify_tooltips(widget=self.ui.attribute_add_bt,
                             short_link=help_attribute_new,
                             help_text=self.asc.help_tooltip)

        self.ui.attribute_list_bt.clicked.connect(self.attributs_menu_afficher)
        self.ui.attribute_list_bt.customContextMenuRequested.connect(self.attributs_menu_afficher)

        # ---------------------------------------
        # Loading signals edit
        # ---------------------------------------

        self.ui.del_bt.clicked.connect(self.hierarchie_supprimer)

        help_modify_tooltips(widget=self.ui.del_bt,
                             short_link="SPE",
                             help_text=self.asc.help_tooltip)

        self.ui.cut_bt.clicked.connect(self.hierarchie_couper)

        help_modify_tooltips(widget=self.ui.cut_bt,
                             short_link="SPE",
                             help_text=self.asc.help_tooltip)

        self.ui.copy_bt.clicked.connect(self.hierarchie_copier)

        help_modify_tooltips(widget=self.ui.copy_bt,
                             short_link="SPE",
                             help_text=self.asc.help_tooltip)

        self.ui.paste_bt.clicked.connect(self.hierarchie_coller)

        help_modify_tooltips(widget=self.ui.paste_bt,
                             short_link="SPE",
                             help_text=self.asc.help_tooltip)

        self.ui.paste_list_bt.clicked.connect(self.hierarchie_coller_menu_afficher)
        self.ui.paste_list_bt.customContextMenuRequested.connect(self.hierarchie_coller_menu_afficher)

        # ---------------------------------------
        # Loading signals model
        # ---------------------------------------

        self.ui.model_bt.clicked.connect(self.asc.formula_widget_close)
        self.ui.model_bt.clicked.connect(self.models_widget.model_personnaliser)

        help_modify_tooltips(widget=self.ui.model_bt,
                             short_link=help_model_what,
                             help_text=self.asc.help_tooltip)

        self.ui.model_add_bt.clicked.connect(self.hierarchie_modele_enregistrer)

        help_modify_tooltips(widget=self.ui.model_add_bt,
                             short_link=help_model_new,
                             help_text=self.asc.help_tooltip)

        # ---------------------------------------
        # Loading signals Library
        # ---------------------------------------

        self.ui.library_bt.clicked.connect(self.hierarchie_bible_afficher)

        help_modify_tooltips(widget=self.ui.library_bt,
                             short_link=help_library_what,
                             help_text=self.asc.help_tooltip)

        # ---------------------------------------
        # Loading signals Hierarchy
        # ---------------------------------------

        self.hierarchy.selectionModel().selectionChanged.connect(self.hierarchie_gestion_selection)
        self.hierarchy.customContextMenuRequested.connect(self.hierarchie_menu_contextuel)
        self.hierarchy.clicked.connect(self.hierarchie_simple_clic)
        self.hierarchy.doubleClicked.connect(self.hierarchie_double_clic)

        self.hierarchy.setWhatsThis(help_interface_hierarchy)

        # ---------------------------------------
        # Loading signals Attributes detail
        # ---------------------------------------

        self.ui.attributes_detail.selectionModel().selectionChanged.connect(self.asc.attribut_clic)
        self.ui.attributes_detail.customContextMenuRequested.connect(self.attribut_menu_contextuel)

        self.ui.attributes_detail.setWhatsThis(help_interface_attribute)

    @staticmethod
    def a___________________hierarchy______():
        pass

    def hierarchie_simple_clic(self):

        self.asc.buttons_manage()

    def hierarchie_double_clic(self, qmodelindex: QModelIndex):

        self.library_selection_changed()

        if not qm_check(qmodelindex):
            return

        qm_parent = qmodelindex.parent()

        if not qm_check(qm_parent):

            qm_val = self.hierarchy.model().index(qmodelindex.row(), col_cat_value)

        else:

            qm_val = qm_parent.child(qmodelindex.row(), col_cat_value)

        qm_val = self.hierarchy.map_to_filter(qm=qm_val)

        if not qm_check(qm_val):
            return

        expanded = self.hierarchy.isExpanded(qm_val)

        self.hierarchy.setExpanded(qm_val, not expanded)

    def hierarchie_gestion_selection(self):

        self.hierarchy.selection_manage()

        self.hierarchie_selection_change()

    def hierarchie_selection_change(self):

        self.catalog.change_made = True

        if self.hierarchy.cat_model.rowCount() > 0:
            self.hierarchy.header_manage()

        qs_selection_list = self.hierarchy.get_qs_selection_list()

        formula_widget_number = self.formula_editor_widget.formula_selection_changed()

        if self.ui.attributes_detail.count() != 0:
            self.ui.attributes_detail.clear()

        self.library_selection_changed()

        if len(qs_selection_list) == 0:
            self.asc.buttons_manage()
            return

        qs: MyQstandardItem = qs_selection_list[0]

        if not isinstance(qs, MyQstandardItem):
            self.asc.buttons_manage()
            return

        if self.hierarchy.cat_filter_1.rowCount() != 0:

            last_qm_model_selection_list = self.hierarchy.get_qm_model_selection_list()

            if len(last_qm_model_selection_list) != 0:
                self.hierarchy.selected_list = last_qm_model_selection_list

        ele_type: str = qs.data(user_data_type)

        if len(qs_selection_list) > 1:

            qs_current: MyQstandardItem = qs_selection_list[0]

            if not isinstance(qs_current, MyQstandardItem):
                self.asc.buttons_manage()
                return

            type_element = qs_current.data(user_data_type)
            type_dossier = all(qstandarditem.data(user_data_type) for qstandarditem in qs_selection_list
                               if isinstance(qstandarditem, MyQstandardItem))

            if type_dossier and type_element == folder_code:
                self.attributes_detail_loader.add_name(qs_value=qs,
                                                       qs_selection_list=qs_selection_list)

            self.asc.buttons_manage()

            return

        qm_parent = qs.index()
        material_linked = False

        # --------------------------------
        # Dossier
        # --------------------------------

        if ele_type == folder_code:

            qs_parent: MyQstandardItem = qs.parent()

            if qs_parent is None:
                qs_parent = self.hierarchy.cat_model.invisibleRootItem()

            row_actuel = qs.row()

            qs_desc = qs_parent.child(row_actuel, col_cat_desc)

            qs_attrib = qs.child(0, col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get("207")

            if not isinstance(attribute_obj, AttributeDatas):
                print("bar_action -- hierarchie_selection_change -- not isinstance(attribute_obj, AttributeDatas) 1")
                return

            self.attributes_detail_loader.add_name(qs_value=qs,
                                                   qs_selection_list=None)

            self.attributes_detail_loader.add_lineedit_str(qm_parent=qs.index(),
                                                           qs_value=qs_attrib,
                                                           qs_desc=qs_desc,
                                                           attribute_obj=attribute_obj,
                                                           is_material=False)

            self.asc.buttons_manage()
            return

        # --------------------------------
        # Lien
        # --------------------------------

        if ele_type == link_code:

            link_model = QStandardItemModel()
            link_model.setHorizontalHeaderLabels([self.tr("Code"), self.tr("Description")])

            qs_root = link_model.invisibleRootItem()
            qs_root.setText("Root")

            material_name = qm_parent.data()

            qm_desc = self.hierarchy.cat_model.index(qm_parent.row(), col_cat_desc, qm_parent.parent())

            if not qm_check(qm_desc):
                description_txt = ""
            else:
                description_txt = qm_desc.data()

            font = QStandardItem().font()
            font.setBold(True)

            qs_sub_material = QStandardItem(get_icon(material_icon), material_name)
            qs_sub_material.setData(material_code, user_data_type)
            qs_sub_material.setFont(font)
            qs_sub_material.setEnabled(False)

            qs_sub_description = QStandardItem(description_txt)
            qs_sub_description.setFont(font)
            qs_sub_description.setEnabled(False)

            qs_root.appendRow([qs_sub_material, qs_sub_description])

            self.catalog.link_get_structure(material_name=material_name, qs_parent=qs_sub_material, visited=set())

            self.attributes_detail_loader.add_lien(qm_parent.parent(), qm_parent.row(), link_model)
            self.asc.buttons_manage()
            return

        if ele_type != material_code and ele_type != component_code:
            self.asc.buttons_manage()
            return

        if ele_type == material_code:
            forbidden_names_list = list(material_upper_list)

            nom_ouvrage = qm_parent.data()

            material_linked = nom_ouvrage in link_list

        else:

            forbidden_names_list = list()

        attribute_obj = self.allplan.attributes_dict.get(attribut_default_obj.current)

        if not isinstance(attribute_obj, AttributeDatas):
            print("bar_action -- hierarchie_selection_change -- not isinstance(attribute_obj, AttributeDatas) 2")
            return

        self.attributes_detail_loader.add_code(qs_value=qs,
                                               forbidden_names_list=forbidden_names_list,
                                               material_linked=material_linked,
                                               attribute_obj=attribute_obj)

        nb_attributs: int = qs.rowCount()

        attributes_classic_list = list()

        attributes_order_list = list()

        full_datas = dict()

        fill_datas = dict()
        fill_title = ""

        layer_datas = dict()
        layer_title = ""

        room_datas = dict()
        room_title = ""

        for attribute_index in range(nb_attributs):

            qs_value = qs.child(attribute_index, col_cat_value)
            qs_index = qs.child(attribute_index, col_cat_index)
            qs_number = qs.child(attribute_index, col_cat_number)

            if not isinstance(qs_number, Info):
                continue

            if not isinstance(qs_index, Info):
                continue

            if not isinstance(qs_value, Attribute):
                break

            number_str = qs_number.text()

            if not isinstance(number_str, str):
                continue

            if number_str in full_datas:
                continue

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):
                print("bar_action -- hierarchie_selection_change -- not isinstance(attribute_obj, AttributeDatas) 3")
                continue

            attrib_name = attribute_obj.name

            # --------------------------------
            # Description
            # --------------------------------

            if number_str == "207":

                qs_parent = qs.parent()

                if qs_parent is None:
                    qs_attrib = None
                    is_material = False

                else:

                    qs_attrib = qs_parent.child(qs.row(), col_cat_desc)
                    is_material = isinstance(qs, Material)

                self.attributes_detail_loader.add_lineedit_str(qm_parent=qm_parent,
                                                               qs_value=qs_value,
                                                               qs_desc=qs_attrib,
                                                               attribute_obj=attribute_obj,
                                                               is_material=is_material)

                self.attributes_detail_loader.add_title(self.tr("Attributs additionnels"))

                continue

            # --------------------------------

            if number_str in self.asc.attributes_order_list and self.asc.attributes_order_custom:

                value = number_str
                current_list = attributes_order_list

            else:

                current_list = attributes_classic_list

                if self.asc.attributes_order_col == 1:
                    value = attrib_name
                else:
                    value = number_str

            # --------------------------------
            # Layer
            # --------------------------------

            if number_str in attribute_val_default_layer:
                layer_datas[number_str] = attribute_index

                if number_str != attribute_val_default_layer_first:
                    continue

                current_list.append(value)
                layer_title = value
                continue

            # --------------------------------
            # Fill
            # --------------------------------

            if number_str in attribute_val_default_fill:

                fill_datas[number_str] = attribute_index

                if number_str != attribute_val_default_fill_first:
                    continue

                current_list.append(value)
                fill_title = value
                continue

            # --------------------------------
            # Room
            # --------------------------------

            elif number_str in attribute_val_default_room:

                room_datas[number_str] = attribute_index

                if number_str != attribute_val_default_room_first:
                    continue

                current_list.append(value)
                room_title = value
                continue

            # --------------------------------
            # others
            # --------------------------------

            current_list.append(value)

            # --------------------------------
            # Add to datas
            # --------------------------------

            full_datas[value] = {"attrib_number": number_str,
                                 "attrib_name": attrib_name,
                                 "attribute_index": attribute_index,
                                 "attribute_obj": attribute_obj,
                                 "qs_val": qs_value,
                                 "qs_index": qs_index}

        # --------------------------------
        # sort classic
        # --------------------------------

        if self.asc.attributes_order_col:
            attributes_classic_list.sort(reverse=self.asc.attributes_order == 1)

        else:

            attributes_classic_list.sort(key=int, reverse=self.asc.attributes_order == 1)

        # --------------------------------
        # sort user
        # --------------------------------

        if len(attributes_order_list) != 0:

            attributes_order_list_sorted = [number for number in self.asc.attributes_order_list
                                            if number in attributes_order_list]

            attributes_final_list = attributes_order_list_sorted + attributes_classic_list

        else:

            attributes_final_list = attributes_classic_list

        if len(attributes_final_list) == 0:
            self.asc.buttons_manage()
            return

        # --------------------------------
        # Add widgets
        # --------------------------------

        for value in attributes_final_list:

            # --------------------------------
            # Add layer widget
            # --------------------------------

            if value == layer_title:

                if len(layer_datas) == 0:
                    continue

                self.attributes_detail_loader.add_layer(qs_val=qs, datas_index_row=layer_datas)

                continue

            # --------------------------------
            # Add Fill widget
            # --------------------------------

            if value == fill_title:

                if len(fill_datas) == 0:
                    continue

                self.attributes_detail_loader.add_filling(qs_val=qs, datas_index_row=fill_datas)

                continue

            # --------------------------------
            # Add Room widget
            # --------------------------------

            if value == room_title:

                if len(room_datas) == 0:
                    continue

                self.attributes_detail_loader.add_room(qs_val=qs, datas_index_row=room_datas)

                continue

            # --------------------------------
            # Add other widgets
            # --------------------------------

            current_datas = full_datas.get(value, None)

            if not isinstance(current_datas, dict):
                continue

            if len(current_datas) == 0:
                continue

            self.attribute_load_list(current_datas=current_datas, qm_parent=qm_parent)

        # --------------------------------

        self.asc.buttons_manage()

        if formula_widget_number == "":
            return

        attributes_count = self.ui.attributes_detail.count()

        if attributes_count == 0:
            return

        for row_index in range(attributes_count):

            qlistwidgetitem = self.ui.attributes_detail.item(row_index)

            if not isinstance(qlistwidgetitem, QListWidgetItem):
                continue

            number_current = qlistwidgetitem.data(user_data_number)

            if number_current != formula_widget_number:
                continue

            formula_widget = self.ui.attributes_detail.itemWidget(qlistwidgetitem)

            if not isinstance(formula_widget, AttributeFormula):
                continue

            formula_widget.ouvrir_createur_formule()
            return

        self.formula_editor_widget.close()

    def attribute_load_list(self, current_datas: dict, qm_parent: QModelIndex):

        number_str: str = current_datas.get("attrib_number")

        if not isinstance(number_str, str):
            print("bar_action -- attribute_load_list -- not isinstance(number_str, str)")
            return

        # --------------------------------
        # Attribute 18358
        # --------------------------------

        if number_str == "18358" and len(self.allplan.allplan_18358_dict) != 0:
            self.choices_widget.choice_show(choice_dict=self.allplan.allplan_18358_dict,
                                            title=self.tr("Modèle d'ensemble d'attributs"))

        attrib_name: str = current_datas.get("attrib_name")

        if not isinstance(attrib_name, str):
            print("bar_action -- attribute_load_list -- not isinstance(attrib_name, str)")
            return

        # ------

        attribute_index: int = current_datas.get("attribute_index")

        if not isinstance(attribute_index, int):
            print("bar_action -- attribute_load_list -- not isinstance(attribute_index, int)")
            return

        # ------

        attribute_obj: AttributeDatas = current_datas.get("attribute_obj")

        if not isinstance(attribute_obj, AttributeDatas):
            print("bar_action -- attribute_load_list -- not isinstance(attribute_obj, AttributeDatas)")
            return

        # ------

        qs_val = current_datas.get("qs_val")

        if not isinstance(qs_val, MyQstandardItem):
            print("bar_action -- attribute_load_list -- not isinstance(qs_val, MyQstandardItem)")
            return

        # ------

        qs_index: QStandardItem = current_datas.get("qs_index")

        if not isinstance(qs_index, MyQstandardItem):
            print("bar_action -- attribute_load_list -- not isinstance(qs_index, MyQstandardItem)")
            return

        # ------

        if not isinstance(attribute_obj.option, str):
            print("bar_action -- attribute_load_list -- not isinstance(attribute_obj.option)")
            return

        # --------------------------------
        # Unknown attribute
        # --------------------------------

        if type_unknown in attribute_obj.option:
            self.attributes_detail_loader.add_unknown(attribute_obj=attribute_obj, value=qs_val.text())
            return

        # --------------------------------
        # Surface
        # --------------------------------

        if number_str == "335":
            self.attributes_detail_loader.add_surface(qs_val=qs_val, attribute_obj=attribute_obj)
            return

        # --------------------------------
        # Formule
        # --------------------------------

        if "Formule" in attribute_obj.option:
            self.attributes_detail_loader.add_formula(qs_val=qs_val, attribute_obj=attribute_obj)
            return

        # --------------------------------
        # Combobox
        # --------------------------------

        if "ComboBox" in attribute_obj.option:
            self.attributes_detail_loader.add_combobox(qs_value=qs_val,
                                                       qs_index=qs_index,
                                                       attribute_obj=attribute_obj)
            return

        # --------------------------------
        # Checkbox
        # --------------------------------

        if attribute_obj.option == code_attr_chk:
            self.attributes_detail_loader.ajouter_checkbox(qs_val=qs_val,
                                                           attribute_obj=attribute_obj)
            return

        # --------------------------------
        # Date
        # --------------------------------

        if attribute_obj.option == "Date" or attrib_name.startswith("Date"):
            self.attributes_detail_loader.add_date(qs_value=qs_val, attribute_obj=attribute_obj)

            return

        # --------------------------------
        # TextBox
        # --------------------------------
        qs_parent = self.hierarchy.cat_model.itemFromIndex(qm_parent)

        if not isinstance(qs_parent, (Material, Component)):
            print("bar_action -- attribute_load_list -- not isinstance(qs_parent, (Material, Component))")
            return

        if attribute_obj.option == code_attr_str:
            self.attributes_detail_loader.add_lineedit_str(qm_parent=qm_parent,
                                                           qs_value=qs_val,
                                                           qs_desc=None,
                                                           attribute_obj=attribute_obj,
                                                           is_material=isinstance(qs_parent, Material))
            return

        self.attributes_detail_loader.add_lineedit(qs_value=qs_val,
                                                   attribute_obj=attribute_obj,
                                                   is_material=isinstance(qs_parent, Material))

    def hierarchie_menu_contextuel(self, point: QPoint):

        if self.catalog.catalog_path == "":
            return

        menu = self.hierarchy_menu

        menu.clear()

        if self.catalog.change_made:
            menu.add_title(title=self.tr("Enregistrer"))

            menu.add_action(qicon=get_icon(save_icon),
                            title=self.tr("Enregistrer"),
                            action=self.catalog.catalog_save,
                            tooltips=self.ui.save_bt.toolTip(),
                            short_link=self.ui.save_bt.whatsThis())

            menu.add_action(qicon=get_icon(update_cat_icon),
                            title=self.tr("Mettre à jour les catalogues"),
                            action=self.asc.catalogue_update,
                            tooltips=self.ui.update_cat_bt.toolTip(),
                            short_link=self.ui.update_cat_bt.whatsThis())

        # ------------------------------
        # Déplier
        # ------------------------------

        menu.add_title(title=self.tr("Affichage"))

        if self.hierarchy.description_show:

            menu.add_action(qicon=get_icon(description_off_icon),
                            title=self.tr("Afficher / Masquer les descriptions de la hiérarchie"),
                            action=self.hierarchie_description,
                            tooltips=self.tr("Afficher / Masquer les descriptions de la hiérarchie"),
                            short_link=help_interface_hierarchy)

        else:

            menu.add_action(qicon=get_icon(description_on_icon),
                            title=self.tr("Afficher / Masquer les descriptions de la hiérarchie"),
                            action=self.hierarchie_description,
                            tooltips=self.tr("Afficher / Masquer les descriptions de la hiérarchie"),
                            short_link=help_interface_hierarchy)

        # ------------------------------
        if self.ui.expand_all_bt.isEnabled() or self.ui.collapse_all_bt.isEnabled():
            menu.addSeparator()

        # ------------------------------

        if self.ui.expand_all_bt.isEnabled():
            expand_action = menu.add_action(qicon=get_icon(expand_all_icon),
                                            title=self.tr("Déplier"),
                                            tooltips=self.ui.expand_all_bt.toolTip(),
                                            short_link=self.ui.expand_all_bt.whatsThis())

            expand_action.setMenu(self.hierarchy.expand_menu_creation())

        # ------------------------------

        if self.ui.collapse_all_bt.isEnabled():
            collapse_action = menu.add_action(qicon=get_icon(collapse_all_icon),
                                              title=self.tr("Replier"),
                                              tooltips=self.ui.collapse_all_bt.toolTip(),
                                              short_link=self.ui.collapse_all_bt.whatsThis())

            collapse_action.setMenu(self.hierarchy.collapse_menu_creation())

        # ------------------------------

        qs = self.hierarchy.get_current_qs()

        # ------------------------------
        # Déplacement
        # ------------------------------

        move_to_new_foler = isinstance(qs, Material)

        if self.ui.move_up_bt.isEnabled() or self.ui.move_down_bt.isEnabled() or move_to_new_foler:
            menu.add_title(title=self.tr("Déplacement"))

        if self.ui.move_up_bt.isEnabled():
            menu.add_action(qicon=get_icon(move_up_icon),
                            title=self.tr("Monter"),
                            action=self.monter,
                            tooltips=self.ui.move_up_bt.toolTip(),
                            short_link=self.ui.move_up_bt.whatsThis())

        if self.ui.move_down_bt.isEnabled():
            menu.add_action(qicon=get_icon(move_down_icon),
                            title=self.tr("Descendre"),
                            action=self.descendre,
                            tooltips=self.ui.move_down_bt.toolTip(),
                            short_link=self.ui.move_down_bt.whatsThis())

        if move_to_new_foler:
            menu.add_action(qicon=get_icon(merge_icon),
                            title=self.tr("Déplacer les ouvrages dans un nouveau dossier"),
                            action=self.catalog.material_to_new_folder,
                            short_link=help_interface_hierarchy)

        # ------------------------------
        # Ajouter
        # ------------------------------

        translate_dict = {folder_code: self.tr("Dossier"),
                          material_code: self.tr("Ouvrage"),
                          component_code: self.tr("Composant"),
                          link_code: self.tr("Lien"),
                          attribute_code: self.tr("Attribut")}

        if self.ui.folder_add_bt.isEnabled() or self.ui.material_add_bt.isEnabled() or \
                self.ui.component_add_bt.isEnabled() or self.ui.link_add_bt.isEnabled() or \
                self.ui.attribute_add_bt.isEnabled():
            menu.add_title(self.tr("Ajouter"))

        if self.ui.folder_add_bt.isEnabled():
            menu.add_action(qicon=get_icon(folder_icon),
                            title=translate_dict[folder_code],
                            action=self.folder_add,
                            tooltips=self.ui.folder_add_bt.toolTip(),
                            short_link=self.ui.folder_add_bt.whatsThis())

        if self.ui.material_add_bt.isEnabled():

            add_ouvrage = menu.add_action(qicon=get_icon(material_icon),
                                          title=translate_dict[material_code],
                                          tooltips=self.ui.material_add_bt.toolTip(),
                                          objectname=f"Add_{material_code}",
                                          short_link=self.ui.material_add_bt.whatsThis())

            sub_menu = self.hierarchie_sous_menu_ajouter(ele_type=material_code,
                                                         short_link=self.ui.material_add_bt.whatsThis())

            if len(sub_menu.actions()) != 0:
                add_ouvrage.setMenu(sub_menu)

        if self.ui.component_add_bt.isEnabled():

            add_composant = menu.add_action(qicon=get_icon(component_icon),
                                            title=translate_dict[component_code],
                                            tooltips=self.ui.component_add_bt.toolTip(),
                                            objectname=f"Add_{component_code}",
                                            short_link=self.ui.component_add_bt.whatsThis())

            sub_menu = self.hierarchie_sous_menu_ajouter(ele_type=component_code,
                                                         short_link=self.ui.component_add_bt.whatsThis())

            if len(sub_menu.actions()) != 0:
                add_composant.setMenu(sub_menu)

        if self.ui.link_add_bt.isEnabled():

            add_lien = menu.add_action(qicon=get_icon(link_icon),
                                       title=translate_dict[link_code],
                                       tooltips=self.ui.link_add_bt.toolTip(),
                                       objectname=f"Add_{link_code}",
                                       short_link=self.ui.link_add_bt.whatsThis())

            sub_menu = self.hierarchie_sous_menu_lien()

            if len(sub_menu.actions()) != 0:
                add_lien.setMenu(sub_menu)

        if self.ui.attribute_add_bt.isEnabled():

            add_attribut = menu.add_action(qicon=get_icon(attribute_add_icon),
                                           title=translate_dict[attribute_code],
                                           tooltips=self.ui.attribute_add_bt.toolTip(),
                                           objectname=f"Add_{attribute_code}",
                                           short_link=self.ui.attribute_add_bt.whatsThis())

            sub_menu = self.hierarchie_sous_menu_ajouter(ele_type=attribute_code,
                                                         short_link=self.ui.attribute_add_bt.whatsThis())

            if len(sub_menu.actions()) != 0:
                add_attribut.setMenu(sub_menu)

        # ------------------------------
        # Edition
        # ------------------------------

        if self.ui.del_bt.isEnabled() or self.ui.cut_bt.isEnabled() or self.ui.copy_bt.isEnabled() or \
                self.ui.paste_bt.isEnabled():
            menu.add_title(title=self.tr("Édition"))

        if self.ui.del_bt.isEnabled():
            menu.add_action(qicon=get_icon(delete_icon),
                            title=self.tr("Supprimer"),
                            action=self.hierarchie_supprimer,
                            tooltips=self.ui.del_bt.toolTip(),
                            short_link=self.ui.del_bt.whatsThis())

        if self.ui.cut_bt.isEnabled():
            menu.add_action(qicon=get_icon(cut_icon),
                            title=self.tr("Couper"),
                            action=self.hierarchie_couper,
                            tooltips=self.ui.cut_bt.toolTip(),
                            short_link=self.ui.cut_bt.whatsThis())

        if self.ui.copy_bt.isEnabled():
            menu.add_action(qicon=get_icon(copy_icon),
                            title=self.tr("Copier"),
                            action=self.hierarchie_copier,
                            tooltips=self.ui.copy_bt.toolTip(),
                            short_link=self.ui.copy_bt.whatsThis())

        # ------------------------------
        # Coller
        # ------------------------------

        if isinstance(qs, (Folder, Material, Component, Link)):
            dict_compatible = qs.get_type_possibilities()
        else:
            dict_compatible = {folder_code: self.tr("Enfant")}

        paste_menu = False

        if folder_code in dict_compatible and self.catalog.clipboard_folder.len_datas() != 0:

            if not paste_menu:
                menu.add_title(title=self.tr("Coller"))
                paste_menu = True

            title = translate_dict[folder_code]

            folder_menu = menu.add_action(qicon=get_icon(folder_icon),
                                          title=title,
                                          objectname=f"Paste_{folder_code}",
                                          short_link=help_folder_paste)

            sub_menu = self.hierarchie_sous_menu_coller(clipboard=self.catalog.clipboard_folder,
                                                        type_ele=folder_code,
                                                        title=title,
                                                        short_link=help_folder_paste)

            folder_menu.setMenu(sub_menu)

        if material_code in dict_compatible and self.catalog.clipboard_material.len_datas() != 0:

            if not paste_menu:
                menu.add_title(title=self.tr("Coller"))
                paste_menu = True

            title = translate_dict[material_code]

            material_menu = menu.add_action(qicon=get_icon(material_icon),
                                            title=title,
                                            objectname=f"Paste_{material_code}",
                                            short_link=help_material_paste)

            sub_menu = self.hierarchie_sous_menu_coller(clipboard=self.catalog.clipboard_material,
                                                        type_ele=material_code,
                                                        title=title,
                                                        short_link=help_material_paste)

            material_menu.setMenu(sub_menu)

        if component_code in dict_compatible and self.catalog.clipboard_component.len_datas() != 0:

            if not paste_menu:
                menu.add_title(title=self.tr("Coller"))
                paste_menu = True

            title = translate_dict[component_code]

            component_menu = menu.add_action(qicon=get_icon(component_icon),
                                             title=title,
                                             objectname=f"Paste_{component_code}",
                                             short_link=help_component_paste)

            sub_menu = self.hierarchie_sous_menu_coller(clipboard=self.catalog.clipboard_component,
                                                        type_ele=component_code,
                                                        title=title,
                                                        short_link=help_component_paste)

            component_menu.setMenu(sub_menu)

        if link_code in dict_compatible and self.catalog.clipboard_link.len_datas() != 0:

            if not paste_menu:
                menu.add_title(title=self.tr("Coller"))
                paste_menu = True

            title = translate_dict[link_code]

            link_menu = menu.add_action(qicon=get_icon(link_icon),
                                        title=title,
                                        objectname=f"Paste_{link_code}",
                                        short_link=help_link_paste)

            sub_menu = self.hierarchie_sous_menu_coller(clipboard=self.catalog.clipboard_link,
                                                        type_ele=link_code,
                                                        title=title,
                                                        short_link=help_link_paste)

            link_menu.setMenu(sub_menu)

        qs_selection_list = self.hierarchy.get_qs_selection_list()

        if self.catalog.attribut_coller_recherche(qs_selection_list):

            if self.catalog.clipboard_attribute.len_datas() != 0:

                if not paste_menu:
                    menu.add_title(title=self.tr("Coller"))

                title = translate_dict[attribute_code]

                attribute_menu = menu.add_action(qicon=get_icon(paste_icon),
                                                 title=title,
                                                 objectname=f"Paste_{attribute_code}",
                                                 short_link=help_attribute_paste)

                sub_menu = self.hierarchie_sous_menu_coller(clipboard=self.catalog.clipboard_attribute,
                                                            type_ele=attribute_code,
                                                            title=title,
                                                            short_link=help_attribute_paste)

                attribute_menu.setMenu(sub_menu)

        # ------------------------------
        # Modèle
        # ------------------------------

        if self.ui.model_bt.isEnabled() or self.ui.model_add_bt.isEnabled():
            menu.add_title(title=self.tr("Modèles"))

            menu.add_action(qicon=get_icon(attribute_model_show_icon),
                            title=self.tr("Afficher les modèles"),
                            action=self.models_widget.model_personnaliser,
                            tooltips=self.ui.model_bt.toolTip(),
                            short_link=self.ui.model_bt.whatsThis())

        if self.ui.model_add_bt.isEnabled():
            menu.add_action(qicon=get_icon(attribute_model_save_icon),
                            title=self.tr("Enregister attributs actuels comme nouveau modèle"),
                            action=self.hierarchie_modele_enregistrer,
                            tooltips=self.ui.model_add_bt.toolTip(),
                            short_link=self.ui.model_add_bt.whatsThis())

        # ------------------------------
        # Bible
        # ------------------------------

        if self.ui.library_bt.isEnabled():
            menu.add_title(title=self.tr("Bible externe"))

            menu.add_action(qicon=get_icon(external_bdd_show_icon),
                            title=self.tr("Afficher bibliothèque externe"),
                            action=self.hierarchie_bible_afficher,
                            tooltips=self.ui.library_bt.toolTip(),
                            short_link=self.ui.library_bt.whatsThis())

        menu.exec_(self.hierarchy.mapToGlobal(point))

    def hierarchie_sous_menu_coller(self, clipboard: ClipboardDatas,
                                    type_ele: str,
                                    title: str,
                                    short_link: str) -> QMenu:

        menu = MyContextMenu(short_link=short_link)  # OK
        menu.help_request.connect(self.asc.help_request)

        d = self.tr("Coller")

        if len(clipboard.datas) == 0:
            return menu

        icon_path = f":/Images/{type_ele.lower()}.png"

        menu.add_title(title=title)

        for datas in clipboard.datas:
            datas: dict

            title = datas.get("key")
            id_ele = datas.get("id", "0")

            menu.add_action(qicon=get_icon(icon_path),
                            title=f"{d} {title}",
                            action=lambda val1=title, val2=type_ele, val3=id_ele:
                            self.hierarchie_bt_coller_action_list(title=val1,
                                                                  ele_type=val2,
                                                                  id_ele=val3))

        return menu

    def hierarchie_sous_menu_ajouter(self, ele_type: str, short_link: str) -> QMenu:

        menu = MyContextMenu(short_link=short_link)  # OK
        menu.help_request.connect(self.asc.help_request)

        dict_onglets = self.models_widget.recherche_type_element(ele_type)

        if ele_type == attribute_code and self.ui.attribute_add_bt.isEnabled():
            menu.add_title(title=self.tr("Ajouter"))

            menu.add_action(qicon=get_icon(attribute_add_icon),
                            title=self.tr("Ajouter un nouvel attribut"),
                            action=self.attributs_ajouter)

        if len(dict_onglets) == 0:
            return menu

        menu.add_title(title=self.tr("Modèles"))

        for index_menu, nom_onglet in enumerate(dict_onglets):

            datas_onglet = dict_onglets.get(nom_onglet, None)

            if not isinstance(datas_onglet, tuple):
                continue

            if len(datas_onglet) != 2:
                continue

            icone_onglet, tooltips = datas_onglet

            if ele_type == "Material":

                menu.add_action(qicon=get_icon(icone_onglet),
                                title=nom_onglet,
                                action=lambda val1=nom_onglet: self.material_add_action(val1),
                                tooltips=tooltips)

            elif ele_type == "Component":

                menu.add_action(qicon=get_icon(icone_onglet),
                                title=nom_onglet,
                                action=lambda val1=nom_onglet: self.component_add_action(val1),
                                tooltips=tooltips)

            elif ele_type == "Attribute":

                menu.add_action(qicon=get_icon(icone_onglet),
                                title=nom_onglet,
                                action=lambda val1=nom_onglet: self.attribut_lancer_creation(val1),
                                tooltips=tooltips)
            else:
                continue

        return menu

    def hierarchie_sous_menu_lien(self) -> QMenu:

        menu = MyContextMenu(short_link=help_link_new)  # OK
        menu.help_request.connect(self.asc.help_request)

        # -------------------

        qs_current = self.hierarchy.get_current_qs()

        if isinstance(qs_current, (Component, Link)):
            qs_current = qs_current.parent()

        if not isinstance(qs_current, Material):
            return menu

        material_name = qs_current.text()

        # -------------------

        search_start = self.hierarchy.cat_model.index(0, 0)

        qm_link_search = self.hierarchy.cat_model.match(search_start, user_data_type, link_code, -1,
                                                        Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_link_search) == 0:
            return menu

        menu.add_title(title=self.tr("Ajouter un lien déjà existant"))

        # -------------------

        title_list = list()

        forbidden_list = set()
        self.catalog.link_get_forbidden_list(material_name=material_name, forbidden_list=forbidden_list)

        loop_message = self.tr("Lien Impossible : boucle")

        for qm_val in qm_link_search:

            title_original = qm_val.data()

            if not isinstance(title_original, str):
                continue

            if title_original in title_list:
                continue

            qm_parent = qm_val.parent()

            description = ""

            if qm_check(qm_parent):

                qm_description = self.hierarchy.cat_model.index(qm_val.row(), col_cat_desc, qm_parent)

                if qm_check(qm_description):
                    description = qm_description.data()

            title_list.append(title_original)

            if description == "" or description == title_original:
                title_temp = title_original
            else:
                title_temp = f"{title_original} - {description}"

            item = menu.add_action(title=title_temp,
                                   action=lambda val1=title_original, val2=description:
                                   self.lien_ajouter_action([[val1, val2]]))

            if title_original in forbidden_list:
                item.setEnabled(False)
                item.setToolTip(loop_message)
                item.setIcon(get_icon(lock_icon))
            else:
                item.setIcon(get_icon(link_icon))

        return menu

    @staticmethod
    def bouton_replier(liste_selection_qstandarditem) -> bool:

        replier = False

        if len(liste_selection_qstandarditem) > 0:

            qs: MyQstandardItem = liste_selection_qstandarditem[0]

            if qs is None:
                return replier

            liste_types_enfants = qs.get_children_type_list()

            if isinstance(qs, Folder):
                replier = folder_code in liste_types_enfants or material_code in liste_types_enfants

            elif isinstance(qs, Material):
                replier = component_code in liste_types_enfants

        return replier

    @staticmethod
    def a___________________attributes______():
        pass

    def attribut_menu_contextuel(self, point: QPoint):

        if self.catalog.catalog_path == "":
            return

        current_item = self.ui.attributes_detail.currentItem()

        if current_item is not None:
            self.asc.attribut_clic()

        menu = self.detail_menu
        menu.clear()

        # ------------------------------
        # Attribut
        # ------------------------------

        if self.catalog.change_made:
            menu.add_title(title=self.tr("Enregistrer"))

            menu.add_action(qicon=get_icon(save_icon),
                            title=self.tr("Enregistrer"),
                            action=self.catalog.catalog_save,
                            tooltips=self.ui.save_bt.toolTip(),
                            short_link=self.ui.save_bt.whatsThis())

            menu.add_action(qicon=get_icon(refresh_icon),
                            title=self.tr("Mettre à jour les catalogues"),
                            action=self.asc.catalogue_update,
                            tooltips=self.ui.update_cat_bt.toolTip(),
                            short_link=self.ui.update_cat_bt.whatsThis())

        selections = self.ui.attributes_detail.selectionModel().selectedRows(0)
        nb_selection = len(selections)

        titre_ajouter = False

        if self.asc.attributes_order_custom:
            menu.add_title(title=self.tr("Classement"))

            menu.add_action(qicon=get_icon(order_19),
                            title=self.tr("Gestion ordre personnalisé"),
                            action=self.attributes_order_custom_clicked,
                            short_link=help_attribute_order)

        if self.ui.attribute_add_bt.isEnabled():

            if not titre_ajouter:
                menu.add_title(title=self.tr("Attribut"))
                titre_ajouter = True

            add_attribut = menu.add_action(qicon=get_icon(attribute_add_icon),
                                           title=self.tr("Ajouter"),
                                           tooltips=self.ui.attribute_add_bt.toolTip(),
                                           objectname=f"Add_{attribute_code}",
                                           short_link=self.ui.attribute_add_bt.whatsThis())

            ss_menu = self.hierarchie_sous_menu_ajouter(ele_type=attribute_code,
                                                        short_link=self.ui.attribute_add_bt.whatsThis())

            if len(ss_menu.actions()) != 0:
                add_attribut.setMenu(ss_menu)

        if nb_selection != 0 and self.ui.del_bt.isEnabled():

            if not titre_ajouter:
                menu.add_title(title=self.tr("Attribut"))
                titre_ajouter = True

            menu.add_action(qicon=get_icon(delete_icon),
                            title=self.tr("Supprimer"),
                            action=self.catalog.attribute_delete,
                            tooltips=self.ui.del_bt.toolTip(),
                            short_link=help_attribute_del)

        if nb_selection != 0 and self.ui.cut_bt.isEnabled():

            if not titre_ajouter:
                menu.add_title(title=self.tr("Attribut"))
                titre_ajouter = True

            menu.add_action(qicon=get_icon(cut_icon),
                            title=self.tr("Couper"),
                            action=self.catalog.attribute_cut,
                            tooltips=self.ui.cut_bt.toolTip(),
                            short_link=help_attribute_copy)

        if nb_selection != 0 and self.ui.copy_bt.isEnabled():

            if not titre_ajouter:
                menu.add_title(title=self.tr("Attribut"))
                titre_ajouter = True

            menu.add_action(qicon=get_icon(copy_icon),
                            title=self.tr("Copier"),
                            action=self.catalog.attribute_copy,
                            tooltips=self.ui.copy_bt.toolTip(),
                            short_link=help_attribute_copy)

        qs: MyQstandardItem = self.hierarchy.get_current_qs()

        if qs is None:
            ele_type = folder_code
        else:
            ele_type = qs.data(user_data_type)

        if self.ui.paste_bt.isEnabled():

            d = self.tr("Coller")

            liste_selections_qs = self.hierarchy.get_qs_selection_list()

            if self.catalog.attribut_coller_recherche(liste_selections_qs):

                nb_keys = self.catalog.clipboard_attribute.len_datas()

                if nb_keys != 0:

                    description = ele_type != folder_code

                    if not description:

                        for key in self.catalog.clipboard_attribute.keys():
                            if "207" in key:
                                description = True
                                break

                    if description:

                        if not titre_ajouter:
                            menu.add_title(title=self.tr("Attribut"))

                        attribute_txt = self.tr("Attribut")
                        title = f"{d} {attribute_txt}"

                        menu_attribut = menu.add_action(qicon=get_icon(paste_icon),
                                                        title=title,
                                                        objectname=f"Paste_attribute",
                                                        short_link=help_attribute_paste)

                        ss_menu = self.hierarchie_sous_menu_coller(clipboard=self.catalog.clipboard_attribute,
                                                                   type_ele=attribute_code,
                                                                   title=title,
                                                                   short_link=help_attribute_paste)

                        menu_attribut.setMenu(ss_menu)

        if self.ui.model_bt.isEnabled() and ele_type != link_code:
            menu.add_title(title=self.tr("Modèles"))

            menu.add_action(qicon=get_icon(attribute_model_show_icon), title=self.tr("Afficher les modèles"),
                            action=self.models_widget.model_personnaliser,
                            tooltips=self.ui.model_bt.toolTip(),
                            short_link=self.ui.model_bt.whatsThis())

        if self.ui.model_add_bt.isEnabled() and ele_type != link_code:
            menu.add_action(qicon=get_icon(attribute_model_save_icon),
                            title=self.tr("Enregister attributs actuels comme nouveau modèle"),
                            action=self.hierarchie_modele_enregistrer,
                            tooltips=self.ui.model_add_bt.toolTip(),
                            short_link=self.ui.model_add_bt.whatsThis())

        menu.exec_(self.ui.attributes_detail.mapToGlobal(point))

    @staticmethod
    def a__________________undo_buttons______():
        pass

    def undo_button_pressed(self):

        self.asc.formula_widget_close()

        undo_list = self.catalog.undo_list.action_get_list()

        if len(undo_list) == 0:
            return

        last_name = undo_list[-1]

        last_action = self.catalog.undo_list.action_dict.get(last_name, None)

        if last_action is None:
            return

        self.catalog.history_pressed(last_action)

    def undo_menu(self):

        dict_actions = self.catalog.undo_list.action_dict

        if len(dict_actions) == 0:
            return

        self.undo_widget.chargement(dict_actions)

        move_widget_ss_bouton(button=self.ui.undo_list_bt, widget=self.undo_widget)

        self.undo_widget.show()

    def undo_action(self, undo_list: list):

        self.asc.formula_widget_close()

        for nom_action in undo_list:

            action = self.catalog.undo_list.action_dict.get(nom_action, None)

            if action is None:
                return

            self.catalog.history_pressed(action)

    @staticmethod
    def a___________________redo_buttons______():
        pass

    def redo_button_pressed(self):

        self.asc.formula_widget_close()

        redo_list = self.catalog.redo_list.action_get_list()

        if len(redo_list) == 0:
            return

        last_name = redo_list[-1]

        last_action = self.catalog.redo_list.action_dict.get(last_name, None)

        if last_action is None:
            return

        self.catalog.history_pressed(action_current=last_action, undo=False)

    def redo_menu(self):

        dict_actions = self.catalog.redo_list.action_dict

        if len(dict_actions) == 0:
            return

        self.redo_widget.chargement(dict_actions)

        move_widget_ss_bouton(button=self.ui.redo_list_bt, widget=self.redo_widget)

        self.redo_widget.show()

    def redo_action(self, redo_list: list):

        self.asc.formula_widget_close()

        for nom_action in redo_list:

            action = self.catalog.redo_list.action_dict.get(nom_action, None)

            if action is None:
                return

            self.catalog.history_pressed(action_current=action, undo=False)

    @staticmethod
    def a___________________descriptions_manage______():
        pass

    def hierarchie_description(self):

        self.hierarchy.description_show = not self.hierarchy.description_show

        self.hierarchy.header_manage()

    @staticmethod
    def a___________________expand_buttons______():
        pass

    def expand_menu_show(self):

        self.asc.formula_widget_close()

        expand_menu = self.hierarchy.expand_menu_creation()
        expand_menu.exec_(find_global_point(self.ui.expand_all_bt))

    @staticmethod
    def a___________________collapse_buttons______():
        pass

    def collapse_menu_show(self):

        self.asc.formula_widget_close()

        collapse_menu = self.hierarchy.collapse_menu_creation()
        collapse_menu.exec_(find_global_point(self.ui.collapse_all_bt))

    @staticmethod
    def a___________________move_buttons______():
        pass

    def monter(self):

        self.asc.formula_widget_close()

        liste_selection_qstandarditem = self.hierarchy.get_qs_selection_list()

        if len(liste_selection_qstandarditem) == 0:
            return

        # --------------
        # Analyse parents / row indexes
        # --------------

        select_dict = dict()

        for qs_selected in liste_selection_qstandarditem:

            if not isinstance(qs_selected, (Folder, Material, Component, Link)):
                continue

            qs_parent = self.hierarchy.get_parent(qs=qs_selected)

            if not isinstance(qs_parent, QStandardItem):
                continue

            parent_id = id(qs_parent)

            row_current = qs_selected.row()

            if parent_id in select_dict:

                row_list = select_dict[parent_id]["row_list"]

                row_list.append(row_current)

            else:

                if qs_parent == self.hierarchy.cat_model.invisibleRootItem():

                    child_list = self.hierarchy.get_root_children_type_list()

                else:

                    child_list = qs_parent.get_children_type_list()

                select_dict[parent_id] = {"row_list": [row_current],
                                          "child_count": len(child_list),
                                          "qs_parent": qs_parent}

        # --------------

        modifiers = QApplication.keyboardModifiers()
        liste_selections_fin = list()

        for datas in select_dict.values():

            if not isinstance(datas, dict):
                continue

            qs_parent = datas.get("qs_parent", None)

            if qs_parent == self.hierarchy.cat_model.invisibleRootItem():
                qs_parent_top_index = 0
            else:
                qs_parent_top_index = qs_parent.get_insertion_index()

            if not isinstance(qs_parent, QStandardItem):
                continue

            row_list = datas.get("row_list", list())

            if not isinstance(row_list, list):
                continue

            parent_row_count_no_attribute = datas.get("child_count", 0)

            if not isinstance(parent_row_count_no_attribute, int):
                continue

            if parent_row_count_no_attribute == 0:
                continue

            row_list.sort()

            for index_list, row_current in enumerate(row_list):

                if row_current == index_list + qs_parent_top_index:
                    liste_selections_fin.append(qs_parent.child(row_current, 0))
                    continue

                qs_current = qs_parent.child(row_current, col_cat_value)

                if not isinstance(qs_current, MyQstandardItem):
                    continue

                qs_deleted_list = qs_parent.takeRow(row_current)

                if not isinstance(qs_deleted_list, list):
                    continue

                if len(qs_deleted_list) != qs_parent.columnCount():
                    continue

                if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

                    row_new = index_list + qs_parent_top_index

                else:

                    row_new = row_current - 1

                qs_parent.insertRow(row_new, qs_deleted_list)

                qs_current = qs_parent.child(row_new, col_cat_value)

                if not isinstance(qs_current, MyQstandardItem):
                    continue

                liste_selections_fin.append(qs_parent.child(row_new, col_cat_value))

                self.catalog.history_move_ele(qs_current=qs_current,
                                              row_current=row_current,
                                              row_new=row_new)

        if len(liste_selections_fin) == 0:
            return

        self.hierarchy.select_list(selected_list=liste_selections_fin)

        self.catalog.change_made = True

    def descendre(self):

        self.asc.formula_widget_close()

        liste_selection_qstandarditem = self.hierarchy.get_qs_selection_list()

        if len(liste_selection_qstandarditem) == 0:
            return

        # --------------
        # Analyse parents / row indexes
        # --------------

        select_dict = dict()

        for qs_selected in liste_selection_qstandarditem:

            if not isinstance(qs_selected, (Folder, Material, Component, Link)):
                continue

            qs_parent = self.hierarchy.get_parent(qs=qs_selected)

            if not isinstance(qs_parent, QStandardItem):
                continue

            parent_id = id(qs_parent)

            row_current = qs_selected.row()

            if parent_id in select_dict:

                row_list = select_dict[parent_id]["row_list"]

                row_list.append(row_current)

            else:

                if qs_parent == self.hierarchy.cat_model.invisibleRootItem():

                    child_list = self.hierarchy.get_root_children_type_list()

                else:

                    child_list = qs_parent.get_children_type_list()

                select_dict[parent_id] = {"row_list": [row_current],
                                          "child_count": len(child_list),
                                          "qs_parent": qs_parent}

        # --------------

        modifiers = QApplication.keyboardModifiers()

        liste_selections_fin = list()

        for datas in select_dict.values():

            if not isinstance(datas, dict):
                continue

            qs_parent = datas.get("qs_parent", None)

            if not isinstance(qs_parent, QStandardItem):
                continue

            row_list = datas.get("row_list", list())

            if not isinstance(row_list, list):
                continue

            parent_row_count_no_attribute = datas.get("child_count", 0)

            if not isinstance(parent_row_count_no_attribute, int):
                continue

            if parent_row_count_no_attribute == 0:
                continue

            if parent_row_count_no_attribute == len(row_list):
                continue

            row_list.sort(reverse=True)

            for index_list, row_current in enumerate(row_list):

                qs_current = qs_parent.child(row_current, col_cat_value)

                if not isinstance(qs_current, MyQstandardItem):
                    continue

                parent_row_count = qs_parent.rowCount()

                if ((modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier)
                        and row_current == parent_row_count - 1):
                    continue

                if row_current == parent_row_count - 1 - index_list:
                    liste_selections_fin.append(qs_parent.child(row_current, 0))
                    continue

                qs_deleted_list = qs_parent.takeRow(row_current)

                if not isinstance(qs_deleted_list, list):
                    continue

                if len(qs_deleted_list) != qs_parent.columnCount():
                    continue

                if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

                    row_new = parent_row_count - index_list - 1

                else:

                    row_new = row_current + 1

                qs_parent.insertRow(row_new, qs_deleted_list)

                qs_current = qs_parent.child(row_new, col_cat_value)

                if not isinstance(qs_current, MyQstandardItem):
                    continue

                self.catalog.history_move_ele(qs_current=qs_current,
                                              row_current=row_current,
                                              row_new=row_new)

                liste_selections_fin.append(qs_parent.child(row_new, col_cat_value))

        if len(liste_selections_fin) == 0:
            return

        self.hierarchy.select_list(selected_list=liste_selections_fin)

        self.catalog.change_made = True

    @staticmethod
    def a___________________folder_add_button______():
        pass

    def folder_add(self):
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

            move_window_tool(widget_parent=self.asc, widget_current=self.number_widget, always_center=True)
            self.number_widget.personnaliser(folder_code, self.tr("Dossier"))

        else:
            self.item_ajouter_action([""], folder_code, self.tr("Dossier"))

    @staticmethod
    def a___________________material_add_manage______():
        pass

    def material_add(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

            move_window_tool(widget_parent=self.asc, widget_current=self.number_widget, always_center=True)

            self.number_widget.personnaliser(material_code, self.tr("Ouvrage"))

        else:
            self.item_ajouter_action([""], material_code, self.tr("Ouvrage"))

    def material_menu_show(self):

        self.material_menu.clear()

        dict_onglets = self.models_widget.recherche_type_element(material_code)

        self.material_menu.add_title(title=self.tr("Ouvrage"))

        for index_menu, nom_onglet in enumerate(dict_onglets):

            datas_onglet = dict_onglets.get(nom_onglet, None)

            if not isinstance(datas_onglet, tuple):
                continue

            if len(datas_onglet) != 2:
                continue

            icone_onglet, tooltips = datas_onglet

            self.material_menu.addAction(self.menu_deroulant_chemin(nom_onglet, icone_onglet, index_menu,
                                                                    material_code, tooltips))

        self.material_menu.exec_(find_global_point(self.ui.material_list_bt))

    def material_add_action(self, tab_name: str):

        self.material_menu.close()

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

            move_window_tool(widget_parent=self.asc, widget_current=self.number_widget, always_center=True)

            self.number_widget.personnaliser(material_code, tab_name)

        else:
            self.item_ajouter_action([""], material_code, tab_name)

    @staticmethod
    def a___________________component_add_button______():
        pass

    def component_add(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

            move_window_tool(widget_parent=self.asc, widget_current=self.number_widget, always_center=True)

            self.number_widget.personnaliser(component_code, self.tr("Composant"))

        else:
            self.item_ajouter_action([""], component_code, self.tr("Composant"))

    def component_menu_show(self):

        self.component_menu.clear()

        dict_onglets = self.models_widget.recherche_type_element(component_code)

        self.component_menu.add_title(title=self.tr("Composant"))

        for index_menu, nom_onglet in enumerate(dict_onglets):

            datas_onglet = dict_onglets.get(nom_onglet, None)

            if datas_onglet is None:
                continue

            if len(datas_onglet) != 2:
                continue

            icone_onglet, tooltips = datas_onglet

            self.component_menu.addAction(self.menu_deroulant_chemin(nom_onglet, icone_onglet, index_menu,
                                                                     component_code, tooltips))

        self.component_menu.exec_(find_global_point(self.ui.component_list_bt))

    def component_add_action(self, nom_onglet):

        self.component_menu.close()

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

            move_window_tool(widget_parent=self.asc, widget_current=self.number_widget, always_center=True)

            self.number_widget.personnaliser(component_code, nom_onglet)

        else:
            self.item_ajouter_action([""], component_code, nom_onglet)

    @staticmethod
    def a___________________link_add_manage______():
        pass

    def link_add(self):

        qs: MyQstandardItem = self.hierarchy.get_current_qs()

        if qs is None:
            msg(titre=application_title,
                message=self.tr("Aucun élément de la hiérarchie n'est sélectionné."),
                type_bouton=QMessageBox.Ok,
                icone_avertissement=True)
            return

        if isinstance(qs, Component) or isinstance(qs, Link):
            son_parent: MyQstandardItem = qs.parent()

            if son_parent is None:
                return

            if not isinstance(son_parent, Material):
                msg(titre=application_title,
                    message=self.tr("L'élément actuel ne peut pas recevoir de lien, désolé"),
                    type_bouton=QMessageBox.Ok,
                    icone_avertissement=True)
                return

            material_text = son_parent.text()
        else:

            material_text = qs.text()

        move_window_tool(widget_parent=self.asc, widget_current=self.link_creation_widget, always_center=True)

        self.link_creation_widget.link_creation_show(material_text)

    def link_menu_show(self):

        qs_current = self.hierarchy.get_current_qs()

        if isinstance(qs_current, (Component, Link)):
            qs_current = qs_current.parent()

        if not isinstance(qs_current, Material):
            return

        material_name = qs_current.text()

        # -------------------

        search_start = self.hierarchy.cat_model.index(0, 0)

        qm_link_search = self.hierarchy.cat_model.match(search_start, user_data_type, link_code, -1,
                                                        Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_link_search) == 0:
            msg(titre=application_title,
                message=self.tr("Aucun lien n'est présent dans ce catalogue."),
                type_bouton=QMessageBox.Ok,
                icone_avertissement=True)
            return

        # -------------------

        qs_list = list()
        title_list = list()

        forbidden_list = set()
        self.catalog.link_get_forbidden_list(material_name=material_name, forbidden_list=forbidden_list)

        loop_message = self.tr("Lien Impossible : boucle")

        for qm_val in qm_link_search:

            title_original = qm_val.data()

            if not isinstance(title_original, str):
                continue

            if title_original in title_list:
                continue

            qm_parent = qm_val.parent()

            description = ""

            if qm_check(qm_parent):

                qm_description = self.hierarchy.cat_model.index(qm_val.row(), col_cat_desc, qm_parent)

                if qm_check(qm_description):
                    description = qm_description.data()

            title_list.append(title_original)

            if description == "" or description == title_original:
                title_temp = title_original
            else:
                title_temp = f"{title_original} - {description}"

            if title_original not in forbidden_list:
                qs_link = QStandardItem(get_icon(link_icon), title_temp)
            else:
                qs_link = QStandardItem(get_icon(lock_icon), title_temp)
                qs_link.setToolTip(loop_message)
                qs_link.setEnabled(False)

            qs_link.setData(title_original, user_data_type)
            qs_link.setData(description, Qt.UserRole + 2)

            qs_list.append(qs_link)

        if len(title_list) == 0:
            msg(titre=application_title,
                message=self.tr("Aucun lien n'est présent dans ce catalogue."),
                type_bouton=QMessageBox.Ok,
                icone_avertissement=True)
            return

        # -------------------

        qm_current = self.link_add_widget.ui.links_list.currentIndex()
        current_text = ""

        if qm_check(qm_current):
            current_text = qm_current.data()

        self.link_add_widget.link_model.clear()
        self.link_add_widget.link_model.appendColumn(qs_list)

        self.link_add_widget.link_filter.setFilterRegExp(self.link_add_widget.ui.search_bar.text())

        if current_text != "":
            search_start = self.link_add_widget.link_filter.index(0, 0)
            qm_link_search = self.link_add_widget.link_filter.match(search_start, Qt.DisplayRole, current_text,
                                                                    -1, Qt.MatchExactly)

            if len(qm_link_search) != 0:
                qm_new = qm_link_search[0]
                self.link_add_widget.ui.links_list.setCurrentIndex(qm_new)
                self.link_add_widget.ui.links_list.scrollTo(qm_new,
                                                            QAbstractItemView.PositionAtTop)

        self.link_add_widget.link_filter.sort(0, Qt.AscendingOrder)

        move_widget_ss_bouton(self.ui.link_list_bt, self.link_add_widget)

        self.link_add_widget.show()

    @staticmethod
    def a___________________attributes_add_button______():
        pass

    def attributs_ajouter(self):

        self.asc.formula_widget_close()

        current_qs: MyQstandardItem = self.hierarchy.get_current_qs()

        if current_qs is None:
            return

        liste_attributs_actuel = current_qs.get_attribute_numbers_list()
        liste_attributs_actuel.insert(0, attribut_default_obj.current)

        self.attributes_widget.attribute_show(current_mod="",
                                              attributes_list=liste_attributs_actuel,
                                              current_widget=self.asc)

    def attributs_menu_afficher(self):

        self.attribute_menu.clear()

        dict_onglets = self.models_widget.recherche_type_element(attribute_code)

        self.attribute_menu.add_title(self.tr("Attribut"))

        for index_menu, nom_onglet in enumerate(dict_onglets):

            datas_onglet = dict_onglets.get(nom_onglet, None)

            if datas_onglet is None:
                continue

            if len(datas_onglet) != 2:
                continue

            icone_onglet, tooltips = datas_onglet

            self.attribute_menu.addAction(self.menu_deroulant_chemin(nom_onglet, icone_onglet, index_menu,
                                                                     attribute_code, tooltips))

        self.attribute_menu.popup(find_global_point(self.ui.attribute_list_bt))

    def attribut_lancer_creation(self, nom_onglet):

        liste_attribut = self.models_widget.creation_liste_attributs(nom_onglet)

        self.attribute_menu.close()

        if len(liste_attribut) == 0:
            return

        self.attributs_ajouter_action(liste_attribut)

    def attributs_ajouter_action(self, liste_numeros: list):

        qm_filter_selection_list: list = self.hierarchy.get_qm_filter_selection_list()

        for qm_filter in qm_filter_selection_list:

            if not qm_check(qm_filter):
                print("bar_action -- attributs_ajouter_action --> not qm_check(qm_filter)")
                continue

            qs_parent = self.hierarchy.get_qs_by_qm(qm=qm_filter)

            if not isinstance(qs_parent, (Material, Component)):
                print("bar_action -- attributs_ajouter_action --> not isinstance(qs_parent, (Material, Component))")
                continue

            attributes_list = qs_parent.get_attribute_numbers_list()
            attributes_list.insert(0, attribute_default_base)

            attribute_data_layer = list()
            attribute_data_fill = list()
            attribute_data_room = list()

            for number_str in liste_numeros:

                if number_str in attributes_list:
                    print("bar_action -- attribute_add_list -- number_str in attributes_list")                                     
                    continue

                index_insertion = qs_parent.get_attribute_insertion_index(number_str)

                if number_str in attribute_val_default_room:

                    if number_str == "232":
                        value = self.allplan.traduire_valeur_232(default=True)

                    elif number_str == "233":
                        value = self.allplan.traduire_valeur_233(default=True)

                    elif number_str == "235":
                        value = self.allplan.traduire_valeur_235(default=True)

                    else:
                        value = attribute_val_default_room[number_str]

                else:

                    attribute_obj = self.allplan.attributes_dict.get(number_str)

                    if isinstance(attribute_obj, AttributeDatas):

                        value = attribute_obj.value

                    else:

                        value = ""

                qs_list = self.creation.attribute_line(value=value, number_str=number_str)

                qs_parent.insertRow(index_insertion, qs_list)

                qs_value = qs_list[col_cat_value]

                if not isinstance(qs_value, Attribute):
                    continue

                if number_str in attribute_val_default_layer:

                    attribute_data_layer.append(AttributeData(guid_current=qs_value.data(user_guid),
                                                              row_current=index_insertion,
                                                              qs_list=qs_list))

                    if number_str == attribute_val_default_layer_last:
                        self.catalog.history_add_attribute(guid_parent=qs_value.data(user_guid),
                                                           attribute_data=attribute_data_layer,
                                                           parent_name=qs_value.text(),
                                                           number=self.tr("Groupe Layer"))

                elif number_str in attribute_val_default_fill:

                    attribute_data_fill.append(AttributeData(guid_current=qs_value.data(user_guid),
                                                             row_current=index_insertion,
                                                             qs_list=qs_list))

                    if number_str == attribute_val_default_fill_last:
                        self.catalog.history_add_attribute(guid_parent=qs_value.data(user_guid),
                                                           attribute_data=attribute_data_fill,
                                                           parent_name=qs_value.text(),
                                                           number=self.tr("Groupe Remplissage"))

                elif number_str in attribute_val_default_room:

                    attribute_data_room.append(AttributeData(guid_current=qs_value.data(user_guid),
                                                             row_current=index_insertion,
                                                             qs_list=qs_list))

                    if number_str == attribute_val_default_room_last:
                        self.catalog.history_add_attribute(guid_parent=qs_value.data(user_guid),
                                                           attribute_data=attribute_data_room,
                                                           parent_name=qs_value.text(),
                                                           number=self.tr("Groupe Pièce"))

                else:

                    attribute_data = [(AttributeData(guid_current=qs_value.data(user_guid),
                                                     row_current=index_insertion,
                                                     qs_list=qs_list))]

                    self.catalog.history_add_attribute(guid_parent=qs_value.data(user_guid),
                                                       attribute_data=attribute_data,
                                                       parent_name=qs_value.text(),
                                                       number=f"@{number_str}@")

        self.hierarchie_selection_change()
        self.catalog.change_made = True

    @staticmethod
    def a___________________edit_buttons______():
        pass

    def hierarchie_supprimer(self):

        self.asc.formula_widget_close()

        object_name = self.ui.del_bt.objectName()

        if object_name == f"delete_{attribute_code}":

            liste_details = self.ui.attributes_detail.selectionModel().selectedRows()
            nb_details = len(liste_details)

            if nb_details == 0:
                return

            self.catalog.attribute_delete()
            return

        self.catalog.catalog_delete()

    def hierarchie_couper(self):

        object_name = self.ui.cut_bt.objectName()

        if object_name == f"cut_{attribute_code}":

            liste_details = self.ui.attributes_detail.selectionModel().selectedRows()
            nb_details = len(liste_details)

            if nb_details == 0:
                return

            self.catalog.attribute_cut()
            return

        self.catalog.catalog_copy_action(cut=True)

    def hierarchie_copier(self):

        object_name = self.ui.copy_bt.objectName()

        if object_name == f"copy_{attribute_code}":

            liste_details = self.ui.attributes_detail.selectionModel().selectedRows()
            nb_details = len(liste_details)

            if nb_details == 0:
                return

            self.catalog.attribute_copy()
            return

        self.catalog.catalog_copy_action()

    @staticmethod
    def a___________________paste_buttons______():
        pass

    def hierarchie_coller(self):
        """
        Le bouton coller vient d'être appuyé
        :return:
        """

        self.asc.formula_widget_close()

        object_name = self.ui.paste_bt.objectName()

        if object_name == f"paste_{attribute_code}" or self.catalog.clipboard_current == attribute_code:
            self.catalog.attribute_paste()
            self.hierarchie_selection_change()
            return

        if self.catalog.clipboard_current == "":
            return

        self.catalog.catalog_paste(self.catalog.clipboard_current)

    def hierarchie_coller_menu_afficher(self):
        """
        Gestion du menu coller selon le nom du bouton
        :return:
        """

        self.asc.formula_widget_close()

        qstandarditem: Folder = self.hierarchy.get_current_qs()

        if qstandarditem is None:
            dict_compatible = {folder_code: self.tr("Enfant")}
            type_element = folder_code
        else:
            dict_compatible = qstandarditem.get_type_possibilities()
            type_element = qstandarditem.data(user_data_type)

        self.paste_widget.clear_menu()

        if folder_code in dict_compatible and self.catalog.clipboard_folder.len_datas() != 0:
            self.hierarchie_coller_menu_creation(clipboard=self.catalog.clipboard_folder,
                                                 type_ele=folder_code)

        if material_code in dict_compatible and self.catalog.clipboard_material.len_datas() != 0:
            self.hierarchie_coller_menu_creation(clipboard=self.catalog.clipboard_material,
                                                 type_ele=material_code)

        if component_code in dict_compatible and self.catalog.clipboard_component.len_datas() != 0:
            self.hierarchie_coller_menu_creation(clipboard=self.catalog.clipboard_component,
                                                 type_ele=component_code)

        if link_code in dict_compatible and self.catalog.clipboard_link.len_datas() != 0:
            self.hierarchie_coller_menu_creation(clipboard=self.catalog.clipboard_link,
                                                 type_ele=link_code)

        liste_selections_qs = self.hierarchy.get_qs_selection_list()

        if self.catalog.attribut_coller_recherche(liste_selections_qs):

            nb_keys = self.catalog.clipboard_attribute.len_datas()

            if nb_keys != 0:

                description = type_element != folder_code

                if not description:

                    for key in self.catalog.clipboard_attribute.keys():
                        if "207" in key:
                            description = True
                            break

                if description:
                    self.hierarchie_coller_menu_creation(clipboard=self.catalog.clipboard_attribute,
                                                         type_ele=attribute_code)

        move_widget_ss_bouton(self.ui.paste_list_bt, self.paste_widget)
        self.paste_widget.chargement()

    def hierarchie_coller_menu_creation(self, clipboard: ClipboardDatas, type_ele: str):

        if clipboard.len_datas() > 0:
            qs_master: QStandardItem = self.paste_widget.append_titre(ele_type=type_ele)

            for datas in clipboard.datas:
                datas: dict

                titre = datas.get("key")
                id_ele = datas.get("id", "0")

                self.paste_widget.append_element(qs_master=qs_master,
                                                 titre=titre,
                                                 type_element=type_ele,
                                                 id_ele=id_ele)

    def hierarchie_bt_coller_action_list(self, title: str, ele_type: str, id_ele="0"):

        clipboard, clipboard_cut = self.catalog.get_clipboard(ele_type=ele_type, reset_clipboard=False)

        clipboard: ClipboardDatas
        clipboard_cut: ClipboardDatas

        if not isinstance(clipboard, ClipboardDatas) or not isinstance(clipboard_cut, ClipboardDatas):
            return

        if ele_type == folder_code:
            titre_element = self.tr("Dossier")
        elif ele_type == material_code:
            titre_element = self.tr("Ouvrage")
        elif ele_type == component_code:
            titre_element = self.tr("Composant")
        elif ele_type == link_code:
            titre_element = self.tr("Lien")
        elif ele_type == attribute_code:
            titre_element = self.tr("Attribut")
        else:
            return

        if clipboard.check_title_exist(title):

            if ele_type == attribute_code:
                resultat = self.catalog.attribute_paste(title, id_ele)
            else:
                resultat = self.catalog.hierarchie_coller_datas(clipboard, clipboard_cut, title, id_ele)

        elif title == titre_element:

            if ele_type == attribute_code:
                resultat = self.catalog.attribute_paste()
            else:
                resultat = self.catalog.hierarchie_coller_datas(clipboard, clipboard_cut)

        else:
            print(f"onglet_hierarchie -- hierarchie_bt_coller_action_list -- erreur titre : {title}")
            return

        if not resultat:
            print("onglet_hierarchie -- hierarchie_bt_coller_action_list -- erreur resultat")
            return

        self.catalog.clipboard_current = ele_type

        self.hierarchie_selection_change()

        if clipboard_cut.len_datas() == 0:
            return

        self.catalog.hierarchie_couper_coller_action(clipboard_cut=clipboard_cut)

    @staticmethod
    def attribut_coller_recherche_existant(qstandarditem: MyQstandardItem) -> tuple:

        rows_count: int = qstandarditem.rowCount()

        numbers_list = list()
        values_list = list()
        qs_list = list()

        for attribute_index in range(rows_count):

            qs_val: MyQstandardItem = qstandarditem.child(attribute_index, col_cat_value)
            qs_number: MyQstandardItem = qstandarditem.child(attribute_index, col_cat_number)

            ele_type: str = qs_val.data(user_data_type)

            if attribute_code not in ele_type:
                return numbers_list, values_list, qs_list

            numbers_list.append(qs_number.text())
            values_list.append(qs_val.text())
            qs_list.append(qs_val)

        return list(), list(), list()

    @staticmethod
    def a__________________link_buttons______():
        pass

    def lien_ajouter_action(self, link_list_add: list):

        self.asc.formula_widget_close()

        qs_selection_list: list = self.hierarchy.get_qs_selection_list()

        if len(qs_selection_list) == 0:
            print("bar_action -- lien_ajouter_action -- len(qs_selection_list) == 0")
            return

        current_selection = None

        for qs_current in qs_selection_list:

            qs_current: Material

            if not isinstance(qs_current, (Material, Component, Link)):
                print("bar_action -- lien_ajouter_action -- not isinstance(qs_current, Material)")
                continue

            elements_compatibles: dict = qs_current.get_add_possibilities(ele_type=link_code)

            elements_compatibles_count = len(elements_compatibles)

            if elements_compatibles_count != 1:
                continue

            values_list: list = list(elements_compatibles.values())[0]

            if len(values_list) != 2:
                print("bar_action -- lien_ajouter_action -- len(values_list) != 2")
                continue

            qs_parent, index_ele = values_list

            if not isinstance(qs_parent, Material) or not isinstance(index_ele, int):
                print("bar_action -- lien_ajouter_action -- not isinstance(qs_destination, Material)")
                continue

            destination_txt = qs_parent.text()

            if not isinstance(destination_txt, str):
                print("bar_action -- lien_ajouter_action -- not isinstance(destination_txt, str)")
                continue

            destination_txt = destination_txt.upper()

            for link_data in link_list_add:

                if not isinstance(link_data, list):
                    print("bar_action -- lien_ajouter_action -- not isinstance(link_data, list)")
                    continue

                if len(link_data) != 2:
                    print("bar_action -- lien_ajouter_action -- len(link_data) != 2")
                    continue

                material_name, description = link_data

                if not isinstance(material_name, str):
                    print("bar_action -- lien_ajouter_action -- not isinstance(material_name, str)")
                    continue

                if not isinstance(description, str):
                    print("bar_action -- lien_ajouter_action -- not isinstance(material_name, str)")
                    continue

                liste_ele = self.creation.link_line(value=material_name, description=description)

                qs_current: MyQstandardItem = liste_ele[col_cat_value]

                qs_parent.insertRow(index_ele, liste_ele)

                current_selection = qs_current

                link_list.append(material_name)

                if destination_txt not in material_with_link_list:
                    material_with_link_list.append(destination_txt)

                self.catalog.material_refresh_look(material_name=material_name)

                self.catalog.history_add_ele(qs_current=qs_current)

        if current_selection is not None:
            self.hierarchy.select_list(selected_list=[current_selection])

        self.catalog.change_made = True

    @staticmethod
    def a___________________model_buttons______():
        pass

    def hierarchie_modele_enregistrer(self):

        self.asc.formula_widget_close()

        if self.ui.attributes_detail.count() == 0:
            return

        liste_hierarchie_selection: list = self.hierarchy.get_qm_filter_selection_list()

        if len(liste_hierarchie_selection) != 1:
            return

        hierarchie_qmodelindex = liste_hierarchie_selection[0]

        hierarchie_qmodelindex: QModelIndex

        type_onglet = hierarchie_qmodelindex.data(user_data_type)

        if type_onglet != material_code and type_onglet != component_code:
            return

        qstandarditem: MyQstandardItem = self.hierarchy.get_qs_by_qm(qm=hierarchie_qmodelindex)

        if qstandarditem is None:
            print("onglet_hierarchie -- attributs_coller_action --> qstandarditem is None")
            return

        liste_attributs = qstandarditem.get_attribute_numbers_list()

        if len(liste_attributs) == 0:
            return

        if attribut_default_obj.current in liste_attributs:
            liste_attributs.remove(attribut_default_obj.current)

        for numero in attribute_val_default_layer:

            if numero == attribute_val_default_layer_first:
                continue

            if numero in liste_attributs:
                liste_attributs.remove(numero)

        for numero in attribute_val_default_fill:

            if numero == attribute_val_default_fill_first:
                continue

            if numero in liste_attributs:
                liste_attributs.remove(numero)

        for numero in attribute_val_default_room:

            if numero == attribute_val_default_room_first:
                continue

            if numero in liste_attributs:
                liste_attributs.remove(numero)

        # for numero in attribute_val_default_ht:
        #
        #     if numero == "112":
        #         continue
        #
        #     if numero in liste_attributs:
        #         liste_attributs.remove(numero)

        type_onglet = qstandarditem.data(user_data_type)

        nom_onglet = qstandarditem.text()

        datas_elements = settings_read(model_config_file)

        if nom_onglet in datas_elements:
            nom_onglet = find_new_title(nom_onglet, list(datas_elements))

        if nom_onglet is None:
            return

        datas_elements[nom_onglet] = {"icon": f"{type_onglet.lower()}.png",
                                      "type": type_onglet,
                                      "attributes": liste_attributs}

        settings_save(model_config_file, datas_elements)

        b = self.tr("Voulez-vous afficher les modèles d'attributs")

        if msg(titre=application_title,
               message=f"{b}?",
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               bt_ok=self.tr("Afficher les modèles"),
               defaut_bouton=QMessageBox.Ok,
               icone_question=True) != QMessageBox.Ok:
            return

        self.models_widget.model_personnaliser(type_onglet, nom_onglet)

    @staticmethod
    def a___________________library_buttons______():
        pass

    def hierarchie_bible_afficher(self):

        self.asc.formula_widget_close()

        if self.library_widget.isVisible():
            self.library_widget.raise_()
            return

        current_qs = self.hierarchy.get_current_qs()

        if current_qs is None:
            current_qs = self.hierarchy.cat_model.invisibleRootItem()

        self.library_widget.show_library(current_qs=current_qs,
                                         current_parent=self.asc)

    def library_selection_changed(self):

        if not self.library_widget.isVisible():
            return

        if self.library_widget.isMinimized():
            self.library_widget.showNormal()
        elif not self.library_widget.isActiveWindow():
            self.library_widget.raise_()

        current_qs = self.hierarchy.get_current_qs()

        if current_qs is None:
            current_qs = self.hierarchy.cat_model.invisibleRootItem()

        self.library_widget.hierarchy_selection_changed(new_qs=current_qs)

    @staticmethod
    def a___________________attributs_order______():
        pass

    def attributes_order_changed(self, attributes_order=0, attributes_order_col=0, attributes_order_custom=False):

        self.ui.attributes_detail.setFocus()

        if attributes_order_custom:

            self.asc.attributes_order_custom = self.attributes_order_custom_load()

            if self.asc.attributes_order_custom:
                self.hierarchie_selection_change()
                return

        self.asc.attributes_order = attributes_order
        self.asc.attributes_order_col = attributes_order_col
        self.asc.attributes_order_custom = False
        self.asc.attributes_order_list = list()

        self.hierarchie_selection_change()

    def attributes_order_custom_load(self) -> bool:

        order_settings = settings_read(order_setting_file)

        if not isinstance(order_settings, dict):
            return False

        other_attributes = order_settings.get("other", order_setting_datas.get("other", 0))

        if not isinstance(other_attributes, int):
            return False

        if other_attributes == 1:
            self.asc.attributes_order = 1
            self.asc.attributes_order_col = 0

        elif other_attributes == 2:
            self.asc.attributes_order = 0
            self.asc.attributes_order_col = 1

        elif other_attributes == 3:
            self.asc.attributes_order = 1
            self.asc.attributes_order_col = 1

        else:
            self.asc.attributes_order = 0
            self.asc.attributes_order_col = 0

        attributes_list = self.order_widget.order_read_config()

        if not isinstance(attributes_list, list):
            return False

        if len(attributes_list) == 0:
            return False

        self.asc.attributes_order_list = attributes_list
        return True

    def attributes_order_custom_clicked(self):

        self.asc.formula_widget_close()
        self.order_widget.order_show()

    @staticmethod
    def a___________________attributs_selection______():
        pass

    def attributs_select_all(self):

        nb_items = self.ui.attributes_detail.count()

        for index_item in range(nb_items):

            if index_item == 0:
                continue

            listwidgetitem: QListWidgetItem = self.ui.attributes_detail.item(index_item)

            listwidgetitem.setSelected(True)

    def attributs_deselect_all(self):
        self.ui.attributes_detail.clearSelection()

    @staticmethod
    def a___________________attributs_details______():
        pass

    def menu_deroulant_chemin(self, nom_onglet: str, icone_onglet: str, index_menu: int,
                              type_element: str, tooltips="") -> QWidgetAction:

        action_widget = QWidgetAction(self.asc)
        action_widget.setEnabled(True)
        action_widget.setIconVisibleInMenu(False)

        widget = QWidget()

        font = widget.font()
        font.setPointSize(taille_police_menu)
        widget.setFont(font)

        widget.setMinimumWidth(150)
        widget.setFixedHeight(menu_ht_ligne)

        if index_menu % 2:
            widget.setStyleSheet("QWidget{background-color: #E7E7E7}"
                                 "QPushButton:hover{background-color: #BAD0E7; "
                                 "border-style: inset; border-width: 0px;}"
                                 "QPushButton:pressed{background-color: #8FADCC; "
                                 "border-style: inset; border-width: 0px;}")
        else:
            widget.setStyleSheet("QWidget{background-color: #FFFFFF}"
                                 "QPushButton:hover{background-color: #BAD0E7; "
                                 "border-style: inset; border-width: 0px;}"
                                 "QPushButton:pressed{background-color: #8FADCC; "
                                 "border-style: inset; border-width: 0px;}")

        horizontallayout = QHBoxLayout(widget)
        horizontallayout.setContentsMargins(6, 0, 6, 0)

        # ---------

        pushbutton_creation = QPushButton(get_icon(icone_onglet), f"   {nom_onglet}")
        pushbutton_creation.setFlat(True)
        pushbutton_creation.setIconSize(QSize(18, 18))
        pushbutton_creation.setFixedHeight(menu_ht_ligne)
        pushbutton_creation.setMinimumWidth(150)
        pushbutton_creation.setFont(font)
        pushbutton_creation.setStyleSheet("padding-left:4px; text-align:left")
        pushbutton_creation.setFont(font)

        horizontallayout.addWidget(pushbutton_creation)

        if type_element == material_code:
            pushbutton_creation.clicked.connect(lambda: self.material_add_action(nom_onglet))
        elif type_element == component_code:
            pushbutton_creation.clicked.connect(lambda: self.component_add_action(nom_onglet))
        else:
            pushbutton_creation.clicked.connect(lambda: self.attribut_lancer_creation(nom_onglet))

        pushbutton_creation.setToolTip(tooltips)

        # ---------

        pushbutton_options = QPushButton(get_icon(options_icon), "")
        pushbutton_options.setFlat(True)
        pushbutton_options.setIconSize(QSize(18, 18))
        pushbutton_options.setFixedSize(QSize(24, 24))

        tooltips_msg = self.tr("Éditer les options de :")

        pushbutton_options.setToolTip(f"{tooltips_msg} {nom_onglet}")

        if nom_onglet == self.tr("Sans attribut"):
            pushbutton_options.setEnabled(False)
        else:
            pushbutton_options.clicked.connect(
                lambda: self.models_widget.model_personnaliser(nom_onglet=nom_onglet, type_element=type_element))

        # ---------
        horizontallayout.addWidget(pushbutton_options)

        widget.sizeHint()

        action_widget.setDefaultWidget(widget)

        return action_widget

    def item_ajouter_action(self, titles_list: list, ele_type="", tab_name=""):

        self.asc.formula_widget_close()

        if ele_type == "":
            ele_type = material_code

        qs_selection_list: list = self.hierarchy.get_qs_selection_list()

        if len(qs_selection_list) == 0:

            if ele_type != folder_code:
                return

            current_qstandarditem = None
            liste_titre_actuel = self.hierarchy.get_root_children_name(upper=True)

            for title in titles_list:

                if isinstance(title, list):
                    title, description = title
                else:
                    description = ""

                if not isinstance(title, str):
                    continue

                title = title.strip()

                if title == "":
                    if ele_type == folder_code:
                        title = self.tr("Dossier")
                    elif ele_type == material_code:
                        title = self.tr("Ouvrage")
                    elif ele_type == component_code:
                        title = self.tr("Composant")
                    else:
                        continue

                nouveau_nom = find_new_title(base_title=title, titles_list=liste_titre_actuel)

                liste_titre_actuel.append(nouveau_nom.upper())

                liste_ajouter = self.creation.folder_line(value=nouveau_nom, description=description)

                self.hierarchy.cat_model.invisibleRootItem().appendRow(liste_ajouter)

                qs_val: MyQstandardItem = liste_ajouter[col_cat_value]

                current_qstandarditem = qs_val

            if current_qstandarditem is not None:
                self.hierarchy.select_list(selected_list=[current_qstandarditem])

            return

        expanded_list = list()
        current_selection = None

        for qs in qs_selection_list:

            qs: Material

            if qs is None:
                print(f"onglet_hierarchie -- item_ajouter_action --> qstandarditem is None")
                continue

            elements_compatibles: dict = qs.get_add_possibilities(ele_type)

            elements_compatibles_count = len(elements_compatibles)

            if elements_compatibles_count == 0:
                continue

            if elements_compatibles_count == 1:

                values_list: list = list(elements_compatibles.values())[0]

                qs_destination, insertion_index = values_list

                if qs_destination is None:
                    if ele_type != folder_code:
                        continue

                    qs_destination = self.hierarchy.cat_model.invisibleRootItem()

            elif elements_compatibles_count == 2:

                # Parent --
                liste_valeurs_parent: list = elements_compatibles[self.tr("Frère")]
                qstandarditem_1, row_parent = liste_valeurs_parent

                if qstandarditem_1 is None or qstandarditem_1 == self.hierarchy.cat_model.invisibleRootItem():

                    if ele_type != folder_code:
                        continue

                    qstandarditem_1 = self.hierarchy.cat_model.invisibleRootItem()
                    parent_texte = self.tr("Racine de la hiérarchie")

                else:
                    parent_texte = qstandarditem_1.text()

                parent_type = qstandarditem_1.data(user_data_type)

                # enfant --
                liste_valeurs_enfant: list = elements_compatibles[self.tr("Enfant")]
                qstandarditem_2, row_enfant = liste_valeurs_enfant
                enfant_texte = qstandarditem_2.text()
                enfant_type = qstandarditem_2.data(user_data_type)

                msgbox = MsgLocalication()

                # Si un élément est selectionné
                if len(titles_list) == 1:
                    msgbox.show_message_location(message=self.tr("Où voulez-vous ajouter cet élément?"),
                                                 parent_txt=parent_texte,
                                                 parent_type=parent_type,
                                                 child_txt=enfant_texte,
                                                 child_type=enfant_type)

                else:
                    msgbox.show_message_location(message=self.tr("Où voulez-vous ajouter ces éléments?"),
                                                 parent_txt=parent_texte,
                                                 parent_type=parent_type,
                                                 child_txt=enfant_texte,
                                                 child_type=enfant_type)

                reponse = msgbox.reponse

                # Si l'utilisateur annule -> quitter
                if reponse == QMessageBox.Cancel:
                    return

                # Si l'utilisateur choisi en dessous, ajout dans le parent du dossier selectionné ->
                # frère du dossier selection
                if reponse == QMessageBox.No:

                    qs_destination: MyQstandardItem = qstandarditem_1
                    insertion_index = row_parent

                # Si l'utilisateur choisi "Dans ce dossier" , ajout dans le dossier selectionné ->
                # enfant du dossier selectionné
                else:

                    qs_destination: MyQstandardItem = qstandarditem_2
                    insertion_index = row_enfant

            else:
                continue

            repetition = 0

            for title in titles_list:

                if isinstance(title, list):
                    title, description = title
                else:
                    description = ""

                if not isinstance(title, str):
                    continue

                if qs_destination == self.hierarchy.cat_model.invisibleRootItem():

                    if ele_type == folder_code:

                        liste_titre_actuel = self.hierarchy.get_root_children_name()

                    else:
                        continue

                else:

                    if ele_type == material_code:
                        liste_titre_actuel = material_upper_list

                    else:
                        liste_titre_actuel = qs_destination.get_children_name(upper=True)

                title = title.strip()

                if title == "":
                    if ele_type == folder_code:
                        title = self.tr("Dossier")
                    elif ele_type == material_code:
                        title = self.tr("Ouvrage")
                    elif ele_type == component_code:
                        title = self.tr("Composant")

                nouveau_nom = find_new_title(base_title=title, titles_list=liste_titre_actuel)

                if ele_type == folder_code:
                    liste_ajouter = self.creation.folder_line(value=nouveau_nom, description=description)

                elif ele_type == material_code:

                    if description == "":
                        description = nouveau_nom

                    liste_ajouter = self.creation.material_line(value=nouveau_nom, description=description)

                    material_upper_list.append(nouveau_nom.upper())
                    material_list.append(nouveau_nom)

                else:

                    if description == "":
                        description = nouveau_nom

                    liste_ajouter = self.creation.component_line(value=nouveau_nom, description=description)

                qs_val: MyQstandardItem = liste_ajouter[col_cat_value]

                if ele_type == material_code or ele_type == component_code:

                    attributes_list = self.models_widget.creation_liste_attributs(tab_name)

                    for number in attributes_list:
                        qs_attribute_list = self.creation.attribute_line(value="", number_str=number, use_default=True)
                        qs_val.appendRow(qs_attribute_list)

                qs_destination.insertRow(insertion_index + repetition, liste_ajouter)

                qs_current = liste_ajouter[col_cat_value]

                if not isinstance(qs_current, MyQstandardItem):
                    print("bar_action -- item_ajouter_action -- not isinstance(qs_current, MyQstandardItem)")
                    continue

                self.catalog.history_add_ele(qs_current=qs_current)

                repetition += 1

                if ele_type == material_code or ele_type == folder_code:
                    if qs_destination not in expanded_list:
                        expanded_list.append(qs_destination)

                current_selection = qs_val

        if len(expanded_list) != 0:
            self.hierarchy.expand_list(expanded_list)

        if current_selection is not None:
            self.hierarchy.select_list(selected_list=[current_selection])

        self.catalog.change_made = True

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent.MouseButtonRelease):

        if event.type() != QEvent.MouseButtonRelease:
            return super().eventFilter(obj, event)

        if event.button() == Qt.RightButton:
            return super().eventFilter(obj, event)

        if not isinstance(obj, QMenu):
            return super().eventFilter(obj, event)

        if not obj.isVisible():
            return super().eventFilter(obj, event)

        position = event.pos()

        action = obj.actionAt(position)

        if not isinstance(action, QAction):
            return super().eventFilter(obj, event)

        name_actual = action.objectName()

        if not name_actual.startswith("Paste") and not name_actual.startswith("Add"):
            return super().eventFilter(obj, event)

        print(self.attribute_menu.height())

        obj.close()

        if name_actual == f"Add_{material_code}":
            self.material_add()
            return super().eventFilter(obj, event)

        if name_actual == f"Add_{component_code}":
            self.component_add()
            return super().eventFilter(obj, event)

        if name_actual == f"Add_{link_code}":
            self.link_add()
            return super().eventFilter(obj, event)

        if name_actual == f"Add_{attribute_code}":
            self.attributs_ajouter()
            return super().eventFilter(obj, event)

        titre = action.text()

        if name_actual == f"Paste_{folder_code}":
            self.hierarchie_bt_coller_action_list(title=titre, ele_type=folder_code, id_ele="0")
            return super().eventFilter(obj, event)

        if name_actual == f"Paste_{material_code}":
            self.hierarchie_bt_coller_action_list(title=titre, ele_type=material_code, id_ele="0")
            return super().eventFilter(obj, event)

        if name_actual == f"Paste_{component_code}":
            self.hierarchie_bt_coller_action_list(title=titre, ele_type=component_code, id_ele="0")
            return super().eventFilter(obj, event)

        if name_actual == f"Paste_{link_code}":
            self.hierarchie_bt_coller_action_list(title=titre, ele_type=link_code, id_ele="0")
            return super().eventFilter(obj, event)

        if name_actual == f"Paste_{attribute_code}":
            self.hierarchie_bt_coller_action_list(title=titre, ele_type=attribute_code, id_ele="0")
            return super().eventFilter(obj, event)

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
