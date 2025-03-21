import uuid

from PyQt5.QtGui import QStandardItem

from main_datas import col_cat_value, col_cat_number, col_cat_index, user_guid, folder_code, material_code, \
    component_code, link_code, attribute_code, attribute_val_default_layer, attribute_val_default_fill, \
    attribute_val_default_room


class ClipboardItem:

    def __init__(self, title: str, qs_parent: QStandardItem, qs_list: list, guid=""):
        super().__init__()

        self.title = title

        if guid != "":
            self.guid = guid
        else:
            self.guid = str(uuid.uuid4())

        # --------

        self.qs_parent = None
        self.guid_parent = None
        self.row_parent = -1
        self.row_count_parent = 0

        self.value_parent = ""

        # --------

        self.qs_attribute_list = list()

        # --------

        self.qs_value = None
        self.guid_value = None
        self.row_value = -1
        self.row_count_value = 0

        self.value = ""

        # --------

        self.qs_value_index = None

        self.guid_value_index = None
        self.value_index = ""

        # --------

        self.qs_number = None

        self.guid_number = None
        self.number = ""

        # --------

        self.get_data(qs_parent=qs_parent, qs_attribute_list=qs_list)

    @staticmethod
    def a___________________data______():
        pass

    def get_data(self, qs_parent: QStandardItem, qs_attribute_list: list):

        # ----------------------------------

        if isinstance(qs_parent, QStandardItem):

            self.qs_parent = qs_parent

            guid_parent = self.qs_parent.data(user_guid)

            if isinstance(guid_parent, str):
                self.guid_parent = guid_parent

            self.row_parent = qs_parent.row()

            self.row_count_parent = qs_parent.rowCount()

            value_parent = qs_parent.text()

            if isinstance(value_parent, str):
                self.value_parent = value_parent

        # ----------------------------------

        if not isinstance(qs_attribute_list, list):
            return

        self.qs_attribute_list = qs_attribute_list

        # -------------

        qs_value = qs_attribute_list[col_cat_value]

        if isinstance(qs_value, QStandardItem):

            self.qs_value = qs_value

            # -------------

            guid_value = self.qs_value.data(user_guid)

            if isinstance(guid_value, str):
                self.guid_value = guid_value

            # -------------

            self.row_value = qs_value.row()
            self.row_value = qs_value.rowCount()

            # -------------

            value = qs_value.text()

            if isinstance(value, str):
                self.value = value

        # -------------

        qs_value_index = qs_attribute_list[col_cat_index]

        if isinstance(qs_value_index, QStandardItem):
            self.qs_value_index = qs_value_index

            # -------------

            guid_value_index = self.qs_value_index.data(user_guid)

            if isinstance(guid_value_index, str):
                self.guid_value_index = guid_value_index

            # -------------

            value_index = qs_value_index.text()

            if isinstance(value_index, str):
                self.value_index = value_index

        # -------------

        qs_number = qs_attribute_list[col_cat_number]

        if isinstance(qs_number, QStandardItem):
            self.qs_number = qs_number

            # -------------

            guid_number = self.qs_number.data(user_guid)

            if isinstance(guid_number, str):
                self.guid_number = guid_number

            # -------------

            number = qs_number.text()

            if isinstance(number, str):
                self.number = number

    @staticmethod
    def a___________________end______():
        pass


class ClipboardDataa:

    def __init__(self):

        super().__init__()

        self.data = list()

    def item_add(self, title: str, qs_parent: QStandardItem, qs_list: list, guid="") -> ClipboardItem:
        pass

    def item_count(self) -> int:
        pass

    def item_delete(self, guid: str) -> ClipboardItem:
        pass

    def reset(self):
        pass

    @staticmethod
    def a___________________get______():
        pass

    def get_list(self, attribute_name: str) -> list:
        pass

    def get_item_by_guid(self, guid: str) -> ClipboardItem | None:
        pass

    def get_menu_dict(self) -> dict:
        pass

    @staticmethod
    def a___________________check______():
        pass

    def guid_exists(self, guid: str) -> bool:
        pass

    @staticmethod
    def a___________________end______():
        pass


class ClipboardType(ClipboardDataa):

    def __init__(self):
        super().__init__()

        pass

    @staticmethod
    def a___________________manage______():
        pass

    def item_add(self, title: str, qs_parent: QStandardItem, qs_list: list, guid="") -> ClipboardItem:

        new_data = ClipboardItem(title=title, qs_parent=qs_parent, qs_list=qs_list, guid=guid)

        self.data.append(new_data)

        return new_data

    def item_delete(self, guid: str) -> ClipboardItem:

        item = self.get_item_by_guid(guid=guid)

        if not isinstance(item, ClipboardItem):
            print("clipboard -- ClipboardType -- item_delete -- not isinstance(item, ClipboardItem)")
            return

        self.data.remove(item)
        return item

    def item_count(self) -> int:
        return len(self.data)

    def reset(self):
        self.data.clear()

    @staticmethod
    def a___________________get______():
        pass

    def get_list(self, attribute_name: str) -> list | None:

        attribute_list = list()

        for clipboard_item in self.data:

            try:
                item_data = getattr(clipboard_item, attribute_name, None)

            except Exception as error:
                print(f"clipboard -- ClipboardType -- get_list -- error : {error}")
                return list()

            if item_data is None:
                return list()

            attribute_list.append(item_data)

        return attribute_list

    def get_item_by_guid(self, guid: str) -> ClipboardItem | None:

        for item in self.data:

            if not isinstance(item, ClipboardItem):
                print("clipboard -- ClipboardType -- get_item_by_guid -- not isinstance(item, ClipboardItem)")
                return

            if item.guid == guid:
                return item

    def get_menu_dict(self) -> dict:

        menu_dict = dict()

        for item in self.data:

            if not isinstance(item, ClipboardItem):
                print("clipboard -- ClipboardType -- get_menu_dict -- not isinstance(item, ClipboardItem)")
                return

            menu_dict[item.guid] = item.title

        return menu_dict

    @staticmethod
    def a___________________check______():
        pass

    def guid_exists(self, guid: str) -> bool:

        guid_list = self.get_list(attribute_name="guid")

        if guid_list is None:
            print("clipboard -- ClipboardType -- guid_exists -- guid_list is None")
            return False

        return guid in guid_list

    @staticmethod
    def a___________________end______():
        pass


class ClipboardFolder(ClipboardType):
    pass


class ClipboardMaterial(ClipboardType):
    pass


class ClipboardComponent(ClipboardType):
    pass


class ClipboardLink(ClipboardType):
    pass


class ClipboardAttribute(ClipboardDataa):

    def __init__(self):

        super().__init__()

        self.data = list()

        self.data_layer = list()
        self.guid_layer = ""

        self.data_fill = list()
        self.guid_fill = ""

        self.data_room = list()
        self.guid_room = ""

    @staticmethod
    def a___________________manage______():
        pass

    def item_add(self, title: str, qs_parent: QStandardItem, qs_list: list, guid="") -> ClipboardItem | None:

        clipboard_item = ClipboardItem(title=title, qs_parent=qs_parent, qs_list=qs_list, guid=guid)

        number = clipboard_item.number

        if not isinstance(number, str):
            print("clipboard -- ClipboardAttribute -- item_add -- not isinstance(number, str)")
            return

        if number == "":
            print("clipboard -- ClipboardAttribute -- item_add -- not isinstance(number, str)")
            return

        data = self.get_source(number=number)

        data.append(clipboard_item)

        if data == self.data_layer:
            self.guid_layer = clipboard_item.guid
        elif data == self.data_fill:
            self.guid_fill = clipboard_item.guid
        elif data == self.data_room:
            self.guid_room = clipboard_item.guid

        return clipboard_item

    def item_count(self, number="") -> int:

        if number == "":
            return len(self.data) + len(self.data_layer) + len(self.data_fill) + len(self.data_room)

        data = self.get_source(number=number)

        return len(data)

    def item_delete(self, guid: str) -> ClipboardItem | None:

        clipboard_item = self.get_item_by_guid(guid=guid)

        if not isinstance(clipboard_item, ClipboardItem):
            print("clipboard -- ClipboardType -- item_delete -- not isinstance(item, ClipboardItem)")
            return

        data = self.get_source(number=clipboard_item.number)

        if not isinstance(data, list):
            print("clipboard -- ClipboardType -- item_delete -- not isinstance(data, list)")
            return

        data.remove(clipboard_item)

        return clipboard_item

    def reset(self):
        self.data.clear()
        self.data_layer.clear()
        self.data_fill.clear()
        self.data_room.clear()

    @staticmethod
    def a___________________get______():
        pass

    def get_list(self, attribute_name: str) -> list:

        attribute_list = list()

        for data in [self.data, self.data_layer, self.data_fill, self.data_room]:

            for clipboard_item in data:

                try:
                    item_data = getattr(clipboard_item, attribute_name, None)

                except Exception as error:
                    print(f"clipboard -- ClipboardType -- get_list -- error : {error}")
                    return list()

                if item_data is None:
                    return list()

                attribute_list.append(item_data)

        return attribute_list

    def get_item_by_guid(self, guid: str) -> ClipboardItem | None:

        for data in [self.data, self.data_layer, self.data_fill, self.data_room]:
            for clipboard_item in data:

                if not isinstance(clipboard_item, ClipboardItem):
                    print("clipboard -- ClipboardType -- get_item_by_guid -- not isinstance(item, ClipboardItem)")
                    return

                if clipboard_item.guid == guid:
                    return clipboard_item

    def get_source(self, number: str) -> list:

        if number in attribute_val_default_layer:
            return self.data_layer

        if number in attribute_val_default_fill:
            return self.data_fill

        if number in attribute_val_default_room:
            return self.data_room

        return self.data

    def get_menu_dict(self) -> dict:

        menu_dict = dict()

        for data in [self.data, self.data_layer, self.data_fill, self.data_room]:
            for item in data:

                if not isinstance(item, ClipboardItem):
                    print("clipboard -- ClipboardType -- get_menu_dict -- not isinstance(item, ClipboardItem)")
                    return

                menu_dict[item.guid] = item.title

        return menu_dict


class ClipboardManager:

    def __init__(self):

        super().__init__()

        self.clipboards = {folder_code: ClipboardFolder(),
                           material_code: ClipboardMaterial(),
                           component_code: ClipboardComponent(),
                           link_code: ClipboardLink(),
                           attribute_code: ClipboardAttribute()}

        self.clipboards_cut = {folder_code: ClipboardFolder(),
                               material_code: ClipboardMaterial(),
                               component_code: ClipboardComponent(),
                               link_code: ClipboardLink(),
                               attribute_code: ClipboardAttribute()}

        self.current = ""

    @staticmethod
    def a___________________clipboard______():
        pass

    def get_clipboard(self, ele_type: str, reset=False) -> ClipboardType | ClipboardAttribute | None:

        clipboard = self.clipboards.get(ele_type)

        if not isinstance(clipboard, (ClipboardType, ClipboardAttribute)):
            return

        if reset:
            clipboard.reset()

        return clipboard

    def get_clipboard_cut(self, ele_type: str, reset=False) -> ClipboardType | ClipboardAttribute | None:

        clipboard = self.clipboards_cut.get(ele_type)

        if not isinstance(clipboard, (ClipboardType, ClipboardAttribute)):
            return

        if reset:
            clipboard.reset()

        return clipboard

    def get_all_clipboard(self, ele_type: str, reset=False) -> tuple:

        clipboard = self.get_clipboard(ele_type=ele_type, reset=reset)
        clipboard_cut = self.get_clipboard(ele_type=ele_type, reset=reset)

        return clipboard, clipboard_cut

    def reset_all(self) -> bool:

        self.current = ""

        for clipboard in self.clipboards:

            if not isinstance(clipboard, ClipboardType):
                print("clipboard -- reset_all -- not isinstance(clipboard, ClipboardType)")
                return False

            clipboard.reset()

        return True

    @staticmethod
    def a___________________end______():
        pass
