#!/usr/bin/python3
# -*- coding: utf-8 -*
from allplan_manage import AttributeDatas
from hierarchy import MyQstandardItem
from history_manage import AttributeModifyData
from main_datas import *
from tools import set_appearance_number
from ui_attribute_checkbox import Ui_AttributeCheckbox


class AttributeCheckbox(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict)

    def __init__(self, qs_value: MyQstandardItem, attribute_obj: AttributeDatas):
        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeCheckbox()
        self.ui.setupUi(self)

        # ----------------------------------

        if isinstance(attribute_obj, AttributeDatas):
            self.ui.num_attrib.setText(attribute_obj.number)

            self.ui.name_attrib.setText(attribute_obj.name)
            self.ui.name_attrib.setToolTip(attribute_obj.tooltips)

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.qs_value = qs_value
        valeur_qs = qs_value.text()

        if valeur_qs == "1":
            self.ui.value_attrib.setChecked(True)

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.value_attrib.clicked.connect(self.checkbox_update)

        # -----------------------------------------------

    @staticmethod
    def a___________________checkbox_loading______():
        pass

    def checkbox_loading(self):

        set_appearance_number(self.ui.num_attrib)

    @staticmethod
    def a___________________checkbox_update______():
        pass

    def checkbox_update(self):

        value_current = self.qs_value.text()

        if self.ui.value_attrib.isChecked():
            value_new = "1"
        else:
            value_new = "0"

        if value_current == value_new:
            return

        self.qs_value.setText(value_new)

        # -------------

        number_current = self.ui.num_attrib.text()

        value_dict = {number_current: [value_current, value_new]}

        # -------------

        qs_parent = self.qs_value.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_checkbox -- checkbox_update -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_checkbox -- checkbox_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_checkbox -- checkbox_update -- not isinstance(parent_name, str)")
            return

        # -------------

        data = AttributeModifyData(number_current=number_current, value_new=value_current)

        attribute_data = [data]

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict)

    @staticmethod
    def a___________________end______():
        pass
