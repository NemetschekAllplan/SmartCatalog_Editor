#!/usr/bin/python3
# -*- coding: utf-8 -*
from attribute_error import AttributeUnknown
from attribute_lineedit_str import AttributeLineeditStr
from catalog_manage import *
from attribute_date import AttributeDate
from attribute_checkbox import AttributeCheckbox
from attribute_code import AttributeCode
from attribute_combobox import AttributeCombobox
from formula_attribute import AttributeFormula
from link_attribute import AttributeLink
from attribute_lineedit import AttributeLineedit
from attribute_name import AttributeName
from attribute_335 import Attribute335
from attribute_layer import AttributeLayer
from room_attribute import AttributeRoom
from attribute_filling import AttributeFilling
from attribute_title import AttributeTitle


class AttributesDetailLoader(QWidget):

    def __init__(self, asc):
        super().__init__()

        self.asc = asc

        self.catalog: CatalogDatas = self.asc.catalog
        self.hierarchy: Hierarchy = self.catalog.hierarchy

        self.allplan: AllplanDatas = self.asc.allplan

        self.liste_details: QListWidget = self.asc.ui.attributes_detail

    @staticmethod
    def a___________________creation_widgets______():
        pass

    def add_name(self, qs_value: QStandardItem, qs_selection_list=None):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setFlags(listwidgetitem.flags() & ~Qt.ItemIsSelectable)

        # ------------

        listwidgetitem.setData(user_data_type, type_nom)
        listwidgetitem.setData(user_data_number, attribut_default_obj.current)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeName(allplan=self.allplan,
                               qs_value=qs_value,
                               qs_selection_list=qs_selection_list)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        widget.attribute_changed_signal.connect(self.hierarchy.header_manage)

        widget.icon_changed_signal.connect(self.catalog.history_change_icon)

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.formatting_bt.installEventFilter(self)
        widget.ui.verification_bt.installEventFilter(self)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setSizeHint(widget.sizeHint())
        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_lien(self, parent_index: QModelIndex, current_row: int, link_model: QStandardItemModel):

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setFlags(listwidgetitem.flags() & ~Qt.ItemIsSelectable)

        # ------------

        listwidgetitem.setData(user_data_type, type_lien)
        listwidgetitem.setData(user_data_number, type_lien)

        # ---------------
        # Création widget
        # ---------------

        widget = AttributeLink(allplan=self.allplan, link_model=link_model)

        widget.ui.bt_afficher.installEventFilter(self)
        widget.ui.liste_composants.installEventFilter(self)

        widget.material_open.connect(self.catalog.goto_material)
        widget.component_open.connect(self.catalog.goto_component)

        # ---------------
        # Création mapper
        # ---------------

        qm_material_name = self.hierarchy.cat_model.index(current_row, col_cat_value, parent_index)

        if not qm_check(qm_material_name):
            material_name = self.tr("Lien")
        else:
            material_name = qm_material_name.data()

        qm_material_desc = self.hierarchy.cat_model.index(current_row, col_cat_desc, parent_index)

        if not qm_check(qm_material_desc):
            description = ""
        else:
            description = qm_material_desc.data()

        if description != "" and description != material_name:
            title = f"{material_name} - {description}"
        else:
            title = material_name

        widget.ui.nom_attr.setText(title)

        widget.material_name = material_name

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem.setData(user_data_number, "Lien")
        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

    def add_code(self, qs_value: MyQstandardItem, forbidden_names_list: list, attribute_obj: AttributeDatas,
                 material_linked=False):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setFlags(listwidgetitem.flags() & ~Qt.ItemIsSelectable)

        # ------------

        listwidgetitem.setData(user_data_type, type_code)
        listwidgetitem.setData(user_data_number, attribut_default_obj.current)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeCode(qs_value=qs_value,
                               material_linked=material_linked,
                               forbidden_names_list=forbidden_names_list,
                               attribute_obj=attribute_obj)

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.formatting_bt.installEventFilter(self)
        widget.ui.verification_bt.installEventFilter(self)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.code_changed_signal.connect(self.catalog.material_code_renamed)

        widget.attribute_defaul_signal.connect(self.asc.main_bar.catalogue_modifier_parametres)

        if material_linked:
            self.catalog.material_update_link_number(widget.ui.value_attrib.text())

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        widget.attribute_changed_signal.connect(self.hierarchy.header_manage)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setSizeHint(widget.sizeHint())
        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_lineedit(self, qs_value: MyQstandardItem, attribute_obj: AttributeDatas,
                     is_material=False):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_ligne)
        listwidgetitem.setData(user_data_number, attribute_obj.number)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeLineedit(allplan_version=self.allplan.version_allplan_current,
                                   qs_value=qs_value,
                                   attribute_obj=attribute_obj,
                                   is_material=is_material)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.lineedit_loading()

        # ------------------------
        # Creation signals
        # ------------------------

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        widget.ui.value_attrib.installEventFilter(self)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setSizeHint(widget.sizeHint())
        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_lineedit_str(self, qm_parent: QModelIndex, qs_value: MyQstandardItem, qs_desc,
                         attribute_obj: AttributeDatas, is_material=False):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_ligne)
        listwidgetitem.setData(user_data_number, attribute_obj.number)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeLineeditStr(allplan_version=self.allplan.version_allplan_current,
                                      qs_value=qs_value,
                                      qs_desc=qs_desc,
                                      attribute_obj=attribute_obj,
                                      is_material=is_material,
                                      listwidgetitem=listwidgetitem)

        # ------------------------
        # Creation mapper -- code
        # ------------------------

        mapper_parent = QDataWidgetMapper(self.asc)
        mapper_parent.setModel(self.hierarchy.cat_model)

        mapper_parent.addMapping(widget.code_title, col_cat_value, b"text")

        code_index: QModelIndex = qm_parent.parent()

        mapper_parent.setRootIndex(code_index)
        mapper_parent.setCurrentIndex(qm_parent.row())

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.lineedit_loading()

        self.asc.ui.splitter.splitterMoved.connect(widget.adjust_width)
        self.asc.ui_resized.connect(widget.adjust_width)

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.formatting_bt.installEventFilter(self)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.link_desc_changed_signal.connect(self.catalog.material_desc_changed)
        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_formula(self, qs_val: QStandardItem, attribute_obj: AttributeDatas):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_formule)
        listwidgetitem.setData(user_data_number, attribute_obj.number)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeFormula(asc=self.asc,
                                  qs_value=qs_val,
                                  attribute_obj=attribute_obj,
                                  listwidgetitem=listwidgetitem)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.chargement(search_error_active=self.hierarchy.cat_filter_1.filterRole() == user_formule_ok)

        self.asc.ui.splitter.splitterMoved.connect(widget.adjust_width)
        self.asc.ui_resized.connect(widget.adjust_width)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.viewport().installEventFilter(self)
        widget.ui.formula_verification_bt.installEventFilter(self)
        widget.ui.formula_editor_bt.installEventFilter(self)
        widget.ui.formula_color_bt.installEventFilter(self)
        widget.ui.formula_favorite_bt.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)
        widget.formula_changed.connect(self.catalog.select_first_formula_error)
        widget.formula_corrected.connect(self.catalog.formula_correct)

        widget.ui.value_attrib.size_change.connect(self.catalog.formula_size_change_signal.emit)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_combobox(self, qs_value: QStandardItem, qs_index: QStandardItem, attribute_obj: AttributeDatas):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_combo)
        listwidgetitem.setData(user_data_number, attribute_obj.number)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeCombobox(attribute_datas=attribute_obj,
                                   qs_value=qs_value,
                                   qs_index=qs_index)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.combo_loading()

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.lineEdit().installEventFilter(self)
        widget.ui.value_attrib.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setSizeHint(widget.sizeHint())
        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def ajouter_checkbox(self, qs_val: QStandardItem, attribute_obj: AttributeDatas):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_checkbox)
        listwidgetitem.setData(user_data_number, attribute_obj.number)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeCheckbox(qs_value=qs_val, attribute_obj=attribute_obj)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.checkbox_loading()

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_date(self, qs_value: QStandardItem, attribute_obj: AttributeDatas):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_date)
        listwidgetitem.setData(user_data_number, attribute_obj.number)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeDate(qs_value=qs_value, language=self.asc.langue, attribute_obj=attribute_obj)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.date_loading()

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.calendar_bt.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setSizeHint(widget.sizeHint())
        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_surface(self, qs_val: QStandardItem, attribute_obj: AttributeDatas):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_texture)
        listwidgetitem.setData(user_data_number, attribute_obj.number)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = Attribute335(asc=self.asc, qs_value=qs_val, attribute_obj=attribute_obj)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.browser_bt.installEventFilter(self)
        widget.ui.preview_bt.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setSizeHint(widget.sizeHint())
        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_layer(self, qs_val: QStandardItem, datas_index_row: dict):

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_layer)
        listwidgetitem.setData(user_data_number, attribute_val_default_layer_first)

        # ---------------
        # Création widget
        # ---------------

        widget = AttributeLayer(self.asc)

        widget.ui.value_141.lineEdit().installEventFilter(self)
        widget.ui.value_346.lineEdit().installEventFilter(self)
        widget.ui.value_345.lineEdit().installEventFilter(self)
        widget.ui.value_347.lineEdit().installEventFilter(self)

        widget.ui.value_349_stroke.installEventFilter(self)
        widget.ui.value_349_pen.installEventFilter(self)
        widget.ui.value_349_color.installEventFilter(self)

        widget.ui.lock_141.installEventFilter(self)

        # ---------------
        # Création mapper - Layer
        # ---------------

        number_str = "141"

        if number_str in datas_index_row:
            widget.qs_141_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_141_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.name_141.setText(attribute_obj.name)
                widget.ui.name_141.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - style de ligne
        # ---------------

        number_str = "349"

        if number_str in datas_index_row:
            widget.qs_349 = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.name_349.setText(attribute_obj.name)
                widget.ui.name_349.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - épaisseur
        # ---------------

        number_str = "346"

        if number_str in datas_index_row:
            widget.qs_346_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_346_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.name_346.setText(attribute_obj.name)
                widget.ui.name_346.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - trait
        # ---------------

        number_str = "345"

        if number_str in datas_index_row:
            widget.qs_345_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_345_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.name_345.setText(attribute_obj.name)
                widget.ui.name_345.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - couleur
        # ---------------

        number_str = "347"

        if number_str in datas_index_row:
            widget.qs_347_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_347_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.name_347.setText(attribute_obj.name)
                widget.ui.name_347.setToolTip(attribute_obj.tooltips)

        # ---------------
        # chargement
        # ---------------

        widget.chargement(row_index=self.liste_details.count())

        # ---------------
        # Définition signal
        # ---------------

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        widget.listwidgetitem = listwidgetitem

    def add_filling(self, qs_val: QStandardItem, datas_index_row: dict):

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_fill)
        listwidgetitem.setData(user_data_number, attribute_val_default_fill_first)

        # ---------------
        # Création widget
        # ---------------

        widget = AttributeFilling(self.asc)

        widget.ui.hachurage.lineEdit().installEventFilter(self)
        widget.ui.motif.lineEdit().installEventFilter(self)
        widget.ui.couleur.lineEdit().installEventFilter(self)
        widget.ui.surface.installEventFilter(self)
        widget.ui.style.lineEdit().installEventFilter(self)

        widget.ui.chb_hachurage.installEventFilter(self)
        widget.ui.chb_motif.installEventFilter(self)
        widget.ui.chb_style.installEventFilter(self)
        widget.ui.chb_couleur.installEventFilter(self)
        widget.ui.chb_surface.installEventFilter(self)

        widget.ui.browser_bt.installEventFilter(self)
        widget.ui.preview_bt.installEventFilter(self)

        # ---------------
        # Création mapper - 118
        # ---------------

        number_str = "118"

        if number_str in datas_index_row:
            widget.qs_118 = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.titre_infos.setText(attribute_obj.name)
                widget.ui.titre_infos.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - 111
        # ---------------

        number_str = "111"

        if number_str in datas_index_row:
            widget.qs_111_val = qs_val.child(datas_index_row[number_str], col_cat_value)
            widget.qs_111_ind = qs_val.child(datas_index_row[number_str], col_cat_index)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):

                widget.ui.titre_hachurage.setText(attribute_obj.name)
                widget.ui.titre_hachurage.setToolTip(attribute_obj.tooltips)

                widget.ui.titre_motif.setText(attribute_obj.name)
                widget.ui.titre_motif.setToolTip(attribute_obj.tooltips)

                widget.ui.titre_style.setText(attribute_obj.name)
                widget.ui.titre_style.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - 252
        # ---------------
        number_str = "252"

        if number_str in datas_index_row:
            widget.qs_252_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_252_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.titre_couleur_2.setText(attribute_obj.name)
                widget.titre_couleur_2.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - 336
        # ---------------
        number_str = "336"

        if number_str in datas_index_row:
            widget.qs_336 = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.titre_surface.setText(attribute_obj.name)
                widget.ui.titre_surface.setToolTip(attribute_obj.tooltips)

        # ---------------
        # chargement
        # ---------------
        widget.chargement(row_index=self.liste_details.count())

        # ---------------
        # Définition signal
        # ---------------

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        widget.listwidgetitem = listwidgetitem

    def add_room(self, qs_val: QStandardItem, datas_index_row: dict):

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ------------

        listwidgetitem.setData(user_data_type, type_room)
        listwidgetitem.setData(user_data_number, attribute_val_default_room_first)

        # ---------------
        # Création widget
        # ---------------

        widget = AttributeRoom(self.asc)

        widget.ui.valeur_fav.lineEdit().installEventFilter(self)
        widget.ui.valeur_231.lineEdit().installEventFilter(self)
        widget.ui.valeur_235.lineEdit().installEventFilter(self)
        widget.ui.valeur_232.lineEdit().installEventFilter(self)
        widget.ui.valeur_266.installEventFilter(self)
        widget.ui.valeur_233.lineEdit().installEventFilter(self)
        widget.ui.valeur_264.installEventFilter(self)

        widget.ui.formatting_bt.installEventFilter(self)
        widget.ui.formatting_2_bt.installEventFilter(self)
        widget.ui.bt_231.installEventFilter(self)
        widget.ui.bt_235.installEventFilter(self)
        widget.ui.bt_232.installEventFilter(self)
        widget.ui.bt_233.installEventFilter(self)

        # ---------------
        # Création mapper - Pourtour de salle
        # ---------------

        number_str = "231"

        if number_str in datas_index_row:
            widget.qs_231_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_231_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.titre_231.setText(attribute_obj.name)
                widget.ui.titre_231.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - type d'utilisation
        # ---------------

        number_str = "235"

        if number_str in datas_index_row:
            widget.qs_235_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_235_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.titre_235.setText(attribute_obj.name)
                widget.ui.titre_235.setToolTip(attribute_obj.tooltips)

            widget.qstandarditem_349 = qs_val.child(datas_index_row[number_str], col_cat_value)

        # ---------------
        # Création mapper - Type de surface
        # ---------------

        number_str = "232"

        if number_str in datas_index_row:
            widget.qs_232_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_232_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.titre_232.setText(attribute_obj.name)
                widget.ui.titre_232.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - facteur_din
        # ---------------

        number_str = "266"

        if number_str in datas_index_row:
            widget.qs_266 = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.titre_266.setText(attribute_obj.name)
                widget.ui.titre_266.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - Type surface habitable
        # ---------------

        number_str = "233"

        if number_str in datas_index_row:
            widget.qs_233_ind = qs_val.child(datas_index_row[number_str], col_cat_index)
            widget.qs_233_val = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.titre_233.setText(attribute_obj.name)
                widget.ui.titre_233.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Création mapper - facteur_surface_hab
        # ---------------

        number_str = "264"

        if number_str in datas_index_row:
            widget.qs_264 = qs_val.child(datas_index_row[number_str], col_cat_value)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if isinstance(attribute_obj, AttributeDatas):
                widget.ui.titre_264.setText(attribute_obj.name)
                widget.ui.titre_264.setToolTip(attribute_obj.tooltips)

        # ---------------
        # Définition variable
        # ---------------

        widget.chargement()

        # ---------------
        # Définition signal
        # ---------------

        widget.attribute_changed_signal.connect(self.catalog.history_modify_attribute)

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

    def add_unknown(self, attribute_obj: AttributeDatas, value: str):

        if not isinstance(value, str):
            value = ""

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        # ---------------

        listwidgetitem.setData(user_data_type, type_unknown)
        listwidgetitem.setData(user_data_number, attribute_obj.number)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeUnknown(attribute_obj=attribute_obj, value=value)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.installEventFilter(self)

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem.setSizeHint(widget.sizeHint())
        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ---------------

    def add_title(self, title: str):

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setFlags(listwidgetitem.flags() & ~Qt.ItemIsSelectable)

        # ------------

        listwidgetitem.setData(user_data_type, type_title)
        listwidgetitem.setData(user_data_number, type_title)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeTitle(self.asc, title=title)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.attribute_add_bt.clicked.connect(self.asc.action_bar.attributs_ajouter)
        widget.ui.attribute_add_bt.customContextMenuRequested.connect(self.asc.action_bar.attributs_ajouter)

        # ---------------

        widget.ui.order_19.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=0,
                                                                 attributes_order_col=0,
                                                                 attributes_order_custom=False))

        widget.ui.order_91.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=1,
                                                                 attributes_order_col=0,
                                                                 attributes_order_custom=False))

        widget.ui.order_az.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=0,
                                                                 attributes_order_col=1,
                                                                 attributes_order_custom=False))

        widget.ui.order_za.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=1,
                                                                 attributes_order_col=1,
                                                                 attributes_order_custom=False))

        widget.ui.order_custom.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=0,
                                                                 attributes_order_col=0,
                                                                 attributes_order_custom=True))

        widget.ui.order_setting.clicked.connect(self.asc.action_bar.attributes_order_custom_clicked)

        # ---------------
        # Création listwidgetitem
        # ---------------

        listwidgetitem.setSizeHint(widget.sizeHint())
        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent):

        if event.type() != event.MouseButtonPress:
            return super().eventFilter(obj, event)

        if not isinstance(obj, QWidget):
            self.asc.attribut_clic()
            return super().eventFilter(obj, event)

        parent_actuel = obj.parent()

        if parent_actuel is None:
            self.asc.attribut_clic()
            return super().eventFilter(obj, event)

        if isinstance(parent_actuel, QComboBox) or isinstance(parent_actuel, QPlainTextEdit):

            parent_actuel = parent_actuel.parent()

            if parent_actuel is None:
                self.asc.attribut_clic()
                return super().eventFilter(obj, event)

        nb_details = self.liste_details.count()

        if nb_details < 2:
            self.asc.attribut_clic()
            return super().eventFilter(obj, event)

        for index_row in range(1, nb_details):

            qm = self.liste_details.model().index(index_row, 0)

            if qm_check(qm):
                self.asc.attribut_clic()
                return super().eventFilter(obj, event)

            obj_actuel = self.liste_details.indexWidget(self.liste_details.model().index(index_row, 0))

            if obj_actuel != parent_actuel:
                continue

            self.liste_details.setCurrentRow(index_row)

            self.asc.attribut_clic()

            break

        self.asc.attribut_clic()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
