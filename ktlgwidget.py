#!/usr/bin/python3
# -*- coding: utf-8 -*

import os.path

from PyQt5.Qt import *
from lxml import etree

from allplan_manage import AllplanDatas, AllplanPaths, AttributeDatas
from main_datas import favorite_save_icon, select_none_icon, catalog_icon, reset_icon, browser_icon, refresh_icon
from main_datas import allplan_icon, external_bdd_nevaris_icon, external_bdd_bcm_icon, external_bdd_frilo
from main_datas import get_icon, folder_icon, user_data_number, select_all_icon, user_data_type, favorite_open_icon
from main_datas import open_icon, open_text_editor_icon, cat_list_file, external_bdd_bimplus_icon
from tools import afficher_message, make_backup, find_folder_path, find_filename, settings_list, copy_to_clipboard
from tools import xml_load_root, get_look_treeview, qm_check, MyContextMenu, find_global_point, browser_file
from tools import open_folder, open_file
from ui_ktlg import Ui_Ktlg
from ui_ktlg_light import Ui_KtlgLight


class Makro(QStandardItem):

    def __init__(self, text: str, id_val: str, title: str, virtual_order: str):
        super().__init__()

        # ----------------
        # MakroTyp Data
        # ----------------
        self.id_val = id_val

        # ----------------
        # Translation id -> Category Name
        # ----------------

        self.title = title

        self.setText(text)

        # ----------------
        # Virtual Order in View
        # ----------------

        self.setData(virtual_order, user_data_number)

        # ----------------

        self.setFlags(Qt.ItemIsEnabled)

        # ----------------

        if text != "":
            self.setIcon(get_icon(folder_icon))

            font_qs = self.font()
            font_qs.setBold(True)
            self.setFont(font_qs)


class MakroAttribute(QStandardItem):

    def __init__(self, text: str, id_val: str, catalog_id: str,
                 virtual_order: str, is_default: bool, catalog_name_default: str):
        super().__init__()

        self.setText(text)

        # ----------------
        # MaterialTyp Data
        # ----------------

        self.id_val = id_val
        self.catalog_id = catalog_id

        # ----------------
        # if this attribute is the default attribute in this MacroTyp
        # ----------------
        self.is_default = is_default

        # ----------------
        # Virtual Order in View
        # ----------------

        self.setData(virtual_order, user_data_number)

        # ----------------
        # The default catalog name if reset
        # ----------------
        self.catalog_name_default = catalog_name_default

        # ----------------

        if self.is_default:
            self.setForeground(QColor("red"))
            font_qs = self.font()
            font_qs.setBold(True)
            self.setFont(font_qs)

            self.setForeground(QColor("red"))
            self.setFont(font_qs)

            self.setData("Default", user_data_type)


class KtlgLightWidget(QWidget):
    more_options = pyqtSignal()
    default_clicked = pyqtSignal()
    current_clicked = pyqtSignal()
    favorite_changed = pyqtSignal(str)

    def __init__(self, allplan: AllplanDatas):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_KtlgLight()
        self.ui.setupUi(self)

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.allplan = allplan

        # ---------------------------------------
        # VARIABLES
        # ---------------------------------------

        self.file_path = ""

        # -----------------------------------------------
        # Signals
        # -----------------------------------------------

        self.ui.default_bt.clicked.connect(self.default_clicked.emit)

        self.ui.current_bt.clicked.connect(self.current_clicked.emit)

        # ----------

        self.ui.option_bt.clicked.connect(self.more_options.emit)

        self.ui.favorite_bt.clicked.connect(self.light_favorite)

        # ----------

        self.ui.quit_bt.clicked.connect(self.close)

    @staticmethod
    def a___________________light______():
        pass

    def light_favorite(self):

        file_txt = self.tr("Fichier")

        datas_filters = {f"{file_txt} XML": [".xml"]}

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [f"{self.allplan.allplan_paths.usr_path}Local\\",
                              self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=self.tr("Bibliothèque assignée"),
                                 registry=[],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters=datas_filters,
                                 current_path=self.file_path,
                                 default_path="",
                                 use_setting_first=False)

        if file_path == "":
            return

        root = xml_load_root(file_path=file_path)

        if not isinstance(root, etree._Element):
            afficher_message(titre=self.tr("Bibliothèque assignée"),
                             message=self.tr("Cette base de données n'a pas été reconnue."),
                             icone_critique=True)
            return False

        if root.tag != "CatalogData":
            afficher_message(titre=self.tr("Bibliothèque assignée"),
                             message=self.tr("Cette base de données n'a pas été reconnue."),
                             icone_critique=True)
            return False

        self.favorite_changed.emit(file_path)


