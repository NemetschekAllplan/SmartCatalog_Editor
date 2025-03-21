#!/usr/bin/python3
# -*- coding: utf-8 -*
import uuid

from main_datas import *
from tools import qm_check, MyContextMenu, get_look_treeview, afficher_message


# ====================================================== GENERAL ===============

class ClipboardDatas:

    def __init__(self, type_element):
        super().__init__()

        self.type_element = type_element
        self.datas = []

    def append(self, key: str, value: list) -> None:

        if key != "":
            self.datas.append({"key": key, "value": value, "id": f"{id(key)}"})

    def keys(self) -> list:

        liste_keys = [item["key"] for item in self.datas]
        return liste_keys

    def get_titles_list(self, upper=False) -> list:

        titles_list = list()

        for item in self.datas:

            if not isinstance(item, dict):
                continue

            qs_list = item.get("value")

            if not isinstance(qs_list, list):
                continue

            if len(qs_list) != col_cat_count:
                continue

            qs = qs_list[0]

            if not isinstance(qs, QStandardItem):
                continue

            title_current = qs.text()

            if upper:
                title_current = title_current.upper()

            titles_list.append(title_current)

        return titles_list

    def get_values_list(self) -> list:

        values_list = [item["value"] for item in self.datas]

        return values_list

    def clear(self) -> None:

        self.datas.clear()

    def check_title_exist(self, title: str) -> bool:

        title_list = self.keys()

        return title in title_list

    def get_datas_title(self, title: str, id_ele="0") -> list:

        for datas_current in self.datas:

            datas_current: dict

            title_current = datas_current["key"]

            if title == title_current:

                if id_ele == "0":
                    return [datas_current["value"]]

                id_current = datas_current["id"]

                if id_current == id_ele:
                    return [datas_current["value"]]

        return list()

    def get_real_title(self, title: str, ele_id="0") -> str:

        for datas_current in self.datas:

            datas_current: dict

            title_current = datas_current["key"]

            if title == title_current:

                if ele_id == "0":

                    datas: list = datas_current.get("value", list())

                    if len(datas) == 0:
                        return title

                    qs: QStandardItem = datas[0]

                    if not isinstance(qs, QStandardItem):
                        return title

                    return qs.text()

                id_current = datas_current["id"]

                if id_current == ele_id:

                    datas: list = datas_current.get("value", list())

                    if len(datas) == 0:
                        return title

                    qs: QStandardItem = datas[0]

                    if not isinstance(qs, QStandardItem):
                        return title

                    return qs.text()

        return title

    def len_datas(self) -> int:
        return len(self.datas)

    def get_cut_datas(self, title: str) -> tuple:

        datas_full: list = self.get_datas_title(title)

        if len(datas_full) == 0:
            return None, None

        datas = datas_full[0]

        if len(datas) < 2:
            return None, None

        qs_parent: QStandardItem = datas[0]

        if qs_parent is None:
            return None, None

        qs_current: MyQstandardItem = datas[1]

        if qs_current is None:
            return None, None

        row_index: int = qs_current.row()

        return qs_parent, row_index


def a___________________qstandarditem______():
    pass


class MyQstandardItem(QStandardItem):

    def __init__(self):
        super().__init__()

        pass

    def appendRow(self, items, check=True):

        if not isinstance(items, list):
            print("hierarchy -- MyQstandardItem -- not isinstance(items, list")
            return

        if check and len(items) != col_cat_count:
            print("hierarchy -- MyQstandardItem -- len(items) < col_cat_count")
            return

        super().appendRow(items)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self, new=True, tooltips=True):
        """

        :param new:
        :return:
        :rtype: MyQstandardItem
        """
        pass

    @staticmethod
    def clone_children(qs_original: QStandardItem, qs_destination: QStandardItem, new=True, link=True, recursive=-1,
                       tooltips=True):

        if not isinstance(qs_original, MyQstandardItem):
            return

        children_list = qs_original.get_children_qs(children=True, attributes=True)

        for row_list in children_list:

            row_list: list
            cloned_list = list()

            if len(row_list) != col_cat_count:
                print("hierarchy -- MyQStandardItem -- clone_children -- len(row_list) != col_cat_count")
                continue

            qs_value = row_list[col_cat_value]

            if isinstance(qs_value, Link) and not link:
                continue

            for column_qs in row_list:

                qs_cloned = column_qs.clone_creation(new=new, tooltips=tooltips)

                if column_qs.column() == col_cat_value:

                    if column_qs.hasChildren():

                        if recursive == -1:
                            column_qs.clone_children(qs_original=column_qs, qs_destination=qs_cloned, new=new,
                                                     tooltips=tooltips, recursive=recursive)

                        elif recursive != 0:
                            column_qs.clone_children(qs_original=column_qs, qs_destination=qs_cloned, new=new,
                                                     tooltips=tooltips, recursive=recursive - 1)

                cloned_list.append(qs_cloned)

            qs_destination.appendRow(cloned_list)

    @staticmethod
    def clone_attributes(qs_original: QStandardItem, qs_destination: QStandardItem, new=True):

        if not isinstance(qs_original, MyQstandardItem):
            return

        children_list = qs_original.get_children_qs(children=False, attributes=True)

        attributes_list = [attribut_default_obj.current]

        for row_list in children_list:

            row_list: list
            cloned_list = list()

            qs_number: QStandardItem = row_list[col_cat_number]

            if not isinstance(qs_number, Info):
                break

            number_current = qs_number.text()

            if number_current in attributes_list:
                continue

            attributes_list.append(number_current)

            for qs_column in row_list:
                qs_cloned = qs_column.clone_creation(new=new)

                cloned_list.append(qs_cloned)

            qs_destination.appendRow(cloned_list)

    @staticmethod
    def a___________________attributes_search______():
        pass

    def get_attribute_numbers_list(self) -> list:

        attributes_list = list()

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, Attribute):
                return attributes_list

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Info):
                continue

            attributes_list.append(qs_number.text())

        return attributes_list

    def get_attribute_numbers_datas(self) -> dict:

        attributes_dict = dict()

        columns_count = self.columnCount()

        for index_row in range(self.rowCount()):

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Info):
                continue

            number = qs_number.text()

            if not isinstance(number, str):
                continue

            if number in attributes_dict:
                continue

            attributes_dict[number] = [self.child(index_row, column) for column in range(columns_count)]

        return attributes_dict

    def get_attribute_value_by_number(self, number: str):

        if number == attribut_default_obj.current:
            return self.text()

        if self.data(user_data_type) == link_code:

            if number != "207":
                return None

            qs_parent = self.parent()

            if not isinstance(qs_parent, QStandardItem):
                return None

            current_row = self.row()

            qs_desc = qs_parent.child(current_row, col_cat_desc)

            if not isinstance(qs_desc, Info):
                return None

            desc = qs_desc.text()

            if not isinstance(desc, str):
                return None

            return desc

        for index_row in range(self.rowCount()):

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Info):
                return None

            number_value = qs_number.text()

            if number_value != number:
                continue

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, Attribute):
                return None

            value = qs_value.text()

            if not isinstance(value, str):
                return None

            return qs_value.text()

        return None

    def get_attribute_line_by_number(self, number: str) -> list:

        if number == attribut_default_obj.current:
            return list()
        for index_row in range(self.rowCount()):

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Info):
                return list()

            if qs_number.text() != number:
                continue

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, Attribute):
                return list()

            qs_list = list()

            for column in range(self.columnCount()):

                qs = self.child(index_row, column)

                if qs is None:
                    return list()

                qs_list.append(qs)

            return qs_list

        return list()

    def get_row_attribute_by_number(self, number: str) -> int:

        for index_row in range(self.rowCount()):

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Info):
                return list()

            if qs_number.text() != number:
                continue

            return index_row

        return -1

    @staticmethod
    def a___________________children_list______():
        pass

    def get_link_infos(self):

        link_datas = list()

        for index_row in range(self.rowCount()):

            # search component

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, Component):
                continue

            code = qs_value.text()
            description = formula = ""

            # Search attributes infos

            for index_attribute_row in range(qs_value.rowCount()):

                qs_number = qs_value.child(index_attribute_row, col_cat_number)

                if not isinstance(qs_number, Info):
                    break

                number_value = qs_number.text()

                if number_value == "207":

                    qs_attribute = qs_value.child(index_attribute_row, col_cat_value)

                    if not isinstance(qs_attribute, Attribute):
                        continue

                    description = qs_attribute.text()
                    continue

                if number_value == "267":

                    qs_attribute = qs_value.child(index_attribute_row, col_cat_value)

                    if not isinstance(qs_attribute, Attribute):
                        continue

                    formula = qs_attribute.text()
                    break

            link_datas.append([code, description, formula])

        return link_datas

    def get_children_type_list(self) -> list:

        children_type_list = list()

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, MyQstandardItem):
                continue

            if isinstance(qs_value, Attribute):
                continue

            children_type_list.append(qs_value.data(user_data_type))

        return children_type_list

    def get_children_count(self) -> list:

        counter = 0

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, MyQstandardItem):
                continue

            if isinstance(qs_value, Attribute):
                continue

            counter += 1

        return counter

    def get_children_name(self, upper: bool) -> list:

        name_list = list()

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, MyQstandardItem):
                continue

            if isinstance(qs_value, Attribute):
                continue

            value = qs_value.text()

            if not isinstance(value, str):
                continue

            name_list.append(value.upper() if upper else value)

        return name_list

    def get_children_qs(self, children=True, attributes=True) -> list:

        children_qs_list = list()

        if not children and not attributes:
            return children_qs_list

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not attributes and isinstance(qs_value, Attribute):
                continue

            if not children and not isinstance(qs_value, Attribute):
                continue

            children_qs_column_list = list()

            for column_index in range(self.columnCount()):

                qs_child = self.child(index_row, column_index)

                if qs_child is None:
                    return list()

                children_qs_column_list.append(qs_child)

            children_qs_list.append(children_qs_column_list)

        return children_qs_list

    def get_children_value_qs(self) -> list:

        children_qs_list = list()

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if isinstance(qs_value, Attribute):
                continue

            children_qs_list.append(qs_value)

        return children_qs_list

    def has_link(self):

        children_list = self.get_children_type_list()
        return link_code in children_list

    def has_children(self):

        type_ele = self.data(user_data_type)

        if type_ele == component_code or type_ele == link_code:
            return False

        return len(self.get_children_type_list()) != 0

    @staticmethod
    def a___________________insertion_index______():
        pass

    def get_insertion_index(self):

        if self.rowCount() == 0:
            return 0

        return len(self.get_attribute_numbers_list())

    def get_attribute_insertion_index(self, number: str) -> int:

        if self.rowCount() == 0:
            return 0

        liste_actuelle = self.get_attribute_numbers_list()

        liste_actuelle.append(number)
        liste_actuelle.sort(key=int)

        liste_finale = [numero for numero in liste_attributs_ordre if numero in liste_actuelle]
        liste_finale += [numero for numero in liste_actuelle if numero not in liste_finale]

        index_insertion = liste_finale.index(number)
        return index_insertion

    @staticmethod
    def a___________________update______():
        pass

    @staticmethod
    def update_with(qs_current: QStandardItem, qs_futur: QStandardItem) -> bool:

        text_current = qs_current.text()
        text_futur = qs_futur.text()

        if text_current != text_futur:
            return False

        datas_futur = dict()
        numbers_list = list()

        # ----------
        # get datas of futur qs
        # ----------

        for child_index in range(qs_futur.rowCount()):

            qs_number = qs_futur.child(child_index, col_cat_number)

            if not isinstance(qs_number, Info):
                break

            number = qs_number.text()

            if number == "":
                continue

            values_list = list()
            column_count = qs_futur.columnCount()

            for column_index in range(qs_futur.columnCount()):
                qs_tps = qs_futur.child(child_index, column_index)

                if not isinstance(qs_tps, MyQstandardItem):
                    break

                values_list.append(qs_tps.text())

            if len(values_list) == column_count:
                datas_futur[number] = values_list
                numbers_list.append(number)

        # ----------
        # Update
        # ----------

        for child_index in range(qs_current.rowCount()):

            qs_number = qs_futur.child(child_index, col_cat_number)

            if not isinstance(qs_number, Info):
                break

            number = qs_number.text()

            if number not in datas_futur:
                continue

            for column_index, value_futur in enumerate(datas_futur.get(number, list())):

                qs_tps = qs_current.child(child_index, column_index)

                if not isinstance(qs_tps, (Attribute, Info)):
                    break

                qs_tps.setText(value_futur)

            numbers_list.remove(number)

        return len(numbers_list) == 0

    @staticmethod
    def a___________________end______():
        pass


