#!/usr/bin/python3
# -*- coding: utf-8 -*

import os.path
import shutil

from catalog_manage import *
from convert_manage import BddTypeDetection
from formatting_widget import Formatting
from main_datas import app_setting_file
from tools import afficher_message as msg
from tools import get_look_tableview, make_backup, find_folder_path, get_bdd_paths, browser_file
from tools import settings_save, catalog_name_is_correct, move_window_tool, get_look_combobox
from tools import verification_projet, parcourir_dossier, get_real_path_of_apn_file, find_filename, get_project_use
from ui_catalog_new import Ui_CatalogNew
from ui_catalog_update import Ui_CatalogUpdate

col_save_nom = 0
col_save_chemin = 1
convert_valid_bdd = [bdd_type_allmetre_a, bdd_type_allmetre_e, bdd_type_bcm, bdd_type_kukat, bdd_type_nevaris,
                     bdd_type_bcm_c]


class WidgetCatalogNew(QWidget):

    def __init__(self, asc):
        super().__init__()

        self.ui = Ui_CatalogNew()
        self.ui.setupUi(self)

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.widget_options = Formatting()

        # -------------

        self.new = True
        self.convert_bdd = False
        self.modify = False

        self.catalog: CatalogDatas = self.asc.catalog
        self.allplan: AllplanDatas = self.asc.allplan

        self.bdd_type = ""

        # -------------
        # Nom du catalogue
        # -------------

        self.ui.cat_name.textChanged.connect(self.catalog_title_change)

        self.ui.verification.clicked.connect(self.catalog_verification_show)

        self.ui.format_bt.clicked.connect(self.options_afficher)
        self.widget_options.save_modif_formatage.connect(self.options_retour_datas)

        # -------------
        # Version Allplan à utiliser
        # -------------

        self.ui.version_list.addItems(self.allplan.versions_list)
        self.ui.version_list.currentTextChanged.connect(self.allplan_change)
        self.ui.version_list.installEventFilter(self)

        get_look_combobox(self.ui.version_list)

        # -------------
        # Où enregistrer le catalogue
        # -------------

        self.ui.save_std.clicked.connect(self.allplan_change)

        self.ui.save_other.clicked.connect(self.allplan_change)
        self.ui.save_other.clicked.connect(self.catalog_browser)

        self.ui.save_browser.clicked.connect(self.catalog_browser)

        # -------------
        # Données issues du
        # -------------

        self.ui.datas_std.clicked.connect(self.allplan_change)

        self.ui.datas_prj.clicked.connect(self.allplan_change)
        self.ui.datas_prj.clicked.connect(self.datas_browser)

        self.ui.datas_browser.clicked.connect(self.datas_browser)

        self.ui.datas_apn_browse.clicked.connect(self.allplan_apn)

        # -------------
        # Attribut par défaut
        # -------------

        get_look_combobox(self.ui.attribute_list)

        # -------------
        # Chemin base de données
        # -------------

        self.ui.bdd_browser.clicked.connect(self.bdd_browser)

        # -------------
        # valider
        # -------------

        self.ui.bt_creation.clicked.connect(self.catalog_new_creation_start)
        self.ui.bt_quitter.clicked.connect(self.close)

    def personnalisation(self, new=False, modify=False, convert_bdd=False, file_path="") -> bool:

        self.new = new
        self.convert_bdd = convert_bdd
        self.modify = modify

        # -------------

        self.catalog_attribute_load()

        # -------------

        if new + convert_bdd + modify != 1:
            return False

        # -------------

        self.setAcceptDrops(self.convert_bdd)

        # -------------

        if new:

            self.ui.save_widget.show()
            self.ui.bdd_widget.hide()
            self.ui.attribute_widget.show()

            self.ui.bt_creation.setText(self.tr("Création"))
            self.setWindowTitle(self.tr("Nouveau catalogue"))

        elif modify:

            self.ui.save_widget.hide()
            self.ui.bdd_widget.hide()
            self.ui.attribute_widget.show()

            self.ui.bt_creation.setText(self.tr("Modifier"))
            self.setWindowTitle(self.tr("Modifier les paramètres"))

        elif convert_bdd:

            self.ui.save_widget.show()
            self.ui.bdd_widget.show()
            self.ui.attribute_widget.hide()

            self.ui.bt_creation.setText(self.tr("Importer"))
            self.setWindowTitle(self.tr("Convertir"))

        else:
            return False

        # -------------------
        # Nom catalogue
        # -------------------

        if modify:
            self.ui.cat_name.setText(self.catalog.catalog_name)

        elif convert_bdd and file_path != "":
            if not self.recherche_valide(file_path=file_path, add=True, message=False):
                return False
        else:
            self.ui.cat_name.setText(self.catalog_find_name())

        self.ui.cat_name.setEnabled(not modify)

        # -------------------
        # Version Allplan
        # -------------------

        version_allplan = self.allplan.version_allplan_current

        self.ui.version_list.blockSignals(True)

        if version_allplan == "":
            version_allplan = self.ui.version_list.currentText()
        else:
            self.ui.version_list.setCurrentText(version_allplan)

        self.ui.version_list.blockSignals(False)

        if version_allplan not in self.allplan.version_datas:
            return False

        version_obj = self.allplan.version_datas[version_allplan]

        if not isinstance(version_obj, AllplanPaths):
            return False

        dossier_std = version_obj.std_path

        try:
            version_allplan_int = int(version_allplan)

            if version_allplan_int >= 2024:
                self.ui.datas_apn_browse.setVisible(True)
            else:
                self.ui.datas_apn_browse.setVisible(False)

        except Exception:
            self.ui.datas_apn_browse.setVisible(False)

        # -------------------
        # Où enregistrer le catalogue
        # -------------------

        if not modify:

            dossier_cat: str = self.catalog.catalog_folder

            if dossier_cat == "" or not os.path.exists(dossier_cat):
                dossier_cat = dossier_std

            if dossier_std.lower() in dossier_cat.lower():
                self.ui.save_std.setChecked(True)
            else:
                self.ui.save_other.setChecked(True)

            self.ui.save_path.setText(self.catalog.catalog_folder)

        # -------------------
        # Données issues du
        # -------------------

        chemin_donnees = self.allplan.catalog_user_path

        if chemin_donnees == "" or not os.path.exists(chemin_donnees):
            chemin_donnees = dossier_std

        chemin_donnees_upper = chemin_donnees.upper()

        if "STD" not in chemin_donnees_upper:
            self.ui.datas_prj.setChecked(True)
        else:
            self.ui.datas_std.setChecked(True)

        self.ui.datas_path.setText(chemin_donnees)

        # -------------------

        self.setMaximumHeight(16777215)

        width = self.width()

        self.adjustSize()

        self.resize(width, self.height())
        self.setMaximumHeight(self.height())

        # -------------------

        self.catalog_title_change()

        move_window_tool(widget_parent=self.asc, widget_current=self, always_center=True)

        self.show()
        return True

    def catalog_attribute_load(self) -> None:

        self.ui.attribute_list.clear()

        attributes_list = list()
        current_index = -1

        self.allplan: AllplanDatas

        for number in attribut_default_obj.valid_list:

            if number == attribut_default_obj.current:
                current_index = len(attributes_list)

            if number == "":
                attributes_list.append(self.tr("Aucun"))
                continue

            name = self.allplan.find_number_by_number(number=number)

            if name != "":
                attributes_list.append(f"{number} -- {name}")

        self.ui.attribute_list.addItems(attributes_list)

        if current_index == -1:
            return

        self.ui.attribute_list.setCurrentIndex(current_index)

    def catalog_find_name(self) -> str:

        filenames_list = glob.glob(f"{self.catalog.catalog_folder}*.xml")

        files_name_list = list()

        for file_path in filenames_list:

            filename = find_filename(file_path)

            if filename == "":
                continue

            files_name_list.append(filename)

        new_name = find_new_title(base_title=self.tr("Nouveau catalogue"), titles_list=files_name_list)

        return new_name

    @staticmethod
    def a___________________catalogue______():
        pass

    def catalog_browser(self):

        version_allplan = self.ui.version_list.currentText()

        if version_allplan in self.allplan.version_datas:

            version_obj = self.allplan.version_datas[version_allplan]

        else:

            version_obj = self.allplan.allplan_paths

        if isinstance(version_obj, AllplanPaths):

            path_default = version_obj.std_path

            # shortcuts_list = [self.allplan.allplan_paths.etc_cat_path,
            #                   self.allplan.allplan_paths.std_cat_path,
            #                   self.allplan.allplan_paths.prj_path,
            #                   self.allplan.allplan_paths.tmp_path]
        else:
            path_default = ""

            # shortcuts_list = list()

        dossier = parcourir_dossier(parent=self,
                                    title=application_title,
                                    registry=[app_setting_file, "path_catalog_save"],
                                    current=self.ui.save_path.text(),
                                    default=path_default,
                                    use_setting_first=False)
        if dossier == "":
            return

        self.ui.save_path.setText(dossier)

        self.catalog_title_change()

    def catalog_title_change(self) -> str:

        verification = self.verification_title()

        if verification == "Ok":

            self.ui.verification.setIcon(get_icon(valid_icon))
            self.ui.verification.setToolTip(self.tr("C'est tout bon!"))

            self.ui.bt_creation.setEnabled(not self.convert_bdd or (self.convert_bdd and self.bdd_type != ""))
            self.ui.bt_creation.setToolTip("")

            self.ui.cat_name.setStyleSheet("QLineEdit{padding-left: 5px; "
                                           "border: 1px solid #8f8f91; "
                                           "border-right-width: 0px; "
                                           "border-top-left-radius:5px; "
                                           "border-bottom-left-radius: 5px; }")

        else:

            self.ui.verification.setIcon(get_icon(error_icon))
            self.ui.verification.setToolTip(verification)

            self.ui.bt_creation.setEnabled(False)
            self.ui.bt_creation.setToolTip(verification)

            self.ui.cat_name.setStyleSheet("QLineEdit{padding-left: 5px; "
                                           "border: 2px solid orange; "
                                           "border-top-left-radius:5px; "
                                           "border-bottom-left-radius: 5px; }")
        return verification

    def verification_title(self) -> str:

        catalog_folder = self.ui.save_path.text()
        catalog_name = self.ui.cat_name.text()

        verification = catalog_name_is_correct(catalog_name=catalog_name)

        if verification != "Ok":
            return verification

        already_exist = self.tr("Ce catalogue existe déjà.")

        if self.modify:

            if catalog_name != self.catalog.catalog_name and os.path.exists(f"{catalog_folder}{catalog_name}.xml"):
                return already_exist

            return "Ok"

        if os.path.exists(f"{catalog_folder}{catalog_name}.xml"):
            return already_exist

        return "Ok"

    def catalog_verification_show(self):

        tooltips = self.ui.verification.toolTip()
        icon_avert = tooltips != self.tr("C'est tout bon!")

        msg(titre=self.windowTitle(),
            message=self.ui.verification.toolTip(),
            icone_critique=icon_avert,
            icone_valide=not icon_avert)

    def options_afficher(self):
        """
        Permet d'afficher le widget option
        :return: None
        """

        self.widget_options.formatting_show(current_parent=self.ui.format_bt,
                                            current_text=self.ui.cat_name.text(),
                                            show_code=False,
                                            show_search=False)

    def options_retour_datas(self, nouveau_texte: str):

        self.ui.cat_name.setText(nouveau_texte)

    @staticmethod
    def a___________________allplan______():
        pass

    def allplan_change(self):

        version_allplan = self.ui.version_list.currentText()

        if version_allplan not in self.allplan.version_datas:
            return

        version_obj = self.allplan.version_datas[version_allplan]

        if not isinstance(version_obj, AllplanPaths):
            return

        chemin_std = version_obj.std_path
        chemin_cat = version_obj.std_cat_path

        try:
            version_allplan_int = int(version_allplan)
            apn_visible = version_allplan_int >= 2024

        except Exception:

            apn_visible = False

        self.ui.datas_apn_browse.setVisible(apn_visible)

        if self.ui.datas_std.isChecked():
            self.ui.datas_path.setText(chemin_std)
        else:

            chemin_donnees = self.ui.datas_path.text().upper()

            if "STD" in chemin_donnees:
                self.ui.datas_path.setText(chemin_std)

        if self.ui.save_std.isChecked():
            self.ui.save_path.setText(chemin_cat)

        self.catalog_title_change()

    def datas_browser(self):

        version_allplan = self.ui.version_list.currentText()

        if version_allplan in self.allplan.version_datas:

            version_obj = self.allplan.version_datas[version_allplan]

        else:

            version_obj = self.allplan.allplan_paths

        if isinstance(version_obj, AllplanPaths):

            path_default = version_obj.prj_path

            # shortcuts_list = [self.allplan.allplan_paths.etc_cat_path,
            #                   self.allplan.allplan_paths.std_cat_path,
            #                   self.allplan.allplan_paths.prj_path,
            #                   self.allplan.allplan_paths.tmp_path]

        else:
            path_default = ""

            # shortcuts_list = list()

        dossier = parcourir_dossier(parent=self,
                                    title=application_title,
                                    registry=[app_setting_file, "path_catalog_prj"],
                                    current=path_default,
                                    default=self.ui.datas_path.text(),
                                    use_setting_first=False)
        if dossier == "":
            return

        if not dossier.endswith(".prj\\"):
            msg(titre=self.windowTitle(),
                message=self.tr("Le Nom du dossier choisi doit finir par '.prj', désolé"),
                icone_critique=True)
            return

        verification = verification_projet(dossier)

        if verification:
            msg(titre=self.windowTitle(),
                message=self.tr("L'ensemble des paramètres de ce projet est en STD."),
                icone_avertissement=True)

            return

        self.ui.datas_path.setText(dossier)
        self.ui.datas_prj.setChecked(True)

    def allplan_apn(self):

        version_allplan = self.ui.version_list.currentText()

        if version_allplan in self.allplan.version_datas:

            version_obj = self.allplan.version_datas[version_allplan]

        else:

            version_obj = self.allplan.allplan_paths

        if isinstance(version_obj, AllplanPaths):

            path_default = version_obj.prj_path

            shortcuts_list = [version_obj.etc_cat_path,
                              version_obj.std_cat_path,
                              version_obj.prj_path,
                              version_obj.tmp_path]
        else:
            path_default = ""

            shortcuts_list = list()

        a = self.tr("Fichier")

        file_path = browser_file(parent=self.asc,
                                 title=application_title,
                                 registry=[app_setting_file, "path_catalog_apn"],
                                 datas_filters={f"{a} Allplan": [".apn", ".prj"]},
                                 shortcuts_list=shortcuts_list,
                                 current_path=path_default,
                                 default_path=self.ui.datas_path.text(),
                                 use_setting_first=True)

        if file_path == "":
            return

        # todo à modifier

        version_allplan = self.ui.version_list.currentText()

        if version_allplan not in self.allplan.version_datas:
            return

        version_obj = self.allplan.version_datas[version_allplan]

        if not isinstance(version_obj, AllplanPaths):
            return

        chemin_prj = version_obj.prj_path

        if chemin_prj == "":
            print("widget_nouveau -- allplan_apn -- erreur : dossier prj inconnu")
            return

        dossier_prj_tps = get_real_path_of_apn_file(file_path, chemin_prj)

        if dossier_prj_tps == "":
            print("widget_nouveau -- allplan_apn -- erreur : dossier temporaire prj vide")
            return

        verification = verification_projet(dossier_prj_tps)

        if not verification:
            msg(titre=self.windowTitle(),
                message=self.tr("L'ensemble des paramètres de ce projet est en STD."),
                icone_avertissement=True)

            return

        self.ui.datas_path.setText(dossier_prj_tps)

    @staticmethod
    def a___________________convert______():
        pass

    def bdd_browser(self):

        version_allplan = self.ui.version_list.currentText()

        if version_allplan in self.allplan.version_datas:

            version_obj = self.allplan.version_datas[version_allplan]

        else:

            version_obj = self.allplan.allplan_paths

        if isinstance(version_obj, AllplanPaths):

            path_default = version_obj.std_path

            shortcuts_list = [version_obj.etc_cat_path,
                              version_obj.std_cat_path,
                              version_obj.prj_path,
                              version_obj.tmp_path]

        else:
            path_default = ""

            shortcuts_list = list()

        get_bdd_paths(shortcuts_list=shortcuts_list, short_list=True)

        a = self.tr("Fichier")
        b = self.tr("Bible externe")

        datas_filters = {b: [".DBF", ".ARA", ".KAT", ".XML"],
                         f"{a} DBF": [".DBF"],
                         f"{a} ARA": [".ARA"],
                         f"{a} KAT": [".KAT"],
                         f"{a} XML": [".XML"]}

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[app_setting_file, "path_catalog_import"],
                                 datas_filters=datas_filters,
                                 shortcuts_list=shortcuts_list,
                                 current_path=self.ui.bdd_path.text(),
                                 default_path=path_default,
                                 use_setting_first=True)

        if file_path == "":
            return

        self.recherche_valide(file_path=file_path, add=True, message=True)

    def recherche_valide(self, file_path: str, add=False, message=False) -> bool:

        if not isinstance(file_path, str):
            return False

        file_path = file_path.replace("/", "\\")

        detection_tool = BddTypeDetection()

        check = detection_tool.search_bdd_type(file_path=file_path)

        modifiers = QApplication.keyboardModifiers()

        if not check:
            return False

        bdd_type = detection_tool.bdd_type
        bdd_title = detection_tool.bdd_title
        file_path = detection_tool.file_path

        if bdd_type == bdd_type_bcm_c and modifiers != Qt.ControlModifier:

            if message:
                msg(titre=self.windowTitle(),
                    message=self.tr("Cette base de données est une base composant."),
                    icone_critique=True)
            return False

        if bdd_type == bdd_type_xml:
            if message:
                msg(titre=self.windowTitle(),
                    message=self.tr("Cette base de données est déjà un Smart-Catalogue."),
                    icone_critique=True)
            return False

        if bdd_type not in convert_valid_bdd:
            return False

        if not add:
            return True

        folder = find_folder_path(file_path)

        settings_save_value(file_name=app_setting_file, key_name="path_catalog_import", value=folder)

        return self.convert_define_data(bdd_type=bdd_type, title=bdd_title, file_path=file_path)

    def convert_define_data(self, bdd_type: str, title: str, file_path: str) -> bool:

        if bdd_type not in convert_valid_bdd:
            self.bdd_type = ""
            self.ui.bt_creation.setEnabled(False)
            return False

        self.bdd_type = bdd_type

        self.ui.bdd_path.setText(file_path)
        self.ui.bt_creation.setEnabled(True)

        title_current = self.ui.cat_name.text()

        if title_current.startswith(self.tr("Nouveau catalogue")) and title != "":
            self.ui.cat_name.setText(title)
            self.catalog_title_change()

        return True

    @staticmethod
    def a___________________creation______():
        pass

    def catalog_new_creation_start(self):

        catalog_name = self.ui.cat_name.text().strip()
        catalog_folder = self.ui.save_path.text()

        # -----------------

        catalog_path = f"{catalog_folder}{catalog_name}.xml"

        verification = self.catalog_title_change()

        if verification != "Ok":
            msg(titre=self.windowTitle(),
                message=verification,
                icone_critique=True)
            return

        # -----------------

        version_allplan = self.ui.version_list.currentText()
        user_folder = self.ui.datas_path.text()

        attribute_current = attribut_default_obj.get_value(index=self.ui.attribute_list.currentIndex())

        attribute_old = attribut_default_obj.current

        # -----------------

        if self.new:

            if not self.catalog.catalog_save_ask():
                return

            # ------

            self.close()

            # ------

            if not self.catalog.catalog_create_new(catalog_folder=catalog_folder,
                                                   catalog_name=catalog_name,
                                                   user_folder=user_folder,
                                                   version_allplan=version_allplan,
                                                   attribute_number=attribute_current):
                return

            # ------

            attribut_default_obj.set_current(number=attribute_current)

            # ------

            self.catalog.catalog_load_start(catalog_path=catalog_path)

            return

        # -----------------

        if self.modify:

            if (self.allplan.version_allplan_current == self.ui.version_list.currentText() and
                    self.allplan.catalog_user_path == self.ui.datas_path.text() and
                    attribute_old == attribute_current):

                self.close()

                return

            # ------

            if not self.catalog.catalog_create_path_file(catalog_folder=self.catalog.catalog_folder,
                                                         catalog_name=self.catalog.catalog_name,
                                                         user_data_path=user_folder,
                                                         allplan_version=version_allplan,
                                                         attribute_default=attribute_current):
                return

            # ------

            attribut_default_obj.set_current(number=attribute_current)

            # ------

            if attribute_old != attribute_current:

                if not self.catalog.catalog_save_action(exlcude_default_attribute=attribute_old):
                    return

            elif not self.catalog.catalog_save_ask():
                return

            # ------

            self.close()

            # ------

            self.catalog.catalog_load_start(catalog_path=self.catalog.catalog_path)

            return

        # -----------------

        if self.convert_bdd:

            if not self.catalog.catalog_save_ask():
                return

            # ------

            self.close()

            # ------

            a = self.tr("Attention, une mauvaise configuration de la version d'Allplan et du chemin de données")
            b = self.tr("peut entrainer la perte d'informations ou la corruption du catalogue")
            c = self.tr("Voulez-vous continuer")

            if msg(titre=self.windowTitle(),
                   message=f"{a} \n{b}.\n{c} ?",
                   type_bouton=QMessageBox.Ok | QMessageBox.Cancel,
                   icone_avertissement=True) == QMessageBox.Cancel:
                return

            if not self.catalog.catalog_create_path_file(catalog_folder=catalog_folder,
                                                         catalog_name=catalog_name,
                                                         user_data_path=user_folder,
                                                         allplan_version=version_allplan,
                                                         attribute_default=attribute_current):
                return

            # ------

            chemin_bdd = self.ui.bdd_path.text()

            # ------

            attribut_default_obj.set_current(number=attribute_current)

            # ------

            if self.bdd_type in [bdd_type_allmetre_a, bdd_type_allmetre_e, bdd_type_bcm, bdd_type_bcm_c]:
                self.catalog_convert_action(catalog_path=catalog_path, loader="BCM", chemin_bdd=chemin_bdd)
                return

            # ------

            if self.bdd_type == bdd_type_kukat:
                self.catalog_convert_action(catalog_path=catalog_path, loader="KUKAT", chemin_bdd=chemin_bdd)
                return

            # ------

            if self.bdd_type == bdd_type_nevaris:
                self.catalog_convert_action(catalog_path=catalog_path, loader="NEVARIS", chemin_bdd=chemin_bdd)
                return

    def catalog_convert_action(self, catalog_path: str, loader: str, chemin_bdd: str):

        self.catalog.catalog_load_start(catalog_path=catalog_path, loader=loader, chemin_bdd=chemin_bdd)

        move_window_tool(widget_parent=self.asc, widget_current=self.asc.loading, always_center=True)

        self.asc.loading.launch_show(self.tr("Enregistrement du catalogue ..."))

        CatalogSave(self.asc, self.catalog, self.allplan)

        self.asc.loading.hide()

        self.asc.modification_mod = False

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj != self.ui.version_list:
            return super().eventFilter(obj, event)

        if event.type() == QEvent.Wheel:
            if not self.ui.version_list.hasFocus():
                event.ignore()
                return True
            else:
                event.accept()
                return super().eventFilter(obj, event)

        return super().eventFilter(obj, event)

    def dragEnterEvent(self, event: QDragEnterEvent):

        if not self.convert_bdd:
            event.ignore()
            return

        if not event.mimeData().hasUrls():
            event.ignore()
            return

        urls = event.mimeData().urls()

        if len(urls) != 1:
            event.ignore()
            return

        url = urls[0]
        file_path = url.toLocalFile()

        if self.recherche_valide(file_path=file_path, add=False):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):

        if not self.convert_bdd:
            event.ignore()
            return

        if not event.mimeData().hasUrls():
            event.ignore()
            return

        urls = event.mimeData().urls()

        if len(urls) != 1:
            event.ignore()
            return

        url = urls[0]
        file_path = url.toLocalFile()

        if self.recherche_valide(file_path=file_path, add=False):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):

        if not self.convert_bdd:
            event.ignore()
            return

        if not event.mimeData().hasUrls():
            event.ignore()
            return

        urls = event.mimeData().urls()

        if len(urls) != 1:
            event.ignore()
            return

        url = urls[0]
        file_path = url.toLocalFile()

        if self.recherche_valide(file_path=file_path, add=True, message=True):
            event.accept()
        else:
            event.ignore()

    @staticmethod
    def a___________________end______():
        pass


