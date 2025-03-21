#!/usr/bin/python3
# -*- coding: utf-8 -*


from PyQt5.Qt import *

from catalog_manage import CatalogDatas
from main_datas import get_icon, folder_code, material_code, component_code, link_code, attribute_code
from tools import get_look_treeview, taille_police, qm_check
from ui_paste import Ui_Paste


class WidgetPaste(QWidget):

    coller_menu = pyqtSignal(str, str, str)

    def __init__(self, catalogue: CatalogDatas):
        super().__init__()

        # Création de l'interface
        self.ui = Ui_Paste()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.Popup)

        self.catalogue = catalogue

        # Model ouvrages
        self.model_coller = QStandardItemModel()

        self.ui.tree.setModel(self.model_coller)
        get_look_treeview(self.ui.tree)

        self.ui.tree.clicked.connect(self.enregistrer)

    @staticmethod
    def a___________________chargement______():
        pass

    def chargement(self):

        if self.model_coller.columnCount() == 3:
            self.ui.tree.setColumnHidden(1, True)
            self.ui.tree.setColumnHidden(2, True)

        self.ui.tree.expandAll()
        self.ui.tree.resizeColumnToContents(0)

        self.show()

    def append_titre(self, ele_type: str) -> QStandardItem:

        chemin_icone = f":/Images/{ele_type.lower()}.png"

        if ele_type == folder_code:
            title_element = self.tr("Dossier")
        elif ele_type == material_code:
            title_element = self.tr("Ouvrage")
        elif ele_type == component_code:
            title_element = self.tr("Composant")
        elif ele_type == link_code:
            title_element = self.tr("Lien")
        elif ele_type == attribute_code:
            title_element = self.tr("Attribut")
        else:
            title_element = ele_type.title()

        qs_master = QStandardItem(get_icon(chemin_icone), title_element)
        police = QStandardItem().font()

        police.setFamily("Segoe UI")
        police.setPointSize(taille_police)
        police.setBold(True)

        qs_master.setFont(police)

        self.model_coller.appendRow([qs_master, QStandardItem(ele_type), QStandardItem("0")])

        return qs_master

    def append_element(self, qs_master: QStandardItem, titre: str, type_element: str, id_ele=0):

        chemin_icone = f":/Images/{type_element.lower()}.png"

        a = self.tr("Coller")

        qs_ele = QStandardItem(get_icon(chemin_icone), f"{a} {titre}")

        police = qs_ele.font()
        police.setFamily("Segoe UI")
        police.setPointSize(taille_police)
        police.setItalic(True)

        qs_ele.setFont(police)

        qs_master.appendRow([qs_ele, QStandardItem(type_element), QStandardItem(f"{id_ele}")])

    def clear_menu(self):
        self.model_coller.clear()

    @staticmethod
    def a___________________fermeture_enregistrer______():
        pass

    def enregistrer(self):

        liste_select = self.ui.tree.selectionModel().selectedIndexes()

        if len(liste_select) != 3:
            self.close()
            return

        qm_choix = liste_select[0]
        qm_type = liste_select[1]
        qm_id = liste_select[2]

        if (not qm_check(qm_choix) or
                not qm_check(qm_type) or
                not qm_check(qm_id)):

            self.close()
            return

        choix: str = qm_choix.data()
        type_ele = qm_type.data()
        id_ele = qm_id.data()

        if not isinstance(choix, str) or not isinstance(type_ele, str) or not isinstance(id_ele, str):
            self.close()
            return

        a = self.tr("Coller")

        if qm_choix.parent().isValid() and choix.startswith(a):
            choix = choix.replace(a, "").strip()

        self.coller_menu.emit(choix, type_ele, id_ele)
        print(choix, "--", type_ele, "--", id_ele)
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