# ====================================================== FOLDER ===============

class Folder(MyQstandardItem):

    def __init__(self, value: str, tooltips=True, icon_path="", guid=""):
        super().__init__()

        # ---------------- Type Element ----------------

        self.setData(folder_code, user_data_type)

        # ---------------- GUID ----------------

        if guid == "":
            self.setData(str(uuid.uuid4()), user_guid)
        else:
            self.setData(guid, user_guid)

        # ---------------- Title ----------------

        self.setText(value)

        # ---------------- Icon ----------------

        if icon_path != "":
            self.icon_path = icon_path
            self.setData(get_icon(icon_path), Qt.DecorationRole)

        else:

            self.icon_path = folder_icon
            self.setData(get_icon(folder_icon), Qt.DecorationRole)

            # ---------------- Tooltips ----------------

        if not tooltips:
            return

        a = QCoreApplication.translate("MyQstandarditem", "Dossier")
        b = QCoreApplication.translate("MyQstandarditem", "Classement de vos Dossiers ou de vos Ouvrages")
        c = QCoreApplication.translate("MyQstandarditem", "Un dossier peut contenir des dossiers OU des Ouvrages")

        tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                   f"{b}<br><br>"
                   f"<b><u>/!\\</u> {c} <u>/!\\</u></p>")

        if debug_tooltips:
            tooltip += f"<br>guid={self.data(user_guid)}"

        self.setData(tooltip, Qt.ToolTipRole)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self, new=True, tooltips=True):
        """

        :param new:
        :return:
        :rtype: Folder
        """

        if new:
            guid = ""
        else:
            guid = self.data(user_guid)

        return Folder(value=self.text(), tooltips=tooltips, icon_path=self.icon_path, guid=guid)

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Component / Link
        # ------------------------------

        if ele_type == component_code or ele_type == link_code:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")
        child = QCoreApplication.translate("hierarchie_qs", "Enfant")

        parent = self.parent()

        if parent is None:
            parent = self.model().invisibleRootItem()

        # ------------------------------
        # Folder
        # ------------------------------

        if ele_type == folder_code:

            children_list = self.get_children_type_list()

            if material_code in children_list:
                return {brother: [parent, self.row() + 1]}

            return {brother: [parent, self.row() + 1],
                    child: [self, self.get_insertion_index()]}

        # ------------------------------
        # Material
        # ------------------------------
        children_list = self.get_children_type_list()

        if folder_code in children_list:
            return dict()

        return {child: [self, self.get_insertion_index()]}

    def get_type_possibilities(self):

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")
        child = QCoreApplication.translate("hierarchie_qs", "Enfant")

        children_list = self.get_children_type_list()

        or_txt = QCoreApplication.translate("hierarchie_qs", "ou")

        if folder_code in children_list:
            return {folder_code: f"{brother} {or_txt} {child}"}

        if material_code in children_list:
            return {folder_code: brother, material_code: child}

        return {folder_code: f"{brother} {or_txt} {child}", material_code: child}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()

    @staticmethod
    def a___________________end______():
        pass


# ====================================================== MATERIAL ===============


