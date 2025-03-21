#!/usr/bin/python3
# -*- coding: utf-8 -*

import os.path

from allplan_manage import AllplanDatas, AllplanPaths
from formatting_widget import Formatting
from hierarchy import Folder
from main_datas import *
from history_manage import AttributeModifyData
from tools import afficher_message as msg, MyContextMenu
from tools import get_most_used, get_lastest_used, get_image_dimensions
from tools import set_appareance_button, find_global_point, browser_file
from ui_attribute_name import Ui_AttributeName


class AttributeName(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict)
    icon_changed_signal = pyqtSignal(QStandardItem)

    def __init__(self, allplan: AllplanDatas, qs_value: Folder, qs_selection_list: list):

        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeName()
        self.ui.setupUi(self)

        set_appareance_button(self.ui.formatting_bt)

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.allplan: AllplanDatas = allplan

        self.qs_value = qs_value
        self.ui.value_attrib.setText(self.qs_value.text())

        self.ui.icon_folder.setIcon(get_icon(self.qs_value.icon_path))

        self.qs_selection_list = qs_selection_list

        if self.qs_selection_list is not None:
            self.ui.value_attrib.setEnabled(False)
            self.ui.verification_bt.setEnabled(False)
            self.ui.formatting_bt.setEnabled(False)

        # -----------------------------------------------
        # Formatting
        # -----------------------------------------------

        self.formatting_widget = Formatting()
        self.formatting_widget.save_modif_formatage.connect(self.formatting_changed)

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.icon_folder.clicked.connect(self.icon_menu_show)
        self.ui.icon_folder.customContextMenuRequested.connect(self.icon_menu_show)

        self.ui.value_attrib.textChanged.connect(self.name_loading)
        self.ui.value_attrib.editingFinished.connect(self.name_check_end)

        self.ui.formatting_bt.clicked.connect(self.formatting_show)

        self.ui.verification_bt.clicked.connect(self.verification_show_msg)

        # -----------------------------------------------
        # Loading
        # -----------------------------------------------

        self.name_loading()

        # -----------------------------------------------

    @staticmethod
    def a___________________name_loading______():
        pass

    def name_loading(self):

        value = self.ui.value_attrib.text().strip()

        self.ui.formatting_bt.setEnabled(value != "")

        if value == "":
            self.ui.verification_bt.setIcon(get_icon(error_icon))
            self.ui.verification_bt.setToolTip(self.tr("Impossible de laisser ce titre sans texte."))

            self.ui.value_attrib.setStyleSheet("QLineEdit{padding-left: 5px; "
                                               "border: 1px solid orange; "
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

    def name_check_end(self):
        self.name_check_before_update(value_new=self.ui.value_attrib.text())

    def name_check_before_update(self, value_new: str):

        value_current = self.qs_value.text()

        if value_new != value_new.strip():
            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(value_new.strip())
            self.ui.value_attrib.blockSignals(False)
            value_new = value_new.strip()

        if value_new == "":
            msg(titre=application_title,
                message=self.tr("Impossible de laisser ce titre sans texte."),
                icone_critique=True)

            self.ui.value_attrib.setText(value_current)
            return

        if value_current == value_new:
            return

        self.qs_value.setText(value_new)

        # -------------

        value_dict = {attribut_default_obj.current: [value_current, value_new]}

        # -------------

        guid_parent = self.qs_value.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_name -- name_check_before_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = self.qs_value.text()

        if not isinstance(parent_name, str):
            print("attribute_name -- name_check_before_update -- not isinstance(parent_name, str)")
            return

        # -------------

        data = AttributeModifyData(number_current=attribut_default_obj.current, value_new=value_current)

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
        self.name_check_before_update(new_text)

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
    def a___________________icon_manage______():
        pass

    def icon_browse(self):

        nom_fichier = os.path.basename(self.qs_value.icon_path)

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [icons_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[app_setting_file, "path_icons"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={self.tr("Image"): [".png"]},
                                 current_path=self.qs_value.icon_path,
                                 default_path=icons_path,
                                 file_name=nom_fichier,
                                 use_setting_first=False)

        if file_path == "":
            return

        if not get_image_dimensions(file_path):
            return

        self.icon_changed(file_path=file_path)

    def icon_changed(self, file_path: str):

        if not isinstance(self.qs_value, Folder):
            return

        self.allplan.recent_icons_list.append(file_path)

        self.ui.icon_folder.setIcon(get_icon(file_path))

        self.allplan.icon_list.append(file_path)
        self.allplan.recent_icons_list.append(file_path)

        if self.qs_selection_list is None:
            self.icon_changed_signal.emit(self.qs_value)

            self.qs_value.icon_path = file_path
            self.qs_value.setIcon(get_icon(file_path))
            return

        for qs_value in self.qs_selection_list:

            if not isinstance(qs_value, Folder):
                continue

            self.icon_changed_signal.emit(qs_value)

            qs_value.icon_path = file_path
            qs_value.setIcon(get_icon(file_path))

    @staticmethod
    def a___________________icon_menu______():
        pass

    def icon_menu_show(self):

        menu = MyContextMenu()  # No help

        point = find_global_point(self.ui.icon_folder)

        menu.add_title(title=self.tr("Gestion Icône"))

        menu.add_action(qicon=get_icon(folder_icon),
                        title=self.tr("Remettre icône Dossier"),
                        action=self.icon_reset)

        menu.add_action(qicon=get_icon(none_icon),
                        title=self.tr("Aucun icône"),
                        action=self.icon_none)

        menu.addSeparator()

        menu.add_action(qicon=get_icon(browser_icon),
                        title=self.tr("Parcourir icône"),
                        action=self.icon_browse)

        if len(self.allplan.icon_list) == 0:
            menu.exec_(point)
            return

        recent_icons_list = get_lastest_used(self.allplan.recent_icons_list)
        recent_count = len(recent_icons_list)

        most_used_list = get_most_used(self.allplan.icon_list)
        most_used_count = len(most_used_list)

        if recent_count + most_used_count != 0:
            menu.addSeparator()

        if most_used_count != 0:

            menu_most_used = MyContextMenu(title=self.tr("Les plus utilisés"),
                                           qicon=get_icon(attribute_model_show_icon))
            # No help

            menu.addMenu(menu_most_used)

            for icon_path in most_used_list:
                menu_most_used.add_action(qicon=get_icon(icon_path),
                                          title=os.path.basename(icon_path),
                                          action=lambda val=icon_path: self.icon_changed(val))

        if recent_count != 0:

            menu_recent = MyContextMenu(title=self.tr("Les plus récents"),
                                        qicon=get_icon(recent_icon))
            menu.addMenu(menu_recent)

            for icon_path in recent_icons_list:
                menu_recent.add_action(qicon=get_icon(icon_path),
                                       title=os.path.basename(icon_path),
                                       action=lambda val=icon_path: self.icon_changed(val))

        menu.exec_(point)

    def icon_reset(self):
        self.icon_changed(folder_icon)

    def icon_none(self):
        self.icon_changed(empty_icon)

    @staticmethod
    def a___________________end______():
        pass
