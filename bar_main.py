#!/usr/bin/python3
# -*- coding: utf-8 -*

import shutil

from catalog import WidgetCatalogNew
from catalog_manage import *
from tools import get_real_path_of_apn_file, settings_save, MyContextMenu, help_modify_tooltips, move_widget_ss_bouton
from tools import open_folder, verification_catalogue_correct, verification_nom_catalogue, browser_file
from ui_catalog_recent import Ui_CatalogRecent


class CatalogRecentCategory:

    def __init__(self, icons: QIcon, categorie_data: str, categorie_title: str):
        super().__init__()

        self.categorie_data = categorie_data

        # --------

        font_bold = QStandardItem().font()
        font_bold.setBold(True)

        # --------

        self.qs_type = QStandardItem()
        self.qs_type.setIcon(icons)
        self.qs_type.setData(categorie_data, user_data_type)
        self.qs_type.setFlags(Qt.ItemIsEnabled)
        self.qs_type.setData(QColor("#BAD0E7"), Qt.BackgroundRole)

        # --------

        qs_categorie = QStandardItem(categorie_title)
        qs_categorie.setFont(font_bold)
        qs_categorie.setFlags(Qt.ItemIsEnabled)
        qs_categorie.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        qs_categorie.setData(QColor("#BAD0E7"), Qt.BackgroundRole)
        qs_categorie.setData(QColor("#4D4D4D"), Qt.ForegroundRole)

        # --------

        qs_del = QStandardItem()
        qs_del.setFlags(Qt.ItemIsEnabled)
        qs_del.setData(QColor("#BAD0E7"), Qt.BackgroundRole)

        # --------

        self.qs_list = [self.qs_type, qs_categorie, qs_del]

        # --------

        self.titles = list()
        self.child = dict()

        # --------

    def add_child(self, title: str, qs_list):
        self.titles.append(title)
        self.child[title] = qs_list

    def sort_and_add(self) -> list:
        self.titles.sort()

        for title in self.titles:
            self.qs_type.appendRow(self.child[title])

        return self.qs_list


class CatalogRecentItem:

    def __init__(self, title: str, qs_list: list):
        super().__init__()

        self.title = title
        self.qs_list = qs_list


