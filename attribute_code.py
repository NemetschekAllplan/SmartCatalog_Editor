#!/usr/bin/python3
# -*- coding: utf-8 -*
from allplan_manage import AttributeDatas
from formatting_widget import Formatting
from hierarchy import MyQstandardItem, Material, Component
from history_manage import AttributeModifyData
from main_datas import *
from tools import afficher_message as msg
from tools import set_appareance_button
from ui_attribute_code import Ui_AttributeCode


class AttributeCode(QWidget):
    code_changed_signal = pyqtSignal(str, str)
    attribute_changed_signal = pyqtSignal(str, list, str, dict)

    attribute_defaul_signal = pyqtSignal()

    def __init__(self, qs_value: MyQstandardItem, material_linked: bool, forbidden_names_list: list,
                 attribute_obj: AttributeDatas):
        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeCode()
        self.ui.setupUi(self)

        set_appareance_button(self.ui.formatting_bt)

        # ----------------------------------

        if isinstance(attribute_obj, AttributeDatas):

            if attribute_obj.number != "":

                self.ui.num_attrib.setToolTip(attribute_obj.tooltips)
                self.ui.name_attrib.setToolTip(attribute_obj.tooltips)

            # ----------------------------------

            if isinstance(qs_value, Material):

                self.ui.num_attrib.setIcon(get_icon(material_icon))

            elif isinstance(qs_value, Component):

                self.ui.num_attrib.setIcon(get_icon(component_icon))

            else:

                self.ui.num_attrib.setIcon(get_icon(error_icon))

        # ----------------------------------

        else:

            self.ui.num_attrib.setIcon(get_icon(error_icon))

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.qs_value = qs_value
        self.ui.value_attrib.setText(self.qs_value.text())

        self.material_linked = material_linked
        self.forbidden_names_list = forbidden_names_list

        # -----------------------------------------------
        # Formatting
        # -----------------------------------------------

        self.formatting_widget = Formatting()
        self.formatting_widget.save_modif_formatage.connect(self.formatting_changed)

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.value_attrib.textChanged.connect(self.code_loading)
        self.ui.value_attrib.editingFinished.connect(self.code_check_end)

        self.ui.formatting_bt.clicked.connect(self.formatting_show)

        self.ui.verification_bt.clicked.connect(self.verification_show_msg)

        self.ui.num_attrib.clicked.connect(self.attribute_defaul_signal.emit)

        # -----------------------------------------------
        # Loading
        # -----------------------------------------------

        self.code_loading()

        # ------------------------

    @staticmethod
    def a___________________code_loading______():
        pass

    def code_loading(self):

        value = self.ui.value_attrib.text().strip()
        value_original = self.qs_value.text()

        self.ui.formatting_bt.setEnabled(value != "")

        if value == "":
            self.ui.verification_bt.setIcon(get_icon(error_icon))
            self.ui.verification_bt.setToolTip(self.tr("Impossible de laisser ce titre sans texte."))

            self.ui.value_attrib.setStyleSheet("QLineEdit{padding-left: 5px; "
                                               "border: 2px solid orange; "
                                               "border-top-left-radius:5px; "
                                               "border-bottom-left-radius: 5px; }")

            return

        if value.upper() in self.forbidden_names_list and value.upper() != value_original.upper():
            self.ui.verification_bt.setIcon(get_icon(error_icon))

            self.ui.verification_bt.setToolTip(self.tr("Ce titre est déjà utilisé."))

            self.ui.value_attrib.setStyleSheet("QLineEdit{padding-left: 5px; "
                                               "border: 2px solid orange; "
                                               "border-top-left-radius:5px; "
                                               "border-bottom-left-radius: 5px; }")

            return

        self.ui.verification_bt.setIcon(get_icon(valid_icon))

        self.ui.verification_bt.setToolTip(self.tr("C'est tout bon!"))

        self.ui.value_attrib.setStyleSheet("QLineEdit{padding-left: 5px; "
                                           "border: 1px solid #8f8f91; "
                                           "border-right-width: 0px; "
                                           "border-top-left-radius:5px; "
                                           "border-bottom-left-radius: 5px; }")

    def code_check_end(self):
        self.code_check_before_update(value_new=self.ui.value_attrib.text())

    def code_check_before_update(self, value_new: str):

        value_current = self.qs_value.text()

        if value_new != value_new.strip():
            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(value_new.strip())
            self.ui.value_attrib.blockSignals(False)
            value_new = value_new.strip()

        # -------------

        if value_new == "":
            msg(titre=application_title,
                message=self.tr("Impossible de laisser ce titre sans texte."),
                icone_critique=True)

            self.ui.value_attrib.setText(value_current)
            return

        if value_new.upper() in self.forbidden_names_list and value_new.upper() != value_current.upper():
            msg(titre=application_title,
                message=self.tr("Ce titre est déjà utilisé."),
                icone_critique=True)

            self.ui.value_attrib.setText(value_current)
            return

        if value_current == value_new:
            return

        # -------------

        if value_current.upper() in self.forbidden_names_list:
            self.forbidden_names_list.remove(value_current.upper())
            self.forbidden_names_list.append(value_new.upper())

        # -------------

        self.code_changed_signal.emit(value_current, value_new)

        # -------------

        self.qs_value.setText(value_new)

        # -------------

        number_current = self.ui.num_attrib.text()

        value_dict = {number_current: [value_current, value_new]}

        # -------------

        guid_parent = self.qs_value.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_code -- code_check_before_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = self.qs_value.text()

        if not isinstance(parent_name, str):
            print("attribute_code -- code_check_before_update -- not isinstance(parent_name, str)")
            return

        # -------------

        data = AttributeModifyData(number_current=number_current, value_new=value_current)

        attribute_data = [data]

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict)

    @staticmethod
    def a___________________formatting______():
        pass

    def formatting_show(self):
        self.formatting_widget.formatting_show(current_parent=self.ui.formatting_bt,
                                               current_text=self.ui.value_attrib.text(),
                                               show_code=False)

    def formatting_changed(self, new_text: str):

        self.ui.value_attrib.setText(new_text)
        self.code_check_before_update(value_new=new_text)

    @staticmethod
    def a___________________verification_msg______():
        pass

    def verification_show_msg(self):

        tooltip = self.ui.verification_bt.toolTip()

        if tooltip == self.tr("C'est tout bon!"):

            msg(titre=application_title,
                message=self.tr("Ce titre est correct, pas de soucis!"),
                icone_valide=True)

        else:

            msg(titre=application_title,
                message=f"{tooltip}",
                icone_critique=True)

    @staticmethod
    def a___________________end______():
        pass
