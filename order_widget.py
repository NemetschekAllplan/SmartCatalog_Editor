#!/usr/bin/python3
# -*- coding: utf-8 -*

from allplan_manage import *
from attribute_add import AttributesWidget
from catalog_manage import CatalogDatas
from ui_order import Ui_Order
from tools import get_look_tableview, find_folder_path, find_filename, make_backup, move_window_tool, MyContextMenu
from tools import settings_save, read_file_to_text, browser_file


class OrderWidget(QWidget):
    order_edit_signal = pyqtSignal(int, int, bool)

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_Order()
        self.ui.setupUi(self)

        get_look_tableview(self.ui.order_table)

        # ---------------------------------------
        # LOADING PARENT
        # ---------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.allplan: AllplanDatas = self.asc.allplan
        self.catalog: CatalogDatas = self.asc.catalog

        self.modification_made = False

        self.number_selected_list = list()

        # ---------------------------------------
        # LOADING Attributes widget
        # ---------------------------------------

        self.widget_attribut: AttributesWidget = self.asc.attributes_widget
        self.widget_attribut.add_options.connect(self.order_add_action)

        # -----------------------------------------------
        # read settings
        # -----------------------------------------------

        order_settings = settings_read(order_setting_file)

        # -----------------------------------------------

        self.ismaximized_on = order_settings.get("ismaximized_on", order_setting_datas.get("ismaximized_on", False))

        if not isinstance(self.ismaximized_on, bool):
            self.ismaximized_on = order_setting_datas.get("ismaximized_on", False)

        # -----------------------------------------------

        width = order_settings.get("width", order_setting_datas.get("width", 800))

        if not isinstance(width, int):
            width = order_setting_datas.get("width", 800)

        # -----------------------------------------------

        height = order_settings.get("height", order_setting_datas.get("height", 800))

        if not isinstance(height, int):
            height = order_setting_datas.get("height", 800)

        self.resize(width, height)

        # -----------------------------------------------

        import_path = order_settings.get("path_import", order_setting_datas.get("path_import", ""))

        if not isinstance(import_path, str):
            import_path = order_setting_datas.get("path_import", "")

        self.import_path = import_path

        # -----------------------------------------------

        export_path = order_settings.get("path_export", order_setting_datas.get("path_export", ""))

        if not isinstance(export_path, str):
            export_path = order_setting_datas.get("path_export", "")

        self.export_path = export_path

        # -----------------------------------------------

        other_attributes = order_settings.get("other", order_setting_datas.get("other", 0))

        if other_attributes not in [0, 1, 2, 3]:
            other_attributes = order_setting_datas.get("other", 0)

        self.other_attributes = other_attributes

        if other_attributes == 1:
            self.ui.order_91.setChecked(True)
        elif other_attributes == 2:
            self.ui.order_az.setChecked(True)
        elif other_attributes == 3:
            self.ui.order_za.setChecked(True)
        else:
            self.ui.order_19.setChecked(True)

        # -----------------------------------------------
        # Model
        # -----------------------------------------------

        self.order_model = QStandardItemModel()

        self.ui.order_table.setModel(self.order_model)

        self.ui.order_table.clicked.connect(self.order_buttons_manage)
        self.ui.order_table.selectionModel().selectionChanged.connect(self.order_buttons_manage)

        self.ui.order_table.customContextMenuRequested.connect(self.order_table_menu_show)

        # ---------------------------------------
        # SIGNAl
        # --------------------------------------

        self.ui.order_add.clicked.connect(self.order_add_clicked)
        self.ui.order_add_auto.clicked.connect(self.order_add_auto_clicked)

        # --------------------------------------

        self.ui.order_up.clicked.connect(self.order_up_clicked)
        self.ui.order_down.clicked.connect(self.order_down_clicked)

        # --------------------------------------

        self.ui.order_del.clicked.connect(self.order_delete_clicked)
        self.ui.order_cut.clicked.connect(self.order_cut_clicked)
        self.ui.order_paste.clicked.connect(self.order_paste_clicked)

        # --------------------------------------

        self.ui.order_import.clicked.connect(self.order_import_clicked)
        self.ui.order_export.clicked.connect(self.order_export_clicked)

        # --------------------------------------

        self.ui.order_save.clicked.connect(self.order_save_clicked)
        self.ui.order_quit.clicked.connect(self.close)

    @staticmethod
    def a___________________order_init______():
        pass

    def order_show(self) -> None:

        attributes_list = self.order_read_config()

        self.order_model_init(attributes_list=attributes_list)

        self.modification_made = False

        # -----------------

        move_window_tool(widget_parent=self.asc, widget_current=self)

        if self.ismaximized_on:

            self.showMaximized()
        else:
            self.show()

    def order_read_config(self) -> list:

        config_path = f"{asc_settings_path}{order_config_file}.csv"

        if os.path.exists(config_path):

            order_config = self.order_read_config_action(file_path=config_path)

            return order_config

        else:

            return order_config_datas

    @staticmethod
    def order_read_config_action(file_path: str) -> list:

        if not isinstance(file_path, str):
            return list()

        if not os.path.exists(file_path):
            return list()

        content = read_file_to_text(file_path=file_path)

        if "," not in content:
            return list()

        attribute_list = content.split(", ")

        return attribute_list

    def order_model_init(self, attributes_list: list) -> bool:

        selection_list = self.order_save_selection()

        self.order_model.clear()
        self.order_model.setHorizontalHeaderLabels([self.tr("Numéro"), self.tr("Nom")])

        attribute_obj = self.allplan.attributes_dict.get(attribut_default_obj.current)

        if not isinstance(attribute_obj, AttributeDatas):
            print("order_widget -- order_model_init -- not isinstance(attribute_obj, AttributeDatas)")
            return False

        qs_83_number = QStandardItem(attribut_default_obj.current)
        qs_83_number.setSelectable(False)

        qs_83_name = QStandardItem(attribute_obj.name)
        qs_83_name.setSelectable(False)

        self.order_model.appendRow([qs_83_number, qs_83_name])

        # --------

        attribute_obj = self.allplan.attributes_dict.get("207")

        if not isinstance(attribute_obj, AttributeDatas):
            print("order_widget -- order_model_init -- not isinstance(attribute_obj, AttributeDatas) 2")
            return False

        qs_207_number = QStandardItem("207")

        qs_207_name = QStandardItem(attribute_obj.name)

        self.order_model.appendRow([qs_207_number, qs_207_name])

        if not isinstance(attributes_list, list):
            self.order_buttons_manage()
            return False

        layer_in = False
        fill_in = False
        room_in = False

        for number_str in attributes_list:

            if not isinstance(number_str, str):
                continue

            if number_str in ["83", "207"]:
                continue

            if number_str in attribute_val_default_layer:
                if not layer_in:

                    attribute_obj = self.allplan.attributes_dict.get(attribute_val_default_layer_first)

                    if not isinstance(attribute_obj, AttributeDatas):
                        print("order_widget -- order_model_init -- not isinstance(attribute_obj, AttributeDatas) 3")
                        continue

                    self.order_model.appendRow(
                        [QStandardItem(attribute_val_default_layer_first), QStandardItem(attribute_obj.name)])

                    layer_in = True
                    continue
                continue

            if number_str in attribute_val_default_fill:

                if not fill_in:

                    attribute_obj = self.allplan.attributes_dict.get(attribute_val_default_fill_first)

                    if not isinstance(attribute_obj, AttributeDatas):
                        print("order_widget -- order_model_init -- not isinstance(attribute_obj, AttributeDatas) 4")
                        continue

                    self.order_model.appendRow(
                        [QStandardItem(attribute_val_default_fill_first), QStandardItem(attribute_obj.name)])

                    fill_in = True
                    continue
                continue

            if number_str in attribute_val_default_room:

                if not room_in:

                    attribute_obj = self.allplan.attributes_dict.get(attribute_val_default_room_first)

                    if not isinstance(attribute_obj, AttributeDatas):
                        print("order_widget -- order_model_init -- not isinstance(attribute_obj, AttributeDatas) 5")
                        continue

                    self.order_model.appendRow(
                        [QStandardItem(attribute_val_default_room_first), QStandardItem(attribute_obj.name)])

                    room_in = True
                    continue
                continue

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):
                print("order_widget -- order_model_init -- not isinstance(attribute_obj, AttributeDatas) 6")
                continue

            self.order_model.appendRow([QStandardItem(number_str), QStandardItem(attribute_obj.name)])

        if len(selection_list) != 0:
            self.order_restore_selection(old_selection=selection_list)

        self.order_buttons_manage()
        return True

    def order_save_selection(self) -> list:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return list()

        selection_list.sort()

        numbers_list = list()

        for qm_number in selection_list:

            if not qm_check(qm_number):
                continue

            number = qm_number.data()

            if not isinstance(number, str):
                continue

            if number in numbers_list:
                continue

            numbers_list.append(number)

        return numbers_list

    def order_restore_selection(self, old_selection: list) -> None:

        if not isinstance(old_selection, list):
            return

        search_start = self.order_model.index(0, 0)

        self.ui.order_table.clearSelection()

        selection = QItemSelectionModel.Select | QItemSelectionModel.Rows

        for number in old_selection:

            search = self.order_model.match(search_start, Qt.DisplayRole, number, 1, Qt.MatchExactly)

            if len(search) == 0:
                continue

            qm = search[0]

            if not qm_check(qm):
                continue

            self.ui.order_table.selectionModel().select(qm, selection)

    @staticmethod
    def a___________________buttons_manage______():
        pass

    def order_buttons_manage(self) -> None:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        self.ui.order_del.setEnabled(self.order_is_description())
        self.ui.order_up.setEnabled(self.order_up_is_possible())
        self.ui.order_down.setEnabled(self.order_down_is_possible())

        self.ui.order_cut.setEnabled(self.order_is_description())

        self.ui.order_paste.setEnabled(len(selection_list) == 1 and len(self.number_selected_list) != 0)

        self.ui.order_export.setEnabled(self.order_model.rowCount() > 2)

    def order_scroll_to(self, qm: QModelIndex):

        self.ui.order_table.setFocus()

        if qm_check(qm):
            self.ui.order_table.scrollTo(qm, QAbstractItemView.PositionAtCenter)

    def order_is_description(self) -> bool:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        selection_count = len(selection_list)

        if selection_count == 0:
            return False

        if selection_count != 1:
            return True

        qm_number = selection_list[0]

        if not qm_check(qm_number):
            return False

        number = qm_number.data()

        return number != "207"

    @staticmethod
    def a___________________add______():
        pass

    def order_add_clicked(self) -> None:

        self.widget_attribut.attribute_show(current_mod="Order",
                                            attributes_list=list(),
                                            current_widget=self)

    def order_add_action(self, attributes_list: list, insert=True) -> None:

        attributes_exist_list = self.order_get_attributes_list()
        end_qm_selection = list()
        search_start = self.order_model.index(0, 0)

        # ---------------------------

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) != 1:
            insert_row_index = -1

        elif insert:

            qm = selection_list[0]

            if not qm_check(qm):
                insert_row_index = -1
            else:

                insert_row_index = qm.row() + 1

        else:
            insert_row_index = -1

        # ---------------------------

        self.ui.order_table.clearSelection()

        selection = QItemSelectionModel.Select | QItemSelectionModel.Rows

        qm_end = None

        for number_str in attributes_list:

            if not isinstance(number_str, str):
                continue

            if number_str in attribute_val_default_layer:
                number_str = attribute_val_default_layer_first

            elif number_str in attribute_val_default_fill:
                number_str = attribute_val_default_fill_first

            elif number_str in attribute_val_default_room:
                number_str = attribute_val_default_room_first

            if number_str in attributes_exist_list:

                search = self.order_model.match(search_start, Qt.DisplayRole, number_str, 1, Qt.MatchExactly)

                if len(search) == 0:
                    continue

                qm = search[0]

                if not qm_check(qm):
                    continue

                end_qm_selection.append(qm)

                continue

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):
                print("order_widget -- order_add_action -- not isinstance(attribute_obj, AttributeDatas)")
                continue

            self.modification_made = True

            if insert_row_index == -1:

                self.order_model.appendRow([QStandardItem(number_str), QStandardItem(attribute_obj.name)])
                qm_end = self.order_model.index(self.order_model.rowCount() - 1, 0)

            else:

                self.order_model.insertRow(insert_row_index,
                                           [QStandardItem(number_str), QStandardItem(attribute_obj.name)])

                qm_end = self.order_model.index(insert_row_index, 0)

                insert_row_index += 1

            self.ui.order_table.selectionModel().select(qm_end, selection)

        self.order_scroll_to(qm=qm_end)

        self.order_buttons_manage()

    def order_add_auto_clicked(self):

        attributes_list = self.catalog.get_attributes_list()

        attributes_list_order = self.order_get_attributes_list()

        new_order_list = list()

        for number in attributes_list:

            if number in attributes_list_order and number not in new_order_list:
                continue

            new_order_list.append(number)

        if len(attributes_list_order) == 0:
            return

        self.order_add_action(attributes_list=new_order_list, insert=False)

    @staticmethod
    def a___________________move______():
        pass

    def order_up_is_possible(self) -> bool:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return False

        row_list = [qm.row() for qm in selection_list if qm_check(qm)]

        first_index = 2

        row_list.sort()

        for index_list, index_row in enumerate(row_list):

            if index_row < first_index:
                continue

            if index_row == index_list + first_index:
                continue

            return True

        return False

    def order_up_clicked(self) -> None:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) == 0:
            self.order_buttons_manage()
            return

        modifiers = QApplication.keyboardModifiers()

        end_selection_list = list()

        first_index = 2

        row_list = [qm.row() for qm in selection_list if qm_check(qm)]

        row_list.sort()

        for index_list, index_row in enumerate(row_list):

            if index_row < first_index:
                continue

            if index_row == index_list + first_index:
                end_selection_list.append(self.order_model.index(index_row, 0))
                continue

            qs_deleted_list = self.order_model.takeRow(index_row)

            if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

                row_futur = index_list + first_index

            else:

                row_futur = index_row - 1

            if len(qs_deleted_list) != self.order_model.columnCount():
                continue

            self.order_model.insertRow(row_futur, qs_deleted_list)
            end_selection_list.append(self.order_model.index(row_futur, 0))

            self.modification_made = True

        if len(end_selection_list) == 0:
            self.order_buttons_manage()
            return

        self.ui.order_table.clearSelection()

        for qm in end_selection_list:
            self.ui.order_table.selectionModel().select(qm, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.order_buttons_manage()

    def order_down_is_possible(self) -> bool:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return False

        first_index = 2
        last_index = self.order_model.rowCount()

        row_list = [qm.row() for qm in selection_list if qm_check(qm)]

        row_list.sort(reverse=True)

        for index_list, index_row in enumerate(row_list):

            if index_row < first_index:
                continue

            if index_row == last_index - 1 - index_list:
                continue

            return True

        return False

    def order_down_clicked(self) -> None:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return

        modifiers = QApplication.keyboardModifiers()

        end_selection_list = list()

        first_index = 2
        last_index = self.order_model.rowCount()

        row_list = [qm.row() for qm in selection_list if qm_check(qm)]

        row_list.sort(reverse=True)

        for index_list, index_row in enumerate(row_list):

            if index_row < first_index:
                continue

            if modifiers == Qt.ControlModifier and index_row == last_index - 1:
                end_selection_list.append(self.order_model.index(index_row, 0))
                continue

            if index_row == last_index - 1 - index_list:
                end_selection_list.append(self.order_model.index(index_row, 0))
                continue

            qs_deleted_list = self.order_model.takeRow(index_row)

            if len(qs_deleted_list) != self.order_model.columnCount():
                continue

            if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:

                row_futur = last_index - index_list - 1

            else:

                row_futur = index_row + 1

            self.order_model.insertRow(row_futur, qs_deleted_list)

            end_selection_list.append(self.order_model.index(row_futur, 0))

            self.modification_made = True

        if len(end_selection_list) == 0:
            self.order_buttons_manage()
            return

        self.ui.order_table.clearSelection()

        for qm in end_selection_list:
            self.ui.order_table.selectionModel().select(qm, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.order_buttons_manage()

    @staticmethod
    def a___________________cut______():
        pass

    def order_cut_clicked(self) -> None:

        number_selected_list = self.order_save_selection()

        self.number_selected_list = number_selected_list

        self.order_display_cut()

        self.order_buttons_manage()

    def order_display_cut(self) -> None:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return

        row_count = self.order_model.rowCount()

        for row_index in range(row_count):

            qm_number = self.order_model.index(row_index, 0)

            if not qm_check(qm_number):
                continue

            qm_name = self.order_model.index(row_index, 1)

            if not qm_check(qm_name):
                continue

            if qm_number in selection_list:

                color = QColor(Qt.red)

            else:

                color = QColor(Qt.black)

            self.order_model.setData(qm_number, color, Qt.ForegroundRole)
            self.order_model.setData(qm_name, color, Qt.ForegroundRole)

    def order_display_cut_clear(self) -> None:

        row_count = self.order_model.rowCount()

        for row_index in range(row_count):

            qm_number = self.order_model.index(row_index, 0)

            if not qm_check(qm_number):
                continue

            qm_name = self.order_model.index(row_index, 1)

            if not qm_check(qm_name):
                continue

            self.order_model.setData(qm_number, QColor(Qt.black), Qt.ForegroundRole)
            self.order_model.setData(qm_name, QColor(Qt.black), Qt.ForegroundRole)

        self.number_selected_list = list()
        self.order_buttons_manage()

    def order_paste_clicked(self) -> bool:

        if len(self.number_selected_list) == 0:
            self.order_buttons_manage()
            return False

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) != 1:
            self.order_buttons_manage()
            return False

        qm = selection_list[0]

        if not qm_check(qm):
            self.order_display_cut_clear()
            return False

        current_number = qm.data()

        search_start = self.order_model.index(0, 0)

        qm_end = None

        selection = QItemSelectionModel.Select | QItemSelectionModel.Rows

        self.ui.order_table.clearSelection()

        for number in self.number_selected_list:

            # -------------------
            # Search cut number
            # -------------------

            search = self.order_model.match(search_start, Qt.DisplayRole, number, 1, Qt.MatchExactly)

            if len(search) == 0:
                continue

            qm_cut = search[0]

            if not qm_check(qm_cut):
                continue

            row_cut_index = qm_cut.row()

            # -------------------
            qs_cut_list = self.order_model.takeRow(row_cut_index)

            # -------------------
            # Search current number
            # -------------------

            search = self.order_model.match(search_start, Qt.DisplayRole, current_number, 1, Qt.MatchExactly)

            if len(search) == 0:
                continue

            qm_current = search[0]

            if not qm_check(qm_current):
                continue

            row_current_index = qm_current.row() + 1

            self.order_model.insertRow(row_current_index, qs_cut_list)

            qm_end = self.order_model.index(row_current_index, 0)

            self.ui.order_table.selectionModel().select(qm_end, selection)

            current_number = number

        self.order_scroll_to(qm=qm_end)

        self.order_display_cut_clear()

        return True

    @staticmethod
    def a___________________delete______():
        pass

    def order_delete_clicked(self) -> None:

        selection_list = self.ui.order_table.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return

        index_list = list()

        for qm in selection_list:

            if not qm_check(qm):
                continue

            row_current = qm.row()

            index_list.append(row_current)

        # ------------

        index_list.sort(reverse=True)

        for row_index in index_list:
            self.order_model.takeRow(row_index)

            self.modification_made = True

        self.order_buttons_manage()

    @staticmethod
    def a___________________import_export______():
        pass

    def order_import_verification(self, file_path: str) -> bool:

        attributes_list = self.order_read_config_action(file_path=file_path)

        return len(attributes_list) != 0

    def order_import_clicked(self) -> bool:

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
                                 registry=[order_setting_file, "path_import"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{a} CSV": [".csv"]},
                                 current_path=self.import_path,
                                 default_path=asc_export_path,
                                 use_setting_first=False,
                                 use_save=False)

        if file_path == "":
            return False

        attributes_list = self.order_read_config_action(file_path=file_path)

        self.modification_made = True

        return self.order_model_init(attributes_list=attributes_list)

    def order_export_clicked(self) -> bool:

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
                                 registry=[order_setting_file, "path_export"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{b} CSV": [".csv"]},
                                 current_path=self.export_path,
                                 default_path=asc_export_path,
                                 use_setting_first=False,
                                 use_save=True)
        if file_path == "":
            return False

        return self.order_save_config(file_path=file_path)

    @staticmethod
    def a___________________table______():
        pass

    def order_table_menu_show(self, point: QPoint) -> None:

        menu = MyContextMenu()

        # ------------------------------
        # Add
        # ------------------------------

        if self.ui.order_add.isEnabled() or self.ui.order_add_auto.isEnabled():

            menu.add_title(title=self.ui.order_add_title.text())

            if self.ui.order_add.isEnabled():
                menu.add_action(qicon=get_icon(attribute_add_icon),
                                title=self.ui.order_add.toolTip(),
                                action=self.order_add_clicked)

            if self.ui.order_add_auto.isEnabled():
                menu.add_action(qicon=get_icon(attribute_add_auto_icon),
                                title=self.ui.order_add_auto.toolTip(),
                                action=self.order_add_auto_clicked)

        # ------------------------------
        # Move
        # ------------------------------

        if self.ui.order_up.isEnabled() or self.ui.order_down.isEnabled():

            menu.add_title(title=self.ui.order_move_title.text())

            if self.ui.order_up.isEnabled():
                menu.add_action(qicon=get_icon(move_up_icon),
                                title=self.ui.order_up.toolTip(),
                                action=self.order_up_clicked)

            if self.ui.order_down.isEnabled():
                menu.add_action(qicon=get_icon(move_down_icon),
                                title=self.ui.order_down.toolTip(),
                                action=self.order_down_clicked)

        # ------------------------------
        # Edit
        # ------------------------------

        if self.ui.order_del.isEnabled() or self.ui.order_cut.isEnabled() or self.ui.order_down.isEnabled():

            menu.add_title(title=self.ui.order_edit_title.text())

            if self.ui.order_del.isEnabled():
                menu.add_action(qicon=get_icon(delete_icon),
                                title=self.ui.order_del.toolTip(),
                                action=self.order_delete_clicked)

            if self.ui.order_cut.isEnabled():
                menu.add_action(qicon=get_icon(cut_icon),
                                title=self.ui.order_cut.toolTip(),
                                action=self.order_cut_clicked)

            if self.ui.order_paste.isEnabled():
                menu.add_action(qicon=get_icon(paste_icon),
                                title=self.ui.order_paste.toolTip(),
                                action=self.order_paste_clicked)

        # ------------------------------
        # Import
        # ------------------------------

        if self.ui.order_import.isEnabled() or self.ui.order_export.isEnabled():

            menu.add_title(title=self.ui.order_fav_title.text())

            if self.ui.order_import.isEnabled():
                menu.add_action(qicon=get_icon(favorite_open_icon),
                                title=self.ui.order_import.toolTip(),
                                action=self.order_import_clicked)

            if self.ui.order_export.isEnabled():
                menu.add_action(qicon=get_icon(favorite_save_icon),
                                title=self.ui.order_export.toolTip(),
                                action=self.order_export_clicked)

        menu.exec_(self.ui.order_table.mapToGlobal(point))

    @staticmethod
    def a___________________save______():
        pass

    def order_save_clicked(self) -> None:

        self.order_save_action()

        self.modification_made = False

        # ------------

        self.close()

    def order_save_action(self) -> None:

        config_path = f"{asc_settings_path}{order_config_file}.csv"

        self.order_save_config(file_path=config_path)

        # ------------

        if self.ui.order_91.isChecked():

            attributes_order_col = 0
            attributes_order = 1

        elif self.ui.order_az.isChecked():

            attributes_order_col = 1
            attributes_order = 0

        elif self.ui.order_za.isChecked():

            attributes_order_col = 1
            attributes_order = 1

        else:

            attributes_order_col = 0
            attributes_order = 0

        self.order_edit_signal.emit(attributes_order, attributes_order_col, True)

    def order_save_setting(self) -> bool:

        order_settings = settings_read(file_name=order_setting_file)

        order_settings["path_import"] = self.import_path
        order_settings["path_export"] = self.export_path

        # ---------------

        if self.ui.order_91.isChecked():
            order_settings["other"] = 1
        elif self.ui.order_az.isChecked():
            order_settings["other"] = 2
        elif self.ui.order_za.isChecked():
            order_settings["other"] = 3
        else:
            order_settings["other"] = 0

        # ---------------

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                order_settings["height"] = screen.height()
                order_settings["width"] = screen.width()
                order_settings["ismaximized_on"] = True

                return settings_save(file_name=order_setting_file, config_datas=order_settings)

        order_settings["height"] = self.size().height()
        order_settings["width"] = self.size().width()
        order_settings["ismaximized_on"] = False

        return settings_save(file_name=order_setting_file, config_datas=order_settings)

    def order_save_config(self, file_path: str) -> bool:

        folder = find_folder_path(file_path)

        file = find_filename(file_path)

        backup = f"{folder}backup\\"

        if folder == "" or file == "" or backup == "":
            return False

        make_backup(chemin_dossier=folder,
                    fichier=file,
                    extension=".csv",
                    dossier_sauvegarde=backup,
                    nouveau=False)

        attributes_list = self.order_get_attributes_list()

        try:
            with open(file_path, "w") as file:
                file.writelines(", ".join(attributes_list))

        except Exception as error:

            msg(titre=self.windowTitle(),
                message=self.tr("Une erreur est survenue."),
                details=error,
                icone_critique=True)

            return False
        return True

    def order_get_attributes_list(self) -> list:

        attributes_list = ["83", "207"]

        row_count = self.order_model.rowCount()

        layer_in = False
        fill_in = False
        room_in = False

        for row_index in range(row_count):

            qm_number = self.order_model.index(row_index, 0)

            if not qm_check(qm_number):
                continue

            number = qm_number.data()

            if not isinstance(number, str):
                continue

            if number in attributes_list:
                continue

            if number in attribute_val_default_layer:

                if not layer_in:
                    attributes_list.append(attribute_val_default_layer_first)
                    layer_in = True

                    continue
                continue

            if number in attribute_val_default_fill:

                if not fill_in:
                    attributes_list.append(attribute_val_default_fill_first)
                    fill_in = True

                    continue
                continue

            if number in attribute_val_default_room:

                if not room_in:
                    attributes_list.append(attribute_val_default_room_first)

                    room_in = True
                    continue
                continue

            attributes_list.append(number)

        return attributes_list

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            self.close()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            self.order_save_action()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Up:
            self.order_up_clicked()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Down:
            self.order_down_clicked()
            return

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

            attributes_list = self.order_read_config_action(file_path=file_path)

            if len(attributes_list) != 0:
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

            attributes_list = self.order_read_config_action(file_path=file_path)

            if len(attributes_list) != 0:
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

            attributes_list = self.order_read_config_action(file_path=file_path)

            if len(attributes_list) != 0:

                self.order_model_init(attributes_list=attributes_list)

                self.modification_made = True

                event.accept()

            else:
                event.ignore()
        else:
            event.ignore()

    def closeEvent(self, event: QCloseEvent):

        super().closeEvent(event)

        self.order_save_setting()

        if not self.modification_made:
            return

        if msg(titre=self.windowTitle(),
               message=self.tr("Voulez-vous enregistrer les modifications?"),
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               defaut_bouton=QMessageBox.Ok,
               icone_sauvegarde=True) == QMessageBox.Ok:
            self.order_save_action()

        self.modification_made = False

    @staticmethod
    def a___________________end______():
        pass
