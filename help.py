#!/usr/bin/python3
# -*- coding: utf-8 -*

from allplan_manage import *
from tools import help_open_link, help_get_short_link, settings_save
from tools import move_window_tool, get_look_treeview, MyContextMenu, copy_to_clipboard, help_get_full_link
from ui_help import Ui_Help


class HelpWidget(QWidget):

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_Help()
        self.ui.setupUi(self)

        get_look_treeview(widget=self.ui.help_tree)

        # ---------------------------------------
        # LOADING PARENT
        # ---------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        # ---------------------------------------
        # LOADING settings
        # ---------------------------------------

        help_settings = settings_read(file_name=help_setting_file)

        width = help_settings.get("width", help_setting_datas.get("width", 600))

        if not isinstance(width, int):
            width = help_setting_datas.get("width", 600)

        height = help_settings.get("height", help_setting_datas.get("height", 800))

        if not isinstance(height, int):
            height = help_setting_datas.get("height", 800)

        self.resize(width, height)

        # ---------------------------------------

        ismaximized_on = help_settings.get("ismaximized_on", help_setting_datas.get("ismaximized_on", False))

        if not isinstance(ismaximized_on, bool):
            self.ismaximized_on = help_setting_datas.get("ismaximized_on", False)
        else:
            self.ismaximized_on = ismaximized_on

        # ---------------------------------------

        current_article = help_settings.get("current_article", help_setting_datas.get("current_article", ""))

        if not isinstance(current_article, str):
            current_article = help_setting_datas.get("current_article", "")

        self.current_article = current_article

        # ---------------------------------------
        # LOADING Model
        # ---------------------------------------

        self.help_model = QStandardItemModel()

        # ---------------------------------------
        # LOADING filter
        # ---------------------------------------

        self.help_filter = QSortFilterProxyModel()
        self.help_filter.setSourceModel(self.help_model)
        self.help_filter.setRecursiveFilteringEnabled(True)
        self.help_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.help_filter.setSortLocaleAware(True)
        self.help_filter.setSourceModel(self.help_model)

        self.ui.help_tree.setModel(self.help_filter)

        # ---------------------------------------
        # SIGNAl - Tree
        # ---------------------------------------

        self.asc.langue_change.connect(self.help_model_clear)
        self.ui.help_tree.doubleClicked.connect(self.help_item_double_clicked)

        self.ui.help_tree.customContextMenuRequested.connect(self.help_tree_menu_show)

        # ---------------------------------------
        # SIGNAl - Buttons
        # ---------------------------------------

        self.ui.search_bar.textChanged.connect(self.help_search_changed)
        self.ui.search_clear_bt.clicked.connect(self.help_search_clear)

        self.ui.quit.clicked.connect(self.close)

    @staticmethod
    def a___________________init_______________():
        pass

    def help_show(self, short_link=""):

        if self.help_model.rowCount() == 0:
            self.ui.search_bar.clear()
            self.help_load_model()

            if short_link == "":
                short_link = self.current_article

        if short_link != "":
            self.help_model_select_short_link(short_link=short_link)

        self.ui.search_bar.setFocus()

        move_window_tool(widget_parent=self.asc, widget_current=self)

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

        # self.create_footer()

    @staticmethod
    def a___________________model_______________():
        pass

    def help_load_model(self):

        # ----------------------------
        # Interface
        # ----------------------------

        qs_intro = QStandardItem(get_icon(asc_icon), self.tr("Introduction"))

        # ---------

        qs_intro_001 = self.help_add_article(
            title=self.tr("Présentation du SmartCatalog Editor"),
            link=help_interface_presentat,
            tags=list())

        qs_intro_002 = self.help_add_article(
            title=self.tr("Interface : ActionBar"),
            link=help_interface_actionbar,
            tags=list())

        qs_intro_003 = self.help_add_article(
            title=self.tr("Interface : Hiérarchie"),
            link=help_interface_hierarchy,
            tags=list())

        qs_intro_004 = self.help_add_article(
            title=self.tr("Interface : Attributs"),
            link=help_interface_attribute,
            tags=list())

        qs_intro_005 = self.help_add_article(
            title=self.tr("Changer la langue"),
            link=help_interface_langue,
            tags=list())

        qs_intro.appendColumn([qs_intro_001, qs_intro_002, qs_intro_003, qs_intro_004, qs_intro_005])

        # ----------------------------
        # Allplan
        # ----------------------------

        qs_allplan = QStandardItem(get_icon(allplan_icon), "Allplan")

        # ---------

        qs_allplan_001 = self.help_add_article(
            title=self.tr("Connecter un catalogue à un projet"),
            link=help_allplan_connect_prj,
            tags=list())

        qs_allplan_002 = self.help_add_article(
            title=self.tr("Configurer l'affichage de votre catalogue dans Allplan"),
            link=help_allplan_display,
            tags=list())

        qs_allplan_003 = self.help_add_article(
            title=self.tr("Choisir un ouvrage de votre catalogue dans Allplan"),
            link=help_allplan_material,
            tags=list())

        qs_allplan_004 = self.help_add_article(
            title=self.tr("Créer un quantitatif"),
            link=help_allplan_report,
            tags=list())

        qs_allplan_005 = self.help_add_article(
            title=self.tr("Rafraichir les données Allplan"),
            link=help_allplan_refresh,
            tags=list())

        qs_allplan_006 = self.help_add_article(
            title=self.tr("Lire les rapports d'erreurs d'Allplan"),
            link=help_allplan_error,
            tags=list())

        qs_allplan.appendColumn([qs_allplan_001, qs_allplan_002, qs_allplan_003,
                                 qs_allplan_004, qs_allplan_005, qs_allplan_006])

        # ----------------------------
        # Catalogue
        # ----------------------------

        qs_catalog = QStandardItem(get_icon(catalog_icon), self.tr("Catalogue"))

        # ---------

        qs_catalog_001 = self.help_add_article(
            title=self.tr("Qu'est-ce qu'un catalogue"),
            link=help_cat_what,
            tags=list())

        qs_catalog_002 = self.help_add_article(
            title=self.tr("Nouveau catalogue"),
            link=help_cat_new_cat,
            tags=list())

        qs_catalog_003 = self.help_add_article(
            title=self.tr("Convertir une base de données BCM en catalogue"),
            link=help_cat_convert,
            tags=list())

        qs_catalog_004 = self.help_add_article(
            title=self.tr("Ouvrir un catalogue"),
            link=help_cat_open_cat,
            tags=list())

        qs_catalog_005 = self.help_add_article(
            title=self.tr("Modifier les paramètres du catalogue"),
            link=help_cat_settings,
            tags=list())

        qs_catalog_006 = self.help_add_article(
            title=self.tr("Gérer la liste des catalogues récents"),
            link=help_cat_recent,
            tags=list())

        qs_catalog_007 = self.help_add_article(
            title=self.tr("Enregistrer un catalogue"),
            link=help_cat_save,
            tags=list())

        qs_catalog_008 = self.help_add_article(
            title=self.tr("Dupliquer un catalogue"),
            link=help_cat_save_as,
            tags=list())

        qs_catalog_009 = self.help_add_article(
            title=self.tr("Mettre à jour les catalogues de vos projets"),
            link=help_cat_update,
            tags=list())

        qs_catalog_010 = self.help_add_article(
            title=self.tr("Restaurer une sauvegarde"),
            link=help_cat_restore,
            tags=list())

        qs_catalog.appendColumn([qs_catalog_001, qs_catalog_002, qs_catalog_003,
                                 qs_catalog_004, qs_catalog_005, qs_catalog_006,
                                 qs_catalog_007, qs_catalog_008, qs_catalog_009,
                                 qs_catalog_010])

        # ----------------------------
        # Folder
        # ----------------------------

        qs_folder = QStandardItem(get_icon(folder_icon), self.tr("Dossier"))

        # ---------

        qs_folder_001 = self.help_add_article(
            title=self.tr("Qu'est-ce qu'un dossier"),
            link=help_folder_what,
            tags=list())

        qs_folder_002 = self.help_add_article(
            title=self.tr("Créer un nouveau dossier"),
            link=help_folder_new,
            tags=list())

        qs_folder_003 = self.help_add_article(
            title=self.tr("Supprimer un dossier"),
            link=help_folder_del,
            tags=list())

        qs_folder_004 = self.help_add_article(
            title=self.tr("Couper/Copier un dossier"),
            link=help_folder_copy,
            tags=list())

        qs_folder_005 = self.help_add_article(
            title=self.tr("Coller un dossier"),
            link=help_folder_paste,
            tags=list())

        qs_folder_006 = self.help_add_article(
            title=self.tr("Changer icône dossier"),
            link=help_folder_icon,
            tags=list())

        qs_folder.appendColumn([qs_folder_001, qs_folder_002, qs_folder_003,
                                qs_folder_004, qs_folder_005, qs_folder_006])

        # ----------------------------
        # Material
        # ----------------------------

        qs_material = QStandardItem(get_icon(material_icon), self.tr("Ouvrage"))

        # ---------

        qs_material_001 = self.help_add_article(
            title=self.tr("Qu'est-ce qu'un ouvrage"),
            link=help_material_what,
            tags=list())

        qs_material_002 = self.help_add_article(
            title=self.tr("Créer un nouvel ouvrage"),
            link=help_material_new,
            tags=list())

        qs_material_003 = self.help_add_article(
            title=self.tr("Supprimer un ouvrage"),
            link=help_material_del,
            tags=list())

        qs_material_004 = self.help_add_article(
            title=self.tr("Couper/Copier un ouvrage"),
            link=help_material_copy,
            tags=list())

        qs_material_005 = self.help_add_article(
            title=self.tr("Coller un ouvrage"),
            link=help_material_paste,
            tags=list())

        qs_material.appendColumn([qs_material_001, qs_material_002, qs_material_003,
                                  qs_material_004, qs_material_005])
        # ----------------------------
        # Component
        # ----------------------------

        qs_composant = QStandardItem(get_icon(component_icon), self.tr("Composant"))

        # ---------

        qs_composant_001 = self.help_add_article(
            title=self.tr("Qu'est-ce qu'un composant"),
            link=help_component_what,
            tags=list())

        qs_composant_002 = self.help_add_article(
            title=self.tr("Créer un nouveau composant"),
            link=help_component_new,
            tags=list())

        qs_composant_003 = self.help_add_article(
            title=self.tr("Supprimer un composant"),
            link=help_component_del,
            tags=list())

        qs_composant_004 = self.help_add_article(
            title=self.tr("Couper/Copier un composant"),
            link=help_component_copy,
            tags=list())

        qs_composant_005 = self.help_add_article(
            title=self.tr("Coller un composant"),
            link=help_component_paste,
            tags=list())

        qs_composant.appendColumn([qs_composant_001, qs_composant_002, qs_composant_003,
                                   qs_composant_004, qs_composant_005])

        # ----------------------------
        # Link
        # ----------------------------

        qs_link = QStandardItem(get_icon(link_icon), self.tr("Lien"))

        # ---------

        qs_link_001 = self.help_add_article(
            title=self.tr("Qu'est-ce qu'un lien"),
            link=help_link_what,
            tags=list())

        qs_link_002 = self.help_add_article(
            title=self.tr("Créer un nouveau lien"),
            link=help_link_new,
            tags=list())

        qs_link_003 = self.help_add_article(
            title=self.tr("Supprimer un lien"),
            link=help_link_del,
            tags=list())

        qs_link_004 = self.help_add_article(
            title=self.tr("Couper/Copier un lien"),
            link=help_link_copy,
            tags=list())

        qs_link_005 = self.help_add_article(
            title=self.tr("Coller un lien"),
            link=help_link_paste,
            tags=list())

        qs_link.appendColumn([qs_link_001, qs_link_002, qs_link_003,
                              qs_link_004, qs_link_005])

        # ----------------------------
        # Attribute
        # ----------------------------

        qs_attribute = QStandardItem(get_icon(attribute_icon), self.tr("Attribut"))

        # ---------

        qs_attribute_001 = self.help_add_article(
            title=self.tr("Qu'est-ce qu'un attribut"),
            link=help_attribute_what,
            tags=list())

        qs_attribute_002 = self.help_add_article(
            title=self.tr("Ajouter un attribut"),
            link=help_attribute_new,
            tags=list())

        qs_attribute_003 = self.help_add_article(
            title=self.tr("Gérer vos favoris d'attributs"),
            link=help_attribute_fav,
            tags=list())

        qs_attribute_004 = self.help_add_article(
            title=self.tr("Supprimer un attribut"),
            link=help_attribute_del,
            tags=list())

        qs_attribute_005 = self.help_add_article(
            title=self.tr("Couper/Copier un attribut"),
            link=help_attribute_copy,
            tags=list())

        qs_attribute_006 = self.help_add_article(
            title=self.tr("Coller un attribut"),
            link=help_attribute_paste,
            tags=list())

        qs_attribute_007 = self.help_add_article(
            title=self.tr("Gérer l'ordre d'affichage des attributs"),
            link=help_attribute_order,
            tags=list())

        qs_attribute.appendColumn([qs_attribute_001, qs_attribute_002, qs_attribute_003,
                                   qs_attribute_004, qs_attribute_005, qs_attribute_006,
                                   qs_attribute_007])

        # ----------------------------
        # Formula
        # ----------------------------

        qs_formula = QStandardItem(get_icon(formula_icon), self.tr("Formule"))

        # ---------

        qs_formula_001 = self.help_add_article(
            title=self.tr("Fonctionnement des formules"),
            link=help_formula_what,
            tags=list())

        qs_formula_002 = self.help_add_article(
            title=self.tr("L'éditeur de formules"),
            link=help_formula_editor,
            tags=list())

        qs_formula_003 = self.help_add_article(
            title=self.tr("Créer une formule"),
            link=help_formula_new,
            tags=list())

        qs_formula_004 = self.help_add_article(
            title=self.tr("Rechercher les formules contenant des erreurs"),
            link=help_formula_search,
            tags=list())

        qs_formula_005 = self.help_add_article(
            title=self.tr("Aide Allplan : Les fonctions"),
            link=help_formula_function,
            tags=list())

        qs_formula_006 = self.help_add_article(
            title=self.tr("Aide Allplan : Les attributs"),
            link=help_formula_attribute,
            tags=list())

        qs_formula_007 = self.help_add_article(
            title=self.tr("Aide Allplan : Les Portes et fenêtres"),
            link=help_formula_door,
            tags=list())

        qs_formula.appendColumn([qs_formula_001, qs_formula_002, qs_formula_003,
                                 qs_formula_004, qs_formula_005, qs_formula_006,
                                 qs_formula_007])

        # ----------------------------
        # Formula favorites
        # ----------------------------

        qs_formula_fav = QStandardItem(get_icon(formula_favorite_icon), self.tr("Favoris de formule"))

        # ---------

        qs_formula_fav_001 = self.help_add_article(
            title=self.tr("Enregistrer une formule dans mes favoris"),
            link=help_formula_fav_save,
            tags=list())

        qs_formula_fav_002 = self.help_add_article(
            title=self.tr("Utiliser une formule de vos favoris"),
            link=help_formula_fav_use,
            tags=list())

        qs_formula_fav_003 = self.help_add_article(
            title=self.tr("Gérer vos favoris de formule"),
            link=help_formula_fav_manage,
            tags=list())

        qs_formula_fav.appendColumn([qs_formula_fav_001, qs_formula_fav_002, qs_formula_fav_003])

        # ----------------------------
        # Search
        # ----------------------------

        qs_search = QStandardItem(get_icon(search_icon), self.tr("Rechercher"))

        # ---------

        qs_search_001 = self.help_add_article(
            title=self.tr("Rechercher dans votre catalogue"),
            link=help_search_cat,
            tags=list())

        qs_search_002 = self.help_add_article(
            title=self.tr("Gérer les filtres de la recherche"),
            link=help_search_filter,
            tags=list())

        qs_search.appendColumn([qs_search_001, qs_search_002])

        # ----------------------------
        # Search and replace
        # ----------------------------

        qs_replace = QStandardItem(get_icon(search_replace_icon), self.tr("Rechercher et remplacer"))

        # ---------

        qs_replace_001 = self.help_add_article(
            title=self.tr("Rechercher et remplacer"),
            link=help_replace_cat,
            tags=list())

        qs_replace.appendColumn([qs_replace_001])

        # ----------------------------
        # Models
        # ----------------------------

        qs_model = QStandardItem(get_icon(attribute_model_show_icon), self.tr("Modèle"))

        # ---------

        qs_model_001 = self.help_add_article(
            title=self.tr("Qu'est ce qu'un modèle"),
            link=help_model_what,
            tags=list())

        qs_model_002 = self.help_add_article(
            title=self.tr("Créer un modèle"),
            link=help_model_new,
            tags=list())

        qs_model_003 = self.help_add_article(
            title=self.tr("Gérer les attributs d'un modèle"),
            link=help_model_manage,
            tags=list())

        qs_model_004 = self.help_add_article(
            title=self.tr("Gérer les modèles"),
            link=help_model_modify,
            tags=list())

        qs_model_005 = self.help_add_article(
            title=self.tr("Importer/exporter un modèle"),
            link=help_model_import,
            tags=list())

        qs_model.appendColumn([qs_model_001, qs_model_002, qs_model_003,
                               qs_model_004, qs_model_005])

        # ----------------------------
        # Libraries
        # ----------------------------

        qs_library = QStandardItem(get_icon(external_bdd_option_icon), self.tr("Bible externe"))

        # ---------

        qs_library_001 = self.help_add_article(
            title=self.tr("Qu'est ce qu'une bible externe"),
            link=help_library_what,
            tags=list())

        qs_library_002 = self.help_add_article(
            title=self.tr("Ajouter une bible externe"),
            link=help_library_new,
            tags=list())

        qs_library_003 = self.help_add_article(
            title=self.tr("Gérer vos bibles externes"),
            link=help_library_manage,
            tags=list())

        qs_library_004 = self.help_add_article(
            title=self.tr("Importer des éléments dans votre catalogue"),
            link=help_library_import,
            tags=list())

        qs_library_005 = self.help_add_article(
            title=self.tr("Synchroniser les éléments de votre catalogue"),
            link=help_library_sync,
            tags=list())

        qs_library.appendColumn([qs_library_001, qs_library_002, qs_library_003,
                                 qs_library_004, qs_library_005])

        # ----------------------------

        self.help_model.appendColumn([qs_intro, qs_allplan, qs_catalog, qs_folder, qs_material, qs_composant,
                                      qs_link, qs_attribute, qs_formula, qs_formula_fav, qs_search, qs_replace,
                                      qs_model, qs_library])
        # self.print_list()
        # self.create_footer()

    def print_list(self):

        row_count = self.help_model.rowCount()

        for row_index in range(row_count):

            qs_parent = self.help_model.item(row_index, 0)

            title_parent = qs_parent.text()

            child_count = qs_parent.rowCount()

            for row_child_index in range(child_count):

                qs_child = qs_parent.child(row_child_index, 0)

                title_child = qs_child.text()

                if " : " in title_child:
                    title_child = title_child.replace(" : ", " ")

                if "/" in title_child:
                    title_child = title_child.replace("/", " ")

                short_link = qs_child.data(user_data_type)

                print(f"{str(row_index).zfill(2)} - {title_parent} - {short_link} - {title_child}")

    def create_footer(self):

        if self.asc.langue != "FR":
            return

        folder_path = "C:\\Users\\jmauger\\OneDrive - Allplan Group\\Documents\\ASC\\"

        row_count = self.help_model.rowCount()

        articles_list = list()

        for row_index in range(row_count):

            qs_parent = self.help_model.item(row_index, 0)

            title_parent = qs_parent.text()

            child_count = qs_parent.rowCount()

            for row_child_index in range(child_count):

                qs_child = qs_parent.child(row_child_index, 0)

                title_child = qs_child.text()

                if " : " in title_child:
                    title_child = title_child.replace(" : ", " ")

                if "/" in title_child:
                    title_child = title_child.replace("/", " ")

                short_link = qs_child.data(user_data_type)

                folder_name = f"{str(row_index).zfill(2)} - {title_parent} - {short_link} - {title_child}\\"

                full_path = f"{folder_path}{folder_name}"

                if not os.path.exists(full_path):

                    try:

                        os.mkdir(full_path)

                    except Exception as error:
                        print(f"error : {error}")
                        continue

                articles_list.append([short_link, title_child, f"{full_path}{short_link}_footer_FR.html"])

                if not os.path.exists(f"{full_path}{short_link}_FR.txt"):

                    try:

                        with open(f"{full_path}{short_link}_FR.txt", "w", encoding="UTF-8") as file:

                            file.write(f"PROBLEMATIQUE :\n\n"
                                       f"{title_child}\n\n"
                                       f"SOLUTION :\n\n"
                                       f"\n"
                                       f"\nÉtape 1 : \n"
                                       f"\n"
                                       f"Étape 2 : ")

                    except Exception as error:
                        print(f"error : {error}")
                        continue

        articles_count = len(articles_list)

        for index_list, datas in enumerate(articles_list):

            short_link, description, full_path = datas

            if short_link == "ASC8769":
                print("a")

            text = ('<span style="font-size: 14px;"><u><strong>PROBLEMATIQUE :</strong></u><br/>\n'
                    '<br/>\n'
                    f'{description}<br/>\n'
                    '<br/>\n'
                    '<u><strong>SOLUTION :</strong></u><br/>\n'
                    '<br/>\n'
                    '<br/>\n'
                    '<br/>\n'
                    '<u><strong>&Eacute;tape 1 :</strong></u> <br/>\n'
                    '<br/>\n'
                    '<u><strong>&Eacute;tape 2 :</strong></u> <br/>\n'
                    '</span>\n')

            if index_list == 0:

                next_datas = articles_list[index_list + 1]

                next_short_link = next_datas[0]
                next_title = next_datas[1]

                text += ('<div style="text-align: center; margin-top:40px;">'
                         '<span style="font-size: 14px;">'
                         f'<a href="https://allplan.my.site.com/Customer/s/article/{next_short_link}?'
                         f'name={next_short_link}&language=fr" target="_blank">'
                         f'{next_title}'
                         '<img src="https://allplan.file.force.com/servlet/'
                         'rtaImage?eid=ka0Vi0000003cFF&feoid=00N7U000000dikS&refid=0EMVi000005EwSg" '
                         'style="margin-left: 5px;width: 8px;height: 14px;"/></a></span></div>\n')

            elif index_list == articles_count - 1:

                previous_datas = articles_list[index_list - 1]

                previous_short_link = previous_datas[0]
                previous_title = previous_datas[1]

                text += ('<div style="text-align: center; margin-top:40px;">'
                         '<span style="font-size: 14px;">'
                         f'<a href="https://allplan.my.site.com/Customer/s/article/{previous_short_link}?'
                         f'name={previous_short_link}&language=fr" target="_blank">'
                         f'<img src="https://allplan.file.force.com/servlet/'
                         f'rtaImage?eid=ka0Vi0000003cFF&feoid=00N7U000000dikS&refid=0EMVi000005EwSf" '
                         f'style="margin-right: 5px;width: 8px;height: 14px;"/>'
                         f'{previous_title}</a></span></div>\n')

            else:

                previous_datas = articles_list[index_list - 1]

                previous_short_link = previous_datas[0]
                previous_title = previous_datas[1]

                next_datas = articles_list[index_list + 1]

                next_short_link = next_datas[0]
                next_title = next_datas[1]

                text += ('<div style="text-align: center; margin-top:40px;">'
                         '<span style="font-size: 14px;">'
                         f'<a href="https://allplan.my.site.com/Customer/s/article/{previous_short_link}?'
                         f'name={previous_short_link}&language=fr" target="_blank">'
                         f'<img src="https://allplan.file.force.com/servlet/'
                         f'rtaImage?eid=ka0Vi0000003cFF&feoid=00N7U000000dikS&refid=0EMVi000005EwSf" '
                         f'style="margin-right: 5px;width: 8px;height: 14px;"/>'
                         f'{previous_title}</a>&nbsp;--&nbsp;'
                         f'<a href="https://allplan.my.site.com/Customer/s/article/{next_short_link}?'
                         f'name={next_short_link}&language=fr" target="_blank">'
                         f'{next_title}'
                         f'<img src="https://allplan.file.force.com/servlet/'
                         f'rtaImage?eid=ka0Vi0000003cFF&feoid=00N7U000000dikS&refid=0EMVi000005EwSg" '
                         f'style="margin-left: 5px;width: 8px;height: 14px;"/></a></span></div>\n')

            try:

                with open(full_path, "w", encoding="UTF-8") as file:
                    file.write(text)

            except Exception as error:
                print(f"error : {error}")
                continue

    @staticmethod
    def help_add_article(title: str, link: str, tags: list) -> QStandardItem:

        qs_title = QStandardItem(get_icon(help_icon), title)

        if link != "":
            qs_title.setData(link, user_data_type)

        if len(tags) != 0:
            pass

        return qs_title

    def help_model_clear(self):

        self.help_model.clear()

        self.ui.search_bar.clear()

    def help_model_select_short_link(self, short_link: str):

        if not isinstance(short_link, str):
            return

        short_link = short_link.upper()

        if not short_link.startswith("ASC"):
            return

        search_start = self.help_model.index(0, 0)

        search = self.help_model.match(search_start, user_data_type, short_link, 1,
                                       Qt.MatchContains | Qt.MatchRecursive)

        if len(search) == 0:
            return

        qm_model = search[0]

        if not qm_check(qm_model):
            return

        qm_filter = self.help_filter.mapFromSource(qm_model)

        if not qm_check(qm_filter):
            return

        qm_parent = qm_filter.parent()

        if not qm_check(qm_parent):
            return

        if not self.ui.help_tree.isExpanded(qm_parent):
            self.ui.help_tree.setExpanded(qm_parent, True)

        self.ui.help_tree.clearSelection()
        self.ui.help_tree.selectionModel().select(qm_filter, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.ui.help_tree.setFocus()

    @staticmethod
    def a___________________tree_menu_______________():
        pass

    def help_tree_menu_show(self, point: QPoint):

        qm_current = self.help_tree_get_current()

        if not qm_check(qm_current):
            is_folder = False
            collapsed = False

        else:

            is_folder = qm_current.data(user_data_type) is None
            collapsed = self.ui.help_tree.isExpanded(qm_current)

        menu = MyContextMenu()

        if not is_folder:
            menu.add_title(title=self.tr("Article"))

            menu.add_action(qicon=get_icon(open_icon),
                            title=self.tr("Afficher l'article"),
                            action=lambda: self.help_tree_expand(qm=qm_current))

            menu.add_action(qicon=get_icon(text_copy_icon),
                            title=self.tr("Copier le lien dans le presse-papier"),
                            action=self.help_tree_copy_to_clipboard)

        menu.add_title(title=self.tr("Affichage"))

        if is_folder and not collapsed:
            menu.add_action(qicon=get_icon(expand_all_icon),
                            title=self.tr("Déplier"),
                            action=lambda: self.help_tree_expand(qm=qm_current))

        menu.add_action(qicon=get_icon(expand_all_icon),
                        title=self.tr("Déplier tous"),
                        action=self.help_tree_expand_all)

        menu.addSeparator()

        if is_folder and collapsed:
            menu.add_action(qicon=get_icon(expand_all_icon),
                            title=self.tr("Replier"),
                            action=lambda: self.help_tree_collapse(qm=qm_current))

        menu.add_action(qicon=get_icon(expand_all_icon),
                        title=self.tr("Replier tous"),
                        action=self.help_tree_collapse_all)

        menu.exec_(self.ui.help_tree.mapToGlobal(point))

    @staticmethod
    def a___________________tree_clicked_______________():
        pass

    def help_item_double_clicked(self):

        qm_selection_list = self.ui.help_tree.selectionModel().selectedRows()

        if len(qm_selection_list) == 0:
            return

        qm = qm_selection_list[0]

        if not qm_check(qm):
            return

        short_link = qm.data(user_data_type)

        if not isinstance(short_link, str):
            return

        full_link = help_get_full_link(short_link=short_link, langue=self.asc.langue)

        if not full_link.startswith("https"):
            return

        help_open_link(full_link=full_link)

    @staticmethod
    def a___________________tree_display_______________():
        pass

    def help_tree_expand(self, qm: QModelIndex):

        if not qm_check(qm):
            return

        self.ui.help_tree.expand(qm)

    def help_tree_expand_all(self):

        self.ui.help_tree.expandAll()

    def help_tree_collapse(self, qm: QModelIndex):

        if not qm_check(qm):
            return

        self.ui.help_tree.collapse(qm)

    def help_tree_collapse_all(self):

        self.ui.help_tree.collapseAll()

    @staticmethod
    def a___________________tree_tools_______________():
        pass

    def help_tree_get_current(self):

        selection_list = self.ui.help_tree.selectionModel().selectedRows()

        if len(selection_list) != 1:
            return None

        qm = selection_list[0]

        if not qm_check(qm):
            return None

        return qm

    def help_tree_get_full_link(self) -> str:

        qm_current = self.help_tree_get_current()

        if not qm_check(qm_current):
            return ""

        short_link = qm_current.data(user_data_type)

        if not isinstance(short_link, str):
            return ""

        full_link = help_get_full_link(short_link=short_link, langue=self.asc.langue)

        if not full_link.startswith("https"):
            return ""

        return full_link

    def help_tree_get_short_link(self) -> str:

        full_link = self.help_tree_get_full_link()

        if full_link == "":
            return ""

        sort_link = help_get_short_link(full_link=full_link)

        if not sort_link.startswith("ASC"):
            return ""

        return sort_link

    def help_tree_copy_to_clipboard(self):

        link = self.help_tree_get_full_link()

        if link == "":
            return

        copy_to_clipboard(value=link)

    @staticmethod
    def a___________________search_______________():
        pass

    def help_search_changed(self):

        self.help_filter.setFilterRegExp(self.ui.search_bar.text())

        self.ui.help_tree.expandAll()
        self.help_search_define_look()

    def help_search_clear(self):
        self.ui.search_bar.clear()
        self.help_search_define_look()

    def help_search_define_look(self):

        current_text = self.ui.search_bar.text()

        if current_text == "":
            self.ui.search_bar.setStyleSheet("QLineEdit{border: 1px solid #8f8f91; "
                                             "border-top-left-radius: 5px; "
                                             "border-bottom-left-radius: 5px; "
                                             "padding-left: 5px; font: 14px;}")
            return

        self.ui.search_bar.setStyleSheet("QLineEdit{border: 2px solid orange; "
                                         "border-top-left-radius: 5px; "
                                         "border-bottom-left-radius: 5px; "
                                         "padding-left: 5px; font: bold 14px;}")

    @staticmethod
    def a___________________save______():
        pass

    def help_save_setting(self):

        # ---------------------------------------

        help_settings = settings_read(file_name=help_setting_file)

        self.current_article = self.help_tree_get_short_link()

        help_settings["current_article"] = self.current_article

        # ---------------------------------------

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                help_settings["height"] = screen.height()
                help_settings["width"] = screen.width()
                help_settings["ismaximized_on"] = True

        else:

            help_settings["height"] = self.size().height()
            help_settings["width"] = self.size().width()
            help_settings["ismaximized_on"] = False

        settings_save(file_name=help_setting_file, config_datas=help_settings)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):

        super().closeEvent(event)

        self.help_save_setting()

    def changeEvent(self, event: QEvent):

        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.ismaximized_on = True

            else:
                self.ismaximized_on = False
                move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    @staticmethod
    def a___________________end_______________():
        pass

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setApplicationVersion(application_version)
#
#     font = app.font()
#     font.setFamily("Segoe UI")
#     font.setPointSize(taille_police)
#     app.setFont(font)
#
#     app.setStyle('Fusion')
#
#     app.setStyleSheet("""QToolTip {background-color: white; padding: 2px;  border: 2px solid #E7E7E7}""")
#
#     ex = HelpWidget(asc=None)
#
#     sys.exit(app.exec_())
