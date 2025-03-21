#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.QtWidgets import QWidget

from allplan_manage import AttributeDatas
from tools import set_appearance_number
from ui_attribute_unknown import Ui_AttributeUnknown


class AttributeUnknown(QWidget):

    def __init__(self, attribute_obj: AttributeDatas, value: str):
        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeUnknown()
        self.ui.setupUi(self)

        # ------------

        if isinstance(attribute_obj, AttributeDatas):
            self.ui.num_attrib.setText(attribute_obj.number)

            # ------------

            self.ui.name_attrib.setText(attribute_obj.name)
            self.ui.name_attrib.setToolTip(attribute_obj.tooltips)

        # ------------

        set_appearance_number(self.ui.num_attrib)
        self.ui.value_attrib.setText(value)

        # ------------