class KtlgWidget(QWidget):

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_Ktlg()

        self.ui.setupUi(self)

        get_look_treeview(self.ui.ktlg_view)

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.allplan: AllplanDatas = self.asc.allplan

        # ---------------------------------------
        # VARIABLES
        # ---------------------------------------

        self.file_path = "C:\\Users\\jmauger\\Documents\\Nemetschek\\Allplan\\2025\\Usr\\Local\\ktlg.xml"

        self.catalog_current = ""

        # ------

        self.table_makro_name = dict()

        self.table_makro_order = {"1": "01",
                                  "2": "05",
                                  "3": "06",
                                  "4": "?",
                                  "5": "04",
                                  "6": "?",
                                  "7": "07",
                                  "8": "10",
                                  "9": "03",
                                  "10": "02",
                                  "11": "09",
                                  "12": "08",
                                  "13": "?",
                                  "14": "?"}

        self.table_makro_name_dafault = {"1": "katlg1",
                                         "2": "katlg1",
                                         "3": "katlg1",
                                         "4": "katlg1",
                                         "5": "katlg5",
                                         "6": "?",
                                         "7": "katlg7",
                                         "8": "katlg8",
                                         "9": "katlg9",
                                         "10": "katlg7",
                                         "11": "katlg10",
                                         "12": "katlg11",
                                         "13": "katlg1",
                                         "14": "katlg1"}

        self.table_makro_attribute_default = {"1": "1",
                                              "2": "1",
                                              "3": "1",
                                              "4": "?",
                                              "5": "5",
                                              "6": "?",
                                              "7": "5",
                                              "8": "5",
                                              "9": "1",
                                              "10": "1",
                                              "11": "5",
                                              "12": "5",
                                              "13": "?",
                                              "14": "?"}

        # ------------

        self.table_attribute_names = {"1": "508", "5": "507", "2": "570", "3": "571", "4": "574", "6": "575"}

        self.table_attribute_order = {"1": "1", "5": "2", "2": "3", "3": "4", "4": "5", "6": "6"}

        # ------------

        self.table_other_db = {"111": "ALLPLAN BCM",
                               "115": "BIMPLUS",
                               "114": "NEVARIS",
                               "110": "NORMEN",
                               "113": "STATIK"}

        self.table_other_db_icon = {"111": external_bdd_bcm_icon,
                                    "115": external_bdd_bimplus_icon,
                                    "114": external_bdd_nevaris_icon,
                                    "110": allplan_icon,
                                    "113": external_bdd_frilo}

        # ------------------------
        # Model & Filter
        # ------------------------

        self.ktlg_model = QStandardItemModel()
        self.ktlg_filter = QSortFilterProxyModel()
        self.ktlg_filter.setSortRole(user_data_number)
        self.ktlg_filter.setSourceModel(self.ktlg_model)
        self.ktlg_filter.setFilterRegExp(r"^[^?]")

        self.ui.ktlg_view.setModel(self.ktlg_filter)

        # ------------------------
        # Signals
        # ------------------------

        self.ui.open_favorite_bt.clicked.connect(self.ktlg_favorite_open_clicked)
        self.ui.save_favorite_bt.clicked.connect(self.ktlg_favorite_save_clicked)

        # -----

        self.ui.select_bt.clicked.connect(self.ktlg_select_clicked)
        self.ui.select_none_bt.clicked.connect(self.ktlg_select_none_clicked)

        # ----

        self.ui.current_bt.clicked.connect(self.ktlg_curent_clicked)
        self.ui.default_bt.clicked.connect(self.ktlg_default_clicked)

        self.ui.browser_bt.clicked.connect(self.ktlg_browser_clicked)

        # ----

        self.ui.tools_bt.clicked.connect(self.ktlg_tools_clicked)

        # ----

        self.ui.ktlg_view.selectionModel().selectionChanged.connect(self.ktlg_selection_changed)
        self.ui.ktlg_view.customContextMenuRequested.connect(self.ktlg_menu)

        # ----

        self.ui.save_bt.clicked.connect(self.ktlg_save_xml_current)

        self.ui.quit_bt.clicked.connect(self.close)

        # ------------------------
        # Light Widget
        # ------------------------

        self.light_widget = KtlgLightWidget(allplan=self.allplan)

        self.asc.langue_change.connect(lambda main=self: self.light_widget.ui.retranslateUi(main))

        # ------------------------
        # Signals - Light Widget
        # ------------------------

        self.light_widget.more_options.connect(self.ktlg_light_options_clicked)

        self.light_widget.current_clicked.connect(self.ktlg_light_current_clicked)
        self.light_widget.default_clicked.connect(self.ktlg_light_default_clicked)

        self.light_widget.favorite_changed.connect(self.ktlg_light_favorite_changed)

    @staticmethod
    def a___________________load______():
        pass

    def load_settings(self):
        pass

    def ktlg_load_current_file(self) -> bool:
        return self.ktlg_load_file(file_path=self.file_path)

    def ktlg_load_file(self, file_path: str, update_title=True):

        if not os.path.exists(file_path):
            print("Ktlg -- ktlg_load_file -- not os.path.exists(file_path)")
            return False

        # ------

        root = xml_load_root(file_path=file_path)

        if not isinstance(root, etree._Element):
            print("Ktlg -- ktlg_load_file -- not isinstance(root, etree._Element)")
            return False

        # -----

        if update_title:
            title = self.tr("Bibliothèque assignée")

            self.setWindowTitle(f"{title} -- {file_path}")

        # ------

        elements = root.findall(".//MakroTyp")

        if len(elements) == 0:
            print("Ktlg -- ktlg_load_file -- len(elements) == 0")
            afficher_message(titre=self.tr("Bibliothèque assignée"),
                             message=self.tr("Une erreur est survenue."))
            return False

        # ------

        if self.ktlg_model.rowCount() != 0:
            self.ktlg_model.clear()

        self.ktlg_model.setHorizontalHeaderLabels([self.tr("Attribut"), self.tr("Catalogue")])

        # ------

        self.table_makro_name = {"1": self.tr("Élément de construction"),
                                 "2": self.tr("Surface"),
                                 "3": self.tr("Plinthe"),
                                 "4": "?",
                                 "5": self.tr("Pièce"),
                                 "6": "?",
                                 "7": self.tr("Macro"),
                                 "8": self.tr("Parcelle"),
                                 "9": self.tr("Escalier"),
                                 "10": self.tr("Macro d'appui de fenêtre"),
                                 "11": self.tr("Objet surfacique"),
                                 "12": self.tr("Objet linéaire"),
                                 "13": "?",
                                 "14": "?"}

        # ------

        for element in elements:

            # ------------------------
            # Makro
            # ------------------------

            makro_id_val = element.get("id")

            if not isinstance(makro_id_val, str):
                print("Ktlg -- ktlg_load_file -- not isinstance(makro_id_val, str)")
                continue

            # ------

            if makro_id_val not in self.table_makro_name:
                print("Ktlg -- ktlg_load_file -- makro_id_val not in self.table_makro_name")
                continue

            title = self.table_makro_name[makro_id_val]

            # ------

            if makro_id_val not in self.table_makro_order:
                print("Ktlg -- ktlg_load_file -- makro_id_val not in self.table_makro_order")
                continue

            virtual_order = self.table_makro_order[makro_id_val]

            # ------

            qs_makro_col_1 = Makro(text=title, id_val=makro_id_val, title=title, virtual_order=virtual_order)

            qs_makro_col_2 = QStandardItem()
            qs_makro_col_2.setFlags(Qt.ItemIsEnabled)

            qs_makro_list = [qs_makro_col_1, qs_makro_col_2]

            # ------------------------
            # Makro Attribute
            # ------------------------

            if makro_id_val not in self.table_makro_attribute_default:
                print("Ktlg -- ktlg_load_file -- makro_id_val not in self.table_makro_attribute_default")
                continue

            attribute_default = self.table_makro_attribute_default[makro_id_val]

            # ------

            if makro_id_val not in self.table_makro_name_dafault:
                print("Ktlg -- ktlg_load_file -- makro_id_val not in self.table_makro_name_dafault")
                continue

            catalog_name_default = self.table_makro_name_dafault[makro_id_val]

            # ------

            for material_ele in element:

                # ------

                if not isinstance(material_ele, etree._Element):
                    print("Ktlg -- ktlg_load_file -- not isinstance(material_ele, etree._Element)")
                    continue

                # ------

                attribute_id_val = material_ele.get("id")

                if not isinstance(attribute_id_val, str):
                    print("Ktlg -- ktlg_load_file -- not isinstance(attribute_id_val, str)")
                    continue

                # ------

                if attribute_id_val not in self.table_attribute_names:
                    print("Ktlg -- ktlg_load_file -- attribute_id_val not in self.table_attribute_names")
                    continue

                number = self.table_attribute_names[attribute_id_val]

                attribute_obj = self.allplan.attributes_dict.get(number)

                if not isinstance(attribute_obj, AttributeDatas):
                    print("Ktlg -- ktlg_load_file -- not isinstance(attribute_obj, AttributeDatas)")
                    continue

                attribute_number = f"{number} -- {attribute_obj.name}"

                # ------

                catalog_id = material_ele.get("catalog_id")

                if not isinstance(catalog_id, str):
                    print("Ktlg -- ktlg_load_file -- not isinstance(catalog_id, str)")
                    continue

                # ------

                if catalog_id in self.table_other_db:
                    catalog_name = self.table_other_db[catalog_id]
                else:
                    catalog_name = material_ele.get("catalog_name")

                # ------

                if not isinstance(catalog_name, str):
                    print("Ktlg -- ktlg_load_file -- not isinstance(catalog_name, str)")
                    continue

                # ------

                if attribute_id_val not in self.table_attribute_order:
                    print("Ktlg -- ktlg_load_file -- attribute_id_val not in self.table_attribute_order")
                    continue

                attribute_order = self.table_attribute_order[attribute_id_val]

                # --------

                is_default = attribute_default == attribute_id_val

                # --------

                qs_makro_attribute = MakroAttribute(text=attribute_number,
                                                    id_val=attribute_id_val,
                                                    catalog_id=catalog_id,
                                                    virtual_order=attribute_order, is_default=is_default,
                                                    catalog_name_default=catalog_name_default)

                qs_makro_attribute2 = MakroAttribute(text=catalog_name,
                                                     id_val=attribute_id_val,
                                                     catalog_id=catalog_id,
                                                     virtual_order=attribute_order, is_default=is_default,
                                                     catalog_name_default=catalog_name_default)

                # ------

                qs_makro_col_1.appendRow([qs_makro_attribute, qs_makro_attribute2])

                # ------

            self.ktlg_model.appendRow(qs_makro_list)

        self.ktlg_filter.sort(0, Qt.AscendingOrder)

        self.ui.ktlg_view.expandAll()

        self.ktlg_select_master()
        return True

    @staticmethod
    def a___________________buttons______():
        pass

    def ktlg_buttons_manage(self) -> None:

        select_bt = len(self.ui.ktlg_view.selectionModel().selectedRows(1)) != 0

        self.ui.current_bt.setEnabled(select_bt)
        self.ui.default_bt.setEnabled(select_bt)
        self.ui.browser_bt.setEnabled(select_bt)

        active_bt = self.ktlg_model.rowCount() != 0

        self.ui.open_favorite_bt.setEnabled(active_bt)
        self.ui.save_favorite_bt.setEnabled(active_bt)
        self.ui.select_bt.setEnabled(active_bt)
        self.ui.select_none_bt.setEnabled(active_bt)
        self.ui.tools_bt.setEnabled(active_bt)

        self.ktlg_header_manage()

    @staticmethod
    def a___________________header___________________():
        pass

    def ktlg_header_manage(self) -> bool:

        if not isinstance(self.ui.ktlg_view.header(), QHeaderView):
            print("Ktlg -- ktlg_header_manage -- not isinstance(self.ui.ktlg_view.header(), QHeaderView)")
            return False

        if self.ui.ktlg_view.header().height() != 24:
            self.ui.ktlg_view.header().setFixedHeight(24)

        size_now = self.ui.ktlg_view.header().sectionSize(0)

        hearder_size = self.ui.ktlg_view.header().width() - 50

        if size_now > hearder_size:
            size_after = hearder_size
            self.ui.ktlg_view.header().resizeSection(0, size_after)
            return True

        self.ui.ktlg_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        size_after = self.ui.ktlg_view.header().sectionSize(0)

        if size_after < size_now:
            self.ui.ktlg_view.header().setSectionResizeMode(0, QHeaderView.Interactive)
            self.ui.ktlg_view.header().resizeSection(0, size_now)

        else:
            self.ui.ktlg_view.header().setSectionResizeMode(0, QHeaderView.Interactive)

        return True

    @staticmethod
    def a___________________favorite______():
        pass

    def ktlg_favorite_open_clicked(self):

        file_txt = self.tr("Fichier")

        datas_filters = {f"{file_txt} XML": [".xml"]}

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [f"{self.allplan.allplan_paths.usr_path}Local\\",
                              self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=self.tr("Bibliothèque assignée"),
                                 registry=[],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters=datas_filters,
                                 current_path=self.file_path,
                                 default_path="",
                                 use_setting_first=False)

        if file_path == "":
            return

        root = xml_load_root(file_path=file_path)

        if not isinstance(root, etree._Element):
            afficher_message(titre=self.tr("Bibliothèque assignée"),
                             message=self.tr("Cette base de données n'a pas été reconnue."),
                             icone_critique=True)
            return False

        if root.tag != "CatalogData":
            afficher_message(titre=self.tr("Bibliothèque assignée"),
                             message=self.tr("Cette base de données n'a pas été reconnue."),
                             icone_critique=True)
            return False

        if self.ktlg_load_file(file_path=file_path, update_title=False):
            self.ui.save_bt.setEnabled(True)

    def ktlg_favorite_save_clicked(self):

        file_txt = self.tr("Fichier")

        datas_filters = {f"{file_txt} XML": [".xml"]}

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [f"{self.allplan.allplan_paths.usr_path}Local\\",
                              self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=self.tr("Bibliothèque assignée"),
                                 registry=[],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters=datas_filters,
                                 current_path=self.file_path,
                                 default_path="",
                                 use_setting_first=False,
                                 use_save=True)

        if file_path == "":
            return

        self.ktlg_save_xml(file_path=file_path)

    @staticmethod
    def a___________________selection______():
        pass

    def ktlg_selection_changed(self) -> None:
        self.ktlg_buttons_manage()

    def ktlg_select_clicked(self) -> None:

        menu = MyContextMenu(tooltips_visible=False)

        menu.add_title(title=self.tr("Sélection"))

        menu.add_action(qicon=get_icon(select_all_icon),
                        title=self.tr("Sélectionner tous"),
                        action=self.ktlg_select_all,
                        tooltips="",
                        short_link="")

        menu.add_action(qicon=get_icon(select_all_icon),
                        title=self.tr("Sélectionner les défauts"),
                        action=self.ktlg_select_master,
                        tooltips="",
                        short_link="")

        menu.exec_(find_global_point(self.ui.select_bt))

    def ktlg_select_all(self) -> None:
        self.ui.ktlg_view.selectAll()
        self.ktlg_buttons_manage()

    def ktlg_select_master(self) -> bool:

        search_start = self.ktlg_filter.index(0, 1)

        search = self.ktlg_filter.match(search_start, user_data_type, "Default", -1,
                                        Qt.MatchExactly | Qt.MatchRecursive)

        if len(search) == 0:
            print("Ktlg -- ktlg_select_master -- not isinstance(qs, MakroAttribute)")
            return False

        self.ui.ktlg_view.clearSelection()

        for qm_filter in search:
            self.ui.ktlg_view.selectionModel().select(qm_filter, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.ktlg_buttons_manage()
        return True

    def ktlg_select_none_clicked(self) -> None:
        self.ui.ktlg_view.clearSelection()
        self.ktlg_buttons_manage()

    @staticmethod
    def a___________________buttons_edit______():
        pass

    def ktlg_curent_clicked(self) -> None:
        self.ktlg_set_catalog_name(catalog_name=self.catalog_current)

    def ktlg_set_catalog_name(self, catalog_name: str, catalog_id="116"):

        qm_selection_list = self.ui.ktlg_view.selectionModel().selectedRows(1)

        for qm_filter in qm_selection_list:

            if not qm_check(qm_filter):
                print("Ktlg -- ktlg_curent_clicked -- not qm_check(qm_filter)")
                continue

            qm_model = self.ktlg_filter.mapToSource(qm_filter)

            if not qm_check(qm_model):
                print("Ktlg -- ktlg_curent_clicked -- not qm_check(qm_model)")
                continue

            qs = self.ktlg_model.itemFromIndex(qm_model)

            if not isinstance(qs, MakroAttribute):
                print("Ktlg -- ktlg_curent_clicked -- not isinstance(qs, MakroAttribute)")
                continue

            qs.setText(catalog_name)

            qs.catalog_id = catalog_id

        # -------

        self.ui.save_bt.setEnabled(True)

    def ktlg_default_clicked(self) -> None:

        qm_selection_list = self.ui.ktlg_view.selectionModel().selectedRows(1)

        for qm_filter in qm_selection_list:

            if not qm_check(qm_filter):
                print("Ktlg -- ktlg_default_clicked -- not qm_check(qm_filter)")
                continue

            qm_model = self.ktlg_filter.mapToSource(qm_filter)

            if not qm_check(qm_model):
                print("Ktlg -- ktlg_default_clicked -- not qm_check(qm_model)")
                continue

            qs = self.ktlg_model.itemFromIndex(qm_model)

            if not isinstance(qs, MakroAttribute):
                print("Ktlg -- ktlg_default_clicked -- not isinstance(qs, MakroAttribute)")
                continue

            qs.setText(qs.catalog_name_default)
            qs.catalog_id = "1006"

        # -------

        self.ui.save_bt.setEnabled(True)

    def ktlg_browser_clicked(self):

        catalog_list = settings_list(file_name=cat_list_file)

        if len(catalog_list) == 0:
            self.ktlg_browser_catalog()
            return

        names_list = list()

        menu = MyContextMenu(tooltips_visible=False)

        # ---------------- Browser

        menu.add_title(title=self.tr("Parcourir"))

        menu.add_action(qicon=get_icon(browser_icon),
                        title=self.tr("Parcourir"),
                        action=self.ktlg_browser_catalog,
                        tooltips="",
                        short_link="")

        menu.add_title(title=self.tr("Autre"))

        for other_db_index, other_db_name in self.table_other_db.items():
            icon = get_icon(self.table_other_db_icon.get(other_db_index))

            menu.add_action(qicon=icon,
                            title=other_db_name,
                            action=lambda val=other_db_name, val2=other_db_index:
                            self.ktlg_set_catalog_name(catalog_name=val, catalog_id=val2),
                            tooltips="",
                            short_link="")

        # ---------------- catalog_list_2

        menu.add_title(title=self.tr("Catalogues récents"))

        catalog_list_2 = [find_filename(file_path=file_path) for file_path in catalog_list]
        catalog_list_2.sort(key=str.lower)

        for file_path in catalog_list_2:

            file_name = find_filename(file_path=file_path)

            if file_name not in names_list:
                names_list.append(file_name)

                menu.add_action(qicon=get_icon(catalog_icon),
                                title=file_name,
                                action=lambda val=file_name: self.ktlg_set_catalog_name(catalog_name=val),
                                tooltips="",
                                short_link="")

        # ----------------

        menu.exec_(find_global_point(self.ui.browser_bt))

    def ktlg_browser_catalog(self):

        file_txt = self.tr("Fichier")

        datas_filters = {f"{file_txt} XML": [".xml"]}

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [f"{self.allplan.allplan_paths.usr_path}Local\\",
                              self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=self.tr("Bibliothèque assignée"),
                                 registry=[],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters=datas_filters,
                                 current_path=self.file_path,
                                 default_path="",
                                 use_setting_first=False)

        if file_path == "":
            return

        root = xml_load_root(file_path=file_path)

        if not isinstance(root, etree._Element):
            afficher_message(titre=self.tr("Bibliothèque assignée"),
                             message=self.tr("Cette base de données n'a pas été reconnue."),
                             icone_critique=True)
            return False

        if root.tag != "AllplanCatalog":
            text = self.tr("Le fichier ne semble pas être un Catalogue, désolé")

            afficher_message(titre=self.tr("Bibliothèque assignée"),
                             message=f"{text}!",
                             icone_critique=True)
            return False

        file_name = find_filename(file_path=file_path)

        if not file_name == "":
            self.ktlg_set_catalog_name(catalog_name=file_name)

        settings_list(cat_list_file, ele_add=file_path)

    @staticmethod
    def a___________________buttons_tools______():
        pass

    def ktlg_tools_clicked(self):

        vob_menu = MyContextMenu(tooltips_visible=False)

        vob_menu.add_action(qicon=get_icon(refresh_icon),
                            title=self.tr("Rafraichir"),
                            action=self.ktlg_load_current_file)

        vob_menu.addSeparator()

        vob_menu.add_action(qicon=get_icon(open_icon),
                            title=self.tr("Ouvrir le dossier"),
                            action=self.ktlg_tools_open_folder)

        vob_menu.add_action(qicon=get_icon(open_text_editor_icon),
                            title=self.tr("Ouvrir le fichier"),
                            action=self.ktlg_tools_open_file)

        vob_menu.exec_(find_global_point(self.ui.tools_bt))

    def ktlg_tools_open_folder(self):

        modifiers = QApplication.keyboardModifiers()

        folder_path = find_folder_path(file_path=self.file_path)

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=folder_path, show_msg=True)
            return

        open_folder(folder_path=folder_path)

    def ktlg_tools_open_file(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.file_path, show_msg=True)
            return

        open_file(file_path=self.file_path)

    @staticmethod
    def a___________________tree_menu______():
        pass

    def ktlg_menu(self, point: QPoint):

        if self.ktlg_model.rowCount() == 0:
            return

        menu = MyContextMenu(tooltips_visible=False)

        # ----------------

        menu.add_title(title=self.ui.favorite_title.text())

        menu.add_action(qicon=get_icon(favorite_open_icon),
                        title=self.ui.open_favorite_bt.toolTip(),
                        action=self.ktlg_favorite_open_clicked,
                        tooltips="",
                        short_link="")

        menu.add_action(qicon=get_icon(favorite_save_icon),
                        title=self.ui.save_favorite_bt.toolTip(),
                        action=self.ktlg_favorite_save_clicked,
                        tooltips="",
                        short_link="")

        # ----------------

        menu.add_title(title=self.ui.select_title.text())

        menu.add_action(qicon=get_icon(select_all_icon),
                        title=self.tr("Sélectionner tous"),
                        action=self.ktlg_select_all,
                        tooltips="",
                        short_link="")

        menu.add_action(qicon=get_icon(select_all_icon),
                        title=self.tr("Sélectionner les défauts"),
                        action=self.ktlg_select_master,
                        tooltips="",
                        short_link="")

        menu.add_action(qicon=get_icon(select_none_icon),
                        title=self.ui.select_none_bt.toolTip(),
                        action=self.ktlg_select_none_clicked,
                        tooltips="",
                        short_link="")

        # ----------------

        if self.ui.current_bt.isEnabled():
            menu.add_title(title=self.ui.options_title.text())

            menu.add_action(qicon=get_icon(catalog_icon),
                            title=self.ui.current_bt.toolTip(),
                            action=self.ktlg_curent_clicked,
                            tooltips="",
                            short_link="")

            menu.add_action(qicon=get_icon(reset_icon),
                            title=self.ui.default_bt.toolTip(),
                            action=self.ktlg_default_clicked,
                            tooltips="",
                            short_link="")

            menu.add_action(qicon=get_icon(browser_icon),
                            title=self.ui.browser_bt.toolTip(),
                            action=self.ktlg_browser_clicked,
                            tooltips="",
                            short_link="")

        # ----------------

        menu.exec_(self.ui.ktlg_view.mapToGlobal(point))

    @staticmethod
    def a___________________light_mod______():
        pass

    def ktlg_light_show(self, file_path: str, catalog_name: str):

        self.file_path = self.light_widget.file_path = file_path
        self.catalog_current = catalog_name

        # --------

        if not self.ktlg_load_current_file():
            return False

        # --------

        title = self.tr("Bibliothèque assignée")

        self.light_widget.setWindowTitle(f"{title} - Allplan {self.allplan.version_allplan_current}")

        # --------

        self.light_widget.show()

    def ktlg_light_options_clicked(self) -> None:
        self.light_widget.hide()
        self.show()
        self.ktlg_buttons_manage()

    def ktlg_light_default_clicked(self) -> None:

        row_count = self.ktlg_model.rowCount()

        for makro_row in range(row_count):

            qs_makro = self.ktlg_model.item(makro_row, 0)

            if not isinstance(qs_makro, Makro):
                print("Ktlg -- ktlg_light_default_clicked -- not qm_check(qm_filter)")
                continue

            attribute_count = qs_makro.rowCount()

            for attribute_row in range(attribute_count):

                qs_attribute = qs_makro.child(attribute_row, 1)

                if not isinstance(qs_attribute, MakroAttribute):
                    print("Ktlg -- ktlg_light_default_clicked -- not qm_check(qm_filter)")
                    continue

                qs_attribute.setText(qs_attribute.catalog_name_default)
                qs_attribute.catalog_id = "1006"

        # -----------

        if not self.ktlg_save_datas():
            print("Ktlg -- ktlg_light_default_clicked -- not self.ktlg_save_datas()")
            return False

        # -----------

        return True

    def ktlg_light_current_clicked(self) -> bool:

        row_count = self.ktlg_model.rowCount()

        for makro_row in range(row_count):

            qs_makro = self.ktlg_model.item(makro_row, 0)

            if not isinstance(qs_makro, Makro):
                print("Ktlg -- ktlg_light_current_clicked -- not qm_check(qm_filter)")
                continue

            attribute_count = qs_makro.rowCount()

            for attribute_row in range(attribute_count):

                qs_attribute = qs_makro.child(attribute_row, 1)

                if not isinstance(qs_attribute, MakroAttribute):
                    print("Ktlg -- ktlg_light_current_clicked -- not qm_check(qm_filter)")
                    continue

                if not qs_attribute.is_default:
                    continue

                qs_attribute.setText(self.catalog_current)
                qs_attribute.catalog_id = "116"

        # -----------

        if not self.ktlg_save_datas():
            print("Ktlg -- ktlg_light_current_clicked -- not self.ktlg_save_datas()")
            return False

        # -----------

        return True

    def ktlg_light_favorite_changed(self, file_path: str) -> bool:

        if not self.ktlg_load_file(file_path=file_path, update_title=False):
            return False

        # -----------

        if not self.ktlg_save_datas():
            print("Ktlg -- ktlg_light_favorite_changed -- not self.ktlg_save_datas()")
            return False

        # -----------

        return True

    @staticmethod
    def a___________________save______():
        pass

    def ktlg_save_ask(self) -> bool:

        if not self.ui.save_bt.isEnabled():
            return True

        response = afficher_message(titre=self.tr("Bibliothèque assignée"),
                                    message=self.tr("Voulez-vous enregistrer les modifications?"),
                                    type_bouton=QMessageBox.Ok | QMessageBox.No,
                                    defaut_bouton=QMessageBox.Ok,
                                    icone_question=True)

        if response == QMessageBox.Cancel:
            return False

        if response == QMessageBox.No:
            return True

        return self.ktlg_save_datas()

    def ktlg_save_datas(self) -> bool:
        self.ktlg_save_settings()
        return self.ktlg_save_xml_current()

    def ktlg_save_xml_current(self) -> bool:
        if not self.ktlg_save_xml(file_path=self.file_path):
            return False

        afficher_message(titre=self.tr("Bibliothèque assignée"),
                         message=self.tr("Modification effectuée"),
                         icone_valide=True)

        self.ui.save_bt.setEnabled(False)
        return True

    def ktlg_save_xml(self, file_path: str):

        try:
            root = etree.Element("CatalogData",
                                 nsmap={"xsd": "http://www.w3.org/2001/XMLSchema",
                                        "xsi": "http://www.w3.org/2001/XMLSchema-instance"},
                                 Region="DE")

            # ---------

            if isinstance(self.allplan.allplan_paths, AllplanPaths):
                if self.allplan.allplan_paths.allplan_version_int > 2024:
                    current_version_element = etree.SubElement(root, "CurrentVersion")
                    current_version_element.text = "1.1"

            # ---------

            macro_def_element = etree.SubElement(root, "MakroDef")

            # ---------

            row_count = self.ktlg_model.rowCount()

            for makro_row in range(row_count):
                qs_makro = self.ktlg_model.item(makro_row, 0)

                if not isinstance(qs_makro, Makro):
                    print("Ktlg -- save_xml -- not isinstance(qs_makro, Makro)")
                    continue

                makro_id = qs_makro.id_val

                makro_ele = etree.SubElement(macro_def_element, "MakroTyp", id=makro_id)

                makro_count = qs_makro.rowCount()

                for attribute_row in range(makro_count):

                    qs_attribute = qs_makro.child(attribute_row, 1)

                    if not isinstance(qs_attribute, MakroAttribute):
                        print("Ktlg -- save_xml -- not isinstance(qs_attribute, MakroAttribute")
                        continue

                    # ---------

                    catalog_id = qs_attribute.catalog_id

                    if catalog_id not in ["116", "1006"]:
                        catalog_name = ""
                    else:
                        catalog_name = qs_attribute.text()

                    # ---------

                    etree.SubElement(makro_ele,
                                     "MaterialTyp",
                                     id=qs_attribute.id_val,
                                     catalog_id=catalog_id,
                                     catalog_name=catalog_name)

            # --------------
            # Backup
            # --------------

            folder_path = find_folder_path(file_path=file_path)
            file_name = find_filename(file_path=file_path)

            if not make_backup(chemin_dossier=folder_path,
                               fichier=file_name,
                               extension=".xml",
                               dossier_sauvegarde=f"{folder_path}Backup\\",
                               nouveau=False):
                print(f"Ktlg -- save_xml -- not make_backup")
                return False

            # --------------
            # Save file
            # --------------

            tree = etree.ElementTree(root)
            tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        except Exception as error:
            print(f"Ktlg -- save_xml -- error : {error}")
            return False

        return True

    def ktlg_save_settings(self):
        pass

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        self.ktlg_save_settings()

        if not self.ktlg_save_ask():
            event.ignore()
            return

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass
