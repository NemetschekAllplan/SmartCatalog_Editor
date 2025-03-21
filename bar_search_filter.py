#!/usr/bin/python3
# -*- coding: utf-8 -*
import json

from PyQt5.Qt import *

from allplan_manage import AllplanDatas, AllplanPaths, AttributeDatas
from attribute_add import NumericSortProxyModel, AttributesWidget
from main_datas import asc_export_path, asc_settings_path, search_setting_file, search_setting_datas, \
    attribut_default_obj
from main_datas import attribute_icon, get_icon, user_data_type, application_title, folder_code, material_code
from main_datas import col_cat_number, col_cat_value, component_code, link_code
from tools import get_look_tableview, get_look_combobox, move_widget_ss_bouton, qm_check, browser_file, settings_read
from ui_search_filters import Ui_SearchFilter


class SearchFiterWidget(QWidget):
    # ele_type, filter_column, number, mode_index, case
    modify_search_filter = pyqtSignal()
    cancel_search_filter = pyqtSignal()

    def __init__(self, asc, filter_button: QPushButton):
        super().__init__()

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_SearchFilter()
        self.ui.setupUi(self)

        # ---------------------------------------
        # LOADING PARENT
        # ---------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))
        self.asc.langue_change.connect(self.search_reset)

        self.filter_button = filter_button

        self.allplan: AllplanDatas = self.asc.allplan

        # ---------------------------------------
        # Variables
        # ---------------------------------------

        self.change_made = False
        self.save_ok = False

        self.search_current = ""
        self.search_number_current = ""

        self.attributes_list = list()
        self.export_path = asc_export_path
        self.import_path = asc_export_path

        self.search_type = ""
        self.search_column = 0
        self.search_number = ""
        self.search_mode = 0
        self.search_case = False

        # ---------------------------------------
        # SETTINGS
        # ---------------------------------------

        self.search_load_settings(file_path=f"{asc_settings_path}{search_setting_file}.ini", import_mode=False)

        # ---------------------------------------
        # Datas
        # ---------------------------------------

        self.search_model = QStandardItemModel()
        self.search_model.setHorizontalHeaderLabels(["", ""])

        self.search_filter = NumericSortProxyModel(column_number=0)
        self.search_filter.setSourceModel(self.search_model)

        self.search_tableview = QTableView()
        self.search_tableview.setModel(self.search_filter)
        self.ui.search_in_attribute_list.setModel(self.search_filter)

        get_look_tableview(self.search_tableview)

        self.search_model_creation(attributes_list=self.attributes_list)

        self.search_tableview.horizontalHeader().resizeSection(1, 24)
        self.search_tableview.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.search_tableview.verticalHeader().hide()
        self.search_tableview.horizontalHeader().hide()

        self.search_tableview.setAlternatingRowColors(True)

        self.ui.search_in_attribute_list.setView(self.search_tableview)

        # ---------------------------------------
        # Widget Attributes
        # ---------------------------------------

        self.attributes_widget: AttributesWidget = self.asc.attributes_widget

        self.attributes_widget.search_signal.connect(self.search_attribute_closed)

        # ---------------------------------------
        # Signals - Element types
        # ---------------------------------------

        self.ui.search_type_folder.clicked.connect(self.search_type_changed)
        self.ui.search_type_material.clicked.connect(self.search_type_changed)
        self.ui.search_type_component.clicked.connect(self.search_type_changed)
        self.ui.search_type_link.clicked.connect(self.search_type_changed)

        self.ui.search_type_select_all.clicked.connect(self.search_type_select_all)

        # ---------------------------------------
        # Signals - Find in
        # ---------------------------------------

        self.ui.search_in_code.clicked.connect(self.search_options_changed)
        self.ui.search_in_attribute_all.clicked.connect(self.search_options_changed)

        self.ui.search_in_attribute_one.clicked.connect(self.search_options_changed)
        self.ui.search_in_attribute_open.clicked.connect(self.search_attribute_open_clicked)

        self.ui.search_in_attribute_list.currentIndexChanged.connect(self.search_number_changed)

        self.ui.search_in_number.clicked.connect(self.search_options_changed)

        # ---------------------------------------
        # Signals - Modes
        # ---------------------------------------

        self.ui.search_mode_list.currentIndexChanged.connect(self.search_mode_changed)

        get_look_combobox(widget=self.ui.search_mode_list)

        # ---------------------------------------
        # Signals - Case
        # ---------------------------------------

        self.ui.search_mode_case.clicked.connect(self.search_case_changed)

        # ---------------------------------------
        # Signals - Favorites
        # ---------------------------------------

        self.ui.bt_export.clicked.connect(self.search_export)
        self.ui.bt_import.clicked.connect(self.search_import)

        # ---------------------------------------
        # Signals - Reset
        # ---------------------------------------

        self.ui.reset.clicked.connect(self.search_settings_reset)

        # ---------------------------------------
        # Signals - Others
        # ---------------------------------------

        self.ui.ok.clicked.connect(self.search_ok_clicked)
        self.ui.quit.clicked.connect(self.search_quit_clicked)

    @staticmethod
    def a___________________search_init______():
        pass

    def search_load_settings(self, file_path: str, import_mode=False):

        # ---------------------------------------
        # SETTINGS - read
        # ---------------------------------------

        try:

            with open(file_path, 'r', encoding="Utf-8") as file:

                search_datas = json.load(file)

        except Exception:
            search_datas = dict(search_setting_datas)

        if not isinstance(search_datas, dict):
            search_datas = dict(search_setting_datas)

        # -----------------------------------------------
        #
        # -----------------------------------------------

        ele_type = search_datas.get("ele_type", search_setting_datas.get("ele_type"))

        if not isinstance(ele_type, list):
            ele_type = search_setting_datas.get("ele_type")

        if len(ele_type) != 4:
            ele_type = search_setting_datas.get("ele_type")

        self.ui.search_type_folder.setChecked(ele_type[0] is True)
        self.ui.search_type_material.setChecked(ele_type[1] is True)
        self.ui.search_type_component.setChecked(ele_type[2] is True)
        self.ui.search_type_link.setChecked(ele_type[3] is True)

        self.search_type_changed()

        # -----------------------------------------------

        search_option = search_datas.get("search_option", search_setting_datas.get("search_option"))

        if not isinstance(search_option, int):
            search_option = search_setting_datas.get("search_option")

        if search_option == 1:
            self.ui.search_in_attribute_all.setChecked(True)
        elif search_option == 2:
            self.ui.search_in_attribute_one.setChecked(True)
        elif search_option == 3:
            self.ui.search_in_number.setChecked(True)
        else:
            self.ui.search_in_code.setChecked(True)

        self.search_options_changed()

        # -----------------------------------------------

        if not import_mode:

            attributes_list = search_datas.get("attributes_list", search_setting_datas.get("attributes_list"))

            if not isinstance(attributes_list, list):
                attributes_list = search_setting_datas.get("attributes_list")

            if len(attributes_list) == 0:
                attributes_list = search_setting_datas.get("attributes_list")

        else:

            attributes_list = list()

        attributes_list.sort(key=int)

        self.attributes_list = attributes_list

        # -----------------------------------------------

        search_mode = search_datas.get("search_mode", search_setting_datas.get("search_mode"))

        if not isinstance(search_mode, int):
            search_mode = search_setting_datas.get("search_mode")

        self.ui.search_mode_list.setCurrentIndex(search_mode)

        self.search_mode_changed()

        # -----------------------------------------------

        search_number = search_datas.get("search_number", search_setting_datas.get("search_number"))

        if not isinstance(search_number, str):
            search_number = search_setting_datas.get("search_number")

        self.search_number_current = search_number

        # -----------------------------------------------

        search_case = search_datas.get("search_case", search_setting_datas.get("search_case"))

        if not isinstance(search_case, bool):
            search_case = search_setting_datas.get("search_case")

        self.ui.search_mode_case.setChecked(search_case)

        self.search_case_changed()

        # -----------------------------------------------

        if import_mode:
            return

        path_export = search_datas.get("path_export", search_setting_datas.get("path_export"))

        if not isinstance(path_export, str):
            path_export = search_setting_datas.get("path_export")

        self.export_path = path_export

        # -----------------------------------------------

        path_import = search_datas.get("path_import", search_setting_datas.get("path_import"))

        if not isinstance(path_import, str):
            path_import = search_setting_datas.get("path_import")

        self.import_path = path_import

    def search_reset(self):

        self.search_load_settings(file_path=f"{asc_settings_path}{search_setting_file}.ini", import_mode=False)

        self.search_model_reset(attributes_list=self.attributes_list)

        self.change_made = False

    def search_show(self, search_current: str):

        move_widget_ss_bouton(button=self.filter_button, widget=self, left_force=True)

        self.search_current = search_current

        self.search_options_changed()

        self.change_made = False
        self.save_ok = False

        self.show()

    @staticmethod
    def a___________________search_ele_type______():
        pass

    def search_type_changed(self):

        error_visibility = (not self.ui.search_type_folder.isChecked() and
                            not self.ui.search_type_material.isChecked() and
                            not self.ui.search_type_component.isChecked() and
                            not self.ui.search_type_link.isChecked())

        self.ui.ok.setEnabled(not error_visibility)

        self.ui.search_in_error.setVisible(error_visibility)

        self.ui.search_type_select_all.setEnabled(not (self.ui.search_type_folder.isChecked() and
                                                       self.ui.search_type_material.isChecked() and
                                                       self.ui.search_type_component.isChecked() and
                                                       self.ui.search_type_link.isChecked()))

        self.search_type = self.search_get_type()

    def search_type_select_all(self):

        self.ui.search_type_folder.setChecked(True)
        self.ui.search_type_material.setChecked(True)
        self.ui.search_type_component.setChecked(True)
        self.ui.search_type_link.setChecked(True)

        self.search_type_changed()

    @staticmethod
    def a___________________search_options______():
        pass

    def search_options_changed(self):

        attribute_spe = self.ui.search_in_attribute_one.isChecked()

        self.ui.search_in_attribute_list.setEnabled(attribute_spe)
        self.ui.search_in_attribute_open.setEnabled(attribute_spe)

        if self.search_current == "" or self.search_current.isdigit() or not self.ui.search_in_number.isChecked():
            self.ui.search_in_number_error.setVisible(False)
        else:
            self.ui.search_in_number_error.setVisible(True)

        self.search_column = self.search_get_column()
        self.search_number = self.search_get_number()

    @staticmethod
    def a___________________search_model______():
        pass

    def search_model_reset(self, attributes_list: list):

        if not isinstance(attributes_list, list):
            return

        self.search_model.blockSignals(True)

        self.search_model.clear()

        self.search_model_creation(attributes_list=attributes_list)

        self.search_model.blockSignals(False)

    def search_model_creation(self, attributes_list: list):

        if not isinstance(attributes_list, list):
            print("bar_search -- SearchFilterWidget -- search_model_creation -- not isinstance(attributes_list, list)")
            return list()

        if len(attributes_list) == 0:
            print("bar_search -- SearchFilterWidget -- search_model_creation -- len(attributes_list) == 0")
            return list()

        new_attributes_list = list()

        for number_str in attributes_list:

            try:
                number_int = int(number_str)

                number_str = str(number_int)
            except Exception:
                print("bar_search -- SearchFilterWidget -- search_model_creation -- value isn't number")
                continue

            if number_str in new_attributes_list:
                print("bar_search -- SearchFilterWidget -- search_model_creation --  number in new_attributes_list")
                continue

            if len(number_str) > 5:
                print("bar_search -- SearchFilterWidget -- search_model_creation -- len(number) > 5")
                continue

            if number_str == "0":
                print("bar_search -- SearchFilterWidget -- search_model_creation -- number == 0")
                continue

            if not self.search_model_add(number_str=number_str, add_button=False):
                return

        self.search_model_sort()

        self.search_model_select(number=self.search_number_current)

    def search_model_add(self, number_str: str, name="", add_button=True):

        attribute_obj = self.allplan.attributes_dict.get(number_str)

        if not isinstance(attribute_obj, AttributeDatas):
            print("bar_search -- SearchFilterWidget -- search_model_add --  "
                  "not isinstance(attribute_obj, AttributeDatas)")
            return False

        if name == "":
            name = attribute_obj.name

        try:
            number_str = str(int(number_str))
        except Exception:
            print("bar_search -- SearchFilterWidget -- search_model_add -- value isn't number")
            return False

        row_current = self.search_get_index(name=name, on_filter=False)

        if row_current > -1:
            return False

        self.search_model_add_item(name=name, number=number_str, add_button=add_button)

        if add_button:
            self.search_model_select(number=self.search_number_current)

        return True

    def search_model_add_item(self, name: str, number: str, add_button=True) -> None:

        try:
            number_int = int(number)

        except Exception:

            print("bar_search -- SearchFilterWidget -- search_model_add_item -- value isn't number")
            return

        qs = QStandardItem(get_icon(attribute_icon), number)
        qs.setToolTip(name)

        qs.setData(number_int, user_data_type)

        qs_delete = QStandardItem("")
        qs_delete.setToolTip(self.tr("Supprimer cet attribut de la liste"))

        self.search_model.appendRow([qs, qs_delete])

        if not add_button:
            return

        self.search_model_sort()

    def search_model_sort(self):

        self.search_filter.sort(0, Qt.AscendingOrder)

        self.search_model_button_refresh()

    def search_model_select(self, number: str) -> bool:

        row_index = self.search_get_index(number=number, on_filter=True)

        if row_index == -1:
            print("bar_search -- SearchFilterWidget -- search_model_select -- search_index == -1")
            return False

        self.ui.search_in_attribute_list.setCurrentIndex(row_index)

        self.search_number_current = number

        self.search_number = self.search_get_number()

        return True

    def search_get_index(self, name="", number="", on_filter=True):

        if name != "":
            role = Qt.ToolTipRole
            value = name
        elif number != "":
            role = Qt.DisplayRole
            value = number
        else:
            print("bar_search -- SearchFilterWidget -- search_get_index -- bad parameters")
            return

        search_start = self.search_model.index(0, 0)

        search = self.search_model.match(search_start, role, value, 1, Qt.MatchExactly)

        if len(search) == 0:
            return -1

        qm = search[0]

        if not qm_check(qm):
            print("bar_search -- SearchFilterWidget -- search_get_index -- not qm_check(qm)")
            return -1

        if not on_filter:
            return qm.row()

        qm_filter = self.search_filter.mapFromSource(qm)

        if not qm_check(qm):
            print("bar_search -- SearchFilterWidget -- search_get_index -- not qm_check(qm)")
            return -1

        return qm_filter.row()

    @staticmethod
    def a___________________search_model_button_______________():
        pass

    def search_model_button_creation(self, row_index: int) -> None:

        qm = self.search_filter.index(row_index, 0)

        if not qm_check(qm):
            return

        number = qm.data(Qt.ToolTipRole)

        enable = number != "83"

        button = QPushButton(QIcon(":/Images/delete.svg"), "")

        button.setIconSize(QSize(20, 20))
        button.setFlat(True)
        button.setEnabled(enable)

        button.clicked.connect(self.search_model_bouton_clicked(row_index))

        self.search_tableview.setIndexWidget(self.search_filter.index(row_index, 1), button)

        return

    def search_model_button_refresh(self) -> None:

        row_count = self.search_filter.rowCount()

        for row_index in range(row_count):
            self.search_model_button_creation(row_index=row_index)

    def search_model_bouton_clicked(self, row_index: int):
        def delete_row():
            self.search_filter.removeRow(row_index)
            self.search_model_button_refresh()

        return delete_row

    @staticmethod
    def a___________________search_attribute______():
        pass

    def search_attribute_open_clicked(self):

        self.attributes_widget.attribute_show(current_mod="Search",
                                              current_widget=self.asc,
                                              attributes_list=self.search_get_attributes_list())

    def search_attribute_closed(self, number: str):

        self.ui.search_in_attribute_list.blockSignals(True)

        self.search_model_add(number_str=number, add_button=True)

        self.search_model_select(number=number)

        self.ui.search_in_attribute_list.blockSignals(False)

        self.search_show(search_current=self.search_current)

    @staticmethod
    def a___________________search_number______():
        pass

    def search_number_changed(self):

        self.search_number = self.search_get_number()

    @staticmethod
    def a___________________search_mode______():
        pass

    def search_mode_changed(self):

        index_current = self.ui.search_mode_list.currentIndex()

        self.ui.search_mode_case.setEnabled(index_current != 4)

        self.search_mode = self.search_get_mode()

    @staticmethod
    def a___________________search_case______():
        pass

    def search_case_changed(self):

        self.search_case = self.search_get_case()

    @staticmethod
    def a___________________search_import______():
        pass

    def search_import(self):

        a = self.tr("Fichier")

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [asc_export_path,
                              self.allplan.allplan_paths.std_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.usr_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[search_setting_file, "path_import"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{a} INI": [".ini"]},
                                 current_path=self.import_path,
                                 default_path=asc_export_path,
                                 use_setting_first=False,
                                 use_save=False)

        if file_path == "":
            self.search_show(search_current=self.search_current)
            return

        self.search_load_settings(file_path=file_path, import_mode=True)

        self.change_made = True

        self.search_show(search_current=self.search_current)

    def search_export(self):

        b = self.tr("Fichier")

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [asc_export_path,
                              self.allplan.allplan_paths.std_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.usr_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[search_setting_file, "path_export"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{b} INI": [".ini"]},
                                 current_path=self.export_path,
                                 default_path=asc_export_path,
                                 use_setting_first=False,
                                 use_save=True)
        if file_path == "":
            self.search_show(search_current=self.search_current)
            return

        self.search_save_settings(file_path=file_path, export_mode=True)

        self.search_show(search_current=self.search_current)

    @staticmethod
    def a___________________search_get_datas______():
        pass

    def search_get_type(self) -> str:

        # --------------------------------------
        # Element type
        # --------------------------------------

        search_type = ""

        if self.ui.search_type_folder.isChecked():
            search_type = f"^({folder_code}"

        if self.ui.search_type_material.isChecked():
            if search_type == "":

                search_type = f"^({material_code}"

            else:

                search_type += f"|{material_code}"

        if self.ui.search_type_component.isChecked():

            if search_type == "":

                search_type = f"^({component_code}"

            else:

                search_type += f"|{component_code}"

        if self.ui.search_type_link.isChecked():

            if search_type == "":

                search_type = f"^({link_code}"

            else:

                search_type += f"|{link_code}"

        if search_type != "":
            search_type += ")$"

        if self.search_type != search_type:
            self.change_made = True

        return search_type

    def search_get_column(self) -> int:

        # --------------------------------------
        # Search in : Column
        # --------------------------------------

        if self.ui.search_in_number.isChecked():

            if self.search_column != col_cat_number:
                self.change_made = True

            return col_cat_number

        if self.search_column != col_cat_value:
            self.change_made = True

        return col_cat_value

    def search_get_number(self) -> str:

        # --------------------------------------
        # Search in : Attribute
        # --------------------------------------

        if self.ui.search_in_code.isChecked():

            if self.search_number != attribut_default_obj.current:
                self.change_made = True

            return attribut_default_obj.current

        if self.ui.search_in_attribute_one.isChecked():

            number_user = self.ui.search_in_attribute_list.currentText()

            if number_user != "" and number_user.isdigit():

                if self.search_number != number_user:
                    self.change_made = True

                return number_user

        if self.search_number != "":
            self.change_made = True

        return ""

    def search_get_mode(self) -> int:

        # --------------------------------------
        # Search Mode
        # --------------------------------------

        search_mode_index = self.ui.search_mode_list.currentIndex()

        if search_mode_index not in [0, 1, 2, 3]:

            if self.search_mode != 0:
                self.change_made = True
            return 0

        if self.search_mode != search_mode_index:
            self.change_made = True

        return search_mode_index

    def search_get_case(self) -> int:

        # --------------------------------------
        # Search Mode - Case
        # --------------------------------------

        if self.ui.search_mode_case.isChecked():

            if self.search_case != Qt.CaseSensitive:
                self.change_made = True

            return Qt.CaseSensitive

        if self.search_case != Qt.CaseInsensitive:
            self.change_made = True

        return Qt.CaseInsensitive

    @staticmethod
    def a___________________search_reset______():
        pass

    def search_settings_reset(self):

        # ------------------------
        # Search type
        # ------------------------

        self.ui.search_type_folder.setChecked(True)
        self.ui.search_type_material.setChecked(True)
        self.ui.search_type_component.setChecked(True)
        self.ui.search_type_link.setChecked(True)

        self.search_type_changed()

        # ------------------------
        # Search option
        # ------------------------

        self.ui.search_in_attribute_all.setChecked(True)

        self.search_options_changed()

        # ------------------------
        # Search Mode
        # ------------------------

        self.ui.search_mode_list.setCurrentIndex(0)

        self.search_mode_changed()

        # ------------------------
        # Search Case
        # ------------------------

        self.ui.search_mode_case.setChecked(False)

        self.search_case_changed()

    @staticmethod
    def a___________________search_save______():
        pass

    def search_ok_clicked(self):

        self.save_ok = True

        self.search_type = self.search_get_type()
        self.search_column = self.search_get_column()
        self.search_number = self.search_get_number()
        self.search_mode = self.search_get_mode()
        self.search_case = self.search_get_case()

        self.close()

        self.modify_search_filter.emit()

    def search_save_settings(self, file_path: str, export_mode=False):

        search_datas = settings_read(search_setting_file)

        if not isinstance(search_datas, dict):
            return

        # ----------------
        # attributes_list
        # ----------------

        if not export_mode:
            search_datas["attributes_list"] = self.search_get_attributes_list()

        elif "attributes_list" in search_datas:
            search_datas.pop("attributes_list")

        # ----------------
        # ele_type
        # ----------------

        search_datas["ele_type"] = [self.ui.search_type_folder.isChecked(),
                                    self.ui.search_type_material.isChecked(),
                                    self.ui.search_type_component.isChecked(),
                                    self.ui.search_type_link.isChecked()]

        # ----------------
        # path_export
        # ----------------
        if not export_mode:
            search_datas["path_export"] = self.export_path

        # ----------------
        # path_import
        # ----------------
        if not export_mode:
            search_datas["path_import"] = self.import_path

        # ----------------
        # search_case
        # ----------------

        search_datas["search_case"] = self.ui.search_mode_case.isChecked()

        # ----------------
        # search_mode
        # ----------------

        search_datas["search_mode"] = self.ui.search_mode_list.currentIndex()

        # ----------------
        # search_mode
        # ----------------

        search_datas["search_number"] = self.ui.search_in_attribute_list.currentText()

        # ----------------
        # search_option
        # ----------------

        if self.ui.search_in_attribute_all.isChecked():

            search_datas["search_option"] = 1

        elif self.ui.search_in_attribute_one.isChecked():

            search_datas["search_option"] = 2

        elif self.ui.search_in_number.isChecked():

            search_datas["search_option"] = 3

        else:

            search_datas["search_option"] = 0

        # ----------------
        # save file
        # ----------------

        try:

            with open(file_path, 'w', encoding="Utf-8") as file:

                json.dump(search_datas, file, ensure_ascii=False, indent=2)

                return True

        except Exception as error:
            print(f"bar_search -- SearchFilterWidget --  search_save_settings -- {error}")
            return False

    @staticmethod
    def a___________________search_close______():
        pass

    def search_quit_clicked(self):
        self.save_ok = False
        self.close()

    @staticmethod
    def a___________________search_tools______():
        pass

    def search_get_attributes_list(self) -> list:

        attributes_list = list()

        row_count = self.search_model.rowCount()

        for row_index in range(row_count):

            qm_number = self.search_model.index(row_index, 0)

            if not qm_check(qm_number):
                continue

            number = qm_number.data()

            if not isinstance(number, str):
                continue

            if not number.isnumeric():
                continue

            if number in attributes_list:
                continue

            attributes_list.append(number)

        return attributes_list

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.search_ok_clicked()

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):

        self.search_save_settings(file_path=f"{asc_settings_path}{search_setting_file}.ini", export_mode=False)

        if not self.save_ok and self.change_made:
            self.cancel_search_filter.emit()

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass
