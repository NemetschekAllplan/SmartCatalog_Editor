#!/usr/bin/python3
# -*- coding: utf-8 -*
import json
import os.path
from datetime import datetime
from typing import Tuple

from attribute_layer import AttributeLayer
from room_attribute import AttributeRoom
from attribute_filling import AttributeFilling
from allplan_manage import *
from attribute_code import AttributeCode
from attribute_name import AttributeName
from convert_manage import ConvertBcmMaterial, ConvertKukat, ConvertNevarisXml, ConvertTemplate
from history_manage import *
from message import *
from tools import afficher_message as msg
from tools import get_catalog_setting_display_file, catalog_xml_region, read_catalog_paths_file, catalog_xml_date
from tools import get_catalog_setting_folder, get_catalog_setting_path_file, find_new_title, settings_list
from tools import make_backup, settings_save_value, settings_get, find_folder_path
from tools import recherche_chemin_bcm, find_filename, write_catalog_paths_file, move_window_tool, qm_check
from tools import catalog_xml_find_all
from ui_main_windows import Ui_MainWindow


class CatalogDatas(QObject):
    formula_color_change_signal = pyqtSignal()
    formula_size_change_signal = pyqtSignal(int)
    close_library_signal = pyqtSignal()

    def __init__(self, asc):
        super().__init__()

        self.asc = asc
        self.ui: Ui_MainWindow = self.asc.ui

        # ---------

        self.hierarchy: Hierarchy = self.ui.hierarchy

        # todo clipboard - library drop
        # self.hierarchy.drop_finised.connect(self.coller_update)

        # ---------

        self.allplan: AllplanDatas = self.asc.allplan

        # ---------

        self.loading: LoadingSplash = self.asc.loading

        self.catalog_path = ""

        self.catalog_region = ""

        self.catalog_folder = ""
        self.catalog_name = ""
        self.catalog_settings_folder = ""
        self.catalog_setting_path_file = ""
        self.catalog_setting_display_file = ""

        # self.hierarchy.cat_model = QStandardItemModel()
        # col_cat_count = 0

        self.change_made = False
        self.undo_list = ActionsData()
        self.redo_list = ActionsData()
        self.library_synchro_list = list()

        # ---------------------------------------
        # FILTER TYPE
        # ---------------------------------------

        self.bcm_path = recherche_chemin_bcm()
        self.allmetre_path = settings_get(library_setting_file, "path_alltop")

        # ---------------------------------------
        # Loading Clipboard
        # ---------------------------------------

        self.clipboard_folder = ClipboardDatas(folder_code)
        self.clipboard_folder_cut = ClipboardDatas(folder_code)

        self.clipboard_material = ClipboardDatas(material_code)
        self.clipboard_material_cut = ClipboardDatas(material_code)

        self.clipboard_component = ClipboardDatas(component_code)
        self.clipboard_component_cut = ClipboardDatas(component_code)

        self.clipboard_link = ClipboardDatas(link_code)
        self.clipboard_link_cut = ClipboardDatas(link_code)

        self.clipboard_attribute = ClipboardDatas(attribute_code)
        self.clipboard_attribute_cut = ClipboardDatas(attribute_code)

        self.clipboard_current = ""

    @staticmethod
    def a___________________catalog_creation___________________():
        pass

    def catalog_create_new(self, catalog_folder: str, catalog_name, user_folder: str, version_allplan: str,
                           attribute_number: str) -> bool:

        # ------------------------------
        # Catalog path
        # ------------------------------

        catalog_path = f"{catalog_folder}{catalog_name}.xml"

        # ------------------------------
        # display path
        # ------------------------------

        if not self.catalog_create_path_file(catalog_folder=catalog_folder,
                                             catalog_name=catalog_name,
                                             user_data_path=user_folder,
                                             allplan_version=version_allplan,
                                             attribute_default=attribute_number):
            return False

        # ------------------------------
        # display creation
        # ------------------------------

        catalog_settings_folder = get_catalog_setting_folder(catalog_folder=catalog_folder)

        if not catalog_settings_folder:
            print("catalog_manage -- catalog_create_new -- not catalog_settings_folder")
            return False

        catalog_setting_display_file = get_catalog_setting_display_file(catalog_settings_folder=catalog_settings_folder,
                                                                        catalog_name=catalog_name)

        if not catalog_setting_display_file:
            print("catalog_manage -- catalog_create_new -- not catalog_setting_display_file")
            return False

        return self.catalog_create_new_action(version_allplan="1.0",
                                              catalog_path=catalog_path,
                                              catalog_setting_display_file=catalog_setting_display_file)

    def catalog_create_new_action(self, version_allplan: str, catalog_path: str, catalog_setting_display_file) -> bool:

        region = catalog_xml_region(current_language=self.allplan.langue)

        version_xml = version_allplan
        # version_xml = catalog_xml_version(allplan_version=version_allplan)

        date_modif = catalog_xml_date(current_language=self.allplan.langue)

        a = self.tr("Dernier enregistrement")
        new = self.tr("Nouveau dossier")

        root = etree.Element('AllplanCatalog',
                             Region=region,
                             version=version_xml)

        root.set("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation",
                 "../Xsd/AllplanCatalog.xsd")

        root_expand = etree.Element('Smart-Catalog')

        etree.SubElement(root, 'Node', name=f"------------------- {a} : {date_modif} ------------------- ")
        etree.SubElement(root, 'Node', name=new)

        etree.SubElement(root_expand, 'Node', name=f"------------------- {a} : {date_modif} ------------------- ")
        etree.SubElement(root_expand, 'Node', name=new)

        a = self.tr("Une erreur est survenue.")

        try:
            catalogue = etree.tostring(root,
                                       pretty_print=True,
                                       xml_declaration=True,
                                       encoding='UTF-8').decode()

            sauvegarde_expand = etree.tostring(root_expand,
                                               pretty_print=True,
                                               xml_declaration=True,
                                               encoding='UTF-8').decode()

        except Exception as erreur:
            msg(titre=application_title,
                message=f'{a} : {catalog_path}',
                icone_critique=True,
                details=f"{erreur}")
            return False

        try:

            with open(catalog_path, "w", encoding="utf_8_sig") as file:
                file.write(catalogue)

        except IOError as erreur:

            msg(titre=application_title,
                message=f'{a} : {catalog_path}',
                icone_critique=True,
                details=f"{erreur}")
            return False

        except Exception as erreur:
            msg(titre=application_title,
                message=f'{a} : {catalog_path}',
                icone_critique=True,
                details=f"{erreur}")
            return False

        try:
            with open(catalog_setting_display_file, "w", encoding="utf_8") as file:

                file.write(sauvegarde_expand)

        except OSError as erreur:

            msg(titre=application_title,
                message=f"{a} : {catalog_setting_display_file}",
                icone_avertissement=True,
                details=f"{erreur}")
            return False

        return True

    @staticmethod
    def a___________________catalog_path_file___________________():
        pass

    def catalog_define_paths(self, catalog_path: str) -> bool:

        # -----------------------------
        #         catalog_folder
        # -----------------------------

        catalog_folder = find_folder_path(file_path=catalog_path)

        if not catalog_folder:
            print("catalog_manage -- catalog_define_paths -- not catalog_folder")
            return False

        # -----------------------------
        #         catalog_name
        # -----------------------------

        catalog_name = find_filename(file_path=catalog_path)

        if not catalog_name:
            print("catalog_manage -- catalog_define_paths -- not catalog_name")
            return False

        # -----------------------------
        #    catalog_settings_folder
        # -----------------------------

        catalog_settings_folder = get_catalog_setting_folder(catalog_folder=catalog_folder)

        if not catalog_settings_folder:
            print("catalog_manage -- catalog_define_paths -- not catalog_settings_folder")
            return False

        # -----------------------------
        #    catalog_setting_path_file
        # -----------------------------

        catalog_setting_path_file = get_catalog_setting_path_file(catalog_settings_folder=catalog_settings_folder,
                                                                  catalog_name=catalog_name)

        if not catalog_setting_path_file:
            print("catalog_manage -- catalog_define_paths -- not catalog_setting_path_file")
            return False

        # -----------------------------
        #    catalog_setting_display_file
        # -----------------------------

        catalog_setting_display_file = get_catalog_setting_display_file(catalog_settings_folder=catalog_settings_folder,
                                                                        catalog_name=catalog_name)

        if not catalog_setting_display_file:
            print("catalog_manage -- catalog_define_paths -- not catalog_setting_display_file")
            return False

        # -----------------------------
        #    copy all paths
        # -----------------------------

        self.catalog_path = catalog_path

        self.catalog_folder = catalog_folder
        self.catalog_name = catalog_name

        self.catalog_settings_folder = catalog_settings_folder
        self.catalog_setting_path_file = catalog_setting_path_file
        self.catalog_setting_display_file = catalog_setting_display_file

        return True

    @staticmethod
    def catalog_create_path_file(catalog_folder: str, catalog_name: str,
                                 user_data_path: str, allplan_version: str,
                                 attribute_default: str) -> bool:

        """
        Creation of the catalog setting file : CatalogName_path.ini
        :param catalog_folder: path of catalog's folder
        :param catalog_name: name of catalog
        :param user_data_path: path of user's datas
        :param allplan_version: name of version Allplan
        :param attribute_default: attribute_number
        :return: success (bool)
        """

        # -----------------------------
        # Définie the path of settings
        # -----------------------------

        catalog_settings_folder = get_catalog_setting_folder(catalog_folder=catalog_folder)

        if not catalog_settings_folder:
            print("catalog_manage -- catalog_create_path_file -- not catalog_settings_folder")
            return False

        # -----------------------------
        # Define the path of the file : CatalogName_path.ini
        # -----------------------------

        catalog_setting_path_file = get_catalog_setting_path_file(catalog_settings_folder=catalog_settings_folder,
                                                                  catalog_name=catalog_name)

        if not catalog_setting_path_file:
            print("catalog_manage -- catalog_create_path_file -- not catalog_setting_path_file")
            return False

        # -----------------------------
        # write the file
        # -----------------------------

        if not write_catalog_paths_file(catalog_setting_path_file=catalog_setting_path_file,
                                        user_data_path=user_data_path,
                                        allplan_version=allplan_version,
                                        attribute_default=attribute_default):
            print("catalog_manage -- catalog_create_path_file -- not write_catalog_paths_file")
            return False

        return True

    def catalog_load_path_file(self, catalog_setting_path_file) -> bool:
        """
        Load
        :return:
        """

        # -----------------------------
        # find default settings
        # -----------------------------

        version_allplan_default = self.allplan.versions_list[0]

        if version_allplan_default == "99" and len(self.allplan.versions_list) > 1:
            version_allplan_default = self.allplan.versions_list[1]

        for annee in reversed(self.allplan.versions_list):

            if annee in catalog_setting_path_file:
                version_allplan_default = annee
                break

        if version_allplan_default not in self.allplan.version_datas:
            return False

        version_obj = self.allplan.version_datas[version_allplan_default]

        if not isinstance(version_obj, AllplanPaths):
            return False

        folder_std = version_obj.std_path
        folder_prj = version_obj.prj_path

        if folder_std == "" or folder_prj == "":
            print("catalog_manage -- catalog_load_path_file -- folder_std is empty or folder_prj is empty")
            return False

        # -----------------------------
        # load settings
        # -----------------------------

        datas = read_catalog_paths_file(catalog_setting_path_file=catalog_setting_path_file,
                                        folder_std=folder_std,
                                        folder_prj=folder_prj,
                                        allplan_version_default=version_allplan_default,
                                        allplan_version_list=self.allplan.versions_list)

        # -----------------------------

        self.allplan.version_allplan_current = datas.get("allplan_version", version_allplan_default)

        allplan_paths = self.allplan.version_datas.get(self.allplan.version_allplan_current)

        if not isinstance(allplan_paths, AllplanPaths):
            print("catalog_manage -- catalog_load_path_file -- not isinstance(allplan_paths, AllplanPaths)")
            return False

        allplan_version = datas.get("allplan_version", version_allplan_default)
        attribute_default = attribut_default_obj.check_number(datas.get("attribute_default"))

        # -----------------------------
        # Apply settings
        # -----------------------------

        user_data_path = datas.get("user_data_path", folder_std)

        if "\\STD\\" in user_data_path.upper():
            if user_data_path != allplan_paths.std_path:
                user_data_path = allplan_paths.std_path

                write_catalog_paths_file(catalog_setting_path_file=catalog_setting_path_file,
                                         user_data_path=user_data_path,
                                         allplan_version=allplan_version,
                                         attribute_default=attribute_default)

        self.allplan.catalog_user_path = user_data_path
        self.allplan.user_attributes_xml_path = f"{user_data_path}Xml\\"

        # -----------------------------

        self.allplan.version_allplan_current = allplan_version

        # -----------------------------

        attribut_default_obj.set_current(number=attribute_default)

        # -----------------------------

        if help_mode:
            self.ui.statusbar.showMessage('Allplan 202X -- C:\\Data\\Allplan\\202X\\STD\\')

        else:

            self.ui.statusbar.showMessage(f'Allplan {self.allplan.version_allplan_current} -- '
                                          f'{self.allplan.catalog_user_path}')

        return True

    @staticmethod
    def catalog_is_locked(catalog_path: str) -> bool:

        if not os.path.exists(catalog_path):
            print("catalog_manage -- catalog_is_locked -- not os.path.exists(catalog_path)")
            return False

        folder_path = find_folder_path(file_path=catalog_path)
        file_name = find_filename(file_path=catalog_path)

        lock_file_path = f"{folder_path}ASC_settings\\{file_name}.lck"

        if not os.path.exists(lock_file_path):
            return False

        try:

            with open(lock_file_path, 'r', encoding="Utf-8") as file:

                config: list = json.load(file)

                if not isinstance(config, list):
                    print("catalog_manage -- catalog_is_locked -- not isinstance(config, list)")
                    return False

                if len(config) == 0:
                    return False

                if len(config) > 1:
                    return True

                username_use = config[0]

                computer_name = os.environ['COMPUTERNAME']
                username = os.environ['USERNAME']

                user_current = f"{computer_name} -- {username}"

                if username_use != user_current:
                    return True

        except Exception as error:
            print(f"catalog_manage -- catalog_is_locked -- error : {error}")

        return False

    def catalog_lock_file(self, catalog_path: str, lock: bool) -> bool:

        if not os.path.exists(catalog_path):
            print("catalog_manage -- catalog_lock_file -- not os.path.exists(catalog_path)")
            return False

        used = self.catalog_is_locked(catalog_path=catalog_path)

        folder_path = find_folder_path(file_path=catalog_path)
        file_name = find_filename(file_path=catalog_path)

        # ------------

        lock_file_path = f"{folder_path}ASC_settings\\{file_name}.lck"

        config = list()

        if os.path.exists(lock_file_path):

            try:

                with open(lock_file_path, 'r', encoding="Utf-8") as file:

                    config: list = json.load(file)

                    if not isinstance(config, list):
                        print("catalog_manage -- catalog_is_locked -- not isinstance(config, list)")
                        config = list()

            except Exception as error:
                print(f"catalog_manage -- catalog_lock_file -- error : {error}")
                config = list()

        # ------------

        computer_name = os.environ['COMPUTERNAME']
        username = os.environ['USERNAME']

        user_current = f"{computer_name} -- {username}"

        # ------------
        #  Lock
        # ------------

        if lock:

            if used:
                msg(titre=application_title,
                    message=self.tr("Attention, ce catalogue est déjà utilisé par un autre SmartCatalog Editor"),
                    icone_lock=True)

            if user_current not in config:

                config.append(user_current)

            else:
                return True

        # ------------
        #  Unlock
        # ------------

        else:

            if user_current in config:
                config.remove(user_current)

            # ------------ Remove empty file

            if len(config) == 0:

                if not os.path.exists(lock_file_path):
                    return True

                try:
                    os.remove(lock_file_path)
                    return True

                except Exception as error:
                    print(f"catalog_manage -- catalog_is_locked -- error : {error}")

                return False

        # ------------
        #  Update file
        # ------------

        try:

            with open(lock_file_path, 'w', encoding="Utf-8") as file:

                json.dump(config, file, ensure_ascii=False, indent=2)
                return True

        except Exception as error:
            print(f"catalog_manage -- catalog_lock_file -- error : {error}")

        return False

    @staticmethod
    def a___________________catalog_user_path___________________():
        pass

    def catalog_user_path_check(self, user_path: str):

        version_allplan = self.allplan.version_allplan_current

        if version_allplan not in self.allplan.version_datas:
            return

        version_obj = self.allplan.version_datas[version_allplan]

        if not isinstance(version_obj, AllplanPaths):
            return

        folder_std = version_obj.std_path
        folder_prj = version_obj.prj_path

        if user_path is None:
            print("catalog_manage -- catalog_user_path_check -- user_path is None")
            return self.catalog_user_path_define(user_path=folder_std)

        if user_path == "":
            print("catalog_manage -- catalog_user_path_check -- user_path is empty")
            return self.catalog_user_path_define(user_path=folder_std)

        user_path = user_path.strip()

        if os.path.exists(user_path):
            return self.catalog_user_path_define(user_path=user_path)

        try:
            project_name = os.path.basename(os.path.normpath(user_path))

            # dernier_backslash = chemin_utilisateur.rfind('\\')
            #
            # nom_projet = chemin_utilisateur[dernier_backslash + 1:-1]

            if project_name.endswith(".prj"):

                tmp_path = f"{folder_prj}{project_name}"

                if os.path.exists(tmp_path):
                    return self.catalog_user_path_define(tmp_path)

        except Exception as error:
            print(f"catalog_manage -- catalog_user_path_check -- error : {error}")
            return self.catalog_user_path_define(folder_std)

        return self.catalog_user_path_define(user_path=folder_std)

    def catalog_user_path_define(self, user_path: str):

        folder_changed = self.allplan.catalog_user_path != user_path

        self.allplan.catalog_user_path = user_path
        self.allplan.user_attributes_xml_path = f"{user_path}Xml\\"

        print(f"catalog_manage -- catalog_user_path_define -- catalog_user_path ==> "
              f"{self.allplan.catalog_user_path}")

        print(f"catalog_manage -- catalog_user_path_define -- user_attributes_xml_path ==> "
              f"{self.allplan.user_attributes_xml_path}")

        self.ui.statusbar.showMessage(f'Allplan {self.allplan.version_allplan_current} -- '
                                      f'{self.allplan.catalog_user_path}')

        return folder_changed

    @staticmethod
    def a___________________catalog_loading___________________():
        pass

    def catalog_load_start(self, catalog_path: str, loader="xml", chemin_bdd=""):

        # ------------------------
        # Define all paths
        # ------------------------
        if self.catalog_path != "":
            self.catalog_lock_file(catalog_path=self.catalog_path, lock=False)

        self.catalog_lock_file(catalog_path=catalog_path, lock=True)

        self.close_library_signal.emit()

        # ------------------------
        # Define all paths
        # ------------------------

        self.catalog_define_paths(catalog_path=catalog_path)

        # ------------------------
        # Clear attributes (ui)
        # ------------------------

        self.ui.attributes_detail.clear()

        self.undo_list.action_clear()
        self.redo_list.action_clear()

        # ------------------------
        # clear current search (ui)
        # ------------------------

        if self.ui.search_error_bt.isChecked():
            self.ui.search_error_bt.setChecked(False)
            self.ui.search_error_bt.clicked.emit()

        if self.ui.search_line.text() != "":
            self.ui.search_line.setText("")

        print("------------------------------------------------------------")

        # ------------------------
        # Show avertissements message
        # ------------------------

        catalog_name = self.catalog_name.lower()

        if catalog_name == "test":
            a = self.tr("Il est déconseillé d'utiliser 'test' comme nom de catalogue")
            b = self.tr("Allplan ne voudra pas l'afficher")

            msg(titre=application_title,
                message=f"{a}.\n{b}.")

        elif len(catalog_name) > 27:
            a = self.tr("Le nom de catalogue ne doit pas dépassé 27 caractères")
            b = self.tr("actuellement")
            c = self.tr("Allplan ne voudra pas l'afficher")

            msg(titre=application_title,
                message=f"{a} \n"
                        f"({b} : {len(catalog_name)}.\n"
                        f"{c}.")

        # ------------------------
        # Show "Loading"
        # ------------------------

        move_window_tool(widget_parent=self.asc, widget_current=self.loading, always_center=True)

        if loader == "Allmétré" or loader == "BCM" or loader == "KUKAT":

            a = self.tr("Conversion de la base de données")

            self.loading.launch_show(f"{a} : {loader} ...")

        else:

            self.loading.launch_show(self.tr("Chargement en cours ..."))

        # ------------------------
        # Load setting file : CatalogName_path.ini
        # ------------------------

        if not self.catalog_load_path_file(catalog_setting_path_file=self.catalog_setting_path_file):
            print("catalog_manage -- catalog_load_start -- not self.catalog_load_path_file")
            return

        # ------------------------
        # Load datas Allplan
        # ------------------------

        self.allplan.allplan_loading()

        # ------------------------
        # Initialisation of catalog loading
        # ------------------------

        if loader == "BCM":
            catalog_loading = ConvertBcmMaterial(allplan=self.allplan,
                                                 file_path=chemin_bdd,
                                                 bdd_title=self.catalog_name,
                                                 conversion=True)

        elif loader == "KUKAT":
            catalog_loading = ConvertKukat(allplan=self.allplan,
                                           file_path=chemin_bdd,
                                           bdd_title=self.catalog_name,
                                           conversion=True)

        elif loader == "NEVARIS":
            catalog_loading = ConvertNevarisXml(allplan=self.allplan,
                                                file_path=chemin_bdd,
                                                bdd_title=self.catalog_name,
                                                conversion=True)

        else:

            catalog_loading = CatalogLoad(allplan=self.allplan,
                                          file_path=self.catalog_path,
                                          bdd_title=self.catalog_name)

        print(f"catalog_manage -- catalog_load_start -- starting load catalog : {self.catalog_name}")

        # ------------------------

        material_list.clear()
        catalog_loading.material_list = material_list

        material_upper_list.clear()
        catalog_loading.material_upper_list = material_upper_list

        link_list.clear()
        catalog_loading.link_list = link_list

        material_with_link_list.clear()
        catalog_loading.material_with_link_list = material_with_link_list

        # ------------------------
        # Connecting end signals
        # ------------------------

        catalog_loading.loading_completed.connect(self.hierarchy.loading_model)
        catalog_loading.loading_completed.connect(self.catalog_load_end)

        catalog_loading.number_error_signal.connect(self.catalog_number_error_show)
        catalog_loading.errors_signal.connect(self.catalog_error_show)

        # ------------------------
        # start
        # ------------------------

        catalog_loading.run()

    def catalog_load_end(self):

        self.loading.hide()

        # --------------

        settings_save_value(file_name=app_setting_file, key_name="path_catalog", value=self.catalog_path)

        catalog_opened_list = settings_list(file_name=cat_list_file, ele_add=self.catalog_path)

        self.asc.open_list_manage(catalog_opened_list=catalog_opened_list)

        # --------------

        # Modification du titre
        self.asc.catalog_load_title()

        # --------------

        # suppression du ctrl+z / ctrl+y
        self.undo_list.action_clear()
        self.redo_list.action_clear()
        self.undo_button_manage()
        self.redo_button_manage()

        # --------------

        self.change_made = False

    def catalog_number_error_show(self, number_error_list: list):

        if len(number_error_list) == 0:
            return

        number_error_list.sort(key=int)

        txt1 = self.tr("Des attributs n'existent pas dans le chemin de données choisi,")
        txt2 = self.tr("Voulez-vous supprimer ces attributs du catalogue?")

        response = msg(titre=application_title,
                       message=f"{txt1}<br><b>{txt2}<b>",
                       icone_avertissement=True,
                       type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                       defaut_bouton=QMessageBox.No,
                       bt_ok=self.tr("Tous supprimer"),
                       bt_no=self.tr("Modifier le chemin de données"),
                       details=number_error_list,
                       afficher_details=True)

        if response == QMessageBox.Ok:
            self.attribute_delete_unknown()
            return

        if response == QMessageBox.No:
            self.asc.new_catalog_widget.personnalisation(modify=True)

    def catalog_error_show(self, errors_list: list):

        if len(errors_list) != 0:
            msg(titre=application_title,
                message=self.tr("Des erreurs ont été détectées lors de la lecture du catalogue"),
                icone_avertissement=True,
                details=errors_list,
                afficher_details=True)

    @staticmethod
    def a___________________catalogue_save___________________():
        pass

    def catalog_save_ask(self, exlcude_default_attribute=""):

        if self.hierarchy.cat_model.rowCount() == 0:
            return True

        print(f"catalog_manage -- demande_enregistrer -- modification_en_cours == {self.change_made}")

        if not self.change_made:
            return True

        result = msg(titre=application_title,
                     message=self.tr("Voulez-vous sauvegarder votre travail?"),
                     type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                     defaut_bouton=QMessageBox.Ok,
                     icone_sauvegarde=True)

        if result == QMessageBox.Ok:

            if self.ui.search_error_bt.isChecked():
                self.ui.search_error_bt.setChecked(False)
                self.ui.search_error_bt.clicked.emit()

            self.catalog_save_action(exlcude_default_attribute=exlcude_default_attribute)
            self.change_made = False
            return True

        if result == QMessageBox.No:

            if self.ui.search_error_bt.isChecked():
                self.ui.search_error_bt.setChecked(False)
                self.ui.search_error_bt.clicked.emit()

            self.change_made = False
            return True

        return False

    def catalog_save(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            self.asc.app_save_datas()
        else:
            self.asc.app_save_all()

    def catalog_save_action(self, exlcude_default_attribute="") -> bool:

        used = self.catalog_is_locked(catalog_path=self.catalog_path)

        if used:
            if msg(titre=application_title,
                   message=self.tr("Attention, ce catalogue est déjà utilisé par un autre SmartCatalog Editor"),
                   icone_critique=True,
                   type_bouton=QMessageBox.Ok | QMessageBox.Cancel,
                   bt_ok=self.tr("Enregistrer"),
                   defaut_bouton=QMessageBox.Cancel) != QMessageBox.Ok:
                return False

        tps_start = time.perf_counter()

        move_window_tool(widget_parent=self.asc, widget_current=self.loading, always_center=True)

        self.loading.launch_show(self.tr("Enregistrement du catalogue ..."))

        CatalogSave(asc=self.asc, catalog=self, allplan=self.allplan,
                    exlcude_default_attribute=exlcude_default_attribute)

        self.asc.catalog_load_title()

        self.loading.hide()

        self.change_made = False

        print(f"enregistrement terminé en {time.perf_counter() - tps_start}sec")

        return True

    @staticmethod
    def a___________________catalog_modification___________________():
        pass

    def catalog_modif_manage(self):

        if self.change_made:
            return

        # print("catalog_manage -- gestion_modification")
        self.change_made = True

    @staticmethod
    def a___________________clipboard___________________():
        pass

    def clipboard_clear_all(self):

        self.clipboard_folder = ClipboardDatas(folder_code)
        self.clipboard_folder_cut = ClipboardDatas(folder_code)

        self.clipboard_material = ClipboardDatas(material_code)
        self.clipboard_material_cut = ClipboardDatas(material_code)

        self.clipboard_component = ClipboardDatas(component_code)
        self.clipboard_component_cut = ClipboardDatas(component_code)

        self.clipboard_link = ClipboardDatas(link_code)
        self.clipboard_link_cut = ClipboardDatas(link_code)

        self.clipboard_attribute = ClipboardDatas(attribute_code)
        self.clipboard_attribute_cut = ClipboardDatas(attribute_code)

        self.clipboard_current = ""

    def get_clipboard(self, ele_type: str, reset_clipboard=False) -> tuple:

        if ele_type == folder_code:
            if reset_clipboard:
                self.clipboard_folder = ClipboardDatas(folder_code)
                self.clipboard_folder_cut = ClipboardDatas(folder_code)
            return self.clipboard_folder, self.clipboard_folder_cut

        if ele_type == material_code:
            if reset_clipboard:
                self.clipboard_material = ClipboardDatas(material_code)
                self.clipboard_material_cut = ClipboardDatas(material_code)
            return self.clipboard_material, self.clipboard_material_cut

        if ele_type == component_code:
            if reset_clipboard:
                self.clipboard_component = ClipboardDatas(component_code)
                self.clipboard_component_cut = ClipboardDatas(component_code)
            return self.clipboard_component, self.clipboard_component_cut

        if ele_type == link_code:

            if reset_clipboard:
                self.clipboard_link = ClipboardDatas(link_code)
                self.clipboard_link_cut = ClipboardDatas(link_code)
            return self.clipboard_link, self.clipboard_link_cut

        if ele_type == attribute_code:

            if reset_clipboard:
                self.clipboard_attribute = ClipboardDatas(attribute_code)
                self.clipboard_attribute_cut = ClipboardDatas(attribute_code)
            return self.clipboard_attribute, self.clipboard_attribute_cut

        return None, None

    @staticmethod
    def a___________________catalog_search___________________():
        pass

    def search_current_selection_text(self) -> str:

        qm_selection_list = self.hierarchy.get_qm_model_selection_list()

        if len(qm_selection_list) != 1:
            return ""

        qm_current: QModelIndex = qm_selection_list[0]

        if not qm_check(qm_current):
            print("catalog_manage -- search_current_selection_text -- not qm_check(qm_current)")
            return ""

        text_current: str = qm_current.data()

        actionbar_widget: QWidget = self.ui.actionbar

        try:
            last_focused_widget = QApplication.focusWidget()

            if last_focused_widget is None:
                return text_current

            if last_focused_widget == actionbar_widget:
                return text_current

            parent_current = last_focused_widget.parent()

            if parent_current is None:
                return text_current

        except Exception as error:
            print(f"catalog_manage -- search_current_selection_text -- error : {error}")
            return text_current

        liste_details: QListWidget = self.ui.attributes_detail

        nb_attributs = liste_details.count()
        liste_valeur_attr = [type_nom, type_code, type_ligne, type_date, type_texture, type_formule, type_combo]

        for index_row in range(nb_attributs):

            listwidgetitem: QListWidgetItem = liste_details.item(index_row)

            type_widget = listwidgetitem.data(user_data_type)

            if type_widget == type_checkbox or type_widget == type_lien:
                continue

            widget = liste_details.itemWidget(listwidgetitem)

            if widget is None:
                print("catalog_manage -- search_current_selection_text -- widget is None")
                continue

            if parent_current != widget:
                continue

            if type_widget in liste_valeur_attr:
                return self.search_selected_text(widget=widget.ui.value_attrib, text_current=text_current)

            if type_widget == type_layer:

                widget: AttributeLayer

                widget_layer: QComboBox = widget.ui.value_141

                if widget_layer != last_focused_widget:
                    return text_current

                return self.search_selected_text(widget=widget_layer, text_current=text_current)

            if type_widget == type_fill:

                widget: AttributeFilling
                widget_style: QComboBox = widget.ui.style

                if widget_style == last_focused_widget:
                    return self.search_selected_text(widget=widget_style, text_current=text_current)

                widget_surface: QLineEdit = widget.ui.surface

                if widget_surface == last_focused_widget:
                    return self.search_selected_text(widget=widget_surface, text_current=text_current)

            if type_widget == type_room:

                widget: AttributeRoom

                widget_valeur: QLineEdit = widget.ui.valeur_fav

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                widget_valeur: QLineEdit = widget.ui.valeur_231

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                widget_valeur: QLineEdit = widget.ui.valeur_235

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                widget_valeur: QLineEdit = widget.ui.valeur_232

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                widget_valeur: QLineEdit = widget.ui.valeur_233

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                return text_current

        return text_current

    @staticmethod
    def search_selected_text(widget: QWidget, text_current: str) -> str:

        if isinstance(widget, QLineEdit):

            text_selected = widget.selectedText()

            if text_selected != "":
                return text_selected

            text_selected = widget.text()

            if text_selected != "":
                return text_selected

            return text_current

        if isinstance(widget, QComboBox):

            text_selected = widget.lineEdit().selectedText()

            if text_selected != "":
                return text_selected

            text_selected = widget.currentText()

            if text_selected != "":
                return text_selected

            return text_current

        if isinstance(widget, QPlainTextEdit):

            text_selected = widget.textCursor().selectedText()

            if text_selected != "":
                return text_selected

            text_selected = widget.toPlainText()

            if text_selected != "":
                return text_selected

            return text_current
        return text_current

    def get_attributes_list(self) -> list:

        search_start = self.hierarchy.cat_model.index(0, col_cat_number)

        search = self.hierarchy.cat_model.match(search_start, user_data_type, attribute_code, -1,
                                                Qt.MatchExactly | Qt.MatchRecursive)

        attributes_list = list()

        if len(search) == 0:
            return attributes_list

        exclude_list = ["83", "207"]

        for qm_number in search:

            if not qm_check(qm_number):
                continue

            number = qm_number.data()

            if not isinstance(number, str):
                continue

            if number in exclude_list:
                continue

            if number in attribute_val_default_layer:
                number = attribute_val_default_layer_first

            elif number in attribute_val_default_fill:
                number = attribute_val_default_fill_first

            elif number in attribute_val_default_room:
                number = attribute_val_default_room_first

            if number in attributes_list:
                continue

            attributes_list.append(number)

        # -----------------------------

        if self.asc.attributes_order_col == 0:

            try:

                attributes_list.sort(key=int, reverse=self.asc.attributes_order == 1)

            except Exception:
                pass

        else:

            attributes_list.sort(reverse=self.asc.attributes_order == 1)

        return attributes_list

    @staticmethod
    def a___________________material_manage___________________():
        pass

    def get_qm_filter_by_material_name(self, material_name: str) -> list:

        if not isinstance(material_name, str) or material_name == "":
            return list()

        search_start: QModelIndex = self.hierarchy.cat_model.index(0, 0)

        qm_list: list = self.hierarchy.cat_model.match(search_start,
                                                       Qt.DisplayRole,
                                                       material_name,
                                                       -1,
                                                       Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_list) == 0:
            print("catalog_manage -- ouvrage_rechercher_qmodelindex_filtre -- recherche == 0")
            return list()

        qm_filter_list = list()

        for qm_model in qm_list:

            if qm_model.data(user_data_type) != material_code:
                continue

            qm_filter = self.hierarchy.map_to_filter(qm=qm_model)

            if qm_filter is None:
                print("catalog_manage -- ouvrage_rechercher_qmodelindex_filtre -- qmodelindex_filtre is None")
                continue

            qm_filter_list.append(qm_filter)

        return qm_filter_list

    def get_qs_by_material_name(self, material_name: str):

        if not isinstance(material_name, str) or material_name == "":
            return

        search_start: QModelIndex = self.hierarchy.cat_model.index(0, 0)

        qm_list: list = self.hierarchy.cat_model.match(search_start,
                                                       Qt.DisplayRole,
                                                       material_name,
                                                       -1,
                                                       Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_list) == 0:
            print("catalog_manage -- ouvrage_rechercher_qmodelindex_filtre -- recherche == 0")
            return

        for qm in qm_list:

            if qm.data(user_data_type) != material_code:
                continue

            qs: MyQstandardItem = self.hierarchy.get_qs_by_qm(qm=qm)

            if qs is None:
                print("catalog_manage -- ouvrage_rechercher_qstandarditem -- qmodelindex_filtre is None")
                continue

            return qs

    def goto_material(self, material_name: str):

        if self.ui.search_bt.isChecked():
            self.ui.search_bt.setChecked(False)
            self.ui.search_bt.clicked.emit()

        elif self.ui.search_error_bt.isChecked():
            self.ui.search_error_bt.setChecked(False)
            self.ui.search_error_bt.clicked.emit()

        search_qm = self.get_qm_filter_by_material_name(material_name)

        if len(search_qm) == 0:
            msg(titre=application_title,
                message=self.tr("L'ouvrage n'a pas été trouvé."),
                icone_avertissement=True)
            return

        qm_filter: QModelIndex = search_qm[0]

        self.hierarchy.select_list(selected_list=[qm_filter])

    def goto_component(self, material_name: str, component_name: str):

        if self.ui.search_bt.isChecked():
            self.ui.search_bt.setChecked(False)
            self.ui.search_bt.clicked.emit()

        elif self.ui.search_error_bt.isChecked():
            self.ui.search_error_bt.setChecked(False)
            self.ui.search_error_bt.clicked.emit()

        qs_material = self.get_qs_by_material_name(material_name)

        if not isinstance(qs_material, Material):
            msg(titre=application_title,
                message=self.tr("L'ouvrage n'a pas été trouvé."),
                icone_avertissement=True)
            return

        qs_component = qs_material.get_component_by_name(component_name)

        if qs_component is None:
            msg(titre=application_title,
                message=self.tr("Le composant n'a pas été trouvé."),
                icone_avertissement=True)
            return

        qm_filter = self.hierarchy.map_to_filter(qm=qs_component.index())

        if not qm_check(qm_filter):
            msg(titre=application_title,
                message=self.tr("Le composant n'a pas été trouvé."),
                icone_avertissement=True)
            return

        self.hierarchy.select_list(selected_list=[qm_filter])

    def material_refresh_look(self, material_name: str):

        if not isinstance(material_name, str) or material_name == "":
            return

        search_start: QModelIndex = self.hierarchy.cat_model.index(0, 0)

        qm_list: list = self.hierarchy.cat_model.match(search_start,
                                                       Qt.DisplayRole,
                                                       material_name,
                                                       -1,
                                                       Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_list) == 0:
            print("catalog_manage -- ouvrage_rechercher_qmodelindex_filtre -- recherche == 0")
            return

        for qm in qm_list:

            qs: MyQstandardItem = self.hierarchy.get_qs_by_qm(qm=qm)

            if not isinstance(qs, Material):
                continue

            value: str = qs.text()

            link_count = link_list.count(value)

            used_by_links_count = qs.used_by_links_count != 0

            if not used_by_links_count and link_count == 0:
                return

            if link_count == 0:
                qs.set_material_classic()
                return

            qs.set_material_look(used_by_links_count=link_count)
            return

    def material_update_link_number(self, material_name: str):

        link_count = link_list.count(material_name)

        search_start: QModelIndex = self.hierarchy.cat_model.index(0, 0)

        qm_list: list = self.hierarchy.cat_model.match(search_start,
                                                       Qt.DisplayRole,
                                                       material_name,
                                                       -1,
                                                       Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_list) == 0:
            return

        for qm in qm_list:
            qm: QModelIndex

            qs: MyQstandardItem = self.hierarchy.get_qs_by_qm(qm=qm)

            if not isinstance(qs, Material):
                continue

            qs.set_material_look(link_count)

    def material_code_renamed(self, code_before: str, code_after: str):

        if not isinstance(code_before, str) or not isinstance(code_after, str):
            print("catalog_manage -- material_code_renamed -- not isinstance(code_before, str)")
            return

        if code_before == code_after:
            return

        # -----------------
        # Update links
        # -----------------

        search_start: QModelIndex = self.hierarchy.cat_model.index(0, 0)

        qm_model_list: list = self.hierarchy.cat_model.match(search_start,
                                                             Qt.DisplayRole,
                                                             code_before,
                                                             -1,
                                                             Qt.MatchExactly | Qt.MatchRecursive)

        for qm in qm_model_list:

            qs: MyQstandardItem = self.hierarchy.get_qs_by_qm(qm=qm)

            if not isinstance(qs, Link):
                continue

            qs.setText(code_after)

        # -----------------
        # Update link_list
        # -----------------

        if code_before in link_list:
            link_list[:] = [x if x != code_before else code_after for x in link_list]

        # -----------------
        # Update material_list
        # -----------------

        if code_before in material_list:

            code_index = material_list.index(code_before)

            if code_index < 0:
                print("catalog_manage -- material_code_renamed -- material_list -- index_code < 0")
            else:
                material_list[code_index] = code_after

        code_before = code_before.upper()
        code_after = code_after.upper()

        # -----------------
        # Update material_upper_list
        # -----------------

        if code_before in material_upper_list:

            code_index = material_upper_list.index(code_before)

            if code_index < 0:
                print("catalog_manage -- material_code_renamed -- material_upper_list -- index_code_upper < 0")
            else:
                material_upper_list[code_index] = code_after

        # -----------------
        # Update material_with_link_list
        # -----------------

        if code_before in material_with_link_list:

            code_index = material_with_link_list.index(code_before)

            if code_index < 0:
                print("catalog_manage -- material_code_renamed -- index_code < 0")
            else:
                material_with_link_list[code_index] = code_after

    def material_desc_changed(self, material_name: str, link_desc_after: str):

        if not isinstance(material_name, str) or not isinstance(link_desc_after, str):
            print("catalog_manage -- material_desc_changed -- not isinstance(material_name, str)")
            return

        search_start: QModelIndex = self.hierarchy.cat_model.index(0, 0)

        qm_model_list: list = self.hierarchy.cat_model.match(search_start,
                                                             Qt.DisplayRole,
                                                             material_name,
                                                             -1,
                                                             Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_model_list) == 0:
            print("catalog_manage -- material_desc_changed -- len(qm_model_list) == 0")
            return

        for qm in qm_model_list:

            qs_val: MyQstandardItem = self.hierarchy.get_qs_by_qm(qm=qm)

            if not isinstance(qs_val, Link):
                continue

            qs_parent = qs_val.parent()

            if not isinstance(qs_parent, Material):
                print("catalog_manage -- material_desc_changed -- not isinstance(qs_parent, Material)")
                continue

            qs_desc = qs_parent.child(qs_val.row(), col_cat_desc)

            if not isinstance(qs_desc, Info):
                print("catalog_manage -- material_desc_changed -- not isinstance(qs_desc, Info)")
                continue

            qs_desc.setText(link_desc_after)

    def material_add(self, qs: MyQstandardItem):

        if isinstance(qs, Component):
            return True

        if isinstance(qs, Link):

            link_name = qs.text()

            link_list.append(link_name)

            qs_material = qs.parent()

            if not isinstance(qs_material, Material):
                print("catalog_manage -- material_add -- not isinstance(qs_material, Material)")
                return False

            material_name = qs_material.text()

            material_name = material_name.upper()

            if material_name not in material_with_link_list:
                material_with_link_list.append(material_name)

            self.material_update_link_number(material_name=link_name)

            return True

        if isinstance(qs, Folder):

            search_start = self.hierarchy.cat_model.index(0, col_cat_value, qs.index())

            search = self.hierarchy.cat_model.match(search_start, user_data_type, material_code, -1,
                                                    Qt.MatchExactly | Qt.MatchRecursive)

            if len(search) == 0:
                return True

        elif isinstance(qs, Material):
            search = [qs.index()]

        else:
            print("catalog_manage -- material_add -- not isinstance(qs, MyQstandardItem)")
            return False

        for qm_material in search:

            if not qm_check(qm_material):
                print("catalog_manage -- material_add -- not qm_check(qm_material)")
                continue

            material_name = qm_material.data()

            if not isinstance(material_name, str):
                print("catalog_manage -- material_add -- not isinstance(material_name, str)")
                continue

            if material_name in material_list:
                material_list.append(material_name)

            if material_name.upper() in material_upper_list:
                material_upper_list.append(material_name.upper())

            search_link_start = self.hierarchy.cat_model.index(0, col_cat_value, qm_material)

            search_link = self.hierarchy.cat_model.match(search_link_start, user_data_type, link_code, -1,
                                                         Qt.MatchExactly)

            if len(search_link) == 0:
                continue

            if material_name.upper() in material_with_link_list:
                material_with_link_list.append(material_name.upper())

            for qm_link in search_link:

                if not qm_check(qm_link):
                    print("catalog_manage -- material_add -- not qm_check(qm_link)")
                    continue

                link_name = qm_link.data()

                if link_name in link_list:
                    link_list.append(link_name)
                    self.material_update_link_number(link_name)

        return True

    def material_is_deletable(self, qs: MyQstandardItem) -> bool:
        """
        Check if deletable ONLY
        :param qs: current QStandardItem
        :return: delete is possible or not
        """

        if isinstance(qs, Component) or isinstance(qs, Link):
            return True

        if isinstance(qs, Folder):

            search_start = self.hierarchy.cat_model.index(0, col_cat_value, qs.index())

            search = self.hierarchy.cat_model.match(search_start, user_data_type, material_code, -1,
                                                    Qt.MatchExactly | Qt.MatchRecursive)

            if len(search) == 0:
                return True

        elif isinstance(qs, Material):
            search = [qs.index()]

        else:
            print("catalog_manage -- material_is_deletable -- not isinstance(qs, MyQstandardItem)")
            return False

        for qm_material in search:

            if not qm_check(qm_material):
                print("catalog_manage -- material_is_deletable -- not qm_check(qm_material)")
                continue

            material_name = qm_material.data()

            if not isinstance(material_name, str):
                print("catalog_manage -- material_is_deletable -- not isinstance(material_name, str)")
                continue

            if material_name in link_list:
                return False

        return True

    def material_delete(self, qs: MyQstandardItem) -> bool:
        """
        Check if deletable and delete
        :param qs: current QStandardItem
        :return: delete is Ok or not
        """

        if not self.material_is_deletable(qs=qs):
            return False

        # ----------

        if isinstance(qs, Component):
            return True

        # ----------

        if isinstance(qs, Link):

            search_link_start = self.hierarchy.cat_model.index(0, col_cat_value)

            link_name = qs.text()

            if link_name in link_list:
                link_list.remove(link_name)
            else:
                print("catalog_manage -- material_delete -- link_name not in link_list")

            search_link = self.hierarchy.cat_model.match(search_link_start, Qt.DisplayRole, link_name, -1,
                                                         Qt.MatchExactly | Qt.MatchRecursive)

            if len(search_link) == 0:
                print("catalog_manage -- material_delete -- len(search_link) == 0")
                return False

            for qm_current in search_link:

                if not qm_check(qm_current):
                    print("catalog_manage -- material_delete -- not qm_check(qm_current)")
                    continue

                if qm_current.data(user_data_type) != material_code:
                    continue

                material_name = qm_current.data()

                self.material_update_link_number(material_name=material_name)

                search_link_start = self.hierarchy.cat_model.index(0, col_cat_value, qm_current)

                search_link = self.hierarchy.cat_model.match(search_link_start, user_data_type, link_code, -1,
                                                             Qt.MatchExactly)

                if len(search_link) == 0:
                    continue

                if material_name.upper() not in material_with_link_list:
                    print("catalog_manage -- material_delete -- not isinstance(qs_material, Material)")
                    continue

                material_with_link_list.remove(material_name.upper())

                self.material_update_link_number(material_name=material_name)
                continue

            return True

        # ----------

        if isinstance(qs, Folder):

            search_start = self.hierarchy.cat_model.index(0, col_cat_value, qs.index())

            search = self.hierarchy.cat_model.match(search_start, user_data_type, material_code, -1,
                                                    Qt.MatchExactly | Qt.MatchRecursive)

            if len(search) == 0:
                return True

        # ----------

        elif isinstance(qs, Material):
            search = [qs.index()]

        # ----------

        else:
            print("catalog_manage -- material_delete -- not isinstance(qs, MyQstandardItem)")
            return False

        for qm_material in search:

            if not qm_check(qm_material):
                print("catalog_manage -- material_delete -- not qm_check(qm_material)")
                continue

            material_name = qm_material.data()

            if not isinstance(material_name, str):
                print("catalog_manage -- material_delete -- not isinstance(material_name, str)")
                continue

            if material_name in material_list:
                material_list.remove(material_name)

            if material_name.upper() in material_upper_list:
                material_upper_list.remove(material_name.upper())

            search_link_start = self.hierarchy.cat_model.index(0, col_cat_value, qm_material)

            search_link = self.hierarchy.cat_model.match(search_link_start, user_data_type, link_code, -1,
                                                         Qt.MatchExactly)

            if len(search_link) == 0:
                continue

            if material_name.upper() in material_with_link_list:
                material_with_link_list.remove(material_name.upper())

            for qm_link in search_link:

                if not qm_check(qm_link):
                    print("catalog_manage -- material_delete -- not qm_check(qm_link)")
                    continue

                link_name = qm_link.data()

                if link_name in link_list:
                    link_list.remove(link_name)
                    self.material_update_link_number(material_name=link_name)

        return True

    def material_to_new_folder(self) -> bool:

        selection_qs_list = self.hierarchy.get_qs_selection_list()

        if len(selection_qs_list) == 0:
            print("catalog_manage -- material_to_new_folder -- len(selection_qs_list) == 0")
            return False

        selection_qs_list.sort()

        return self.material_to_new_folder_action(qs_material_list=selection_qs_list)

    def material_to_new_folder_action(self, qs_material_list: list, guid_new_folder=None) -> bool:

        if not isinstance(qs_material_list, list):
            print("catalog_manage -- material_to_new_folder_action -- len(selection_qs_list) == 0")
            return False

        # -------------

        expanded_list = list()
        qs_parent_dict = dict()

        # -------------
        # New folder to receive materials
        # -------------

        for qs_material in qs_material_list:

            if not isinstance(qs_material, Material):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(qs, Material)")
                return False

            qs_parent = qs_material.parent()

            if not isinstance(qs_parent, Folder):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(qs_parent, Folder)")
                return False

            # -------------

            material_name = qs_material.text()

            if not isinstance(material_name, str) or material_name == "":
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(material_name, str)")
                return False

            # -------------

            qs_desc = qs_parent.child(qs_material.row(), col_cat_desc)

            if not isinstance(qs_desc, Info):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(qs_desc, Info)")
                return False

            # -------------

            description = qs_desc.text()

            if not isinstance(description, str):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(description, str)")
                return False

            # -------------

            guid_parent = qs_parent.data(user_guid)

            if guid_parent in qs_parent_dict:
                continue

            folder_qs_list = self.allplan.creation.folder_line(value=material_name, description=description)

            if not isinstance(folder_qs_list, list):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(folder_qs_list, list)")
                return False

            if len(folder_qs_list) != col_cat_count:
                print("catalog_manage -- material_to_new_folder_action -- len(folder_qs_list) != col_cat_count")
                return False

            qs_folder_new = folder_qs_list[col_cat_value]

            if not isinstance(qs_folder_new, Folder):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(qs_folder_new, Folder)")
                return False

            expanded_list.append(qs_folder_new)
            qs_parent.appendRow(folder_qs_list)

            # -------------

            qs_parent_dict[guid_parent] = qs_folder_new

        # -------------
        # Déplacement
        # -------------

        for qs_material in qs_material_list:

            if not isinstance(qs_material, Material):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(qs, Material)")
                return False

            qs_parent = qs_material.parent()

            if not isinstance(qs_parent, Folder):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(qs_parent, Folder)")
                return False

            # -------------

            guid_parent = qs_parent.data(user_guid)

            if guid_parent not in qs_parent_dict:
                continue

            # -------------

            qs_folder_new = qs_parent_dict[guid_parent]

            if not isinstance(qs_folder_new, Folder):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(qs_folder_new, Folder)")
                return False

            attributes_list = qs_folder_new.get_attribute_numbers_list()

            if not isinstance(attributes_list, list):
                print("catalog_manage -- material_to_new_folder_action -- not isinstance(attributes_list, list)")
                return False

            attributes_count = len(attributes_list)

            # -------------

            parent_child_count = qs_parent.rowCount()

            # -------------
            # Move material to new folder
            # -------------

            qs_first = None
            guid_first = None

            for row_index in reversed(range(parent_child_count)):

                qs_child_current = qs_parent.child(row_index, 0)

                if not isinstance(qs_child_current, Material):
                    continue

                qs_list = qs_parent.takeRow(row_index)

                if len(qs_list) != col_cat_count:
                    print("catalog_manage -- material_to_new_folder_action -- len(qs_list) != col_cat_count")
                    return False

                qs_folder_new.insertRow(attributes_count, qs_list)

                if qs_first is None:

                    qs_first = qs_list[col_cat_value]

                    if not isinstance(qs_first, Material):
                        print("catalog_manage -- material_to_new_folder_action -- not isinstance(qs_first, Material)")
                        return False

                    guid_first = qs_first.data(user_guid)

            if guid_first is None:
                print("catalog_manage -- material_to_new_folder_action -- guid_first is None")
                return False

            # -------------
            # Classic
            # -------------

            if guid_new_folder is None:
                self.history_move_materials(guid_parent=qs_parent.data(user_guid),
                                            guid_material=guid_first,
                                            guid_new_folder=qs_folder_new.data(user_guid),
                                            material_name=qs_first.text())

                continue

            # -------------
            # Redo
            # -------------

            qs_folder_new.setData(guid_new_folder, user_guid)

        # -------------

        self.hierarchy.select_list(selected_list=expanded_list, scrollto=True, expand=True)

        return True

    @staticmethod
    def a___________________link_mange___________________():
        pass

    def link_refresh_code(self, link_name_before: str, link_name_after: str):

        search_start: QModelIndex = self.hierarchy.cat_model.index(0, 0)

        qm_model_list: list = self.hierarchy.cat_model.match(search_start,
                                                             Qt.DisplayRole,
                                                             link_name_before,
                                                             -1,
                                                             Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_model_list) == 0:
            return

        for qm in qm_model_list:

            qs: MyQstandardItem = self.hierarchy.get_qs_by_qm(qm=qm)

            if not isinstance(qs, Link):
                continue

            qs.setText(link_name_after)

    def link_get_structure(self, material_name: str, qs_parent: Material, visited: set) -> bool:

        if material_name in visited:
            print(f"catalog_manage -- link_get_structure -- {material_name} in visited")
            return False

        visited.add(material_name)

        qs_material: MyQstandardItem = self.get_qs_by_material_name(material_name)

        if not isinstance(qs_material, Material):
            return False

        qs_children_list = qs_material.get_children_qs(children=True, attributes=False)

        if len(qs_children_list) == 0:
            return True

        for qs_list in qs_children_list:

            if not isinstance(qs_list, list):
                print("catalog_manage -- link_get_structure -- not isinstance(qs_list, list)")
                continue

            if len(qs_list) < col_cat_count:
                print("catalog_manage -- link_get_structure -- len(qs_list) < col_cat_count")
                continue

            qs_value = qs_list[col_cat_value]
            qs_desc = qs_list[col_cat_desc]

            if not isinstance(qs_desc, Info):
                print("catalog_manage -- link_get_structure -- not isinstance(qs_desc, Info)")
                continue

            if isinstance(qs_value, Component):
                qs_component = QStandardItem(get_icon(component_icon), qs_value.text())
                qs_component.setData(component_code, user_data_type)

                qs_parent.appendRow([qs_component, QStandardItem(qs_desc.text())])
                # print(f"Ajout component : {qs_component.text()} dans : {qs_parent.text()}")
                continue

            if isinstance(qs_value, Link):
                sub_material_name = qs_value.text()

                font = QStandardItem().font()
                font.setBold(True)

                qs_sub_material = QStandardItem(get_icon(material_icon), sub_material_name)
                qs_sub_material.setData(material_code, user_data_type)
                qs_sub_material.setFont(font)

                qs_sub_description = QStandardItem(qs_desc.text())
                qs_sub_description.setFont(font)

                if self.link_get_structure(material_name=sub_material_name, qs_parent=qs_sub_material, visited=visited):
                    qs_parent.appendRow([qs_sub_material, qs_sub_description])

                    # print(f"Ajout Material : {qs_sub_material.text()} dans : {qs_parent.text()}")
                    continue

                qs_sub_material.setIcon(get_icon(error_icon))
                qs_sub_material.setToolTip(self.tr("Liens : Boucle détéctée"))
                qs_sub_material.setForeground(QColor("red"))

                qs_sub_description.setForeground(QColor("red"))

                qs_parent.appendRow([qs_sub_material, qs_sub_description])

                print("catalog_manage -- link_get_structure -- loop detected")

        visited.remove(material_name)
        return True

    def link_get_forbidden_list(self, material_name: str, forbidden_list: set,
                                ignore_qm_link=None, ignore_parent_name="") -> bool:

        if material_name in forbidden_list:
            return True

        forbidden_list.add(material_name)

        search_start = self.hierarchy.cat_model.index(0, col_cat_value)

        search = self.hierarchy.cat_model.match(search_start, Qt.DisplayRole, material_name, -1,
                                                Qt.MatchExactly | Qt.MatchRecursive)

        if len(search) == 0:
            print("catalog_manage -- link_get_forbidden_list -- len(search) == 0 -> Error")
            return False

        for qm in search:

            if not qm_check(qm):
                print("catalog_manage -- link_get_forbidden_list -- not qm_check(qm):")
                continue

            if qm == ignore_qm_link and material_name == ignore_parent_name:
                continue

            if qm.data(user_data_type) != link_code:
                continue

            qm_parent = qm.parent()

            if not qm_check(qm_parent):
                print("catalog_manage -- link_get_forbidden_list -- not qm_check(qm_parent):")
                continue

            parent_name = qm_parent.data()

            if not isinstance(parent_name, str):
                print("catalog_manage -- link_get_forbidden_list -- not isinstance(parent_name, str)")
                continue

            if not self.link_get_forbidden_list(material_name=parent_name,
                                                forbidden_list=forbidden_list,
                                                ignore_qm_link=ignore_qm_link,
                                                ignore_parent_name=ignore_parent_name):
                continue

        return True

    @staticmethod
    def a___________________catalog_delete___________________():
        pass

    def catalog_delete(self):

        qs_selecion_list = self.hierarchy.get_qs_selection_list()
        selection_index = 0
        parent_selection = None

        for qs_current in reversed(qs_selecion_list):

            if not isinstance(qs_current, MyQstandardItem):
                print("catalog_manage -- catalog_delete --> not isinstance(qs_current, MyQstandardItem)")
                return None

            children_list = qs_current.get_children_name(upper=False)
            children_count = len(children_list)

            if children_count == 1:

                question = msg(titre=application_title,
                               message=self.tr("Voulez-vous vraiment supprimer cet élément?"),
                               infos="hierarchy_delete_item",
                               type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                               defaut_bouton=QMessageBox.Ok,
                               icone_avertissement=True,
                               infos_defaut=QMessageBox.Ok,
                               details=children_list)

            elif children_count > 1:

                question = msg(titre=application_title,
                               message=self.tr("Voulez-vous vraiment supprimer ces éléments?"),
                               infos="hierarchy_delete_item",
                               type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                               defaut_bouton=QMessageBox.Ok,
                               icone_avertissement=True,
                               infos_defaut=QMessageBox.Ok,
                               details=children_list)

            else:
                question = QMessageBox.Ok

            if question == QMessageBox.Cancel:
                return

            if question == QMessageBox.No:
                continue

            qs_parent = self.hierarchy.get_parent(qs=qs_current)

            if qs_parent is None:
                continue

            row_current = qs_current.row()

            if not self.material_delete(qs=qs_current):

                if isinstance(qs_current, Material):

                    msg(titre=application_title,
                        message=self.tr("Vous ne pouvez supprimer cet ouvrage, "
                                        "il est encore utilisé en tant que lien."),
                        icone_critique=True)

                else:

                    msg(titre=application_title,
                        message=self.tr("Vous ne pouvez supprimer ce dossier, "
                                        "des ouvrages sont utilisés en tant que lien."),
                        icone_critique=True)

                continue

            qs_list = qs_parent.takeRow(row_current)

            self.history_del_ele(qs_parent=qs_parent, qs_current=qs_current, row_current=row_current, qs_list=qs_list)

            selection_index = row_current
            parent_selection = qs_parent

        if isinstance(parent_selection, MyQstandardItem):

            children_list = parent_selection.get_children_type_list()
            children_count = len(children_list)

            if children_count == 0:
                selection_item = parent_selection

            elif selection_index > children_count:
                selection_item = parent_selection.child(selection_index - 1, col_cat_value)

            else:
                selection_item = parent_selection.child(selection_index, col_cat_value)

            self.hierarchy.select_list(selected_list=[selection_item])

        self.change_made = True

        return

    @staticmethod
    def a___________________catalog_copy___________________():
        pass

    def catalog_copy_action(self, cut=False):

        qs_selected_list = self.hierarchy.get_qs_selection_list()

        ele_list = list()

        for qs in qs_selected_list:

            qs: MyQstandardItem

            if not isinstance(qs, MyQstandardItem):
                print("catalog_manage -- catalog_copy_action -- not isinstance(qs, MyQstandardItem)")
                self.asc.boutons_hierarchie_coller(attribute_code)
                return

            ele_type = qs.data(user_data_type)

            self.clipboard_current = ele_type

            if ele_type not in ele_list:
                ele_list.append(ele_type)
                zero = True
            else:
                zero = False

            clipboard, clipboard_cut = self.get_clipboard(ele_type=ele_type, reset_clipboard=zero)

            if not isinstance(clipboard, ClipboardDatas):
                print("catalog_manage -- catalog_copy_action -- not isinstance(clipboard, ClipboardDatas)")
                continue

            title = qs.text()

            if not isinstance(title, str):
                print("catalog_manage -- catalog_copy_action -- not isinstance(title, str)")
                continue

            description = qs.get_attribute_value_by_number(number="207")

            if not isinstance(description, str) or description == "":
                text = title
            else:
                text = f"{title} - {description}"

            current_row = qs.row()

            if current_row == -1:
                print("catalog_manage -- catalog_copy_action -- current_row == -1")
                continue

            qs_parent = self.hierarchy.get_parent(qs=qs)

            if not isinstance(qs_parent, QStandardItem):
                print("catalog_manage -- catalog_copy_action -- not isinstance(qs_parent, QStandardItem)")
                continue

            qs_list = self.catalog_copy_search_column(qs_parent, current_row)

            if not isinstance(qs_list, list):
                print("catalog_manage -- catalog_copy_action -- not isinstance(qs_list, list)")
                self.asc.boutons_hierarchie_coller(None)
                return

            clipboard.append(text, qs_list)

            if cut:
                clipboard_cut.append(text, [qs_parent, qs])

            self.asc.boutons_hierarchie_coller(ele_type)

    @staticmethod
    def catalog_copy_search_column(qs_parent: MyQstandardItem, child_index: int):

        qs_list = list()

        for column_index in range(col_cat_count):

            qs = qs_parent.child(child_index, column_index)

            if not isinstance(qs, MyQstandardItem):
                print("catalog_manage -- catalog_copy_search_column -- not isinstance(qs, MyQstandardItem)")
                return None

            qs_clone = qs.clone_creation(new=False)

            if column_index == col_cat_value and qs.hasChildren():
                qs.clone_children(qs_original=qs, qs_destination=qs_clone, new=False)

            qs_list.append(qs_clone)

        if len(qs_list) != col_cat_count:
            print("catalog_manage -- catalog_copy_search_column -- len(liste_qstandarditem) != col_cat_count")
            return None

        return qs_list

    @staticmethod
    def a___________________catalog_paste___________________():
        pass

    def catalog_paste(self, ele_type):
        clipboard, clipboard_cut = self.get_clipboard(ele_type=ele_type, reset_clipboard=False)

        clipboard: ClipboardDatas
        clipboard_cut: ClipboardDatas

        result = self.hierarchie_coller_datas(pressepapier=clipboard, presse_papier_couper=clipboard_cut)

        if not result:
            return

        if clipboard_cut.len_datas() == 0:
            return

        self.hierarchie_couper_coller_action(clipboard_cut=clipboard_cut)

    def hierarchie_couper_coller_action(self, clipboard_cut: ClipboardDatas):

        liste_elements = clipboard_cut.get_values_list()

        for liste_datas in liste_elements:
            liste_datas: list

            # liste_datas = [qstandarditem_parent, qstandarditem]

            qs_parent: MyQstandardItem = liste_datas[0]
            datas: MyQstandardItem = liste_datas[1]

            if not isinstance(qs_parent, QStandardItem):
                continue

            if isinstance(datas, MyQstandardItem):

                index_row: int = datas.row()

                qstandarditem_sup = qs_parent.child(index_row, col_cat_value)

                if qstandarditem_sup != datas:
                    continue

                qs_parent.takeRow(index_row)

            elif isinstance(datas, list):

                for qs in datas:

                    index_row: int = qs.row()

                    qstandarditem_sup = qs_parent.child(index_row, col_cat_value)

                    if qstandarditem_sup != qs:
                        continue

                    qs_parent.takeRow(index_row)

        # reset cut clipboard !

        clipboard_cut.clear()
        self.change_made = True

    def hierarchy_paste_datas(self, clipboard: ClipboardDatas):
        pass

    def hierarchie_coller_datas(self, pressepapier: ClipboardDatas, presse_papier_couper: ClipboardDatas,
                                titre_spe="", id_ele="0") -> bool:

        # ---- library ----

        bible_externe_open = self.asc.library_widget.isVisible()

        if not isinstance(presse_papier_couper, ClipboardDatas):
            print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(presse_papier_couper, ClipboardDatas)")
            return

        # ---- cut ----

        couper = presse_papier_couper.len_datas() != 0

        type_element_futur = pressepapier.type_element
        liste_titres_futur = pressepapier.get_titles_list(upper=True)

        if titre_spe == "":
            liste_qs_futur_tous: list = pressepapier.get_values_list()

        else:

            liste_qs_futur_tous: list = pressepapier.get_datas_title(titre_spe, id_ele)

            titre_spe = pressepapier.get_real_title(titre_spe, id_ele)

        if couper:
            liste_copier_enfants = [liste_qstandarditem_pp_row[col_cat_value]
                                    for liste_qstandarditem_pp_row in liste_qs_futur_tous]

        else:
            liste_copier_enfants: list = self.recherche_enfants(liste_qs_futur_tous=liste_qs_futur_tous)

            if liste_copier_enfants is None:

                if bible_externe_open:
                    self.asc.library_widget.ne_pas_fermer_ui()
                return False

        datas: list = self.recherche_localisation(type_element_futur=type_element_futur,
                                                  liste_titre_futur=liste_titres_futur)

        if len(datas) == 0:

            if bible_externe_open:
                self.asc.library_widget.ne_pas_fermer_ui()
            return False

        for dict_datas in datas:
            for index_liste, liste_qs_futur in enumerate(liste_qs_futur_tous):

                if not isinstance(liste_qs_futur, list):
                    print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(liste_qs_futur, list)")
                    continue

                if len(liste_qs_futur) != col_cat_count:
                    if not isinstance(liste_qs_futur, list):
                        print(f"catalog_manage -- hierarchie_coller_datas -- len(liste_qs_futur) != column_count")
                        continue

                qs_futur: MyQstandardItem = liste_qs_futur[col_cat_value]

                if not isinstance(qs_futur, MyQstandardItem):
                    print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(qs_futur, MyQstandardItem)")
                    continue

                dict_datas["ajouter_enfants"] = qs_futur in liste_copier_enfants

        if not couper:
            self.recherche_existant(datas=datas,
                                    titre_spe=titre_spe,
                                    liste_titre_futur=liste_titres_futur)

        if len(datas) == 0:
            if bible_externe_open:
                self.asc.library_widget.ne_pas_fermer_ui()
            return False

        liste_selection_futur = list()

        for dict_datas in datas:

            qs_parent = dict_datas.get("qstandarditem_destination")

            if not isinstance(qs_parent, QStandardItem):
                print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(qs_parent, QStandardItem)")
                continue

            nom = dict_datas.get("nom_parent")

            if not isinstance(nom, str):
                print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(nom, str)")
                continue

            index_insertion = dict_datas.get("index_insertion")

            if not isinstance(index_insertion, int):
                print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(index_insertion, int)")
                continue

            update: bool = dict_datas.get("update")
            remplacer: bool = dict_datas.get("remplacer")
            ignorer: bool = dict_datas.get("ignorer")

            if not isinstance(update, bool) or not isinstance(remplacer, bool) or not isinstance(ignorer, bool):
                print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(update, bool)")
                continue

            qs_actuel = dict_datas.get("qs_actuel")

            if not isinstance(qs_actuel, QStandardItem):
                print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(qs_actuel, MyQstandardItem)")
                continue

            index_actuel = qs_actuel.row()

            if index_actuel == -1 and nom == self.tr("Racine de la hiérarchie"):
                index_actuel = self.hierarchy.cat_model.invisibleRootItem().rowCount()
            elif index_actuel == -1:
                continue

            if remplacer:
                self.material_delete(qs=qs_actuel)
                qs_parent.takeRow(qs_actuel.row())

            if ignorer:
                continue

            for index_liste, liste_qs_futur in enumerate(liste_qs_futur_tous):

                if not isinstance(liste_qs_futur, list):
                    print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(liste_qs_futur, list)")
                    continue

                if len(liste_qs_futur) != col_cat_count:
                    print(f"catalog_manage -- hierarchie_coller_datas -- len(liste_qs_futur) != column_count")
                    continue

                index_final = index_insertion + index_liste

                qs_futur = liste_qs_futur[0]

                if not isinstance(qs_futur, MyQstandardItem):
                    print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(qs_futur, MyQstandardItem)")
                    continue

                texte_futur = qs_futur.text()

                if not isinstance(texte_futur, str):
                    print(f"catalog_manage -- hierarchie_coller_datas -- not isinstance(texte_futur, str)")
                    continue

                ajouter_enfants = qs_futur in liste_copier_enfants

                # if update:
                #     txt = "Update"
                # elif remplacer:
                #     txt = "Remplacer"
                # else:
                #     txt = "Copie"

                # print(f"catalog_manage -- hierarchie_coller_datas -- {txt} de : '{texte_futur}' dans '{nom}' "
                #       f"à l'index : {index_final} -- avec enfants : {ajouter_enfants}")

                # if remplacer:
                #     index_final = index_actuel
                #     self.supprimer_ouvrage_bdd(qs_actuel)
                #     qs_parent.takeRow(qs_actuel.row())
                #
                # if ignorer:
                #     continue

                if self.coller_update(qs_parent=qs_parent,
                                      liste_qs_futur=liste_qs_futur,
                                      index_insertion=index_final,
                                      index_actuel=index_actuel,
                                      ajouter_enfant=ajouter_enfants,
                                      couper=couper,
                                      update=update,
                                      start=True) == -1:
                    presse_papier_couper.clear()
                    return

                qm = qs_parent.child(index_final, col_cat_value)

                if not isinstance(qs_futur, Attribute):
                    if qm not in liste_selection_futur:
                        liste_selection_futur.append(qm)

                    continue

                qm = qs_parent.index()

                if qm not in liste_selection_futur:
                    liste_selection_futur.append(qm)

        self.hierarchy.select_list(selected_list=liste_selection_futur,
                                   scrollto=len(liste_selection_futur) != 1,
                                   expand=True)
        return True

    def recherche_enfants(self, liste_qs_futur_tous: list):

        dict_futur = dict()

        for index_item, liste_qs_futur_row in enumerate(liste_qs_futur_tous):

            qs_futur: MyQstandardItem = liste_qs_futur_row[0]
            texte_futur = qs_futur.text()

            liste_enfants_futur = qs_futur.get_children_name(upper=False)
            nb_enfants_futur = len(liste_enfants_futur)

            if nb_enfants_futur == 0:
                continue

            dict_futur[texte_futur] = [qs_futur, liste_enfants_futur]

        nb_items_futur = len(dict_futur)

        if nb_items_futur == 0:
            return list()

        msgbox = MessageChildren()

        liste_copie_enfants = list()
        defaut_bouton = "ok"
        reponse_enfants = None

        index_actuel = 0

        checkbox = True

        for texte_futur, donnees in dict_futur.items():

            qs_futur = donnees[0]
            liste_enfants_futur: list = donnees[1]
            nb_enfants_futur = len(liste_enfants_futur)
            index_actuel += 1

            if reponse_enfants is None:

                if nb_enfants_futur == 1:

                    a = self.tr("contient 1 enfant")
                    b = self.tr("Voulez-vous l'ajouter également")

                    msgbox.show_message_children(message=f"<b>'{texte_futur}'</b> {a}. {b} ?",
                                                 bt_ok=self.tr("Avec l'enfant"),
                                                 bt_no=self.tr("Sans l'enfant"),
                                                 chk_all=checkbox,
                                                 checkbox_index=index_actuel,
                                                 checkbox_total=nb_items_futur,
                                                 checkbox_tooltips="\n".join(dict_futur),
                                                 details=liste_enfants_futur,
                                                 default_bouton=defaut_bouton)

                else:

                    a = self.tr("contient des enfants")
                    c = self.tr("Voulez-vous les ajouter également")

                    msgbox.show_message_children(message=f"<b>'{texte_futur}'</b> {a}. {c}?",
                                                 bt_ok=self.tr("Avec les enfants"),
                                                 bt_no=self.tr("Sans les enfants"),
                                                 chk_all=checkbox,
                                                 checkbox_index=index_actuel,
                                                 checkbox_total=nb_items_futur,
                                                 checkbox_tooltips="\n".join(dict_futur),
                                                 details=liste_enfants_futur,
                                                 default_bouton=defaut_bouton)

                reponse_enfants = msgbox.reponse

            if reponse_enfants == QMessageBox.Cancel:
                return None

            if reponse_enfants == QMessageBox.NoAll:
                return list()

            if reponse_enfants == QMessageBox.YesAll:
                liste_copie_enfants.append(qs_futur)
                continue

            if reponse_enfants == QMessageBox.No:
                checkbox = False
                defaut_bouton = "no"
                reponse_enfants = None
                continue

            if reponse_enfants == QMessageBox.Yes:
                liste_copie_enfants.append(qs_futur)
                checkbox = False
                reponse_enfants = None
                defaut_bouton = "ok"
                continue

        return liste_copie_enfants

    def recherche_localisation(self, type_element_futur: str, liste_titre_futur: list) -> list:

        nb_titre_futur = len(liste_titre_futur)

        liste_selection_actuel = self.hierarchy.get_qs_selection_list()
        liste_selection_actuel.sort()
        # liste_parent_actuel = list()

        datas = list()

        if len(liste_selection_actuel) == 0:
            liste_selection_actuel.append(self.hierarchy.cat_model.invisibleRootItem())

        for qs_selection in liste_selection_actuel:

            if not isinstance(qs_selection, QStandardItem):
                print("catalog_manage -- recherche_localisation -- not isinstance(qs_selection, QStandardItem)")
                continue

            index_selection = qs_selection.row()

            if qs_selection == self.hierarchy.cat_model.invisibleRootItem():

                elements_compatibles = {self.tr("Frère"): [qs_selection, self.hierarchy.cat_model.rowCount()]}

            else:

                elements_compatibles = qs_selection.get_add_possibilities(ele_type=type_element_futur)

            nb_elements_compatibles = len(elements_compatibles)

            if nb_elements_compatibles == 0:
                continue

            if nb_elements_compatibles != 1:

                liste_enfant: list = elements_compatibles[self.tr("Enfant")]
                liste_frere: list = elements_compatibles[self.tr("Frère")]

                qs_enfant_actuel: MyQstandardItem = liste_enfant[0]
                enfant_actuel_index = liste_enfant[1]
                enfant_actuel_texte = qs_enfant_actuel.text()
                enfant_actuel_type = qs_enfant_actuel.data(user_data_type)

                qs_parent_actuel: MyQstandardItem = liste_frere[0]
                parent_type_actuel = qs_parent_actuel.data(user_data_type)

                if qs_parent_actuel == self.hierarchy.cat_model.invisibleRootItem():
                    parent_texte_actuel = self.tr("Racine de la hiérarchie")
                else:
                    parent_texte_actuel = qs_parent_actuel.text()

                parent_index_actuel = liste_frere[1]

                msgbox = MessageLocation()

                if nb_titre_futur == 1:

                    msgbox.show_message_location(message=self.tr("Où voulez-vous ajouter cet élément?"),
                                                 parent_txt=parent_texte_actuel,
                                                 parent_type=parent_type_actuel,
                                                 child_txt=enfant_actuel_texte,
                                                 child_type=enfant_actuel_type)

                else:
                    msgbox.show_message_location(message=self.tr("Où voulez-vous ajouter ces éléments?"),
                                                 parent_txt=parent_texte_actuel,
                                                 parent_type=parent_type_actuel,
                                                 child_txt=enfant_actuel_texte,
                                                 child_type=enfant_actuel_type)

                reponse_loc = msgbox.reponse

                if reponse_loc == QMessageBox.Yes:
                    qstandarditem_destination: MyQstandardItem = qs_enfant_actuel
                    index_insertion: int = enfant_actuel_index

                elif reponse_loc == QMessageBox.No:
                    qstandarditem_destination: MyQstandardItem = qs_parent_actuel
                    index_insertion: int = parent_index_actuel

                else:
                    return list()

            else:

                resultat: list = list(elements_compatibles.values())[0]

                qstandarditem_destination: MyQstandardItem = resultat[0]
                index_insertion: int = resultat[1]

            if qstandarditem_destination is None:
                continue

            if qstandarditem_destination == self.hierarchy.cat_model.invisibleRootItem():

                ses_enfants = self.hierarchy.get_root_children_name()

            else:

                ses_enfants = qstandarditem_destination.get_children_name(upper=True)
            #
            # if qstandarditem_destination in liste_parent_actuel:
            #     if type_element_futur == type_element_actuel:
            #         continue
            #
            # liste_parent_actuel.append(qstandarditem_destination)

            if qstandarditem_destination == self.hierarchy.cat_model.invisibleRootItem():
                nom_parent = self.tr("Racine de la hiérarchie")
            else:
                nom_parent = qstandarditem_destination.text()

            datas.append({"qstandarditem_destination": qstandarditem_destination,
                          "nom_parent": nom_parent,
                          "parent_ses_enfants": ses_enfants,
                          "qs_actuel": qs_selection,
                          "nom_actuel": qs_selection.text(),
                          "index_insertion": index_insertion,
                          "index_actuel": index_selection,
                          "update": False,
                          "remplacer": False,
                          "ajouter_enfants": False,
                          "ignorer": False})

        return datas

    def recherche_existant(self, datas: list, titre_spe: str, liste_titre_futur: list) -> list:

        dict_doublons = dict()
        liste_suivants = list()
        liste_parents = list()

        for index_item, datas_dict in enumerate(datas):
            qs_destination: str = datas_dict["qstandarditem_destination"]
            texte_actuel: str = datas_dict["nom_parent"]
            ses_enfants_actuel: list = datas_dict["parent_ses_enfants"]
            ajouter_enfants = datas_dict["ajouter_enfants"]

            if titre_spe == "":

                liste_similaire = [titre for titre in ses_enfants_actuel if titre in liste_titre_futur]

            else:

                if titre_spe.upper() in ses_enfants_actuel:

                    liste_similaire = [titre_spe]
                else:

                    liste_similaire = list()

            if len(liste_similaire) == 0:
                continue

            if qs_destination in liste_parents:
                index_doublons = liste_parents.index(qs_destination)

                liste_doublons_precedent = dict_doublons[index_doublons][1]

                if liste_doublons_precedent == liste_similaire:
                    datas_dict["ignorer"] = True

            else:
                liste_parents.append(qs_destination)

            dict_doublons[index_item] = [texte_actuel, liste_similaire, ajouter_enfants]
            liste_suivants.append(texte_actuel)

        nb_items = len(dict_doublons)

        if nb_items == 0:
            return datas

        msgbox = MessageExisting()

        reponse_exist = None

        checkbox = True
        defaut_bouton = "bt_maj"

        index_actuel = 0

        for index_item, donnees in dict_doublons.items():

            texte_actuel: str = donnees[0]
            liste_similaire: list = donnees[1]
            ajouter_enfants = donnees[2]

            if ajouter_enfants:

                update_txt = self.tr("Mettre à jour et ses enfants")
                replace_txt = self.tr("Remplacer et ses enfants")
                duplicate_txt = self.tr("Dupliquer et ses enfants")

            else:

                update_txt = self.tr("Mettre à jour et ses enfants")
                replace_txt = self.tr("Remplacer et ses enfants")
                duplicate_txt = self.tr("Dupliquer et ses enfants")

            nb_elements_existants = len(liste_similaire)
            index_actuel += 1

            datas_dict: dict = datas[index_item]

            liste_similaire.insert(0, f" --- {texte_actuel} ---\n")

            if reponse_exist is None:

                todo = self.tr("Que souhaitez-vous faire")

                if nb_elements_existants == 1:

                    all_ready_exist = self.tr("existe déjà")

                    msgbox.show_message_existing(message=f"<b>'{liste_similaire[1]}' {all_ready_exist} !</b><br>"
                                                         f'{todo} ? ',
                                                 bt_update=update_txt,
                                                 bt_replace=replace_txt,
                                                 bt_duplicate=duplicate_txt,
                                                 chk_all=checkbox,
                                                 checkbox_index=index_actuel,
                                                 checkbox_total=nb_items,
                                                 checkbox_tooltips="\n".join(liste_suivants),
                                                 details=liste_similaire,
                                                 default_bouton=defaut_bouton)
                else:

                    all_ready_exist = self.tr("éléments existent déjà")

                    msgbox.show_message_existing(message=f"<b>{nb_elements_existants}</b> {all_ready_exist} !\n"
                                                         f'{todo} ? ',
                                                 bt_update=update_txt,
                                                 bt_replace=replace_txt,
                                                 bt_duplicate=duplicate_txt,
                                                 chk_all=checkbox,
                                                 checkbox_index=index_actuel,
                                                 checkbox_total=nb_items,
                                                 checkbox_tooltips="\n".join(liste_suivants),
                                                 details=liste_similaire,
                                                 default_bouton=defaut_bouton)

                reponse_exist = msgbox.reponse

            if reponse_exist == QMessageBox.Cancel:
                datas.clear()
                return list()

            if reponse_exist == QMessageBox.YesAll:
                datas_dict["update"] = True
                datas_dict["remplacer"] = False
                continue

            if reponse_exist == QMessageBox.SaveAll:
                datas_dict["update"] = False
                datas_dict["remplacer"] = True
                continue

            if reponse_exist == QMessageBox.NoAll:
                return datas

            if reponse_exist == QMessageBox.Yes:
                datas_dict["update"] = True
                datas_dict["remplacer"] = False
                checkbox = False
                reponse_exist = None
                defaut_bouton = "bt_maj"
                continue

            if reponse_exist == QMessageBox.Save:
                datas_dict["update"] = False
                datas_dict["remplacer"] = True
                checkbox = False
                reponse_exist = None
                defaut_bouton = "bt_dupliquer"
                continue

            if reponse_exist == QMessageBox.No:
                checkbox = False
                reponse_exist = None
                defaut_bouton = "bt_remplacer"
                continue

        return datas

    def coller_update(self, qs_parent: MyQstandardItem, liste_qs_futur: list, index_insertion: int, index_actuel: int,
                      ajouter_enfant: bool, couper=False, update=False, start=False) -> int:

        qs_futur = liste_qs_futur[col_cat_value]

        if not isinstance(qs_futur, MyQstandardItem):
            print(f"catalog_manage -- coller_update -- not isinstance(qs_futur, MyQstandardItem)")
            return -1

        texte_futur = qs_futur.text()

        if not isinstance(texte_futur, str):
            print(f"catalog_manage -- coller_update -- not isinstance(texte_futur, str)")
            return -1

        index_recherche = self.recherche_index_valeur(qs_parent=qs_parent,
                                                      valeur=texte_futur, index_initial=index_actuel)

        attributes_count = 0

        if not update:
            nouveau_qs_parent = self.coller_creation(qs_parent=qs_parent,
                                                     index_insertion=index_insertion,
                                                     liste_qs_futur=liste_qs_futur,
                                                     couper=couper,
                                                     start=start)

            if not isinstance(nouveau_qs_parent, QStandardItem):
                return -1

            attributes_count = nouveau_qs_parent.rowCount()
            index_tps = index_insertion + attributes_count

        else:

            if not self.update_with(qs_parent=qs_parent,
                                    index_actuel=index_recherche,
                                    liste_qs_futur=liste_qs_futur):
                return -1

            nouveau_qs_parent = qs_parent.child(index_recherche, col_cat_value)

            if nouveau_qs_parent is None:
                print(f"{qs_parent.text(), qs_parent.data(user_data_type)}")

            index_tps = index_recherche

        if not ajouter_enfant:
            return index_tps

        liste_enfants = qs_futur.get_children_qs(children=True, attributes=False)

        for index_insertion, liste_qs_futur in enumerate(liste_enfants):

            if not isinstance(liste_qs_futur, list):
                print(f"catalog_manage -- coller_update -- not isinstance(liste_qs_futur, list)")
                return -1

            if len(liste_qs_futur) != col_cat_count:
                if not isinstance(liste_qs_futur, list):
                    print(f"catalog_manage -- coller_update -- len(liste_qs_futur) != column_count")
                    return -1

            if self.coller_update(qs_parent=nouveau_qs_parent,
                                  liste_qs_futur=liste_qs_futur,
                                  index_insertion=index_insertion + attributes_count,
                                  index_actuel=index_insertion,
                                  ajouter_enfant=ajouter_enfant,
                                  couper=couper,
                                  update=update,
                                  start=False) == -1:
                return -1

        return index_tps

    def coller_creation(self, qs_parent: QStandardItem, index_insertion: int, liste_qs_futur: list,
                        couper: bool, start=False) -> QStandardItem:

        # print("catalog_manage -- coller_creation -- start")

        # -------------------
        # Verification
        # -------------------

        if len(liste_qs_futur) != col_cat_count:
            print("catalog_manage -- coller_creation -- len(liste_qs_futur) != col_cat_count")
            return None

        qs_value = liste_qs_futur[col_cat_value]
        qs_desc = liste_qs_futur[col_cat_desc]
        qs_number = liste_qs_futur[col_cat_number]

        if (not isinstance(qs_value, MyQstandardItem) or not isinstance(qs_desc, Info) or
                not isinstance(qs_number, Info) or not isinstance(qs_parent, QStandardItem)):
            print("catalog_manage -- coller_creation -- not isinstance(qs_value, MyQstandardItem)")
            return None

        # -------------------
        # Datas
        # -------------------

        ele_type = qs_value.data(user_data_type)

        value = qs_value.text()
        desc = qs_desc.text()

        parent_name = qs_parent.text()

        if not isinstance(value, str) or not isinstance(desc, str) or not isinstance(parent_name, str):
            print("catalog_manage -- coller_creation -- not isinstance(value, str)")
            return None

        # -------------------
        # Clone
        # -------------------

        qs_value_cloned = qs_value.clone_creation(new=not couper)
        qs_desc_cloned = qs_desc.clone_creation(new=not couper)
        qs_number_cloned = qs_number.clone_creation(new=not couper)

        # -------------------
        # Chacking Material Name
        # -------------------

        if not couper:

            self.coller_gestion_nom_ouvrage(qs_value_cloned)

            if isinstance(qs_value_cloned, Folder):

                if qs_parent == self.hierarchy.cat_model.invisibleRootItem():
                    liste_dossiers = self.hierarchy.get_root_children_name()
                else:
                    if isinstance(qs_parent, MyQstandardItem):
                        liste_dossiers = qs_parent.get_children_name(upper=True)
                    else:
                        liste_dossiers = list()

                value = find_new_title(qs_value_cloned.text(), liste_dossiers)

                qs_value_cloned.setText(value)

        if ele_type == link_code:

            if value.upper() not in material_upper_list:
                impossible_message = self.tr("Impossible de coller ce lien")
                inexist_message = self.tr("L'ouvrage correspondant n'existe pas")

                msg(titre=application_title,
                    message=f"{impossible_message} : {value}.<br><b>{inexist_message}!</b>",
                    icone_critique=True)
                return QStandardItem()

            forbidden_list = set()
            copy_valid = self.link_get_forbidden_list(material_name=parent_name, forbidden_list=forbidden_list)

            if value in forbidden_list:
                copy_valid = False

            if not copy_valid:
                print("catalog_manage -- coller_creation -- loop error")

                impossible_message = self.tr("Impossible de coller ce lien")
                loop_message = self.tr("Liens : Boucle détéctée")

                msg(titre=application_title,
                    message=f"{impossible_message} : {qs_value_cloned.text()}.<br><b>{loop_message}!</b>",
                    icone_critique=True)
                return QStandardItem()

            if not couper:
                link_list.append(value)

            parent_name = parent_name.upper()

            if parent_name not in material_with_link_list:
                material_with_link_list.append(parent_name)

            self.material_update_link_number(material_name=value)

        liste_cloner = [qs_value_cloned, qs_desc_cloned, qs_number_cloned]

        if qs_value.hasChildren():
            qs_value.clone_attributes(qs_original=qs_value, qs_destination=qs_value_cloned, new=not couper)

        # ----------

        child_count = qs_parent.rowCount()

        if index_insertion > child_count:
            index_insertion = child_count - 1

        # ----------

        qs_parent.insertRow(index_insertion, liste_cloner)

        if couper:

            full_title = f"{value} - {desc}"

            clipboard, clipboard_cut = self.get_clipboard(ele_type=ele_type, reset_clipboard=False)

            if not isinstance(clipboard, ClipboardDatas) or not isinstance(clipboard_cut, ClipboardDatas):
                return qs_value_cloned

            qs_parent_actuel, row_current = clipboard_cut.get_cut_datas(full_title)

            if not isinstance(qs_parent_actuel, QStandardItem) or not isinstance(row_current, int):
                return qs_value_cloned

            if qs_parent == qs_parent_actuel and row_current > index_insertion:
                row_current -= 1

            self.history_cut_ele(guid_parent_new=qs_parent_actuel.data(user_guid),
                                 qs_current=qs_value_cloned,
                                 row_new=row_current)
        elif start:

            self.history_add_ele(qs_current=qs_value_cloned, paste=True)

        # print(f"catalog_manage -- creation -- Fin")
        return qs_value_cloned

    def update_with(self, qs_parent: QStandardItem, index_actuel, liste_qs_futur: list) -> bool:

        # print("catalog_manage -- update_with")

        # --------------------------------------------------------------------------------------
        # Mise à jour de l'élément actuel : colonnes  = valeur, description, index, numero, nom
        # --------------------------------------------------------------------------------------

        if len(liste_qs_futur) != col_cat_count:
            return False

        qs_actuel = qs_parent.child(index_actuel, col_cat_value)

        if not isinstance(qs_actuel, MyQstandardItem):
            return False

        texte_actuel = qs_actuel.text()
        type_actuel = qs_actuel.data(user_data_type)

        qs_futur = liste_qs_futur[0]

        if not isinstance(qs_futur, MyQstandardItem):
            return False

        texte_futur = qs_futur.text()

        if texte_actuel != texte_futur:
            return False

        print(f"catalog_manage -- update_with -- {qs_futur.text()} ({qs_futur.data(user_data_type)})")

        for numero_col in [col_cat_value, col_cat_desc]:
            qs_tps_actuel = qs_parent.child(index_actuel, numero_col)

            if qs_tps_actuel is None:
                return False

            texte_actuel = qs_parent.text()

            qs_tps_futur: QStandardItem = liste_qs_futur[numero_col]

            if qs_tps_futur is None:
                return False

            if type_actuel == material_code:
                continue

            texte_futur = qs_tps_futur.text()

            if texte_actuel == texte_futur:
                continue

            qs_tps_actuel.setText(texte_futur)

        # --------------------------------------------------------------------------------------
        # Analyse des numéros d'attributs présent dans l'élément actuel
        # --------------------------------------------------------------------------------------

        datas_actuel = dict()
        liste_numeros_actuels = list()

        for index_child_actuel in range(qs_actuel.rowCount()):

            qs_val_actuel: MyQstandardItem = qs_actuel.child(index_child_actuel, col_cat_value)

            if qs_val_actuel is None:
                return False

            if not isinstance(qs_val_actuel, Attribute):
                continue

            liste = list()
            numero_actuel = ""

            for index_colonne in range(col_cat_count):
                qs_tps = qs_actuel.child(index_child_actuel, index_colonne)

                if qs_tps is None:
                    return False

                if index_colonne == col_cat_number:
                    numero_actuel = qs_tps.text()

                liste.append(qs_tps)

            datas_actuel[numero_actuel] = liste
            liste_numeros_actuels.append(numero_actuel)

        # --------------------------------------------------------------------------------------
        # Copie / Mise à jour des attributs
        # --------------------------------------------------------------------------------------

        for index_child_futur in range(qs_futur.rowCount()):

            qs_val_futur: MyQstandardItem = qs_futur.child(index_child_futur, col_cat_value)

            if qs_val_futur is None:
                return False

            if not isinstance(qs_val_futur, Attribute):
                continue

            qs_number_futur = qs_futur.child(index_child_futur, col_cat_number)

            if not isinstance(qs_number_futur, Info):
                return False

            numero_futur = qs_number_futur.text()

            # --------------------------------------------------------------------------------------
            # Mise à jour attribut
            # --------------------------------------------------------------------------------------

            if numero_futur in liste_numeros_actuels:

                print(f"catalog_manage -- update_with -- {qs_futur.text()} : MAJ attribut {numero_futur} = "
                      f"{qs_futur.child(index_child_futur, col_cat_value).text()}")

                liste_colonnes_actuelle: list = datas_actuel[numero_futur]

                for index_colonne in [col_cat_value, col_cat_index]:
                    qs_tps_actuel: QStandardItem = liste_colonnes_actuelle[index_colonne]
                    valeur_actuelle = qs_tps_actuel.text()
                    valeur_future = qs_futur.child(index_child_futur, index_colonne).text()

                    if valeur_actuelle == valeur_future:
                        continue

                    qs_tps_actuel.setText(valeur_future)

                continue

            # --------------------------------------------------------------------------------------
            # Copie attribut
            # --------------------------------------------------------------------------------------

            print(f"catalog_manage -- update_with -- {qs_futur.text()} : Création attribut {numero_futur} = "
                  f"{qs_futur.child(index_child_futur, col_cat_value).text()}")

            index_insertion = qs_actuel.get_attribute_insertion_index(number=numero_futur)

            liste_qs_creation = list()

            for index_colonne in range(col_cat_count):
                new_qs = qs_futur.child(index_child_futur, index_colonne).clone_creation(new=True)

                liste_qs_creation.append(new_qs)

            qs_actuel.insertRow(index_insertion, liste_qs_creation)

        if qs_parent == self.hierarchy.cat_model.invisibleRootItem():
            return True

        if not isinstance(qs_parent, Component) and not isinstance(qs_parent, Link):

            qmodelindex_filtre: QModelIndex = self.hierarchy.map_to_filter(qm=qs_parent.index())

            if qmodelindex_filtre is not None:
                self.hierarchy.expand(qmodelindex_filtre)

        # print("catalog_manage -- update_with -- Fin")
        return True

    def coller_gestion_nom_ouvrage(self, qs_clone: MyQstandardItem):

        if isinstance(qs_clone, Attribute) or isinstance(qs_clone, Component) or isinstance(qs_clone, Link):
            return

        if isinstance(qs_clone, Material):

            texte = qs_clone.text()
            texte_upper = texte.upper()

            if texte_upper in material_upper_list:
                texte = find_new_title(texte, material_upper_list)
                texte_upper = texte.upper()

                qs_clone.setText(texte)
                qs_clone.ouvrage_lien = False

                material_list.append(texte)
                material_upper_list.append(texte_upper)

            else:

                material_list.append(texte)
                material_upper_list.append(texte_upper)
                qs_clone.setText(texte)

            # ----------------
            # link
            # ----------------

            if texte_upper in material_with_link_list:
                return

            qs_children_list = qs_clone.get_children_qs(children=True, attributes=False)

            if len(qs_children_list) == 0:
                return

            for qs_column_list in qs_children_list:

                if not isinstance(qs_column_list, list):
                    print("catalog_mane -- coller_gestion_nom_ouvrage -- not isinstance(qs_column_list, list)")
                    return

                if len(qs_column_list) != col_cat_count:
                    print("catalog_mane -- coller_gestion_nom_ouvrage -- len(qs_column_list) != columns_count")
                    return

                qs_value = qs_column_list[0]

                if not isinstance(qs_value, Link):
                    continue

                if texte_upper not in material_with_link_list:
                    material_with_link_list.append(texte_upper)
                    return
            return

        nb_enfants = qs_clone.rowCount()

        if nb_enfants == 0:
            return

        for index_child in range(nb_enfants):
            qstandarditem_child: MyQstandardItem = qs_clone.child(index_child, col_cat_value)

            self.coller_gestion_nom_ouvrage(qstandarditem_child)

    @staticmethod
    def recherche_index_valeur(qs_parent: QStandardItem, valeur: str, index_initial: int) -> int:

        if qs_parent.rowCount() == 0:
            return index_initial

        for index_qstandarditem in range(qs_parent.rowCount()):

            qstandarditem_enfant_valeur = qs_parent.child(index_qstandarditem, col_cat_value)
            valeur_actuelle = qstandarditem_enfant_valeur.text()

            if valeur_actuelle == valeur:
                return index_qstandarditem

        return index_initial

    @staticmethod
    def a___________________attribute_clean______():
        pass

    def attributes_clean_up(self):

        self.ui.attributes_detail.clear()

    @staticmethod
    def a___________________attribute_delete______():
        pass

    def attribute_delete(self) -> bool:

        qs_selection_list = self.hierarchy.get_qs_selection_list()

        if len(qs_selection_list) != 1:
            print("catalog_manage -- attribute_delete -- len(qs_selection_list) != 1")
            return False

        qs_parent = qs_selection_list[0]

        if not isinstance(qs_parent, (Material, Component)):
            print("catalog_manage -- attribute_delete -- not isinstance(qs_current, (Material, Component))")
            return False

        # -------------

        number_list = self.get_attribute_number_selection_list()

        if not isinstance(number_list, set):
            print("catalog_manage -- attribute_delete -- not isinstance(number_list, set)")
            return False

        if len(number_list) == 0:
            print("catalog_manage -- attribute_delete -- len(number_list) == 0")
            return False

        # -------------

        for number in number_list:

            if number == attribute_default_base or number == "207":
                continue

            self.attribute_delete_action(qs_parent=qs_parent, number=number)

        # -------------

        self.hierarchy.select_list(selected_list=[qs_parent], scrollto=False)

        self.ui.attributes_detail.setFocus()

    def attribute_delete_action(self, qs_parent: MyQstandardItem, number: str):

        if number == attribute_val_default_layer_first:
            number = self.tr("Groupe Layer")
            number_list = attribute_val_default_layer

        elif number == attribute_val_default_layer_first:
            number = self.tr("Groupe Remplissage")
            number_list = attribute_val_default_layer

        elif number == attribute_val_default_layer_first:
            number = self.tr("Groupe Pièce")
            number_list = attribute_val_default_layer

        else:
            number_list = [number]
            number = f"@{number}@"

        attribute_data = list()

        for number in number_list:

            qs_list = qs_parent.get_attribute_line_by_number(number=number)

            if not isinstance(qs_list, list):
                print("catalog_manage -- attribute_delete -- not isinstance(qs_list, list)")
                break

            if len(qs_list) != col_cat_count:
                print("catalog_manage -- attribute_delete -- len(qs_list) != col_cat_count")
                break

            qs_value = qs_list[col_cat_value]

            if not isinstance(qs_value, Attribute):
                print("catalog_manage -- attribute_delete -- not isinstance(qs_value, Attribute)")
                break

            row_current = qs_value.row()

            qs_list = qs_parent.takeRow(row_current)

            if not isinstance(qs_list, list):
                print("catalog_manage -- attribute_delete -- not isinstance(qs_list, list)")
                break

            if len(qs_list) != col_cat_count:
                print("catalog_manage -- attribute_delete -- len(qs_list) != col_cat_count")
                break

            attribute_data.append(AttributeData(guid_current=qs_value.data(user_guid),
                                                row_current=row_current,
                                                qs_list=qs_list))

        self.history_del_attribute(guid_parent=qs_parent.data(user_guid),
                                   attribute_data=attribute_data,
                                   parent_name=qs_parent.text(),
                                   number=number)

    def attribute_delete_unknown(self):

        search_start = self.hierarchy.cat_model.index(0, 0)

        search = self.hierarchy.cat_model.match(search_start, user_unknown, type_unknown, -1, Qt.MatchRecursive)

        if len(search) == 0:
            print("catalog_manage -- attribute_delete_unknown -- len(search) == 0")
            return

        for qm in search:

            if not qm_check(qm):
                print("catalog_manage -- attribute_delete_unknown -- not qm_check(qm)")
                continue

            # ------ Parent

            qs_parent = self.hierarchy.get_qs_by_qm(qm=qm.parent())

            if not isinstance(qs_parent, (Material, Component)):
                print("catalog_manage -- attribute_delete_unknown -- not isinstance(qs_parent, (Material, Component))")
                continue

            # ------ Number

            row_current = qm.row()

            qs_number = qs_parent.child(row_current, col_cat_number)

            if not isinstance(qs_number, Info):
                print("catalog_manage -- attribute_delete_unknown -- not isinstance(qs_number, Info)")
                continue

            number = qs_number.text()

            if not isinstance(number, str):
                print("catalog_manage -- attribute_delete_unknown -- not isinstance(number, str)")
                continue

            # ------ Delete

            self.attribute_delete_action(qs_parent=qs_parent, number=number)

        return

    @staticmethod
    def a___________________attributes_copy______():
        pass

    def attribute_cut(self):

        self.attribute_copy_search(cut=True)

    def attribute_copy(self):

        self.attribute_copy_search()

    def attribute_copy_search(self, cut=False):

        selection_list = self.get_attribute_selection_list()

        if len(selection_list) == 0:
            return

        qs_selection_list = self.hierarchy.get_qs_selection_list()

        if len(qs_selection_list) == 0:
            return

        first_qs: MyQstandardItem = qs_selection_list[0]

        if not isinstance(first_qs, MyQstandardItem):
            return

        if isinstance(first_qs, Link):
            return

        clipboard, clipboard_cut = self.get_clipboard(ele_type=attribute_code, reset_clipboard=True)

        self.clipboard_current = attribute_code

        for qlistwidgetitem in selection_list:

            qlistwidgetitem: QListWidgetItem

            widget_type = qlistwidgetitem.data(user_data_type)
            number_str = qlistwidgetitem.data(user_data_number)

            if widget_type == type_nom or widget_type == type_code or \
                    widget_type == type_lien:
                continue

            if widget_type == type_layer:

                temp_list = list()
                cut_list = list()

                for number_str in attribute_val_default_layer:

                    qs_list: list = self.attribute_copy_action(qs=first_qs, number=number_str)

                    if qs_list is None:
                        temp_list = list()
                        break

                    temp_list.extend(qs_list)
                    cut_list.append(qs_list[0])

                if len(temp_list) == 0:
                    continue

                clipboard.append(key=self.tr("Groupe Layer"),
                                 value=temp_list)

                if cut:

                    qs_value_list = self.attribute_get_original(qs_parent=first_qs,
                                                                numbers_list=list(attribute_val_default_layer.keys()))

                    if len(qs_value_list) != len(attribute_val_default_layer):
                        continue

                    clipboard_cut.append(key=self.tr("Groupe Layer"),
                                         value=[first_qs, qs_value_list])

                continue

            if widget_type == type_fill:

                temp_list = list()
                cut_list = list()

                for number_str in attribute_val_default_fill:

                    qs_list: list = self.attribute_copy_action(qs=first_qs, number=number_str)

                    if qs_list is None:
                        temp_list = list()
                        break

                    temp_list.extend(qs_list)
                    cut_list.append(qs_list[0])

                if len(temp_list) == 0:
                    continue

                clipboard.append(key=self.tr("Groupe Remplissage"),
                                 value=temp_list)

                if cut:

                    qs_value_list = self.attribute_get_original(qs_parent=first_qs,
                                                                numbers_list=list(attribute_val_default_fill.keys()))

                    if len(qs_value_list) != len(attribute_val_default_fill):
                        continue

                    clipboard_cut.append(key=self.tr("Groupe Remplissage"),
                                         value=[first_qs, qs_value_list])

                continue

            if widget_type == type_room:

                temp_list = list()
                cut_list = list()

                for number_str in attribute_val_default_room:

                    qs_list: list = self.attribute_copy_action(qs=first_qs, number=number_str)

                    if qs_list is None:
                        temp_list = list()
                        break

                    temp_list.extend(qs_list)
                    cut_list.append(qs_list[0])

                if len(temp_list) == 0:
                    continue

                clipboard.append(key=self.tr("Groupe Pièce"),
                                 value=temp_list)

                if cut:

                    qs_value_list = self.attribute_get_original(qs_parent=first_qs,
                                                                numbers_list=list(attribute_val_default_room.keys()))

                    if len(qs_value_list) != len(attribute_val_default_room):
                        continue

                    clipboard_cut.append(key=self.tr("Groupe Pièce"),
                                         value=[first_qs, qs_value_list])
                continue

            qs_list: list = self.attribute_copy_action(qs=first_qs, number=number_str)

            if qs_list is None:
                continue

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):
                continue

            qs_value: MyQstandardItem = qs_list[0]
            value = qs_value.text()

            clipboard.append(key=f"{number_str} -- {attribute_obj.name} -- {value}",
                             value=qs_list)

            if cut:

                qs_value_list = self.attribute_get_original(qs_parent=first_qs, numbers_list=[number_str])

                if len(qs_value_list) != 1:
                    continue

                clipboard_cut.append(key=f"{number_str} -- {attribute_obj.name} -- {value}",
                                     value=[first_qs, qs_value_list[0]])

        self.asc.boutons_hierarchie_coller(attribute_code)

    @staticmethod
    def attribute_get_original(qs_parent: MyQstandardItem, numbers_list: list) -> list:

        if not isinstance(qs_parent, (Material, Component)) or not isinstance(numbers_list, list):
            return list()

        qs_value_list = list()

        for number in numbers_list:

            qs_original_list: list = qs_parent.get_attribute_line_by_number(number=number)

            if len(qs_original_list) != col_cat_count:
                return list()

            qs_value_original = qs_original_list[col_cat_value]

            if not isinstance(qs_value_original, Attribute):
                continue

            qs_value_list.append(qs_value_original)

        return qs_value_list

    def get_attribute_selection_list(self) -> list:

        selection_list = self.ui.attributes_detail.selectedItems()

        if len(selection_list) == 0:
            return selection_list

        datas = dict()
        row_list = list()

        for qlistwidgetitem in selection_list:
            qlistwidgetitem: QListWidgetItem

            row_index = self.ui.attributes_detail.row(qlistwidgetitem)

            datas[row_index] = qlistwidgetitem
            row_list.append(row_index)

        row_list.sort(key=int)

        final_list = [datas[row_index] for row_index in row_list]

        return final_list

    def get_attribute_number_selection_list(self) -> list:

        number_list = set()

        selection_list = self.ui.attributes_detail.selectedItems()

        if len(selection_list) == 0:
            return number_list

        for qlistwidgetitem in selection_list:

            if not isinstance(qlistwidgetitem, QListWidgetItem):
                continue

            number = qlistwidgetitem.data(user_data_number)

            if not isinstance(number, str):
                print("catalog_manage -- get_attribute_number_selection_list -- not isinstance(number, str)")

            if number == "Lien":
                continue

            if number in number_list:
                continue

            number_list.add(number)

        return number_list

    @staticmethod
    def attribute_copy_action(qs: MyQstandardItem, number: str):

        attributes_count = qs.rowCount()

        qs_list = list()

        for attribute_index in range(attributes_count):

            qs_value: MyQstandardItem = qs.child(attribute_index, col_cat_value)
            qs_number: MyQstandardItem = qs.child(attribute_index, col_cat_number)

            if not isinstance(qs_value, Attribute) or not isinstance(qs_number, Info):
                return qs_list

            current_number: str = qs_number.text()

            if current_number != number:
                continue

            for column_index in range(col_cat_count):
                qs_copy: MyQstandardItem = qs.child(attribute_index, column_index)

                if qs_copy is None:
                    return qs_list

                qs_list.append(qs_copy.clone_creation(new=False))

            return qs_list

        return list()

    @staticmethod
    def a___________________attributes_paste______():
        pass

    def attribute_paste(self, title="", id_ele="0") -> bool:
        return self.attribute_paste_action(clipboard_attribute=self.clipboard_attribute, title=title, id_ele=id_ele)

    def attribute_paste_action(self, clipboard_attribute: ClipboardDatas, title="", id_ele="0") -> bool:

        qs_selection_list: list = self.hierarchy.get_qs_selection_list()

        if not isinstance(qs_selection_list, list):
            print("catalog_manage -- attribute_paste_action -- not isinstance(qs_selection, list)")
            return False

        # ----------------

        selection_count = len(qs_selection_list)

        if selection_count == 0:
            return False

        # ----------------

        attribute_copy = dict()

        if title == "":

            for title in clipboard_attribute.keys():
                self.attributs_coller_datas(clipboard_attribute=clipboard_attribute,
                                            titre_actuel=title,
                                            attributs_copier=attribute_copy,
                                            id_ele=id_ele)

        elif title in clipboard_attribute.keys():
            self.attributs_coller_datas(clipboard_attribute=clipboard_attribute,
                                        titre_actuel=title,
                                        attributs_copier=attribute_copy,
                                        id_ele=id_ele)

        # ----------------

        attribut_copy_count: int = len(attribute_copy)

        if attribut_copy_count == 0:
            print("catalog_manage -- attribute_paste_action -- attribut_copy_count == 0")
            return False

        # ------------------------------------------------------------------------
        # Check if single selection or extend selection
        # ------------------------------------------------------------------------

        if selection_count > 1:

            self.clipboard_attribute_cut.clear()

            if attribut_copy_count == 1:

                for attribute_data in attribute_copy.items():

                    if not isinstance(attribute_data, tuple):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(attribute_data, tuple)")
                        return False

                    if len(attribute_data) != 2:
                        print("catalog_manage -- attribute_paste_action -- len(attribute_data) != 2")
                        return False

                    qs_copied_list = attribute_data[1]

                    # qs_copied_list = ( number, [qstandarditem col0, qstandarditem col1, ...])

                    if len(qs_copied_list) != col_cat_count:
                        print("catalog_manage -- attribute_paste_action -- len(qs_copied_list) != col_cat_count")
                        return False

                    result = msg(titre=application_title,
                                 message=self.tr("Voulez-vous vraiment coller l'attribut dans "
                                                 "les éléments selectionnés?"),
                                 type_bouton=QMessageBox.Ok | QMessageBox.No,
                                 defaut_bouton=QMessageBox.Ok,
                                 icone_avertissement=True)

                    if result == QMessageBox.No or result == QMessageBox.Cancel:
                        return False

            else:

                result = msg(titre=application_title,
                             message=self.tr("Voulez-vous vraiment coller les attributs "
                                             "dans les éléments selectionnés?"),
                             type_bouton=QMessageBox.Ok | QMessageBox.No,
                             defaut_bouton=QMessageBox.Ok,
                             icone_avertissement=True)

                if result == QMessageBox.No or result == QMessageBox.Cancel:
                    return False

        # ------------------------------------------------------------------------
        # search if some attributes exist in the selection (if not cut)
        # ------------------------------------------------------------------------

        cut = self.clipboard_attribute_cut.len_datas() != 0

        # ----------------

        attribute_update = True
        attribute_exist_list = list()

        for qs_parent_select in qs_selection_list:

            if not isinstance(qs_parent_select, (Folder, Material, Component)):
                print("catalog_manage -- attribute_paste_action -- not isinstance(qs_parent, (Folder)")
                return False

            number_list = qs_parent_select.get_attribute_numbers_list()

            for number_current in number_list:

                if number_current == attribute_default_base:
                    continue

                if number_current in attribute_val_default_layer:
                    number_current = attribute_val_default_layer_first

                elif number_current in attribute_val_default_fill:
                    number_current = attribute_val_default_fill_first

                elif number_current in attribute_val_default_room:
                    number_current = attribute_val_default_room_first

                if number_current not in attribute_copy:
                    continue

                if number_current not in attribute_exist_list:
                    attribute_exist_list.append(number_current)

            # ----------------

            qs_first = qs_selection_list[0]

            if not isinstance(qs_first, Folder):

                message = self.tr("existe déjà, voulez-vous le mettre à jour?")

                if len(attribute_exist_list) != 0:

                    title = attribute_exist_list[0]

                    result = msg(titre=application_title,
                                 message=f"{title} {message}",
                                 type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                                 defaut_bouton=QMessageBox.Ok,
                                 infos="attributes_update",
                                 bt_ok=self.tr("Mettre à jour"),
                                 bt_no=self.tr("Ignorer"),
                                 icone_question=True)

                    if result == QMessageBox.Cancel:
                        return False

                    if result == QMessageBox.No:
                        attribute_update = False

        # ------------------------------------------------------------------------
        # Cut Datas attribute
        # ------------------------------------------------------------------------

        if cut:

            result = self.attribute_get_cut_datas()

            if not isinstance(result, tuple):
                print("catalog_manage -- attribute_paste_action -- not isinstance(result, tuple)")
                return False

            if len(result) != 2:
                print("catalog_manage -- attribute_paste_action -- not isinstance(result, tuple)")
                return False

            # ----------------

            qs_parent_original, attribute_original_dict = result

            if not isinstance(qs_parent_original, MyQstandardItem) or not isinstance(attribute_original_dict, dict):
                print(
                    "catalog_manage -- attribute_paste_action -- "
                    "not isinstance(qs_parent_original, MyQstandardItem)")
                return False

            if len(attribute_original_dict) == 0:
                print("catalog_manage -- attribute_paste_action -- len(attribute_original_dict) == 0")
                return False

            # ----------------

            guid_parent_original = qs_parent_original.data(user_guid)

            if not isinstance(guid_parent_original, str):
                print("catalog_manage -- attribute_paste_action -- not isinstance(guid_parent_original, str)")
                return False

            # ----------------

            parent_name_original = qs_parent_original.text()

            if not isinstance(parent_name_original, str):
                print("catalog_manage -- attribute_paste_action -- not isinstance(parent_name_original, str)")
                return False

            # ----------------

        else:
            qs_parent_original = MyQstandardItem()
            attribute_original_dict = dict()
            guid_parent_original = ""
            parent_name_original = ""

        # ------------------------------------------------------------------------
        # Copy
        # ------------------------------------------------------------------------

        for qs_parent_select in qs_selection_list:

            if not isinstance(qs_parent_select, MyQstandardItem):
                print("catalog_manage -- attribute_paste_action -- not isinstance(qs_parent_select, MyQstandardItem)")
                return False

            guid_parent_select = qs_parent_select.data(user_guid)

            number_list = qs_parent_select.get_attribute_numbers_list()

            attribute_data_layer = list()
            attribute_data_fill = list()
            attribute_data_room = list()

            value_dict_layer = dict()
            value_dict_fill = dict()
            value_dict_room = dict()

            for number_current in attribute_copy:

                if not cut:

                    # ----------------------------------
                    #  Update attribute -> if attribute exists and attribute update
                    # ----------------------------------

                    if number_current in number_list and attribute_update:

                        qs_select_list = qs_parent_select.get_attribute_line_by_number(number_current)

                        if len(qs_select_list) != col_cat_count:
                            print("catalog_manage -- attribute_paste_action -- "
                                  "len(qs_select_list) != col_cat_count")
                            return False

                        # ----------------

                        qs_value_select, qs_index_select = qs_select_list[col_cat_value], qs_select_list[col_cat_index]

                        if not isinstance(qs_value_select, Attribute) or not isinstance(qs_index_select, Info):
                            print("catalog_manage -- attribute_paste_action -- "
                                  "not isinstance(qs_value_select, Attribute)")
                            return False

                        # ----------------

                        value_select = qs_value_select.text()
                        value_index_select = qs_index_select.text()

                        # ----------------

                        qs_value_original = attribute_copy[number_current][col_cat_value]
                        qs_index_original = attribute_copy[number_current][col_cat_index]

                        if not isinstance(qs_value_original, Attribute) or not isinstance(qs_index_original, Info):
                            print("catalog_manage -- attribute_paste_action -- "
                                  "not isinstance(qs_value_original, Attribute)")
                            return False

                        # ----------------

                        value_original = qs_value_original.text()
                        value_index_original = qs_index_original.text()

                        # ----------------

                        # print(f"{value_current} ({value_current}) --> {value_new} ({value_index_new})")

                        # ----------------

                        qs_value_select.setText(value_original)
                        qs_index_select.setText(value_index_original)

                        # ----------------

                        self.change_made = True

                        # ---------------- History -----

                        if number_current in attribute_val_default_layer:

                            data = AttributeModifyData(number_current=number_current,
                                                       value_new=value_select,
                                                       value_index_new=value_index_select)

                            attribute_data_layer.append(data)

                            # -------------------

                            value_dict_layer[number_current] = [value_select, value_original]

                            # -------------------

                            if number_current != attribute_val_default_layer_last:
                                continue

                            self.history_modify_attribute(guid_parent=guid_parent_select,
                                                          attribute_data=attribute_data_layer,
                                                          parent_name=qs_parent_select.text(),
                                                          value_dict=value_dict_layer,
                                                          attribute_type=self.tr("Groupe Layer"))
                            continue

                        if number_current in attribute_val_default_fill:

                            data = AttributeModifyData(number_current=number_current,
                                                       value_new=value_select,
                                                       value_index_new=value_index_select)

                            attribute_data_fill.append(data)

                            # -------------------

                            value_dict_fill[number_current] = [value_select, value_original]

                            # -------------------

                            if number_current != attribute_val_default_fill_last:
                                continue

                            self.history_modify_attribute(guid_parent=guid_parent_select,
                                                          attribute_data=attribute_data_fill,
                                                          parent_name=qs_parent_select.text(),
                                                          value_dict=value_dict_fill,
                                                          attribute_type=self.tr("Groupe Remplissage"))

                            continue

                        if number_current in attribute_val_default_room:

                            data = AttributeModifyData(number_current=number_current,
                                                       value_new=value_select,
                                                       value_index_new=value_index_select)

                            attribute_data_room.append(data)

                            # -------------------

                            value_dict_layer[number_current] = [value_select, value_original]

                            # -------------------

                            if number_current != attribute_val_default_room_last:
                                continue

                            self.history_modify_attribute(guid_parent=guid_parent_select,
                                                          attribute_data=attribute_data_room,
                                                          parent_name=qs_parent_select.text(),
                                                          value_dict=value_dict_room,
                                                          attribute_type=self.tr("Groupe Pièce"))

                            continue

                        data = AttributeModifyData(number_current=number_current,
                                                   value_new=value_select,
                                                   value_index_new=value_index_select)

                        # -------------------

                        self.history_modify_attribute(guid_parent=guid_parent_select,
                                                      attribute_data=[data],
                                                      parent_name=qs_parent_select.text(),
                                                      value_dict={number_current: [value_select, value_original]})

                        # ----------------

                        if number_current == "207":
                            self.attributs_update_description(qs_current=qs_parent_select,
                                                              value_new=value_select)

                        continue

                    # ----------------------------------
                    #  Creation if attribute not exists
                    # ----------------------------------

                    if number_current not in number_list:

                        index_insertion = qs_parent_select.get_attribute_insertion_index(number=number_current)

                        qs_list_new = list()
                        qs_list_current: list = attribute_copy[number_current]

                        for qs_current_column in qs_list_current:

                            if not isinstance(qs_current_column, MyQstandardItem):
                                print("catalog_manage -- attribute_paste_action -- "
                                      "not isinstance(qs_current_column, MyQstandardItem)")
                                return False

                            qs_cloned = qs_current_column.clone_creation(new=True)

                            if qs_current_column.column() == col_cat_value:
                                qs_current_column.clone_children(qs_original=qs_current_column,
                                                                 qs_destination=qs_cloned,
                                                                 new=True)

                            qs_list_new.append(qs_cloned)

                        # ----------------

                        if len(qs_list_new) != col_cat_count:
                            print("catalog_manage -- attribute_paste_action -- len(qs_list_new) != col_cat_count")
                            return False

                        # ----------------

                        qs_parent_select.insertRow(index_insertion, qs_list_new)

                        # ----------------

                        self.change_made = True

                        # ----------------

                        qs_value_new = qs_list_new[col_cat_value]

                        if not isinstance(qs_value_new, Attribute):
                            print("catalog_manage -- attribute_paste_action -- not isinstance(qs_value_new, Attribute)")
                            return False

                        guid_current = qs_value_new.data(user_guid)

                        # ---------------- History -----

                        if number_current in attribute_val_default_layer:

                            attribute_data_layer.append(AttributeData(guid_current=guid_current,
                                                                      row_current=index_insertion,
                                                                      qs_list=qs_list_new))

                            if number_current == attribute_val_default_layer_last:
                                self.history_add_attribute(guid_parent=qs_parent_select.data(user_guid),
                                                           attribute_data=attribute_data_layer,
                                                           parent_name=qs_parent_select.text(),
                                                           number=self.tr("Groupe Layer"))

                            continue

                        # -------------------

                        if number_current in attribute_val_default_fill:

                            attribute_data_fill.append(AttributeData(guid_current=guid_current,
                                                                     row_current=index_insertion,
                                                                     qs_list=qs_list_new))

                            if number_current == attribute_val_default_fill_last:
                                self.history_add_attribute(guid_parent=guid_parent_select,
                                                           attribute_data=attribute_data_fill,
                                                           parent_name=qs_parent_select.text(),
                                                           number=self.tr("Groupe Remplissage"))

                            continue

                        # -------------------

                        if number_current in attribute_val_default_room:

                            attribute_data_room.append(AttributeData(guid_current=guid_current,
                                                                     row_current=index_insertion,
                                                                     qs_list=qs_list_new))

                            if number_current == attribute_val_default_room_last:
                                self.history_add_attribute(guid_parent=qs_parent_select.data(user_guid),
                                                           attribute_data=attribute_data_room,
                                                           parent_name=qs_parent_select.text(),
                                                           number=self.tr("Groupe Pièce"))

                            continue

                        # -------------------

                        attribute_data = [AttributeData(guid_current=guid_current,
                                                        row_current=index_insertion,
                                                        qs_list=qs_list_new)]

                        self.history_add_attribute(guid_parent=qs_parent_select.data(user_guid),
                                                   attribute_data=attribute_data,
                                                   parent_name=qs_parent_select.text(),
                                                   number=f"@{number_current}@")

                        continue

                    else:
                        print("catalog_manage -- attribute_paste_action -- ignore")
                        continue

                attribute_data = attribute_original_dict.get(number_current)

                if not isinstance(attribute_data, AttributeCutData):
                    print("catalog_manage -- attribute_paste_action -- not isinstance(qs_value, Attribute)")
                    return False

                # -----------------

                if number_current in number_list and attribute_update:

                    attribute_data.attribute_delete = False

                    # -----------------

                    qs_list_select = qs_parent_select.get_attribute_line_by_number(number=number_current)

                    if not isinstance(qs_list_select, list):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(qs_list_select, list)")
                        return False

                    if len(qs_list_select) != col_cat_count:
                        print("catalog_manage -- attribute_paste_action -- len(qs_list_select) != col_cat_count")
                        return False

                    # -------------------

                    qs_value_select = qs_list_select[col_cat_value]

                    if not isinstance(qs_value_select, Attribute):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(qs_value_select, Attribute)")
                        return False

                    # -------------------

                    row_select = qs_value_select.row()

                    if row_select == -1:
                        print("catalog_manage -- attribute_paste_action -- row_select == -1")
                        return False

                    # -------------------

                    value_select = qs_value_select.text()

                    if not isinstance(value_select, str):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(value_select, str)")
                        return False

                    # -------------------

                    guid_select = qs_value_select.data(user_guid)

                    if not isinstance(guid_select, str):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(guid_select, str)")
                        return False

                    # -------------------

                    qs_value_index_select = qs_list_select[col_cat_index]

                    if not isinstance(qs_value_index_select, Info):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(qs_value_index_select, Info)")
                        return False

                    # -------------------

                    value_index_select = qs_value_index_select.text()

                    if not isinstance(value_index_select, str):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(value_index_select, str)")
                        return False

                    # -----------------

                    qs_list_original = qs_parent_original.get_attribute_line_by_number(number=number_current)

                    if not isinstance(qs_list_original, list):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(qs_list_original, list)")
                        return False

                    if len(qs_list_original) != col_cat_count:
                        print("catalog_manage -- attribute_paste_action -- len(qs_list_original) != col_cat_count")
                        return False

                    # -------------------

                    qs_value_original = qs_list_original[col_cat_value]

                    if not isinstance(qs_value_original, Attribute):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(qs_value_select, Attribute)")
                        return False

                    # -------------------

                    qs_value_index_original = qs_list_original[col_cat_index]

                    if not isinstance(qs_value_index_original, Info):
                        print("catalog_manage -- attribute_paste_action -- "
                              "not isinstance(qs_value_index_original, Info)")
                        return False

                    # -------------------

                    row_original = qs_value_original.row()

                    if row_original == -1:
                        print("catalog_manage -- attribute_paste_action -- row_original == -1")
                        return False

                    # ------------------- Save Select Datas

                    attribute_data.row_select = row_select
                    attribute_data.guid_select = guid_select
                    attribute_data.value_select = value_select
                    attribute_data.value_index_select = value_index_select

                    # ------------------- Copy original Datas

                    qs_value_select.setText(attribute_data.value_original)
                    qs_value_select.setData(attribute_data.guid_original)

                    qs_value_index_select.setText(attribute_data.value_index_original)

                    # ------------------- suppression original

                    qs_list_original = qs_parent_original.takeRow(row_original)

                    if not isinstance(qs_list_original, list):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(qs_list_original, list)")
                        return False

                    if len(qs_list_original) != col_cat_count:
                        print("catalog_manage -- attribute_paste_action -- len(qs_list_original) != col_cat_count")
                        return False

                elif number_current not in number_list:

                    attribute_data.attribute_delete = True

                    row_select = qs_parent_select.get_attribute_insertion_index(number=number_current)

                    # -------------------

                    qs_list_original = attribute_data.qs_list_original

                    if not isinstance(qs_list_original, list):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(qs_list_original, list)")
                        return False

                    if len(qs_list_original) != col_cat_count:
                        print("catalog_manage -- attribute_paste_action -- len(qs_list_original) != col_cat_count")
                        return False

                    # -------------------

                    qs_list_select = list()
                    row_original = -1

                    for qs_current_column in qs_list_original:

                        if not isinstance(qs_current_column, MyQstandardItem):
                            print("catalog_manage -- attribute_paste_action -- "
                                  "not isinstance(qs_current_column, MyQstandardItem)")
                            return False

                        qs_cloned = qs_current_column.clone_creation(new=False)

                        if qs_current_column.column() == col_cat_value:
                            row_original = qs_current_column.row()

                            qs_current_column.clone_children(qs_original=qs_current_column,
                                                             qs_destination=qs_cloned,
                                                             new=False)

                        qs_list_select.append(qs_cloned)

                    # -------------------

                    qs_parent_select.insertRow(row_select, qs_list_select)

                    # ------------------- Delete original

                    qs_list_original = qs_parent_original.takeRow(row_original)

                    if not isinstance(qs_list_original, list):
                        print("catalog_manage -- attribute_paste_action -- not isinstance(qs_list_original, list)")
                        return False

                    if len(qs_list_original) != col_cat_count:
                        print("catalog_manage -- attribute_paste_action -- len(qs_list_original) != col_cat_count")
                        return False

                    attribute_data.row_original = row_original
                    attribute_data.qs_list_original = qs_list_original

                    # -------------------

                else:
                    print("catalog_manage -- attribute_paste_action -- ignore")
                    continue

                self.change_made = True

                # ----------------- History

                if number_current in attribute_val_default_layer:

                    attribute_data_layer.append(attribute_data)

                    if number_current == attribute_val_default_layer_last:
                        self.history_cut_attribute(guid_parent_original=guid_parent_original,
                                                   guid_parent_select=guid_parent_select,
                                                   attribute_data=attribute_data_layer,
                                                   parent_name=parent_name_original,
                                                   number=self.tr("Groupe Layer"))

                    continue

                # -------------------

                if number_current in attribute_val_default_fill:

                    attribute_data_fill.append(attribute_data)

                    if number_current == attribute_val_default_fill_last:
                        self.history_cut_attribute(guid_parent_original=guid_parent_original,
                                                   guid_parent_select=guid_parent_select,
                                                   attribute_data=attribute_data_fill,
                                                   parent_name=parent_name_original,
                                                   number=self.tr("Groupe Remplissage"))

                    continue

                # -------------------

                if number_current in attribute_val_default_room:

                    attribute_data_room.append(attribute_data)

                    if number_current == attribute_val_default_room_last:
                        self.history_cut_attribute(guid_parent_original=guid_parent_original,
                                                   guid_parent_select=guid_parent_select,
                                                   attribute_data=attribute_data_room,
                                                   parent_name=parent_name_original,
                                                   number=self.tr("Groupe Pièce"))

                    continue

                # -------------------

                self.history_cut_attribute(guid_parent_original=guid_parent_original,
                                           guid_parent_select=guid_parent_select,
                                           attribute_data=[attribute_data],
                                           parent_name=parent_name_original,
                                           number=f"@{number_current}@")

                # -------------------

        self.clipboard_attribute_cut.clear()

        # -------------------

        qs_selection = qs_selection_list[-1]

        if not isinstance(qs_selection, (Folder, Material, Component)):
            return True

        self.hierarchy.select_list(selected_list=[qs_selection], scrollto=True, expand=True)
        return True

    def attribut_coller_recherche(self, liste_selections_qstandarditem: list, message=False) -> bool:

        nb_selections = len(liste_selections_qstandarditem)

        nb_attribut_copier: int = self.clipboard_attribute.len_datas()
        nb_attribut_couper: int = self.clipboard_attribute_cut.len_datas()

        if nb_selections == 0 or nb_attribut_copier == 0:
            return False

        qstandarditem: MyQstandardItem = liste_selections_qstandarditem[0]

        if not isinstance(qstandarditem, MyQstandardItem):
            return False

        if isinstance(qstandarditem, Link):
            return False

        if isinstance(qstandarditem, Folder):

            if nb_attribut_copier != 1:
                return False

            if nb_attribut_couper != 0:
                return False

            liste_titres: list = self.clipboard_attribute.keys()

            for key in liste_titres:

                if "207" in key:
                    return True

            return False

        if len(liste_selections_qstandarditem) > 1 and nb_attribut_couper != 0:

            if not message:
                return False

            if nb_attribut_couper == 2:
                msg(titre=application_title,
                    message=self.tr("Impossible de couper/coller un attribut dans plusieurs éléments."),
                    icone_critique=True)
                return False

            msg(titre=application_title,
                message=self.tr("Impossible de couper/coller des attributs dans plusieurs éléments."),
                icone_critique=True)
            return False

        return True

    def attributs_coller_datas(self, clipboard_attribute: ClipboardDatas,
                               titre_actuel: str, attributs_copier: dict, id_ele="0"):

        liste_attributs_a: list = clipboard_attribute.get_datas_title(titre_actuel, id_ele)
        nb_items = len(liste_attributs_a)

        if nb_items == 0:
            return

        liste_attributs_a: list = liste_attributs_a[0]

        nb_items = len(liste_attributs_a)

        if titre_actuel == self.tr("Groupe Layer"):

            if nb_items != col_cat_count * len(attribute_val_default_layer):
                print("onglet_hierarchie -- attributs_coller_action --> nb_items != nb_colonnes * 5")
                return

            index_1 = 0
            index_2 = 1

            for numero in attribute_val_default_layer:
                attributs_copier[numero] = liste_attributs_a[col_cat_count * index_1:col_cat_count * index_2]
                index_1 += 1
                index_2 += 1
            return

        if titre_actuel == self.tr("Groupe Remplissage"):

            if nb_items != col_cat_count * len(attribute_val_default_fill):
                print("onglet_hierarchie -- attributs_coller_action --> nb_items != nb_colonnes * 5")
                return

            index_1 = 0
            index_2 = 1

            for numero in attribute_val_default_fill:
                attributs_copier[numero] = liste_attributs_a[col_cat_count * index_1:col_cat_count * index_2]
                index_1 += 1
                index_2 += 1
            return

        if titre_actuel == self.tr("Groupe Pièce"):

            if nb_items != col_cat_count * len(attribute_val_default_room):
                print("onglet_hierarchie -- attributs_coller_action --> nb_items != nb_colonnes * 6")
                return

            index_1 = 0
            index_2 = 1

            for numero in attribute_val_default_room:
                attributs_copier[numero] = liste_attributs_a[col_cat_count * index_1:col_cat_count * index_2]
                index_1 += 1
                index_2 += 1
            return

        if " -- " not in titre_actuel:
            print("onglet_hierarchie -- attributs_coller_action --> titre non valide")
            return

        numero, _ = titre_actuel.split(sep=" -- ", maxsplit=1)
        datas = clipboard_attribute.get_datas_title(titre_actuel, id_ele)

        if len(datas) != 0:
            attributs_copier[numero] = datas[0]

    def attributs_update_description(self, qs_current: MyQstandardItem, value_new: str) -> bool:

        if not isinstance(value_new, str):
            print("catalog_manage -- attributs_update_description -- not isinstance(value_new, str)")
            return False

        if not isinstance(qs_current, (Folder, Material, Component)):
            print("catalog_manage -- attributs_update_description -- not isinstance(qs_current, Folder)")
            return False

        # ----------------

        qs_parent = qs_current.parent()

        if qs_parent is None:
            qs_parent = self.hierarchy.cat_model.invisibleRootItem()

        if not isinstance(qs_parent, QStandardItem):
            print("catalog_manage -- attributs_update_description -- not isinstance(qs_parent, QStandardItem)")
            return False

        # ----------------

        current_row = qs_current.row()

        # ----------------

        qs_desc = qs_parent.child(current_row, col_cat_desc)

        if not isinstance(qs_desc, Info):
            print("catalog_manage -- attributs_update_description -- not isinstance(qs_desc, Info)")
            return False

        qs_desc.setText(value_new)

        # ----------------

        if not isinstance(qs_current, Material):
            return True

        material_name = qs_current.text()

        if not isinstance(material_name, str):
            print("catalog_manage -- attributs_update_description -- not isinstance(material_name, str)")
            return False

        self.material_desc_changed(material_name=material_name, link_desc_after=value_new)

        return True

    def attribute_get_cut_datas(self):

        attribute_dict = dict()

        qs_parent_original = None
        cut_values = self.clipboard_attribute_cut.get_values_list()

        if not isinstance(cut_values, list):
            print("catalog_manage -- attribute_get_cut_datas -- not isinstance(value, list)")
            return None, dict()

        if len(cut_values) == 0:
            return

        for datas in cut_values:

            if not isinstance(datas, list):
                print("catalog_manage -- attribute_get_cut_datas -- not isinstance(datas, list)")
                return None, dict()

            # ---------

            if len(datas) != 2:
                print("catalog_manage -- attribute_get_cut_datas -- len(datas) != 2")
                return None, dict()

            # ---------

            qs_parent_original, qs_attribute_list = datas

            if not isinstance(qs_parent_original, (Folder, Material, Component)):
                print("catalog_manage -- attribute_get_cut_datas -- not isinstance(qs_parent, MyQstandardItem)")
                return None, dict()

            # ---------

            row_parent_original = qs_parent_original.row()

            if row_parent_original == -1:

                guid_parent_original = qs_parent_original.data(user_guid)

                if not isinstance(guid_parent_original, str):
                    print("catalog_manage -- attribute_get_cut_datas -- not isinstance(guid_parent_original, str)")
                    return None, dict()

                qs_parent_original = self.guid_get_qs(guid=guid_parent_original)

                if not isinstance(qs_parent_original, (Folder, Material, Component)):
                    return None, dict()

                row_parent_original = qs_parent_original.row()

                if row_parent_original == -1:
                    print("catalog_manage -- attribute_get_cut_datas -- row_parent_original == -1")
                    return None, dict()

            # ===================================

            if isinstance(qs_attribute_list, list):

                for qs_value in qs_attribute_list:

                    result = self.attribute_get_cut_infos(qs_parent=qs_parent_original, qs_value=qs_value)

                    if not isinstance(result, tuple):
                        print("catalog_manage -- attribute_get_cut_datas -- not isinstance(result, tuple)")
                        return None, dict()

                    if len(result) != 2:
                        print("catalog_manage -- attribute_get_cut_datas -- len(result) != 2")
                        return None, dict()

                    number, data = result

                    attribute_dict[number] = data

            elif isinstance(qs_attribute_list, Attribute):

                result = self.attribute_get_cut_infos(qs_parent=qs_parent_original, qs_value=qs_attribute_list)

                if not isinstance(result, tuple):
                    print("catalog_manage -- attribute_get_cut_datas -- not isinstance(result, tuple)")
                    continue

                if len(result) != 2:
                    print("catalog_manage -- attribute_get_cut_datas -- len(result) != 2")
                    continue

                number, data = result

                attribute_dict[number] = data

            else:
                print("catalog_manage -- attribute_get_cut_datas -- error type)")
                return None, dict()

        return qs_parent_original, attribute_dict

    def attribute_get_cut_infos(self, qs_parent: MyQstandardItem, qs_value: Attribute):

        # print(qs_parent.rowCount(), qs_parent.text(), qs_parent.data(user_guid))

        if not isinstance(qs_value, Attribute):
            print("catalog_manage -- attribute_get_cut_infos -- not isinstance(qs_attribute, Attribute)")
            return

            # -------------

        guid_original = qs_value.data(user_guid)

        if not isinstance(guid_original, str):
            print("catalog_manage -- attribute_get_cut_infos -- not isinstance(guid_original, str)")
            return

        # -------------

        row_original = qs_value.row()

        if row_original == -1:

            qs_value = self.guid_get_qs(guid=guid_original, parent=qs_parent.index)

            if not isinstance(qs_value, Attribute):
                print("catalog_manage -- attribute_get_cut_infos -- not isinstance(qs_attribute, Attribute)")
                return

            row_original = qs_value.row()

            if row_original == -1:
                print("catalog_manage -- attribute_get_cut_infos -- not isinstance(qs_attribute, Attribute)")
                return

        # -------------

        value_original = qs_value.text()

        if not isinstance(value_original, str):
            print("catalog_manage -- attribute_get_cut_infos -- not isinstance(value_original, str)")
            return

        # -------------

        qs_number = qs_parent.child(row_original, col_cat_number)

        if not isinstance(qs_number, Info):
            print("catalog_manage -- attribute_get_cut_infos -- not isinstance(qs_number, Info)")
            return

        # -------------

        number_current = qs_number.text()

        if not isinstance(number_current, str):
            print("catalog_manage -- attribute_get_cut_infos -- not isinstance(number_current, str)")
            return

        # -------------

        qs_index = qs_parent.child(row_original, col_cat_index)

        if not isinstance(qs_index, Info):
            print("catalog_manage -- attribute_get_cut_infos -- not isinstance(qs_index, Info)")
            return

        # -------------

        value_index_original = qs_index.text()

        if not isinstance(value_index_original, str):
            print("catalog_manage -- attribute_get_cut_infos -- not isinstance(value_index_original, str)")
            return

        # print(f"parent: {qs_parent.text()} (guid: {guid_original}, "
        #       f"number: {number_current}, row_current: {row_original}")

        return number_current, AttributeCutData(number_current=number_current,
                                                guid_original=guid_original,
                                                row_original=row_original,
                                                qs_list_original=[qs_value, qs_index, qs_number],
                                                value_original=value_original,
                                                value_index_original=value_index_original)

    @staticmethod
    def a___________________gestion_erreurs___________________():
        pass

    def select_first_formula_error(self):

        if not self.ui.search_error_bt.isChecked():
            return

        if self.hierarchy.cat_filter_2.rowCount() == 0:
            self.ui.search_error_bt.setChecked(False)
            self.ui.search_error_bt.clicked.emit()
            return

        self.hierarchy.select_first_formula()

        attributes_count = self.ui.attributes_detail.count()

        for row_index in range(attributes_count):

            qlw = self.ui.attributes_detail.item(row_index)

            if not isinstance(qlw, QListWidgetItem):
                print("catalog_manage -- select_first_formula_error -- not isinstance(qlw, QListWidgetItem)")
                continue

            if qlw.data(user_data_type) != type_formule:
                continue

            widget = self.ui.attributes_detail.itemWidget(qlw)

            try:
                plain_text_edit = widget.ui.value_attrib
                plain_text_edit.setFocus()

                cursor = plain_text_edit.textCursor()
                cursor.movePosition(QTextCursor.End)
                plain_text_edit.setTextCursor(cursor)
            except Exception:
                pass

            return

    def formula_find_similar(self, qs_formula: Attribute) -> list:

        if not isinstance(qs_formula, Attribute):
            print("catalog_manage -- formula_find_similar -- not isinstance(qs_formula, Attribute)")
            return list()

        formula_current = qs_formula.text()

        if not isinstance(formula_current, str):
            print("catalog_manage -- formula_find_similar -- not isinstance(formula_current, str)")
            return list()

        search_start = self.hierarchy.cat_model.index(0, col_cat_value)

        search = self.hierarchy.cat_model.match(search_start, Qt.DisplayRole, formula_current, -1,
                                                Qt.MatchRecursive | Qt.MatchExactly)

        return search

    def formula_correct(self, qs_formula: Attribute, number_current: str, value_new: str) -> bool:

        if not self.ui.search_error_bt.isChecked():
            return False

        if not isinstance(value_new, str) or not isinstance(number_current, str):
            print("catalog_manage -- formula_correct -- not isinstance(value_new, str)")
            return False

        qm_list = self.formula_find_similar(qs_formula=qs_formula)

        similar_count = len(qm_list)

        if similar_count < 2:
            print("catalog_manage -- formula_correct -- len(qm_list) < 2>")
            return False

        message = self.tr("Voulez-vous corriger les {x} formules identiques?")
        message = message.replace("{x}", f"{similar_count}")

        if msg(titre=application_title,
               message=message,
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               defaut_bouton=QMessageBox.No,
               icone_question=True) != QMessageBox.Ok:
            return False

        qm_current = qs_formula.index()

        for qm in qm_list:

            if qm == qm_current:
                continue

            if not qm_check(qm):
                print("catalog_manage -- formula_correct -- not qm_check(qm)")
                continue

            qm: QModelIndex

            # -------------

            value_current = qm.data()

            if value_current == value_new:
                continue

            # -------------

            qm_parent = qm.parent()

            if not qm_check(qm_parent):
                print("catalog_manage -- formula_correct -- not qm_check(qm_parent)")
                continue

            # -------------

            guid_parent = qm_parent.data(user_guid)

            if not isinstance(guid_parent, str):
                print("catalog_manage -- formula_correct -- not isinstance(guid_parent, str)")
                continue

            # -------------

            parent_name = qm_parent.data()

            if not isinstance(parent_name, str):
                print("catalog_manage -- formula_correct -- not isinstance(parent_name, str)")
                continue

            # -------------

            data = AttributeModifyData(number_current=number_current, value_new=value_current)

            attribute_data = [data]

            value_dict = {number_current: [value_current, value_new]}

            # -------------

            self.hierarchy.cat_model.setData(qm, value_new)
            self.hierarchy.cat_model.setData(qm, "", user_formule_ok)

            # -------------

            self.history_modify_attribute(guid_parent=guid_parent, attribute_data=attribute_data,
                                          parent_name=parent_name, value_dict=value_dict)

        if self.hierarchy.cat_filter_2.rowCount() == 0:
            msg(titre=application_title,
                message=self.tr("Aucune formule avec erreur trouvée!"),
                icone_valide=True)

            self.hierarchy.search_clear()

    @staticmethod
    def a___________________gestion_renommer___________________():
        pass

    def renommer_item(self):

        if self.ui.attributes_detail.count() == 0:
            return

        qlistwidgetitem: QListWidgetItem = self.ui.attributes_detail.item(0)

        widget = self.ui.attributes_detail.itemWidget(qlistwidgetitem)

        if not isinstance(widget, AttributeCode) and not isinstance(widget, AttributeName):
            return

        widget.ui.value_attrib.selectAll()
        widget.ui.value_attrib.setFocus()

    @staticmethod
    def a___________________gestion_formule_parentheses______():
        pass

    def change_highlighter(self):

        self.allplan.formula_color = not self.allplan.formula_color
        self.formula_color_change_signal.emit()

    @staticmethod
    def a___________________history_tools___________________():
        pass

    def get_special_number(self, qs_parent: MyQstandardItem, number: str) -> Tuple[str, dict]:
        """
        Rechercher si numéro d'attribut est un numéro spécial.
        :param qs_parent:
        :param number:
        :return: type de d'attribut , dict {index_ele : liste_ele}
        """

        if number in attribute_val_default_layer:
            return "Layer", self.creation_liste_complementaire(qs_parent=qs_parent,
                                                               datas_dict=attribute_val_default_layer)

        if number in attribute_val_default_fill:
            return "Remplissage", self.creation_liste_complementaire(qs_parent=qs_parent,
                                                                     datas_dict=attribute_val_default_fill)

        if number in attribute_val_default_room:
            return "Pièce", self.creation_liste_complementaire(qs_parent=qs_parent,
                                                               datas_dict=attribute_val_default_room)

        return "", dict()

    @staticmethod
    def creation_liste_complementaire(qs_parent: MyQstandardItem, datas_dict: dict) -> dict:

        dict_complementaires = dict()

        for numero_rechercher in datas_dict:

            qs_list = qs_parent.get_attribute_line_by_number(number=numero_rechercher)

            if not isinstance(qs_list, list):
                print("catalog_manage -- creation_liste_complementaire -- not isinstance(qs_list, list)")
                continue

            if len(qs_list) != col_cat_count:
                print("catalog_manage -- creation_liste_complementaire -- len(qs_list) != col_cat_count")
                continue

            qs_value = qs_list[col_cat_value]

            if not isinstance(qs_value, Attribute):
                print("catalog_manage -- creation_liste_complementaire -- not isinstance(qs_value, Attribute)")
                continue

            index_ele = qs_value.row() + 1

            liste_ele = [qs_parent.child(index_ele, index_colonne)
                         for index_colonne in range(col_cat_count)
                         if qs_parent.child(index_ele, index_colonne) is not None]

            dict_complementaires[index_ele] = liste_ele

        return dict_complementaires

    def guid_get_qs(self, guid: str, parent=None, column=col_cat_value):

        if not isinstance(guid, str):
            print("catalog_manage -- guid_get_qs -- not isinstance(guid, str)")
            return None

        if self.hierarchy.cat_model.invisibleRootItem().data(user_guid) == guid:
            return self.hierarchy.cat_model.invisibleRootItem()

        if isinstance(parent, QModelIndex):
            start_search = self.hierarchy.cat_model.index(0, column, parent)
        else:
            start_search = self.hierarchy.cat_model.index(0, column)

        search = self.hierarchy.cat_model.match(start_search, user_guid, guid, -1, Qt.MatchExactly | Qt.MatchRecursive)

        if len(search) != 1:
            print("catalog_manage -- guid_get_qs -- len(search) != 1")
            return None

        qs = self.hierarchy.get_qs_by_qm(qm=search[0])

        if not isinstance(qs, QStandardItem):
            print("catalog_manage -- guid_get_qs -- not isinstance(qs, QStandardItem)")
            return None

        return qs

    @staticmethod
    def a___________________history___________________():
        pass

    def history_add_ele(self, qs_current: MyQstandardItem, paste=False):

        ele_type = qs_current.data(user_data_type)
        ele_name = qs_current.text()

        if paste:
            title = self.tr("Coller")
            action_name = f'{title} {ele_type} : {ele_name}'

        else:
            title = self.tr("Ajout")
            action_name = f'{title} {ele_type} : {ele_name}'

        self.undo_list.action_add_ele(action_name=action_name, qs_current=qs_current)

        self.redo_clear()
        self.undo_button_manage()

    def history_del_ele(self, qs_parent: QStandardItem, qs_current: QStandardItem, row_current: int, qs_list: list):

        ele_type = qs_current.data(user_data_type)
        ele_name = qs_current.text()

        title = self.tr("Supprimer")

        self.undo_list.action_del_ele(action_name=f'{title} {ele_type} : {ele_name}',
                                      guid_parent=qs_parent.data(user_guid),
                                      qs_current=qs_current,
                                      row_current=row_current,
                                      qs_list=qs_list)

        self.redo_clear()
        self.undo_button_manage()

    def history_move_ele(self, qs_current: QStandardItem, row_current: int, row_new: int):

        title = self.tr("Déplacement")
        ele_name = qs_current.text()

        self.undo_list.action_move_ele(action_name=f"{title} : {ele_name}",
                                       guid_current=qs_current.data(user_guid),
                                       row_current=row_new,
                                       row_new=row_current)

        self.redo_clear()
        self.undo_button_manage()

    def history_cut_ele(self, guid_parent_new: str, qs_current: QStandardItem, row_new: int):

        ele_type = qs_current.data(user_data_type)
        ele_name = qs_current.text()

        title = self.tr("Couper/Coller")

        self.undo_list.action_cut_ele(action_name=f'{title} {ele_type} : {ele_name}',
                                      guid_parent_new=guid_parent_new,
                                      guid_current=qs_current.data(user_guid),
                                      row_new=row_new)

        self.redo_clear()
        self.undo_button_manage()

    def history_move_materials(self, guid_parent: str, guid_material: str, guid_new_folder: str, material_name):

        action_name = self.tr("Déplacement vers dossier")
        action_name += f": {material_name}"

        self.undo_list.action_move_materials(action_name=action_name,
                                             guid_parent=guid_parent,
                                             guid_new_folder=guid_new_folder,
                                             guid_material=guid_material)

        self.redo_clear()
        self.undo_button_manage()

    def history_change_icon(self, qs_current: QStandardItem):

        title = self.tr("Changement icône")
        ele_name = qs_current.text()

        self.undo_list.action_change_icon(action_name=f"{title} : {ele_name}",
                                          guid_current=qs_current.data(user_guid),
                                          icon_new=qs_current.icon())

        self.redo_clear()
        self.undo_button_manage()

    def history_add_attribute(self, guid_parent: str, attribute_data: list, parent_name: str, number: str):

        if "@" in number:
            title = self.tr("Ajouter")
        else:
            title = self.tr("Ajouter attribut")

        action_name = f"[{parent_name}] {title} : {number}"

        self.undo_list.action_add_attribute(action_name=action_name,
                                            guid_parent=guid_parent,
                                            attribute_data=attribute_data)

        self.redo_clear()
        self.undo_button_manage()

    def history_del_attribute(self, guid_parent: str, attribute_data: dict, parent_name: str, number: str):

        if "@" in number:
            title = self.tr("Supprimer")
        else:
            title = self.tr("Supprimer attribut")

        action_name = f"[{parent_name}] {title} : {number}"

        self.undo_list.action_del_attribute(action_name=action_name,
                                            guid_parent=guid_parent,
                                            attribute_data=attribute_data)

        self.redo_clear()
        self.undo_button_manage()

    def history_cut_attribute(self, guid_parent_original: str, guid_parent_select: str, attribute_data: list,
                              parent_name: str, number: str):

        if "@" in number:
            title = self.tr("Couper")
        else:
            title = self.tr("Couper attribut")

        action_name = f"[{parent_name}] {title} : {number}"

        self.undo_list.action_cut_attribute(action_name=action_name,
                                            guid_parent_original=guid_parent_original,
                                            guid_parent_select=guid_parent_select,
                                            attribute_data=attribute_data)

        self.redo_clear()
        self.undo_button_manage()

    def history_modify_attribute(self, guid_parent: str, attribute_data: list, parent_name: str,
                                 value_dict: dict, attribute_type=""):

        if isinstance(guid_parent, float):
            guid_parent = int(guid_parent)

        if not isinstance(value_dict, dict):
            print("catalog_manage -- history_modify_attribute -- not isinstance(value_dict, dict)")
            return

        tooltips_list = list()
        empty_txt = self.tr("Vide")
        number = ""

        for number, value_list in value_dict.items():

            if not isinstance(number, str) or not isinstance(value_list, list):
                print("catalog_manage -- history_modify_attribute -- not isinstance(number, str)")
                return

            if len(value_list) != 2:
                print("catalog_manage -- history_modify_attribute -- len(value_list) != 2")
                return

            value_current, value_new = value_list

            if not isinstance(value_current, str) or not isinstance(value_new, str):
                print("catalog_manage -- history_modify_attribute -- not isinstance(value_current, str)")
                return

            if value_current == "":
                value_current = empty_txt

            if value_new == "":
                value_new = empty_txt

            tooltips_list.append(f"     {value_current} --> {value_new}")

        if attribute_type == "":
            title = self.tr("modification")
        else:
            title = self.tr("modification attribut")
            number = attribute_type

        action_name = f"[{parent_name}] {title} : {number}"

        tooltips = f'{action_name}\n{"\n".join(tooltips_list)}'

        self.undo_list.action_modify_attribute(action_name=action_name,
                                               tooltips=tooltips,
                                               guid_parent=guid_parent,
                                               attribute_data=attribute_data)

        self.redo_clear()
        self.undo_button_manage()

    def history_library_synchro(self):

        if len(self.library_synchro_list) == 0:
            return

        self.undo_list.action_library_synchro(action_name=self.tr("Synchronisation"),
                                              library_synchro_list=self.library_synchro_list)

        self.redo_clear()
        self.undo_button_manage()

    @staticmethod
    def a___________________undo_action___________________():
        pass

    def history_pressed(self, action_current: ActionInfo, undo=True) -> bool:

        # =========================
        # Add Item
        # =========================

        if isinstance(action_current, ActionAddEle):
            if undo:
                return self.action_add_ele(action_current=action_current, undo=undo)

            return self.action_del_ele(action_current=action_current, undo=undo)

        # =========================
        # Delete Item
        # =========================

        if isinstance(action_current, ActionDelEle):
            if undo:
                return self.action_del_ele(action_current=action_current, undo=undo)

            return self.action_add_ele(action_current=action_current, undo=undo)

        # =========================
        # Cut Item
        # =========================

        if isinstance(action_current, ActionCutEle):
            return self.action_cut_ele(action_current=action_current, undo=undo)

        # =========================
        # Move Item
        # =========================

        if isinstance(action_current, ActionMoveEle):
            return self.action_move_ele(action_current=action_current, undo=undo)

        # =========================
        # Move Material
        # =========================

        if isinstance(action_current, ActionMoveMaterial):
            return self.action_move_material(action_current=action_current, undo=undo)

        # =========================
        # Change Icon
        # =========================

        if isinstance(action_current, ActionChangeIcon):
            return self.action_change_icon(action_current=action_current, undo=undo)

        # =========================
        # Add attribute
        # =========================

        if isinstance(action_current, ActionAddAttribute):
            if undo:
                return self.action_add_attribute(action_current=action_current, undo=undo)

            return self.action_del_attribute(action_current=action_current, undo=undo)

        # =========================
        # Delete attribute
        # =========================

        if isinstance(action_current, ActionDelAttribute):
            if undo:
                return self.action_del_attribute(action_current=action_current, undo=undo)

            return self.action_add_attribute(action_current=action_current, undo=undo)

        # =========================
        # Modify attribute
        # =========================

        if isinstance(action_current, ActionModifyAttribute):
            return self.action_modify_attribute(action_current=action_current, undo=undo)

        # =========================
        # Cut attribute
        # =========================

        if isinstance(action_current, ActionCutAttribute):
            return self.action_cut_attribute(action_current=action_current, undo=undo)

        # -------------------------
        # Library synchonization
        # -------------------------

        if isinstance(action_current, ActionLibrarySynchro):
            return self.action_library_synchro(action_current=action_current, undo=undo)

        print("catalog_manage -- history_pressed -- unknow action")
        return False

    @staticmethod
    def a___________________undo_action_element___________________():
        pass

    def action_add_ele(self, action_current: ActionAddEle, undo: bool) -> bool:

        # ----------

        qs_current = self.guid_get_qs(guid=action_current.guid_current)

        if not isinstance(qs_current, (Folder, Material, Component, Link)):
            print("catalog_manage -- action_add_ele -- not isinstance(qs_current, MyQstandardItem)")
            return False

        # ----------

        row_current = qs_current.row()

        if row_current == -1:
            print("catalog_manage -- action_add_ele -- row_current == -1")
            return False

        # ----------

        qs_parent = qs_current.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("catalog_manage -- action_add_ele -- not isinstance(qs_parent, QStandardItem)")
            return False

        # ----------

        if not self.material_delete(qs=qs_current):
            print("catalog_manage -- action_add_ele -- not self.material_delete(qs=qs_current)")
            return False

        # ----------

        qs_list = qs_parent.takeRow(row_current)

        if not isinstance(qs_list, list):
            print("catalog_manage -- action_add_ele -- not isinstance(qs_list, list)")
            return False

        if len(qs_list) != col_cat_count:
            print("catalog_manage -- action_add_ele -- len(liste_ele) != column_count")
            return False

        action_current.guid_parent = qs_parent.data(user_guid)
        action_current.row_current = row_current
        action_current.qs_list = qs_list

        # ----------

        last_item = qs_parent.rowCount()

        if isinstance(qs_parent, MyQstandardItem):
            attributes_list = qs_parent.get_attribute_numbers_list()
            first_item = len(attributes_list)
        else:
            first_item = 0

        if last_item == first_item:

            self.hierarchy.select_list(selected_list=[qs_parent], expand=True)

        else:

            if row_current < first_item:
                row_current = first_item

            elif row_current >= last_item:

                if last_item > first_item:
                    row_current = last_item - 1
                else:
                    row_current = first_item

            qs_selection = qs_parent.child(row_current, col_cat_value)

            if not isinstance(qs_selection, MyQstandardItem):
                print("catalog -- action_add_ele -- not isinstance(qs_selection, MyQstandardItem)")
            else:
                self.hierarchy.select_list(selected_list=[qs_selection], expand=True)

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    # ==========================================================================================

    def action_del_ele(self, action_current: ActionDelEle, undo: bool) -> bool:

        qs_parent = self.guid_get_qs(guid=action_current.guid_parent)

        if not isinstance(qs_parent, QStandardItem):
            print("catalog_manage -- action_del_ele -- not isinstance(qs_parent, QStandardItem)")
            return False

        # ----------

        qs_list = action_current.qs_list

        if not isinstance(qs_list, list):
            print("catalog_manage -- action_del_ele -- not isinstance(qs_list, list)")
            return False

        if len(qs_list) != col_cat_count:
            print("catalog_manage -- action_del_ele -- len(qs_list) != column_count")
            return False

        # ----------

        row_current = action_current.row_current

        if not isinstance(row_current, int):
            print("catalog_manage -- action_del_ele -- not isinstance(row_current, int)")
            return False

        if row_current == -1:
            print("catalog_manage -- action_del_ele -- row_current == -1")
            return False

        # ----------

        qs_parent.insertRow(row_current, qs_list)

        # ----------

        qs_selection = qs_list[col_cat_value]

        if not isinstance(qs_selection, MyQstandardItem):
            print("catalog_manage -- action_del_ele -- not isinstance(qs_selection, MyQstandardItem)")
            return False

        self.material_add(qs_selection)

        self.hierarchy.select_list(selected_list=[qs_selection], expand=True)

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    # ==========================================================================================

    def action_move_ele(self, action_current: ActionMoveEle, undo: bool) -> bool:

        qs_current = self.guid_get_qs(guid=action_current.guid_current)

        if not isinstance(qs_current, MyQstandardItem):
            print("catalog_manage -- action_move_ele -- not isinstance(qs_actuel, QStandardItem)")
            return False

        # ----------

        row_current = qs_current.row()

        if not isinstance(row_current, int):
            print("catalog_manage -- action_move_ele -- not isinstance(row_current, int)")
            return False

        # ----------

        qs_parent = qs_current.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("catalog_manage -- action_move_ele -- not isinstance(qs_parent, QStandardItem)")
            return False

        # ----------

        row_new = action_current.row_new

        if row_new == -1 or row_new == row_current:
            print("catalog_manage -- action_move_ele -- row_new == -1")
            return False

        if row_new == row_current:
            print("catalog_manage -- action_move_ele -- row_new == row_current")
            return False

        # ----------

        qs_list = qs_parent.takeRow(row_current)

        if not isinstance(qs_list, list):
            print("catalog_manage -- action_move_ele -- not isinstance(liste_ele, list)")
            return False

        if len(qs_list) != col_cat_count:
            print("catalog_manage -- action_move_ele -- len(liste_ele) != column_count")
            return False

        qs_parent.insertRow(row_new, qs_list)

        # ----------

        action_current.row_new = row_current

        # ----------

        qs_current = qs_list[col_cat_value]

        if not isinstance(qs_current, MyQstandardItem):
            print("catalog_manage -- action_move_ele -- not isinstance(qs_actuel, MyQstandardItem)")
            return False

        self.hierarchy.select_list(selected_list=[qs_current], expand=True)

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    # ==========================================================================================

    def action_cut_ele(self, action_current: ActionCutEle, undo: bool) -> bool:

        qs_current = self.guid_get_qs(guid=action_current.guid_current)

        if not isinstance(qs_current, (Folder, Material, Component, Link)):
            print("catalog_manage -- action_cut_ele -- not isinstance(qs_current, MyQstandardItem)")
            return False

        qs_parent_current = qs_current.parent()

        if not isinstance(qs_parent_current, QStandardItem):
            print("catalog_manage -- action_cut_ele -- not isinstance(qs_parent_current, QStandardItem)")
            return False

        row_current = qs_current.row()

        if not isinstance(row_current, int):
            print("catalog_manage -- action_cut_ele -- not isinstance(row_current, int)")
            return False

        if row_current == -1:
            print("catalog_manage -- action_cut_ele -- row_current == -1")
            return False

        # ----------

        qs_parent_new = self.guid_get_qs(guid=action_current.guid_parent_new)

        if not isinstance(qs_parent_new, QStandardItem):
            print("catalog_manage -- action_cut_ele -- not isinstance(qs_parent_new, QStandardItem)")
            return False

        # ----------

        qs_list = qs_parent_current.takeRow(row_current)

        if not isinstance(qs_list, list):
            print("catalog -- action_cut_ele -- not isinstance(liste_ele, list)")
            return False

        if len(qs_list) != col_cat_count:
            print("catalog -- action_cut_ele -- len(liste_ele) != column_count")
            return False

        # ----------

        row_new = action_current.row_new

        if row_new == -1:
            print("catalog_manage -- action_cut_ele -- row_new == -1")
            return False

        qs_parent_new.insertRow(row_new, qs_list)

        action_current.guid_parent_new = qs_parent_current.data(user_guid)
        action_current.row_new = row_current

        # ----------

        qs_selection = qs_list[col_cat_value]

        if not isinstance(qs_selection, MyQstandardItem):
            print("catalog -- action_cut_ele -- not isinstance(qs_selection, MyQstandardItem)")
            return False

        self.hierarchy.select_list(selected_list=[qs_selection], expand=True)

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    def action_change_icon(self, action_current: ActionChangeIcon, undo: bool) -> bool:

        qs_current = self.guid_get_qs(guid=action_current.guid_current)

        if not isinstance(qs_current, Folder):
            print("catalog_manage -- action_change_icon -- not isinstance(qs_actuel, Folder)")
            return False

        # ----------

        icon_new = action_current.icon_new

        if not isinstance(icon_new, QIcon):
            print("catalog_manage -- action_change_icon -- not isinstance(icon_new, QIcon)")
            return False

        # ----------

        icon_current = qs_current.icon()

        if not isinstance(icon_current, QIcon):
            print("catalog_manage -- action_change_icon -- not isinstance(icon_current, QIcon)")
            return False

        # ----------

        qs_current.setIcon(icon_new)

        action_current.icon_new = icon_current

        # ----------

        qs_select = self.hierarchy.get_current_qs()

        if qs_select == qs_current:
            self.hierarchy.select_list(selected_list=[qs_select])

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    def action_move_material(self, action_current: ActionMoveMaterial, undo: bool) -> bool:

        guid_parent = action_current.guid_parent

        if not isinstance(guid_parent, str):
            print("catalog_manage -- undo_move_material_action -- not isinstance(guid_parent, str)")
            return False

        # ----------

        qs_parent = self.guid_get_qs(guid_parent)

        if not isinstance(qs_parent, Folder):
            print("catalog_manage -- undo_move_material_action -- not isinstance(qs_parent, Folder)")
            return False

        # ----------

        guid_material = action_current.guid_material

        if not isinstance(guid_material, str):
            print("catalog_manage -- undo_move_material_action -- not isinstance(guid_material, str)")
            return False

        # ----------

        if undo:

            qs_material = self.guid_get_qs(guid_material, parent=guid_parent)

            if not isinstance(qs_material, Material):
                print("catalog_manage -- undo_move_material_action -- not isinstance(qs_material, Material)")
                return False

            # ----------

            qs_new_folder = qs_material.parent()

            if not isinstance(qs_new_folder, Folder):
                print("catalog_manage -- undo_move_material_action -- not isinstance(qs_new_folder, Folder)")
                return False

            # ----------

            row_new_folder = qs_new_folder.row()

            row_new_material = row_new_folder + 1

            # ----------

            row_count = qs_new_folder.rowCount()

            for row_index in reversed(range(row_count)):

                qs_material = qs_new_folder.child(row_index, col_cat_value)

                if not isinstance(qs_material, Material):
                    continue

                qs_list = qs_new_folder.takeRow(row_index)

                if not isinstance(qs_list, list):
                    print("catalog_manage -- undo_move_material_action -- not isinstance(qs_list, list)")
                    return False

                if len(qs_list) != col_cat_count:
                    print("catalog_manage -- undo_move_material_action -- len(qs_list) != col_cat_count")
                    return False

                qs_parent.insertRow(row_new_material, qs_list)

            qs_list = qs_parent.takeRow(row_new_folder)

            if not isinstance(qs_list, list):
                print("catalog_manage -- undo_move_material_action -- not isinstance(qs_list, list)")
                return False

            if len(qs_list) != col_cat_count:
                print("catalog_manage -- undo_move_material_action -- len(qs_list) != col_cat_count")
                return False

            # ----------

            self.hierarchy.select_list(selected_list=[qs_parent])

            # ----------

            return self.undo_action_end(action_id=action_current.action_id)

        # ---------------
        # REDO
        # ---------------

        qs_material = self.guid_get_qs(guid_material, parent=guid_parent)

        if not isinstance(qs_material, Material):
            print("catalog_manage -- undo_move_material_action -- not isinstance(qs_material, Material)")
            return False

        # ---------------

        guid_new_folder = action_current.guid_new_folder

        if not isinstance(guid_new_folder, str):
            print("catalog_manage -- undo_move_material_action -- not isinstance(guid_new_folder, str)")
            return False

        # ---------------

        if not self.material_to_new_folder_action(qs_material_list=[qs_material], guid_new_folder=guid_new_folder):
            print("catalog_manage -- undo_move_material_action -- "
                  "not self.material_to_new_folder_action(qs_material_list=qs_material_list)")
            return False

        # ----------

        return self.redo_action_end(action_id=action_current.action_id)

    @staticmethod
    def a___________________undo_action_attribute___________________():
        pass

    def action_add_attribute(self, action_current: ActionAddAttribute, undo: bool) -> bool:

        qs_parent = self.guid_get_qs(guid=action_current.guid_parent)

        if not isinstance(qs_parent, QStandardItem):
            print("catalog_manage -- action_add_attribute -- not isinstance(qs_parent, QStandardItem)")
            return False

        attribute_data = action_current.attribute_data

        if not isinstance(attribute_data, list):
            print("catalog_manage -- action_add_attribute -- not isinstance(attribute_data, list)")
            return False

        if len(attribute_data) == 0:
            print("catalog_manage -- action_add_attribute -- len(attribute_data) == 0")
            return False

        for data in reversed(attribute_data):

            if not isinstance(data, AttributeData):
                print("catalog_manage -- action_add_attribute -- not isinstance(data, AttributeData)")
                return False

            # ----------

            guid_code = data.guid_current

            if not isinstance(guid_code, str):
                print("catalog_manage -- action_add_attribute -- not isinstance(guid_code, str)")
                return False

            # ----------

            qs_current = self.guid_get_qs(guid=guid_code, parent=qs_parent.index())

            if not isinstance(qs_current, Attribute):
                print("catalog_manage -- action_add_attribute -- not isinstance(qs_current, Attribute)")
                return False

            # ----------

            row_current = qs_current.row()

            if row_current == -1:
                print("catalog_manage -- action_add_attribute -- row_current == -1")
                return False

            # ----------

            qs_list = qs_parent.takeRow(row_current)

            if not isinstance(qs_list, list):
                print("catalog_manage -- action_add_attribute -- not isinstance(qs_list, list)")
                return False

            if len(qs_list) != col_cat_count:
                print("catalog_manage -- action_add_attribute -- len(liste_ele) != column_count")
                return False

            data.row_current = row_current
            data.qs_list = qs_list

        # ----------

        if isinstance(qs_parent, (Material, Component)):
            self.hierarchy.select_list(selected_list=[qs_parent], expand=True)

        else:

            print("catalog_manage -- action_add_attribute -- isinstance(qs_parent, (Material, Component))")
            return False

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    def action_del_attribute(self, action_current: ActionDelAttribute, undo: bool) -> bool:

        qs_parent = self.guid_get_qs(guid=action_current.guid_parent)

        if not isinstance(qs_parent, QStandardItem):
            print("catalog_manage -- action_del_attribute -- not isinstance(qs_parent, QStandardItem)")
            return False

        attribute_data = action_current.attribute_data

        if not isinstance(attribute_data, list):
            print("catalog_manage -- action_del_attribute -- not isinstance(attribute_data, list)")
            return False

        if len(attribute_data) == 0:
            print("catalog_manage -- action_del_attribute -- len(attribute_data) == 0")
            return False

        try:

            attribute_data.sort(key=lambda x: x.row_current)

        except Exception as error:
            print(f"catalog_manage -- action_del_attribute -- error : {error}")
            return False

        for data in attribute_data:

            if not isinstance(data, AttributeData):
                print("catalog_manage -- action_del_attribute -- not isinstance(data, AttributeData)")
                return False

            row_current: int = data.row_current

            if not isinstance(row_current, int):
                print("catalog_manage -- action_del_attribute -- not isinstance(row_current, int)")
                return False

            qs_list: list = data.qs_list

            if not isinstance(qs_list, list):
                print("catalog_manage -- undo_del_attribute_action -- not isinstance(qs_list, list)")
                return False

            if len(qs_list) != col_cat_count:
                print("catalog_manage -- undo_del_attribute_action -- len(qs_list) != column_count")
                return False

            qs_parent.insertRow(row_current, qs_list)

        # ----------

        self.hierarchy.select_list(selected_list=[qs_parent])

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    def action_cut_attribute(self, action_current: ActionCutAttribute, undo: bool) -> bool:

        qs_parent_original = self.guid_get_qs(guid=action_current.guid_parent_original)

        qs_selection = None

        if not isinstance(qs_parent_original, (Folder, Material, Component)):
            print("catalog_manage -- action_cut_attribute -- not isinstance(qs_parent_original, MyQstandardItem)")
            return False

        # ----------

        qs_parent_select = self.guid_get_qs(guid=action_current.guid_parent_select)

        if not isinstance(qs_parent_select, (Folder, Material, Component)):
            print("catalog_manage -- action_cut_attribute -- not isinstance(qs_parent_select, MyQstandardItem)")
            return False

        # ----------

        attribute_data = action_current.attribute_data

        if not isinstance(attribute_data, list):
            print("catalog_manage -- action_cut_attribute -- not isinstance(attribute_data, list)")
            return False

        if len(attribute_data) == 0:
            print("catalog_manage -- action_cut_attribute -- len(attribute_data) == 0")
            return False

        if undo:
            attribute_data = list(attribute_data)
            attribute_data.reverse()
        # ----------

        for data in attribute_data:

            if not isinstance(data, AttributeCutData):
                print("catalog_manage -- action_cut_attribute -- not isinstance(data, AttributeCutData)")
                return False

            # ----------

            number_current = data.number_current

            if not isinstance(number_current, str):
                print("catalog_manage -- action_cut_attribute -- not isinstance(number_current, str)")
                return False

            # ----------

            attribute_delete = data.attribute_delete

            # ----------
            # UNDO --> selection -> Original
            # ----------

            if undo:

                # ----------

                row_original = data.row_original

                if row_original == -1:
                    print("catalog_manage -- action_cut_attribute -- row_original == -1")
                    return False

                # ----------

                row_select = qs_parent_select.get_row_attribute_by_number(number=number_current)

                if row_select == -1:
                    print("catalog_manage -- action_cut_attribute -- row_select == -1:")
                    return False

                data.row_select = row_select

                # ----------

                qs_list_original = data.qs_list_original

                if not isinstance(qs_list_original, list):
                    print("catalog_manage -- action_cut_attribute -- not isinstance(qs_list_original, list)")
                    return False

                if len(qs_list_original) != col_cat_count:
                    print("catalog_manage -- action_cut_attribute --len(qs_list_original) != col_cat_count")
                    return False

                # ---------- attribute doesn't exist in the selection -> move only

                if attribute_delete:

                    qs_list_select = qs_parent_select.takeRow(row_select)

                    # ----------

                    if not isinstance(qs_list_select, list):
                        print("catalog_manage -- action_cut_attribute -- not isinstance(qs_list_select, list)")
                        return False

                    if len(qs_list_select) != col_cat_count:
                        print("catalog_manage -- action_cut_attribute --len(qs_list_select) != col_cat_count")
                        return False

                    # ----------

                    data.qs_list_select = qs_list_select

                    data.row_original = qs_parent_original.get_attribute_insertion_index(number=number_current)

                    qs_parent_original.insertRow(data.row_original, qs_list_original)

                    qs_selection = qs_parent_original
                    # ----------

                    continue

                # ---------- attribute exists in the selection -> restore values

                qs_value_select = qs_parent_select.child(row_select, col_cat_value)

                if not isinstance(qs_value_select, Attribute):
                    print("catalog_manage -- action_cut_attribute -- not isinstance(qs_value_select, Attribute)")
                    return False

                # ----------

                qs_value_index_select = qs_parent_select.child(row_select, col_cat_index)

                if not isinstance(qs_value_index_select, Info):
                    print("catalog_manage -- action_cut_attribute -- not isinstance(qs_value_index_select, Info)")
                    return False

                # ----------

                value_select = data.value_select

                if not isinstance(value_select, str):
                    print("catalog_manage -- action_cut_attribute -- not isinstance(value_select, str)")
                    return False

                # ----------

                value_index_select = data.value_index_select

                if not isinstance(value_index_select, str):
                    print("catalog_manage -- action_cut_attribute -- not isinstance(value_index_select, str)")
                    return False

                # ----------

                guid_select = data.guid_select

                if not isinstance(guid_select, str):
                    print("catalog_manage -- action_cut_attribute -- not isinstance(guid_select, str)")
                    return False

                # ----------

                qs_value_select.setData(guid_select, user_guid)
                qs_value_select.setText(value_select)
                qs_value_index_select.setText(value_index_select)

                # ----------

                data.row_original = qs_parent_original.get_attribute_insertion_index(number=number_current)

                qs_parent_original.insertRow(data.row_original, qs_list_original)

                qs_selection = qs_parent_original
                # ----------

                continue

            # ----------
            # Redo --> Original -> selection
            # ----------

            row_original = qs_parent_original.get_row_attribute_by_number(number=number_current)

            if row_original == -1:
                print("catalog_manage -- action_cut_attribute -- row_original == -1")
                return False

            # ---------- attribute doesn't exist in the selection -> move only

            if attribute_delete:

                qs_list_original = qs_parent_original.takeRow(row_original)

                # ----------

                if not isinstance(qs_list_original, list):
                    print("catalog_manage -- action_cut_attribute -- not isinstance(qs_list_original, list)")
                    return False

                if len(qs_list_original) != col_cat_count:
                    print("catalog_manage -- action_cut_attribute --len(qs_list_original) != col_cat_count")
                    return False

                # ----------

                qs_list_select = data.qs_list_select

                # ----------

                if not isinstance(qs_list_select, list):
                    print("catalog_manage -- action_cut_attribute -- not isinstance(qs_list_select, list)")
                    return False

                if len(qs_list_select) != col_cat_count:
                    print("catalog_manage -- action_cut_attribute --len(qs_list_select) != col_cat_count")
                    return False

                # ----------

                data.row_select = qs_parent_select.get_attribute_insertion_index(number=number_current)

                # ----------

                qs_parent_select.insertRow(data.row_select, qs_list_select)

                qs_selection = qs_parent_select
                # ----------

                continue

            # ---------- attribute exists in the selection -> restore values

            row_select = qs_parent_select.get_row_attribute_by_number(number=number_current)

            if row_select == -1:
                print("catalog_manage -- action_cut_attribute -- row_select == -1:")
                return False

            data.row_select = row_select

            # ----------

            qs_value_select = qs_parent_select.child(row_select, col_cat_value)

            if not isinstance(qs_value_select, Attribute):
                print("catalog_manage -- action_cut_attribute -- not isinstance(qs_value_select, Attribute)")
                return False

            # ----------

            qs_value_index_select = qs_parent_select.child(row_select, col_cat_index)

            if not isinstance(qs_value_index_select, Info):
                print("catalog_manage -- action_cut_attribute -- not isinstance(qs_value_index_select, Info)")
                return False

            # ----------

            value_original = data.value_original

            if not isinstance(value_original, str):
                print("catalog_manage -- action_cut_attribute -- not isinstance(value_original, str)")
                return False

            # ----------

            value_index_original = data.value_index_original

            if not isinstance(value_index_original, str):
                print("catalog_manage -- action_cut_attribute -- not isinstance(value_index_original, str)")
                return False

            # ----------

            guid_original = data.guid_original

            if not isinstance(guid_original, str):
                print("catalog_manage -- action_cut_attribute -- not isinstance(guid_original, str)")
                return False

            # ----------

            qs_value_select.setText(value_original)
            qs_value_select.setData(guid_original, user_guid)
            qs_value_index_select.setText(value_index_original)

            # ----------

            qs_list_original = qs_parent_original.takeRow(row_original)

            # ----------

            if not isinstance(qs_list_original, list):
                print("catalog_manage -- action_cut_attribute -- not isinstance(qs_list_original, list)")
                return False

            if len(qs_list_original) != col_cat_count:
                print("catalog_manage -- action_cut_attribute --len(qs_list_original) != col_cat_count")
                return False

            # ----------

            qs_selection = qs_parent_select
            continue

        # ----------

        if isinstance(qs_selection, MyQstandardItem):
            self.hierarchy.select_list(selected_list=[qs_selection], scrollto=True, expand=True)

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    def action_modify_attribute(self, action_current: ActionModifyAttribute, undo: bool) -> bool:

        qs_parent = self.guid_get_qs(guid=action_current.guid_parent)

        if not isinstance(qs_parent, MyQstandardItem):
            print("catalog_manage -- action_modify_attribute -- not isinstance(qs_parent, MyQstandardItem)")
            return False

        attribute_data = action_current.attribute_data

        if not isinstance(attribute_data, list):
            print("catalog_manage -- action_modify_attribute -- not isinstance(attribute_data, list)")
            return False

        if len(attribute_data) == 0:
            print("catalog_manage -- action_modify_attribute -- len(attribute_data) == 0")
            return False

        # ----------

        for data in attribute_data:

            if not isinstance(data, AttributeModifyData):
                print("catalog_manage -- action_modify_attribute -- not isinstance(data, ActionModifyAttribute)")
                return False

            # ----------

            number_current = data.number_current

            if not isinstance(number_current, str):
                print("catalog_manage -- action_modify_attribute -- not isinstance(number_current, str)")
                return False

            # ----------

            value_new = data.value_new

            if not isinstance(value_new, str):
                print("catalog_manage -- action_modify_attribute -- not isinstance(value_new, str)")
                return False

            # ----------

            value_index_new = data.value_index_new

            if not isinstance(value_index_new, str):
                print("catalog_manage -- action_modify_attribute -- not isinstance(value_index_new, str)")
                return False

            # ----------

            if number_current == attribute_default_base:

                value_current = qs_parent.text()

                if not isinstance(value_current, str):
                    print("catalog_manage -- action_modify_attribute -- not isinstance(value_current, str)")
                    return False

                # ----------

                if value_new != value_current:

                    qs_parent.setText(value_new)
                    data.value_new = value_current

                    # ----------

                    if isinstance(qs_parent, Material):
                        self.material_code_renamed(code_before=value_current,
                                                   code_after=value_new)

                    # ----------

                    self.hierarchy.select_list(selected_list=[qs_parent])

                # ----------

                if undo:
                    return self.undo_action_end(action_id=action_current.action_id)

                return self.redo_action_end(action_id=action_current.action_id)

                # ========================================================================

            qs_list = qs_parent.get_attribute_line_by_number(number=number_current)

            if not isinstance(qs_list, list):
                print("catalog_manage -- action_modify_attribute -- not isinstance(qs_list, list)")
                return False

            if len(qs_list) != col_cat_count:
                print("catalog_manage -- action_modify_attribute -- len(qs_list) != col_cat_count")
                return False

            # ----------

            qs_value = qs_list[col_cat_value]

            if not isinstance(qs_value, Attribute):
                print("catalog_manage -- action_modify_attribute -- not isinstance(qs_value, Attribute)")
                return False

            value_current = qs_value.text()

            if not isinstance(value_current, str):
                print("catalog_manage -- action_modify_attribute -- not isinstance(value_current, str)")
                return False

            # ----------

            qs_index = qs_list[col_cat_index]

            if not isinstance(qs_index, Info):
                print("catalog_manage -- action_modify_attribute -- not isinstance(qs_index, Info)")
                return False

            value_index_current = qs_index.text()

            if not isinstance(value_index_current, str):
                print("catalog_manage -- action_modify_attribute -- not isinstance(value_index_current, str)")
                return False

            # ----------

            if value_new == value_current and value_index_new == value_index_current:

                if undo:
                    return self.undo_action_end(action_id=action_current.action_id)

                return self.redo_action_end(action_id=action_current.action_id)

            # ----------

            if number_current == "207" and value_new != value_current:

                guid_desc = data.guid_desc

                qs_desc = self.guid_get_qs(guid=guid_desc, column=col_cat_desc)

                if not isinstance(qs_desc, Info):
                    print("catalog_manage -- action_modify_attribute -- not isinstance(qs_desc, Info)")
                    return False

                qs_desc.setText(value_new)

            # ----------

            if value_new != value_current:
                qs_value.setText(value_new)
                data.value_new = value_current

            if value_index_new != value_index_current:
                qs_index.setText(value_index_new)
                data.value_index_new = value_index_current

            # ----------

        self.hierarchy.select_list(selected_list=[qs_parent])

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    def action_library_synchro(self, action_current: ActionLibrarySynchro, undo: bool) -> bool:

        library_synchro_list = action_current.library_synchro_list

        if not isinstance(library_synchro_list, list):
            print("catalog_manage -- undo_library_synchro -- not isinstance(library_synchro_list, list)")
            return False

        for data in reversed(library_synchro_list):

            if not isinstance(data, LibraryData):
                print("catalog_manage -- undo_library_synchro -- not isinstance(datas, LibraryData)")
                return False

            # ----------

            guid_parent = data.guid_parent

            if not isinstance(guid_parent, str):
                print("catalog_manage -- undo_library_synchro -- not isinstance(guid_parent, str)")
                return False

            # ----------

            qs_parent = self.guid_get_qs(guid=guid_parent)

            if not isinstance(qs_parent, (Folder, Material, Component)):
                print("catalog_manage -- undo_library_synchro -- not isinstance(qs_parent, Folder)")
                return False

            # ----------

            guid_current = data.guid_current

            if not isinstance(guid_current, str):
                print("catalog_manage -- undo_library_synchro -- not isinstance(guid_current, str)")
                return False

            # ----------

            qs_current = self.guid_get_qs(guid=guid_current, parent=qs_parent.index())

            if not isinstance(qs_current, Attribute):
                print("catalog_manage -- undo_library_synchro -- not isinstance(qs_current, Attribute)")
                return False

            # ----------

            row_current = qs_current.row()

            if row_current == -1:
                print("catalog_manage -- undo_library_synchro -- row_current == -1")
                return False

            if data.is_creation:

                # ------------
                # Delete Attribute --> UNDO
                # ------------

                if undo:

                    qs_list = qs_parent.takeRow(row_current)

                    if not isinstance(qs_list, list):
                        print("catalog_manage -- undo_library_synchro -- not isinstance(qs_list, list)")
                        return False

                    if len(qs_list) != col_cat_count:
                        print("catalog_manage -- undo_library_synchro -- len(qs_list) != col_cat_count")
                        return False

                    # ----------

                    data.row_current = row_current
                    data.qs_list = qs_list

                    continue

                # ------------
                # Add Attribute --> RDO
                # ------------

                qs_list = data.qs_list

                if not isinstance(qs_list, list):
                    print("catalog_manage -- redo_library_synchro -- not isinstance(qs_list, list)")
                    return False

                if len(qs_list) != col_cat_count:
                    print("catalog_manage -- redo_library_synchro -- len(qs_list) != col_cat_count")
                    return False

                row_current = data.row_current

                if row_current == -1:
                    print("catalog_manage -- redo_library_synchro -- row_current == -1")
                    return False

                qs_parent.insertRow(row_current, qs_list)

                # ----------

                data.row_current = -1
                data.qs_list = list()

                continue

            # ------------
            # Update
            # ------------

            value_current = qs_current.text()

            if not isinstance(value_current, str):
                print("catalog_manage -- undo_library_synchro -- not isinstance(value_current, str)")
                return False

            # ------------ update data

            value_new = data.value_new

            if not isinstance(value_new, str):
                print("catalog_manage -- undo_library_synchro -- not isinstance(value_new, str)")
                return False

            qs_current.setText(value_new)

            # ------------ copy new data

            data.value_new = value_current

            # ------------ Description (207)

            if isinstance(data.guid_desc, str):

                qs_desc = self.guid_get_qs(guid=data.guid_desc, column=col_cat_desc)

                if not isinstance(qs_desc, Info):
                    print("catalog_manage -- undo_library_synchro -- not isinstance(qs_desc, Info)")
                    return False

                qs_desc.setText(value_new)

            # ------------ check if value_index exists

            value_index_new = data.value_index_new

            if not isinstance(value_index_new, str):
                continue

            qs_value_index = qs_parent.child(row_current, col_cat_index)

            if not isinstance(qs_value_index, Info):
                print("catalog_manage -- undo_library_synchro -- not isinstance(qs_value_index, Info))")
                return False

            # ------------

            value_index_current = qs_value_index.text()

            if not isinstance(value_index_current, str):
                print("catalog_manage -- undo_library_synchro -- not isinstance(value_index_current, str)")
                return False

            # ------------

            value_index_new = data.value_index_new

            if not isinstance(value_index_new, str):
                print("catalog_manage -- undo_library_synchro -- not isinstance(value_index_new, str)")
                return False

            # ------------

            qs_value_index.setText(value_index_new)

            data.value_index_new = value_index_current

            # ------------

        qs_selection = self.hierarchy.get_current_qm_filter()

        if isinstance(qs_selection, QModelIndex):
            self.hierarchy.select_list(selected_list=[qs_selection])

        # ----------

        if undo:
            return self.undo_action_end(action_id=action_current.action_id)

        return self.redo_action_end(action_id=action_current.action_id)

    @staticmethod
    def a___________________undo_action_end___________________():
        pass

    def undo_action_end(self, action_id: int) -> bool:

        action = self.undo_list.action_dict.get(action_id, None)

        if action is None:
            print("catalog_manage -- undo_action_end -- action is None")
            return False

        self.redo_list.action_dict[action_id] = action

        result = self.undo_list.supprimer_action(action_id)

        self.undo_button_manage()
        self.redo_button_manage()

        return result

    def undo_button_manage(self):
        self.ui.undo_bt.setEnabled(len(self.undo_list.action_dict) != 0)
        self.ui.undo_list_bt.setEnabled(len(self.undo_list.action_dict) != 0)

    @staticmethod
    def a___________________redo_action_end___________________():
        pass

    def redo_action_end(self, action_id: int) -> bool:

        action = self.redo_list.action_dict.get(action_id, None)

        if action is None:
            print("catalog_manage -- redo_action_end -- action is None")
            return False

        self.undo_list.action_dict[action_id] = action

        result = self.redo_list.supprimer_action(action_id)

        self.undo_button_manage()
        self.redo_button_manage()

        return result

    def redo_clear(self):

        self.redo_list.action_clear()
        self.redo_button_manage()

    def redo_button_manage(self):

        self.ui.redo_bt.setEnabled(len(self.redo_list.action_dict) != 0)
        self.ui.redo_list_bt.setEnabled(len(self.redo_list.action_dict) != 0)

    @staticmethod
    def a___________________library_update_description___________________():
        pass

    def library_synchro(self, code: str, number: str, value: str, index_value: str, item_type: str,
                        creation: bool) -> int:

        search_code = self.hierarchy.cat_model.findItems(code, Qt.MatchExactly | Qt.MatchRecursive, col_cat_value)

        synchro_count = 0

        if len(search_code) == 0:
            return synchro_count

        for qs in search_code:

            qs: MyQstandardItem

            ele_type_curent = qs.data(user_data_type)

            if item_type != ele_type_curent:
                continue

            results = qs.get_attribute_line_by_number(number=number)

            if not isinstance(results, list):
                continue

            if len(results) < col_cat_desc:

                if not creation:
                    continue

                insertion_index = qs.get_attribute_insertion_index(number=number)

                if not isinstance(insertion_index, int):
                    print("catalog_manage -- library_synchro -- not isinstance(insertion_index, int)")
                    continue

                if insertion_index < 0:
                    print("catalog_manage -- library_synchro -- insertion_index < 0")
                    continue

                if index_value != "-1":
                    qs_list = self.allplan.creation.attribute_line(value=index_value, number_str=number)
                else:
                    qs_list = self.allplan.creation.attribute_line(value=value, number_str=number)

                if not isinstance(qs_list, list):
                    print("catalog_manage -- library_synchro -- not isinstance(qs_list, list)")
                    continue

                qs.insertRow(insertion_index, qs_list)

                qs_value = qs_list[col_cat_value]

                if not isinstance(qs_value, Attribute):
                    print("catalog_manage -- library_synchro -- not isinstance(qs_value, Attribute)")
                    continue

                self.library_synchro_list.append(LibraryData(is_creation=True,
                                                             guid_parent=qs.data(user_guid),
                                                             guid_current=qs_value.data(user_guid)))

                synchro_count += 1

                continue

            # ------------------------------

            qs_attribute_value = results[col_cat_value]

            if not isinstance(qs_attribute_value, Attribute):
                print("catalog_manage -- library_synchro -- not isinstance(qs_attribute_value, Attribute)")
                continue

            attribute_value = qs_attribute_value.text()

            if not isinstance(attribute_value, str):
                print("catalog_manage -- library_synchro -- not isinstance(attribute_value, str)")
                continue

            if attribute_value == value:
                continue

            # ------------------------------

            qs_index = results[col_cat_index]

            if not isinstance(qs_index, Info):
                print("catalog_manage -- library_synchro -- not isinstance(qs_index_value, Info)")
                continue

            index_value_before = qs_index.text()

            if not isinstance(index_value_before, str):
                print("catalog_manage -- library_synchro -- not isinstance(index_value_before, str)")
                continue

            # ------------------------------

            if number == "207":

                qs_parent = qs.parent()

                if not isinstance(qs_parent, MyQstandardItem):
                    print("catalog_manage -- library_synchro -- not isinstance(qs_parent, MyQstandardItem)")
                    continue

                qs_desc = qs_parent.child(qs.row(), col_cat_desc)

                if not isinstance(qs_desc, Info):
                    print("catalog_manage -- library_synchro -- not isinstance(qs_desc, Info)")
                    continue

                qs_desc.setText(value)
                guid_desc = qs_desc.data(user_guid)

                index_value_before = "-1"

            else:
                guid_desc = None

                # ------------------------------

            if index_value_before != index_value:
                qs_index.setText(index_value)

            qs_attribute_value.setText(value)

            synchro_count += 1

            self.library_synchro_list.append(LibraryData(is_creation=False,
                                                         guid_parent=qs.data(user_guid),
                                                         guid_current=qs_attribute_value.data(user_guid),
                                                         value_new=attribute_value,
                                                         value_index_new=index_value_before,
                                                         guid_desc=guid_desc))

        return synchro_count

    def library_synchro_end(self):
        self.catalog_modif_manage()

        selection_list = self.hierarchy.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return

        self.hierarchy.select_list(selected_list=selection_list, scrollto=False)

    @staticmethod
    def a___________________backup_restore___________________():
        pass

    def backup_restore_action(self, backup_path: str, backup_index: str) -> str:

        if not os.path.exists(backup_path):
            print("catalog_manage -- backup_restore_action -- not os.path.exists(backup_path")
            return f"{backup_path} don't exist"

        backup_time = os.path.getmtime(backup_path)

        # ------------------------
        # Swap catalog
        # ------------------------

        try:

            new_path = f"{backup_path}.bak"

            if os.path.exists(new_path):
                os.remove(new_path)

            os.rename(self.catalog_path, new_path)

            os.rename(backup_path, self.catalog_path)

            os.rename(new_path, backup_path)

        except Exception as error:
            return f"error swap catalog: {error}"

        # ------------------------
        # Swap display
        # ------------------------

        if not os.path.exists(self.catalog_settings_folder):
            print(f"catalog_manage -- backup_restore_action -- not os.path.exists(self.catalog_settings_folder)")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        if not os.path.exists(self.catalog_setting_display_file):
            print(f"catalog_manage -- backup_restore_action -- not os.path.exists(self.catalog_setting_display_file)")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        if backup_index == "00":
            backup_display = f"{self.catalog_settings_folder}backup\\{self.catalog_name}_display.xml"
        else:
            backup_display = f"{self.catalog_settings_folder}backup\\{self.catalog_name}_display - {backup_index}.xml"

        if not os.path.exists(backup_display):
            print(f"catalog_manage -- backup_restore_action -- not os.path.exists(backup_display)")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        try:

            backup_display_time = os.path.getmtime(backup_display)

            datetime1 = datetime.fromtimestamp(backup_time)
            datetime2 = datetime.fromtimestamp(backup_display_time)

            time_difference = abs(datetime1 - datetime2).total_seconds()

            if time_difference > 10:
                print(f"catalog_manage -- backup_restore_action -- time_difference > 10")
                self.catalog_load_start(catalog_path=self.catalog_path)
                return ""

        except Exception as error:
            print(f"catalog_manage -- backup_restore_action -- error time difference : {error}")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        try:

            new_path = f"{backup_display}.bak"

            if os.path.exists(new_path):
                os.remove(new_path)

            os.rename(self.catalog_setting_display_file, new_path)

            os.rename(backup_display, self.catalog_setting_display_file)

            os.rename(new_path, backup_display)

            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        except Exception as error:
            print(f"catalog_manage -- backup_restore_action -- error swap display : {error}")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

    @staticmethod
    def a___________________end___________________():
        pass


class CatalogLoad(ConvertTemplate):

    def __init__(self, allplan, file_path: str, bdd_title: str, conversion=False):
        super().__init__(allplan, file_path, bdd_title, conversion)

        # ---------------------------------------
        # LOADING VARIABLES
        # ---------------------------------------
        self.root = None

        self.region = ""

        self.link_used_count = dict()
        self.dict_liens_node = dict()

        self.img_path_dict = dict()

        self.find_list = list()
        self.link_orphan = list()

        # ---------------------------------------
        # LOADING Translation
        # ---------------------------------------
        self.unknow_title = self.tr("Attribut inconnu")
        self.error_material_exist = self.tr("Détection Doublons dans le dossier")

    def run(self):

        self.start_loading()

        try:

            tree = etree.parse(self.file_path)
            self.root = tree.getroot()

            self.region = self.root.get("Region", self.allplan.langue)

            if self.region == "GB":
                self.region = "EN"

            self.allplan.formula_convert_name = self.region == self.allplan.langue

        except Exception as error:
            print(f"catalog_manage -- CatalogLoad -- analyse_display -- {error}")
            self.errors_list.append(f"run -- {error}")
            return False

        # -------------------------------------------------
        # init affichage
        # -------------------------------------------------

        catalog_folder = find_folder_path(self.file_path)
        catalog_name = find_filename(self.file_path)

        if not catalog_name or not catalog_folder:
            self.loading_completed.emit(self.cat_model,
                                        self.expanded_list,
                                        self.selected_list)
            print(f"catalog_manage -- CatalogLoad -- analyse_display -- not catalog_name or not catalog_folder")
            return

        root_display = self.display_load(catalog_name=catalog_name, catalog_folder=catalog_folder)

        # -------------------------------------------------
        # chargement hierarchie
        # -------------------------------------------------

        self.catalog_load(self.cat_model.invisibleRootItem(), self.root, root_display)

        if len(self.link_orphan) != 0:
            self.cat_model.appendRow(self.link_orphan)

        self.link_verification()

        # -------------

        self.end_loading()

        # -------------

    @staticmethod
    def display_load(catalog_name: str, catalog_folder: str):

        catalog_setting_folder = get_catalog_setting_folder(catalog_folder=catalog_folder)

        if not catalog_setting_folder:
            print(f"catalog_manage -- CatalogLoad --  display_load -- not catalog_setting_folder")
            return None

        catalog_setting_display_file = get_catalog_setting_display_file(catalog_settings_folder=catalog_setting_folder,
                                                                        catalog_name=catalog_name)

        if not catalog_setting_display_file:
            print(f"catalog_manage -- CatalogLoad --  display_load -- not catalog_setting_display_file")
            return None

        if not os.path.exists(catalog_setting_display_file):
            print(f"catalog_manage -- CatalogLoad --  display_load -- not os.path.exists(catalog_setting_display_file)")
            return None

        try:
            tree_display = etree.parse(catalog_setting_display_file)
            return tree_display.getroot()

        except Exception as error:
            print(f"catalog_manage -- CatalogLoad --  display_load -- {error}")
            return None

    def catalog_load(self, qs_parent: QStandardItem, element: etree._Element, element_display: etree._Element):

        for child in element:

            tag = child.tag

            if not isinstance(tag, str):
                print("catalog_manage -- CatalogLoad -- catalog_load -- not isinstance(tag, str)")
                continue

            # -----------------------------------------------
            # Links
            # -----------------------------------------------

            if tag == "Links":
                self.links_load(child)
                continue

            # -----------------------------------------------
            # Node
            # -----------------------------------------------

            if tag == "Node":

                name = child.get('name')

                if name is None:
                    print("catalog_manage -- CatalogLoad -- catalog_load -- name is None")
                    continue

                if name.startswith("------------------- ") and name.endswith(" ------------------- "):
                    continue

                description = child.get('comment', "")

                if name.endswith(f" -- {description}"):
                    name = name.replace(f" -- {description}", "")

                if element_display is None:

                    qs_list = self.creation.folder_line(value=name, description=description)
                    qs_current = qs_list[0]
                    current_display = None

                else:

                    search_child_display = catalog_xml_find_all(element=element_display,
                                                                tag="Node",
                                                                parameter="name",
                                                                value=name)

                    # search_child_display = element_display.findall(f'Node[@name="{name}"]')

                    search_count = len(search_child_display)

                    if search_count == 0:
                        qs_list = self.creation.folder_line(value=name, description=description)
                        qs_current = qs_list[0]
                        current_display = element_display

                        self.catalog_load(qs_current, child, current_display)
                        qs_parent.appendRow(qs_list)

                        continue

                    if search_count == 1:
                        current_display = search_child_display[0]

                    else:
                        current_display = None

                        for element in search_child_display:
                            if element not in self.find_list:
                                current_display = element
                                break

                        if current_display is None:
                            print(f"catalog_manage -- CatalogLoad -- catalog_load -- current_display is None--> "
                                  f"{tag} - {name}")
                            return element_display

                        self.find_list.append(current_display)

                    img_path = current_display.get("icon", current_display.get("icone_dossier", ""))

                    if img_path == "":
                        qs_list = self.creation.folder_line(value=name, description=description)

                    else:

                        if img_path in self.img_path_dict:
                            icon_path = self.img_path_dict[img_path]

                        elif img_path == "folder.png":
                            icon_path = folder_icon
                            self.img_path_dict[img_path] = icon_path

                        else:

                            icon_path = self.find_img(img_path)
                            self.img_path_dict[img_path] = icon_path

                        self.allplan.icon_list.append(icon_path)

                        qs_list = self.creation.folder_line(value=name,
                                                            description=description,
                                                            icon_path=icon_path)

                    qs_current = qs_list[0]

                    if current_display.get("expanded", current_display.get("deplier")) == "True":
                        self.expanded_list.append(qs_current)

                    if current_display.get("selected") == "True":
                        self.selected_list.append(qs_current)

                self.catalog_load(qs_current, child, current_display)

                qs_parent.appendRow(qs_list)

                continue

            # -----------------------------------------------
            # Group and Position
            # -----------------------------------------------

            if tag == "Group" or tag == "Position":
                self.children_load(child, element_display, qs_parent, tag)
                continue

            # -----------------------------------------------
            # Link
            # -----------------------------------------------

            if tag == "Link":

                name = child.get('name')

                if name is None:
                    print("catalog_manage -- CatalogLoad -- catalog_load -- name is None")
                    continue

                material_element = self.root.find(f'.//Group//GroupDef//Attribute[@value="{name}"]')

                description = ""

                if material_element is not None:

                    material_parent_elemnent = material_element.getparent()

                    if material_parent_elemnent is not None:

                        material_element = material_parent_elemnent.find(f'Attribute[@id="207"]')

                        if material_element is not None:
                            description = material_element.get("value", "")

                self.link_list.append(name)
                self.material_with_link_list.append(qs_parent.text().upper())

                qs_list = self.creation.link_line(value=name, description=description)
                qs_parent.appendRow(qs_list)

                self.display_parameters_check(element_display=element_display, qs_current=qs_list[0], tag=tag)

    @staticmethod
    def find_img(current_path: str):

        if current_path is None:
            print("catalog_manage -- CatalogLoad -- current_path -- current_path is None")
            return ""

        if os.path.exists(current_path):
            return current_path

        img_name = current_path.replace(".png", "")

        current_path = f"{icons_path}{datas_icons.get(img_name, img_name)}.png"

        if os.path.exists(current_path):
            return current_path

        print("catalog_manage -- CatalogLoad -- current_path -- img not found")
        return ""

    def children_load(self, child, element_display, qs_parent: QStandardItem, tag: str):

        presence_layer = False
        presence_remplissage = False
        presence_piece = False

        liste_defaut = list()
        datas_attribut_layer = dict(attribute_val_default_layer)
        datas_attribut_remp = dict(attribute_val_default_fill)
        datas_attribut_piece = dict(attribute_val_default_room)

        liste_autres = list()

        liste_attributs = list()

        name = child.get("name", "")
        description = ""

        # ----------------------------
        # search attributes
        # ----------------------------

        attributes = child.findall(f'{tag}Def/Attribute')

        if len(attributes) == 0:
            print("catalog_manage -- CatalogLoad --  children_load -- len(attributes) == 0")
            return None

        for attribute in attributes:

            number_str = attribute.get("id")
            value = attribute.get("value", "")

            if number_str is None:
                print("catalog_manage -- CatalogLoad --  children_load -- number is None")
                return None

            if number_str in liste_attributs:
                print("catalog_manage -- CatalogLoad --  children_load -- number in liste_attributs")
                continue

            liste_attributs.append(number_str)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):

                self.number_error_list.append(number_str)

                try:
                    number_int = int(number_str)

                    user = 1999 < number_int < 12000
                    import_number = 55000 <= number_int < 99000

                except ValueError:
                    continue

                attrib_name = f'{self.unknow_title} ({len(self.number_error_list)})'

                self.allplan.allplan_attribute_add(number_str=number_str,
                                                   name=attrib_name,
                                                   group="",
                                                   value="",
                                                   datatype=type_unknown,
                                                   option=type_unknown,
                                                   unit="",
                                                   uid="???",
                                                   user=user,
                                                   import_number=import_number,
                                                   modify="???",
                                                   visible="???",
                                                   min_val="",
                                                   max_val="",
                                                   enumeration=QStandardItemModel(),
                                                   unkown=True)

                liste_autres.append([number_str, value])
                continue

            # -----------------------------------------
            # Attribute 83
            # -----------------------------------------

            if number_str == attribut_default_obj.current:
                name = value
                continue

            # -----------------------------------------
            # Attribute 207
            # -----------------------------------------

            if number_str == "207":
                description = value
                continue

            # -----------------------------------------
            # Attribute 202
            # -----------------------------------------

            if number_str == "202":
                liste_defaut.append([number_str, self.allplan.convert_unit(unit=value)])
                continue

            # -----------------------------------------
            # Attribute 335
            # -----------------------------------------

            if number_str == "335":
                self.allplan.surface_all_list.append(value)

                if value not in self.allplan.surface_list:
                    self.allplan.surface_list.append(value)

                liste_autres.append([number_str, value])
                continue

            # -----------------------------------------
            # Attribute 120  - 209 - 110
            # -----------------------------------------

            if number_str in attribut_val_defaut_defaut:
                liste_defaut.append([number_str, value])
                continue

            # -----------------------------------------
            # Attribute 141 - 349 - 346 - 345 - 347
            # -----------------------------------------

            if number_str in attribute_val_default_layer:
                presence_layer = True
                datas_attribut_layer[number_str] = value
                continue

            # -----------------------------------------
            # Attribute 118 - 111 - 252 - 336 - 600
            # -----------------------------------------

            if number_str in attribute_val_default_fill:
                presence_remplissage = True
                datas_attribut_remp[number_str] = value
                continue

            # -----------------------------------------
            # Attribute 231 - 235 - 232 - 266 - 233 - 264
            # -----------------------------------------

            if number_str in attribute_val_default_room:
                presence_piece = True

                if number_str == "232":
                    datas_attribut_piece[number_str] = self.allplan.traduire_valeur_232(value_current=value,
                                                                                        region=self.region)

                elif number_str == "233":
                    datas_attribut_piece[number_str] = self.allplan.traduire_valeur_233(value_current=value,
                                                                                        region=self.region)

                elif number_str == "235":
                    datas_attribut_piece[number_str] = self.allplan.traduire_valeur_235(value_current=value,
                                                                                        region=self.region)

                else:
                    datas_attribut_piece[number_str] = value

                continue

            # -----------------------------------------
            # Attribute 76 - 96 - 180 - 267
            # -----------------------------------------

            if number_str in formula_list_attributes:

                if self.allplan.version_allplan_current != "2022":
                    if len(re.findall(pattern=formula_piece_pattern, string=value)):
                        value = re.sub(pattern=formula_piece_pattern,
                                       repl=lambda m: formula_piece_dict.get(m.group(0)),
                                       string=value,
                                       flags=re.IGNORECASE)

                if self.region == self.allplan.langue:
                    value = self.allplan.formula_replace_all_name(formula=value)

                liste_autres.append([number_str, value])
                continue

            # -----------------------------------------
            # Attribute > 1999 & < 12000
            # -----------------------------------------

            try:
                number_int = int(number_str)

                if 1999 < number_int < 12000:

                    if attribute_obj.option not in [code_attr_formule_str, code_attr_formule_int,
                                                    code_attr_formule_float]:
                        liste_autres.append([number_str, value])
                        continue

                    valeur_formule = attribute_obj.value

                    if self.allplan.version_allplan_current != "2022":
                        if len(re.findall(pattern=formula_piece_pattern, string=valeur_formule)):
                            valeur_formule = re.sub(pattern=formula_piece_pattern,
                                                    repl=lambda m: formula_piece_dict.get(m.group(0)),
                                                    string=valeur_formule,
                                                    flags=re.IGNORECASE)

                    liste_autres.append([number_str, valeur_formule])
                    continue

            except ValueError:
                pass

            # -----------------------------------------
            # Attribute Other
            # -----------------------------------------

            liste_autres.append([number_str, value])
            continue

        liste_defaut.sort(key=lambda x: int(x[0]))
        liste_autres.sort(key=lambda x: int(x[0]))

        # ==================================================================== #
        # QStandardItem Creation (Material / Component
        # ==================================================================== #

        if name == "":
            print("catalog_manage -- CatalogLoad --  attributes_add -- name est vide")
            return None

        if tag == "Group":

            material_renamed = name.upper() in self.material_upper_list

            if material_renamed:
                original_name = name

                name = find_new_title(name, self.material_upper_list)

                self.errors_list.append(f"{self.error_material_exist} '{qs_parent.text()}' : "
                                        f"'{original_name}' -->  {name}")

            qs_list = self.creation.material_line(value=name,
                                                  description=description,
                                                  used_by_links=self.link_used_count.get(name, 0))

            qs_current: QStandardItem = qs_list[0]

            self.material_upper_list.append(name.upper())
            self.material_list.append(name)

            if material_renamed:
                self.selected_list.append(qs_current)
                self.expanded_list.append(qs_current)

        elif tag == "Position":

            qs_list = self.creation.component_line(value=name,
                                                   description=description)

            qs_current: QStandardItem = qs_list[0]

        else:

            return None

        if element_display is not None:
            current_display = self.display_parameters_check(element_display, qs_current, tag)
        else:
            current_display = None

        # ==================================================================== #
        # Attribute Creation
        # ==================================================================== #

        # -----------------------------------------
        # Attribute 120  - 209 - 110
        # -----------------------------------------

        for number_str, value in liste_defaut:
            qs_current.appendRow(self.creation.attribute_line(value=value, number_str=number_str))

        # -----------------------------------------
        # Attribute 118 - 111 - 252 - 336 - 600
        # -----------------------------------------

        if presence_remplissage:

            type_remplissage = datas_attribut_remp.get("118", "0")

            if type_remplissage == "1":
                model_enumeration = self.allplan.model_haching
            elif type_remplissage == "2":
                model_enumeration = self.allplan.model_pattern
            elif type_remplissage == "3":
                model_enumeration = self.allplan.model_color
            elif type_remplissage == "5":
                model_enumeration = self.allplan.model_style
            elif type_remplissage == "6":
                model_enumeration = self.allplan.model_none
            else:
                model_enumeration = self.allplan.model_none
                datas_attribut_remp["111"] = "-1"
                datas_attribut_remp["252"] = "-1"
                datas_attribut_remp["336"] = ""
                datas_attribut_remp["600"] = "0"

            for number_str, value in datas_attribut_remp.items():

                if number_str == "111":
                    qs_current.appendRow(self.creation.attribute_line(value=value,
                                                                      number_str=number_str,
                                                                      model_enumeration=model_enumeration))
                    continue

                qs_current.appendRow(self.creation.attribute_line(value=value, number_str=number_str))

        # -----------------------------------------
        # Attribute 141 - 349 - 346 - 345 - 347
        # -----------------------------------------

        if presence_layer:
            for number_str, value in datas_attribut_layer.items():
                qs_current.appendRow(self.creation.attribute_line(value=value, number_str=number_str))
        # -----------------------------------------
        # Attribute 231 - 235 - 232 - 266 - 233 - 264
        # -----------------------------------------

        if presence_piece:

            for number_str, value in datas_attribut_piece.items():
                qs_current.appendRow(self.creation.attribute_line(value=value, number_str=number_str))

        # -----------------------------------------
        # Attributes Other
        # -----------------------------------------

        if len(liste_autres) != 0:
            for number_str, value in liste_autres:
                qs_current.appendRow(self.creation.attribute_line(value=value, number_str=number_str))

        if tag == "Group":
            self.catalog_load(qs_current, child, current_display)

        qs_parent.appendRow(qs_list)

        return

    def display_parameters_check(self, element_display, qs_current: QStandardItem, tag: str):

        if element_display is None:
            return None

        name = qs_current.text()

        search_child_display = catalog_xml_find_all(element=element_display,
                                                    tag=tag,
                                                    parameter="name",
                                                    value=name)

        search_count = len(search_child_display)

        child_display = None

        if search_count == 0:

            if tag != "Link":
                print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- search_child_display is None 0--> "
                      f"{tag} - {name}")

                return element_display

            search_child_display = catalog_xml_find_all(element=element_display,
                                                        tag="link",
                                                        parameter="name",
                                                        value=name)

            # search_child_display = element_display.findall(f'link[@name="{name}"]')

            search_count = len(search_child_display)

            if search_count == 0:
                print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- search_child_display is None 1--> "
                      f"{tag} - {name}")

                return element_display

            if search_count == 1:
                child_display = search_child_display[0]

            else:

                for element in search_child_display:
                    if element not in self.find_list:
                        child_display = element
                        break

                if child_display is None:
                    print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- "
                          f"search_child_display is None 2--> {tag} - {name}")
                    return element_display

                self.find_list.append(child_display)

        if search_count == 1:
            child_display = search_child_display[0]
        else:

            for element in search_child_display:
                if element not in self.find_list:
                    child_display = element
                    break

            if child_display is None:
                print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- search_child_display is None 2--> "
                      f"{tag} - {name}")
                return element_display

            self.find_list.append(child_display)

        name_display = child_display.get("name")

        if name_display is None:
            print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- name_display is None")
            return element_display

        if tag == "Group":

            if child_display.get("expanded", child_display.get("deplier")) == "True":
                self.expanded_list.append(qs_current)

        if child_display.get("selected") == "True":
            self.selected_list.append(qs_current)

        return child_display

    def links_load(self, element):

        if "2022" in self.allplan.version_allplan_current:
            line_1 = self.tr("Ce catalogue utilise des liens et ne sont pas compatible avec Allplan 2022")
            line_2 = self.tr("Allplan 2022 refusera d'ouvrir ce catalogue.")

            msg(titre=application_title,
                message=f"{line_1}\n{line_2}",
                icone_critique=True)

        qs_folder_list = self.creation.folder_line(value=self.tr("Lien"), description="")

        qs_folder: Folder = qs_folder_list[0]

        link_orphan_find = False

        for child in element:

            name = child.get("name")

            if not isinstance(name, str):
                continue

            if name.upper() in self.material_with_link_list:
                continue

            search_link = catalog_xml_find_all(element=self.root,
                                               tag=".//Link",
                                               parameter="name",
                                               value=name)

            # search_link = self.root.findall(f'.//Link[@name="{name}"]')

            self.link_used_count[name] = len(search_link)

            # search_material = self.root.findall(f'.//Group//GroupDef//Attribute[@value="{name}"]')

            search_material = catalog_xml_find_all(element=self.root,
                                                   tag=".//Group//GroupDef//Attribute",
                                                   parameter="value",
                                                   value=name)

            results = [item.get("id") == "83" for item in search_material]

            if True not in results:
                link_orphan_find = True
                # used_by_links = self.root.findall(f'.//Link[@name="{name}"]')

                used_by_links = catalog_xml_find_all(element=self.root,
                                                     tag=".//Link",
                                                     parameter="name",
                                                     value=name)

                qs_material_list = self.creation.material_line(value=name,
                                                               description="",
                                                               used_by_links=used_by_links,
                                                               tooltips=True)

                qs_current: Material = qs_material_list[0]

                component_list = child.findall("Position")

                for component_child in component_list:
                    self.children_load(child=component_child,
                                       element_display=None,
                                       qs_parent=qs_current,
                                       tag="Position")

                qs_folder.appendRow(qs_material_list)

        if link_orphan_find:
            self.link_orphan = qs_folder_list

    def link_verification(self):

        links_set = set(self.link_list)

        link_errors = set()

        for material_name in links_set:

            if material_name in link_errors:
                continue

            if material_name.upper() not in self.material_with_link_list:
                continue

            if not self.link_detect_circular(material_name=material_name, visited=set(), path=list()):
                continue

            link_errors.add(material_name)

    def link_detect_circular(self, material_name: str, visited: set, path: list) -> bool:

        if material_name in visited:
            loop_start_index = path.index(material_name)
            loop_path = " -> ".join(path[loop_start_index:])

            print(f"catalog_manage -- CatalogLoad -- link_detect_circular -- loop detected")

            loop_message = self.tr("Liens : Boucle détéctée")
            self.errors_list.append(f"{loop_message} : {loop_path} -> {material_name}")
            return True

        visited.add(material_name)
        path.append(material_name)

        search_start = self.cat_model.index(0, col_cat_value)

        search = self.cat_model.match(search_start, Qt.DisplayRole, material_name, -1,
                                      Qt.MatchExactly | Qt.MatchRecursive)

        for qm in search:

            if not qm_check(qm):
                continue

            if qm.data(user_data_type) != link_code:
                continue

            qm_parent = qm.parent()

            if not qm_check(qm_parent):
                continue

            parent_name = qm_parent.data()

            if not isinstance(parent_name, str):
                continue

            if self.link_detect_circular(material_name=parent_name, visited=visited, path=path):
                return True

        visited.remove(material_name)
        path.pop()
        return False

    @staticmethod
    def a___________________end___________________():
        pass


class CatalogSave(QObject):

    def __init__(self, asc, catalog, allplan, catalog_path="", catalog_setting_display_file="",
                 exlcude_default_attribute=""):

        super().__init__()

        self.ui: Ui_MainWindow = asc.ui
        self.filtre: QSortFilterProxyModel = self.ui.hierarchy.model()

        self.allplan: AllplanDatas = allplan

        self.catalog: CatalogDatas = catalog

        self.model = self.ui.hierarchy.cat_model

        self.exlcude_default_attribute = exlcude_default_attribute

        self.qm_selection_list = self.ui.hierarchy.get_qm_model_selection_list()
        self.qm_expanded_list = self.ui.hierarchy.get_qm_model_expanded_list()

        self.link_list = list()

        # Informations path catalog

        self.catalog_path = self.catalog.catalog_path

        self.catalog_folder = self.catalog.catalog_folder
        self.catalog_name = self.catalog.catalog_name

        self.catalog_setting_display_file = self.catalog.catalog_setting_display_file

        self.define_paths(catalog_path=catalog_path, catalog_setting_display_file=catalog_setting_display_file)

        self.material_dict = dict()

        if not self.backup_catalogue():
            return

        self.sauvegarde_catalogue()

    def define_paths(self, catalog_path: str, catalog_setting_display_file: str):

        if not isinstance(catalog_path, str) or not isinstance(catalog_setting_display_file, str):
            return

        if catalog_path == "" or catalog_setting_display_file == "":
            return

        catalog_folder = find_folder_path(file_path=catalog_path)

        if catalog_folder == "":
            return

        catalog_name = find_filename(file_path=catalog_path)

        if catalog_name == "":
            return

        self.catalog_path = catalog_path

        self.catalog_folder = catalog_folder
        self.catalog_name = catalog_name

        self.catalog_setting_display_file = catalog_setting_display_file

    def backup_catalogue(self):

        catalog_folder_backup = f"{self.catalog_folder}backup\\"

        if self.catalog_folder == "" or self.catalog_name == "":
            return False

        if not make_backup(chemin_dossier=self.catalog_folder, fichier=self.catalog_name, extension=".xml",
                           dossier_sauvegarde=catalog_folder_backup, nouveau=False):
            return False

        nom_fichier = f"{self.catalog_name}_display"

        catalog_setting_folder = get_catalog_setting_folder(catalog_folder=self.catalog_folder)
        catalog_setting_folder_backup = f"{catalog_setting_folder}backup\\"

        if catalog_setting_folder == "" or nom_fichier == "":
            return False

        if not make_backup(chemin_dossier=catalog_setting_folder, fichier=nom_fichier, extension=".xml",
                           dossier_sauvegarde=catalog_setting_folder_backup, nouveau=False):
            return False

        return True

    def sauvegarde_catalogue(self):

        region = catalog_xml_region(self.allplan.langue)
        # version_xml = catalog_xml_version(self.allplan.version_allplan_current)
        version_xml = "1.0"
        date_modif = catalog_xml_date(self.allplan.langue)

        a = self.tr("Dernier enregistrement")

        root = etree.Element('AllplanCatalog',
                             Region=region,
                             version=version_xml)

        root.set("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation",
                 "../Xsd/AllplanCatalog.xsd")

        root_expand = etree.Element('Smart-Catalog')

        etree.SubElement(root, 'Node', name=f"------------------- {a} : {date_modif} ------------------- ")
        etree.SubElement(root_expand, 'Node', name=f"------------------- {a} : {date_modif} ------------------- ")

        self.sauvegarde_hierarchie(self.model.invisibleRootItem(), root, root_expand)

        if len(self.link_list) != 0:
            self.save_links(root)

        a = self.tr("Une erreur est survenue.")

        tps = time.perf_counter()

        # ------------------------------------------------
        # -------------------- Save catalog --------------
        # ------------------------------------------------

        try:

            catalogue_tree = etree.ElementTree(root)
            catalogue_tree.write(self.catalog_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        except Exception as erreur:
            msg(titre=application_title,
                message=f'{a} : {self.catalog_path}',
                icone_critique=True,
                details=f"{erreur}")
            return False

        # ------------------------------------------------
        # -------------------- Save display --------------
        # ------------------------------------------------
        try:

            expand_tree = etree.ElementTree(root_expand)
            expand_tree.write(self.catalog_setting_display_file,
                              pretty_print=True,
                              xml_declaration=True,
                              encoding="UTF-8")

            print(f"catalogue save : {time.perf_counter() - tps}s")

            return True

        except Exception as erreur:

            msg(titre=application_title,
                message=f"{a} : {self.catalog_setting_display_file}",
                icone_avertissement=True,
                details=f"{erreur}")
            return False

    def save_links(self, root: etree._Element):

        self.link_list.sort()

        if len(self.link_list) == 0:
            return

        links = etree.Element("Links")

        for material_name in self.link_list:

            linkdef = etree.Element("LinkDef", name=material_name)

            self.save_sub_links(material_name=material_name, linkdef=linkdef, visited=set())

            if len(linkdef) == 0:
                continue

            links.append(linkdef)

        if len(links) == 0:
            return

        root.insert(0, links)

    def save_sub_links(self, material_name: str, linkdef: etree._Element, visited: set) -> bool:

        if material_name in visited:
            print(f"catalog_manage -- CatalogSave -- save_sub_link -- {material_name} in visited")
            return True

        qs_material: MyQstandardItem = self.material_dict.get(material_name, None)

        if not isinstance(qs_material, Material):
            print("catalog_manage -- CatalogSave -- save_sub_link -- not isinstance(qs_material, Material)")
            return True

        visited.add(material_name)

        if not qs_material.hasChildren():
            return True

        for index_child in range(qs_material.rowCount()):

            qs_child: MyQstandardItem = qs_material.child(index_child, col_cat_value)

            if isinstance(qs_child, Component):
                self.new_component(item=qs_child, group=linkdef, affichage=None, selected=None)
                continue

            if isinstance(qs_child, Link):
                if self.save_sub_links(material_name=qs_child.text(), linkdef=linkdef, visited=visited):
                    return True

        visited.remove(material_name)
        return False

    def sauvegarde_hierarchie(self, item_parent: MyQstandardItem, racine: etree._Element, affichage: etree._Element):

        for index_row in range(item_parent.rowCount()):

            qs_value = item_parent.child(index_row, col_cat_value)
            qs_desc = item_parent.child(index_row, col_cat_desc)

            if isinstance(qs_value, Attribute):
                continue

            if not isinstance(qs_desc, Info):
                continue

            qm_value = qs_value.index()

            deplier = qm_value in self.qm_expanded_list
            selected = qm_value in self.qm_selection_list

            if isinstance(qs_value, Folder):

                icone_dossier = qs_value.icon_path
                node, node_aff = self.new_folder(qs_value, racine, affichage, deplier, selected, icone_dossier,
                                                 qs_desc.text())

                if not qs_value.hasChildren():
                    continue

                self.sauvegarde_hierarchie(qs_value, node, node_aff)
                continue

            if isinstance(qs_value, Material):
                group, node_aff = self.new_material(qs_value, racine, affichage, deplier, selected)

                if not qs_value.hasChildren():
                    continue

                self.sauvegarde_hierarchie(qs_value, group, node_aff)
                continue

            elif isinstance(qs_value, Component):
                self.new_component(qs_value, racine, affichage, selected)
                continue

            elif isinstance(qs_value, Link):
                self.new_link(qs_value, racine, affichage, selected)
                continue

    @staticmethod
    def new_folder(item: QStandardItem, racine: etree._Element, affichage: etree._Element,
                   deplier: bool, selected: bool, icone_dossier=folder_icon, description=""):

        titre = item.text()
        if description == "":
            node = etree.SubElement(racine, "Node", name=titre)
        else:
            node = etree.SubElement(racine, "Node", name=f"{titre} -- {description}", comment=description)

        datas = dict()

        if deplier:
            datas["expanded"] = "True"

        if selected:
            datas["selected"] = "True"

        if icone_dossier.startswith(":/Images/") and icone_dossier != folder_icon:
            datas["icon"] = icone_dossier.replace(":/Images/", "")

        elif icons_old_path in icone_dossier:
            icone_name = icone_dossier.replace(icons_old_path, "")

            if icone_name in datas_icons:
                icone_name_tmp = datas_icons[icone_dossier]

                if os.path.exists(f"{icons_path}{icone_name_tmp}.png"):
                    datas["icon"] = icone_name_tmp
                else:
                    datas["icon"] = icone_dossier

            else:
                datas["icon"] = icone_dossier

        elif icons_path in icone_dossier:
            icone_dossier = icone_dossier.replace(icons_path, "")

            if icone_dossier in datas_icons:
                icone_dossier = datas_icons[icone_dossier]

            datas["icon"] = icone_dossier

        node_aff = etree.SubElement(affichage, "Node", name=titre, **datas)

        return node, node_aff

    def new_material(self, item: MyQstandardItem, node: etree._Element, affichage: etree._Element,
                     deplier: bool, selected: bool):

        material_name = item.text()

        if material_name in self.material_dict:
            material_name = find_new_title(base_title=material_name, titles_list=material_upper_list)
            print("catalog_manage -- CatalogSave -- creation_ouvrage -- Material already exists !!!")

        self.material_dict[material_name] = item

        # -----------

        group = etree.SubElement(node, "Group", name=material_name)

        group_def = etree.SubElement(group, 'GroupDef')

        self.new_attribute(item=item, definition=group_def)

        # -----------

        datas = dict()

        if deplier:
            datas["expanded"] = "True"

        if selected:
            datas["selected"] = "True"

        node_aff = etree.SubElement(affichage, "Group", name=material_name, **datas)

        return group, node_aff

    def new_component(self, item: MyQstandardItem, group: etree._Element, affichage: etree._Element,
                      selected: bool):

        component_name = item.text()

        position = etree.SubElement(group, "Position", name=component_name)

        position_def = etree.SubElement(position, 'PositionDef')

        self.new_attribute(item=item, definition=position_def)

        if affichage is None:
            return

        if selected:
            etree.SubElement(affichage, "Position", name=component_name, selected="True")
        else:
            etree.SubElement(affichage, "Position", name=component_name)

        return

    def new_link(self, item: MyQstandardItem, group: etree._Element, affichage: etree._Element, selected: bool):

        link_name = item.text()

        if link_name not in self.link_list:
            self.link_list.append(link_name)

        etree.SubElement(group, "Link", name=link_name)

        if affichage is None:
            return

        if selected:
            etree.SubElement(affichage, "Link", name=link_name, selected="True")
        else:
            etree.SubElement(affichage, "Link", name=link_name)

        return

    def new_attribute(self, item: MyQstandardItem, definition: etree._Element):

        # titre = item.text()

        if attribut_default_obj.current != "":
            etree.SubElement(definition, 'Attribute', id=attribut_default_obj.current, value=item.text())

        nb_enfants = item.rowCount()
        plume = True
        trait = True
        couleur = True

        attributes_list = list()

        for index_row in range(nb_enfants):

            qs_child_value: QStandardItem = item.child(index_row, col_cat_value)

            if not isinstance(qs_child_value, Attribute):
                return

            qs_number_child: QStandardItem = item.child(index_row, col_cat_number)

            if not isinstance(qs_number_child, Info):
                print("catalog_manage -- new_attribute -- not isinstance(qs_number_child, Info)")
                return

            valeur = qs_child_value.text()
            number_str = qs_number_child.text()

            if number_str == attribut_default_obj.current or number_str == self.exlcude_default_attribute:
                continue

            if number_str in liste_attributs_with_no_val_no_save and valeur == "":
                continue

            if number_str in attributes_list:
                continue

            if number_str == "349":
                plume, trait, couleur = self.layout_manage(valeur)

            if ((number_str == "346" and not plume) or (number_str == "345" and not trait) or
                    (number_str == "347" and not couleur)):
                continue

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):
                print("catalog_manage -- CatalogSave -- new_attribute -- not isinstance(attribute_obj, AttributeDatas)")
                continue

            type_ele2: str = attribute_obj.option

            if type_ele2 == code_attr_combo_int:
                qs_index_child: QStandardItem = item.child(index_row, col_cat_index)

                if not isinstance(qs_index_child, Info):
                    print("catalog_manage -- CatalogSave -- new_attribute -- not isinstance(qs_index_child, Info)")
                    continue

                valeur = qs_index_child.text()

                if not isinstance(valeur, str):
                    print("catalog_manage -- CatalogSave -- new_attribute -- not isinstance(valeur, str)")
                    continue

                if valeur.startswith("0"):
                    try:

                        valeur_int = int(valeur)

                    except Exception:
                        continue

                    valeur = f"{valeur_int}"

                etree.SubElement(definition, 'Attribute', id=number_str, value=valeur)
                attributes_list.append(number_str)
                continue

            if type_ele2 in [code_attr_formule_str, code_attr_formule_int, code_attr_formule_float]:

                if "\n" in valeur:
                    valeur = valeur.replace("\n", "")

                try:
                    numero_int = int(number_str)

                    if 1999 < numero_int < 12000:
                        valeur = "1"

                    else:

                        valeur = self.allplan.convertir_formule(valeur)

                except ValueError:
                    pass

                etree.SubElement(definition, 'Attribute', id=number_str, value=valeur)
                attributes_list.append(number_str)
                continue

            etree.SubElement(definition, 'Attribute', id=number_str, value=valeur)
            attributes_list.append(number_str)
        return

    @staticmethod
    def layout_manage(numero_style: str):

        plume = True
        trait = True
        couleur = True

        if numero_style == "1":
            plume = False
            return plume, trait, couleur

        if numero_style == "2":
            trait = False
            return plume, trait, couleur

        if numero_style == "3":
            plume = False
            trait = False
            return plume, trait, couleur

        if numero_style == "4":
            couleur = False
            return plume, trait, couleur

        if numero_style == "5":
            plume = False
            couleur = False
            return plume, trait, couleur

        if numero_style == "6":
            trait = False
            couleur = False
            return plume, trait, couleur

        if numero_style == "7":
            plume = False
            trait = False
            couleur = False
            return plume, trait, couleur

        return plume, trait, couleur

    @staticmethod
    def a___________________end___________________():
        pass
