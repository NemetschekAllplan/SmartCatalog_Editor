#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from main_datas import attribute_add_icon, delete_icon, get_icon, cut_icon, move_up_icon, move_down_icon, refresh_icon
from main_datas import attribute_icon, user_guid, merge_icon
from hierarchy import MyQstandardItem

index_action = Qt.UserRole + 2

history_add_ele = "add_ele"
history_cut_ele = "cut_ele"
history_del_ele = "del_ele"
history_move_ele = "move_ele"
history_move_material = "move_material"

history_change_icon = "modify_icon"

history_add_attribute = "add_attribute"
history_modify_attribute = "modifiy_attribute"
history_del_attribute = "del_attribute"

history_library_synchro = "library_synchro"

user_data_type = Qt.UserRole + 1

nb_max = 50


class ActionInfo:
    def __init__(self, action_type: str, action_name: str, action_icon="", action_tooltips=""):

        self.action_id = id(self)
        self.action_type = action_type
        self.action_name = action_name
        self.action_icon = get_icon(action_icon)

        if action_tooltips == "":
            self.action_tooltips = action_name
        else:
            self.action_tooltips = action_tooltips


class ActionAddEle(ActionInfo):
    def __init__(self, action_name: str, qs_current: MyQstandardItem):
        super().__init__(action_type=history_add_ele, action_name=action_name, action_tooltips=action_name)

        self.guid_parent = ""
        self.guid_current = qs_current.data(user_guid)

        self.row_current = qs_current.row()
        self.qs_list = list()

        # -------------------

        self.action_icon = qs_current.icon()


class ActionDelEle(ActionInfo):

    def __init__(self, action_name: str, guid_parent: str, qs_current: MyQstandardItem, row_current: int,
                 qs_list: list):
        super().__init__(action_type=history_del_ele,
                         action_name=action_name,
                         action_icon=delete_icon,
                         action_tooltips=action_name)

        self.guid_parent = guid_parent
        self.guid_current = qs_current.data(user_guid)
        self.row_current = row_current
        self.qs_list = qs_list


class ActionMoveEle(ActionInfo):

    def __init__(self, action_name: str, guid_current: str, row_current: int, row_new: int):

        super().__init__(action_type=history_move_ele, action_name=action_name, action_tooltips=action_name)

        self.guid_current = guid_current
        self.row_current = row_current
        self.row_new = row_new

        # -------------------

        if row_new > row_current:

            self.action_icon = get_icon(move_up_icon)
        else:
            self.action_icon = get_icon(move_down_icon)


class ActionCutEle(ActionInfo):
    def __init__(self, action_name: str, guid_parent_new: str, guid_current: str, row_new: int):
        super().__init__(action_type=history_cut_ele,
                         action_name=action_name,
                         action_icon=cut_icon,
                         action_tooltips=action_name)

        self.guid_parent_new = guid_parent_new
        self.guid_current = guid_current
        self.row_new = row_new


class ActionMoveMaterial(ActionInfo):

    def __init__(self, action_name: str, guid_parent: str, guid_new_folder: str, guid_material: str):
        super().__init__(action_type=history_move_material,
                         action_name=action_name,
                         action_icon=merge_icon,
                         action_tooltips=action_name)

        self.guid_parent = guid_parent
        self.guid_new_folder = guid_new_folder
        self.guid_material = guid_material


class ActionChangeIcon(ActionInfo):

    def __init__(self, action_name: str, guid_current: str, icon_new: QIcon):
        super().__init__(action_type=history_change_icon,
                         action_name=action_name,
                         action_icon=icon_new,
                         action_tooltips=action_name)

        self.guid_current = guid_current

        self.icon_new = icon_new


class AttributeData:

    def __init__(self, guid_current: str, row_current: int, qs_list: list):
        self.guid_current = guid_current
        self.row_current = row_current
        self.qs_list = qs_list


class ActionAddAttribute(ActionInfo):

    def __init__(self, action_name: str, guid_parent: str, attribute_data: list):
        super().__init__(action_type=history_add_attribute,
                         action_name=action_name,
                         action_icon=attribute_add_icon,
                         action_tooltips=action_name)

        self.guid_parent = guid_parent
        self.attribute_data = attribute_data


class ActionDelAttribute(ActionInfo):
    def __init__(self, action_name: str, guid_parent: str, attribute_data: list):
        super().__init__(action_type=history_del_attribute,
                         action_name=action_name,
                         action_icon=delete_icon,
                         action_tooltips=action_name)

        self.guid_parent = guid_parent
        self.attribute_data = attribute_data


class AttributeCutData:
    def __init__(self, number_current: str,

                 guid_original: str, row_original: int, qs_list_original: list,
                 value_original: str, value_index_original: str,

                 guid_select=None, row_select=None, qs_list_select=None,
                 value_select=None, value_index_select=None,

                 attribute_delete=False):

        super().__init__()

        self.number_current = number_current
        self.attribute_delete = attribute_delete

        # -------------

        self.guid_original = guid_original
        self.row_original = row_original
        self.qs_list_original = qs_list_original
        self.value_original = value_original
        self.value_index_original = value_index_original

        # -------------

        self.guid_select = guid_select
        self.row_select = row_select
        self.qs_list_select = qs_list_select
        self.value_select = value_select
        self.value_index_select = value_index_select

        # -------------


