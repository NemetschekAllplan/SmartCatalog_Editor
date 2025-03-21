#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from allplan_manage import AllplanDatas
from main_datas import get_icon, material_icon, component_icon, user_data_type, component_code, material_code
from tools import get_look_tableview, qm_check, MyContextMenu
from ui_attribute_link import Ui_AttributeLink


class AttributeLink(QWidget):
    material_open = pyqtSignal(str)
    component_open = pyqtSignal(str, str)

    def __init__(self, allplan, link_model):
        super().__init__()

        # Chargement du widget + setup
        self.ui = Ui_AttributeLink()
        self.ui.setupUi(self)

        self.allplan: AllplanDatas = allplan

        self.material_name = ""

        self.ui.bt_afficher.clicked.connect(self.material_show)

        self.link_model = link_model

        self.ui.liste_composants.setModel(self.link_model)

        get_look_tableview(self.ui.liste_composants)

        self.ui.liste_composants.expandAll()

        self.link_manage_header()

        self.ui.liste_composants.doubleClicked.connect(self.component_show)

        self.ui.liste_composants.customContextMenuRequested.connect(self.menu_show)

    def material_show(self):
        self.material_open.emit(self.material_name)

    def component_show(self, qm: QModelIndex):

        if not qm_check(qm):
            return

        if qm.column() != 0:
            qm = self.link_model.index(qm.row(), 0)
            if not qm_check(qm):
                return

        item_text = qm.data()

        if not isinstance(item_text, str):
            return

        if item_text == "":
            return

        item_type = qm.data(user_data_type)

        if item_type == component_code:

            qm_parent = qm.parent()

            if qm_check(qm_parent) is None:
                parent_name = self.material_name
            else:

                parent_name = qm_parent.data()

            if not isinstance(parent_name, str):
                return

            self.component_open.emit(parent_name, item_text)

        elif item_type == material_code:
            self.material_open.emit(item_text)

    def menu_show(self, point: QPoint):

        qm = self.ui.liste_composants.indexAt(point)

        if not qm_check(qm):
            return

        if qm.parent() is None:
            material_name = self.material_name
        else:
            material_name = qm.data()

            if not isinstance(material_name, str):
                return

        item_type = qm.data(user_data_type)

        point = QPoint(point.x(), point.y() + 35)

        menu = MyContextMenu()

        menu.add_title(title=self.tr("Lien"))

        menu.add_action(qicon=get_icon(material_icon),
                        title=self.tr("Afficher l'ouvrage"),
                        action=self.material_open.emit(material_name))

        if item_type == component_code:
            menu.add_action(qicon=get_icon(component_icon),
                            title=self.tr('Afficher le composant'),
                            action=lambda: self.component_show(qm=qm))

        menu.exec_(self.ui.liste_composants.mapToGlobal(point))

    def link_manage_header(self):

        row_count = self.link_model.rowCount()

        if row_count == 0:
            return

        size_now = self.ui.liste_composants.header().sectionSize(0)

        self.ui.liste_composants.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        size_after = self.ui.liste_composants.header().sectionSize(0)

        if size_after < size_now:
            self.ui.liste_composants.header().setSectionResizeMode(0, QHeaderView.Interactive)
            self.ui.liste_composants.header().resizeSection(0, size_now)
        else:
            self.ui.liste_composants.header().setSectionResizeMode(0, QHeaderView.Interactive)

    @staticmethod
    def a___________________end______():
        pass
