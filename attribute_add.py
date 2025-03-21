#!/usr/bin/python3
# -*- coding: utf-8 -*


from allplan_manage import *
from tools import afficher_message as msg
from tools import favorites_import_verification, copy_to_clipboard, convert_list_attribute_number, browser_file
from tools import move_window_tool, load_csv, get_look_tableview, qm_check, settings_save, MyContextMenu
from ui_attribute_add import Ui_AttributeAdd


# todo si selection d'un attribut d'une catégorie. après fermeture, l'attribut n'est pas repris.


class AttributesWidget(QWidget):
    add_attributs = pyqtSignal(list)
    add_options = pyqtSignal(list)

    formula_creator_signal = pyqtSignal(str)
    finishing_signal = pyqtSignal(str)
    replace_signal = pyqtSignal(str)
    search_signal = pyqtSignal(str)

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_AttributeAdd()
        self.ui.setupUi(self)

        # ---------------------------------------
        # LOADING PARENT
        # ---------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.allplan: AllplanDatas = self.asc.allplan

        # ---------------------------------------
        # LOADING VARAIBLES
        # ---------------------------------------

        self.favorite_material_code = self.tr("Favoris Ouvrage")
        self.favorite_material_changed = False

        self.favorite_component_code = self.tr("Favoris Composant")
        self.favorite_component_changed = False

        self.favorite_formula_code = self.tr("Favoris Formule")
        self.favorite_formula_changed = False

        self.numbers_current_list = list()

        self.current_mod = ""
        self.reload_autocompletion = False

        # ---------------------------------------
        # FILTER GROUPS
        # ---------------------------------------

        self.group_filter = QSortFilterProxyModel()
        self.group_filter.setSourceModel(self.allplan.attribute_model)
        self.group_filter.setFilterKeyColumn(col_attr_group)
        self.group_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # ---------------------------------------
        # FILTER SEARCH
        # ---------------------------------------

        self.search_filter = NumericSortProxyModel(column_number=col_attr_number)
        self.search_filter.setSourceModel(self.group_filter)
        self.search_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.search_filter.setFilterKeyColumn(col_attr_name)

        self.search_filter.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.search_filter.setSortLocaleAware(True)

        # ---------------------------------------
        # GROUPS LIST
        # ---------------------------------------

        self.ui.group_list.currentItemChanged.connect(self.group_changed)

        self.ui.group_list.customContextMenuRequested.connect(self.group_menu_show)

        get_look_tableview(self.ui.group_list)

        # ---------------------------------------
        # ATTRIBUTES LISTVIEW
        # ---------------------------------------

        self.ui.attributes_list.setModel(self.search_filter)

        self.ui.attributes_list.customContextMenuRequested.connect(self.attribute_menu_show)
        self.ui.attributes_list.doubleClicked.connect(self.attributes_save)
        self.ui.attributes_list.selectionModel().selectionChanged.connect(self.attribute_buttons_manage)

        get_look_tableview(self.ui.attributes_list)

        # ---------------------------------------
        # SIGNAl - FAVORITES
        # ---------------------------------------

        self.ui.material_bt.clicked.connect(self.favorite_material_manage)

        self.ui.component_bt.clicked.connect(self.favorite_component_manage)

        self.ui.formula_bt.clicked.connect(self.favorite_formula_manage)

        self.ui.import_bt.clicked.connect(self.favorite_import)

        self.ui.export_bt.clicked.connect(self.favorite_export)

        # ---------------------------------------
        # SIGNAUX - search
        # ---------------------------------------

        self.ui.search_bar.textChanged.connect(self.search_action)

        self.ui.search_clear_bt.clicked.connect(self.ui.search_bar.clear)

        # ---------------------------------------
        # SIGNALS - OK / QUIT
        # ---------------------------------------

        self.ui.ok.clicked.connect(self.attributes_save)
        self.ui.quit.clicked.connect(self.close)

        # ---------------------------------------
        # SETTINGS
        # ---------------------------------------

        attribute_setting = settings_read(file_name=attribute_setting_file)

        width = attribute_setting.get("width", attribute_setting_datas.get("width", 800))

        if not isinstance(width, int):
            width = attribute_setting_datas.get("width", 800)

        height = attribute_setting.get("height", attribute_setting_datas.get("height", 600))

        if not isinstance(height, int):
            height = attribute_setting_datas.get("height", 600)

        self.resize(width, height)

        # ---------------------------------------

        ismaximized_on = attribute_setting.get("ismaximized_on", attribute_setting_datas.get("ismaximized_on", False))

        if not isinstance(ismaximized_on, bool):
            self.ismaximized_on = attribute_setting_datas.get("ismaximized_on", False)
        else:
            self.ismaximized_on = ismaximized_on

        # ---------------------------------------

        group_index = attribute_setting.get("group_index", attribute_setting_datas.get("group_index", 0))

        if not isinstance(group_index, int):
            group_index = attribute_setting_datas.get("group_index", 0)

        self.ui.group_list.setCurrentRow(group_index)

        header = self.ui.attributes_list.horizontalHeader()

        if header is not None:

            order = attribute_setting.get("order", attribute_setting_datas.get("order", 0))

            if not isinstance(order, int):
                order = attribute_setting_datas.get("order", 0)

            order_col = attribute_setting.get("order_col", attribute_setting_datas.get("order_col", 0))

            if not isinstance(order_col, int):
                order_col = attribute_setting_datas.get("order_col", 0)

            header.setSortIndicator(order_col, order)
            self.ui.attributes_list.sortByColumn(order_col, order)

            header.sortIndicatorChanged.connect(self.attribute_sort_indicator_changed)

    def attribute_show(self, current_mod: str, current_widget: QWidget, attributes_list=None):

        self.current_mod = current_mod

        if attributes_list is None:
            self.numbers_current_list = list()
        else:
            self.numbers_current_list = attributes_list

        self.attribute_header_manage()

        if self.current_mod == "Formula":
            self.setWindowTitle(self.tr("Parcourir les attributs"))
            self.ui.attributes_list.setSelectionMode(QAbstractItemView.SingleSelection)

        elif self.current_mod == "Finishing":
            self.setWindowTitle(self.tr("Parcourir les attributs"))
            self.ui.attributes_list.setSelectionMode(QAbstractItemView.SingleSelection)

        elif self.current_mod == "Model" or self.current_mod == "Order":
            self.setWindowTitle(self.tr("Ajouter attribut"))
            self.ui.attributes_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        elif self.current_mod == "Search":
            self.setWindowTitle(self.tr("Parcourir les attributs"))
            self.ui.attributes_list.setSelectionMode(QAbstractItemView.SingleSelection)

        elif self.current_mod == "Replace":
            self.setWindowTitle(self.tr("Parcourir les attributs"))
            self.ui.attributes_list.setSelectionMode(QAbstractItemView.SingleSelection)

        else:

            self.setWindowTitle(self.tr("Ajouter attribut"))
            self.ui.attributes_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.attribute_buttons_manage()

        group_current_row = self.ui.group_list.currentRow()

        if group_current_row < 0:
            self.ui.group_list.setCurrentRow(0)

        self.group_changed(qlistwidgetitem=self.ui.group_list.currentItem())

        qm_attribute = self.ui.attributes_list.currentIndex()

        if not qm_check(qm_attribute):
            self.ui.attributes_list.setCurrentIndex(self.ui.attributes_list.model().index(0, 0))

        self.ui.search_bar.setFocus()

        move_window_tool(widget_parent=current_widget, widget_current=self)

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

    @staticmethod
    def a___________________group_______________():
        pass

    def get_group_code_by_group_name(self, group_name: str):

        for code, name in self.allplan.group_list.items():
            if name == group_name:
                return code

        print(f"widget_ajouter_attribut -- get_group_name_by_group_code -- {group_name} not found ")
        return ""

    def group_changed(self, qlistwidgetitem: QListWidgetItem):

        if not isinstance(qlistwidgetitem, QListWidgetItem):
            print("attribute_add -- group_changed -- not isinstance(qlistwidgetitem, QListWidgetItem)")
            return

        group_name = qlistwidgetitem.text()

        if (group_name == self.tr("Tous les attributs Allplan") or
                group_name == self.tr("Favoris Ouvrage") or
                group_name == self.tr("Favoris Composant") or
                group_name == self.tr("Favoris Formule")):
            self.select_and_scroll(self.group_filter, group_name)

            return

        group_code = self.get_group_code_by_group_name(group_name=group_name)

        self.select_and_scroll(self.group_filter, group_code)

    def group_menu_show(self, point: QPoint):

        group_name = self.get_group_name_selected_if_favorite()

        if group_name == "":
            return

        group_menu = MyContextMenu(short_link=help_attribute_fav)
        group_menu.help_request.connect(self.asc.help_request)

        self.menu_add_import_section(current_menu=group_menu, attribute_count=self.search_filter.rowCount())

        group_menu.exec_(self.ui.group_list.mapToGlobal(point))

    def get_group_name_selected_if_favorite(self) -> str:

        group_item = self.ui.group_list.currentItem()

        if group_item is None:
            return ""

        group_txt = group_item.text()

        if group_txt not in [self.tr("Favoris Ouvrage"), self.tr("Favoris Composant"), self.tr("Favoris Formule")]:
            return ""

        return group_txt

    @staticmethod
    def a___________________attribute_______________():
        pass

    def attribute_buttons_manage(self):

        is_favorite = self.get_group_name_selected_if_favorite()

        self.ui.import_bt.setEnabled(is_favorite != "")
        self.ui.export_bt.setEnabled(is_favorite != "")

        if is_favorite == "":
            select_txt = self.tr("Sélectionner un favori")

            self.ui.import_bt.setEnabled(False)
            self.ui.import_bt.setToolTip(select_txt)

            self.ui.export_bt.setEnabled(False)
            self.ui.export_bt.setToolTip(select_txt)

        else:

            import_msg = self.tr("Importer favoris")
            import_msg += f" : {is_favorite}"

            self.ui.import_bt.setEnabled(True)
            self.ui.import_bt.setToolTip(import_msg)

            if self.search_filter.rowCount() == 0:

                self.ui.export_bt.setEnabled(False)
                self.ui.export_bt.setToolTip("")

            else:
                export_msg = self.tr("Exporter favoris")
                export_msg += f" :  {is_favorite}"

                self.ui.export_bt.setEnabled(True)
                self.ui.export_bt.setToolTip(export_msg)

        qm_selection_list: list = self.ui.attributes_list.selectionModel().selectedRows()
        enable = len(qm_selection_list) > 0

        self.ui.ok.setEnabled(enable)
        self.ui.material_bt.setEnabled(enable)
        self.ui.component_bt.setEnabled(enable)
        self.ui.formula_bt.setEnabled(enable)

        if not enable:
            material_bt = component_bt = formula_bt = False
        else:
            material_bt, component_bt, formula_bt = self.get_favorite_possibilities()

        self.ui.material_bt.setChecked(material_bt)
        self.ui.component_bt.setChecked(component_bt)
        self.ui.formula_bt.setChecked(formula_bt)

        if material_bt:
            self.ui.material_bt.setToolTip(self.tr("Supprimer des favoris Ouvrage"))
        else:
            self.ui.material_bt.setToolTip(self.tr("Ajouter aux favoris Ouvrage"))

        if component_bt:
            self.ui.component_bt.setToolTip(self.tr("Supprimer des favoris Composant"))
        else:
            self.ui.component_bt.setToolTip(self.tr("Ajouter aux favoris Composant"))

        if formula_bt:
            self.ui.formula_bt.setToolTip(self.tr("Supprimer des favoris Formule"))
        else:
            self.ui.formula_bt.setToolTip(self.tr("Ajouter aux favoris Formule"))

    def attribute_menu_show(self, point):

        attribute_menu = MyContextMenu()  # OK
        attribute_menu.help_request.connect(self.asc.help_request)

        qm_selection_list: list = self.ui.attributes_list.selectionModel().selectedRows()

        qm_selection_count = len(qm_selection_list)

        attribute_count = self.search_filter.rowCount()

        if qm_selection_count == 0:
            # ---------------------------------------
            # IMPORT/EXPORT
            # ---------------------------------------

            self.menu_add_import_section(current_menu=attribute_menu, attribute_count=attribute_count)

            attribute_menu.exec_(self.ui.attributes_list.mapToGlobal(point))
            return

        attribute_menu.add_title(title=self.tr("Attribut"))

        # ---------------------------------------
        # ADD
        # ---------------------------------------

        attribute_menu.add_action(qicon=get_icon(attribute_add_icon),
                                  title=self.tr("Ajouter attribut"),
                                  action=self.attributes_save,
                                  short_link=help_attribute_new)

        if qm_selection_count == 1:

            qm: QModelIndex = qm_selection_list[0]

            if not qm_check(qm):
                return

            row_index = qm.row()

            qm_number = self.search_filter.index(row_index, col_attr_number)
            qm_name = self.search_filter.index(row_index, col_attr_name)

            if not qm_check(qm_number) or not qm_check(qm_name):
                return

            name = qm_name.data()
            number = qm_number.data()

            if number is None or name is None:
                return

            attribute_menu.addSeparator()

            attribute_menu.add_action(qicon=get_icon(text_copy_icon),
                                      title=self.tr("Copier le numéro dans le presse-papier"),
                                      action=lambda: copy_to_clipboard(number))

            attribute_menu.add_action(qicon=get_icon(text_copy_icon),
                                      title=self.tr("Copier le nom dans le presse-papier"),
                                      action=lambda: copy_to_clipboard(name))

        # ---------------------------------------
        # FAVORITE
        # ---------------------------------------

        attribute_menu.add_title(title=self.tr("Favoris"))

        material_bt, component_bt, formula_bt = self.get_favorite_possibilities()

        if material_bt:

            attribute_menu.add_action(qicon=get_icon(delete_icon),
                                      title=self.tr("Supprimer des favoris Ouvrage"),
                                      action=self.favorite_material_change_status,
                                      short_link=help_attribute_fav)

        else:

            attribute_menu.add_action(qicon=get_icon(material_icon),
                                      title=self.tr("Ajouter aux favoris Ouvrage"),
                                      action=self.favorite_material_change_status,
                                      short_link=help_attribute_fav)

        # ---------------------------------------
        # AJOUT - FAVORIS POSITION
        # ---------------------------------------

        if component_bt:

            attribute_menu.add_action(qicon=get_icon(delete_icon),
                                      title=self.tr("Supprimer des favoris Composant"),
                                      action=self.favorite_component_change_status,
                                      short_link=help_attribute_fav)

        else:

            attribute_menu.add_action(qicon=get_icon(component_icon),
                                      title=self.tr("Ajouter aux favoris Composant"),
                                      action=self.favorite_component_change_status,
                                      short_link=help_attribute_fav)

        # ---------------------------------------
        # AJOUT - FAVORIS FORMULE
        # ---------------------------------------

        if formula_bt:
            attribute_menu.add_action(qicon=get_icon(delete_icon),
                                      title=self.tr("Supprimer des favoris Formule"),
                                      action=self.favorite_formula_change_status,
                                      short_link=help_attribute_fav)

        else:

            attribute_menu.add_action(qicon=get_icon(formula_icon),
                                      title=self.tr("Ajouter aux favoris Formule"),
                                      action=self.favorite_formula_change_status,
                                      short_link=help_attribute_fav)

        # ---------------------------------------
        # IMPORT/EXPORT
        # ---------------------------------------

        self.menu_add_import_section(current_menu=attribute_menu, attribute_count=attribute_count)

        attribute_menu.exec_(self.ui.attributes_list.mapToGlobal(point))

    def attribute_header_manage(self):

        self.ui.attributes_list.setColumnHidden(col_attr_datatype, True)
        self.ui.attributes_list.setColumnHidden(col_attr_group, True)

        header = self.ui.attributes_list.horizontalHeader()

        if header is None:
            return

        if header.height() != 24:
            header.setFixedHeight(24)

        if self.allplan.attribute_model.rowCount() == 0:
            return

        header.setDefaultAlignment(Qt.AlignHCenter)

        header.setSectionResizeMode(col_attr_number, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(col_attr_name, QHeaderView.Stretch)
        # header.setSectionResizeMode(col_attr_group, QHeaderView.Stretch)

    def attribute_sort_indicator_changed(self):

        qm_filter_current = self.ui.attributes_list.currentIndex()

        if not qm_check(qm_filter_current):
            return

        self.ui.attributes_list.scrollTo(qm_filter_current, QAbstractItemView.PositionAtCenter)

    def attribute_map_to_model(self, qm: QModelIndex):

        if not qm_check(qm):
            print("widget_ajouter_attribut -- attribut_map_to_model -- qmodelindex is None")
            return None

        model = qm.model()

        if model is None:
            return None

        if model == self.allplan.attribute_model:
            print("widget_ajouter_attribut -- attribut_map_to_model -- model_actuel")
            return qm

        if model == self.group_filter:
            qm_model = self.group_filter.mapToSource(qm)
            return qm_model

        if model == self.search_filter:
            qm_filter1 = self.search_filter.mapToSource(qm)
            qm_model = self.group_filter.mapToSource(qm_filter1)
            return qm_model

        print("widget_ajouter_attribut -- attribut_map_to_model -- error")
        return None

    def get_number_and_name_by_qm(self, qm_filter):

        qm: QModelIndex = self.attribute_map_to_model(qm_filter)

        if not qm_check(qm):
            print("widget_ajouter_attribut -- recherche_numero_nom_by_qmodelindex -- qmodelindex is None")
            return None, None

        current_row = qm.row()

        qm_number = self.allplan.attribute_model.index(current_row, col_attr_number)

        if not qm_check(qm_number):
            print("widget_ajouter_attribut -- recherche_numero_nom_by_qmodelindex -- qmodelindex_numero not valid")
            return None, None

        number = qm_number.data()

        qm_name = self.allplan.attribute_model.index(current_row, col_attr_name)

        if not qm_check(qm_name):
            print("widget_ajouter_attribut -- recherche_numero_nom_by_qmodelindex -- qmodelindex_nom not valid")
            return None, None

        name = qm_name.data()

        return number, name

    @staticmethod
    def a___________________menu_______________():
        pass

    def menu_add_import_section(self, current_menu: MyContextMenu, attribute_count: int):

        is_favorite = self.get_group_name_selected_if_favorite()

        if is_favorite == "":
            return

        import_title = self.tr("Import")
        import_msg = self.tr("Importer favoris")
        import_msg += f" : {is_favorite}"

        if attribute_count == 0:
            current_menu.add_title(title=import_title)

            current_menu.add_action(qicon=get_icon(material_icon),
                                    title=import_msg,
                                    action=self.favorite_import,
                                    short_link=help_attribute_fav)

            return

        export_title = self.tr("Export")

        export_msg = self.tr("Exporter favoris")
        export_msg += f" :  {is_favorite}"

        current_menu.add_title(title=f"{import_title} / {export_title}")

        current_menu.add_action(qicon=get_icon(material_icon),
                                title=import_msg,
                                action=self.favorite_import,
                                short_link=help_attribute_fav)

        current_menu.add_action(qicon=get_icon(favorite_save_icon),
                                title=export_msg,
                                action=self.favorite_export,
                                short_link=help_attribute_fav)

    @staticmethod
    def a___________________favorites_______________():
        pass

    def favorite_manage(self, favorite_type: str, delete=False):

        qm_selection_list: list = self.ui.attributes_list.selectionModel().selectedRows()

        if len(qm_selection_list) == 0:
            return

        qm_selection_list.sort()

        if favorite_type == component_code:
            favorite_list = self.allplan.component_favorite_list
            group_name = self.favorite_component_code

        elif favorite_type == "Formula":
            favorite_list = self.allplan.formula_favorite_list
            group_name = self.favorite_formula_code
            self.reload_autocompletion = True

        elif favorite_type == material_code:
            favorite_list = self.allplan.material_favorite_list
            group_name = self.tr("Favoris Ouvrage")

        else:
            print("WidgetAjouterAttribut -- favoris_gestion -- Mauvais type_favoris_actuel")
            return

        number_list = list()

        for qm in reversed(qm_selection_list):

            qm: QModelIndex

            if not qm_check(qm):
                print("WidgetAjouterAttribut -- favoris_gestion -- not verification_qmodelindex(qmodelindex) !")
                continue

            row_index = qm.row()

            qm_number: QModelIndex = self.search_filter.index(row_index, col_attr_number)

            if not qm_check(qm_number):
                print("WidgetAjouterAttribut -- favoris_gestion -- not verification_qmodelindex(qm_numero) !")
                continue

            number: str = qm_number.data()

            if delete and number not in favorite_list:
                continue

            if not delete and number in favorite_list:
                continue

            number_list.append(number)

        self.favorite_modify_action(numbers_list=number_list, group_name=group_name, delete=delete)

        if delete:

            qm_first: QModelIndex = qm_selection_list[0]

            if qm_first is None:
                return

            filter_row_count = self.search_filter.rowCount() - 1

            if qm_first.row() > filter_row_count:
                qm_new = self.search_filter.index(filter_row_count, col_attr_number)
            else:
                qm_new = self.search_filter.index(qm_first.row(), col_attr_number)

            if qm_check(qm_new):
                self.ui.attributes_list.setCurrentIndex(qm_new)
                self.ui.attributes_list.scrollTo(qm_new, QAbstractItemView.PositionAtTop)
                self.attribute_header_manage()
                self.attribute_buttons_manage()

    def favorite_material_change_status(self):
        if not self.ui.material_bt.isEnabled():
            return

        self.ui.material_bt.setChecked(not self.ui.material_bt.isChecked())
        self.favorite_material_manage()

    def favorite_material_manage(self):
        status = not self.ui.material_bt.isChecked()
        self.favorite_manage(favorite_type=material_code, delete=status)

    def favorite_component_change_status(self):
        if not self.ui.component_bt.isEnabled():
            return

        self.ui.component_bt.setChecked(not self.ui.component_bt.isChecked())
        self.favorite_component_manage()

    def favorite_component_manage(self):
        status = not self.ui.component_bt.isChecked()
        self.favorite_manage(favorite_type=component_code, delete=status)

    def favorite_formula_change_status(self):
        if not self.ui.formula_bt.isEnabled():
            return

        self.ui.formula_bt.setChecked(not self.ui.formula_bt.isChecked())
        self.favorite_formula_manage()

    def favorite_formula_manage(self):
        status = not self.ui.formula_bt.isChecked()
        self.favorite_manage(favorite_type="Formula", delete=status)

    def favorite_modify_action(self, numbers_list: list, group_name: str, delete=False):

        search_start = self.allplan.attribute_model.index(0, col_attr_number)

        for number in numbers_list:

            if not isinstance(number, str):
                print(f"attribute_add -- favorite_import_action -- not isinstance(number, str)")
                return

            search_number: list = self.allplan.attribute_model.match(search_start, Qt.DisplayRole, number, 1,
                                                                     Qt.MatchExactly)

            if len(search_number) != 1:
                print(f"attribute_add -- favorite_import_action -- len(search_number) != 1")
                return

            qm_number = search_number[0]

            if not qm_check(qm_number):
                print(f"attribute_add -- favorite_import_action -- not qm_check(qm)")
                return

            row_index: int = qm_number.row()

            group_index: QModelIndex = self.allplan.attribute_model.index(row_index, col_attr_group)

            if not qm_check(group_index):
                print(f"attribute_add -- favorite_import_action -- not qm_check(group_index)")
                return

            group: str = group_index.data()

            if not delete:

                if group_name in group:
                    print(f"attribute_add -- favorite_import_action -- group_name in group")
                    continue

                group += f", {group_name}"

            else:

                if group_name not in group:
                    print(f"attribute_add -- favorite_import_action -- group_name not in group")
                    continue

                group = group.replace(f", {group_name}", "")

            self.allplan.attribute_model.setData(group_index, group)

            # ---------------------------------------
            # FAVORIS OUVRAGE
            # ---------------------------------------

            if group_name == self.favorite_material_code:

                self.favorite_material_changed = True

                if not delete:

                    if number in self.allplan.material_favorite_list:
                        print(f"attribute_add -- favorite_import_action -- number in material_favorite_list")
                        continue

                    self.allplan.material_favorite_list.append(number)
                    continue

                if number not in self.allplan.material_favorite_list:
                    print(f"attribute_add -- favorite_import_action -- number not in material_favorite_list")
                    continue

                self.allplan.material_favorite_list.remove(number)
                continue

            # ---------------------------------------
            # FAVORIS COMPOSANT
            # ---------------------------------------

            if group_name == self.favorite_component_code:

                self.favorite_component_changed = True

                if not delete:

                    if number in self.allplan.component_favorite_list:
                        print(f"attribute_add -- favorite_import_action -- number in component_favorite_list")
                        continue

                    self.allplan.component_favorite_list.append(number)
                    continue

                if number not in self.allplan.component_favorite_list:
                    print(f"attribute_add -- favorite_import_action -- number not in component_favorite_list")
                    continue

                self.allplan.component_favorite_list.remove(number)
                continue

            # ---------------------------------------
            # FAVORIS FORMULE
            # ---------------------------------------

            if group_name == self.favorite_formula_code:

                self.favorite_formula_changed = True

                if not delete:

                    if number in self.allplan.formula_favorite_list:
                        print(f"attribute_add -- favorite_import_action -- number in formula_favorite_list")
                        continue

                    self.allplan.formula_favorite_list.append(number)
                    continue

                if number not in self.allplan.formula_favorite_list:
                    print(f"attribute_add -- favorite_import_action -- number not in formula_favorite_list")
                    continue

                self.allplan.formula_favorite_list.remove(number)

    def get_favorite_possibilities(self) -> tuple:

        qm_selection_list: list = self.ui.attributes_list.selectionModel().selectedRows()

        material_add = 0
        material_del = 0

        component_add = 0
        component_del = 0

        formula_add = 0
        formula_del = 0

        for qm_group in qm_selection_list:

            qm_group: QModelIndex

            if qm_group is None:
                continue

            row_index = qm_group.row()

            qm_group = self.search_filter.index(row_index, col_attr_group)

            if not qm_check(qm_group):
                continue

            group = qm_group.data()

            if self.favorite_material_code in group:
                material_del += 1
            else:
                material_add += 1

            if self.favorite_component_code in group:
                component_del += 1
            else:
                component_add += 1

            if self.favorite_formula_code in group:
                formula_del += 1
            else:
                formula_add += 1

        material_bt = material_del > material_add
        component_bt = component_del > component_add
        formula_bt = formula_del > formula_add

        return material_bt, component_bt, formula_bt

    @staticmethod
    def a___________________favorites_import_______________():
        pass

    def favorite_import(self):

        group_name = self.get_group_name_selected_if_favorite()

        if group_name == "":
            return

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [asc_export_path,
                              self.allplan.allplan_paths.std_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.usr_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[attribute_setting_file, "path_import"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={self.tr("Fichier CSV"): [".csv"]},
                                 current_path="",
                                 default_path=asc_export_path,
                                 use_setting_first=True)

        if file_path == "":
            return

        self.favorite_import_file_loading(file_path=file_path, group_name=group_name)

    def favorite_import_file_loading(self, file_path: str, group_name: str):

        import_number_list = load_csv(file_path)

        if len(import_number_list) == 0:
            msg(titre=self.windowTitle(),
                message=self.tr("Aucun élément n'a été trouvé"),
                icone_avertissement=True)
            return

        import_number_list = convert_list_attribute_number(number_list=import_number_list)

        number_list = self.get_model_to_list(favorite_name=group_name)

        if len(number_list) == 0:

            self.favorite_modify_action(numbers_list=sorted(import_number_list, key=int),
                                        group_name=group_name,
                                        delete=False)
        else:

            try:
                number_set = set(number_list)

                import_number_set = set(import_number_list)

                number_add_set = import_number_set - number_set
                number_delete_set = number_set - import_number_set

                self.favorite_modify_action(numbers_list=sorted(list(number_add_set), key=int),
                                            group_name=group_name,
                                            delete=False)

                self.favorite_modify_action(numbers_list=sorted(list(number_delete_set), key=int),
                                            group_name=group_name,
                                            delete=True)

            except Exception:
                return

        msg(titre=self.windowTitle(),
            message=self.tr("L'import s'est correctement déroulé!"),
            icone_valide=True)

    @staticmethod
    def a___________________favorites_export_______________():
        pass

    def favorite_export(self):

        group_name = self.get_group_name_selected_if_favorite()

        if group_name == "":
            return

        number_list = self.get_model_to_list(group_name)

        if len(number_list) == 0:
            return

        file_txt = self.tr("Fichier")

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [asc_export_path,
                              self.allplan.allplan_paths.std_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.usr_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[attribute_setting_file, "path_export"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{file_txt} CSV": [".csv"]},
                                 current_path=asc_export_path,
                                 default_path="",
                                 file_name=group_name,
                                 use_setting_first=True,
                                 use_save=True)

        if file_path == "":
            return

        if self.favorite_export_action(number_list=number_list, file_path=file_path):
            msg(titre=self.windowTitle(),
                message=self.tr("L'export s'est correctement déroulé!"),
                icone_valide=True)

    def get_model_to_list(self, favorite_name: str):

        number_list = list()

        search_start = self.allplan.attribute_model.index(0, col_attr_group)

        search_favorite: list = self.allplan.attribute_model.match(search_start, Qt.DisplayRole, favorite_name, -1,
                                                                   Qt.MatchContains)

        for qm in search_favorite:

            qm: QModelIndex
            row_index = qm.row()

            qs_number = self.allplan.attribute_model.index(row_index, col_attr_number)

            if not qm_check(qs_number):
                continue

            number_list.append(qs_number.data())

        return number_list

    def favorite_export_action(self, number_list: list, file_path: str):

        try:
            with open(file_path, "w") as file:
                file.writelines(", ".join(number_list))

        except OSError as error:

            msg(titre=self.windowTitle(),
                message=self.tr("Une erreur est survenue."),
                details=error,
                icone_critique=True)

            return False
        return True

    @staticmethod
    def a___________________search_______________():
        pass

    def search_action(self):

        current_text = self.ui.search_bar.text()

        if current_text == "":
            self.ui.search_bar.setStyleSheet("QLineEdit{border: 1px solid #8f8f91; "
                                             "border-top-left-radius: 5px; "
                                             "border-bottom-left-radius: 5px; "
                                             "padding-left: 5px; }")

            font = self.ui.search_bar.font()
            font.setBold(False)
            self.ui.search_bar.setFont(font)

        else:
            self.ui.search_bar.setStyleSheet("QLineEdit{border: 2px solid orange; "
                                             "border-top-left-radius: 5px; "
                                             "border-bottom-left-radius: 5px; "
                                             "padding-left: 5px; }")

            font = self.ui.search_bar.font()
            font.setBold(True)
            self.ui.search_bar.setFont(font)

            try:
                int(current_text)
                self.search_filter.setFilterKeyColumn(col_attr_number)
            except Exception:
                self.search_filter.setFilterKeyColumn(col_attr_name)

        self.select_and_scroll(self.search_filter, current_text)

    def select_and_scroll(self, filter_current: QSortFilterProxyModel, text_current: str):

        filter_current.setFilterRegExp(text_current)

        self.ui.attributes_list.updateGeometries()

        qm_selection_list: list = self.ui.attributes_list.selectionModel().selectedRows()
        selection_count = len(qm_selection_list)

        qm_first = self.ui.attributes_list.model().index(0, 0)

        if selection_count == 0:
            self.ui.attributes_list.setCurrentIndex(qm_first)
            self.ui.attributes_list.scrollTo(qm_first, QAbstractItemView.PositionAtTop)
            self.attribute_header_manage()
            self.attribute_buttons_manage()
            return

        qm_selection_list.sort()

        qm: QModelIndex = qm_selection_list[0]

        if qm_check(qm):
            self.ui.attributes_list.scrollTo(qm, QAbstractItemView.PositionAtTop)
            self.attribute_header_manage()
            self.attribute_buttons_manage()
            return

        self.ui.attributes_list.setCurrentIndex(qm_first)
        self.ui.attributes_list.scrollTo(qm_first, QAbstractItemView.PositionAtTop)
        self.attribute_header_manage()
        self.attribute_buttons_manage()

    @staticmethod
    def a___________________save_______________():
        pass

    def attributes_save(self):

        self.close()

        if self.current_mod in ["Formula", "Finishing", "Replace", "Search"]:

            qm_filter = self.ui.attributes_list.currentIndex()

            number, name = self.get_number_and_name_by_qm(qm_filter)

            if number is None:
                print("widget_ajouter_attribut -- attributs_ajouter -- numero is None")
                return

            if name is None:
                print("widget_ajouter_attribut -- attributs_ajouter -- nom is None")
                return

            if self.current_mod == "Formula":
                self.formula_creator_signal.emit(f"@{number}@")
                return

            if self.current_mod == "Finishing":
                self.favorite_manage(favorite_type="Formula", delete=False)
                self.finishing_signal.emit(number)
                return

            if self.current_mod == "Replace":
                self.replace_signal.emit(number)
                return

            if self.current_mod == "Search":
                self.search_signal.emit(number)
                return

        qm_selection_list = self.ui.attributes_list.selectionModel().selectedRows()
        qm_selection_list.sort()

        numbers_list = list()

        for qm_filter in qm_selection_list:

            number, name = self.get_number_and_name_by_qm(qm_filter)

            if number is None:
                print("widget_ajouter_attribut -- attributs_ajouter -- numero is None")
                continue

            if name is None:
                print("widget_ajouter_attribut -- attributs_ajouter -- nom is None")
                continue

            if number in self.numbers_current_list:
                continue

            if number in attribute_val_default_layer:

                for number_sub in attribute_val_default_layer:

                    if number_sub not in numbers_list and number_sub not in self.numbers_current_list:
                        numbers_list.append(number_sub)

                continue

            if number in attribute_val_default_fill:

                for number_sub in attribute_val_default_fill:

                    if number_sub not in numbers_list:
                        numbers_list.append(number_sub)

                continue

            elif number in attribute_val_default_room:

                for number_sub in attribute_val_default_room:

                    if number_sub not in numbers_list:
                        numbers_list.append(number_sub)

                continue

            else:

                numbers_list.append(number)

        # ---------------------------------------
        # signal emit
        # ---------------------------------------

        if self.current_mod == "Model" or self.current_mod == "Order":
            self.add_options.emit(numbers_list)
            return

        self.add_attributs.emit(numbers_list)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attributes_save()

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):

        super().closeEvent(event)

        self.ui.search_bar.clear()

        if self.reload_autocompletion:
            self.allplan.autocompletion_loading()

        self.reload_autocompletion = False

        # ---------------------------------------

        datas_config = settings_read(file_name=attribute_setting_file)

        group_index = self.ui.group_list.currentRow()

        if group_index < 0:
            group_index = 0

        datas_config["group_index"] = group_index

        # ---------------------------------------

        header = self.ui.attributes_list.horizontalHeader()

        if header is not None:
            datas_config["order"] = header.sortIndicatorOrder()
            datas_config["order_col"] = header.sortIndicatorSection()

        # ---------------------------------------

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

        settings_save(file_name=attribute_setting_file, config_datas=datas_config)

        # ---------------------------------------

        if not (self.favorite_material_changed + self.favorite_component_changed + self.favorite_formula_changed):
            return

        datas = settings_read(attribute_config_file)

        if self.favorite_material_changed:

            if "material" not in datas:
                print(f"attribute_add -- favorite_import_action -- component not in datas")
                return

            datas["material"] = sorted(self.allplan.material_favorite_list, key=int)

        if self.favorite_component_changed:

            if "component" not in datas:
                print(f"attribute_add -- favorite_import_action -- component not in datas")
                return

            datas["component"] = sorted(self.allplan.component_favorite_list, key=int)

            return

        if self.favorite_formula_changed:

            if "formula" not in datas:
                print(f"attribute_add -- favorite_import_action -- formula not in datas")
                return

            datas["formula"] = sorted(self.allplan.formula_favorite_list, key=int)

        settings_save(attribute_config_file, datas)

        self.favorite_material_changed = False
        self.favorite_component_changed = False
        self.favorite_formula_changed = False

    def changeEvent(self, event: QEvent):

        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.ismaximized_on = True

            else:
                self.ismaximized_on = False
                move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.get_group_name_selected_if_favorite() == "":
                event.ignore()
                return

            if favorites_import_verification(file_path=file_path):
                event.accept()
            else:
                event.ignore()

        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.get_group_name_selected_if_favorite() == "":
                event.ignore()
                return

            if favorites_import_verification(file_path=file_path):
                event.accept()
            else:
                event.ignore()

        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():

            event.setDropAction(Qt.CopyAction)

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            group_name = self.get_group_name_selected_if_favorite()

            if group_name == "":
                event.ignore()
                return

            if favorites_import_verification(file_path=file_path):

                self.favorite_import_file_loading(file_path=file_path, group_name=group_name)
                event.accept()

            else:
                event.ignore()
        else:
            event.ignore()

    @staticmethod
    def a___________________end______():
        pass


class NumericSortProxyModel(QSortFilterProxyModel):

    def __init__(self, column_number):
        super().__init__()

        self.column_number = column_number

    def lessThan(self, qm_left, qm_right):

        if not isinstance(qm_left, QModelIndex) or not isinstance(qm_right, QModelIndex):
            return super().lessThan(qm_left, qm_right)

        if qm_left.column() != self.column_number:
            return super().lessThan(qm_left, qm_right)

        left_number = qm_left.data(user_data_type)
        right_number = qm_right.data(user_data_type)

        if not isinstance(left_number, int) or not isinstance(right_number, int):
            return super().lessThan(qm_left, qm_right)

        try:
            check = left_number < right_number
        except Exception:
            return super().lessThan(qm_left, qm_right)

        return check