class CatalogUpdaterWidget(QWidget):

    def __init__(self, asc, allplan, catalogue):
        super().__init__()

        # ---------------------------------------
        # BOITE DE DIALOGUE
        # ---------------------------------------
        self.ui = Ui_CatalogUpdate()
        self.ui.setupUi(self)

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.catalogue = catalogue
        self.allplan: AllplanDatas = allplan

        # ---------------------------------------
        # Read Settings
        # ---------------------------------------

        update_setting = settings_read(update_setting_file)

        self.ismaximized_on = update_setting.get("ismaximized_on", False)
        self.resize(update_setting.get("width", 400), update_setting.get("height", 500))

        self.order = 0

        # ---------------------------------------
        # Model + Filters
        # ---------------------------------------

        self.projects_models = QStandardItemModel()

        self.projects_filter = QSortFilterProxyModel()
        self.projects_filter.setSourceModel(self.projects_models)
        self.projects_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.projects_filter.setSortLocaleAware(True)

        self.ui.projects_table.setModel(self.projects_filter)
        self.ui.projects_table.selectionModel().selectionChanged.connect(self.update_buttons_manage)

        get_look_tableview(self.ui.projects_table)

        # ---------------------------------------
        # Signals sort
        # ---------------------------------------

        header = self.ui.projects_table.horizontalHeader()

        if header is not None:
            header.sortIndicatorChanged.connect(self.order_changed)

        # ---------------------------------------
        # Signals
        # ---------------------------------------

        self.ui.update_none.clicked.connect(self.select_none)
        self.ui.update_select.clicked.connect(self.select_all)

        self.ui.update_search.textChanged.connect(self.projects_filter.setFilterRegExp)

        self.ui.update_launch.clicked.connect(self.update_action)
        self.ui.update_quit.clicked.connect(self.close)

    def update_show(self):

        # ------------------------------
        # Read settings
        # ------------------------------

        update_setting = settings_read(update_setting_file)

        # ----- Order

        order = update_setting.get("order", 0)

        if not isinstance(order, int):
            self.order = 0
        else:
            self.order = order

        # ----- last_catalog + Search

        last_catalog = update_setting.get("catalog", "")

        if last_catalog != self.catalogue.catalog_path:
            search = ""
        else:
            search = update_setting.get("search", "")

            if not isinstance(search, str):
                search = ""

        # ------------------------------
        # Read config
        # ------------------------------

        config_datas = settings_read(update_config_file)

        if not isinstance(config_datas, dict):
            selected_paths_list = list()
        else:
            selected_paths_list = config_datas.get(self.catalogue.catalog_path, list())

        selected_items_list = list()

        # ----- Clearing

        self.projects_models.clear()

        # ------------------------------
        # ----- initialise model
        # ------------------------------

        self.projects_models.setHorizontalHeaderLabels([self.tr("Nom projet"), ""])

        self.ui.projects_table.setColumnHidden(col_save_chemin, True)

        header = self.ui.projects_table.horizontalHeader()

        if header is not None:
            if header.height() != 24:
                header.setFixedHeight(24)

        # ------------------------------
        # ----- checking allplan_paths
        # ------------------------------

        if not isinstance(self.allplan.allplan_paths, AllplanPaths):
            msg(titre=self.windowTitle(),
                message=self.tr("Le Dossier PRJ n'est pas valide"),
                details="AllplanPath error")
            return

        # ------------------------------
        # ----- search path Project.Dat.xml
        # ------------------------------

        if self.allplan.allplan_paths.workgroup and self.allplan.allplan_paths.net_path != "":

            lck_folder_path = self.allplan.allplan_paths.net_path
            project_file = f"{lck_folder_path}Project.Dat.xml"

            if not os.path.exists(project_file):
                lck_folder_path = self.allplan.allplan_paths.prj_path

        else:
            lck_folder_path = self.allplan.allplan_paths.prj_path

        project_file = f"{lck_folder_path}Project.Dat.xml"

        if not os.path.exists(project_file):
            txt = self.tr("n'a pas été trouvé")
            msg(titre=self.windowTitle(),
                message=f"Project.Dat.xml {txt}")
            return

        # ------------------------------
        # ----- search lck list
        # ------------------------------

        check_number = self.allplan.allplan_paths.allplan_version_int >= 2025

        if check_number:
            lck_list = get_project_use(prj_path=lck_folder_path)
        else:
            lck_list = list()

        # ------------------------------
        # ----- analyze Project.Dat.xml
        # ------------------------------

        project_list = list()

        try:
            tree = etree.parse(project_file)

            root = tree.getroot()

            for project in root:

                # ---------------
                # Number
                # ---------------

                number_search = project.find("Number")

                if number_search is None:
                    print("allplan_manage -- get_projects_dict -- number_search is None")
                    continue

                number_val = number_search.text

                if not isinstance(number_val, str):
                    print("allplan_manage -- get_projects_dict -- not isinstance(number_val, str)")
                    continue

                if not number_val.isnumeric():
                    print("allplan_manage -- get_projects_dict -- not number_val.isnumeric()")
                    continue

                if number_val == "0":
                    continue

                # ---------------
                # Name
                # ---------------

                name_search = project.find("Name")

                if name_search is None:
                    print("allplan_manage -- get_projects_dict -- name_search is None")
                    continue

                name_val = name_search.text

                if not isinstance(name_val, str):
                    print("allplan_manage -- get_projects_dict -- not isinstance(name_val, str)")
                    continue

                # ---------------
                # Project path
                # ---------------

                project_path = f"{self.allplan.allplan_paths.prj_path}{name_val}.prj"

                if not os.path.exists(project_path):
                    print("allplan_manage -- get_projects_dict -- not os.path.exists(project_path)")
                    continue

                if project_path in project_list:
                    print("allplan_manage -- get_projects_dict -- not os.path.exists(project_path)")
                    continue

                if os.path.isfile(project_path):
                    project_path = get_real_path_of_apn_file(file_path=project_path,
                                                             prj_path=self.allplan.allplan_paths.prj_path,
                                                             show_msg=False)

                    if project_path == "":
                        continue

                if not project_path.endswith("\\"):
                    project_path += "\\"

                # ---------------
                # Catalog path
                # ---------------

                folder_cat_path = f"{project_path}Xml\\SmartCatalog\\"

                if not os.path.exists(folder_cat_path):
                    folder_cat_path = f"{project_path}Xml\\AVACatalog\\"

                    if not os.path.exists(folder_cat_path):
                        continue

                # ---------------
                # Catalog check
                # ---------------
                catalog_path = f"{folder_cat_path}{self.catalogue.catalog_name}.xml"

                if catalog_path == self.catalogue.catalog_path:
                    continue

                if not os.path.exists(catalog_path):
                    continue

                # ---------------
                # Lck check
                # ---------------

                used = check_number and number_val in lck_list

                qs_name = QStandardItem(name_val)
                qs_name.setToolTip(catalog_path)

                if used:
                    qs_name.setData("used", user_data_type)

                self.projects_models.appendRow([qs_name, QStandardItem(catalog_path)])

                if catalog_path in selected_paths_list:
                    selected_items_list.append(qs_name)

        except Exception as error:
            msg(titre=self.windowTitle(),
                message=self.tr("Une erreur est survenue."),
                details=f"{error}")
            return

            # ----- add search same as last time

        if search != "":
            self.ui.update_search.setText(search)

        # ----- select items same as last time

        if len(selected_items_list) != 0:

            qitemselection = QItemSelection()

            nb_column = self.projects_filter.columnCount()

            for qs in selected_items_list:

                if not isinstance(qs, QStandardItem):
                    continue

                qm = qs.index()

                if not qm_check(qm):
                    continue

                qm_filtre = self.projects_filter.mapFromSource(qm)

                if qm_filtre is None:
                    continue

                current_row: int = qm_filtre.row()

                qm_dbu = self.projects_filter.index(current_row, 0)
                qm_fin = self.projects_filter.index(current_row, nb_column - 1)

                qitemselection.select(qm_dbu, qm_fin)

            self.ui.projects_table.selectionModel().select(qitemselection,
                                                           QItemSelectionModel.Select | QItemSelectionModel.Rows)

            # ----- sort same as last time

            if header is not None:
                header.setSortIndicator(0, self.order)
                self.ui.projects_table.sortByColumn(0, self.order)
        else:
            self.select_all()

        if self.projects_models.rowCount() == 0:
            msg(titre=self.windowTitle(),
                message=self.tr("Aucun projet n'utilise ce catalogue."))
            return

        move_window_tool(widget_parent=self.asc, widget_current=self)

        if self.ismaximized_on:

            self.showMaximized()
        else:
            self.show()

        self.ui.projects_table.setFocus()

    @staticmethod
    def a___________________order_change______():
        pass

    def order_changed(self, _, order: int):

        if not isinstance(order, int):
            return

        if order == Qt.DescendingOrder:
            order_code = 1
        else:
            order_code = 0

        self.order = order_code

    @staticmethod
    def a___________________boutons_______________():
        pass

    def select_all(self):
        self.ui.projects_table.selectAll()
        self.ui.projects_table.setFocus()

    def select_none(self):
        self.ui.projects_table.clearSelection()
        self.ui.projects_table.setFocus()

    def update_buttons_manage(self):

        nb_items_selected = len(self.ui.projects_table.selectionModel().selectedRows())
        selection_active = nb_items_selected != 0

        self.ui.update_launch.setEnabled(selection_active)
        self.ui.update_select.setEnabled(selection_active)

    @staticmethod
    def a___________________update_______________():
        pass

    def update_action(self):

        liste_items_selected = self.ui.projects_table.selectionModel().selectedRows(col_save_chemin)

        if len(liste_items_selected) == 0:
            self.close()

        # ------------------------------

        errors = ""
        nb_catalogs = len(liste_items_selected)

        if nb_catalogs == 0:
            msg(titre=self.windowTitle(),
                message=self.tr("Aucun catalogue n'a été mis à jour."),
                icone_valide=True)

            self.close()
            return

        ignore = list()

        txt_error = self.tr("Problème de sauvegarde du catalogue dans le prj")

        for qm_current in liste_items_selected:

            # ------------------------------
            # Analyse de la sélection
            # ------------------------------

            if not qm_check(qm_current):
                print("catalog -- maj -- qmodelindex non valide")
                continue

            qm_project_name = self.projects_filter.index(qm_current.row(), col_save_nom)

            if not qm_check(qm_project_name):
                print("catalog -- maj -- qm_nom_projet non valide")
                continue

            qm_project_path = self.projects_filter.index(qm_current.row(), col_save_chemin)

            if not qm_check(qm_project_path):
                print("catalog -- maj -- qm_project_path non valide")
                continue

            current_name: str = qm_project_name.data()
            current_catalog_path: str = qm_project_path.data()

            used = qm_project_name.data(user_data_type)

            if used == "used":
                ignore.append(current_name)
                continue

            current_catalog_folder_path: str = find_folder_path(qm_current.data())

            if current_catalog_folder_path == "":
                print("catalog -- maj -- dossier_catalogue_save est vide")
                continue

            # ------------------------------
            # Copie du catalogue
            # ------------------------------

            current_xml_folder = current_catalog_folder_path.replace("AVACatalog\\", "")
            current_xml_folder = current_xml_folder.replace("SmartCatalog\\", "")

            current_backup_folder = f"{current_xml_folder}backup\\"

            if current_catalog_folder_path == "" or self.catalogue.catalog_name == "" or current_backup_folder == "":
                continue

            if not make_backup(chemin_dossier=current_catalog_folder_path,
                               fichier=self.catalogue.catalog_name,
                               extension=".xml",
                               dossier_sauvegarde=current_backup_folder,
                               nouveau=True):
                errors += f'{txt_error} {current_name}\n'
                continue

            try:
                shutil.copyfile(self.catalogue.catalog_path, current_catalog_path)

            except Exception:

                errors += f'{txt_error} : {current_name}\n'
                continue

            # ------------------------------
            # Copie display
            # ------------------------------

            current_setting_folder = f"{current_catalog_folder_path}ASC_settings\\"
            current_display_file = f"{current_setting_folder}{self.catalogue.catalog_name}_display.xml"

            current_setting_backup_folder = f"{current_setting_folder}backup\\"

            if current_setting_folder == "" or current_setting_backup_folder == "":
                continue

            if os.path.exists(current_setting_backup_folder):
                make_backup(chemin_dossier=current_setting_folder,
                            fichier=f"{self.catalogue.catalog_name}_display",
                            extension=".xml",
                            dossier_sauvegarde=current_setting_backup_folder,
                            nouveau=True)

            try:
                shutil.copyfile(self.catalogue.catalog_setting_display_file, current_display_file)

            except OSError as error:
                print("maj_tous_les_catalogues -- "
                      f"Problème de copie fichier affichage dans le prj {current_name}\n{error}")

            # ------------------------------
            # Copie path
            # ------------------------------

            current_setting_file = f"{current_setting_folder}{self.catalogue.catalog_name}_path.ini"

            if os.path.exists(current_setting_file):
                make_backup(chemin_dossier=current_setting_folder,
                            fichier=f"{self.catalogue.catalog_name}_path",
                            extension=".ini",
                            dossier_sauvegarde=current_setting_backup_folder,
                            nouveau=True)

            try:
                shutil.copyfile(self.catalogue.catalog_setting_path_file, current_setting_file)

            except OSError as error:
                print(f"maj_tous_les_catalogues -- Problème de copie fichier ini dans le prj {current_name}\n{error}")

        if errors != "":
            msg(titre=self.windowTitle(),
                message=self.tr("Une erreur est survenue."),
                icone_avertissement=True,
                details=errors)

            self.close()
            return

        if len(ignore) != 0:
            txt1 = self.tr("Certains catalogues ont été ignoré parce qu'ils sont en cours d'utilisation.")
            txt2 = self.tr("Allplan vous proposera de le mettre à jour")

            msg(titre=self.windowTitle(),
                message=f"{txt1}\n{txt2}",
                icone_valide=True,
                details=ignore)

            self.close()
            return

        msg(titre=self.windowTitle(),
            message=self.tr("Mise à jour de catalogues terminée"),
            infos="catalogs_updated",
            icone_valide=True)

        self.close()

    @staticmethod
    def a___________________fermeture______():
        pass

    def update_save_setting(self):

        datas_config = settings_read(file_name=update_setting_file)

        datas_config["catalog"] = self.catalogue.catalog_path
        datas_config["search"] = self.ui.update_search.text()
        datas_config["order"] = self.order

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True

                settings_save(file_name=model_setting_file, config_datas=datas_config)
                return

        datas_config["height"] = self.size().height()
        datas_config["width"] = self.size().width()
        datas_config["ismaximized_on"] = False

        settings_save(file_name=update_setting_file, config_datas=datas_config)

    def update_save_config(self):

        # ----- read original config

        config_datas_original = settings_read(update_config_file)

        # ----- check if catalog path exists

        config_datas = dict()

        for catalog_path, paths_list in config_datas_original.items():
            if not os.path.exists(catalog_path):
                continue

            config_datas[catalog_path] = paths_list

        # ----- search selected items

        selected_items_list = self.ui.projects_table.selectionModel().selectedRows()

        selected_paths_list = list()

        if len(selected_items_list) == 0:
            settings_save(update_config_file, config_datas)
            return

        for qm_name in selected_items_list:

            if not qm_check(qm_name):
                continue

            current_row = qm_name.row()

            qm_path = self.projects_filter.index(current_row, col_save_chemin)

            if not qm_check(qm_path):
                continue

            current_path = qm_path.data()

            if current_path is None:
                continue

            selected_paths_list.append(current_path)

        # ----- update list for the current catalog

        config_datas[self.catalogue.catalog_path] = selected_paths_list

        # ----- save settings

        settings_save(update_config_file, config_datas)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_action()

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):

        self.update_save_setting()
        self.update_save_config()

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass
