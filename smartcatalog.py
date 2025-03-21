#!/usr/bin/python3
# -*- coding: utf-8 -*

import os.path

from attribute_add import AttributesWidget
from attributes_loader import AttributesDetailLoader
from backup_restore import BackupRestore
from bar_action import ActionBar
from bar_main import MainBar
from bar_search import SearchBar
from catalog import CatalogUpdaterWidget, WidgetCatalogNew
from catalog_manage import *
from convert_manage import ExportExcel
from error_report import ErrorReport
from formula import Formula
from formula_favorite import FormulaFavorite
from formulaire import Formulaire
from gestion_update import GestionUpdate
from help import HelpWidget
from ktlgwidget import KtlgWidget
from library import Library
from main_datas import application_name, application_version
from message import LoadingSplash
from models import Models
from tools import MyContextMenu, get_real_path_of_apn_file, verification_catalogue_correct, help_pressed
from tools import afficher_message as msg
from tools import get_look_treeview, find_global_point, copy_to_clipboard
from tools import settings_read, settings_save, settings_verifications, browser_file
from tools import taille_police, open_folder, open_file, convertir_langue
from ui_main_windows import Ui_MainWindow
from vob import VobWidget


class Mainwindow(QMainWindow):
    langue_change = pyqtSignal()

    ui_resized = pyqtSignal()

    def __init__(self):
        super().__init__()

        # loading MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ismaximized_on = False
        self.langue = "EN"

        self.actionbar_size = "2"

        settings_verifications()

        self.attributes_order = 0
        self.attributes_order_col = 0
        self.attributes_order_custom = False
        self.attributes_order_list = list()

        self.search_recent = list()

        self.application_chargement_donnees()

        # ---------------------------------------
        # UI loading
        # ---------------------------------------

        self.loading = LoadingSplash()
        self.formulaire_widget = None

        # ---------------------------------------
        # ALLPLAN
        # ---------------------------------------

        self.allplan = AllplanDatas(self.langue)

        # ---------------------------------------
        # Catalogue
        # ---------------------------------------

        self.catalog = CatalogDatas(self)

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

        # ---------------------------------------
        # Loading Help
        # ---------------------------------------

        self.help_tooltip = self.tr("F1 pour ouvrir l'aide")

        self.help_widget = HelpWidget(asc=self)

        # ---------------------------------------
        # Attributs
        # ---------------------------------------

        self.attributes_detail_loader = AttributesDetailLoader(self)

        # ---------------------------------------
        # CHARGEMENT Nouveau catalogue
        # ---------------------------------------

        self.new_catalog_widget = WidgetCatalogNew(self)

        # ---------------------------------------
        # CHARGEMENT catalogue
        # ---------------------------------------

        catalog_path = settings_get(file_name=app_setting_file, info_name="path_catalog")

        if catalog_path != "" and os.path.exists(catalog_path):

            self.catalog.catalog_load_start(catalog_path=catalog_path)

        else:

            self.catalog.catalog_load_start(catalog_path=self.allplan.catlog_default_file_path)

        # ---------------------------------------
        # CHARGEMENT Ajout Attribut
        # ---------------------------------------

        self.attributes_widget = AttributesWidget(self)

        # ---------------------------------------
        # CHARGEMENT bible externe
        # ---------------------------------------

        self.library_widget = Library(self)

        self.catalog.close_library_signal.connect(self.library_widget.tabs_reset_all)

        # ---------------------------------------
        # CHARGEMENT Recherche
        # ---------------------------------------

        self.search_bar = SearchBar(self)

        # ---------------------------------------
        # CHARGEMENT Options attribut
        # ---------------------------------------

        self.models_widget = Models(self)

        # ---------------------------------------
        # CHARGEMENT favoris formule
        # ---------------------------------------

        self.formula_fav_widget = FormulaFavorite(self)

        # ---------------------------------------
        # CREATEUR DE FORMULES
        # ---------------------------------------

        self.formula_editor_widget = Formula(self)
        self.widget_formule_visible = False

        # ---------------------------------------
        # CHARGEMENT Hiérarchie
        # ---------------------------------------

        self.action_bar = ActionBar(self)

        # ---------------------------------------
        # CHARGEMENT Détails
        # ---------------------------------------

        get_look_treeview(self.ui.attributes_detail)

        # ---------------------------------------
        # CHARGEMENT Catalogue
        # ---------------------------------------

        self.main_bar = MainBar(asc=self, new_catalog_widget=self.new_catalog_widget)

        # ---------------------------------------
        # Loading Error Report
        # ---------------------------------------

        self.report_error_widget = ErrorReport(asc=self)

        # ---------------------------------------
        # Loading VOB
        # ---------------------------------------

        self.vob_widget = VobWidget(asc=self)

        # ---------------------------------------
        # Loading Ktlg
        # ---------------------------------------

        self.ktlg_widget = KtlgWidget(asc=self)

        # ---------------------------------------

        self.ui.hierarchy.cat_model.dataChanged.connect(self.catalog.catalog_modif_manage)

        self.ui.hierarchy.expanded.connect(self.catalog.catalog_modif_manage)

        # self.ui.hierarchy.collapsed.connect(self.action_bar.plier_enfants)
        self.ui.hierarchy.collapsed.connect(self.catalog.catalog_modif_manage)

        self.ui.attributes_detail.installEventFilter(self)

        self.ui.statusbar.customContextMenuRequested.connect(self.status_menu_show)

        self.action_bar.hierarchie_selection_change()

        self.ui.menu_bt.clicked.connect(self.main_menu_show)
        self.ui.actionbar.customContextMenuRequested.connect(self.actionbar_menu_show)

        self.catalog_updater_widget = CatalogUpdaterWidget(self, self.allplan, self.catalog)

        # ---------- MATERIAL ----------

        self.material_style = self.ui.material.styleSheet()

        # ----------

        self.material_1 = self.ui.material_add_bt.styleSheet()
        self.ui.material_add_bt.installEventFilter(self)

        # ----------

        self.material_2 = self.ui.material_list_bt.styleSheet()
        self.ui.material_list_bt.installEventFilter(self)

        # ---------- COMPONENT ----------

        self.component_style = self.ui.component.styleSheet()

        # ----------

        self.component_1 = self.ui.component_add_bt.styleSheet()
        self.ui.component_add_bt.installEventFilter(self)

        # ----------

        self.component_2 = self.ui.component_list_bt.styleSheet()
        self.ui.component_list_bt.installEventFilter(self)

        # ---------- LINK ----------

        self.link_style = self.ui.link.styleSheet()

        # ----------

        self.link_1 = self.ui.link_add_bt.styleSheet()
        self.ui.link_add_bt.installEventFilter(self)

        # ----------

        self.link_2 = self.ui.link_list_bt.styleSheet()
        self.ui.link_list_bt.installEventFilter(self)

        # ---------- ATTRIBUTE ----------

        self.attribute_style = self.ui.attribute.styleSheet()

        # ----------

        self.attribute_1 = self.ui.attribute_add_bt.styleSheet()
        self.ui.attribute_add_bt.installEventFilter(self)

        # ----------

        self.attribute_2 = self.ui.attribute_list_bt.styleSheet()
        self.ui.attribute_list_bt.installEventFilter(self)

        # ---------- PASTE ----------

        self.paste_style = self.ui.paste.styleSheet()

        # ----------

        self.paste_1 = self.ui.paste_bt.styleSheet()
        self.ui.paste_bt.installEventFilter(self)

        # ----------

        self.paste_2 = self.ui.paste_list_bt.styleSheet()
        self.ui.paste_list_bt.installEventFilter(self)

        # ----------

        self.catalog.change_made = False

        # ---------------------------------------
        # Update
        # ---------------------------------------

        if special_version:
            self.gestion_update = GestionUpdate(self)

            test = sys.argv[0]

            if test != 'C:\\Stockage\\GIT\\GitHub\\smartest2\\smartcatalog.py':
                self.gestion_update.check_update(show_message=False)

            # if self.langue == "FR":

            # data = settings_get(app_setting_file, "message")
            #
            # if data != application_version:
            #     msg(titre=f"{application_title} -- Nouveautés",
            #         message="<center>"
            #                 "Désormais, vous pouvez effectuer un <b>glisser-déposer</b><br>"
            #                 "des éléments des <b>bibles externes vers le catalogue.</b><br>"
            #                 "<br>"
            #                 "Nouveau menu pour la liste des fichiers récents avec filtres<br>"
            #                 "<br>"
            #                 "Lors d’une recherche de formules contenant des erreurs,<br>"
            #                 "après correction d’une formule utilisée à plusieurs endroits,<br>"
            #                 "il vous sera proposé de les corriger toutes automatiquement.<br>"
            #                 "<br>"
            #                 "Pour toute suggestion d’amélioration ou pour signaler un bug,<br>"
            #                 "n’hésitez pas à nous écrire à : <b>support.fr@allplan.com")
            #
            # settings_save_value(app_setting_file, "message", application_version)

        else:
            self.gestion_update = None

    @staticmethod
    def a___________________application_chargement_donnees______():
        pass

    def application_chargement_donnees(self):

        app_config = settings_read(app_setting_file)

        if not isinstance(app_config, dict):
            app_config = dict(app_setting_datas)

        # -----------

        largeur_app = app_config.get('width', app_setting_datas.get('width', 1250))

        if not isinstance(largeur_app, int):
            largeur_app = app_setting_datas.get('width', 1250)

        # -----------

        hauteur_app = app_config.get('height', app_setting_datas.get('height', 875))

        if not isinstance(hauteur_app, int):
            hauteur_app = app_setting_datas.get('height', 875)

        # -----------

        position_x = app_config.get('posx', app_setting_datas.get('posx', 0))

        if not isinstance(position_x, int):
            position_x = app_setting_datas.get('posx', 0)

        # -----------

        position_y = app_config.get('posy', app_setting_datas.get('posx', 0))

        if not isinstance(position_y, int):
            position_y = app_setting_datas.get('posx', 0)

        # -----------

        ismaximized_on = app_config.get('ismaximized_on', app_setting_datas.get('ismaximized_on', False))

        if not isinstance(ismaximized_on, bool):
            ismaximized_on = app_setting_datas.get('ismaximized_on', False)

        self.ismaximized_on = ismaximized_on

        # ---------------------------------------
        # resize and move main windows
        # ---------------------------------------

        liste_ecrans = app.screens()
        cp = QDesktopWidget().availableGeometry().center()
        ecran_largeur = 0
        ecran_hauteur = 0

        liste_position_ecran = list()
        dict_ecran = dict()

        for ecran in liste_ecrans:
            ecran: QScreen

            ecran_pos_x = ecran.availableGeometry().x()

            liste_position_ecran.append(ecran_pos_x)
            dict_ecran[ecran_pos_x] = ecran

        liste_position_ecran.sort()

        for position_ecran in liste_position_ecran:

            if position_x >= position_ecran:
                ecran_analyser = dict_ecran[position_ecran]

                cp = ecran_analyser.availableGeometry().center()

                ecran_largeur = ecran_analyser.size().width()
                ecran_hauteur = ecran_analyser.size().height()

            elif position_x < position_ecran:
                break

        if largeur_app > ecran_largeur:
            largeur_app = ecran_largeur

        if position_y > ecran_hauteur:
            position_y = 0
        elif position_y < 0:
            position_y = 0

        hauteur_av_position = hauteur_app + position_y + 71

        if hauteur_av_position > ecran_hauteur:
            position_y = ecran_hauteur - hauteur_app - 71

            if position_y < 0:
                hauteur_app = hauteur_app + position_y

        self.resize(largeur_app, hauteur_app)

        qr = self.frameGeometry()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # ---------------------------------------
        # Language app
        # ---------------------------------------

        langue_actuelle = app_config.get('language', app_setting_datas.get('language', language_default))

        self.langue = convertir_langue(langue_actuelle)

        self.translation_loading()
        self.translation_changed_emit()

        # ---------------------------------------
        # gestion du bouton : liste des catalogues ouverts
        # ---------------------------------------

        self.open_list_manage(settings_list(cat_list_file))

        # ---------------------------------------
        # Action bar
        # ---------------------------------------

        actionbar_size = app_config.get("actionbar_size", app_setting_datas.get('actionbar_size', "2"))

        if not isinstance(actionbar_size, str):
            actionbar_size = app_setting_datas.get('actionbar_size', "2")

        self.actionbar_size = actionbar_size

        self.actionbar_change_icon_size(self.actionbar_size)

        # ---------------------------------------
        # attributes order
        # ---------------------------------------

        attributes_order = app_config.get("attributes_order", app_setting_datas.get('attributes_order', 0))

        if attributes_order not in [0, 1]:
            attributes_order = app_setting_datas.get('attributes_order', 0)

        self.attributes_order = attributes_order

        # ---------------------------------------

        attributes_order_col = app_config.get("attributes_order_col", app_setting_datas.get('attributes_order_col', 0))

        if attributes_order_col not in [0, 1]:
            attributes_order_col = app_setting_datas.get('attributes_order_col', 0)

        self.attributes_order_col = attributes_order_col

        # ---------------------------------------

        attributes_order_custom = app_config.get("attributes_order_custom",
                                                 app_setting_datas.get('attributes_order_custom', False))

        if not isinstance(attributes_order_custom, bool):
            attributes_order_custom = app_setting_datas.get('attributes_order_custom', False)

        self.attributes_order_custom = attributes_order_custom

        # ---------------------------------------

        search_recent = app_config.get("search_recent",
                                       app_setting_datas.get('search_recent', list()))

        if not isinstance(search_recent, list):
            search_recent = app_setting_datas.get('search_recent', list())

        self.search_recent = search_recent

    @staticmethod
    def a___________________gestion_langue______():
        pass

    def langue_changer(self, langue_choisie: str):
        """
        Changer langue
        :param langue_choisie: langue choisie
        :return: None
        """

        langue_choisie = convertir_langue(langue_choisie)

        if self.langue == langue_choisie:
            return

        settings_save_value(app_setting_file, "language", langue_choisie)

        self.langue = langue_choisie
        self.allplan.langue = langue_choisie

        self.langue_changer_action()
        return

    def langue_changer_action(self):
        """
        traduction des textes et chargement du catalogue
        :return: None
        """

        self.formula_widget_close()

        if self.catalog.change_made:
            if not self.catalog.catalog_save_ask():
                return

        self.translation_loading()

        self.catalog.clipboard_clear_all()

        self.allplan.allplan_retranslate()
        self.translation_changed_emit()

        self.catalog.catalog_load_start(catalog_path=self.catalog.catalog_path)

        self.allplan.autocompletion_refresh_signal.emit()

    def translation_loading(self):

        trad2 = f"{asc_folder_path}translation\\{self.langue.lower()}.qm"

        if not os.path.exists(trad2):
            trad2 = f"{asc_folder_path}translation\\en.qm"

        app.removeTranslator(translator)
        translator.load(trad2, QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        app.installTranslator(translator)

    def translation_changed_emit(self):

        self.ui.retranslateUi(self)
        self.langue_change.emit()

    @staticmethod
    def a___________________main_menu______():
        pass

    def main_menu_show(self):

        menu = MyContextMenu(tooltips_visible=False)
        menu.help_request.connect(self.help_request)

        menu.add_action(qicon=get_icon(catalog_icon),
                        title=self.tr("Nouveau catalogue"),
                        action=self.main_bar.catalogue_nouveau,
                        short_link=help_cat_new_cat)

        menu.add_action(qicon=get_icon(convert_bdd_icon),
                        title=self.tr("Importer une base de données"),
                        action=self.main_bar.catalogue_importer,
                        short_link=help_cat_convert)

        menu.addSeparator()

        menu.add_action(qicon=get_icon(open_catalog_icon),
                        title=self.tr("Ouvrir un catalogue"),
                        action=self.main_bar.catalog_open_browse,
                        short_link=help_cat_open_cat)

        cat_open_sub_menu = MyContextMenu(qicon=get_icon(recent_icon),
                                          title=self.tr("Catalogues récents"))

        liste_fichiers_ouverts = settings_list(cat_list_file)

        liste_fichiers = [chemin_fichier for chemin_fichier in liste_fichiers_ouverts
                          if os.path.exists(chemin_fichier) and len(chemin_fichier) > 2]

        if len(liste_fichiers) != 0:

            # liste_fichiers_ouverts.sort()

            for path_file in reversed(liste_fichiers):
                projet = self.menu_titre_projet(path_file)

                cat_open_sub_menu.add_action(qicon=get_icon(recent_icon),
                                             title=projet,
                                             action=lambda val=path_file: self.main_bar.catalog_open_file(val),
                                             tooltips=path_file,
                                             short_link=help_cat_recent)

        menu.addMenu(cat_open_sub_menu)

        menu.addSeparator()

        menu.add_action(qicon=get_icon(save_icon),
                        title=self.tr("Enregistrer"),
                        action=self.catalog.catalog_save,
                        short_link=help_cat_save)

        menu.add_action(qicon=get_icon(save_as_icon),
                        title=self.tr("Enregistrer sous"),
                        action=self.main_bar.catalog_save_as,
                        short_link=help_cat_save_as)

        menu.addSeparator()

        menu.add_action(qicon=get_icon(options_icon),
                        title=self.tr("Modifier le chemin de données"),
                        action=self.main_bar.catalogue_modifier_parametres,
                        short_link=help_cat_settings)

        menu.add_action(qicon=get_icon(update_cat_icon),
                        title=self.tr("Mettre à jour les catalogues"),
                        action=self.catalogue_update,
                        short_link=help_cat_update)

        if self.backup_restore_menu():
            menu.add_action(qicon=get_icon(refresh_icon),
                            title=self.tr("Restaurer une sauvegarde"),
                            action=self.backup_restore_show,
                            short_link=help_cat_restore)

        menu.addSeparator()

        # ----------------------------------------------------------------------------

        qicon = get_icon(f":/Images/{self.langue}.png")

        langue_sub_menu = MyContextMenu(qicon=qicon,
                                        title=self.tr("Changer de langue"),
                                        short_link=help_interface_langue,
                                        tooltips_visible=False)

        for language, title in language_title.items():
            langue_sub_menu.add_action(qicon=get_icon(f":/Images/{language}.png"),
                                       title=title,
                                       action=lambda val=language: self.langue_changer(val))

        menu.addMenu(langue_sub_menu)

        # ----------------------------------------------------------------------------

        tools_sub_menu = MyContextMenu(qicon=get_icon(tool_icon),
                                       title=self.tr("Outils"),
                                       tooltips_visible=False)

        tools_sub_menu.add_action(qicon=get_icon(excel_icon),
                                  title=self.tr("Exporter vers Excel"),
                                  action=self.export_excel)

        # ----------------------------------------------------------------------------

        tools_sub_menu.addSeparator()

        tools_sub_menu.add_action(qicon=get_icon(asc_icon),
                                  title=self.tr("Ouvrir le dossier de l'application"),
                                  action=self.dossier_asc)

        tools_sub_menu.add_action(qicon=get_icon(asc_icon),
                                  title=self.tr("Ouvrir le dossier des exports"),
                                  action=self.dossier_export_asc)

        tools_sub_menu.add_action(qicon=get_icon(asc_icon),
                                  title=self.tr("Ouvrir le dossier des paramètres"),
                                  action=self.dossier_settings_asc)

        tools_sub_menu.addSeparator()

        # ----------------------------------------------------------------------------

        tools_sub_menu.add_action(qicon=get_icon(open_icon),
                                  title=self.tr("Ouvrir le dossier du catalogue"),
                                  action=self.dossier_cat)

        tools_sub_menu.add_action(qicon=get_icon(folder_icon),
                                  title=self.tr("Ouvrir le dossier de données choisi"),
                                  action=self.dossier_user)

        tools_sub_menu.addSeparator()

        tools_sub_menu.add_action(qicon=get_icon(open_text_editor_icon),
                                  title=self.tr("Ouvrir le catalogue dans un éditeur de texte"),
                                  action=self.fichier_cat)

        tools_sub_menu.add_action(qicon=get_icon(open_text_editor_icon),
                                  title=self.tr("Ouvrir le fichier des unités"),
                                  action=self.fichier_unite)

        menu.addMenu(tools_sub_menu)

        # ----------------------------------------------------------------------------

        menu_allplan = MyContextMenu(qicon=get_icon(allplan_icon),
                                     title="Allplan",
                                     tooltips_visible=False)

        menu_allplan.add_action(qicon=get_icon(refresh_icon),
                                title=self.tr("Rafraichir les données Allplan"),
                                action=self.allplan_refresh,
                                short_link=help_allplan_refresh)

        menu_allplan.add_action(qicon=get_icon(error_icon),
                                title=self.tr("Rapport d'erreurs Allplan"),
                                action=self.report_error,
                                short_link=help_allplan_error)

        menu_allplan.addSeparator()

        menu_allplan.add_action(qicon=get_icon(tool_icon),
                                title=self.tr("Editer fichier VOB"),
                                action=self.vob_editor_show)

        menu_allplan.add_action(qicon=get_icon(tool_icon),
                                title=self.tr("Bibliothèque assignée"),
                                action=self.ktlg_editor_show)

        menu_allplan.addSeparator()

        menu_allplan.add_action(qicon=get_icon(":/Images/etc.png"),
                                title=self.tr("Personnaliser dossiers SmartCatalog"),
                                action=self.allplan.allplan_customize_folder_name_apply)

        menu_allplan.add_action(qicon=get_icon(reset_icon),
                                title=self.tr("Réinitialiser dossiers SmartCatalog"),
                                action=self.allplan.allplan_customize_folder_name_remove)

        menu_allplan.addSeparator()

        menu_allplan.add_action(qicon=get_icon(open_icon),
                                title=self.tr("Ouvrir le dossier STD"),
                                action=self.ouvrir_std)

        menu_allplan.add_action(qicon=get_icon(open_icon),
                                title=self.tr("Ouvrir le dossier PRJ"),
                                action=self.ouvrir_prj)

        menu_allplan.addSeparator()

        menu_allplan.add_action(qicon=get_icon(open_icon),
                                title=self.tr("Ouvrir le dossier PRG"),
                                action=self.ouvrir_prg)

        menu_allplan.add_action(qicon=get_icon(open_icon),
                                title=self.tr("Ouvrir le dossier ETC"),
                                action=self.ouvrir_etc)

        menu_allplan.addSeparator()

        menu_allplan.add_action(qicon=get_icon(open_icon),
                                title=self.tr("Ouvrir le dossier USR"),
                                action=self.ouvrir_usr)

        menu_allplan.add_action(qicon=get_icon(open_icon),
                                title=self.tr("Ouvrir le dossier TMP"),
                                action=self.ouvrir_tmp)

        menu.addMenu(menu_allplan)

        # ----------------------------------------------------------------------------

        datas_msg = {
            "attributes_update": self.tr("Afficher message : Attribut existant -> Mise à jour?"),

            "catalogs_updated": self.tr("Afficher message : Sauvegarde tous -> OK"),

            "hierarchy_delete_item": self.tr(
                "Afficher message : Hiérarchie = Demande avant suppression")}

        datas = settings_read(warning_setting_file)
        liste_avertissement_ok = list()

        for key, value in datas.items():

            if value != QMessageBox.Ok and value != QMessageBox.No and value != QMessageBox.Save:
                continue

            liste_avertissement_ok.append(key)

        if len(liste_avertissement_ok) != 0:

            menu.addSeparator()

            warning_sub_menu = MyContextMenu(qicon=get_icon(reset_icon),
                                             title=self.tr("Reset paramètres 'Ne plus afficher'"),
                                             tooltips_visible=False)

            for avertissement in liste_avertissement_ok:
                message = datas_msg.get(avertissement, None)

                if message is None:
                    continue

                warning_sub_menu.add_action(qicon=get_icon(delete_icon),
                                            title=message,
                                            action=lambda val=avertissement: self.settings_reset_param(val))
            menu.addMenu(warning_sub_menu)

        if special_version:
            menu.addSeparator()

            menu.add_action(qicon=get_icon(update_app_icon),
                            title="Rechercher mise à jour",
                            action=self.app_update)

            menu.add_action(qicon=get_icon(outlook_icon),
                            title="Contacter support",
                            action=self.envoyer_message)

        menu.addSeparator()

        menu.add_action(qicon=get_icon(information_icon),
                        title=self.tr("A propos"),
                        action=self.app_infos)

        menu.add_action(qicon=get_icon(help_icon),
                        title=self.tr("Aide"),
                        action=self.app_aide)

        menu.addSeparator()

        menu.add_action(qicon=get_icon(exit_icon),
                        title=self.tr("Quitter"),
                        action=self.app_quitter)

        menu.exec_(find_global_point(self.ui.menu_bt))

    def actionbar_menu_show(self, point: QPoint):

        menu = MyContextMenu(tooltips_visible=False)

        menu.add_action(qicon=None,
                        title=self.tr("Petit icône"),
                        action=lambda val="1": self.actionbar_change_icon_size(val))

        menu.add_action(qicon=None,
                        title=self.tr("Moyenne icône"),
                        action=lambda val="2": self.actionbar_change_icon_size(val))

        menu.add_action(qicon=None,
                        title=self.tr("Grande icône"),
                        action=lambda val="3": self.actionbar_change_icon_size(val))

        menu.add_action(qicon=None,
                        title=self.tr("Très grande icône"),
                        action=lambda val="4": self.actionbar_change_icon_size(val))

        menu.exec_(self.ui.actionbar.mapToGlobal(point))

    def actionbar_change_icon_size(self, size: str):

        self.actionbar_size = size

        current_font = self.ui.display_title.font()

        if size == "1":
            # size2 * 0.8333
            icon_size = QSize(20, 20)
            title_height = 13
            icon_width = 33
            title_width = icon_width * 2
            sub_menu_icon_size = QSize(13, 13)

            current_font.setPointSize(6)

        elif size == "3":
            # size2 * 1.1666
            icon_size = QSize(28, 28)
            title_height = 19
            icon_width = 47
            title_width = icon_width * 2
            sub_menu_icon_size = QSize(19, 19)

            current_font.setPointSize(10)

        elif size == "4":
            # size2 * 1.333
            icon_size = QSize(32, 32)
            title_height = 22
            icon_width = 54
            title_width = icon_width * 2
            sub_menu_icon_size = QSize(21, 21)

            current_font.setPointSize(11)

        else:
            # size2 == default
            icon_size = QSize(24, 24)
            title_height = 16
            icon_width = 40
            title_width = icon_width * 2
            sub_menu_icon_size = QSize(16, 16)

            current_font.setPointSize(8)

        # --------------------------------
        # Display
        # --------------------------------

        self.ui.display_title.setMinimumSize(QSize(title_width, title_height))

        self.ui.expand_all_bt.setIconSize(icon_size)
        self.ui.expand_all_bt.setMinimumWidth(icon_width)

        self.ui.collapse_all_bt.setIconSize(icon_size)
        self.ui.collapse_all_bt.setMinimumWidth(icon_width)

        # --------------------------------
        # Move
        # --------------------------------

        self.ui.move_title.setMinimumSize(QSize(title_width, title_height))

        self.ui.move_up_bt.setIconSize(icon_size)
        self.ui.move_up_bt.setMinimumWidth(icon_width)

        self.ui.move_down_bt.setIconSize(icon_size)
        self.ui.move_down_bt.setMinimumWidth(icon_width)

        # --------------------------------
        # Add
        # --------------------------------

        self.ui.add_title.setMinimumHeight(title_height)

        self.ui.folder_add_bt.setIconSize(icon_size)
        self.ui.folder_add_bt.setMinimumWidth(icon_width)

        self.ui.material_add_bt.setIconSize(icon_size)
        self.ui.material_add_bt.setMinimumWidth(icon_width)
        self.ui.material_list_bt.setIconSize(sub_menu_icon_size)
        self.ui.material_list_bt.setMaximumHeight(title_height)

        self.ui.component_add_bt.setIconSize(icon_size)
        self.ui.component_add_bt.setMinimumWidth(icon_width)
        self.ui.component_list_bt.setIconSize(sub_menu_icon_size)
        self.ui.component_list_bt.setMaximumHeight(title_height)

        self.ui.link_add_bt.setIconSize(icon_size)
        self.ui.link_add_bt.setMinimumWidth(icon_width)
        self.ui.link_list_bt.setIconSize(sub_menu_icon_size)
        self.ui.link_list_bt.setMaximumHeight(title_height)

        self.ui.attribute_add_bt.setIconSize(icon_size)
        self.ui.attribute_add_bt.setMinimumWidth(icon_width)
        self.ui.attribute_list_bt.setIconSize(sub_menu_icon_size)
        self.ui.attribute_list_bt.setMaximumHeight(title_height)

        # --------------------------------
        # Edit
        # --------------------------------

        self.ui.edit_title.setMinimumHeight(title_height)

        self.ui.del_bt.setIconSize(icon_size)
        self.ui.del_bt.setMinimumWidth(icon_width)

        self.ui.cut_bt.setIconSize(icon_size)
        self.ui.cut_bt.setMinimumWidth(icon_width)

        self.ui.copy_bt.setIconSize(icon_size)
        self.ui.copy_bt.setMinimumWidth(icon_width)

        self.ui.paste_bt.setIconSize(icon_size)
        self.ui.paste_bt.setMinimumWidth(icon_width)

        self.ui.paste_list_bt.setIconSize(sub_menu_icon_size)
        self.ui.paste_list_bt.setMaximumHeight(title_height)

        # --------------------------------
        # Models
        # --------------------------------

        self.ui.model_title.setMinimumSize(QSize(title_width, title_height))

        self.ui.model_bt.setIconSize(icon_size)
        self.ui.model_bt.setMinimumWidth(icon_width)

        self.ui.model_add_bt.setIconSize(icon_size)
        self.ui.model_add_bt.setMinimumWidth(icon_width)

        # --------------------------------
        # Libraries
        # --------------------------------

        self.ui.library_title.setMinimumSize(QSize(title_width, title_height))

        self.ui.library_bt.setIconSize(icon_size)
        self.ui.library_bt.setMinimumWidth(icon_width)

        # --------------------------------
        # Libraries
        # --------------------------------

        self.ui.end_title.setMinimumHeight(title_height)

    @staticmethod
    def menu_titre_projet(chemin) -> str:

        nom_catalogue = os.path.basename(chemin)

        if ".prj" not in chemin:
            return nom_catalogue

        try:
            start = chemin.rfind("\\", 0, chemin.find(".prj"))
            end = chemin.find(".prj")

            if start == -1:
                return nom_catalogue
            elif end == 3:
                return nom_catalogue
            else:
                nom_fichier = chemin[start + 1:end]
                return f"{nom_fichier} --> {nom_catalogue}"

        except ValueError:
            return nom_catalogue

    @staticmethod
    def a___________________boutons______():
        pass

    def boutons_catalogue(self, all_items=None, param=False, save=False, maj_cat=False):

        if all_items is None:
            self.ui.parameters_bt.setEnabled(param)
            self.ui.save_bt.setEnabled(save)
            self.ui.update_cat_bt.setEnabled(maj_cat)
        else:
            self.ui.parameters_bt.setEnabled(all_items)
            self.ui.save_bt.setEnabled(all_items)
            self.ui.update_cat_bt.setEnabled(all_items)

    def boutons_hierarchie_pliage(self, expand_all=False, collapse_all=False):

        self.ui.expand_all_bt.setEnabled(expand_all)
        self.ui.collapse_all_bt.setEnabled(collapse_all)

    def boutons_hierarchie_move(self, monter=False, descendre=False):

        self.ui.move_up_bt.setEnabled(monter)
        self.ui.move_down_bt.setEnabled(descendre)

    def boutons_hierarchie_add(self, folder=False, material=False, component=False, link=False, attribute=False):

        self.ui.folder_add_bt.setEnabled(folder)

        self.ui.material_add_bt.setEnabled(material)
        self.ui.material_list_bt.setEnabled(material)

        self.ui.component_add_bt.setEnabled(component)
        self.ui.component_list_bt.setEnabled(component)

        self.ui.link_add_bt.setEnabled(link)
        self.ui.link_list_bt.setEnabled(link)

        self.ui.attribute_add_bt.setEnabled(attribute)
        self.ui.attribute_list_bt.setEnabled(attribute)

    def boutons_hierarchie_model(self, model_show=True, model_add=False):

        self.ui.model_bt.setEnabled(model_show)

        self.ui.model_add_bt.setEnabled(model_add)

    def boutons_hierarchie_edition(self, ele_type=None, delete=True, cut=True, copy=True):

        if ele_type is None:
            self.ui.del_bt.setEnabled(False)
            self.ui.cut_bt.setEnabled(False)
            self.ui.copy_bt.setEnabled(False)
            return

        if ele_type == folder_code:
            del_id = help_folder_del
            copy_id = help_folder_copy

        elif ele_type == material_code:
            del_id = help_material_del
            copy_id = help_material_copy

        elif ele_type == component_code:
            del_id = help_component_del
            copy_id = help_component_copy

        elif ele_type == link_code:
            del_id = help_link_del
            copy_id = help_link_copy

        elif ele_type == attribute_code:
            del_id = help_attribute_del
            copy_id = help_attribute_copy

        else:
            del_id = ""
            copy_id = ""

        self.ui.del_bt.setObjectName(f"delete_{ele_type}")
        self.ui.del_bt.setEnabled(delete)
        self.ui.del_bt.setWhatsThis(del_id)

        self.ui.cut_bt.setObjectName(f"cut_{ele_type}")
        self.ui.cut_bt.setEnabled(cut)
        self.ui.cut_bt.setWhatsThis(copy_id)

        self.ui.copy_bt.setObjectName(f"copy_{ele_type}")
        self.ui.copy_bt.setEnabled(copy)
        self.ui.copy_bt.setWhatsThis(copy_id)

    def boutons_hierarchie_coller(self, ele_type=None):

        if ele_type is None:
            self.ui.paste_bt.setEnabled(False)
            self.ui.paste_list_bt.setEnabled(False)
            self.ui.paste_bt.setWhatsThis("")
            self.ui.paste_list_bt.setWhatsThis("")
            return

        if ele_type == folder_code:
            paste_id = help_folder_paste

        elif ele_type == material_code:
            paste_id = help_material_paste

        elif ele_type == component_code:
            paste_id = help_component_paste

        elif ele_type == link_code:
            paste_id = help_link_paste

        elif ele_type == attribute_code:
            paste_id = help_attribute_paste

        else:
            paste_id = ""

        self.ui.paste_bt.setWhatsThis(paste_id)
        self.ui.paste_list_bt.setWhatsThis(paste_id)

        if ele_type != attribute_code:

            type_actuel = self.hierarchie_coller_recherche_type()

            if type_actuel == "":
                self.ui.paste_bt.setEnabled(False)
                self.ui.paste_list_bt.setEnabled(False)
                return

            if self.ui.search_error_bt.isChecked() or self.ui.search_bt.isChecked():
                self.ui.paste_bt.setEnabled(False)
                self.ui.paste_list_bt.setEnabled(False)
                return

        self.ui.paste_bt.setObjectName(f"paste_{ele_type}")
        self.ui.paste_bt.setEnabled(True)

        self.ui.paste_list_bt.setEnabled(True)

    def hierarchie_coller_recherche_type(self):

        if self.catalog.clipboard_current == "":
            return ""

        liste_selection_qstandarditem = self.ui.hierarchy.get_qs_selection_list()

        nb_selections = len(liste_selection_qstandarditem)

        if nb_selections == 0:
            if self.catalog.clipboard_folder.len_datas() != 0:
                return folder_code
            return ""

        qstandarditem: Folder = liste_selection_qstandarditem[0]

        liste_compatibles = qstandarditem.get_type_possibilities()

        if len(liste_compatibles) == 0:
            return ""

        if not isinstance(qstandarditem, MyQstandardItem):
            return ""

        ele_type = qstandarditem.data(user_data_type)

        current_pp = list()

        if self.catalog.attribut_coller_recherche(liste_selection_qstandarditem, False):
            current_pp.append(attribute_code)

        if folder_code in liste_compatibles:
            nb_dossier_copier = self.catalog.clipboard_folder.len_datas()
            if nb_dossier_copier != 0:
                current_pp.append(folder_code)

        if material_code in liste_compatibles:
            nb_ouvrage_copier = self.catalog.clipboard_material.len_datas()
            if nb_ouvrage_copier != 0:
                current_pp.append(material_code)

        if component_code in liste_compatibles:
            nb_composant_copier = self.catalog.clipboard_component.len_datas()
            if nb_composant_copier != 0:
                current_pp.append(component_code)

        if link_code in liste_compatibles:
            nb_lien_copier = self.catalog.clipboard_link.len_datas()
            if nb_lien_copier != 0:
                current_pp.append(link_code)

        if len(current_pp) == 0:
            return ""

        if self.catalog.clipboard_current in current_pp:
            return self.catalog.clipboard_current

        if ele_type in current_pp:
            return ele_type

        return current_pp[0]

    def boutons_hierarchie_bible(self, bible_show=True):

        self.ui.library_bt.setEnabled(bible_show)

    @staticmethod
    def a___________________boutons_gestion______():
        pass

    def buttons_manage(self):

        # --------------------
        # Si aucun catalogue
        # --------------------

        if self.catalog.catalog_path == "":
            self.boutons_catalogue()

            self.boutons_hierarchie_pliage()
            self.boutons_hierarchie_move()
            self.boutons_hierarchie_add()
            self.boutons_hierarchie_model(model_show=False)
            self.boutons_hierarchie_edition()
            self.boutons_hierarchie_coller()
            self.boutons_hierarchie_bible(bible_show=False)

            self.boutons_recherche(actif=False)
            return

        nb_items_filtre = self.ui.hierarchy.model().rowCount()

        # --------------------
        # Si le filtre est vide
        # --------------------

        if nb_items_filtre == 0:
            self.boutons_catalogue(param=True)

            self.boutons_hierarchie_pliage()
            self.boutons_hierarchie_move()
            self.boutons_hierarchie_add(folder=True)
            self.boutons_hierarchie_model()
            self.boutons_hierarchie_edition()
            self.boutons_hierarchie_coller()
            self.boutons_hierarchie_bible(bible_show=True)

            self.boutons_recherche(actif=False)
            return

        if self.ui.search_error_bt.isChecked() or self.ui.search_bt.isChecked():

            qs = self.ui.hierarchy.get_current_qs()

            if qs is not None:
                ele_type = qs.data(user_data_type)
            else:
                ele_type = None

            self.boutons_hierarchie_pliage(expand_all=True, collapse_all=True)
            self.boutons_hierarchie_move()
            self.boutons_hierarchie_add(attribute=True)
            self.boutons_hierarchie_model(model_add=True)
            self.boutons_hierarchie_edition(ele_type=ele_type)
            self.boutons_hierarchie_coller()
            self.boutons_hierarchie_bible(bible_show=False)

            return

        # --------------------
        # Si aucune selection
        # --------------------

        liste_selection_qs = self.ui.hierarchy.get_qs_selection_list()
        nb_selections = len(liste_selection_qs)

        if nb_selections != 0:
            qs = liste_selection_qs[0]

            if not isinstance(qs, MyQstandardItem):
                nb_selections = 0
        else:
            qs = None

        if nb_selections == 0:

            self.boutons_catalogue(all_items=True)

            self.boutons_hierarchie_pliage(expand_all=nb_items_filtre != 0, collapse_all=nb_items_filtre != 0)
            self.boutons_hierarchie_move()
            self.boutons_hierarchie_add(folder=True)
            self.boutons_hierarchie_model()
            self.boutons_hierarchie_edition()

            if self.catalog.clipboard_folder.len_datas() != 0:
                self.boutons_hierarchie_coller(folder_code)
            else:
                self.boutons_hierarchie_coller()

            self.boutons_hierarchie_bible(bible_show=True)
            self.boutons_recherche()

            return

        # --------------------
        # Recherche possibilités
        # --------------------

        monter, descendre = self.boutons_monter_descendre(liste_selection_qs)

        ele_type = qs.data(user_data_type)

        liste_compatibles = qs.get_type_possibilities()

        folder_add = folder_code in liste_compatibles
        material_add = material_code in liste_compatibles
        component_add = component_code in liste_compatibles
        link_add = link_code in liste_compatibles

        attribut_add = ele_type == material_code or ele_type == component_code

        model_add = attribut_add and len(liste_selection_qs) == 1 and self.ui.attributes_detail.count() > 2

        # --------------------
        # généralités
        # --------------------

        self.boutons_catalogue(all_items=True)

        self.boutons_hierarchie_pliage(expand_all=True, collapse_all=True)

        self.boutons_hierarchie_move(monter=monter, descendre=descendre)

        self.boutons_hierarchie_add(folder=folder_add,
                                    material=material_add,
                                    component=component_add,
                                    link=link_add,
                                    attribute=attribut_add)

        self.boutons_hierarchie_model(model_show=True, model_add=model_add)

        self.boutons_hierarchie_edition(ele_type)

        self.boutons_hierarchie_coller(ele_type)

        self.boutons_hierarchie_bible(bible_show=True)

        self.boutons_recherche()

    def attribut_clic(self):

        type_ele, supprimer, couper, copier = self.bouton_attribut()

        self.boutons_hierarchie_edition(type_ele, supprimer, couper, copier)

        if self.catalog.clipboard_attribute.len_datas() == 0:
            self.boutons_hierarchie_coller(None)
        else:
            self.boutons_hierarchie_coller(attribute_code)

        if self.library_widget.isVisible():
            if self.library_widget.isMinimized():
                self.library_widget.showNormal()
            elif not self.library_widget.isActiveWindow():
                self.library_widget.raise_()

            return

        if self.formula_editor_widget.isVisible():
            if self.formula_editor_widget.isMinimized():
                self.formula_editor_widget.showNormal()
            elif not self.formula_editor_widget.isActiveWindow():
                self.formula_editor_widget.raise_()

    @staticmethod
    def a___________________boutons_gestion_recherche______():
        pass

    @staticmethod
    def bouton_replier(liste_selection_qstandarditem) -> bool:

        replier = False

        if len(liste_selection_qstandarditem) > 0:

            qstandarditem: MyQstandardItem = liste_selection_qstandarditem[0]

            if qstandarditem is None:
                return replier

            type_element = qstandarditem.data(user_data_type)

            liste_types_enfants = qstandarditem.get_children_type_list()

            if type_element == folder_code:
                replier = folder_code in liste_types_enfants or material_code in liste_types_enfants

            elif type_element == material_code:
                replier = component_code in liste_types_enfants

        return replier

    def boutons_monter_descendre(self, liste_selection_qstandarditem) -> tuple:
        """
        Permet de déterminer si les boutons monter, descendre doivent être activer ou pas
        :param liste_selection_qstandarditem: selections actuelles
        :return: bt_monter(bool), bt_descendre(bool)
        :rtype: tuple
        """

        if len(liste_selection_qstandarditem) == 0:
            return False, False

        # --------------
        # Analyse parents / row indexes
        # --------------

        select_dict = dict()

        for qs_selected in liste_selection_qstandarditem:

            if not isinstance(qs_selected, (Folder, Material, Component, Link)):
                continue

            qs_parent = self.ui.hierarchy.get_parent(qs=qs_selected)

            if not isinstance(qs_parent, QStandardItem):
                continue

            parent_id = id(qs_parent)

            row_current = qs_selected.row()

            if parent_id in select_dict:

                row_list = select_dict[parent_id]["row_list"]

                row_list.append(row_current)

            else:

                if qs_parent == self.ui.hierarchy.cat_model.invisibleRootItem():

                    child_list = self.ui.hierarchy.get_root_children_type_list()

                else:

                    child_list = qs_parent.get_children_type_list()

                select_dict[parent_id] = {"row_list": [row_current],
                                          "child_count": len(child_list),
                                          "qs_parent": qs_parent}

        bt_up = False
        bt_down = False

        for datas in select_dict.values():

            if not isinstance(datas, dict):
                continue

            qs_parent = datas.get("qs_parent", None)

            if not isinstance(qs_parent, QStandardItem):
                continue

            if qs_parent == self.ui.hierarchy.cat_model.invisibleRootItem():

                qs_parent_top_index = 0

            else:

                qs_parent_top_index = qs_parent.get_insertion_index()

            row_list = datas.get("row_list", list())

            if not isinstance(row_list, list):
                continue

            parent_row_count_no_attribute = datas.get("child_count", 0)

            if not isinstance(parent_row_count_no_attribute, int):
                continue

            if parent_row_count_no_attribute == 0:
                continue

            if parent_row_count_no_attribute == len(row_list):
                continue

            # ----------------
            # Up
            # ----------------

            if not bt_up:

                row_list.sort()

                for index_list, current_row in enumerate(row_list):

                    if current_row == index_list + qs_parent_top_index:
                        continue

                    bt_up = True

                    break

            # ----------------
            # Down
            # ----------------

            if not bt_down:

                row_list.sort(reverse=True)

                for index_list, current_row in enumerate(row_list):

                    parent_row_count = qs_parent.rowCount()

                    if current_row == parent_row_count - 1 - index_list:
                        continue

                    bt_down = True

                    break

            if bt_down and bt_up:
                return True, True

        return bt_up, bt_down

    def bouton_expand_collapse(self):
        self.ui.hierarchy.header_manage()

    def open_list_manage(self, catalog_opened_list: list):

        nb_items = len(catalog_opened_list)

        if os.path.exists(f"{asc_folder_path}Catalogue - exemples\\2023\\CMI.xml"):
            self.ui.open_list_bt.setEnabled(True)
            return

        if nb_items >= 1:
            self.ui.open_list_bt.setEnabled(True)
            return

        self.ui.open_list_bt.setEnabled(False)

    def bouton_attribut(self) -> tuple:
        """
        analyse la possibilité de supprimer, couper, coller
        :return: type_element: str, supprimer: bool, couper: bool, coller: bool
        """

        if self.catalog.catalog_path == "":
            return attribute_code, False, False, False

        liste_selections_qstandarditem = self.ui.hierarchy.get_qs_selection_list()
        nb_selections = len(liste_selections_qstandarditem)

        if nb_selections == 0:
            return attribute_code, False, False, False

        liste_selection_detail = self.ui.attributes_detail.selectionModel().selectedRows()
        nb_details = len(liste_selection_detail)

        if nb_details == 0:
            return attribute_code, False, False, False

        for item in liste_selection_detail:

            if item.data(user_data_type) == type_unknown:
                return attribute_code, True, False, False

            index_row = item.row()

            if index_row > 1:
                return attribute_code, True, True, True

        return attribute_code, False, False, True

    def boutons_recherche(self, actif=None):

        if actif is None:
            if self.catalog.catalog_path == "" or self.ui.hierarchy.cat_model.rowCount() == 0:
                actif = False
            else:
                actif = True

        if not actif:
            self.ui.search_line.setEnabled(False)
            self.ui.search_bt.setEnabled(False)

            self.ui.search_error_bt.setEnabled(False)
            self.ui.search_replace_bt.setEnabled(False)
            return

        bt_search = not self.ui.search_error_bt.isChecked()
        bt_error = not self.ui.search_bt.isChecked()

        self.ui.search_bt.setEnabled(bt_search)
        self.ui.search_line.setEnabled(bt_search)

        self.ui.search_error_bt.setEnabled(bt_error)

        self.ui.search_replace_bt.setEnabled(bt_search and bt_error)

    @staticmethod
    def a___________________gestion_titre______():
        pass

    def catalog_load_title(self):
        """
        Permet d'afficher le titre de la hiérarchie
        :return: None
        """

        if self.catalog.catalog_path == "":
            self.setWindowTitle(application_title)
            self.ui.hierarchy.cat_model.setHorizontalHeaderItem(0, QStandardItem(""))
            return

        if os.path.exists(self.catalog.catalog_path):

            seconds = os.path.getmtime(self.catalog.catalog_path)
            date_complet_modif = datetime.fromtimestamp(seconds)

            date_modif = catalog_xml_date(current_language=self.langue, date_complet_modif=date_complet_modif)

            a = self.tr("Dernier enregistrement")
            texte_secondaire = f'{a} : {date_modif}'

        else:

            texte_secondaire = self.tr("Pas encore enregistré")

        if not help_mode:
            self.setWindowTitle(f"{application_title} -- {self.catalog.catalog_path} -- {texte_secondaire}")

    def catalogue_update(self):

        self.formula_widget_close()

        if not self.catalog.catalog_save_ask():
            return

        self.catalog_updater_widget.update_show()

    @staticmethod
    def a___________________backup_restore______():
        pass

    def backup_restore_menu(self) -> bool:

        backup_folder = f"{self.catalog.catalog_folder}backup\\"

        backup_filename_list = list()

        if not os.path.exists(backup_folder):
            return False

        file_list = glob.glob(f"{backup_folder}{self.catalog.catalog_name}*.xml")

        if len(file_list) == 0:
            return False

        for backup_path in file_list:

            if not isinstance(backup_path, str):
                print("smartcatalog -- backup_restore_menu -- not isinstance(backup_path, str)")
                continue

            filename = backup_path.replace(f"{backup_folder}{self.catalog.catalog_name}", "").replace(".xml", "")

            if "-" in filename:
                try:
                    indice_str = filename[-2:]
                    int(indice_str)
                except Exception:
                    continue

                if not os.path.exists(f"{backup_folder}{self.catalog.catalog_name} - {indice_str}.xml"):
                    continue
            else:

                if "00" in backup_filename_list:
                    continue

                indice_str = "00"

                if not os.path.exists(f"{backup_folder}{self.catalog.catalog_name}.xml"):
                    continue

            if indice_str in backup_filename_list:
                continue

            backup_filename_list.append(indice_str)

        if len(backup_filename_list) == 0:
            return False

        return True

    def allplan_refresh(self):

        self.formula_widget_close()

        if not self.catalog.catalog_save_ask():
            return

        self.catalog.catalog_load_start(catalog_path=self.catalog.catalog_path)

    def backup_restore_show(self):

        self.formula_widget_close()

        if not self.catalog.catalog_save_ask():
            return

        BackupRestore(asc=self,
                      catalog_folder=self.catalog.catalog_folder,
                      catalog_name=self.catalog.catalog_name,
                      langue=self.langue)

    @staticmethod
    def a___________________information______():
        pass

    def report_error(self):

        self.formula_widget_close()

        move_window_tool(widget_parent=self, widget_current=self.report_error_widget, always_center=True)
        self.report_error_widget.report_show()

    @staticmethod
    def dossier_asc():
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=asc_folder_path, show_msg=True)
            return

        open_folder(asc_folder_path)

    @staticmethod
    def dossier_export_asc():

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=asc_export_path, show_msg=True)
            return

        open_folder(asc_export_path)

    @staticmethod
    def dossier_settings_asc():
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=asc_settings_path, show_msg=True)
            return

        open_folder(asc_settings_path)

    def dossier_user(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.allplan.catalog_user_path, show_msg=True)
            return

        open_folder(self.allplan.catalog_user_path)

    def dossier_cat(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.catalog.catalog_folder, show_msg=True)
            return

        open_folder(self.catalog.catalog_folder)

    def fichier_cat(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.catalog.catalog_path, show_msg=True)
            return

        open_file(self.catalog.catalog_path)

    def fichier_unite(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.allplan.unit_file_path, show_msg=True)
            return

        open_file(self.allplan.unit_file_path)

    def vob_editor_show(self):

        allplan_paths = self.allplan.allplan_paths

        if not isinstance(allplan_paths, AllplanPaths):
            print("smartcatalog -- vob_editor_show -- not isinstance(allplan_paths, AllplanPaths)")
            return False

        vob_file = f"vob_{allplan_paths.allplan_country}.{allplan_paths.allplan_language}"

        vob_path = f"{allplan_paths.etc_path}{vob_file}"

        # if not os.path.exists(vob_path):
        #     msg(titre=self.tr("Editer fichier VOB"),
        #         message=self.tr("Le fichier VOB n'a pas été trouvé."))
        #     return False

        move_window_tool(widget_parent=self, widget_current=self.vob_widget, always_center=True)

        self.vob_widget.vob_show(file_path=vob_path)

    def ktlg_editor_show(self):

        allplan_paths = self.allplan.allplan_paths

        if not isinstance(allplan_paths, AllplanPaths):
            print("smartcatalog -- ktlg_editor_show -- not isinstance(allplan_paths, AllplanPaths)")
            return False

        if self.allplan.allplan_is_runnig():
            msg(titre=self.tr("Bibliothèque assignée"),
                message=self.tr("Veuillez fermer Allplan avant de lancer cette fonction."),
                icone_avertissement=True)
            return False

        # ------

        ktlg_path = f"{allplan_paths.usr_path}Local\\ktlg.xml"

        if not os.path.exists(ktlg_path):
            msg(titre=self.tr("Bibliothèque assignée"),
                message=self.tr("Le fichier n'a pas été trouvé."))
            return False

        # ------

        if self.catalog.catalog_name == "":
            msg(titre=self.tr("Bibliothèque assignée"),
                message=self.tr("Une erreur est survenue."))
            return False

        # ------

        move_window_tool(widget_parent=self, widget_current=self.ktlg_widget.light_widget, always_center=True)

        self.ktlg_widget.ktlg_light_show(file_path=ktlg_path, catalog_name=self.catalog.catalog_name)

    @staticmethod
    def a___________________export______():
        pass

    def export_excel(self):

        self.formula_widget_close()

        b = self.tr("Fichier")

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [asc_export_path,
                              self.allplan.allplan_paths.std_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.usr_path]
        else:

            shortcuts_list = list()

        chemin_fichier = browser_file(parent=self,
                                      title=application_title,
                                      registry=[library_setting_file, "path_excel"],
                                      shortcuts_list=shortcuts_list,
                                      datas_filters={f"{b} Excel": [".xlsx"]},
                                      current_path=asc_export_path,
                                      default_path="",
                                      use_setting_first=True,
                                      use_save=True)

        if chemin_fichier is None:
            return

        if chemin_fichier == "":
            return

        move_window_tool(widget_parent=self, widget_current=self.loading, always_center=True)

        self.loading.launch_show(self.tr("Exporter vers Excel"))

        ExportExcel(self.allplan, self.ui.hierarchy.cat_model, chemin_fichier)

        self.loading.hide()

    @staticmethod
    def a___________________allplan______():
        pass

    def ouvrir_std(self):

        if not isinstance(self.allplan.allplan_paths, AllplanPaths):
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.allplan.allplan_paths.std_path, show_msg=True)
            return

        open_folder(self.allplan.allplan_paths.std_path)

    def ouvrir_prj(self):

        if not isinstance(self.allplan.allplan_paths, AllplanPaths):
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.allplan.allplan_paths.prj_path, show_msg=True)
            return

        open_folder(self.allplan.allplan_paths.prj_path)

    def ouvrir_prg(self):

        if not isinstance(self.allplan.allplan_paths, AllplanPaths):
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.allplan.allplan_paths.prg_path, show_msg=True)
            return

        open_folder(self.allplan.allplan_paths.prg_path)

    def ouvrir_etc(self):

        if not isinstance(self.allplan.allplan_paths, AllplanPaths):
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.allplan.allplan_paths.etc_path, show_msg=True)
            return

        open_folder(self.allplan.allplan_paths.etc_path)

    def ouvrir_usr(self):

        if not isinstance(self.allplan.allplan_paths, AllplanPaths):
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.allplan.allplan_paths.usr_path, show_msg=True)
            return

        open_folder(self.allplan.allplan_paths.usr_path)

    def ouvrir_tmp(self):

        if not isinstance(self.allplan.allplan_paths, AllplanPaths):
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.allplan.allplan_paths.tmp_path, show_msg=True)
            return

        open_folder(self.allplan.allplan_paths.tmp_path)

    @staticmethod
    def a___________________reset______():
        pass

    def settings_reset_param(self, avertissement: str):

        settings_save_value(file_name=warning_setting_file, key_name=avertissement, value=0)

        msg(titre=application_title,
            message=self.tr("La remise à zéro du paramètre choisi est terminée"))

    def app_infos(self):

        self.formula_widget_close()

        b = self.tr("Version actuelle")
        c = self.tr("Application créée par")

        msg(titre=application_title,
            message=f"<center><br>{b} : {application_version}<br><br>"
                    f"{c} MAUGER Jean-françois<br>"
                    "Copyright (c) ALLPLAN GmbH - All rights reserved<br>")

    def app_aide(self):

        if not help_mode:
            help_path = f"{asc_folder_path}help\\Mode d'emploi.pdf"

            if not os.path.exists(help_path):
                msg(titre=application_title,
                    message=self.tr("Aide non disponible."))
                return

            subprocess.Popen([help_path], shell=True)
            return

        self.formula_widget_close()

        self.help_widget.help_show()

    @staticmethod
    def a___________________quitter______():
        pass

    def app_quitter(self):
        self.close()

    @staticmethod
    def a___________menu_____________():
        return

    def status_menu_show(self, point: QPoint):

        menu = MyContextMenu()

        if self.allplan.catalog_user_path != "":
            menu.add_title(title=self.tr("Chemin de données"))

            menu.add_action(qicon=get_icon(options_icon),
                            title=self.tr("Modifier le chemin de données"),
                            action=self.main_bar.catalogue_modifier_parametres)

            menu.add_action(qicon=get_icon(open_icon),
                            title=self.tr("Ouvrir le chemin de données"),
                            action=self.dossier_user)

        if self.catalog.catalog_path != "":
            menu.add_title(title=self.tr("Catalogue"))

            menu.add_action(qicon=get_icon(open_icon),
                            title=self.tr("Ouvrir le dossier du catalogue"),
                            action=self.dossier_cat)

            menu.add_action(qicon=get_icon(open_text_editor_icon),
                            title=self.tr("Ouvrir le catalogue"),
                            action=self.fichier_cat)

        menu.exec_(self.ui.statusbar.mapToGlobal(point))

    @staticmethod
    def a___________________formulaire______():
        pass

    def envoyer_message(self):

        self.formula_widget_close()

        self.formulaire_widget = Formulaire()

        move_window_tool(widget_parent=self, widget_current=self.formulaire_widget, always_center=True)

    @staticmethod
    def a___________________help______():
        pass

    def help_request(self, short_link: str):

        if not help_mode:
            return

        self.formula_widget_close()
        self.help_widget.help_show(short_link=short_link)

    @staticmethod
    def a___________________update______():
        pass

    def app_update(self):

        self.formula_widget_close()
        self.gestion_update.check_update(show_message=True)

    @staticmethod
    def a___________________formula_widget______():
        pass

    def formula_widget_close(self):

        if self.formula_editor_widget.isVisible():
            self.formula_editor_widget.formula_save_ask(close_action=True)

    @staticmethod
    def a___________sauvegarde_____________():
        pass

    def app_save_all(self):
        self.app_save_datas()
        self.catalog.catalog_save_action()

    def app_save_datas(self):

        datas_config = settings_read(app_setting_file)

        datas_config["actionbar_size"] = self.actionbar_size
        datas_config["attributes_order"] = self.attributes_order
        datas_config["attributes_order_col"] = self.attributes_order_col
        datas_config["attributes_order_custom"] = self.attributes_order_custom
        datas_config["brackets_color_on"] = self.allplan.formula_color
        datas_config["description_show"] = self.ui.hierarchy.description_show
        datas_config["ismaximized_on"] = self.isMaximized()
        datas_config["language"] = self.langue
        datas_config["path_catalog"] = self.catalog.catalog_path
        datas_config["search_recent"] = self.search_recent

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["posx"] = screen.x()
                datas_config["posy"] = screen.y()
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()

                settings_save(app_setting_file, datas_config)
                return

        datas_config["posx"] = self.pos().x()
        datas_config["posy"] = self.pos().y()
        datas_config["height"] = self.size().height()
        datas_config["width"] = self.size().width()

        settings_save(app_setting_file, datas_config)

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        self.catalog.catalog_lock_file(catalog_path=self.catalog.catalog_path, lock=False)

        if self.library_widget.isVisible():
            self.library_widget.close()

        self.formula_widget_close()

        self.app_save_datas()

        if not self.catalog.catalog_save_ask():
            event.ignore()
            return

        super().closeEvent(event)

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:

            if self.ui.search_line.hasFocus():
                self.search_bar.search_filter_enter_pressed()
                return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Q:
            sizes_list = self.ui.splitter.sizes()

            left_size = sizes_list[0] - 10
            right_size = sizes_list[1] + 10

            sizes_list = [left_size, right_size]

            self.ui.splitter.setSizes(sizes_list)
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_D:
            sizes_list = self.ui.splitter.sizes()

            left_size = sizes_list[0] + 10
            right_size = sizes_list[1] - 10

            sizes_list = [left_size, right_size]

            self.ui.splitter.setSizes(sizes_list)
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
            self.action_bar.undo_button_pressed()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Y:
            self.action_bar.redo_button_pressed()
            return

        if event.key() == Qt.Key_F1:
            short_link = help_pressed(widget_parent=self)
            self.help_request(short_link=short_link)
            return

        if event.key() == Qt.Key_F2:
            self.catalog.renommer_item()
            return

        if event.key() == Qt.Key_F3:
            self.ui.hierarchy.setFocus()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_N:
            self.main_bar.catalogue_nouveau()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_O:
            self.main_bar.catalog_open_browse()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            self.catalog.catalog_save_action()
            return

        if event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_S:
            self.app_save_datas()
            return

        if event.modifiers() == (Qt.ControlModifier | Qt.ShiftModifier) and event.key() == Qt.Key_S:
            self.main_bar.catalog_save_as()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_M:
            self.catalogue_update()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:

            if self.ui.search_error_bt.isChecked():
                return

            texte = self.catalog.search_current_selection_text()

            if texte != "":
                self.ui.search_line.setText(texte)
                self.ui.search_bt.setChecked(True)
                self.ui.search_bt.clicked.emit()

            self.ui.search_line.setFocus()
            return

    def changeEvent(self, event: QEvent):

        super().changeEvent(event)

        if event.type() != QEvent.WindowStateChange:
            return

        if self.isMaximized():
            return

        screennumber = QApplication.desktop().screenNumber(self)

        screen: QRect = QApplication.desktop().availableGeometry(screennumber)

        screenwidth, screenheight = screen.width(), screen.height()

        dialogwidth, dialogweight = self.width(), self.height()

        if dialogwidth > screenwidth and dialogweight > screenheight:
            self.resize(int(screenwidth * 0.9), int(screenheight * 0.9))

        elif dialogwidth > screenwidth:
            self.resize(int(screenwidth * 0.9), self.height())

        elif dialogweight > screenheight:
            self.resize(self.width(), int(screenheight * 0.9))

        qr = self.frameGeometry()
        qr.moveCenter(screen.center())

        self.move(qr.topLeft())

        self.ui_resized.emit()

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj not in [self.ui.material_add_bt,
                       self.ui.material_list_bt,
                       self.ui.component_add_bt,
                       self.ui.component_list_bt,
                       self.ui.link_add_bt,
                       self.ui.link_list_bt,
                       self.ui.attribute_add_bt,
                       self.ui.attribute_list_bt,
                       self.ui.paste_bt,
                       self.ui.paste_list_bt,
                       self.ui.attributes_detail]:
            return super().eventFilter(obj, event)

        if event.type() == QEvent.KeyPress:

            # noinspection PyUnresolvedReferences
            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()

                self.ui.hierarchy.setFocus()

                # noinspection PyUnresolvedReferences
                QApplication.postEvent(self.ui.hierarchy, QKeyEvent(QEvent.KeyPress, event.key(), Qt.NoModifier))

                return True

            return super().eventFilter(obj, event)

        # -------------------------------
        # -------------------------------

        if event.type() == QEvent.Enter:

            if obj == self.ui.material_add_bt:

                if obj.isEnabled():
                    self.ui.material.setStyleSheet("QWidget#material {border-top:1px solid #B2B2B2; "
                                                   "border-right:1px solid #B2B2B2; "
                                                   "border-left:1px solid #B2B2B2;"
                                                   "background-color: qlineargradient("
                                                   "spread:pad, x1:0, y1:0, x2:0, y2:1,"
                                                   "stop:0 #BAD0E7, "
                                                   "stop:1 #F8F8F8) }")

                return super().eventFilter(obj, event)

            if obj == self.ui.material_list_bt:

                if obj.isEnabled():
                    self.ui.material.setStyleSheet("QWidget#material {border-top:1px solid #B2B2B2; "
                                                   "border-right:1px solid #B2B2B2; "
                                                   "border-left:1px solid #B2B2B2;"
                                                   "border-bottom:1px solid #BAD0E7;}")

                return super().eventFilter(obj, event)

            # -------------------------------

            if obj == self.ui.component_add_bt:

                if obj.isEnabled():
                    self.ui.component.setStyleSheet("QWidget#component {border-top:1px solid #B2B2B2; "
                                                    "border-right:1px solid #B2B2B2; "
                                                    "border-left:1px solid #B2B2B2;"
                                                    "background-color: "
                                                    "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                                                    "stop:0 #BAD0E7, "
                                                    "stop:1 #F8F8F8) }")

                return super().eventFilter(obj, event)

            if obj == self.ui.component_list_bt:
                if obj.isEnabled():
                    self.ui.component.setStyleSheet("QWidget#component {border-top:1px solid #B2B2B2; "
                                                    "border-right:1px solid #B2B2B2; "
                                                    "border-left:1px solid #B2B2B2;"
                                                    "border-bottom:1px solid #BAD0E7;}")

                return super().eventFilter(obj, event)

            # -------------------------------

            if obj == self.ui.link_add_bt:

                if obj.isEnabled():
                    self.ui.link.setStyleSheet("QWidget#link {border-top:1px solid #B2B2B2; "
                                               "border-right:1px solid #B2B2B2; "
                                               "border-left:1px solid #B2B2B2;"
                                               "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                                               "stop:0 #BAD0E7, "
                                               "stop:1 #F8F8F8) }")

                return super().eventFilter(obj, event)

            if obj == self.ui.link_list_bt:

                if obj.isEnabled():
                    self.ui.link.setStyleSheet("QWidget#link {border-top:1px solid #B2B2B2; "
                                               "border-right:1px solid #B2B2B2; "
                                               "border-left:1px solid #B2B2B2;"
                                               "border-bottom:1px solid #BAD0E7;}")

                return super().eventFilter(obj, event)

            # -------------------------------

            if obj == self.ui.attribute_add_bt:

                if obj.isEnabled():
                    self.ui.attribute.setStyleSheet("QWidget#attribute {border-top:1px solid #B2B2B2; "
                                                    "border-right:1px solid #B2B2B2; "
                                                    "border-left:1px solid #B2B2B2;"
                                                    "background-color: "
                                                    "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                                                    "stop:0 #BAD0E7, "
                                                    "stop:1 #F8F8F8) }")

                return super().eventFilter(obj, event)

            if obj == self.ui.attribute_list_bt:

                if obj.isEnabled():
                    self.ui.attribute.setStyleSheet("QWidget#attribute {border-top:1px solid #B2B2B2; "
                                                    "border-right:1px solid #B2B2B2; "
                                                    "border-left:1px solid #B2B2B2;"
                                                    "border-bottom:1px solid #BAD0E7;}")

                return super().eventFilter(obj, event)

            # -------------------------------

            if obj == self.ui.paste_bt:
                if obj.isEnabled():
                    self.ui.paste.setStyleSheet("QWidget#paste {border-top:1px solid #B2B2B2; "
                                                "border-right:1px solid #B2B2B2; "
                                                "border-left:1px solid #B2B2B2;"
                                                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                                                "stop:0 #BAD0E7, "
                                                "stop:1 #F8F8F8) }")

                return super().eventFilter(obj, event)

            if obj == self.ui.paste_list_bt:

                if obj.isEnabled():
                    self.ui.paste.setStyleSheet("QWidget#paste {border-top:1px solid #B2B2B2; "
                                                "border-right:1px solid #B2B2B2; "
                                                "border-left:1px solid #B2B2B2;"
                                                "border-bottom:1px solid #BAD0E7;}")

                return super().eventFilter(obj, event)

        # -------------------------------
        # -------------------------------

        elif event.type() == QEvent.MouseButtonRelease:

            if obj == self.ui.material_add_bt:

                if obj.isEnabled():
                    self.ui.material.setStyleSheet(
                        "QWidget#material {border-top:1px solid #B2B2B2; border-right:1px solid #B2B2B2;"
                        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                        "stop:0 #8FADCC, stop:1 #F8F8F8)}")

                return super().eventFilter(obj, event)

            if obj == self.ui.material_list_bt:

                if obj.isEnabled():
                    self.ui.material.setStyleSheet(
                        "QWidget#material {border-top:1px solid #B2B2B2; "
                        "border-right:1px solid #B2B2B2; "
                        "border-left:1px solid #B2B2B2;"
                        "border-bottom:1px solid #8FADCC;}")

                return super().eventFilter(obj, event)

            # -------------------------------

            if obj == self.ui.component_add_bt:

                if obj.isEnabled():
                    self.ui.component.setStyleSheet(
                        "QWidget#component {border-top:1px solid #B2B2B2; border-right:1px solid #B2B2B2;"
                        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                        "stop:0 #8FADCC, stop:1 #F8F8F8)}")

                return super().eventFilter(obj, event)

            if obj == self.ui.component_list_bt:

                if obj.isEnabled():
                    self.ui.component.setStyleSheet(
                        "QWidget#component {border-top:1px solid #B2B2B2; "
                        "border-right:1px solid #B2B2B2; "
                        "border-left:1px solid #B2B2B2;"
                        "border-bottom:1px solid #8FADCC;}")

                return super().eventFilter(obj, event)

            # -------------------------------

            if obj == self.ui.link_add_bt:

                if obj.isEnabled():
                    self.ui.link.setStyleSheet(
                        "QWidget#link {border-top:1px solid #B2B2B2; border-right:1px solid #B2B2B2;"
                        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                        "stop:0 #8FADCC, stop:1 #F8F8F8)}")

                return super().eventFilter(obj, event)

            if obj == self.ui.link_list_bt:

                if obj.isEnabled():
                    self.ui.link.setStyleSheet(
                        "QWidget#link {border-top:1px solid #B2B2B2; "
                        "border-right:1px solid #B2B2B2; "
                        "border-left:1px solid #B2B2B2;"
                        "border-bottom:1px solid #8FADCC;}")

                return super().eventFilter(obj, event)

            # -------------------------------

            if obj == self.ui.attribute_add_bt:

                if obj.isEnabled():
                    self.ui.attribute.setStyleSheet(
                        "QWidget#attribute {border-top:1px solid #B2B2B2; border-right:1px solid #B2B2B2;"
                        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                        "stop:0 #8FADCC, stop:1 #F8F8F8)}")

                return super().eventFilter(obj, event)

            if obj == self.ui.attribute_list_bt:

                if obj.isEnabled():
                    self.ui.attribute.setStyleSheet(
                        "QWidget#attribute {border-top:1px solid #B2B2B2; "
                        "border-right:1px solid #B2B2B2; "
                        "border-left:1px solid #B2B2B2;"
                        "border-bottom:1px solid #8FADCC;}")

                return super().eventFilter(obj, event)

            # -------------------------------

            if obj == self.ui.paste_bt:

                if obj.isEnabled():
                    self.ui.paste.setStyleSheet(
                        "QWidget#paste {border-top:1px solid #B2B2B2; border-right:1px solid #B2B2B2;"
                        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                        "stop:0 #8FADCC, stop:1 #F8F8F8)}")

                return super().eventFilter(obj, event)

            if obj == self.ui.paste_list_bt:

                if obj.isEnabled():
                    self.ui.paste.setStyleSheet(
                        "QWidget#paste {border-top:1px solid #B2B2B2; "
                        "border-right:1px solid #B2B2B2; "
                        "border-left:1px solid #B2B2B2;"
                        "border-bottom:1px solid #8FADCC;}")

                return super().eventFilter(obj, event)

        # -------------------------------
        # -------------------------------

        elif event.type() == QEvent.Leave:

            self.ui.material.setStyleSheet(self.material_style)
            self.ui.material_add_bt.setStyleSheet(self.material_1)
            self.ui.material_list_bt.setStyleSheet(self.material_2)

            # -------------------------------

            self.ui.component.setStyleSheet(self.component_style)
            self.ui.component_add_bt.setStyleSheet(self.component_1)
            self.ui.component_list_bt.setStyleSheet(self.component_2)

            # -------------------------------

            self.ui.link.setStyleSheet(self.link_style)
            self.ui.link_add_bt.setStyleSheet(self.link_1)
            self.ui.link_list_bt.setStyleSheet(self.link_2)

            # -------------------------------

            self.ui.attribute.setStyleSheet(self.attribute_style)
            self.ui.attribute_add_bt.setStyleSheet(self.attribute_1)
            self.ui.attribute_list_bt.setStyleSheet(self.attribute_2)

            # -------------------------------

            self.ui.paste.setStyleSheet(self.paste_style)
            self.ui.paste_bt.setStyleSheet(self.paste_1)
            self.ui.paste_list_bt.setStyleSheet(self.paste_2)

        return super().eventFilter(obj, event)

    def dragEnterEvent(self, event: QDragEnterEvent):

        if self.library_widget.isVisible():
            event.ignore()
            return

        if event.mimeData().hasUrls():

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.verification_drop(file_path=file_path, add=False):
                event.accept()
            else:
                event.ignore()

        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):

        if self.library_widget.isVisible():
            event.ignore()
            return

        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.verification_drop(file_path=file_path, add=False):
                event.accept()
            else:
                event.ignore()

        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):

        if self.library_widget.isVisible():
            event.ignore()
            return

        if event.mimeData().hasUrls():

            event.setDropAction(Qt.CopyAction)

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.verification_drop(file_path=file_path, add=True):
                event.accept()

            else:
                event.ignore()
        else:
            event.ignore()

    def verification_drop(self, file_path: str, add=False) -> bool:

        if not isinstance(file_path, str):
            return False

        valid_file = False

        for extension in importable_file_extension:

            if file_path.lower().endswith(extension):
                valid_file = True
                break

        if not valid_file:
            return False

        file_path_lower = file_path.lower()

        if file_path_lower.endswith(".apn") or file_path_lower.endswith(".prj"):

            # todo à modifier

            if "2024" in self.allplan.version_datas:
                version_obj = self.allplan.version_datas["2024"]

                if not isinstance(version_obj, AllplanPaths):
                    return False

                chemin_prj = version_obj.prj_path

            elif "2025" in self.allplan.version_datas:

                version_obj = self.allplan.version_datas["2025"]

                if not isinstance(version_obj, AllplanPaths):
                    return False

                chemin_prj = version_obj.prj_path

            else:
                return False

            chemin_catalogue_tmp = get_real_path_of_apn_file(file_path, chemin_prj, True)

            if chemin_catalogue_tmp == "":
                return False

            file_path = chemin_catalogue_tmp
            file_path_lower = file_path.lower()

        if file_path_lower.endswith(".xml"):
            check_catalog = verification_catalogue_correct(file_path, message=False)

            if check_catalog != "XML":
                return False

            if not add:
                return True

            print(f"smartcatlog -- verification_drop -- lancer chargement catalogue : {file_path}")
            self.catalog.catalog_load_start(catalog_path=file_path)
            return True

        if not add:
            return True

        return self.new_catalog_widget.personnalisation(convert_bdd=True, file_path=file_path)

    @staticmethod
    def a___________________end______():
        pass


class SingleApplication(QApplication):
    """Permet d'ouvrir qu'une seule fois l'application"""

    def __init__(self, argv, nom_appli):
        super().__init__(argv)
        # cleanup (only needed for unix)
        QSharedMemory(nom_appli).attach()
        self._memory = QSharedMemory(self)
        self._memory.setKey(nom_appli)
        if self._memory.attach():
            self._running = True
        else:
            self._running = False
            if not self._memory.create(1):
                raise RuntimeError(self._memory.errorString())

    def isrunning(self):
        """Renvoi si d'autres applications sont déjà démarrées"""
        return self._running


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

if __name__ == '__main__':

    tps1 = time.perf_counter()

    print("application start")

    if len(sys.argv) == 2:
        app2 = SingleApplication(sys.argv, "Formulaire")

    else:

        app2 = SingleApplication(sys.argv, application_name)

    if app2.isrunning():

        langue_app = settings_get(app_setting_file, 'language')

        if isinstance(langue_app, str):

            langue_app = langue_app.lower()

            if langue_app == "fr":
                msg(titre=application_title,
                    message="Application déjà ouverte, impossible d'ouvrir plusieurs instances.")

                sys.exit(1)

            if langue_app == "de":
                msg(titre=application_title,
                    message="Die Anwendung ist bereits geöffnet. "
                            "Es können nicht mehrere Instanzen geöffnet werden.")

                sys.exit(1)

            if langue_app == "it":
                msg(titre=application_title,
                    message="L'applicazione è già aperta, non è possibile aprire più istanze.")

                sys.exit(1)

            if langue_app == "es":
                msg(titre=application_title,
                    message="La aplicación ya está abierta, no se pueden abrir varias instancias.")

                sys.exit(1)

        msg(titre=application_title,
            message="Application is already open, impossible to open several instances.")

        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationVersion(application_version)

    font = app.font()
    font.setFamily("Segoe UI")
    font.setPointSize(taille_police)
    app.setFont(font)

    translator = QTranslator()
    app.installTranslator(translator)

    app.setStyle('Fusion')

    app.setStyleSheet("""QToolTip {background-color: white; padding: 2px;  border: 2px solid #E7E7E7}""")

    if len(sys.argv) == 2:
        ex = Formulaire()
    else:
        ex = Mainwindow()

    print("--------------------------------------")
    print(f"temps total d'execution : {time.perf_counter() - tps1} ms")
    print("--------------------------------------")

    sys.exit(app.exec_())