class CatalogRecent(QWidget):
    recent_open_cat = pyqtSignal(str)

    def __init__(self, allplan: AllplanDatas):
        super().__init__()

        self.setWindowFlags(Qt.Popup)

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.allplan = allplan

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_CatalogRecent()
        self.ui.setupUi(self)

        get_look_treeview(self.ui.hierarchy_recent)

        # -----------------------------------------------
        # Model & filter
        # -----------------------------------------------
        self.recent_model = QStandardItemModel()

        self.recent_filter = QSortFilterProxyModel()
        self.recent_filter.setRecursiveFilteringEnabled(False)
        self.recent_filter.setFilterRole(user_data_type)
        self.recent_filter.setSourceModel(self.recent_model)

        self.ui.hierarchy_recent.setModel(self.recent_filter)

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.catalog_path = ""
        self.other_title = self.tr("Autre").upper()
        self.demo_title = self.tr("Catalogue de démo").upper()
        self.change = False
        self.change_settings = False

        self.demo_year_set = set()

        # -----------------------------------------------
        # Signals
        # -----------------------------------------------

        self.ui.etc_bt.clicked.connect(self.recent_button_clicked)
        self.ui.std_bt.clicked.connect(self.recent_button_clicked)
        self.ui.demo_bt.clicked.connect(self.recent_button_clicked)
        self.ui.other_bt.clicked.connect(self.recent_button_clicked)

        self.ui.a2022_bt.clicked.connect(self.recent_button_clicked)
        self.ui.a2023_bt.clicked.connect(self.recent_button_clicked)
        self.ui.a2024_bt.clicked.connect(self.recent_button_clicked)
        self.ui.a2025_bt.clicked.connect(self.recent_button_clicked)
        self.ui.a2026_bt.clicked.connect(self.recent_button_clicked)

        self.ui.hierarchy_recent.clicked.connect(self.recent_item_clicked)

        # -----------------------------------------------

        self.recent_load_settings()

    @staticmethod
    def a___________________initialized______():
        pass

    def recent_load_settings(self):

        recent_config = settings_read(recent_config_file)

        if not isinstance(recent_config, dict):
            recent_config = dict(recent_config_dict)

        # -------

        etc = recent_config.get("etc", recent_config_dict.get("etc", True))

        if isinstance(etc, bool):
            self.ui.etc_bt.setChecked(etc)

        # -------

        std = recent_config.get("std", recent_config_dict.get("std", True))

        if isinstance(std, bool):
            self.ui.std_bt.setChecked(std)

        # -------

        demo = recent_config.get("demo", recent_config_dict.get("demo", True))

        if isinstance(demo, bool):
            self.ui.demo_bt.setChecked(demo)

        # -------

        other = recent_config.get("other", recent_config_dict.get("other", True))

        if isinstance(other, bool):
            self.ui.other_bt.setChecked(other)

        # -------

        a2022 = recent_config.get("2022", recent_config_dict.get("2022", True))

        if isinstance(a2022, bool):
            self.ui.a2022_bt.setChecked(a2022)

        # -------

        a2023 = recent_config.get("2023", recent_config_dict.get("2023", True))

        if isinstance(a2023, bool):
            self.ui.a2023_bt.setChecked(a2023)

        # -------

        a2024 = recent_config.get("2024", recent_config_dict.get("2024", True))

        if isinstance(a2024, bool):
            self.ui.a2024_bt.setChecked(a2024)

        # -------

        a2025 = recent_config.get("2025", recent_config_dict.get("2025", True))

        if isinstance(a2025, bool):
            self.ui.a2025_bt.setChecked(a2025)

        # -------

        a2026 = recent_config.get("2026", recent_config_dict.get("2026", True))

        if isinstance(a2026, bool):
            self.ui.a2026_bt.setChecked(a2026)

    def recent_show(self, catalog_path: str) -> bool:

        self.change = False
        self.change_settings = False

        self.recent_model.clear()

        self.catalog_path = catalog_path

        catalog_list = settings_list(cat_list_file)

        if not isinstance(catalog_list, list):
            print("catalog_recent -- catalog_recent_show -- not isinstance(catalog_list, list)")
            return False

        # -------------

        etc_path_dict = dict()
        std_path_dict = dict()

        category_title_dict = dict()
        category_title_list = list()

        category_set = set()
        year_set = set()

        demo_set = set()

        if self.allplan.langue == "FR":
            catalog_demo = "CMI"

        elif self.allplan.langue == "DE":
            catalog_demo = "Allplan"

        else:
            catalog_demo = f"Allplan_{self.allplan.langue.lower()}"

        # -------------

        for year, version_allplan in self.allplan.version_datas.items():

            if not isinstance(version_allplan, AllplanPaths):
                print("catalog_recent -- catalog_recent_show -- not isinstance(version_allplan, AllplanPaths)")
                continue

            etc_cat_path = version_allplan.etc_cat_path

            if os.path.exists(etc_cat_path):

                etc_path_dict[etc_cat_path.lower()] = year

                # -------

                demo_cat_path = f"{etc_cat_path}{catalog_demo}.xml"

                category_title = self.demo_title

                # -------

                if os.path.exists(demo_cat_path):

                    self.demo_year_set.add(year)

                    demo_set.add(demo_cat_path.lower())

                    if year not in year_set:
                        year_set.add(year)

                    if category_title not in category_title_dict:

                        category_obj = CatalogRecentCategory(icons=get_icon(":/Images/demo.png"),
                                                             categorie_data=f"{category_title} 202X",
                                                             categorie_title=category_title)

                        category_title_dict[category_title] = category_obj
                        category_set.add(category_title)

                    else:

                        category_obj = category_title_dict[category_title]

                    # -------------

                    self.recent_add_path(title=f"{catalog_demo} {year}", catalog_path=demo_cat_path,
                                         categorie_data=f"{category_title} {year}", category_obj=category_obj,
                                         locked=True)

            # -------------

            std_cat_path = version_allplan.std_cat_path

            if os.path.exists(std_cat_path):
                std_path_dict[std_cat_path.lower()] = year

        # -------------

        for catalog_path in catalog_list:

            if catalog_path.lower() in demo_set:
                continue

            if not isinstance(catalog_path, str):
                print("catalog_recent -- catalog_recent_show -- not isinstance(catalog_path, str)")
                self.change = True
                continue

            if not os.path.exists(catalog_path):
                print("catalog_recent -- catalog_recent_show -- not os.path.exists(catalog_path)")
                self.change = True
                continue

            folder = find_folder_path(file_path=catalog_path).lower()
            title = find_filename(file_path=catalog_path)

            if folder in etc_path_dict:
                category = "ETC"
                year = etc_path_dict[folder]
                category_title = categorie_data = f"{category} {year}"
                icons = get_icon(":/Images/etc.png")

                if year not in year_set:
                    year_set.add(year)

                if category_title not in category_title_list:
                    category_title_list.append(category_title)

            elif folder in std_path_dict:
                category = "STD"
                year = std_path_dict[folder]
                category_title = categorie_data = f"{category} {year}"
                icons = get_icon(":/Images/std.png")

                if year not in year_set:
                    year_set.add(year)

                if category_title not in category_title_list:
                    category_title_list.append(category_title)

            else:
                year = "20XX"
                category = category_title = self.other_title
                categorie_data = f"{category} {year}"
                icons = get_icon(":/Images/usr.png")

            # -------

            if category not in category_set:
                category_set.add(category)

            # -------

            if category_title not in category_title_dict:

                category_obj = CatalogRecentCategory(icons=icons,
                                                     categorie_data=categorie_data,
                                                     categorie_title=category_title)

                category_title_dict[category_title] = category_obj

            else:

                category_obj = category_title_dict[category_title]

            # -------

            locked = catalog_path == self.catalog_path

            self.recent_add_path(title=title, catalog_path=catalog_path, categorie_data=category_obj.categorie_data,
                                 category_obj=category_obj, locked=locked)

        # -------

        if self.demo_title in category_title_dict:
            category_obj = category_title_dict[self.demo_title]
            self.recent_model.appendRow(category_obj.sort_and_add())

        if self.other_title in category_title_dict:
            category_obj = category_title_dict[self.other_title]
            self.recent_model.appendRow(category_obj.sort_and_add())

        category_title_list.sort(reverse=True)

        for category_title in category_title_list:
            category_obj = category_title_dict[category_title]
            self.recent_model.appendRow(category_obj.sort_and_add())

        # -------

        self.recent_button_clicked()

        self.ui.hierarchy_recent.expandAll()

        self.recent_header_manage()

        # -------

        if "ETC" not in category_set:
            self.ui.etc_bt.setChecked(False)
            self.ui.etc_bt.setVisible(False)

        if "STD" not in category_set:
            self.ui.std_bt.setChecked(False)
            self.ui.std_bt.setVisible(False)

        if self.demo_title not in category_set:
            self.ui.demo_bt.setChecked(False)
            self.ui.demo_bt.setVisible(False)

        if self.other_title not in category_set:
            self.ui.other_bt.setChecked(False)
            self.ui.other_bt.setVisible(False)

        # -------

        if "2022" not in year_set:
            self.ui.a2022_bt.setChecked(False)
            self.ui.a2022_bt.setVisible(False)

        if "2023" not in year_set:
            self.ui.a2023_bt.setChecked(False)
            self.ui.a2023_bt.setVisible(False)

        if "2024" not in year_set:
            self.ui.a2024_bt.setChecked(False)
            self.ui.a2024_bt.setVisible(False)

        if "2025" not in year_set:
            self.ui.a2025_bt.setChecked(False)
            self.ui.a2025_bt.setVisible(False)

        if "2026" not in year_set:
            self.ui.a2026_bt.setChecked(False)
            self.ui.a2026_bt.setVisible(False)

        self.show()

    def recent_add_path(self, title: str, catalog_path: str, categorie_data: str, category_obj: CatalogRecentCategory,
                        locked=False):

        qs_open = QStandardItem(get_icon(catalog_icon), "")
        qs_open.setData(categorie_data, user_data_type)
        qs_open.setToolTip(self.tr("Afficher ce catalogue dans votre explorateur de fichier"))

        # --------

        qs_title = QStandardItem(title)
        qs_title.setToolTip(catalog_path)

        # --------

        qs_del = QStandardItem(get_icon(delete_icon), "")
        qs_del.setToolTip(self.tr("Supprimer ce catalogue de la liste"))

        if locked:
            qs_del.setEnabled(False)

            font_italic = qs_title.font()

            if self.demo_title in categorie_data:
                qs_del.setToolTip(self.tr("Suppression impossible : Catalogue de démo"))
                font_italic.setItalic(True)
                qs_title.setFont(font_italic)

            else:
                font_italic.setBold(True)
                qs_title.setFont(font_italic)
                qs_del.setToolTip(self.tr("Suppression impossible : Catalogue actif"))

        else:

            qs_del.setToolTip(self.tr("Supprimer ce catalogue de la liste"))

        # --------

        category_obj.add_child(title=title, qs_list=[qs_open, qs_title, qs_del])

    def recent_header_manage(self):

        self.ui.hierarchy_recent.setHeaderHidden(False)

        self.ui.hierarchy_recent.setColumnWidth(0, 70)
        self.ui.hierarchy_recent.setColumnWidth(2, 20)

        self.ui.hierarchy_recent.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.hierarchy_recent.setHeaderHidden(True)

    @staticmethod
    def a___________________hierarchy_clicked______():
        pass

    def recent_item_clicked(self):

        qm_selected_list = self.ui.hierarchy_recent.selectionModel().selectedIndexes()

        if len(qm_selected_list) == 0:
            return

        qm = qm_selected_list[0]

        if not qm_check(qm):
            print("catalog_recent -- recent_item_clicked -- not qm_check(qm)")
            return

        column = qm.column()

        qm_parent = qm.parent()

        if not qm_check(qm_parent):
            print("catalog_recent -- recent_item_clicked -- not qm_check(qm_parent)")
            return

        if column != 1:

            qm = self.recent_filter.index(qm.row(), 1, qm_parent)

            if not qm_check(qm):
                print("catalog_recent -- recent_item_clicked -- not qm_check(qm) 2")
                return

        file_path = qm.data(Qt.ToolTipRole)

        if column == 0:
            open_folder(find_folder_path(file_path=file_path))
            return

        if column == 1:
            self.recent_open_cat.emit(file_path)
            return

        if column == 2:
            self.recent_filter.removeRow(qm.row(), qm_parent)
            self.change = True

    @staticmethod
    def a___________________button_clicked______():
        pass

    def recent_button_clicked(self):

        self.change_settings = True

        folder_list = list()
        other = False
        demo = False

        if self.ui.etc_bt.isChecked():
            folder_list.append("ETC")

        if self.ui.std_bt.isChecked():
            folder_list.append("STD")

        if self.ui.demo_bt.isChecked():
            folder_list.append(self.demo_title)
            demo = True

        if self.ui.other_bt.isChecked():
            folder_list.append(self.other_title)
            other = True

        if len(folder_list) == 0:
            self.recent_filter.setFilterRegExp("")
            self.ui.hierarchy_recent.expandAll()
            return

        pattern = f"^({'|'.join(folder_list)})"

        # --------------

        year_list = list()
        demo_count = 0

        if self.ui.a2022_bt.isChecked():
            year_list.append("2022")
            demo_count += demo and "2022" in self.demo_year_set

        if self.ui.a2023_bt.isChecked():
            year_list.append("2023")
            demo_count += demo and "2023" in self.demo_year_set

        if self.ui.a2024_bt.isChecked():
            year_list.append("2024")
            demo_count += demo and "2024" in self.demo_year_set

        if self.ui.a2025_bt.isChecked():
            year_list.append("2025")
            demo_count += demo and "2025" in self.demo_year_set

        if self.ui.a2026_bt.isChecked():
            year_list.append("2026")
            demo_count += demo and "2026" in self.demo_year_set

        if demo_count != 0:
            year_list.append("202X")

        if len(year_list) != 0:

            if other:
                year_list.append("20XX")

            pattern += f".*({'|'.join(year_list)})$"
            self.recent_filter.setFilterRegExp(pattern)
            self.ui.hierarchy_recent.expandAll()
            return

        self.recent_filter.setFilterRegExp(pattern)
        self.ui.hierarchy_recent.expandAll()

    @staticmethod
    def a___________________save______():
        pass

    def recent_save_list(self):

        row_count = self.recent_model.rowCount()

        catalog_list = list()

        for index_row in range(row_count):

            qs_parent = self.recent_model.item(index_row, 0)

            if not isinstance(qs_parent, QStandardItem):
                print("catalog_recent -- recent_save_list -- not isinstance(qs, QStandardItem)")
                continue

            children_count = qs_parent.rowCount()

            for index_child_row in range(children_count):

                qs_title = qs_parent.child(index_child_row, 1)

                if not isinstance(qs_title, QStandardItem):
                    print("catalog_recent -- recent_save_list -- not isinstance(qs, QStandardItem)")
                    continue

                catalog_path = qs_title.toolTip()

                if not isinstance(catalog_path, str):
                    print("catalog_recent -- recent_save_list -- not isinstance(catalog_path, str)")
                    continue

                if not os.path.exists(catalog_path):
                    print("catalog_recent -- recent_save_list -- not os.path.exists(catalog_path)")
                    continue

                if catalog_path in catalog_list:
                    print("catalog_recent -- recent_save_list -- catalog_path in catalog_list")
                    continue

                catalog_list.append(catalog_path)

        print(catalog_list)

        settings_save(cat_list_file, catalog_list)

    def recent_save_setting(self):

        config_datas = {"etc": self.ui.etc_bt.isChecked(),
                        "std": self.ui.std_bt.isChecked(),
                        "demo": self.ui.demo_bt.isChecked(),
                        "other": self.ui.other_bt.isChecked(),
                        "2022": self.ui.a2022_bt.isChecked(),
                        "2023": self.ui.a2023_bt.isChecked(),
                        "2024": self.ui.a2024_bt.isChecked(),
                        "2025": self.ui.a2025_bt.isChecked(),
                        "2026": self.ui.a2026_bt.isChecked()}

        settings_save(file_name=recent_config_file, config_datas=config_datas)

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.change:
            self.recent_save_list()

        if self.change_settings:
            self.recent_save_setting()

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class MainBar(QObject):

    def __init__(self, asc, new_catalog_widget: WidgetCatalogNew):
        super().__init__()

        self.asc = asc
        self.new_catalog_widget = new_catalog_widget

        self.menu_cat_recent = MyContextMenu()

        self.ui: Ui_MainWindow = self.asc.ui
        self.catalog: CatalogDatas = self.asc.catalog
        self.allplan: AllplanDatas = self.asc.allplan

        # ---------------------------------------

        self.recent_widget = CatalogRecent(allplan=self.allplan)

        self.asc.langue_change.connect(lambda main=self.recent_widget: self.ui.retranslateUi(main))

        self.recent_widget.recent_open_cat.connect(self.catalog_open_file)

        # ---------------------------------------

        self.dossier_defaut_ouvrir = ""

        # ---------------------------------------
        # CHARGEMENT Catalogue - Fichier
        # ---------------------------------------

        self.ui.new_bt.clicked.connect(self.catalogue_nouveau)
        help_modify_tooltips(widget=self.ui.new_bt, short_link=help_cat_new_cat, help_text=self.asc.help_tooltip)

        # -----

        self.ui.open_bt.clicked.connect(self.catalog_open_browse)
        help_modify_tooltips(widget=self.ui.open_bt, short_link=help_cat_open_cat, help_text=self.asc.help_tooltip)

        # -----

        self.ui.open_list_bt.clicked.connect(self.menu_cat_recent_show)
        self.ui.open_list_bt.customContextMenuRequested.connect(self.menu_cat_recent_show)

        # ---------------------------------------
        # CHARGEMENT Catalogue - Paramètre
        # ---------------------------------------

        self.ui.parameters_bt.clicked.connect(self.catalogue_modifier_parametres)
        help_modify_tooltips(widget=self.ui.parameters_bt,
                             short_link=help_cat_settings,
                             help_text=self.asc.help_tooltip)

        # ---------------------------------------
        # CHARGEMENT Catalogue - Enregistrer
        # ---------------------------------------

        self.ui.save_bt.clicked.connect(self.catalog.catalog_save)
        help_modify_tooltips(widget=self.ui.save_bt, short_link=help_cat_save, help_text=self.asc.help_tooltip)

        self.ui.update_cat_bt.clicked.connect(self.asc.catalogue_update)
        help_modify_tooltips(widget=self.ui.update_cat_bt, short_link=help_cat_update, help_text=self.asc.help_tooltip)

        self.ui.save_as_bt.clicked.connect(self.catalog_save_as)
        help_modify_tooltips(widget=self.ui.save_as_bt, short_link=help_cat_save_as, help_text=self.asc.help_tooltip)

    @staticmethod
    def a___________________nouveau______():
        pass

    def catalogue_nouveau(self):

        self.asc.formula_widget_close()

        self.new_catalog_widget.personnalisation(new=True)

    def catalogue_importer(self):

        self.asc.formula_widget_close()

        self.new_catalog_widget.personnalisation(convert_bdd=True)

    @staticmethod
    def a___________________ouvrir______():
        pass

    def catalog_open_browse(self):

        self.asc.formula_widget_close()

        if not self.catalog.catalog_save_ask():
            return

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            path_default = self.allplan.allplan_paths.std_cat_path

            shortcuts_list = [self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.tmp_path]
        else:
            path_default = ""

            shortcuts_list = list()

        chemin_fichier = browser_file(parent=self.asc,
                                      title=application_title,
                                      registry=[app_setting_file, "path_catalog_open"],
                                      shortcuts_list=shortcuts_list,
                                      datas_filters={self.tr("Fichier Catalogue"): [".xml", ".apn", ".prj"]},
                                      current_path=self.catalog.catalog_path,
                                      default_path=path_default,
                                      use_setting_first=True)

        if chemin_fichier == "":
            return

        if chemin_fichier.endswith(".apn") or chemin_fichier.endswith(".prj"):

            # version_current = self.allplan.allplan_paths

            # todo à modifier

            if "2024" in self.allplan.version_datas:

                version_obj = self.allplan.version_datas["2024"]

                if not isinstance(version_obj, AllplanPaths):
                    return

                chemin_prj = version_obj.prj_path

            elif "2025" not in self.allplan.version_datas:

                version_obj = self.allplan.version_datas["2025"]

                if not isinstance(version_obj, AllplanPaths):
                    return

                chemin_prj = version_obj.prj_path

            else:
                return

            chemin_catalogue_tmp = get_real_path_of_apn_file(chemin_fichier, chemin_prj, True)

            if chemin_catalogue_tmp == "":
                return

            chemin_fichier = chemin_catalogue_tmp

        if verification_catalogue_correct(chemin_fichier, True) == "":
            return

        print(f"onglet_catalogue -- catalogue_ouvrir -- lancer chargement catalogue : {chemin_fichier}")

        self.catalog.catalog_load_start(catalog_path=chemin_fichier)

    def menu_cat_recent_show(self):

        move_widget_ss_bouton(self.ui.open_list_bt, self.recent_widget)

        self.recent_widget.recent_show(catalog_path=self.catalog.catalog_path)

    def catalog_open_file(self, chemin_fichier: str):
        print(f"onglet_hierarchie -- menu_bt_charger -- lancer chargement catalogue : {chemin_fichier}")

        self.asc.formula_widget_close()

        self.menu_cat_recent.close()

        if not self.catalog.catalog_save_ask():
            return

        self.catalog.catalog_load_start(catalog_path=chemin_fichier)

    @staticmethod
    def a___________________parametres______():
        pass

    def catalogue_modifier_parametres(self):

        self.asc.formula_widget_close()

        self.new_catalog_widget.personnalisation(modify=True)

    @staticmethod
    def a___________________enregistrer______():
        pass

    def catalog_save_as(self):

        self.asc.formula_widget_close()

        if self.catalog.catalog_path == "":
            return

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            path_default = self.allplan.allplan_paths.std_cat_path

            shortcuts_list = [self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.tmp_path]
        else:
            path_default = ""

            shortcuts_list = list()

        catalog_path_new = browser_file(parent=self.asc,
                                        title=application_title,
                                        registry=[app_setting_file, "path_catalog_save"],
                                        shortcuts_list=shortcuts_list,
                                        datas_filters={self.tr("Fichier Catalogue"): [".xml"]},
                                        current_path=self.catalog.catalog_path,
                                        default_path=path_default,
                                        file_name=self.catalog.catalog_name,
                                        use_setting_first=True,
                                        use_save=True)

        if catalog_path_new == self.catalog.catalog_path or catalog_path_new == "":
            return

        catalog_path_new = verification_nom_catalogue(catalog_path_new)

        # ---------------------
        # Dossier settings
        # ---------------------

        settings_folder_new = get_catalog_setting_folder(catalog_folder=find_folder_path(catalog_path_new))

        catalog_name = find_filename(catalog_path_new)

        # ---------------------
        # Dossier path INI
        # ---------------------

        if os.path.exists(self.catalog.catalog_setting_path_file):

            setting_path_file_new = get_catalog_setting_path_file(catalog_settings_folder=settings_folder_new,
                                                                  catalog_name=catalog_name)

            try:
                shutil.copy(self.catalog.catalog_setting_path_file, setting_path_file_new)

            except Exception as erreur:

                msg(titre=application_title,
                    message=self.tr("Une erreur est survenue."),
                    icone_avertissement=True,
                    details=f"{erreur}")

                return

        else:
            return

        # ---------------------
        # Dossier Affichage
        # ---------------------

        if os.path.exists(self.catalog.catalog_setting_display_file):

            setting_display_file_new = get_catalog_setting_display_file(catalog_settings_folder=settings_folder_new,
                                                                        catalog_name=catalog_name)

            try:
                shutil.copy(self.catalog.catalog_setting_display_file, setting_display_file_new)
            except Exception as erreur:

                msg(titre=application_title,
                    message=self.tr("Une erreur est survenue."),
                    icone_avertissement=True,
                    details=f"{erreur}")

                return

        else:
            return

        # ---------------------
        # Catalogue
        # ---------------------

        CatalogSave(asc=self.asc, catalog=self.catalog, allplan=self.allplan,
                    catalog_path=catalog_path_new,
                    catalog_setting_display_file=setting_display_file_new)

        if msg(titre=application_title,
               message=self.tr("Voulez-vous ouvrir ce nouveau catalogue?"),
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               defaut_bouton=QMessageBox.No,
               icone_ouvrir=True) == QMessageBox.Ok:
            print(f"onglet_catalogue -- catalogue_enregistrer_sous -- lancer chargement catalogue : {catalog_path_new}")

            if not self.catalog.catalog_save_ask():
                return

            self.catalog.catalog_load_start(catalog_path=catalog_path_new)

        else:

            settings_save_value(file_name=app_setting_file, key_name="path_catalog", value=catalog_path_new)

            catalog_opened_list = settings_list(file_name=cat_list_file, ele_add=catalog_path_new)

            self.asc.open_list_manage(catalog_opened_list=catalog_opened_list)

    @staticmethod
    def a___________________end______():
        pass
