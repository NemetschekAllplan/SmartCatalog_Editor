#!/usr/bin/python3
# -*- coding: utf-8 -*
import glob
import os.path
from datetime import datetime

from PyQt5.Qt import *
from catalog_manage import CatalogDatas

from main_datas import get_icon, copy_icon, open_icon
from ui_backup_restore import Ui_BackupRestore
from tools import afficher_message as msg
from tools import application_title, move_window_tool, qm_check, get_look_tableview
from tools import copy_to_clipboard, find_folder_path, open_folder, open_file, MyContextMenu


class BackupRestore(QWidget):

    def __init__(self, asc, catalog_folder: str, catalog_name: str, langue: str):
        super().__init__()

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------
        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.catalog: CatalogDatas = self.asc.catalog

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_BackupRestore()
        self.ui.setupUi(self)

        get_look_tableview(self.ui.table)

        # -----------------------------------------------
        # Variable
        # -----------------------------------------------

        self.catalog_folder = catalog_folder
        self.catalog_name = catalog_name
        self.langue = langue

        # -----------------------------------------------
        # Model
        # -----------------------------------------------

        self.backup_model = QStandardItemModel()
        self.backup_model.setHorizontalHeaderLabels([self.tr("Index"), self.tr("Dernier enregistrement")])

        self.ui.table.setModel(self.backup_model)

        if self.backup_model_creation():

            # -----------------------------------------------
            # Signal buttons
            # -----------------------------------------------

            self.ui.table.selectionModel().selectionChanged.connect(self.button_manage)
            self.ui.table.customContextMenuRequested.connect(self.backup_menu_show)

            self.ui.ok.clicked.connect(self.backup_restore)
            self.ui.quit.clicked.connect(self.close)

            # -----------------------------------------------
            # Show
            # -----------------------------------------------

            move_window_tool(widget_parent=self.asc, widget_current=self)

            self.show()

        else:

            msg(titre=application_title,
                message="Aucune sauvegarde trouvé.")

    @staticmethod
    def a___________________model_creation______():
        pass

    def backup_model_creation(self) -> bool:

        backup_folder = f"{self.catalog_folder}backup\\"

        if not os.path.exists(backup_folder):
            print("BackupRestore -- backup_model_creation -- not os.path.exists(backup_folder)")
            return False

        file_list = glob.glob(f"{backup_folder}{self.catalog_name}*.xml")

        if len(file_list) == 0:
            print("BackupRestore -- backup_model_creation -- len(file_list) == 0")
            return False

        indexes_list = list()

        for backup_path in file_list:

            filename = backup_path.replace(f"{backup_folder}{self.catalog_name}", "").replace(".xml", "")

            seconds = os.path.getmtime(backup_path)
            date_complet_modif = datetime.fromtimestamp(seconds)

            if self.langue == "FR":
                modif_date = date_complet_modif.strftime("%d-%m-%Y - %H:%M:%S")
            else:
                modif_date = date_complet_modif.strftime("%m-%d-%Y - %I:%M:%S %p")

            if "-" in filename:
                try:
                    indice_str = filename[-2:]

                    int(indice_str)

                    if indice_str in indexes_list:
                        print("BackupRestore -- get_backup_list -- indice_str in backup_filename_dict")
                        continue

                except Exception as error:
                    print(f"get_backup_list -- error -- {error}")
                    continue

                if not os.path.exists(f"{backup_folder}{self.catalog_name} - {indice_str}.xml"):
                    continue

            else:

                if "00" in indexes_list:
                    print("BackupRestore -- get_backup_list -- 00 in backup_filename_dict")
                    continue

                indice_str = "00"

                if not os.path.exists(f"{backup_folder}{self.catalog_name}.xml"):
                    continue

            indexes_list.append(indice_str)

            qs_index = QStandardItem(indice_str)
            qs_index.setToolTip(backup_path)

            qs_date = QStandardItem(modif_date)
            qs_date.setToolTip(backup_path)

            self.backup_model.appendRow([qs_index, qs_date])

        if self.backup_model.rowCount() == 0:
            return False

        self.backup_model.sort(0, Qt.AscendingOrder)

        self.ui.table.setCurrentIndex(self.backup_model.index(0, 0))

        return True

    @staticmethod
    def a___________________menu______():
        pass

    def backup_menu_show(self, point: QPoint):

        qm_selected = self.ui.table.indexAt(point)

        if not qm_check(qm_selected):
            print("BackupRestore -- backup_menu_show -- not qm_check(qm_selected)")
            return

        file_path = qm_selected.data(Qt.ToolTipRole)
        folder_path = find_folder_path(file_path)

        menu = MyContextMenu()  # No help

        if not os.path.exists(folder_path):
            print("BackupRestore -- backup_menu_show -- not os.path.exists(folder_path)")
            return

        menu.add_title(title=self.windowTitle())

        menu.add_action(qicon=get_icon(open_icon),
                        title=self.tr("Ouvrir le dossier"),
                        action=lambda: open_folder(folder_path))

        if os.path.exists(file_path):
            menu.addSeparator()

            menu.add_action(qicon=get_icon(open_icon),
                            title=self.tr("Ouvrir le fichier"),
                            action=lambda: open_file(file_path))

            menu.add_action(qicon=get_icon(copy_icon),
                            title=self.tr("Copier le chemin dans le presse-papier"),
                            action=lambda: copy_to_clipboard(file_path))

        menu.exec_(self.ui.table.mapToGlobal(point))

    @staticmethod
    def a___________________button_manage______():
        pass

    def button_manage(self):
        select_list = self.ui.table.selectionModel().selectedRows()

        self.ui.ok.setEnabled(len(select_list) != 0)

    @staticmethod
    def a___________________backup_restore______():
        pass

    def backup_restore(self):

        select_list = self.ui.table.selectionModel().selectedRows()

        if len(select_list) != 1:
            print("BackupRestore -- backup_restore -- len(select_list) != 1")
            return

        qm_backup_selected = select_list[0]

        if not qm_check(qm_backup_selected):
            print("BackupRestore -- backup_restore -- not qm_check(qm_backup_selected)")
            return

        if msg(titre=application_title,
               message=self.tr("Voulez-vous vraiment restaurer cette sauvegarde?\n"),
               icone_question=True,
               type_bouton=QMessageBox.Ok | QMessageBox.Cancel,
               defaut_bouton=QMessageBox.Cancel) != QMessageBox.Ok:
            return

        backup_path = qm_backup_selected.data(Qt.ToolTipRole)

        if not isinstance(backup_path, str):
            print("BackupRestore -- backup_restore -- not isinstance(backup_path, str)")
            return

        column_index = qm_backup_selected.column()

        if column_index != 0:
            qm_backup_selected = self.backup_model.index(qm_backup_selected.row(), 0)

            if not qm_check(qm_backup_selected):
                print("BackupRestore -- backup_restore -- not qm_check(qm_backup_selected)")
                return

        backup_index = qm_backup_selected.data()

        if not isinstance(backup_index, str):
            print("BackupRestore -- backup_restore -- not isinstance(backup_index, str)")
            return

        self.close()

        result = self.catalog.backup_restore_action(backup_path=backup_path, backup_index=backup_index)

        if result == "":
            txt1 = self.tr("Le catalogue a été restauré.")
            txt2 = self.tr("Pour annuler cette restauration, vous devez restaurer la sauvegarde n°")

            msg(titre=application_title,
                message=f"{txt1}\n{txt2} {backup_index}",
                icone_valide=True)
            return

        msg(titre=application_title,
            message=self.tr("Une erreur est survenue."),
            icone_critique=True,
            details=result,
            afficher_details=True)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            self.close()
            return

        if event.key() == Qt.Key_Escape:
            self.close()
            return

    def changeEvent(self, event: QEvent):

        if event.type() == QEvent.WindowStateChange:
            move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    @staticmethod
    def a___________________end______():
        pass
