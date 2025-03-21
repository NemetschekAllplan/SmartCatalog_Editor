#!/usr/bin/python3
# -*- coding: utf-8 -*
import re

from PyQt5.Qt import *

from catalog_manage import CatalogDatas
from hierarchy import Hierarchy
from main_datas import user_data_type, material_code, col_cat_desc, get_icon, material_icon, lock_icon
from tools import get_look_tableview, qm_check
from ui_link_add import Ui_LinkAdd
from ui_link_add_again import Ui_LinkAddAgain


class LinkAdd(QWidget):
    link_add_signal = pyqtSignal(list)

    def __init__(self, catalog: CatalogDatas, hierarchy: Hierarchy):
        super().__init__()

        self.ui = Ui_LinkAdd()
        self.ui.setupUi(self)

        self.catalog: CatalogDatas = catalog
        self.hierarchy: Hierarchy = hierarchy

        self.link_model = QStandardItemModel()

        self.link_filter = NaturalSortProxyModel()
        self.link_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.link_filter.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.link_filter.setSortLocaleAware(True)

        self.ui.links_list.setModel(self.link_filter)

        get_look_tableview(self.ui.links_list)

        self.ui.links_list.doubleClicked.connect(self.save)

        self.ui.links_list.selectionModel().selectionChanged.connect(self.add_button_manage)

        self.add_button_manage()

        self.ui.search_bar.textChanged.connect(self.link_filter.setFilterRegExp)
        self.ui.search_clear.clicked.connect(self.ui.search_bar.clear)

        self.ui.ok.clicked.connect(self.save)
        self.ui.quit.clicked.connect(self.close)

    @staticmethod
    def a___________________loading______():
        pass

    def link_creation_show(self, material_text: str):

        self.link_model.clear()

        a = self.tr("Ouvrage - Actuel")
        b = self.tr("Lien Impossible : boucle")

        search_start = self.hierarchy.cat_model.index(0, 0)

        qm_material_list = self.hierarchy.cat_model.match(search_start, user_data_type, material_code, -1,
                                                        Qt.MatchRecursive)

        forbidden_list = set()

        self.catalog.link_get_forbidden_list(material_name=material_text, forbidden_list=forbidden_list)

        for qm_val in qm_material_list:

            if not qm_check(qm_val):
                continue

            material_current = qm_val.data()

            if not isinstance(material_current, str):
                continue

            qm_parent = qm_val.parent()

            description = ""

            if qm_check(qm_parent):

                qm_desc = self.hierarchy.cat_model.index(qm_val.row(), col_cat_desc, qm_parent)

                if qm_check(qm_desc):
                    description = qm_desc.data()

            if material_current == material_text:
                message = a

            elif material_current in forbidden_list:
                message = b
            else:
                message = ""

            qs = self.creation_qs(material_name=material_current, description=description, message=message)

            self.link_model.appendRow(qs)

        self.link_filter.setSourceModel(self.link_model)
        self.link_filter.sort(0, Qt.AscendingOrder)

        self.show()

    @staticmethod
    def creation_qs(material_name: str, description: str, message="") -> QStandardItem:

        if description == "" or material_name == description:
            title = f'{material_name}'
        else:
            title = f'{material_name} - {description}'

        if message == "":

            qs = QStandardItem(get_icon(material_icon), title)
            qs.setData(material_name, user_data_type)
            qs.setData(description, Qt.UserRole + 2)

        else:

            qs = QStandardItem(get_icon(lock_icon), title)
            qs.setForeground(QColor("red"))
            qs.setEnabled(False)
            qs.setToolTip(message)

        return qs

    @staticmethod
    def a___________________boutons______():
        pass

    def add_button_manage(self):
        self.ui.ok.setEnabled(len(self.ui.links_list.selectionModel().selectedIndexes()) != 0)

    @staticmethod
    def a___________________save______():
        pass

    def save(self):

        qm_selection_list = self.ui.links_list.selectionModel().selectedIndexes()

        if len(qm_selection_list) == 0:
            return

        qm_selection_list.sort()

        link_list_add = list()

        for qm in qm_selection_list:

            if not qm_check(qm):
                continue

            material_name = qm.data(user_data_type)

            if not isinstance(material_name, str):
                continue

            description = qm.data(Qt.UserRole + 2)

            if not isinstance(description, str):
                description = ""

            link_list_add.append([material_name, description])

        self.link_add_signal.emit(link_list_add)
        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class LinKAddAgain(QWidget):
    link_creation_signal = pyqtSignal(list)
    link_open_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_LinkAddAgain()
        self.ui.setupUi(self)

        self.link_model = QStandardItemModel()

        self.link_filter = NaturalSortProxyModel()
        self.link_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.link_filter.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.link_filter.setSortLocaleAware(True)

        self.link_filter.setSourceModel(self.link_model)

        self.ui.links_list.setModel(self.link_filter)

        self.ui.links_list.doubleClicked.connect(self.save)
        self.ui.links_list.selectionModel().selectionChanged.connect(self.add_button_manage)

        self.ui.search_bar.textChanged.connect(self.link_filter.setFilterRegExp)
        self.ui.search_clear.clicked.connect(self.ui.search_bar.clear)

        self.ui.ok.clicked.connect(self.save)
        self.ui.quit.clicked.connect(self.close)

        get_look_tableview(self.ui.links_list)

        self.add_button_manage()

    def add_button_manage(self):
        self.ui.ok.setEnabled(len(self.ui.links_list.selectionModel().selectedRows(0)) != 0)

    def save(self):
        qm = self.ui.links_list.currentIndex()

        if not qm_check(qm):
            return

        title = qm.data()

        if not isinstance(title, str):
            return

        material_name = qm.data(user_data_type)

        if not isinstance(material_name, str):
            return

        description = qm.data(Qt.UserRole + 2)

        if not isinstance(description, str):
            description = ""

        self.link_creation_signal.emit([[material_name, description]])

        self.close()

    @staticmethod
    def a___________________end______():
        pass


class NaturalSortProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def lessThan(self, qm_left, qm_right):

        if not isinstance(qm_left, QModelIndex) or not isinstance(qm_right, QModelIndex):
            return super().lessThan(qm_left, qm_right)

        left_data = qm_left.data(Qt.DisplayRole)
        right_data = qm_right.data(Qt.DisplayRole)

        if not isinstance(left_data, str) or not isinstance(right_data, str):
            return super().lessThan(qm_left, qm_right)

        natural_key_left = self.natural_key(text=left_data)

        if natural_key_left is None:
            return super().lessThan(qm_left, qm_right)

        natural_key_right = self.natural_key(text=right_data)

        if natural_key_right is None:
            return super().lessThan(qm_left, qm_right)

        return natural_key_left < natural_key_right

    @staticmethod
    def natural_key(text):
        try:
            data = [(part.lower() if not part.isdigit() else int(part)) for part in re.split(r'(\d+)', text)]
        except:
            return None

        return data

    @staticmethod
    def a___________________end______():
        pass
