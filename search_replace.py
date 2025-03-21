#!/usr/bin/python3
# -*- coding: utf-8 -*
from attribute_add import AttributesWidget
from attribute_date import WidgetCalendar
from catalog_manage import *
from formatting_widget import Formatting
from library import Library
from tools import ValidatorInt, ValidatorDouble, ValidatorModel, ValidatorDate, move_widget_ss_bouton, MyContextMenu
from tools import get_look_tableview
from tools import afficher_message as msg
from tools import changer_selection_apparence, copy_to_clipboard, settings_save, set_appearence_type
from ui_replace import Ui_Replace

col_icon = 0
col_path = 1


class Replace(QWidget):
    ajouter_signal = pyqtSignal(ClipboardDatas, ClipboardDatas)

    def __init__(self, asc, catalog, library_widget):
        super().__init__()

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))
        self.asc.langue_change.connect(self.attribute_model_reset)

        self.hierarchy: Hierarchy = self.asc.ui.hierarchy

        self.allplan: AllplanDatas = self.asc.allplan

        self.catalog: CatalogDatas = catalog

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_Replace()
        self.ui.setupUi(self)

        changer_selection_apparence(self.ui.results_view)
        # changer_apparence_combobox(self.ui.attribute_combo)

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.paths_dict = dict()

        self.str_save = ""
        self.int_save = 1
        self.float_save = 1.000

        # -----------------------------------------------
        # Settings
        # -----------------------------------------------

        replace_datas = settings_read(replace_setting_file)

        self.ismaximized_on = replace_datas.get("ismaximized_on", False)

        if not isinstance(self.ismaximized_on, bool):
            self.ismaximized_on = False

        width = replace_datas.get("width", replace_setting_datas.get("width"))

        if not isinstance(width, int):
            width = replace_setting_datas.get("width")

        height = replace_datas.get("height", replace_setting_datas.get("height"))

        if not isinstance(height, int):
            width = replace_setting_datas.get("height")

        self.resize(width, height)

        # -----------------------------------------------

        replace_by = replace_datas.get("replace_by", replace_setting_datas.get("replace_by"))

        if not isinstance(replace_by, str):
            replace_by = replace_setting_datas.get("replace_by")

        self.ui.lineedit_value.setText(replace_by)

        # -----------------------------------------------

        ele_type = replace_datas.get("ele_type", replace_setting_datas.get("ele_type"))

        if ele_type == component_code:
            self.ui.component_bt.setChecked(True)
        else:
            self.ui.material_bt.setChecked(True)

        # -----------------------------------------------

        attributes_list = replace_datas.get("attributes_list", replace_setting_datas.get("attributes_list"))

        if not isinstance(attributes_list, list):
            attributes_list = replace_setting_datas.get("attributes_list")

        if len(attributes_list) == 0:
            attributes_list = replace_setting_datas.get("attributes_list")

        # -----------------------------------------------
        number_str = replace_datas.get("attribute", replace_setting_datas.get("attribute"))

        if not isinstance(number_str, str):
            number_str = replace_setting_datas.get("attribute")

        # -----------------------------------------------
        # attributes widget
        # -----------------------------------------------

        self.attribute_widget: AttributesWidget = self.asc.attributes_widget
        self.attribute_widget.replace_signal.connect(self.attribute_changed)

        # -----------------------------------------------
        # Formatting
        # -----------------------------------------------

        self.formatting_widget = Formatting()
        self.formatting_widget.save_modif_formatage.connect(self.lineedit_formatting_changed)

        # -----------------------------------------------
        # Library
        # -----------------------------------------------

        self.library_widget: Library = library_widget
        self.library_widget.choisir_attribut_signal.connect(self.library_changed)

        # -----------------------------------------------
        # Calendar
        # -----------------------------------------------

        self.calendar_widget = WidgetCalendar(self, self.allplan.langue)
        self.calendar_widget.date_changed.connect(self.lineedit_formatting_changed)

        self.ui.calendar_bt.clicked.connect(self.calendar_show)

        # -----------------------------------------------
        # value_search
        # -----------------------------------------------

        self.ui.value_search.textChanged.connect(self.value_search_changed)
        self.ui.value_reset.clicked.connect(self.value_reset)

        # -----------------------------------------------
        # ele_type
        # -----------------------------------------------

        self.ui.material_bt.clicked.connect(self.ele_type_changed)
        self.ui.component_bt.clicked.connect(self.ele_type_changed)

        self.ui.ele_reset_bt.clicked.connect(self.ele_type_reset)

        # -----------------------------------------------
        # attributes model
        # -----------------------------------------------

        self.attribute_model = QStandardItemModel()
        self.attribute_model.setHorizontalHeaderLabels(["", ""])

        self.attribute_filter = QSortFilterProxyModel()
        self.attribute_filter.setSourceModel(self.attribute_model)

        self.tableview = QTableView()
        self.tableview.setModel(self.attribute_filter)
        self.ui.attribute_combo.setModel(self.attribute_filter)

        get_look_tableview(self.tableview)

        self.attribute_model_creation(attributes_list=attributes_list)

        self.tableview.horizontalHeader().resizeSection(1, 24)
        self.tableview.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.tableview.verticalHeader().hide()
        self.tableview.horizontalHeader().hide()

        self.tableview.setAlternatingRowColors(True)

        self.ui.attribute_combo.setView(self.tableview)

        # -----------------------------------------------
        # replace_by model
        # -----------------------------------------------

        self.replace_by_filter = QSortFilterProxyModel()
        self.replace_by_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # -----------------------------------------------
        # attributes
        # -----------------------------------------------

        self.ui.library_show_bt.clicked.connect(self.library_show)

        self.ui.attribute_show_bt.clicked.connect(self.attribut_show)

        self.ui.attribute_reset.clicked.connect(self.attribute_reset)

        self.ui.attribute_combo.currentIndexChanged.connect(self.attribute_combo_changed)

        # -----------------------------------------------
        # replace_by_lineedit
        # -----------------------------------------------

        self.ui.lineedit_value.textChanged.connect(self.replace_by_lineedit_changed)
        self.ui.lineedit_value.editingFinished.connect(self.lineedit_float_formatting)

        self.ui.lineedit_format_bt.clicked.connect(self.formatting_show)

        # -----------------------------------------------
        # replace_by Combobox
        # -----------------------------------------------

        self.ui.combo_value.lineEdit().textEdited.connect(self.replace_by_filter.setFilterFixedString)
        self.ui.combo_value.currentIndexChanged.connect(self.replace_by_combo_changed)

        self.ui.combo_value.installEventFilter(self)

        # -----------------------------------------------
        # Search
        # -----------------------------------------------

        self.ui.search_bt.clicked.connect(self.search_launch)

        # -----------------------------------------------
        # Results model
        # -----------------------------------------------

        self.results_model = QStandardItemModel()

        self.ui.results_view.setModel(self.results_model)

        # -----------------------------------------------
        # Results
        # -----------------------------------------------

        self.ui.results_view.selectionModel().selectionChanged.connect(self.replace_buttons_manage)
        self.ui.results_view.doubleClicked.connect(self.show_selected_qs)
        self.ui.results_view.customContextMenuRequested.connect(self.replace_menu_show)

        # -----------------------------------------------
        # Bottom bar
        # -----------------------------------------------

        self.ui.replace_bt.clicked.connect(self.replace_selected)
        self.ui.replace_all_bt.clicked.connect(self.replace_all)

        self.ui.quit.clicked.connect(self.close)

        # -----------------------------------------------

        attribute_obj = self.allplan.attributes_dict.get(number_str)

        if not isinstance(attribute_obj, AttributeDatas):
            print("order_widget -- order_model_init -- not isinstance(attribute_obj, AttributeDatas) 4")
            return

        row_index = self.ui.attribute_combo.findText(attribute_obj.name, Qt.MatchExactly)

        if row_index == -1:
            return

        self.ui.attribute_combo.blockSignals(True)
        self.ui.attribute_combo.setCurrentIndex(row_index)
        self.ui.attribute_combo.blockSignals(False)

    @staticmethod
    def a___________________loading_______________():
        pass

    def replace_show(self):

        self.ele_type_reset()

        # -------------------------------------------

        move_window_tool(widget_parent=self.asc, widget_current=self, always_center=True)

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

        # -------------------------------------------

        number = self.get_catalog_current_number()

        if number is not None:
            self.attribute_changed(number_str=number)
        else:
            self.attribute_combo_changed(row_index=self.ui.attribute_combo.currentIndex())

        self.ui.attribute_reset.setEnabled(number is not None)

        # -------------------------------------------

        if self.ui.lineedit_widget.isVisible():
            self.ui.lineedit_value.setFocus()
            return

        if self.ui.combo_widget.isVisible():
            self.ui.combo_value.setFocus()
            return

        self.ui.checkbox_value.setFocus()

    @staticmethod
    def a___________________search_value_______________():
        pass

    def value_search_changed(self):
        self.results_clear()

    def value_reset(self):

        number = self.get_combo_current_number()

        value = self.get_catalog_current_value(number=number)

        if value is None:
            print("search_replace -- value_reset -- value is None")
            return

        self.ui.value_search.setText(value)

    def get_catalog_current_value(self, number=""):

        qs: MyQstandardItem = self.hierarchy.get_current_qs()

        if qs is None:
            self.ui.value_reset.setEnabled(False)
            print("search_replace -- get_catalog_current_value -- not isinstance(qs, Material)")
            return

        if self.ui.material_bt.isChecked() and not isinstance(qs, Material):
            self.ui.value_reset.setEnabled(False)
            print("search_replace -- get_catalog_current_value -- not isinstance(qs, Material)")
            return

        if self.ui.component_bt.isChecked() and not isinstance(qs, Component):
            self.ui.value_reset.setEnabled(False)
            print("search_replace -- get_catalog_current_value -- not isinstance(qs, Component)")
            return

        if number == attribut_default_obj.current:
            value = qs.text()

            if value is None:
                self.ui.value_reset.setEnabled(False)
                print("search_replace -- get_catalog_current_value --value is None")
                return

            return value

        if number == "" or number is None:
            number = self.get_catalog_current_number()

        value = qs.get_attribute_value_by_number(number)

        if not isinstance(value, str):
            self.ui.value_reset.setEnabled(False)
            print("search_replace -- get_catalog_current_value -- not isinstance(value, str)")
            return

        self.ui.value_reset.setEnabled(True)
        return value

    @staticmethod
    def a___________________type_ele_______________():
        pass

    def ele_type_changed(self):
        self.results_clear()

    def ele_type_reset(self):

        qs = self.hierarchy.get_current_qs()

        if not isinstance(qs, MyQstandardItem):
            self.replace_buttons_manage()
            print("search_replace -- ele_type_reset -- not isinstance(qs, MyQstandardItem)")
            return

        text = qs.text()

        self.ui.value_search.setText(text)

        if isinstance(qs, Material):
            self.ui.material_bt.setChecked(True)

        elif isinstance(qs, Component):
            self.ui.component_bt.setChecked(True)

        self.replace_buttons_manage()

    @staticmethod
    def a___________________attribute_______________():
        pass

    def attribute_model_reset(self):

        self.attribute_model.blockSignals(True)

        self.attribute_model.clear()

        replace_datas = settings_read(replace_setting_file)

        attributes_list = replace_datas.get("attributes_list", replace_setting_datas["attributes_list"])

        if not isinstance(attributes_list, list):
            attributes_list = replace_setting_datas["attributes_list"]

        if len(attributes_list) == 0:
            attributes_list = replace_setting_datas["attributes_list"]

        self.attribute_model_creation(attributes_list=attributes_list)

        self.attribute_model.blockSignals(False)

    def attribute_model_creation(self, attributes_list: list):

        if not isinstance(attributes_list, list):
            print("search_replace -- attribute_model_creation -- not isinstance(attributes_list, list)")
            return list()

        if len(attributes_list) == 0:
            print("search_replace -- attribute_model_creation -- len(attributes_list) == 0")
            return list()

        new_attributes_list = list()

        for number in attributes_list:

            try:
                number_int = int(number)

                number = str(number_int)
            except Exception:
                print("search_replace -- attribute_model_creation -- value isn't number")
                continue

            if number in new_attributes_list:
                print("search_replace -- attribute_model_creation -- number in new_attributes_list")
                continue

            if len(number) > 5:
                print("search_replace -- attribute_model_creation -- len(number) > 5")
                continue

            if number == "0":
                print("search_replace -- attribute_model_creation -- number == 0")
                continue

            if not self.attribute_model_add(number_str=number, add_button=False):
                return

        self.attribute_filter.sort(0, Qt.AscendingOrder)

        self.button_refresh()

        self.replace_buttons_manage()

    def attribute_model_add(self, number_str: str, name="", add_button=True) -> bool:

        if not isinstance(number_str, str):
            print("search_replace -- attribute_model_add -- not isinstance(number, str)")
            return False

        if name == "":

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):
                print("search_replace -- attribute_model_add -- not isinstance(attribute_obj, AttributeDatas)")
                return False

            name = attribute_obj.name

        if not isinstance(name, str):
            print("search_replace -- attribute_model_add -- not isinstance(name, str)")
            return False

        try:
            number_str = str(int(number_str))
        except Exception:
            print("search_replace -- attribute_model_add -- value isn't number")
            return False

        row_current = self.attribute_get_index(name=name, on_filter=False)

        if row_current > -1:
            return False

        self.attribute_model_add_item(name=name, number=number_str, add_button=add_button)

        return True

    def attribute_model_add_item(self, name: str, number: str, add_button=True) -> None:

        qs = QStandardItem(get_icon(attribute_icon), name)
        qs.setToolTip(number)

        qs_delete = QStandardItem("")
        qs_delete.setToolTip(self.tr("Supprimer cet attribut de la liste"))

        self.attribute_model.appendRow([qs, qs_delete])

        if not add_button:
            return
        qm_model = qs.index()

        if not qm_check(qm_model):
            print("search_replace -- attribute_model_add_item -- not qm_check(qm_model)")
            return

        qm_filter = self.attribute_filter.mapFromSource(qm_model)

        if not qm_check(qm_filter):
            print("search_replace -- attribute_model_add_item -- not qm_check(qm_filter)")
            return

        row_index = qm_filter.row()

        if row_index == -1:
            print("search_replace -- attribute_model_add_item -- row_index == -1")
            return

        self.button_creation(row_index=row_index)

    def attribute_get_index(self, name="", number="", on_filter=True):

        if name != "":
            role = Qt.DisplayRole
            value = name
        elif number != "":
            role = Qt.ToolTipRole
            value = number
        else:
            print("search_replace -- attribute_get_index_of_name -- bad parameters")
            return

        search_start = self.attribute_model.index(0, 0)

        search = self.attribute_model.match(search_start, role, value, 1, Qt.MatchExactly)

        if len(search) == 0:
            return -1

        qm = search[0]

        if not qm_check(qm):
            print("search_replace -- attribute_get_index_of_name -- not qm_check(qm)")
            return -1

        if not on_filter:
            return qm.row()

        qm_filter = self.attribute_filter.mapFromSource(qm)

        if not qm_check(qm):
            print("search_replace -- attribute_get_index_of_name -- not qm_check(qm)")
            return -1

        return qm_filter.row()

    def attribut_show(self):

        self.attribute_widget.attribute_show(current_mod="Replace", current_widget=self)

    def attribute_combo_changed(self, row_index: int):

        if row_index == -1:
            # textbox
            self.ui.lineedit_widget.setVisible(True)

            # Combo
            self.ui.combo_widget.setVisible(False)

            # Checkbox
            self.ui.checkbox_widget.setVisible(False)

            print("search_replace -- attribute_combo_changed -- row_index == -1")
            return

        qm = self.attribute_filter.index(row_index, 0)

        if not qm_check(qm):
            # textbox
            self.ui.lineedit_widget.setVisible(True)

            # Combo
            self.ui.combo_widget.setVisible(False)

            # Checkbox
            self.ui.checkbox_widget.setVisible(False)

            print("search_replace -- attribute_combo_changed -- not qm_check(qm)")
            return

        number = qm.data(Qt.ToolTipRole)

        self.attribute_changed(number_str=number)

    def attribute_changed(self, number_str: str):

        # -------------------------------------------
        # Number
        # -------------------------------------------

        attribute_obj = self.allplan.attributes_dict.get(number_str)

        if not isinstance(attribute_obj, AttributeDatas):
            print("search_replace -- attribute_changed -- not isinstance(attribute_obj, AttributeDatas)")
            return

        # -------------------------------------------
        # Number already exists -> if not -> add number in model
        # -------------------------------------------

        self.attribute_model_add(number_str=number_str, name=attribute_obj.name, add_button=True)

        search_index = self.attribute_get_index(name=attribute_obj.name, on_filter=True)

        if search_index == -1:
            print("search_replace -- attribute_changed -- search_index == -1")
            return

        # -------------------------------------------
        # Number select + manage replace + define new search 
        # -------------------------------------------

        self.ui.attribute_combo.blockSignals(True)

        self.ui.attribute_combo.setCurrentIndex(search_index)

        # -------------------------------------------
        # manage replace
        # -------------------------------------------

        self.replace_by_manage(number_str=number_str)

        self.ui.attribute_combo.blockSignals(False)

        # -------------------------------------------
        # define new search 
        # -------------------------------------------

        self.value_reset()

        # -------------------------------------------
        # Launch search
        # -------------------------------------------

        self.search_launch(message_show=False)

        # -------------------------------------------
        # Manage value type in lineedit
        # -------------------------------------------

        if not self.ui.lineedit_value.isVisible():
            return

        current_type = self.replace_by_save()

        if attribute_obj.option in [code_attr_str, code_attr_formule_str] and current_type != str:
            self.ui.lineedit_value.setText(f"{self.str_save}")
            return

        if attribute_obj.option in [code_attr_int, code_attr_formule_int] and current_type != int:
            self.ui.lineedit_value.setText(f"{self.int_save}")
            return

        if attribute_obj.option in [code_attr_dbl, code_attr_formule_float] and current_type != float:
            self.ui.lineedit_value.setText(f"{self.float_save}")
            self.lineedit_float_formatting()
            return

    def attribute_reset(self):

        number = self.get_catalog_current_number()

        if not isinstance(number, str):
            print("search_replace -- attribute_reset -- not isinstance(number, str)")
            return

        self.attribute_changed(number_str=number)

    def get_combo_current_number(self):

        row_index = self.ui.attribute_combo.currentIndex()

        qm = self.attribute_filter.index(row_index, 0)

        if not qm_check(qm):
            print("search_replace -- get_combo_current_number -- not qm_check(qm)")
            return None

        number = qm.data(Qt.ToolTipRole)

        if not isinstance(number, str):
            print("search_replace -- get_combo_current_number -- not isinstance(number, str)")
            return None

        return f"{number}"

    def get_combo_numbers_list(self) -> list:

        attributes_list = list()

        for row_index in range(self.attribute_model.rowCount()):

            qm = self.attribute_model.index(row_index, 0)

            if not qm_check(qm):
                print("search_replace -- get_combo_numbers_list -- not qm_check(qm)")
                continue

            number = qm.data(Qt.ToolTipRole)

            if number is None:
                print("search_replace -- get_combo_numbers_list -- number is None")
                continue

            attributes_list.append(f"{number}")

        return attributes_list

    def get_catalog_current_number(self):

        qlistwidgetitem_list = self.catalog.get_attribute_selection_list()

        if len(qlistwidgetitem_list) != 1:
            return

        qlistwidgetitem: QListWidgetItem = qlistwidgetitem_list[0]

        number = qlistwidgetitem.data(user_data_number)

        if not isinstance(number, str):
            print("search_replace -- get_catalog_current_number -- not isinstance(number, str)")
            return

        return number

    @staticmethod
    def a___________________button_combo_______________():
        pass

    def button_creation(self, row_index: int) -> None:

        qm = self.attribute_filter.index(row_index, 0)

        if not qm_check(qm):
            return

        number = qm.data(Qt.ToolTipRole)

        enable = number != "83"

        button = QPushButton(QIcon(":/Images/delete.svg"), "")

        button.setIconSize(QSize(20, 20))
        button.setFlat(True)
        button.setEnabled(enable)

        button.clicked.connect(self.bouton_clicked(row_index))

        self.tableview.setIndexWidget(self.attribute_filter.index(row_index, 1), button)

        return

    def button_refresh(self) -> None:

        row_count = self.attribute_filter.rowCount()

        for row_index in range(row_count):
            self.button_creation(row_index=row_index)

    def bouton_clicked(self, row_index: int):
        def delete_row():
            self.attribute_filter.removeRow(row_index)
            self.button_refresh()

        return delete_row

    @staticmethod
    def a___________________replace_by_______________():
        pass

    def replace_by_save(self):

        current_text = self.ui.lineedit_value.text()

        if current_text == "":
            return str

        try:
            self.int_save = int(current_text)
            return int
        except:
            pass

        try:
            self.float_save = float(current_text)
            return float
        except:
            pass

        self.str_save = current_text
        return str

    def replace_by_manage(self, number_str: str):

        attribute_obj = self.allplan.attributes_dict.get(number_str)

        if not isinstance(attribute_obj, AttributeDatas):
            return

        a_type = attribute_obj.option

        # -----------------------------------------------
        # Checkbox
        # -----------------------------------------------

        if a_type == code_attr_chk:
            # Lineedit widget
            self.ui.lineedit_widget.setVisible(False)

            # Combo
            self.ui.combo_widget.setVisible(False)

            # Checkbox
            self.ui.checkbox_widget.setVisible(True)

            return

        # -----------------------------------------------
        # String
        # -----------------------------------------------

        if a_type in [code_attr_str, code_attr_formule_str]:
            # Lineedit widget
            self.ui.lineedit_widget.setVisible(True)

            # Lineedit calendar / help
            self.ui.calendar_bt.setVisible(False)
            self.ui.lineedit_format_bt.setVisible(True)

            # Combo / Checkbox
            self.ui.combo_widget.setVisible(False)
            self.ui.checkbox_widget.setVisible(False)

            # Options
            set_appearence_type(self.ui.lineedit_type, a_type)
            self.ui.lineedit_value.setValidator(None)

            return

        # -----------------------------------------------
        # Integer
        # -----------------------------------------------

        if a_type in [code_attr_int, code_attr_formule_int]:
            # Lineedit widget
            self.ui.lineedit_widget.setVisible(True)

            # Lineedit calendar / help
            self.ui.calendar_bt.setVisible(False)
            self.ui.lineedit_format_bt.setVisible(True)

            # Combo / Checkbox
            self.ui.combo_widget.setVisible(False)
            self.ui.checkbox_widget.setVisible(False)

            # Options
            set_appearence_type(self.ui.lineedit_type, a_type)
            self.ui.lineedit_value.setValidator(ValidatorInt())

            return

        # -----------------------------------------------
        # Float
        # -----------------------------------------------

        if a_type in [code_attr_dbl, code_attr_formule_float]:
            # Lineedit widget
            self.ui.lineedit_widget.setVisible(True)

            # Lineedit calendar / help
            self.ui.calendar_bt.setVisible(False)
            self.ui.lineedit_format_bt.setVisible(True)

            # Combo / Checkbox
            self.ui.combo_widget.setVisible(False)
            self.ui.checkbox_widget.setVisible(False)

            # Options
            set_appearence_type(self.ui.lineedit_type, a_type)
            self.ui.lineedit_value.setValidator(ValidatorDouble())

            return

        # -----------------------------------------------
        # Date
        # -----------------------------------------------

        if a_type == code_attr_date:
            # Lineedit widget
            self.ui.lineedit_widget.setVisible(True)

            # Lineedit calendar / help
            self.ui.calendar_bt.setVisible(True)
            self.ui.lineedit_format_bt.setVisible(False)

            # Combo / Checkbox
            self.ui.combo_widget.setVisible(False)
            self.ui.checkbox_widget.setVisible(False)

            # Options
            set_appearence_type(self.ui.lineedit_type, a_type)

            self.ui.lineedit_value.setValidator(ValidatorDate())
            return

        # -----------------------------------------------
        # Combobox
        # -----------------------------------------------

        if a_type in [code_attr_combo_str_edit, code_attr_combo_float_edit, code_attr_combo_int_edit,
                      code_attr_combo_int]:

            # Lineedit widget
            self.ui.lineedit_widget.setVisible(False)

            # Combo
            self.ui.combo_widget.setVisible(True)

            if "entier" in a_type:
                self.ui.combo_value.setValidator(ValidatorInt())

            elif "décimal" in a_type:
                self.ui.combo_value.setValidator(ValidatorDouble())

            if "modifiable" in a_type:
                self.ui.combo_type.setIcon(get_icon(lock_icon))

                self.ui.combo_type.setToolTip(self.tr("Cette liste déroulante n'est pas éditable"))

                self.ui.combo_value.setValidator(ValidatorModel(model=self.ui.combo_value.model(), column_index=1))

            else:

                self.ui.combo_type.setIcon(get_icon(attribute_editable_icon))

                self.ui.combo_type.setToolTip(self.tr("Cette liste déroulante est éditable"))

                self.ui.combo_value.setValidator(None)

            # Checkbox
            self.ui.checkbox_widget.setVisible(False)

            # enumeration
            combo_model = attribute_obj.enumeration

            self.replace_by_filter.setSourceModel(combo_model)
            self.replace_by_filter.setFilterKeyColumn(1)

            self.ui.combo_value.setModel(combo_model)
            self.ui.combo_value.setModelColumn(1)

            qcompleter = QCompleter()
            qcompleter.setModel(self.replace_by_filter)
            qcompleter.setCompletionColumn(1)
            qcompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            qcompleter.setCaseSensitivity(Qt.CaseInsensitive)

            self.ui.combo_value.setCompleter(qcompleter)

    @staticmethod
    def a___________________replace_by_lineedit_______________():
        pass

    def replace_by_lineedit_changed(self):
        self.replace_buttons_manage()

        if self.ui.lineedit_type.text() == "0.0":
            self.ui.lineedit_value.setText(self.ui.lineedit_value.text().replace(".", ","))

    def formatting_show(self):

        self.formatting_widget.formatting_show(current_parent=self.ui.lineedit_format_bt,
                                               current_code=self.ui.value_search.text(),
                                               current_text=self.ui.lineedit_value.text(),
                                               show_code=False,
                                               show_search=True)

    def lineedit_formatting_changed(self, new_value: str):

        self.ui.lineedit_value.setText(new_value)

    def lineedit_float_formatting(self):

        if self.ui.lineedit_type.text() != "0,0":
            return

        valeur = self.ui.lineedit_value.text()

        if "," in valeur:
            valeur = valeur.replace(",", ".")

        try:
            valeur_decimal = float(valeur)
            valeur = f"{valeur_decimal:.3f}"
        except ValueError:
            pass

        self.ui.lineedit_value.setText(valeur.replace(".", ","))

    @staticmethod
    def a___________________replace_by_date_______________():
        pass

    def calendar_show(self):

        move_widget_ss_bouton(button=self.ui.calendar_bt, widget=self.calendar_widget, left_force=True)

        self.calendar_widget.calendar_loading(self.ui.lineedit_value.text())

    @staticmethod
    def a___________________replace_by_combo_______________():
        pass

    def replace_by_combo_changed(self):

        if self.ui.combo_value.model().rowCount() == 0:
            print("search_replace -- replace_by_combo_changed -- self.ui.combo_value.model().rowCount() == 0")
            return

        if self.ui.combo_value.view().isVisible():
            print("search_replace -- replace_by_combo_changed -- self.ui.combo_value.view().isVisible()")
            return False

        attrib_valeur = self.ui.combo_value.currentText()
        row_index_current = self.ui.combo_value.currentIndex()

        if row_index_current == -1 or attrib_valeur.strip() == "":
            row_index = self.ui.combo_value.findText("", Qt.MatchExactly)
            self.ui.combo_value.setCurrentIndex(row_index)
            self.replace_by_combo_set_index(row_index=row_index)
            return

        search_value = self.ui.combo_value.findText(attrib_valeur, Qt.MatchExactly)

        model = self.replace_by_filter.sourceModel()

        if not isinstance(model, QStandardItemModel):
            print("search_replace -- replace_by_combo_changed -- model is None")
            return

        if search_value == -1:
            search_value = model.rowCount()
            model.appendRow([QStandardItem(f"{search_value}"), QStandardItem(attrib_valeur)])

        search_index_invalid = self.ui.combo_value.findText(self.tr("Index non valide !"), Qt.MatchExactly)

        if search_index_invalid != -1:
            self.ui.combo_value.removeItem(search_index_invalid)

        if search_value != row_index_current:
            qm = model.index(search_value, 0)

            if not qm_check(qm):
                print("search_replace -- replace_by_combo_changed -- not qm_check(qm)")
                return

            index_txt = qm.data()

        else:
            qm = model.index(row_index_current, 0)

            if not qm_check(qm):
                print("search_replace -- replace_by_combo_changed -- not qm_check(qm)")
                return

            index_txt = qm.data()

        self.ui.combo_index.setText(index_txt)

    def replace_by_combo_set_index(self, row_index: int):

        if row_index == -1:
            self.ui.combo_index.setText("-1")
            return

        model = self.replace_by_filter.sourceModel()

        qm: QModelIndex = model.index(row_index, 0)

        if not qm_check(qm):
            print("search_replace -- replace_by_combo_set_index -- not qm_check(qm)")
            return

        index_txt = qm.data()

        self.ui.combo_index.setText(index_txt)

    @staticmethod
    def a___________________replace_by_library_______________():
        pass

    def library_show(self):

        self.library_widget.show_library(current_qs=QStandardItem(),
                                         current_parent=self,
                                         current_mode="Replace")

    def library_changed(self, number: str, new_value: str):

        self.attribute_changed(number_str=number)

        if self.ui.lineedit_widget.isVisible():
            self.ui.lineedit_value.setText(new_value)
            return

        if self.ui.combo_widget.isVisible():

            row_index = self.ui.combo_value.findText(new_value, Qt.MatchExactly)

            if row_index == -1:
                return

            self.ui.combo_value.setCurrentIndex(row_index)

            return

        if self.ui.checkbox_widget.isVisible():
            self.ui.checkbox_value.setChecked(new_value == "1")

    @staticmethod
    def a___________________search_______________():
        pass

    def search_launch(self, message_show=True):

        # -------------------------------------------
        # clear datas
        # -------------------------------------------

        self.results_clear()

        self.paths_dict.clear()

        # -------------------------------------------
        # Value search
        # -------------------------------------------

        value_search = self.ui.value_search.text()

        if value_search == "":
            self.replace_buttons_manage()
            print("search_replace -- search_launch -- value_search empty")
            return

        # -------------------------------------------
        # number & type object & Icon
        # -------------------------------------------

        number_search = self.get_combo_current_number()

        if number_search == attribut_default_obj.current:

            if self.ui.component_bt.isChecked():
                obj_type = Component
                icon_name = "component"

            else:
                obj_type = Material
                icon_name = "material"

        else:
            obj_type = Attribute

            if self.ui.component_bt.isChecked():
                icon_name = "component"
            else:
                icon_name = "material"

        # -------------------------------------------
        # search
        # -------------------------------------------

        search_qs_list = self.hierarchy.cat_model.findItems(value_search,
                                                            Qt.MatchExactly | Qt.MatchRecursive,
                                                            col_cat_value)

        if len(search_qs_list) == 0:
            if self.isVisible() and message_show:
                msg(titre=self.windowTitle(),
                    message=self.tr("Aucun élément n'a été trouvé"),
                    type_bouton=QMessageBox.Ok)
            else:
                print("search_replace -- search_launch -- no result")

            self.replace_buttons_manage()
            return

        # -------------------------------------------
        # Save search datas
        # -------------------------------------------

        for qs in search_qs_list:

            qs: MyQstandardItem

            if not isinstance(qs, obj_type):
                continue

            if obj_type == Attribute:

                qs_current = qs.parent()

                if self.ui.component_bt.isChecked():
                    if not isinstance(qs_current, Component):
                        continue

                elif not isinstance(qs_current, Material):
                    continue

                child_row = qs.row()

                qs_number = qs_current.child(child_row, col_cat_number)

                if not isinstance(qs_number, Info):
                    print("search_replace -- search_launch -- not isinstance(qs_number, Info)")
                    continue

                number_current = qs_number.text()

            else:

                qs_current = qs
                number_current = attribut_default_obj.current

            if number_current != number_search:
                continue

            name_current = qs_current.text()

            current_path = self.get_path_txt(qs=qs_current, current_path=name_current)

            if not isinstance(current_path, str):
                print("search_replace -- search_launch -- not isinstance(current_path, str)")
                continue

            qs_icon = QStandardItem()
            qs_icon.setIcon(get_icon(f":/Images/{icon_name}.png"))

            self.paths_dict[current_path] = qs_current

            self.results_model.appendRow([qs_icon, QStandardItem(current_path)])

        # -------------------------------------------
        # Buttons manage
        # -------------------------------------------

        self.replace_buttons_manage()

        model_row_count = self.results_model.rowCount()

        if model_row_count == 0:
            if self.isVisible() and message_show:
                msg(titre=self.windowTitle(),
                    message=self.tr("Aucun élément n'a été trouvé"),
                    type_bouton=QMessageBox.Ok)
            else:

                print("search_replace -- search_launch -- no result")

            return

    def get_path_txt(self, qs: MyQstandardItem, current_path: str) -> str:

        qs_parent = qs.parent()

        if not isinstance(qs_parent, QStandardItem):
            return current_path

        if qs_parent == self.hierarchy.cat_model.invisibleRootItem():
            return current_path

        current_path = f"{qs_parent.text()}\\{current_path}"

        return self.get_path_txt(qs=qs_parent, current_path=current_path)

    def show_selected_qs(self, qm: QModelIndex):

        if not qm_check(qm):
            print("search_replace -- show_selected_qs -- not qm_check(qm)")
            return

        path_current = qm.data()

        if path_current not in self.paths_dict:
            print("search_replace -- show_selected_qs -- path_current not in self.paths_dict")
            return

        qs = self.paths_dict[path_current]

        if not isinstance(qs, MyQstandardItem):
            print("search_replace -- show_selected_qs -- not isinstance(qs, MyQstandardItem)")
            return

        if isinstance(qs, Attribute):
            qs = qs.parent()

        if not isinstance(qs, Material) and not isinstance(qs, Component):
            print("search_replace -- show_selected_qs -- not isinstance(Material) and not isinstance(Component)")
            return

        self.hierarchy.select_list([qs])

    def replace_menu_show(self, point: QPoint):

        qm = self.ui.results_view.indexAt(point)

        point = QPoint(point.x(), point.y() + 35)

        if not qm_check(qm):
            print("search_replace -- replace_menu_show -- not qm_check(qm)")
            return

        menu = MyContextMenu()

        menu.add_title(title=self.windowTitle())

        menu.add_action(qicon=get_icon(hierarchy_show_item_icon),
                        title=self.tr("Voir l'élément dans la hiérarchie"),
                        action=lambda: self.show_selected_qs(qm))

        menu.add_action(qicon=get_icon(text_copy_icon),
                        title=self.tr("Copier le chemin dans le presse-papier"),
                        action=lambda: copy_to_clipboard(qm.data()))

        menu.exec_(self.ui.results_view.mapToGlobal(point))

    @staticmethod
    def a___________________results_______________():
        """ Partie réservée à la gestion de l'ajout ou suppression des favoris"""
        pass

    def results_clear(self):
        self.results_model.clear()

        self.results_model.setHorizontalHeaderLabels(["", self.tr("Chemin")])

        self.ui.results_view.setColumnWidth(col_icon, 30)

        self.replace_buttons_manage()

    def replace_selected(self):

        # -------------------------------------------
        # Model count
        # -------------------------------------------

        results_count = self.results_model.rowCount()

        if results_count == 0:
            print("search_replace -- replace_selected -- no result")
            return

        # -------------------------------------------
        # Selection
        # -------------------------------------------

        qm_selection_list = self.ui.results_view.selectionModel().selectedRows(col_path)

        if len(qm_selection_list) == 0:
            print("search_replace -- replace_selected -- len(qm_selection_list) == 0")
            return

        self.replace_action(qm_selection_list=qm_selection_list)

    def replace_all(self):

        # -------------------------------------------
        # Model count
        # -------------------------------------------

        results_count = self.results_model.rowCount()

        if results_count == 0:
            print("search_replace -- replace_all -- no result")
            return

        if results_count > 1:

            if msg(titre=self.windowTitle(),
                   message=self.tr("Voulez - vous vraiment remplacer tous les éléments?"),
                   type_bouton=QMessageBox.Ok | QMessageBox.Cancel,
                   defaut_bouton=QMessageBox.Cancel,
                   icone_avertissement=True) != QMessageBox.Ok:
                return

        qm_selection_list = [self.results_model.index(row_index, col_path) for row_index in range(results_count)]

        self.replace_action(qm_selection_list=qm_selection_list)

    def replace_action(self, qm_selection_list: list):

        # -------------------------------------------
        # Number & type object
        # -------------------------------------------

        number = self.get_combo_current_number()

        if number == attribut_default_obj.current:

            if self.ui.component_bt.isChecked():

                obj_type = Component

            else:
                obj_type = Material

        else:

            obj_type = Attribute

        # -------------------------------------------
        # Values & index
        # -------------------------------------------

        value_search = self.ui.value_search.text()

        if self.ui.checkbox_widget.isVisible():
            value_index = "-1"

            if self.ui.checkbox_value.isChecked():
                value_replace = "1"
            else:
                value_replace = "0"

        elif self.ui.lineedit_widget.isVisible():
            value_index = "-1"
            value_replace = self.ui.lineedit_value.text()

        elif self.ui.combo_widget.isVisible():
            value_index = self.ui.combo_index.text()
            value_replace = self.ui.combo_value.currentText()

        else:
            print("search_replace -- replace_action -- No widget found")
            return

        if value_search == value_replace or value_search is None or value_replace is None:
            print("search_replace -- replace_action -- value error")
            return

        if value_search == "" or value_replace == "":
            print("search_replace -- replace_action -- value empty")
            return

        # -------------------------------------------
        # replace
        # -------------------------------------------

        ok_list = list()
        errors_list = list()

        qs_catalog_selected = self.hierarchy.get_current_qs()

        for qm in qm_selection_list:

            qm: QModelIndex

            # if qm.column() != col_path:
            #     qm = self.results_model.index(qm.row(), col_path)

            if not qm_check(qm):
                print("search_replace -- replace_action -- not qm_check(qm)")
                errors_list.append("error qm")
                continue

            path_current = qm.data()

            if path_current not in self.paths_dict:
                print("search_replace -- replace_action -- path_current not in dict !")
                errors_list.append(path_current)
                return False

            qs: MyQstandardItem = self.paths_dict[path_current]

            if not isinstance(qs, MyQstandardItem):
                print(f"search_replace -- replace_action -- not isinstance(qs, MyQstandardItem)")
                errors_list.append(path_current)
                return False

            # -------------------------------------------
            # replace attribute
            # -------------------------------------------

            if obj_type is Attribute and (isinstance(qs, Material) or isinstance(qs, Component)):

                qs_attributes_list = qs.get_attribute_line_by_number(number=number)

                if len(qs_attributes_list) == 0:
                    print(f"search_replace -- replace_action -- len(qs_attributes_list) == 0")
                    errors_list.append(path_current)
                    continue

                qs_value = qs_attributes_list[col_cat_value]

                if not isinstance(qs_value, Attribute):
                    print(f"search_replace -- replace_action -- not isinstance(qs_value, Attribute)")
                    errors_list.append(path_current)
                    continue

                value_current = qs_value.text()

                if value_current != value_search:
                    print(f"search_replace -- replace_action -- value_current != value_search")
                    errors_list.append(path_current)
                    continue

                qs_index = qs_attributes_list[col_cat_index]

                if not isinstance(qs_index, Info):
                    print(f"search_replace -- replace_action -- not isinstance(qs_index, Info)")
                    errors_list.append(path_current)
                    continue

                index_current = qs_index.text()

                if index_current != value_index:
                    qs_index.setText(value_index)

                if number != "207":
                    qs_value.setText(value_replace)
                    ok_list.append(path_current)

                    if qs_catalog_selected == qs:
                        qm_catalog = qs.index()
                        self.hierarchy.select_list(selected_list=[qm_catalog], scrollto=False)
                    continue

                qs_parent = qs.parent()

                if not isinstance(qs_parent, MyQstandardItem):
                    print(f"search_replace -- replace_action -- not isinstance(qs_parent, MyQstandardItem)")
                    errors_list.append(path_current)
                    continue

                row_index = qs.row()

                qs_desc = qs_parent.child(row_index, col_cat_desc)

                if not isinstance(qs_desc, Info):
                    print(f"search_replace -- replace_action -- not isinstance(qs_description, Info)")
                    errors_list.append(path_current)
                    continue

                qs_value.setText(value_replace)
                qs_desc.setText(value_replace)
                ok_list.append(path_current)

                if qs_catalog_selected == qs:
                    qm_catalog = qs.index()
                    self.hierarchy.select_list(selected_list=[qm_catalog], scrollto=False)

                continue

            # -------------------------------------------
            # replace Material / Component code
            # -------------------------------------------

            qs.setText(value_replace)

            if qs_catalog_selected == qs:
                qm_catalog = qs.index()
                self.hierarchy.select_list(selected_list=[qm_catalog], scrollto=False)

            continue

        # -------------------------------------------
        # End - Message
        # -------------------------------------------

        self.catalog.change_made = True

        self.show_end_message(ok_list=ok_list, error_list=errors_list)

        # -------------------------------------------
        # Clear All item to results list
        # -------------------------------------------

        if len(qm_selection_list) == self.results_model.rowCount():
            self.results_clear()
            self.paths_dict.clear()
            return

        # -------------------------------------------
        # Clear selected item to results list
        # -------------------------------------------

        for qm_remove in reversed(qm_selection_list):

            if not qm_check(qm_remove):
                print(f"search_replace -- replace_action -- not qm_check(qm_remove)")
                return

            value_remove = qm_remove.data()

            if value_remove not in self.paths_dict:
                print(f"search_replace -- replace_action -- value_remove not in self.paths_dict")
                return

            self.results_model.removeRow(qm_remove.row())
            self.paths_dict.pop(value_remove)

    def show_end_message(self, ok_list: list, error_list: list):

        if len(error_list) == 0:

            value_txt = self.tr("La valeur")
            replace_txt = self.tr("a correctement été remplacé par")

            msg(titre=self.windowTitle(),
                message=f"{value_txt} {replace_txt}",
                type_bouton=QMessageBox.Ok,
                icone_valide=True,
                details=ok_list)

        else:

            ok_txt = "\n - ".join(ok_list)
            error_txt = "\n - ".join(error_list)

            value_txt = self.tr("Réussite")
            replace_txt = self.tr("Echec")

            details = f'{value_txt} : \n' \
                      f'{ok_txt}\n\n' \
                      f'{replace_txt} : \n' \
                      f'{error_txt}'

            error_txt = self.tr("Une ou des erreurs ont été détectées")
            info_txt = self.tr("Afficher les détails pour plus d'informations")

            msg(titre=self.windowTitle(),
                message=f"{error_txt}! \n{info_txt}",
                type_bouton=QMessageBox.Ok,
                icone_critique=True,
                details=details)

    @staticmethod
    def a___________________buttons_______________():
        pass

    def replace_buttons_manage(self):

        if not self.isVisible():
            return

        search_on = ("QPushButton{"
                     "border: 1px solid #8f8f91; "
                     "border-radius: 5px ; "
                     "padding-right: 10px; "
                     "padding-left: 10px; "
                     "background-color: "
                     "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
                     "QPushButton:hover{background-color: "
                     "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
                     "QPushButton:pressed{background-color: "
                     "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")

        search_off = ("QPushButton{"
                      "border: 2px solid orange; "
                      "border-radius: 5px ; "
                      "padding-right: 10px; "
                      "padding-left: 10px; "
                      "background-color: "
                      "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
                      "QPushButton:hover{background-color: "
                      "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
                      "QPushButton:pressed{background-color: "
                      "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")

        search_not_empty = self.ui.value_search.text() == "" and self.ui.lineedit_value.text() == ""

        if search_not_empty:
            self.ui.search_bt.setEnabled(False)
            self.ui.search_bt.setStyleSheet(search_on)
            self.ui.library_show_bt.setEnabled(False)
            self.ui.replace_bt.setEnabled(False)
            self.ui.replace_all_bt.setEnabled(False)
            return

        if self.ui.attribute_combo.currentText() == "":
            self.ui.search_bt.setEnabled(False)
            self.ui.search_bt.setStyleSheet(search_on)
            self.ui.replace_bt.setEnabled(False)
            self.ui.replace_all_bt.setEnabled(False)
            return

        search_not_empty = self.ui.value_search.text() != ""

        self.ui.search_bt.setEnabled(search_not_empty)

        if search_not_empty and self.results_model.rowCount() == 0:
            self.ui.search_bt.setStyleSheet(search_off)
        else:
            self.ui.search_bt.setStyleSheet(search_on)

        self.ui.library_show_bt.setEnabled(search_not_empty)

        if self.results_model.rowCount() == 0:
            self.ui.replace_bt.setEnabled(False)
            self.ui.replace_all_bt.setEnabled(False)
            return

        if self.ui.lineedit_value.text() == "" and self.ui.lineedit_widget.isVisible():
            self.ui.replace_bt.setEnabled(False)
            self.ui.replace_all_bt.setEnabled(False)
            return

        if self.ui.combo_value.currentText() == "" and self.ui.combo_widget.isVisible():
            self.ui.replace_bt.setEnabled(False)
            self.ui.replace_all_bt.setEnabled(False)
            return

        self.ui.replace_all_bt.setEnabled(True)

        qm_selection_list = self.ui.results_view.selectionModel().selectedRows(0)

        if len(qm_selection_list) == 0:
            self.ui.replace_bt.setEnabled(False)
            return

        self.ui.replace_bt.setEnabled(True)

    @staticmethod
    def a___________________save_______________():
        pass

    def replace_settings_save(self):

        datas_config = settings_read(file_name=replace_setting_file)

        # -----------------------------------------------

        datas_config["replace_by"] = self.ui.lineedit_value.text()

        # -----------------------------------------------

        if self.ui.component_bt.isChecked():
            datas_config["ele_type"] = component_code
        else:
            datas_config["ele_type"] = material_code

        # -----------------------------------------------

        datas_config["attribute"] = self.get_combo_current_number()

        # -----------------------------------------------

        datas_config["attributes_list"] = self.get_combo_numbers_list()

        # -----------------------------------------------

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True

                settings_save(file_name=replace_setting_file, config_datas=datas_config)
                return

        datas_config["height"] = self.size().height()
        datas_config["width"] = self.size().width()
        datas_config["ismaximized_on"] = False

        # -----------------------------------------------

        settings_save(file_name=replace_setting_file, config_datas=datas_config)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            self.close()
            return

    def changeEvent(self, event: QEvent):

        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.ismaximized_on = True

            else:
                self.ismaximized_on = False
                move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent):

        self.replace_settings_save()

        super().closeEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj != self.ui.combo_value:
            return super().eventFilter(obj, event)

        if not isinstance(obj, QComboBox):
            return super().eventFilter(obj, event)

        if obj.view().isVisible():
            return super().eventFilter(obj, event)

        if event.type() == QEvent.FocusOut:
            self.replace_by_combo_changed()
            return super().eventFilter(obj, event)

        if event.type() == QEvent.Wheel:
            if not self.ui.combo_value.hasFocus():
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

    @staticmethod
    def a___________________end______():
        pass