class Material(MyQstandardItem):

    def __init__(self, value: str, used_by_links=0, tooltips=True, guid=""):
        super().__init__()

        # ---------------- GUID ----------------

        if guid == "":
            self.setData(str(uuid.uuid4()), user_guid)
        else:
            self.setData(guid, user_guid)

        # ---------------- Type Element ----------------

        self.setData(material_code, user_data_type)

        # ---------------- Value ----------------

        self.setText(value)

        # ---------------- Icon ----------------

        self.setData(get_icon(material_icon), Qt.DecorationRole)

        # ---------------- Font ----------------

        self.setFont(bold_font)

        # ---------------- Link manage ----------------

        self.used_by_links_count = used_by_links

        # ---------------- Tooltips ----------------

        if used_by_links == 0:
            self.set_material_classic(tooltips=tooltips)
        else:
            self.set_material_link(tooltips=tooltips)

    def set_material_look(self, used_by_links_count=0):

        self.used_by_links_count = used_by_links_count

        if used_by_links_count == 0:
            self.set_material_classic()
        else:
            self.set_material_link()

    def set_material_classic(self, tooltips=True):

        self.setData(QBrush(QColor("#000000")), Qt.ForegroundRole)

        if not tooltips:
            return

        a = QCoreApplication.translate("hierarchie_qs", "Ouvrage")
        b = QCoreApplication.translate("hierarchie_qs", "Correspond à la Désignation/Matériaux dans Allplan")
        c = QCoreApplication.translate("hierarchie_qs", "Un Ouvrage peut contenir des composants ou des liens")

        tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                   f"{b}<br><br>"
                   f"<b><u>/!\\</u> {c} <u>/!\\</u></p>")

        if debug_tooltips:
            tooltip += f"<br>guid={self.data(user_guid)}"

        self.setData(tooltip, Qt.ToolTipRole)

    def set_material_link(self, tooltips=True):

        self.setData(QBrush(QColor("#ff8a65")), Qt.ForegroundRole)

        if not tooltips:
            return

        a = QCoreApplication.translate("hierarchie_qs", "Ouvrage")
        b = QCoreApplication.translate("hierarchie_qs", "Correspond à la Désignation/Matériaux dans Allplan")
        c = QCoreApplication.translate("hierarchie_qs", "Un Ouvrage peut contenir UNIQUEMENT des composants")

        d = QCoreApplication.translate("hierarchie_qs", "Cette ouvrage est utilisé")
        e = QCoreApplication.translate("hierarchie_qs", "fois en tant que lien")

        tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                   f"{b}<br><br>"
                   f"<b><u>/!\\</u> {c} <u>/!\\</u><br><br>"
                   f"{d} {self.used_by_links_count} {e}.")

        if debug_tooltips:
            tooltip += f"<br>guid={self.data(user_guid)}"

        self.setData(tooltip, Qt.ToolTipRole)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self, new=True, tooltips=True):
        """

        :param new:
        :return:
        :rtype: Material
        """

        if new:
            guid = ""
        else:
            guid = self.data(user_guid)

        return Material(value=self.text(), used_by_links=self.used_by_links_count, tooltips=tooltips, guid=guid)

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Folder
        # ------------------------------

        if ele_type == folder_code:
            return dict()

        # ------------------------------

        parent = self.parent()

        if parent is None:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")
        child = QCoreApplication.translate("hierarchie_qs", "Enfant")

        # ------------------------------
        # Material
        # ------------------------------

        if ele_type == material_code:
            return {brother: [parent, self.row() + 1]}

        # ------------------------------
        # Component
        # ------------------------------

        if ele_type == component_code:
            insertion_index = self.get_insertion_index()

            return {child: [self, insertion_index]}

        # ------------------------------
        # Link
        # ------------------------------

        # if self.text() in link_list:
        #     return dict()

        insertion_index = self.get_insertion_index()

        return {brother: [self, insertion_index]}

    @staticmethod
    def get_type_possibilities():

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")
        child = QCoreApplication.translate("hierarchie_qs", "Enfant")

        # if self.text() in link_list:
        #     return {material_code: brother, component_code: child}
        #
        # if len(material_list) - len(material_with_link_list) < 2:
        #     return {material_code: brother, component_code: child}

        return {material_code: brother, component_code: child, link_code: child}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()

    def get_component_by_name(self, component_name):

        for row_index in range(self.rowCount()):

            qs_child = self.child(row_index, col_cat_value)

            if not isinstance(qs_child, Component):
                continue

            component_txt = qs_child.text()

            if not component_txt == component_name:
                continue

            return qs_child

        return None

    def get_link_name(self) -> list:

        link_name_list = list()

        for row_index in range(self.rowCount()):

            qs_child = self.child(row_index, col_cat_value)

            if not isinstance(qs_child, Link):
                continue

            link_text = qs_child.text()

            if not isinstance(link_text, str):
                continue

            if link_text in link_name_list:
                continue

            link_name_list.append(link_text)

        return link_name_list

    @staticmethod
    def a___________________end______():
        pass


# ====================================================== COMPONENT ===============

class Component(MyQstandardItem):

    def __init__(self, value: str, tooltips=True, guid=""):
        super().__init__()

        # ---------------- GUID ----------------

        if guid == "":
            self.setData(str(uuid.uuid4()), user_guid)
        else:
            self.setData(guid, user_guid)

        # ---------------- Type Element ----------------

        self.setData(component_code, user_data_type)

        # ---------------- Value ----------------

        self.setText(value)

        # ---------------- Icon ----------------

        self.setData(get_icon(component_icon), Qt.DecorationRole)

        # ---------------- Font ----------------

        self.setFont(italic_font)

        # ---------------- Tooltips ----------------

        if tooltips:
            a = QCoreApplication.translate("hierarchie_qs", "Composant")
            b = QCoreApplication.translate("hierarchie_qs",
                                           "Correspond aux élements calculés s'affichant dans les rapports d'Allplan")

            c = QCoreApplication.translate("hierarchie_qs", "Un Composant ne peut pas contenir d'enfants")

            tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                       f"{b}<br><br>"
                       f"<b><u>/!\\</u> {c} <u>/!\\</u></p>")

            if debug_tooltips:
                tooltip += f"<br>guid={self.data(user_guid)}"

            self.setData(tooltip, Qt.ToolTipRole)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self, new=True, tooltips=True):

        if new:
            guid = ""
        else:
            guid = self.data(user_guid)

        return Component(value=self.text(), tooltips=tooltips, guid=guid)

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Folder / Material
        # ------------------------------

        if ele_type == folder_code or ele_type == material_code:
            return dict()

        # ------------------------------

        parent = self.parent()

        if parent is None:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        # ------------------------------
        # Component
        # ------------------------------
        if ele_type == component_code or ele_type == link_code:
            return {brother: [parent, self.row() + 1]}

        # ------------------------------
        # Link
        # ------------------------------

        # txt_parent = parent.text()
        #
        # if txt_parent in link_list:
        #     return {}

        return {brother: [parent, self.row() + 1]}

    @staticmethod
    def get_type_possibilities():

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        # if len(material_list) - len(material_with_link_list) < 2:
        #     return {component_code: brother}

        return {component_code: brother, link_code: brother}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()

    @staticmethod
    def a___________________end______():
        pass


# ====================================================== LINK ===============


class Link(MyQstandardItem):

    def __init__(self, value: str, tooltips=True, guid=""):
        super().__init__()

        # ---------------- GUID ----------------

        if guid == "":
            self.setData(str(uuid.uuid4()), user_guid)
        else:
            self.setData(guid, user_guid)

        # ---------------- Type Element ----------------

        self.setData(link_code, user_data_type)

        # ---------------- Value ----------------

        self.setText(value)

        # ---------------- Icon ----------------

        self.setIcon(get_icon(link_icon))

        # ---------------- Font ----------------

        self.setFont(italic_font)

        # ---------------- Tooltips ----------------

        if tooltips:
            a = QCoreApplication.translate("hierarchie_qs", "Lien")
            b = QCoreApplication.translate("hierarchie_qs", "Raccourci vers les composants d'un autre Ouvrage")
            c = QCoreApplication.translate("hierarchie_qs", "Un Lien ne peut pas contenir d'enfants")

            tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                       f"{b}<br><br>"
                       f"<b><u>/!\\</u> {c} <u>/!\\</u></p>")

            if debug_tooltips:
                tooltip += f"<br>guid={self.data(user_guid)}"

            self.setData(tooltip, Qt.ToolTipRole)

        # ---------------- Type Element ----------------

        self.setData(link_code, user_data_type)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self, new=True, tooltips=True):

        if new:
            guid = ""
        else:
            guid = self.data(user_guid)

        return Link(value=self.text(), tooltips=tooltips, guid=guid)

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Folder / Material
        # ------------------------------

        if ele_type == folder_code or ele_type == material_code:
            return dict()

        # ------------------------------

        parent = self.parent()

        if parent is None:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        # ------------------------------
        # Link
        # ------------------------------
        if ele_type == component_code or ele_type == link_code:
            return {brother: [parent, self.row() + 1]}

        # ------------------------------
        # Component
        # ------------------------------

        # txt_parent = parent.text()
        #
        # if txt_parent in link_list:
        #     return dict()

        return {brother: [parent, self.row() + 1]}

    @staticmethod
    def get_type_possibilities():

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        # his_parent = self.parent()
        #
        # if his_parent is None:
        #     return dict()

        # txt_parent = his_parent.text()

        # if txt_parent in link_list:
        #     return {component_code: brother}

        return {component_code: brother, link_code: brother}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()

    @staticmethod
    def a___________________end______():
        pass


# ====================================================== ATTRIBUTE ===============

class Attribute(MyQstandardItem):

    def __init__(self, value: str, guid=""):
        super().__init__()

        # ---------------- GUID ----------------

        if guid == "":
            self.setData(str(uuid.uuid4()), user_guid)
        else:
            self.setData(guid, user_guid)

        # ---------------- Type Element ----------------

        self.setData(attribute_code, user_data_type)

        # ---------------- Value ----------------

        self.setText(value)

        if debug_tooltips:
            tooltip = f"<br>guid={self.data(user_guid)}"

            self.setData(tooltip, Qt.ToolTipRole)

    def clone_creation(self, type_ele="", new=True, tooltips=False):

        if new:
            guid = ""
        else:
            guid = self.data(user_guid)

        qs = Attribute(value=self.text(), guid=guid)

        formula_ok = self.data(user_formule_ok)

        if formula_ok != "":
            qs.setData(formula_ok, user_formule_ok)

        if self.data(user_unknown) is not None:
            qs.setData(type_unknown, user_unknown)

        return qs

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Folder / Material
        # ------------------------------

        if ele_type == folder_code or ele_type == material_code:
            return dict()

        # ------------------------------

        parent = self.parent()

        if parent is None:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        # ------------------------------
        # Link
        # ------------------------------
        if ele_type == link_code:
            return {brother: [parent, self.row() + 1]}

        # ------------------------------
        # Component
        # ------------------------------

        # txt_parent = parent.text()
        #
        # if txt_parent in link_list:
        #     return dict()

        return {brother: [parent, self.row() + 1]}

    @staticmethod
    def get_type_possibilities():
        return {}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()

    @staticmethod
    def a___________________end______():
        pass


# ====================================================== INFO ===============


class Info(MyQstandardItem):

    def __init__(self, value: str, type_ele="", guid=""):
        super().__init__()

        # ---------------- GUID ----------------

        if guid == "":
            self.setData(str(uuid.uuid4()), user_guid)
        else:
            self.setData(guid, user_guid)

        # ---------------- Type Element ----------------

        self.setData(type_ele, user_data_type)

        self.type_ele = type_ele

        # ---------------- Value ----------------

        self.setText(value)

    def clone_creation(self, type_ele="", new=True, tooltips=False):

        if new:
            guid = ""
        else:
            guid = self.data(user_guid)

        if type_ele == "":
            return Info(value=self.text(), type_ele=self.type_ele, guid=guid)

        return Info(value=self.text(), type_ele=type_ele, guid=guid)

    @staticmethod
    def get_type_possibilities():
        return {}

    @staticmethod
    def is_possible_to_add(ele_type: str) -> bool:
        return ele_type in {}

    @staticmethod
    def a___________________end______():
        pass


def a___________________filter______():
    pass


class SpecialFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.search_number = ""
        self.search_type = ""

    def set_custom_filter(self, search_number: str, search_type: str) -> None:

        if not isinstance(search_number, str) or not isinstance(search_type, str):
            self.search_number = ""
            self.search_type = ""
            return

        self.search_type = search_type
        self.search_number = search_number

    def clear_custom_filter(self) -> None:
        self.search_number = ""
        self.search_type = ""

    def active_custom_filter(self) -> bool:
        return self.search_number != "" or self.search_type != ""

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex):

        if self.filterRegExp().isEmpty():
            return True

        model = self.sourceModel()

        if model is None:
            return False

        # ----------
        # Value
        # ----------

        qm_value = model.index(source_row, self.filterKeyColumn(), source_parent)

        if not isinstance(qm_value, QModelIndex):
            return False

        current_value = qm_value.data(self.filterRole())

        if not isinstance(current_value, str):
            return False

        reg_exp = self.filterRegExp()

        valid_text = reg_exp.indexIn(current_value) >= 0

        if self.search_number == "" and self.search_type == "":
            return valid_text

        if not valid_text:
            # print(f"False - None - None --> Value : {current_value} isn't valid ({reg_exp})")
            return False

        # ----------
        # Type
        # ----------

        if self.search_type != "":

            qm_type = model.index(source_row, col_cat_value, source_parent)

            if not isinstance(qm_type, QModelIndex):
                return False

            current_type = qm_type.data(user_data_type)

            # If attribute -> get parent_type
            if current_type == attribute_code:
                qm_type = qm_type.parent()

                if not isinstance(qm_type, QModelIndex):
                    return False

                current_type = qm_type.data(user_data_type)

            regex_type = QRegExp(self.search_type, Qt.CaseInsensitive)

            if regex_type.indexIn(current_type) < 0:
                # print(f"True - False - None --> Value : {current_value} is valid ({reg_exp}) but "
                #       f"type : {current_type} isn't valid {self.search_type}")
                return False

        # else:
        #     current_type = ""

        # ----------
        # Number
        # ----------

        if self.search_number == "":
            return True

        qm_number = model.index(source_row, col_cat_number, source_parent)

        if not isinstance(qm_number, QModelIndex):
            return False

        current_number = qm_number.data()

        valid_number = current_number == self.search_number

        # if not valid_number:
        #     print(f"True - True - False --> Value : {current_value} is valid ({reg_exp}) and "
        #           f"number : {current_number} isn't valid ({self.search_number})")
        #
        # else:
        #
        #     print(f"True - True - True --> Value : {current_value} is valid ({reg_exp}) and "
        #           f"number : {current_number} is valid ({self.search_number})")

        return valid_number

    @staticmethod
    def a___________________end___________________():
        pass


def a___________________qtreeview______():
    pass


class Hierarchy(QTreeView):
    drop_finised = pyqtSignal(QStandardItem, list, int, int, bool, bool, bool, bool)

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.description_show = True

        self.cat_model = QStandardItemModel()
        self.cat_model.invisibleRootItem().setData(folder_code, user_data_type)
        self.cat_model.invisibleRootItem().setData(str(uuid.uuid4()), user_guid)

        self.cat_filter_1 = SpecialFilterProxyModel()
        self.cat_filter_1.setRecursiveFilteringEnabled(True)
        self.cat_filter_1.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.cat_filter_1.setSortLocaleAware(True)
        self.cat_filter_1.setSourceModel(self.cat_model)

        self.cat_filter_2 = QSortFilterProxyModel()
        self.cat_filter_2.setRecursiveFilteringEnabled(True)
        self.cat_filter_2.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.cat_filter_2.setFilterKeyColumn(col_cat_value)
        self.cat_filter_2.setFilterRole(user_data_type)
        self.cat_filter_2.setSortLocaleAware(True)
        self.cat_filter_2.setSourceModel(self.cat_filter_1)

        self.setModel(self.cat_filter_2)

        # ------------------

        self.expanded_list = list()
        self.selected_list = list()

        # ------------------

        self.expanded.connect(self.header_manage)
        self.collapsed.connect(self.header_manage)

        # ------------------

        get_look_treeview(self)

    @staticmethod
    def a___________________loading___________________():
        pass

    def loading_model(self, cat_model: QStandardItemModel, expanded_list: list, selected_list: list):

        self.cat_model = cat_model

        self.cat_model.invisibleRootItem().setData(str(uuid.uuid4()), user_guid)
        self.cat_model.invisibleRootItem().setData(folder_code, user_data_type)

        self.cat_filter_1.setSourceModel(self.cat_model)
        self.cat_filter_1.setFilterRole(user_data_type)

        # --------------

        if not debug:
            self.cat_filter_1.setFilterRegExp(pattern_filter)

        if len(expanded_list) != 0:
            self.expand_list(expanded_list=expanded_list)

        self.header_manage()

        # --------------

        if len(selected_list) == 0:
            return

        if self.selectionModel() is None:
            return

        self.select_list(selected_list=selected_list, scrollto=True)

    @staticmethod
    def a___________________header___________________():
        pass

    def header_manage(self) -> None:

        if not debug and not self.hideColumn(col_cat_index):
            self.setColumnHidden(col_cat_index, True)
            self.setColumnHidden(col_cat_number, True)

        self.setColumnHidden(col_cat_desc, not self.description_show)

        if not isinstance(self.header(), QHeaderView):
            print("Hierarchy -- header_manage -- not isinstance(self.header(), QHeaderView)")
            return

        if self.header().height() != 24:
            self.header().setFixedHeight(24)

        if not self.description_show:
            return

        row_count = self.model().rowCount()

        if row_count == 0:
            return

        size_now = self.header().sectionSize(col_cat_value)

        hearder_size = self.header().width() - 50

        if size_now > hearder_size:
            size_after = hearder_size
            self.header().resizeSection(col_cat_value, size_after)
            return

        self.header().setSectionResizeMode(col_cat_value, QHeaderView.ResizeToContents)

        size_after = self.header().sectionSize(col_cat_value)

        if size_after < size_now:
            self.header().setSectionResizeMode(col_cat_value, QHeaderView.Interactive)
            self.header().resizeSection(col_cat_value, size_now)

        else:
            self.header().setSectionResizeMode(col_cat_value, QHeaderView.Interactive)

    @staticmethod
    def a___________________mapping___________________():
        pass

    def map_to_model(self, qm: QModelIndex) -> QModelIndex | None:

        if not qm_check(qm):
            print("Hierarchy -- map_to_model -- not qm_check(qm)")
            return None

        model = qm.model()

        if model is None:
            print("Hierarchy -- map_to_model -- model is None")
            return None

        if model == self.cat_model:
            return qm

        if model == self.cat_filter_1:
            qm_model = self.cat_filter_1.mapToSource(qm)

            if not qm_check(qm_model):
                print("Hierarchy -- map_to_model -- not qm_check(qm_model)")
                return None

            return qm_model

        if model == self.cat_filter_2:

            qm_filter1 = self.cat_filter_2.mapToSource(qm)

            if not qm_check(qm_filter1):
                print("Hierarchy -- map_to_model -- not qm_check(qm_filter1)")
                return None

            qm_model = self.cat_filter_1.mapToSource(qm_filter1)

            if not qm_check(qm_model):
                print("Hierarchy -- map_to_model -- not qm_check(qm_model)")
                return None

            return qm_model

    def map_to_filter(self, qm: QModelIndex) -> QModelIndex | None:

        if not qm_check(qm):
            print("Hierarchy -- map_to_filter -- not qm_check(qm)")
            return None

        model = qm.model()

        if model is None:
            print("Hierarchy -- map_to_filter -- model is None")
            return None

        if model == self.cat_filter_2:
            return qm

        if model == self.cat_filter_1:

            qm_filter2 = self.cat_filter_2.mapFromSource(qm)

            if not qm_check(qm_filter2):
                print("Hierarchy -- map_to_filter -- not qm_check(qm_filter2)")
                return None

            return qm_filter2

        if model == self.cat_model:

            qm_filter1 = self.cat_filter_1.mapFromSource(qm)

            if not qm_check(qm_filter1):
                print("Hierarchy -- map_to_filter -- not qm_check(qm_filter1)")
                return None

            qm_filter2 = self.cat_filter_2.mapFromSource(qm_filter1)

            if not qm_check(qm_filter2):
                print("Hierarchy -- map_to_filter -- not qm_check(qm_filter2)")
                return None

            return qm_filter2

    @staticmethod
    def a___________________get_datas___________________():
        pass

    def get_parent(self, qs: MyQstandardItem) -> MyQstandardItem:

        qs_parent = qs.parent()

        if qs_parent is None:
            return self.cat_model.invisibleRootItem()

        return qs_parent

    def get_qs_by_qm(self, qm: QModelIndex) -> QStandardItem | None:

        if not qm_check(qm):
            print("Hierarchy -- get_qs_by_qm -- not qm_check(qm)")
            return None

        if qm.model() == self.cat_model:
            return self.cat_model.itemFromIndex(qm)

        qm_model: QModelIndex = self.map_to_model(qm=qm)

        if qm_model is None:
            print("Hierarchy -- get_qs_by_qm -- qm_model is None")
            return None

        qs = self.cat_model.itemFromIndex(qm_model)

        if qs is None:
            print("Hierarchy -- get_qs_by_qm -- qs is None")

        return qs

    def get_current_qm_filter(self) -> QModelIndex | None:

        selected_list: list = self.get_qm_filter_selection_list()

        if len(selected_list) == 0:
            return None

        selected_list.sort()

        qm = selected_list[-1]

        if not qm_check(qm):
            print("Hierarchy -- get_current_qm_filter -- qm is None")
            return None

        return qm

    def get_current_qs(self) -> QStandardItem | None:

        qm_current = self.get_current_qm_filter()

        if qm_current is None:
            return None

        qs = self.get_qs_by_qm(qm_current)

        if not isinstance(qs, QStandardItem):
            print("Hierarchy -- get_current_qs -- qs is None")
            return None

        return qs

    @staticmethod
    def a___________________filters___________________():
        pass

    @staticmethod
    def search_get_regex(current_text: str, search_mode: int, search_case: bool) -> QRegExp:

        # exact
        if search_mode == 1:
            return QRegExp(f"^{QRegExp.escape(current_text)}$", search_case)

        # Start with
        if search_mode == 2:
            return QRegExp(f"^{QRegExp.escape(current_text)}", search_case)

        # End with
        if search_mode == 3:
            return QRegExp(f"{QRegExp.escape(current_text)}$", search_case)

        # Contain
        return QRegExp(QRegExp.escape(current_text), search_case)

    def search_text(self, current_text: str, search_column=0, search_number="", search_type="",
                    search_mode=0, search_case=False) -> bool:

        regex = self.search_get_regex(current_text=current_text, search_mode=search_mode, search_case=search_case)

        # self.save_qm_model_selection_list()

        # ------------
        # Search numbers
        # ------------

        self.setUpdatesEnabled(False)

        if search_column == col_cat_number:

            # ------------
            # First filter -> number
            # ------------

            if self.cat_filter_1.filterKeyColumn() != col_cat_number:
                self.cat_filter_1.setFilterKeyColumn(col_cat_number)

            if self.cat_filter_1.filterRole() != Qt.DisplayRole:
                self.cat_filter_1.setFilterRole(Qt.DisplayRole)

            if self.cat_filter_1.filterRegExp() != regex:
                self.cat_filter_1.setFilterRegExp(regex)

            # row_count = self.catalog.cat_filter.rowCount()

        # ------------
        # Search in attribute
        # ------------

        else:

            # ------------
            # First filter -> number
            # ------------

            if self.cat_filter_1.filterKeyColumn() != col_cat_value:
                self.cat_filter_1.setFilterKeyColumn(col_cat_value)

            if self.cat_filter_1.filterRole() != Qt.DisplayRole:
                self.cat_filter_1.setFilterRole(Qt.DisplayRole)

            self.cat_filter_1.set_custom_filter(search_number=search_number, search_type=search_type)

            self.cat_filter_1.setFilterRegExp(regex)

            if search_mode == 0 and self.cat_filter_1.rowCount() == 0:
                self.cat_filter_1.setFilterRegExp(QRegExp(current_text, search_case))

            # row_count = self.catalog.cat_filter.rowCount()

        # ------------
        # Second filter -> type
        # ------------

        if not debug:

            if self.cat_filter_2.filterRegExp().pattern() != search_type:
                self.cat_filter_2.setFilterRegExp(search_type)

        else:

            if self.cat_filter_2.filterRegExp().pattern() != "":
                self.cat_filter_2.setFilterRegExp("")

            # row_count_2 = self.hierarchy.cat_filter_2.rowCount()

        self.setUpdatesEnabled(True)

        if self.cat_filter_2.rowCount() == 0:
            afficher_message(titre=application_title,
                             message=self.tr("Aucun élément n'a été trouvé"),
                             icone_avertissement=True)

            return False

        self.blockSignals(True)
        self.expandAll()
        self.blockSignals(False)

        if not self.select_list(selected_list=self.selected_list):
            self.select_list(selected_list=[self.cat_filter_2.index(0, 0)])

        self.header_manage()
        return True

    def search_clear(self) -> bool:

        modification = 0

        self.setUpdatesEnabled(False)

        if self.cat_filter_2.filterRegExp().pattern() != "":
            self.cat_filter_2.setFilterRegExp("")
            modification = 1

        if self.cat_filter_1.active_custom_filter():
            self.cat_filter_1.clear_custom_filter()
            modification = 2

        if self.cat_filter_1.filterKeyColumn() != col_cat_value:
            self.cat_filter_1.setFilterKeyColumn(col_cat_value)
            modification = 3

        if self.cat_filter_1.filterRole() != user_data_type:
            self.cat_filter_1.setFilterRole(user_data_type)
            modification = 4

        if debug:

            if self.cat_filter_1.filterRegExp().pattern() != "":
                self.cat_filter_1.setFilterRegExp("")
                modification = 5

        else:

            if self.cat_filter_1.filterRegExp().pattern() != pattern_filter:
                self.cat_filter_1.setFilterRegExp(pattern_filter)
                modification = 5

        self.setUpdatesEnabled(True)

        if modification == 0:
            self.select_list(selected_list=self.selected_list)
            return False

        self.blockSignals(True)
        self.collapseAll()
        self.expand_list(self.expanded_list)
        self.blockSignals(False)

        if not self.select_list(selected_list=self.selected_list):
            self.select_list(selected_list=[self.cat_filter_2.index(0, 0)])

        self.header_manage()

        return True

    def search_formula_with_error(self):

        search_start = self.cat_model.index(0, 0)

        search = self.cat_model.match(search_start, user_formule_ok, r"^.*\S+.*$", -1,
                                      Qt.MatchRecursive | Qt.MatchRegExp)

        error_list = [qm for qm in search if qm.data(user_formule_ok) is not None]

        return len(error_list) != 0

    @staticmethod
    def a___________________get_root_datas___________________():
        pass

    def get_root_children_name(self, upper=True):

        names_list = list()

        row_count = self.cat_model.rowCount()

        for row_index in range(row_count):

            qm: QModelIndex = self.cat_model.index(row_index, col_cat_value)

            if not qm_check(qm):
                print("Hierarchy -- get_root_children_name -- not qm_check(qm)")
                continue

            title: str = qm.data()

            if title is None:
                print("Hierarchy -- get_root_children_name -- title is None")
                continue

            if upper:
                names_list.append(title.upper())
            else:
                names_list.append(title)

        return names_list

    def get_root_children_type_list(self) -> list:

        children_type_list = list()

        row_count = self.cat_model.rowCount()

        for index_row in range(row_count):

            qs_value = self.cat_model.invisibleRootItem().child(index_row, col_cat_value)

            if not isinstance(qs_value, MyQstandardItem):
                continue

            if isinstance(qs_value, Attribute):
                continue

            children_type_list.append(qs_value.data(user_data_type))

        return children_type_list

    @staticmethod
    def a___________________selection_manage______():
        pass

    def selection_manage(self):

        qm_selection_list = self.selectionModel().selectedRows()

        if len(qm_selection_list) < 2:
            return

        current_ele_type = ""
        invalid = QItemSelection()

        for qm in reversed(qm_selection_list):

            qm: QModelIndex

            current_model = qm.model()

            if current_model is None:
                continue

            qm_parent: QModelIndex = qm.parent()

            if qm_parent is None:
                continue

            current_row = qm.row()

            qm_start = current_model.index(current_row, 0, qm_parent)
            qm_end = current_model.index(current_row, col_cat_count - 1, qm_parent)

            ele_type = qm.data(user_data_type)

            if current_ele_type == "":
                current_ele_type = ele_type
                continue

            if current_ele_type != "" and current_ele_type == ele_type:
                continue

            invalid.select(qm_start, qm_end)

        self.selectionModel().select(invalid, QItemSelectionModel.Deselect)

    @staticmethod
    def a___________________selection_get___________________():
        pass

    def get_qm_filter_selection_list(self) -> list:

        if self.selectionModel() is None:
            print("Hierarchy -- get_qm_filter_selection_list -- self.selectionModel() is None")
            return list()

        selected_list = self.selectionModel().selectedRows(col_cat_value)

        selected_list.sort()

        return selected_list

    def get_qs_selection_list(self) -> list:

        qs_list = list()

        if self.selectionModel() is None:
            print("Hierarchy -- get_qs_selection_list -- self.selectionModel()")
            return qs_list

        selected_list = self.get_qm_filter_selection_list()

        if len(selected_list) == 0:
            return qs_list

        for qm_filter in selected_list:
            qs: MyQstandardItem = self.get_qs_by_qm(qm_filter)

            if qs is None:
                print("Hierarchy -- get_qs_selection_list -- qs is None")
                continue

            qs_list.append(qs)

        return qs_list

    @staticmethod
    def a___________________selection_save___________________():
        pass

    def save_qm_model_selection_list(self):

        self.selected_list = self.get_qm_model_selection_list()

    def get_qm_model_selection_list(self) -> list:

        selected_list = list()

        if self.selectionModel() is None:
            print("Hierarchy -- get_qm_filter_selection_list -- self.selectionModel() is None")
            return list()

        qm_filter_selection_list = self.get_qm_filter_selection_list()

        for qm_filter in qm_filter_selection_list:

            qm_model = self.map_to_model(qm=qm_filter)

            if not qm_check(qm_model):
                print("Hierarchy -- get_qm_model_selection_list -- not qm_check(qm_model)")
                continue

            selected_list.append(qm_model)

        return selected_list

    @staticmethod
    def a___________________selection___________________():
        pass

    def select_list(self, selected_list: list, scrollto=True, expand=False) -> bool:

        if self.selectionModel() is None:
            print("Hierarchy -- catalog_select_action -- selectionModel is None")
            return False

        if len(selected_list) == 0:
            print("Hierarchy -- catalog_select_action -- len(selected_list) == 0")
            return False

        current_list = list()

        qitemselection = QItemSelection()

        for qm_model in selected_list:

            if isinstance(qm_model, MyQstandardItem):
                qm_model = self.cat_model.indexFromItem(qm_model)

            elif not isinstance(qm_model, QModelIndex):
                print("catalog_manage -- catalog_select_action -- not isinstance(qm_model, QModelIndex)")
                continue

            if not qm_check(qm_model):
                print("catalog_manage -- catalog_select_action -- qm_check(qm_model)")
                continue

            if qm_model.data(user_data_type) == attribute_code:
                qm_model = qm_model.parent()

                if not qm_check(qm_model):
                    print("catalog_manage -- catalog_select_action -- qm_check(qm_model)")
                    continue

            qm_filter: QModelIndex = self.map_to_filter(qm=qm_model)

            if qm_filter is None:
                print("catalog_manage -- catalog_select_action -- qm_filtre is None")
                continue

            if qm_filter in current_list:
                print("catalog_manage -- catalog_select_action -- qm_filter in current_list")
                continue

            self.expand_all_parents(qm_filter)

            # if len(selected_list) == 1:
            #     self.hierarchy.setCurrentIndex(qm_filter)

            if qm_filter is None:
                print("catalog_manage -- catalog_select_action -- qm_filter is None")
                continue

            model = qm_filter.model()

            if model is None:
                print("catalog_manage -- catalog_select_action -- model is None")
                continue

            current_row: int = qm_filter.row()
            current_parent: QModelIndex = qm_filter.parent()

            if current_parent is None:
                print("catalog_manage -- catalog_select_action -- current_parent is None")
                continue

            current_list.append(qm_filter)

            qm_start = model.index(current_row, 0, current_parent)
            qm_end = model.index(current_row, col_cat_count - 1, current_parent)

            qitemselection.select(qm_start, qm_end)

        if len(current_list) == 0:
            return False

        if scrollto:
            qm_filter = current_list[-1]

            self.scrollTo(qm_filter, QAbstractItemView.PositionAtCenter)
            self.horizontalScrollBar().setValue(0)

        self.clearSelection()

        self.selectionModel().blockSignals(True)

        self.selectionModel().select(qitemselection, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.selectionModel().blockSignals(False)

        self.selectionModel().selectionChanged.emit(qitemselection, qitemselection)

        if not expand:
            return True

        self.expand_list(expanded_list=selected_list)
        return True

    def select_first_formula(self) -> bool:

        if self.cat_filter_2.rowCount() == 0:
            return False

        search_start = self.cat_filter_2.index(0, 0)

        search = self.cat_filter_2.match(search_start, user_data_type, component_code, 1, Qt.MatchRecursive)

        if len(search) != 1:

            search = self.cat_filter_2.match(search_start, user_data_type, material_code, 1, Qt.MatchRecursive)

            if len(search) != 1:
                print("Hierarchy -- select_first -- len(search) != 1")
                return False

        qm_filter = search[0]

        if not qm_check(qm_filter):
            print("Hierarchy -- select_first -- not qm_check(qm_filter)")
            return False

        self.select_list(selected_list=[qm_filter], scrollto=True)
        return True

    @staticmethod
    def a___________________expand______():
        pass

    def expand_start(self):
        self.blockSignals(True)

        # self.save_qm_model_selection_list()

    def expand_end(self):

        self.blockSignals(False)

        self.header_manage()

        self.select_list(selected_list=self.selected_list)

    def expand_menu_creation(self):

        qm_filter_selection_list = self.get_qm_filter_selection_list()

        if len(qm_filter_selection_list) == 0:
            type_ele = ""
        else:
            qm_select = qm_filter_selection_list[0]

            if qm_check(qm_select):
                type_ele = qm_select.data(user_data_type)
            else:
                type_ele = ""

        expand_menu = MyContextMenu(tooltips_visible=False)

        expand_menu.add_title(title=self.tr("Catalogue"))

        expand_menu.add_action(qicon=get_icon(catalog_icon),
                               title=self.tr("Tous le catalogue"),
                               action=self.expand_all,
                               tooltips="",
                               short_link="")

        expand_menu.add_action(qicon=get_icon(catalog_icon),
                               title=self.tr("Tous le catalogue (Dossiers)"),
                               action=lambda val=True: self.expand_all_folders(recursive=val),
                               tooltips="",
                               short_link="")

        expand_menu.add_action(qicon=get_icon(catalog_icon),
                               title=self.tr("Tous le catalogue (Dossiers du 1er niveau)"),
                               action=lambda val=False: self.expand_all_folders(recursive=val),
                               tooltips="",
                               short_link="")

        if type_ele == "" or type_ele == component_code or type_ele == link_code:
            return expand_menu

        expand_menu.add_title(title=self.tr("Sélection"))

        expand_menu.add_action(qicon=get_icon(":/Images/selection_all.png"),
                               title=self.tr("Sélection"),
                               action=lambda val=True, val2=material_code:
                               self.expand_all_sub_items(recursive=val, type_ele=val2),
                               tooltips="",
                               short_link="")

        if type_ele != folder_code:
            return expand_menu

        expand_menu.add_action(qicon=get_icon(":/Images/selection_all.png"),
                               title=self.tr("Sélection (Dossiers)"),
                               action=lambda val=True, val2=folder_code:
                               self.expand_all_sub_items(recursive=val, type_ele=val2),
                               tooltips="",
                               short_link="")

        expand_menu.add_title(title=self.tr("Sélection (1er niveau)"))

        expand_menu.add_action(qicon=get_icon(":/Images/selection_1.png"),
                               title=self.tr("Sélection (1er niveau)"),
                               action=lambda val=False, val2=material_code:
                               self.expand_all_sub_items(recursive=val, type_ele=val2),
                               tooltips="",
                               short_link="")

        return expand_menu

    def expand_all(self):

        self.expand_start()

        # ---------------

        self.expandAll()

        # ---------------

        self.expand_end()

    def expand_all_folders(self, recursive: bool):

        if self.cat_filter_2.rowCount() == 0:
            print("Hierarchy -- expand_all_folders -- self.cat_filter_2.rowCount()")
            return

        # ---------------

        if recursive:
            match_recursive = Qt.MatchRecursive
        else:
            match_recursive = Qt.MatchExactly

        # ---------------

        qm_start = self.cat_filter_2.index(0, 0)

        if not qm_check(qm_start):
            print("Hierarchy -- expand_all_folders -- not qm_check(qm_start)")
            return

        search = self.cat_filter_2.match(qm_start, user_data_type, folder_code, -1, match_recursive)

        if len(search) == 0:
            return

        # ---------------

        self.expand_start()

        # ---------------

        for qm_filter in search:

            if self.isExpanded(qm_filter):
                continue

            self.expand(qm_filter)

        # ---------------

        self.expand_end()

    def expand_all_sub_items(self, recursive: bool, type_ele: str):

        if type_ele not in {folder_code, material_code}:
            print("Hierarchy -- expand_all_sub_items -- type_ele not in {folder_code, material_code}")
            return

        # ---------------

        qm_list = self.selectionModel().selectedRows()

        if len(qm_list) == 0:
            print("Hierarchy -- expand_all_sub_items -- len(qm_list) == 0)")
            return

        # ---------------

        if recursive:
            match_recursive = Qt.MatchRecursive
        else:
            match_recursive = Qt.MatchExactly

        qm_list_done = set()

        # ---------------

        self.expand_start()

        # ---------------

        for qm_selected in qm_list:

            if not qm_check(qm_selected):
                print("Hierarchy -- expand_all_sub_items -- not qm_check(qm_selected)")
                continue

            if qm_selected in qm_list_done:
                continue

            qm_list_done.add(qm_selected)

            # ---------------

            self.expand(qm_selected)

            # ---------------

            qm_start = self.cat_filter_2.index(0, 0, qm_selected)

            if not qm_check(qm_start):
                print("Hierarchy -- expand_all_sub_items -- not qm_check(qm_start)")
                continue

            # ---------------

            search = self.cat_filter_2.match(qm_start, user_data_type, folder_code, -1, match_recursive)

            if type_ele == material_code:
                search_material = self.cat_filter_2.match(qm_start, user_data_type, material_code, -1, match_recursive)

                search.extend(search_material)

            if len(search) == 0:
                continue

            # ---------------

            for qm_filter in search:

                if qm_filter in qm_list_done:
                    continue

                qm_list_done.add(qm_filter)

                if self.isExpanded(qm_filter):
                    continue

                self.expand(qm_filter)

        # ---------------

        self.expand_end()

    def expand_list(self, expanded_list: list) -> None:

        if len(expanded_list) == 0:
            return

        self.expand_start()

        for item in expanded_list:

            if isinstance(item, MyQstandardItem):
                qm_model: QModelIndex = item.index()

            elif isinstance(item, QModelIndex):
                qm_model = item

            else:
                print("Hierarchy -- expand_list -- bad item")
                continue

            qm_filter: QModelIndex = self.map_to_filter(qm=qm_model)

            if not qm_check(qm_filter):
                print("Hierarchy -- expand_list -- qm_check(qm_filter)")
                continue

            if not self.expand(qm_filter):
                self.expand(qm_filter)

        self.expand_end()

    def expand_all_parents(self, qm: QModelIndex):

        if not isinstance(qm, QModelIndex):
            print("Hierarchy -- expand_all_parents -- not isinstance(qm, QModelIndex)")
            return

        model = qm.model()

        if model is None:
            print("Hierarchy -- expand_all_parents -- model is None")
            return

        if model != self.cat_filter_2:
            qm_filter = self.map_to_filter(qm)
        else:
            qm_filter = qm

        qm_parent = qm_filter.parent()

        self.blockSignals(True)

        while True:

            if not qm_check(qm_parent):
                break

            self.expand(qm_parent)
            qm_parent = qm_parent.parent()

        self.blockSignals(False)

    @staticmethod
    def a___________________expand_save___________________():
        pass

    def save_qm_model_expanded_list(self) -> None:

        self.expanded_list = self.get_qm_model_expanded_list()

    def get_qm_model_expanded_list(self) -> list:

        search_start = self.cat_filter_2.index(0, 0)

        search_folder = self.cat_filter_2.match(search_start, user_data_type, folder_code, -1, Qt.MatchRecursive)
        search_material = self.cat_filter_2.match(search_start, user_data_type, material_code, -1, Qt.MatchRecursive)

        search = search_folder + search_material

        if len(search) == 0:
            return list()

        expanded_list = list()

        for qm_filter in search:

            if not qm_check(qm_filter):
                print("Hierarchy -- get_qm_model_expanded_list -- not qm_check(qm_filter)")
                continue

            if not self.isExpanded(qm_filter):
                continue

            qm_model = self.map_to_model(qm=qm_filter)

            expanded_list.append(qm_model)

        return expanded_list

    @staticmethod
    def a___________________collapse______():
        pass

    def collapse_menu_creation(self):

        qm_select = self.selectionModel().currentIndex()

        if qm_check(qm_select):
            type_ele = qm_select.data(user_data_type)
        else:
            type_ele = ""

        collapse_menu = MyContextMenu(tooltips_visible=False)

        collapse_menu.add_title(title=self.tr("Catalogue"))

        collapse_menu.add_action(qicon=get_icon(catalog_icon),
                                 title=self.tr("Tous le catalogue"),
                                 action=self.collapse_all,
                                 tooltips="",
                                 short_link="")

        collapse_menu.add_action(qicon=get_icon(catalog_icon),
                                 title=self.tr("Tous le catalogue (Ouvrages)"),
                                 action=lambda val=True: self.collapse_all_materials(recursive=val),
                                 tooltips="",
                                 short_link="")

        if type_ele == "" or type_ele == component_code or type_ele == link_code:
            return collapse_menu

        collapse_menu.add_title(title=self.tr("Sélection"))

        collapse_menu.add_action(qicon=get_icon(":/Images/selection_all.png"),
                                 title=self.tr("Sélection"),
                                 action=lambda val=True, val2=folder_code:
                                 self.collapse_all_sub_items(recursive=val, type_ele=val2),
                                 tooltips="",
                                 short_link="")

        if type_ele != folder_code:
            return collapse_menu

        collapse_menu.add_action(qicon=get_icon(":/Images/selection_all.png"),
                                 title=self.tr("Sélection (Ouvrages)"),
                                 action=lambda val=True, val2=material_code:
                                 self.collapse_all_sub_items(recursive=val, type_ele=val2),
                                 tooltips="",
                                 short_link="")

        return collapse_menu

    def collapse_all(self):

        self.expand_start()

        self.collapseAll()

        self.expand_end()

    def collapse_all_materials(self, recursive: bool):

        # ---------------

        if recursive:
            match_recursive = Qt.MatchRecursive
        else:
            match_recursive = Qt.MatchExactly

        # ---------------

        qm_start = self.cat_filter_2.index(0, 0)

        if not qm_check(qm_start):
            print("Hierarchy -- collapse_all_materials -- not qm_check(qm_start)")
            return

        # ---------------

        search = self.cat_filter_2.match(qm_start, user_data_type, material_code, -1, match_recursive)

        # ---------------

        if len(search) == 0:
            return

        # ---------------

        self.expand_start()

        # ---------------

        for qm_filter in search:

            if not self.isExpanded(qm_filter):
                continue

            self.setExpanded(qm_filter, False)

        # ---------------

        self.expand_end()

    def collapse_all_sub_items(self, recursive: bool, type_ele: str):

        if type_ele not in {folder_code, material_code}:
            print("Hierarchy -- collapse_all_sub_items -- type_ele not in {folder_code, material_code}")
            return

        # ---------------

        qm_list = self.selectionModel().selectedRows()

        if len(qm_list) == 0:
            print("Hierarchy -- collapse_all_sub_items -- len(qm_list) == 0)")
            return

        # ---------------

        if recursive:
            match_recursive = Qt.MatchRecursive
        else:
            match_recursive = Qt.MatchExactly

        qm_list_done = set()

        # ---------------

        self.expand_start()

        # ---------------

        for qm_selected in qm_list:

            if not qm_check(qm_selected):
                print("Hierarchy -- collapse_all_sub_items -- not qm_check(qm_selected)")
                continue

            if qm_selected in qm_list_done:
                continue

            qm_list_done.add(qm_selected)

            # ---------------

            self.setExpanded(qm_selected, True)

            # ---------------

            qm_start = self.cat_filter_2.index(0, 0, qm_selected)

            if not qm_check(qm_start):
                print("Hierarchy -- collapse_all_sub_items -- not qm_check(qm_start)")
                continue

            # ---------------

            search = self.cat_filter_2.match(qm_start, user_data_type, material_code, -1, match_recursive)

            if type_ele == folder_code:
                search_folder = self.cat_filter_2.match(qm_start, user_data_type, folder_code, -1, match_recursive)

                search.extend(search_folder)

            if len(search) == 0:
                continue

            # ---------------

            for qm_filter in search:

                if qm_filter in qm_list_done:
                    continue

                qm_list_done.add(qm_filter)

                if not self.isExpanded(qm_filter):
                    continue

                self.setExpanded(qm_filter, False)

        # ---------------

        self.expand_end()

    @staticmethod
    def a___________________library______():
        pass

    def library_possible_to_add(self, library_treeview: QTreeView, qs_target: QStandardItem | None) -> bool:

        if not isinstance(library_treeview, Hierarchy):
            print("Hierarchy -- library_possible_to_add -- not isinstance(library_treeview, Hierarchy)")
            return False

        qs_selection_list = library_treeview.get_qs_selection_list()

        if len(qs_selection_list) == 0:
            return False

        qs_value = qs_selection_list[0]

        if not isinstance(qs_value, MyQstandardItem):
            print("Hierarchy -- library_possible_to_add -- not isinstance(qs_value, MyQstandardItem)")
            return False

        if not isinstance(qs_target, MyQstandardItem):
            if isinstance(qs_value, Folder):
                return True

            print("Hierarchy -- library_possible_to_add -- not isinstance(qs_value, Folder)")
            return False

        # -----------------
        # Link & Component
        # -----------------

        if isinstance(qs_value, (Component | Link)):
            if isinstance(qs_target, (Material, Component, Link)):
                return True

            print("Hierarchy -- library_possible_to_add -- not isinstance(self.current_qs, (Material, Component, Link)")
            return False

        # -----------------
        # Material
        # -----------------

        if isinstance(qs_value, Material):

            if not isinstance(qs_target, (Folder, Material)):
                print("Hierarchy -- library_possible_to_add -- not isinstance(self.current_qs, (Folder, Material))")
                return False

            children_list = qs_value.get_children_type_list()

            if len(children_list) == 0:
                if isinstance(qs_target, (Folder, Material)):
                    return True

                print("Hierarchy -- library_possible_to_add -- not isinstance(self.current_qs, (Folder, Material))")

                return False

            if material_code not in children_list and folder_code not in children_list:
                return True

            print("Hierarchy -- library_possible_to_add -- material_code or folder_code in children_list")

            return False

        # -----------------
        # folder
        # -----------------

        if isinstance(qs_value, Folder):

            if not isinstance(qs_target, Folder):
                print("Hierarchy -- library_possible_to_add -- not isinstance(self.current_qs, Folder)")
                return False

            # ----------

            children_list = qs_value.get_children_type_list()

            if len(children_list) == 0:
                return True

            # ----------

            if component_code in children_list or link_code in children_list:
                print("Hierarchy -- library_possible_to_add -- component_code in children_list")
                return False

            # ----------

            if self.library_recurcive_verification(qs_list=qs_selection_list, parent_type=folder_code):
                return True

            print("Hierarchy -- library_possible_to_add -- not self.library_recurcive_verification")
            return False

        # -----------------
        # Other
        # -----------------
        print("Hierarchy -- library_possible_to_add -- Inknown type")
        return False

    def library_recurcive_verification(self, qs_list: list[MyQstandardItem], parent_type: str) -> bool:

        type_items = ""

        for qs in qs_list:

            if not isinstance(qs, MyQstandardItem):
                print("Hierarchy -- library_recurcive_verification -- not isinstance(qs, MyQstandardItem)")
                return False

            type_current = qs.data(user_data_type)

            if type_items == "":

                type_items = qs.data(user_data_type)

                if parent_type == folder_code and type_current not in [folder_code, material_code]:
                    print("Hierarchy -- library_recurcive_verification -- "
                          "parent_type == folder_code and type_current not in [folder_code, material_code]")
                    return False

                if parent_type == material_code and type_current not in [component_code, link_code]:
                    print("Hierarchy -- library_recurcive_verification -- "
                          "parent_type == material_code and type_current not in [component_code, link_code]")
                    return False

            elif type_items != type_current:
                print("Hierarchy -- library_recurcive_verification -- type_items != type_current")
                return False

            qs_children_list = qs.get_children_value_qs()

            if not self.library_recurcive_verification(qs_list=qs_children_list, parent_type=type_items):
                print("Hierarchy -- library_recurcive_verification -- not self.library_recurcive_verification")
                return False

        return True

    @staticmethod
    def a___________________signals______():
        pass

    def get_drag_datas(self):

        qs_selection = self.get_qs_selection_list()

        if len(qs_selection) == 0:
            print("Hierarchy -- get_drag_datas -- len(qs_selection) == 0")
            return

        qs_list = list()
        ele_type = ""

        for qs_value in qs_selection:

            # ------------- Value ------

            if not isinstance(qs_value, (Folder, Material, Component)):
                print("Hierarchy -- get_drag_datas -- not isinstance(qs, (Folder, Material, Component))")
                continue

            row_current = qs_value.row()

            # ------------- Parent ------

            qs_parent = qs_value.parent()

            if not isinstance(qs_parent, MyQstandardItem):
                qs_parent = self.cat_model.invisibleRootItem()

            # ------------- Index ------

            qs_index = qs_parent.child(row_current, col_cat_index)

            if not isinstance(qs_index, Info):
                print("Hierarchy -- get_drag_datas -- not isinstance(qs_index, Info)")
                continue

            # ------------- Number ------

            qs_number = qs_parent.child(row_current, col_cat_number)

            if not isinstance(qs_number, Info):
                print("Hierarchy -- get_drag_datas -- not isinstance(qs_number, Info)")
                continue

            # ------------- type_ele ------

            if ele_type == "":

                ele_type = qs_value.data(user_data_type)

                if not isinstance(ele_type, str):
                    print("Hierarchy -- get_drag_datas -- not isinstance(type_ele, str)")
                    continue

            # ------------- add to list ------

            qs_list.append([qs_value, qs_index, qs_number])

        if len(qs_list) == 0:
            print("Hierarchy -- get_drag_datas -- len(qs_list) == 0")
            return

        return DragObject(qs_list=qs_list, ele_type=ele_type)

    def dragEnterEvent(self, event: QDragEnterEvent):

        super().dragEnterEvent(event)

        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):

        super().dragMoveEvent(event)

        self.drag_and_drop(event=event)

    def dropEvent(self, event: QDropEvent):

        if self.drag_and_drop(event=event, add=True):
            super().dropEvent(event)

    def drag_and_drop(self, event: QDragEnterEvent | QDragMoveEvent, add=False) -> bool:

        if event.mimeData().hasUrls():
            event.ignore()
            return False

        if isinstance(event, QDragMoveEvent):

            event_type = "QDragMoveEvent"

        elif isinstance(event, QDropEvent):

            event_type = "QDropEvent"
        else:
            event.ignore()
            return

        if self.dropIndicatorPosition() not in [QAbstractItemView.OnItem, QAbstractItemView.OnViewport]:
            event.ignore()
            return False

        # -----------

        library_treeview = event.source()

        if not isinstance(library_treeview, Hierarchy):
            event.ignore()
            print(f"Hierarchy -- drag_and_drop -- {event_type} -- not isinstance(library_treeview, Hierarchy)")
            return False

        # -----------

        drag_obj = library_treeview.get_drag_datas()

        if not isinstance(drag_obj, DragObject):
            event.ignore()
            print(f"Hierarchy -- drag_and_drop -- {event_type} -- not isinstance(drag_obj, DragObject)")
            return False

        if len(drag_obj.qs_list) == 0:
            event.ignore()
            print(f"Hierarchy -- drag_and_drop -- {event_type} -- len(drag_obj.qs_list) == 0")
            return False

        # -----------

        position = event.pos()

        qm_filter = self.indexAt(position)

        if not qm_check(qm_filter):

            if drag_obj.ele_type != folder_code:
                event.ignore()
                # print(f"Hierarchy -- drag_and_drop -- {event_type} -- drag_obj.ele_type != folder_code")
                return False

            if not add:
                event.accept()
                return True

            qs_parent_target = self.cat_model.invisibleRootItem()

        else:
            # -----------

            qs_parent_target = self.get_qs_by_qm(qm=qm_filter)

            if isinstance(qs_parent_target, Info):

                qs_parent = qs_parent_target.parent()

                if qs_parent is None:
                    qs_parent = self.cat_model.invisibleRootItem()

                elif not isinstance(qs_parent, MyQstandardItem):
                    event.ignore()
                    print(f"Hierarchy -- drag_and_drop -- {event_type} -- not isinstance(qs_value, MyQstandardItem)")
                    return False

                qs_parent_target = qs_parent.child(qs_parent_target.row(), col_cat_value)

            # -----------

            if not self.library_possible_to_add(library_treeview=library_treeview, qs_target=qs_parent_target):
                event.ignore()
                # print(f"Hierarchy -- drag_and_drop -- {event_type} -- not possibilities")
                return False

                # -----------

            if not add:
                # print(f"Hierarchy -- drag_and_drop -- Valid !!!!!!!!")
                event.accept()
                return True

        # -----------

        if qs_parent_target.data(user_data_type) == drag_obj.ele_type:

            index_insertion = qs_parent_target.row() + 1
            qs_parent_target = qs_parent_target.parent()

            if not isinstance(qs_parent_target, MyQstandardItem):
                qs_parent_target = self.cat_model.invisibleRootItem()
                index_insertion = self.cat_model.rowCount()
        else:

            if isinstance(qs_parent_target, MyQstandardItem):
                index_insertion = qs_parent_target.get_insertion_index()
            else:
                index_insertion = self.cat_model.rowCount()

        # -----------

        for qs_list in reversed(drag_obj.qs_list):

            if len(qs_list) != col_cat_count:
                print(f"Hierarchy -- drag_and_drop -- {event_type} -- len(qs_list) != col_cat_count")
                event.ignore()
                return False

            qs_new_list = list()

            for qs in qs_list:

                qs_cloned: MyQstandardItem = qs.clone_creation(new=True)

                if not isinstance(qs, Info):
                    qs.clone_children(qs_original=qs, qs_destination=qs_cloned, new=True, link=False)

                qs_new_list.append(qs_cloned)

            self.drop_finised.emit(qs_parent_target, qs_new_list, index_insertion, -1, True, False, False, True)

        self.expand_list([qs_parent_target])

        event.accept()

        self.header_manage()

        return True

    @staticmethod
    def a___________________end___________________():
        pass


class DragObject:

    def __init__(self, qs_list: list, ele_type: str):
        super().__init__()

        self.qs_list = qs_list
        self.ele_type = ele_type


def a___________________end___________________():
    pass