class ActionCutAttribute(ActionInfo):
    def __init__(self, action_name: str, guid_parent_original: str, guid_parent_select: str, attribute_data: list):
        super().__init__(action_type=history_del_attribute,
                         action_name=action_name,
                         action_icon=delete_icon,
                         action_tooltips=action_name)

        self.guid_parent_original = guid_parent_original
        self.guid_parent_select = guid_parent_select
        self.attribute_data = attribute_data


class AttributeModifyData:
    def __init__(self, number_current: str, value_new: str, value_index_new="-1", guid_desc=None):
        super().__init__()

        self.number_current = number_current
        self.value_new = value_new
        self.value_index_new = value_index_new
        self.guid_desc = guid_desc


class ActionModifyAttribute(ActionInfo):
    def __init__(self, action_name: str, action_tooltips: str, guid_parent: str, attribute_data: list):
        super().__init__(action_type=history_modify_attribute,
                         action_name=action_name,
                         action_icon=attribute_icon,
                         action_tooltips=action_tooltips)

        self.guid_parent = guid_parent
        self.attribute_data = attribute_data


class ActionLibrarySynchro(ActionInfo):

    def __init__(self, action_name: str, library_synchro_list: list):
        super().__init__(action_type=history_library_synchro,
                         action_name=action_name,
                         action_icon=refresh_icon,
                         action_tooltips=action_name)

        self.library_synchro_list = library_synchro_list


class LibraryData:

    def __init__(self, is_creation: bool, guid_parent: str, guid_current: str,
                 value_new="", value_index_new="-1", guid_desc=None):
        super().__init__()

        self.is_creation = is_creation
        self.guid_parent = guid_parent
        self.guid_current = guid_current

        self.value_new = value_new
        self.value_index_new = value_index_new

        self.guid_desc = guid_desc

        # --------------

        self.row_current = -1
        self.qs_list = list()


# Classe pour stocker et gérer les actions
class ActionsData:
    def __init__(self):
        self.action_dict = dict()

    def action_add_ele(self, action_name: str, qs_current: MyQstandardItem):

        action = ActionAddEle(action_name=action_name,
                              qs_current=qs_current)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_del_ele(self, action_name: str, guid_parent: str, qs_current: MyQstandardItem, row_current: int,
                       qs_list: list):

        action = ActionDelEle(action_name=action_name,
                              guid_parent=guid_parent,
                              qs_current=qs_current,
                              row_current=row_current,
                              qs_list=qs_list)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_move_ele(self, action_name: str, guid_current: str, row_current: int, row_new: int):

        action = ActionMoveEle(action_name=action_name,
                               guid_current=guid_current,
                               row_current=row_current,
                               row_new=row_new)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_move_materials(self, action_name: str, guid_parent: str, guid_new_folder: str, guid_material: str):

        action = ActionMoveMaterial(action_name=action_name,
                                    guid_parent=guid_parent,
                                    guid_new_folder=guid_new_folder,
                                    guid_material=guid_material)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_cut_ele(self, action_name: str, guid_parent_new: str, guid_current: str, row_new: int):

        action = ActionCutEle(action_name=action_name,
                              guid_parent_new=guid_parent_new,
                              guid_current=guid_current,
                              row_new=row_new)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_change_icon(self, action_name: str, guid_current: str, icon_new: QIcon):

        action = ActionChangeIcon(action_name=action_name,
                                  guid_current=guid_current,
                                  icon_new=icon_new)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_add_attribute(self, action_name: str, guid_parent: str, attribute_data: dict):

        action = ActionAddAttribute(action_name=action_name, guid_parent=guid_parent, attribute_data=attribute_data)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_modify_attribute(self, action_name: str, tooltips: str,
                                guid_parent: str, attribute_data: list):

        action = ActionModifyAttribute(action_name=action_name,
                                       action_tooltips=tooltips,
                                       guid_parent=guid_parent,
                                       attribute_data=attribute_data)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_del_attribute(self, action_name: str, guid_parent: str, attribute_data: dict):

        action = ActionDelAttribute(action_name=action_name, guid_parent=guid_parent, attribute_data=attribute_data)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_cut_attribute(self, action_name: str, guid_parent_original: str, guid_parent_select: str,
                             attribute_data: list):

        action = ActionCutAttribute(action_name=action_name,
                                    guid_parent_original=guid_parent_original,
                                    guid_parent_select=guid_parent_select,
                                    attribute_data=attribute_data)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_library_synchro(self, action_name: str, library_synchro_list: list):

        action = ActionLibrarySynchro(action_name=action_name, library_synchro_list=library_synchro_list)

        self.action_dict[action.action_id] = action

        self.action_manage_max()

    def action_get_list(self) -> list:
        return list(self.action_dict.keys())

    def supprimer_action(self, action_id: int) -> bool:

        if action_id not in self.action_dict:
            return False

        self.action_dict.pop(action_id)

        return True

    def action_manage_max(self):

        item_count = len(self.action_dict)

        if item_count > nb_max:
            liste_key = list(self.action_dict)

            liste_a_sup = liste_key[:len(liste_key) - nb_max]

            for key in liste_a_sup:
                self.action_dict.pop(key)

    def action_clear(self):
        self.action_dict.clear()

    @staticmethod
    def a___________________end______():
        pass
