#!/usr/bin/python3
# -*- coding: utf-8 -*
from allplan_manage import AttributeDatas
from hierarchy import MyQstandardItem
from history_manage import AttributeModifyData
from main_datas import *
from tools import ValidatorInt, ValidatorDouble, format_float_value
from tools import set_appearance_number, set_appearence_type
from ui_attribute_lineedit import Ui_AttributeLineedit


class AttributeLineedit(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict)

    def __init__(self, allplan_version: str,
                 qs_value: MyQstandardItem,
                 attribute_obj: AttributeDatas,
                 is_material=False):

        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeLineedit()
        self.ui.setupUi(self)

        self.allplan_version = allplan_version

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.qs_value = qs_value
        self.ui.value_attrib.setText(self.qs_value.text())
        self.ui.value_attrib.home(False)

        # ----------------------------------

        if isinstance(attribute_obj, AttributeDatas):

            self.attrib_option = attribute_obj.option

            self.unit_attrib = attribute_obj.unit

            if is_material:
                min_value = attribute_obj.min_val
                max_value = attribute_obj.max_val

            else:

                min_value = -2147483648
                max_value = 2147483647

            self.ui.num_attrib.setText(attribute_obj.number)

            self.ui.name_attrib.setText(attribute_obj.name)
            self.ui.name_attrib.setToolTip(attribute_obj.tooltips)

        else:

            self.attrib_option = code_attr_str

            self.unit_attrib = ""

            min_value = -2147483648
            max_value = 2147483647

        # ----------------------------------

        if not isinstance(min_value, str):

            self.min_value = None

        else:

            try:

                self.min_value = int(min_value)

            except Exception:

                self.min_value = None

        # ----------------------------------

        if not isinstance(max_value, str):

            self.max_value = None

        else:

            try:

                self.max_value = int(max_value)

            except Exception:

                self.max_value = None

        # ----------------------------------

        if self.unit_attrib != "":
            self.ui.unit_attrib.setText(self.unit_attrib)

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.value_attrib.textChanged.connect(self.lineedit_changed)
        self.ui.value_attrib.editingFinished.connect(self.lineedit_float_formatting)
        self.ui.value_attrib.installEventFilter(self)

        # -----------------------------------------------

    @staticmethod
    def a___________________lineedit_loading______():
        pass

    def lineedit_loading(self):

        set_appearance_number(self.ui.num_attrib)
        set_appearence_type(self.ui.type_attrib, self.attrib_option)

        self.ui.unit_attrib.setVisible(self.unit_attrib != "")

        if self.unit_attrib == "":
            self.ui.value_attrib.setStyleSheet("QLineEdit{"
                                               "padding-left: 5px;"
                                               "border: 1px solid #8f8f91;"
                                               "border-radius:5px}")

        if self.attrib_option == code_attr_int:
            self.ui.value_attrib.setValidator(ValidatorInt(min_val=self.min_value, max_val=self.max_value))
            return

        if self.attrib_option == code_attr_dbl:
            self.ui.value_attrib.setValidator(ValidatorDouble(min_val=self.min_value, max_val=self.max_value))
            return

    @staticmethod
    def a___________________changement______():
        pass

    def lineedit_changed(self):

        if self.attrib_option != code_attr_dbl:
            return

        current_text = self.ui.value_attrib.text()

        if self.allplan_version in ["2022", "2023"]:
            value = current_text.replace(".", ",")
        else:
            value = current_text.replace(",", ".")

        if value != current_text:
            cursor_position = self.ui.value_attrib.cursorPosition()

            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(value)
            self.ui.value_attrib.blockSignals(False)

            self.ui.value_attrib.setCursorPosition(cursor_position)

    def lineedit_float_formatting(self):

        if self.attrib_option != code_attr_dbl:
            self.lineedit_update()
            return

        current_text = self.ui.value_attrib.text()

        value = format_float_value(value=current_text, allplan_version=self.allplan_version)

        if value != current_text:
            cursor_position = self.ui.value_attrib.cursorPosition()

            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(value)
            self.ui.value_attrib.blockSignals(False)

            self.ui.value_attrib.setCursorPosition(cursor_position)

        self.lineedit_update()

    def lineedit_update(self):

        value_current = self.qs_value.text()
        value_new = self.ui.value_attrib.text()

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
            print("attribute_lineedit -- lineedit_update -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_lineedit -- lineedit_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_lineedit -- lineedit_update -- not isinstance(parent_name, str)")
            return

        # -------------

        data = AttributeModifyData(number_current=number_current, value_new=value_current)

        attribute_data = [data]

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict)

    @staticmethod
    def a___________________end______():
        pass
