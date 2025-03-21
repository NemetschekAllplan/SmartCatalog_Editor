#!/usr/bin/python3
# -*- coding: utf-8 -*

import os.path

from bar_search_filter import SearchFiterWidget
from catalog_manage import *
from convert_manage import *
from formatting_widget import Formatting
from hierarchy import *
from models import ModelsTabDel
from tools import afficher_message as msg, get_bdd_paths
from tools import find_global_point, open_folder, open_file, copy_to_clipboard, settings_read
from tools import get_look_tableview, get_real_path_of_apn_file, settings_save, browser_file
from tools import get_look_treeview, settings_get, move_window_tool, MyContextMenu
from translation_manage import *
from ui_library import Ui_Library
from ui_library_modify import Ui_LibraryModify
from ui_library_tab import Ui_LibraryTab
from ui_library_tab_manage import Ui_LibraryTabManage
from ui_library_synchro import Ui_LibrarySynchro

tab_max_count = 11


class Library(QWidget):
    choisir_attribut_signal = pyqtSignal(str, str)

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_Library()
        self.ui.setupUi(self)

        self.tab_bar = LibraryTabBar()

        self.ui.librairies_tabs.setTabBar(self.tab_bar)

        library_setting = settings_read(library_setting_file)

        self.ismaximized_on = library_setting.get("ismaximized_on", False)

        if not self.ismaximized_on:
            largeur = library_setting.get("width", 800)
            hauteur = library_setting.get("height", 600)

            self.resize(largeur, hauteur)

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))
        self.asc.langue_change.connect(self.tabs_reset_all)

        self.allplan: AllplanDatas = self.asc.allplan
        self.catalog: CatalogDatas = self.asc.catalog

        # ---------------------------------------
        # VARIABLES
        # ---------------------------------------

        self.change_made = False

        self.current_qs = None

        self.current_mode = "Ajout"

        current_tab = library_setting.get("index_tab", 0)

        if current_tab < 0:
            current_tab = 0

        self.current_tab_index = current_tab

        # ---------------------------------------
        # LOADING MANAGE TAB
        # ---------------------------------------

        self.widget_manage_tab = LibraryTabManage(self)

        # -----------------------------------------------
        # LOADING WIDGET DELETE
        # -----------------------------------------------

        self.widget_library_del = ModelsTabDel(self.ui.librairies_tabs)
        self.widget_library_del.validation_supprimer.connect(self.widget_manage_tab.library_used_changed)

        self.tab_bar.del_signal.connect(self.tab_delete_confirm_show)

        # -----------------------------------------------
        # LOADING SIGNALS
        # -----------------------------------------------

        self.ui.librairies_tabs.currentChanged.connect(self.tab_changed)

        self.ui.librairies_tabs.tabBarDoubleClicked.connect(self.tab_double_clicked)

        self.ui.librairies_tabs.customContextMenuRequested.connect(self.tab_menu_show)

        self.tab_bar.move_signal.connect(self.tab_moved)

    @staticmethod
    def a___________________initialisation___________________():
        pass

    def tab_manager_creation(self):

        title = self.tr("Gestion")

        self.ui.librairies_tabs.addTab(self.widget_manage_tab,
                                       get_icon(external_bdd_option_icon),
                                       title)

        self.ui.librairies_tabs.setTabToolTip(0, f"{title} (F6)")

    def show_library(self, current_qs: MyQstandardItem, current_parent: QWidget, current_mode="Ajout") -> None:

        self.current_mode = current_mode

        self.current_qs = current_qs

        if current_mode == "Ajout":
            self.setWindowModality(Qt.WindowModal)
        else:
            self.setWindowModality(Qt.ApplicationModal)

        if not self.widget_manage_tab.initialize_ok:
            self.tab_manager_creation()
            self.widget_manage_tab.library_initialize()

        for index_widget in range(1, self.ui.librairies_tabs.count()):

            widget_tab = self.ui.librairies_tabs.widget(index_widget)

            if not isinstance(widget_tab, LibraryTab):
                continue

            widget_tab.current_mode = current_mode

            if current_mode == "Ajout":
                widget_tab.current_qs = current_qs

            widget_tab.mode_manage()

        move_window_tool(widget_parent=current_parent, widget_current=self)

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

        self.tab_changed(tab_index=self.current_tab_index)

    def hierarchy_selection_changed(self, new_qs: QStandardItem):

        for index_widget in range(1, self.ui.librairies_tabs.count()):

            widget_tab = self.ui.librairies_tabs.widget(index_widget)

            if not isinstance(widget_tab, LibraryTab):
                continue

            widget_tab.current_qs = new_qs

            widget_tab.mode_manage()

    @staticmethod
    def a___________________tab_changed___________________():
        pass

    def tab_changed(self, tab_index: int) -> None:

        self.current_tab_index = tab_index

        tab_widget: LibraryTab = self.ui.librairies_tabs.widget(tab_index)

        if not isinstance(tab_widget, LibraryTab):
            return

        tab_widget.ui.hierarchy.setFocus()

        if tab_widget.ui.hierarchy.cat_model.rowCount() != 0:
            return

        if not self.isVisible():
            return

        tab_widget.loading_model()

    @staticmethod
    def a___________________tab_add___________________():
        pass

    def tab_add(self, title: str, bdd_path_file: str, bdd_type: str) -> None:

        for tab_index in range(self.ui.librairies_tabs.count()):
            if self.ui.librairies_tabs.tabText(tab_index) == title:
                return

        widget_library_tab = LibraryTab(self, bdd_type, bdd_path_file, title)

        widget_library_tab.current_qs = self.current_qs

        bdd_icon = get_icon(bdd_icons_dict.get(bdd_type, bdd_icons_dict[bdd_type_xml]))

        tab_index = self.ui.librairies_tabs.addTab(widget_library_tab, bdd_icon, title)

        if tab_index <= 6:
            self.ui.librairies_tabs.setTabToolTip(tab_index, f"{title} (F{tab_index + 6})")
        else:
            self.ui.librairies_tabs.setTabToolTip(tab_index, title)

        widget_library_tab.ajouter_signal.connect(self.catalog.hierarchie_coller_datas)

        widget_library_tab.current_mode = self.current_mode

        widget_library_tab.mode_manage()

    @staticmethod
    def a___________________tab_delete___________________():
        pass

    def tab_delete_confirm_show(self, tab_index: int) -> None:

        if tab_index == -1 or tab_index == 0:
            return

        self.move_widget_under_tab(tab_index=tab_index,
                                   widget_to_show=self.widget_library_del)

        self.widget_library_del.del_ask_show(tab_index=tab_index)

    @staticmethod
    def a___________________tab_moved__________________():
        pass

    def tab_moved(self) -> None:
        self.change_made = True
        self.tab_redefine_shortcut()

    def tab_redefine_shortcut(self):
        tabs_count = self.ui.librairies_tabs.count()

        for tab_index in range(1, tabs_count):
            title = self.ui.librairies_tabs.tabText(tab_index)

            if tab_index <= 6:
                self.ui.librairies_tabs.setTabToolTip(tab_index, f"{title} (F{tab_index + 6})")
            else:
                self.ui.librairies_tabs.setTabToolTip(tab_index, title)

    @staticmethod
    def a___________________tab_renamed__________________():
        pass

    def tab_renamed(self, original_title: str, new_title: str) -> None:

        tabs_count = self.ui.librairies_tabs.count()

        for tab_index in range(tabs_count):

            title = self.ui.librairies_tabs.tabText(tab_index)

            if title == original_title:
                self.ui.librairies_tabs.setTabText(tab_index, new_title)

                if tab_index <= 6:
                    self.ui.librairies_tabs.setTabToolTip(tab_index, f"{title} (F{tab_index + 6})")
                    return

                self.ui.librairies_tabs.setTabToolTip(tab_index, title)
                return

    @staticmethod
    def a___________________tab_double_clicked__________________():
        pass

    def tab_double_clicked(self, tab_index: int) -> None:

        if not isinstance(tab_index, int):
            return

        if tab_index == -1:
            self.widget_manage_tab.library_add_clicked()
            return

        title = self.ui.librairies_tabs.tabText(tab_index)

        self.widget_manage_tab.library_modify_tab(title=title)

    @staticmethod
    def a___________________tab_menu__________________():
        pass

    def tab_menu_show(self, point: QPoint):

        tab_index = self.tab_bar.tabAt(point)

        tab_count = self.ui.librairies_tabs.count()

        title = self.ui.librairies_tabs.tabText(tab_index)

        self.ui.librairies_tabs.setCurrentIndex(tab_index)

        menu = MyContextMenu()
        menu.add_title(title=self.windowTitle())

        menu_empty = True
        # ------------------------------
        # Add
        # ------------------------------

        if tab_count < tab_max_count:
            menu_empty = False

            menu.add_action(qicon=get_icon(add_icon),
                            title=self.tr('Ajouter'),
                            action=self.widget_manage_tab.library_add_clicked)

        # ------------------------------
        # Modify
        # ------------------------------
        if tab_index > 0:

            menu_empty = False

            menu.add_action(qicon=get_icon(external_bdd_option_icon),
                            title=self.tr('Modifier'),
                            action=lambda: self.widget_manage_tab.library_modify_tab(title=title))

            # ------------------------------
            # Used
            # ------------------------------
            menu.add_action(qicon=get_icon(on_icon),
                            title=self.tr("Ne plus utiliser"),
                            action=lambda: self.widget_manage_tab.library_used_changed(tab_index=tab_index))

            # ------------------------------
            # tools
            # ------------------------------

            menu.addSeparator()

            bdd_path = self.widget_manage_tab.find_bdd_path_file(title=title)

            if bdd_path is not None:

                bdd_folder_path: str = find_folder_path(bdd_path)

                if bdd_folder_path != "":

                    if os.path.exists(bdd_folder_path):
                        menu.add_action(qicon=get_icon(open_icon),
                                        title=self.tr("Ouvrir le dossier"),
                                        action=lambda: self.tab_open_folder(bdd_folder_path))

                    menu.addSeparator()

                    if os.path.exists(bdd_path) and bdd_path.endswith(openable_file_extension):
                        menu.add_action(qicon=get_icon(open_text_editor_icon),
                                        title=self.tr("Ouvrir le fichier"),
                                        action=lambda: open_file(bdd_path))

        if not menu_empty:
            menu.exec_(self.tab_bar.mapToGlobal(point))

    @staticmethod
    def tab_open_folder(bdd_foler_path: str):

        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            copy_to_clipboard(value=bdd_foler_path, show_msg=True)
            return

        open_folder(bdd_foler_path)

    @staticmethod
    def tab_open_file(bdd_path: str):

        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            copy_to_clipboard(value=bdd_path, show_msg=True)
            return

        open_file(bdd_path)

    @staticmethod
    def a___________________reset___________________():
        pass

    def tabs_reset_all(self) -> None:

        self.close()

        if not self.widget_manage_tab.initialize_ok:
            return

        self.ui.librairies_tabs.blockSignals(True)

        self.ui.librairies_tabs.clear()

        self.widget_manage_tab.library_reset()
        self.widget_manage_tab.initialize_ok = False

        self.ui.librairies_tabs.blockSignals(False)

    @staticmethod
    def a___________________tab_tools___________________():
        pass

    def move_widget_under_tab(self, tab_index: int, widget_to_show: QWidget) -> None:

        point: QPoint = self.ui.librairies_tabs.tabBar().tabRect(tab_index).bottomRight()
        global_point: QPoint = self.ui.librairies_tabs.tabBar().mapToGlobal(point)

        tab_width = self.ui.librairies_tabs.tabBar().tabRect(tab_index).width()
        widget_width = widget_to_show.size().width()

        position_max = self.size().width()
        position_end = widget_width + point.x()

        if position_end < position_max:
            widget_to_show.move(global_point - QPoint(tab_width, 0))
        else:
            widget_to_show.move(global_point - QPoint(widget_width, 0))

    @staticmethod
    def a___________________signals___________________():
        pass

    def librairie_reception_valeur(self, number: str, value: str) -> None:

        self.choisir_attribut_signal.emit(number, value)

    def ne_pas_fermer_ui(self) -> None:

        current_index = self.ui.librairies_tabs.currentIndex()
        current_tab: LibraryTab = self.ui.librairies_tabs.widget(current_index)

        if current_tab is None:
            return

        current_tab.close_ui = False

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_N:
            self.widget_manage_tab.library_add_clicked()
            return

        if event.key() == Qt.Key_F2:
            tab_index = self.ui.librairies_tabs.currentIndex()

            if tab_index == 0:
                self.widget_manage_tab.library_modify_clicked()
                return

            title = self.ui.librairies_tabs.tabText(tab_index)
            self.widget_manage_tab.library_modify_tab(title=title)

            return

        if event.key() == Qt.Key_Escape:
            self.close()
            return

        shortcuts = [Qt.Key_F6, Qt.Key_F7, Qt.Key_F8, Qt.Key_F9, Qt.Key_F10, Qt.Key_F11, Qt.Key_F12]

        tab_count = self.ui.librairies_tabs.count()

        if event.key() not in shortcuts:
            return

        index_tab = shortcuts.index(event.key())

        if index_tab == -1 or index_tab >= tab_count:
            return

        self.ui.librairies_tabs.setCurrentIndex(index_tab)

    def changeEvent(self, event: QEvent):

        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.ismaximized_on = True

            else:
                self.ismaximized_on = False
                move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent):

        self.widget_manage_tab.library_save_action()

        super().closeEvent(event)

    @staticmethod
    def a___________________end___________________():
        pass


class LibraryTabManage(QWidget):

    def __init__(self, widget_library: Library):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_LibraryTabManage()
        self.ui.setupUi(self)

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.widget_library = widget_library

        self.asc = self.widget_library.asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.library_tabs = self.widget_library.ui.librairies_tabs

        self.widget_library_modify = LibraryModify(self)

        self.widget_library_modify.save_add.connect(self.library_add_action)
        self.widget_library_modify.save_modifications.connect(self.library_modify_action)

        # ---------------------------------------
        # VARIABLES
        # ---------------------------------------

        self.initialize_ok = False

        self.bdd_type_list = list(bdd_icons_dict)

        # ---------------------------------------
        # LOADING CATEGORIES
        # ---------------------------------------

        get_look_tableview(self.ui.category)

        self.category_model = QStandardItemModel()

        self.categories_initialize()

        self.ui.category.setModel(self.category_model)
        self.ui.category.horizontalHeader().setFixedHeight(24)

        self.ui.category.setCurrentIndex(self.category_model.index(0, 0))

        self.ui.category.selectionModel().currentRowChanged.connect(self.category_changed)

        # ---------------------------------------
        # LOADING LIBRARIES
        # ---------------------------------------

        get_look_tableview(self.ui.library)

        self.library_model = QStandardItemModel()
        self.library_model.setHorizontalHeaderLabels(["",
                                                      self.tr("Titre"),
                                                      self.tr("Chemin"),
                                                      self.tr("Type"),
                                                      self.tr("Actif")])

        self.icon_col = 0
        self.title_col = 1
        self.bdd_path_col = 2
        self.bdd_type_col = 3
        self.used_col = 4

        self.library_filter = QSortFilterProxyModel()
        self.library_filter.setSourceModel(self.library_model)
        self.library_filter.setFilterKeyColumn(self.bdd_type_col)
        self.library_filter.setSortLocaleAware(True)

        self.ui.library.setModel(self.library_filter)

        self.ui.library.doubleClicked.connect(self.library_double_clicked)

        self.ui.library.selectionModel().currentRowChanged.connect(self.library_selection_changed)

        self.ui.library.customContextMenuRequested.connect(self.library_menu_show)

        self.ui.library.horizontalHeader().sortIndicatorChanged.connect(self.library_scroll)

        # ---------------------------------------
        # CHARGEMENT boutons
        # ---------------------------------------

        self.ui.library_add.clicked.connect(self.library_add_clicked)
        self.ui.library_del.clicked.connect(self.library_delete_clicked)
        self.ui.library_modify.clicked.connect(self.library_modify_clicked)

        self.ui.library_help.clicked.connect(self.library_help_show)
        self.ui.library_help.customContextMenuRequested.connect(self.library_help_show)

        self.ui.quit.clicked.connect(self.widget_library.close)

    @staticmethod
    def a___________________initialisation___________________():
        pass

    def categories_initialize(self):

        self.category_model.setHorizontalHeaderLabels([self.tr("Type")])

        self.category_model.appendRow([QStandardItem(get_icon(external_bdd_all_icon), self.tr("Toutes"))])

        self.category_model.appendRow([QStandardItem(get_icon(catalog_icon), bdd_type_xml)])

        a = self.tr("Favoris")

        self.category_model.appendRow([QStandardItem(get_icon(attribute_model_show_icon), f"Allplan - {a}")])

        self.category_model.appendRow([QStandardItem(get_icon(allplan_icon), bdd_type_kukat)])

        self.category_model.appendRow([QStandardItem(get_icon(external_bdd_bcm_icon), bdd_type_bcm)])

        self.category_model.appendRow([QStandardItem(get_icon(external_bdd_nevaris_icon), bdd_type_nevaris)])

        self.category_model.appendRow([QStandardItem(get_icon(excel_icon), bdd_type_excel)])

        self.category_model.appendRow([QStandardItem(get_icon(external_bdd_show_icon), self.tr("Autres"))])

    def library_initialize(self):

        if self.initialize_ok:
            return

        library_config = settings_read(library_config_file)

        use_tabs = list()

        for title, datas in library_config.items():

            title: str
            datas: dict

            bdd_path_file = datas.get("path", "")
            bdd_type = datas.get("type", "")

            if self.library_tabs.count() < tab_max_count:
                tab_index = datas.get("use", 0)
            else:
                tab_index = 0

            if bdd_type == "Allplan - Smart-Catalog":
                bdd_type = bdd_type_xml

            if bdd_path_file == "" or bdd_type not in bdd_icons_dict:
                continue

            if not bdd_path_file.startswith("http") and not os.path.exists(bdd_path_file):
                continue

            if bdd_path_file.upper().endswith(".FIC"):
                msg(titre=application_title,
                    message="Attention : Le format de fichier Fic de GIMI n'est plus pris en charge.\n"
                            "Vous pouvez désormais exporter votre bibliothèque GIMI au format XML.\n"
                            "Pour plus d'informations, veuillez contacter Euriciel au 02 47 27 86 29.")

                continue

            if tab_index != 0:

                if tab_index is True:
                    use_tabs.append([len(use_tabs), title, bdd_path_file, bdd_type])
                else:
                    use_tabs.append([tab_index, title, bdd_path_file, bdd_type])

            self.library_add_action(title=title,
                                    bdd_path_file=bdd_path_file,
                                    bdd_type=bdd_type,
                                    used_bool=tab_index != 0)

        use_tabs.sort()

        for tab_data in use_tabs:
            _, title, bdd_path_file, bdd_type = tab_data

            self.widget_library.tab_add(title=title,
                                        bdd_path_file=bdd_path_file,
                                        bdd_type=bdd_type)

        library_setting = settings_read(library_setting_file)

        order = library_setting.get("order", 0)
        order_col = library_setting.get("order_col", 1)

        header = self.library_header_manage()

        if header is not None:

            if isinstance(order, int) and isinstance(order_col, int):
                self.ui.library.sortByColumn(order_col, order)
                header.setSortIndicator(order_col, order)

        self.initialize_ok = True

        if self.library_model.rowCount() == 0:
            return

        catogery_index = library_setting.get("category", 0)

        if isinstance(catogery_index, int):
            self.ui.category.setCurrentIndex(self.category_model.index(catogery_index, 0))
        else:
            self.ui.category.setCurrentIndex(self.category_model.index(0, 0))

        title = library_setting.get("title", "")

        if isinstance(title, str) and title != "":

            self.library_select_row(title)
        else:

            self.ui.library.selectionModel().setCurrentIndex(self.library_filter.index(0, 0),
                                                             QItemSelectionModel.Select |
                                                             QItemSelectionModel.Rows)
        self.library_buttons_refresh()

    def library_reset(self):

        if not self.initialize_ok:
            return

        library_model_row_count = self.library_model.rowCount()

        if library_model_row_count != 0:
            # self.library_model.blockSignals(True)
            self.library_model.clear()
            self.library_model.setHorizontalHeaderLabels(["",
                                                          self.tr("Titre"),
                                                          self.tr("Chemin"),
                                                          self.tr("Type"),
                                                          self.tr("Actif")])

            # self.library_model.blockSignals(False)

        # category_model_row_count = self.category_model.rowCount()
        #
        # if category_model_row_count == 0:
        #     return
        #
        # # self.category_model.blockSignals(True)
        # self.category_model.clear()
        # self.categories_initialize()
        # # self.category_model.blockSignals(False)

    @staticmethod
    def a___________________category___________________():
        pass

    def category_changed(self, qm_category_current: QModelIndex) -> bool:

        if not qm_check(qm_category_current):
            self.library_filter.setFilterRegExp("")
            self.library_header_manage()
            self.library_selection_changed(self.ui.library.currentIndex())
            self.library_buttons_refresh()

            print("library -- WidgetLibraryTabManage -- category_changed -- not qm_check(qm_current)")
            return False

        current_bdd_type = qm_category_current.data()

        txt_favorite = self.tr("Favoris")

        if current_bdd_type == self.tr("Toutes"):
            self.library_filter.setFilterRegExp("")

        elif current_bdd_type == f"Allplan - {txt_favorite}":
            self.library_filter.setFilterRegExp(bdd_type_fav)

        elif current_bdd_type == self.tr("Autres"):
            regexp = "|".join(categories_extern)
            self.library_filter.setFilterRegExp(regexp)

        elif current_bdd_type == bdd_type_nevaris or current_bdd_type == bdd_type_nevaris_xlsx:
            regexp = f"{bdd_type_nevaris}|{bdd_type_nevaris_xlsx}"
            self.library_filter.setFilterRegExp(regexp)

        elif current_bdd_type == bdd_type_bcm_c or current_bdd_type == bdd_type_bcm:
            regexp = f"{bdd_type_bcm_c}|{bdd_type_bcm}"
            self.library_filter.setFilterRegExp(regexp)

        else:
            self.library_filter.setFilterRegExp(current_bdd_type)

        self.library_header_manage()

        qm_current = self.ui.library.currentIndex()

        if not qm_check(qm_current) and self.library_filter.rowCount() > 0:
            qm_current = self.library_filter.index(0, self.title_col)

            if qm_check(qm_current):
                self.ui.library.setCurrentIndex(qm_current)
        else:
            self.library_selection_changed(qm_current)

        self.library_scroll()

        self.library_buttons_refresh()

        return True

    def catagory_choose(self, bdd_type: str) -> bool:

        bdd_type = self.category_convert(category_name=bdd_type)

        # -------------------------------
        # Define new current category
        # -------------------------------

        qm_category_current_index = self.ui.category.currentIndex()

        if not qm_check(qm_category_current_index):
            print("library -- WidgetLibraryTabManage -- catagory_choose -- not qm_check(qm_category_current_index)")
            return False

        current_row = qm_category_current_index.row()

        if current_row == 0:
            return True

        current_type = qm_category_current_index.data()

        if current_type == bdd_type:
            return True

        search_category = self.category_model.findItems(bdd_type, Qt.MatchContains, 0)

        if len(search_category) == 0:
            print("library -- WidgetLibraryTabManage -- catagory_choose -- len(search_category) == 0")
            return False

        qs = search_category[0]

        qm_category_index = qs.index()

        if not qm_check(qm_category_index):
            print("library -- WidgetLibraryTabManage -- catagory_choose -- not qm_check(qm_category_index)")
            return False

        self.ui.category.setCurrentIndex(qm_category_index)

        return True

    def category_convert(self, category_name: str) -> str:

        if category_name in [bdd_type_xml, bdd_type_kukat, bdd_type_excel]:
            return category_name

        if category_name == bdd_type_fav:
            txt_favorite = self.tr("Favoris")
            return f"Allplan - {txt_favorite}"

        if category_name in categories_bcm:
            return bdd_type_bcm

        if category_name in categories_excel:
            return categories_excel

        if category_name in categories_nevaris:
            return "Nevaris"

        if category_name in categories_extern:
            return self.tr("Autres")

        return category_name

    @staticmethod
    def a___________________library_header___________________():
        pass

    def library_header_manage(self):

        header = self.ui.library.horizontalHeader()

        if header is None:
            return None

        if header.height() != 24:
            header.setFixedHeight(24)

        header.setSectionResizeMode(self.icon_col, QHeaderView.Fixed)
        self.ui.library.setColumnWidth(self.icon_col, 35)

        self.ui.library.setColumnHidden(self.bdd_type_col, True)

        header.setSectionResizeMode(self.used_col, QHeaderView.Fixed)
        self.ui.library.setColumnWidth(self.used_col, 50)

        header.setSectionResizeMode(self.title_col, QHeaderView.ResizeToContents)

        header.setSectionResizeMode(self.bdd_path_col, QHeaderView.Stretch)

        return header

    @staticmethod
    def a___________________library_selection___________________():
        pass

    def library_select_row(self, title: str) -> bool:

        selection_model = self.ui.library.selectionModel()

        if selection_model is None:
            print("library -- WidgetLibraryTabManage -- library_select -- selection_model is None")
            return False

        qm_filter_start = self.library_filter.index(0, self.title_col)

        search_library = self.library_filter.match(qm_filter_start, Qt.DisplayRole, title, 1, Qt.MatchExactly)

        if len(search_library) == 0:
            print("library -- WidgetLibraryTabManage -- library_select_row -- len(search_library) == 0")
            return False

        qm_current = search_library[0]

        if not qm_check(qm_current):
            print("library -- WidgetLibraryTabManage -- library_select_row -- not qm_check(qm_library)")
            return False

        self.ui.library.setCurrentIndex(qm_current)

        return True

    def library_select_row_by_qm(self, qm_model: QModelIndex) -> bool:

        if not qm_check(qm_model):
            print("library -- WidgetLibraryTabManage -- library_select_row_by_qm -- not qm_check(qm_model)")
            return False

        # ----------

        qm_filter = self.library_filter.mapFromSource(qm_model)

        if qm_check(qm_filter):
            self.ui.library.setCurrentIndex(qm_filter)
            return True

        # ----------

        qm_category = self.library_model.index(qm_model.row(), 3)

        if not qm_check(qm_category):
            print("library -- WidgetLibraryTabManage -- library_select_row_by_qm -- not qm_check(qm_category)")
            return False

        # ----------

        category_name = qm_category.data()

        if not isinstance(category_name, str):
            print("library -- WidgetLibraryTabManage -- library_select_row_by_qm -- not isinstance(category_name, str)")
            return False

        self.catagory_choose(bdd_type=category_name)

        # ----------

        qm_filter = self.library_filter.mapFromSource(qm_model)

        if qm_check(qm_filter):
            self.ui.library.setCurrentIndex(qm_filter)
            return True

        return False

    def library_selection_changed(self, qm_current: QModelIndex):

        used = self.find_qm(qm_current=qm_current, column=self.used_col, value=True)

        if used is None:
            self.ui.library_del.setEnabled(False)
            return

        self.library_used_manage(used=used)

    def library_double_clicked(self, qm_current: QModelIndex):

        if not qm_check(qm_current):
            print("library -- WidgetLibraryTabManage -- library_double_clicked -- not qm_check(qm_current)")
            return

        current_col = qm_current.column()

        if current_col == self.used_col:
            return

        self.library_used_clicked()

    def library_scroll(self):

        qm_filter_current = self.ui.library.currentIndex()

        if not qm_check(qm_filter_current):
            return

        self.ui.library.scrollTo(qm_filter_current, QAbstractItemView.PositionAtCenter)

    @staticmethod
    def a___________________library_add___________________():
        pass

    def library_add_clicked(self):

        current_index = self.ui.category.selectionModel().currentIndex()

        if not qm_check(current_index):
            print("library -- WidgetLibraryTabManage -- library_add_clicked -- not qm_check(current_index)")
            return

        current_bdd_type = current_index.data()

        if current_bdd_type == bdd_type_bcm:
            default_path = settings_get(file_name=library_setting_file, info_name="path_bcm")

        elif current_bdd_type == bdd_type_xml:
            default_path = settings_get(file_name=library_setting_file, info_name="path_cat")

        elif current_bdd_type == bdd_type_fav:
            default_path = settings_get(file_name=library_setting_file, info_name="path_favorites")

        elif current_bdd_type == bdd_type_kukat:
            default_path = settings_get(file_name=library_setting_file, info_name="path_kukat")

        else:
            default_path = settings_get(file_name=library_setting_file, info_name="path_open")

        move_window_tool(widget_parent=self.asc, widget_current=self.widget_library_modify, always_center=True)

        titles_list = self.library_find_all_titles()

        titre = self.library_find_title(current_title="", titles_list=titles_list)

        self.widget_library_modify.tab_modify_show(bdd_type=bdd_type_xml,
                                                   bdd_path_file="",
                                                   title=titre,
                                                   titles_list=titles_list,
                                                   used_bool=False,
                                                   default_path=default_path,
                                                   modification_mod=False)

    def library_add_drop(self, bdd_type: str, bdd_path_file: str, title: str):

        titles_list = self.library_find_all_titles()

        title = self.library_find_title(current_title=title, titles_list=titles_list)

        self.library_add_action(title=title,
                                bdd_path_file=bdd_path_file,
                                bdd_type=bdd_type,
                                used_bool=False)

    def library_add_action(self, title: str, bdd_path_file: str, bdd_type: str, used_bool=False):

        if bdd_type not in bdd_icons_dict:
            print("library -- WidgetLibraryTabManage -- library_add_action -- bdd_type not in bdd_icons_dict")
            return

        # ------------
        # define font size
        # ------------

        qs_font = QStandardItem().font()
        qs_font.setPointSize(1)

        # ------------
        # icon column
        # ------------

        bdd_icon = get_icon(bdd_icons_dict.get(bdd_type, bdd_icons_dict[bdd_type_xml]))

        qs_icon = QStandardItem()
        qs_icon.setIcon(bdd_icon)

        index_bdd = f"{self.bdd_type_list.index(bdd_type):02d}"
        qs_icon.setText(index_bdd)
        qs_icon.setFont(qs_font)
        qs_icon.setForeground(QColor(255, 255, 255, 255))

        # ------------
        # title column
        # ------------

        qs_title = QStandardItem(title)

        # ------------
        # path column
        # ------------

        qs_bdd_path_file = QStandardItem(bdd_path_file)
        qs_bdd_path_file.setToolTip(bdd_path_file)

        # ------------
        # type column
        # ------------

        qs_bdd_type = QStandardItem(bdd_type)

        # ------------
        # used column
        # ------------

        if used_bool:
            txt = "on"
        else:
            txt = "off"

        qs_used = QStandardItem(txt)
        qs_used.setFont(qs_font)
        qs_used.setTextAlignment(Qt.AlignCenter)
        qs_used.setForeground(QColor(255, 255, 255, 255))
        qs_used.setToolTip(txt)

        if used_bool:
            qs_used.setBackground(QColor('#bad0e7'))

        # ------------
        # add row
        # ------------

        current_index = self.library_model.rowCount()

        self.library_model.appendRow([qs_icon,
                                      qs_title,
                                      qs_bdd_path_file,
                                      qs_bdd_type,
                                      qs_used])

        if self.isVisible():
            self.catagory_choose(bdd_type=bdd_type)

        if not self.isVisible():
            return

        # -------------------------------
        # add button in the used column
        # -------------------------------

        qm_model = self.library_model.index(current_index, self.used_col)

        if not qm_check(qm_model):
            print("library -- WidgetLibraryTabManage -- library_add_action -- if not qm_check(qm_model)")
            return

        qm_filtre = self.library_filter.mapFromSource(qm_model)

        if qm_check(qm_filtre):
            self.library_button_creation(qm_filter=qm_filtre, icone_name=txt)

        # -------------------------------
        # Adjust header + change status
        # -------------------------------

        self.library_header_manage()

        self.widget_library.change_made = True

        # -------------------------------
        # Define new current library
        # -------------------------------

        self.library_select_row(title=title)

    def library_find_all_titles(self) -> list:

        titles_list = list()
        row_count = self.library_model.rowCount()

        for item_index in range(row_count):

            qs = self.library_model.item(item_index, self.title_col)

            if not isinstance(qs, QStandardItem):
                print("library -- WidgetLibraryTabManage -- library_find_all_titles -- "
                      "not isinstance(qs, QStandardItem)")
                continue

            title = qs.text()

            if not isinstance(title, str):
                print("library -- WidgetLibraryTabManage -- library_find_all_titles -- not isinstance(title, str)")
                continue

            if title == "":
                print("library -- WidgetLibraryTabManage -- library_find_all_titles -- title == empty")
                continue

            if title in titles_list:
                print("library -- WidgetLibraryTabManage -- library_find_all_titles -- title in titles_list")
                continue

            titles_list.append(title.upper())

        return titles_list

    def library_find_title(self, current_title: str, titles_list: list) -> str:

        if not isinstance(titles_list, list) or not isinstance(current_title, str):
            print("library -- WidgetLibraryTabManage -- library_find_title -- "
                  "titles_list != list or current_title != str")
            return ""

        if len(titles_list):
            titles_list = self.library_find_all_titles()

        if current_title == "":
            current_title = self.tr("Bible externe")
            current_title += " 01"

        new_name = find_new_title(base_title=current_title, titles_list=titles_list)

        if not isinstance(new_name, str):
            print("library -- WidgetLibraryTabManage -- library_find_title -- not isinstance(new_name, str)")
            return ""

        return new_name

    @staticmethod
    def a___________________library_buttons___________________():
        pass

    def library_button_creation(self, qm_filter: QModelIndex, icone_name: str):

        icon = get_icon(f":/Images/{icone_name}")

        button = QPushButton(icon, "")
        button.setFlat(True)
        button.setIconSize(QSize(20, 20))

        button.clicked.connect(self.library_used_clicked)

        self.ui.library.setIndexWidget(qm_filter, button)

    def library_buttons_refresh(self):

        row_count = self.library_filter.rowCount()

        for item_index in range(row_count):

            qm_filtre = self.library_filter.index(item_index, self.used_col)

            if not qm_check(qm_filtre):
                print("library -- WidgetLibraryTabManage -- library_buttons_refresh -- not qm_check(qm_filtre)")
                continue

            qm_title = self.library_filter.index(item_index, self.title_col)

            if not qm_check(qm_title):
                print("library -- WidgetLibraryTabManage -- library_buttons_refresh -- not qm_check(qm_title)")
                continue

            icone_name = qm_filtre.data()

            self.library_button_creation(qm_filter=qm_filtre, icone_name=icone_name)

    @staticmethod
    def a___________________library_delete___________________():
        pass

    def library_delete_clicked(self):

        qm_current = self.ui.library.selectionModel().currentIndex()
        current_row = qm_current.row()

        used = self.find_qm(qm_current=qm_current, column=self.used_col, value=True)

        if used is None:
            return

        if used == "on":
            return

        if used != "off":
            print("library -- WidgetLibraryTabManage -- library_delete_clicked -- used != off")
            return

        title = self.find_qm(qm_current=qm_current, column=self.title_col, value=True)

        if title is None:
            print("library -- WidgetLibraryTabManage -- library_delete_clicked -- title is None")
            return

        if msg(titre=self.widget_library.windowTitle(),
               message=self.tr("Voulez-vous supprimer la bibliothèque?"),
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               defaut_bouton=QMessageBox.Ok,
               icone_sauvegarde=True) != QMessageBox.Ok:
            return

        self.library_filter.removeRow(current_row)

        self.widget_library.change_made = True

    @staticmethod
    def a___________________library_modify___________________():
        pass

    def library_modify_tab(self, title: str):

        if not isinstance(title, str):
            print("library -- WidgetLibraryTabManage -- library_modify_tab -- not isinstance(title, str)")
            return

        serach_start = self.library_model.index(0, self.title_col)

        search_title = self.library_model.match(serach_start, Qt.DisplayRole, title, 1, Qt.MatchExactly)

        if len(search_title) == 0:
            print("library -- WidgetLibraryTabManage -- library_modify_tab -- len(search_title) == 0")
            return

        qs_title = search_title[0]

        self.library_modify_show(qm_current=qs_title)

    def library_modify_clicked(self):

        qm_current = self.ui.library.selectionModel().currentIndex()

        self.library_modify_show(qm_current)

    def library_modify_show(self, qm_current: QModelIndex):

        # ------------------- TITLE -----------

        title = self.find_qm(qm_current=qm_current, column=self.title_col, value=True)

        if title is None:
            print("library -- WidgetLibraryTabManage -- library_modify_clicked -- title is None")
            return

        # ------------------- BDD PATH -----------

        bdd_path_file = self.find_qm(qm_current=qm_current, column=self.bdd_path_col, value=True)

        if bdd_path_file is None:
            print("library -- WidgetLibraryTabManage -- library_modify_clicked -- bdd_path_file is None")
            return

        # ------------------- BDD TYPE -----------

        bdd_type = self.find_qm(qm_current=qm_current, column=self.bdd_type_col, value=True)

        if bdd_type is None:
            print("library -- WidgetLibraryTabManage -- library_modify_clicked -- bdd_type is None")
            return

        # ------------------- USED -----------

        used = self.find_qm(qm_current=qm_current, column=self.used_col, value=True)

        if used is None:
            print("library -- WidgetLibraryTabManage -- library_modify_clicked -- used is None")
            return

        if used != "on" and used != "off":
            print("library -- WidgetLibraryTabManage -- library_modify_clicked -- used != off")
            return

        # ------------------- default_path -----------

        if bdd_path_file.startswith("http"):

            default_path = bdd_path_file

        else:

            default_path = find_folder_path(bdd_path_file)

        # ------------------- titles list -----------

        titles_list = self.library_find_all_titles()

        # ------------------- show widget -----------

        move_window_tool(widget_parent=self.asc, widget_current=self.widget_library_modify, always_center=True)

        self.widget_library_modify.tab_modify_show(bdd_type=bdd_type,
                                                   bdd_path_file=bdd_path_file,
                                                   title=title,
                                                   titles_list=titles_list,
                                                   used_bool=used == "on",
                                                   default_path=default_path,
                                                   modification_mod=True)

    def library_modify_action(self, bdd_type: str, bdd_path_file: str, title: str, original_title: str):

        qm_current = self.find_qm_title(original_title)

        if qm_current is None:
            print("library -- WidgetLibraryTabManage -- library_modify_action -- qm_current is None")
            return

        # ------------------- USED -----------

        used: QModelIndex = self.find_qm(qm_current=qm_current, column=self.used_col, value=True)

        if used is None:
            print("library -- WidgetLibraryTabManage -- library_modify_action -- qm_used is None")
            return

        if used != "on" and used != "off":
            print("library -- WidgetLibraryTabManage -- library_modify_action -- used != off")
            return

        # ------------------- ICON -----------

        qm_icon: QModelIndex = self.find_qm(qm_current=qm_current, column=self.icon_col, value=False)

        if qm_icon is None:
            print("library -- WidgetLibraryTabManage -- library_modify_action -- qm_icon is None")
            return

        # ------------------- TITLE -----------

        qm_title: QModelIndex = self.find_qm(qm_current=qm_current, column=self.title_col, value=False)

        if qm_title is None:
            print("library -- WidgetLibraryTabManage -- library_modify_action -- qm_title is None")
            return

        current_title = qm_title.data()

        # ------------------- BDD PATH -----------

        qm_bdd_path: QModelIndex = self.find_qm(qm_current=qm_current, column=self.bdd_path_col, value=False)

        if qm_bdd_path is None:
            print("library -- WidgetLibraryTabManage -- library_modify_action -- qm_bdd_path is None")
            return

        current_bdd_path = qm_bdd_path.data()

        # ------------------- BDD TYPE -----------

        qm_bdd_type = self.find_qm(qm_current=qm_current, column=self.bdd_type_col, value=False)

        if bdd_type is None:
            print("library -- WidgetLibraryTabManage -- library_modify_action -- bdd_type is None")
            return

        current_bdd_type = qm_bdd_type.data()

        if bdd_type not in self.bdd_type_list:
            print("library -- WidgetLibraryTabManage -- library_modify_action -- bdd_type not in self.bdd_type_list")
            return

        icon = get_icon(bdd_icons_dict[bdd_type])

        index_bdd = f"{self.bdd_type_list.index(bdd_type):02d}"

        # ------------------- APPLY MODIFICATIONS -----------

        change_made = self.widget_library.change_made

        header = self.ui.library.horizontalHeader()

        if header is not None:
            sort_column = self.ui.library.horizontalHeader().sortIndicatorSection()

        else:
            sort_column = -1

        scroll = False

        # ------------------- ICON -----------

        if current_bdd_type != bdd_type:
            self.library_model.setData(qm_icon, icon, Qt.DecorationRole)
            self.library_model.setData(qm_icon, index_bdd)
            change_made = True

            scroll = sort_column == self.icon_col

        # ------------------- TITLE -----------

        if current_title != title:
            self.library_model.setData(qm_title, title)
            change_made = True

            if not scroll:
                scroll = sort_column == self.title_col

            if used == "on":
                self.widget_library.tab_renamed(original_title=original_title, new_title=title)

        # ------------------- BDD PATH -----------

        if current_bdd_path != bdd_path_file:
            self.library_model.setData(qm_bdd_path, bdd_path_file)
            change_made = True

            if not scroll:
                scroll = sort_column == self.bdd_path_col

        # ------------------- BDD TYPE -----------

        if current_bdd_type != bdd_type:
            self.library_model.setData(qm_bdd_type, bdd_type)
            change_made = True

            if not scroll:
                scroll = sort_column == self.bdd_type_col

        self.widget_library.change_made = change_made

        if sort_column == -1:
            return

        if scroll:
            self.library_scroll()

    @staticmethod
    def a___________________library_used___________________():
        pass

    def library_used_clicked(self):

        qm_filter_current = self.ui.library.selectionModel().currentIndex()

        if not qm_check(qm_filter_current):
            print("library -- WidgetLibraryTabManage -- library_used_clicked -- not qm_check(qm_filter_current)")
            return

        qm_model_current = self.library_filter.mapToSource(qm_filter_current)

        if not qm_check(qm_model_current):
            print("library -- WidgetLibraryTabManage -- library_used_clicked -- not qm_check(qm_model_current)")
            return

        self.library_used_action(qm_model_current=qm_model_current)

    def library_used_changed(self, tab_index: int):

        if not isinstance(tab_index, int):
            print("library -- WidgetLibraryTabManage -- library_used_changed -- not isinstance(tab_index, int)")
            return

        title = self.library_tabs.tabText(tab_index)

        if not isinstance(title, str):
            print("library -- WidgetLibraryTabManage -- library_used_changed -- not isinstance(title, str)")
            return

        qm_current = self.find_qm_title(title)

        if not qm_check(qm_current):
            print("library -- WidgetLibraryTabManage -- library_used_changed -- not qm_check(qm)")
            return

        self.library_used_action(qm_model_current=qm_current)

    def library_used_action(self, qm_model_current: QModelIndex):

        # ------------------- TITLE -----------

        qm_title = self.find_qm(qm_current=qm_model_current, column=self.title_col, value=False)

        if qm_title is None:
            print("library -- WidgetLibraryTabManage -- library_used_clicked -- title is None")
            return

        title = qm_title.data()

        # ------------------- USED -----------

        qm_used = self.find_qm(qm_current=qm_model_current, column=self.used_col, value=False)

        if qm_used is None:
            print("library -- WidgetLibraryTabManage -- library_used_clicked -- qm_used is None")
            return

        used: str = qm_used.data()

        if used != "on" and used != "off":
            print("library -- WidgetLibraryTabManage -- library_used_clicked -- used != on and  used != off")
            return

        qm_used_filter = self.library_filter.mapFromSource(qm_used)
        button = None

        if qm_check(qm_used_filter):

            button = self.ui.library.indexWidget(qm_used_filter)

            if not isinstance(button, QPushButton):
                print("library -- WidgetLibraryTabManage -- library_used_clicked -- "
                      "not isinstance(button, QPushButton)")
                return

        if used == "off":

            if self.library_tabs.count() > tab_max_count:
                msg(titre=self.widget_library.windowTitle(),
                    message=self.tr("Vous avez atteint le nombre maximun de bibliothèques externes."),
                    type_bouton=QMessageBox.Ok,
                    icone_avertissement=True)
                return

            icon = get_icon(on_icon)
            used_new_state = "on"

            # ------------------- BDD PATH -----------

            bdd_path_file = self.find_qm(qm_current=qm_model_current, column=self.bdd_path_col, value=True)

            if bdd_path_file is None:
                print("library -- WidgetLibraryTabManage -- library_used_clicked -- bdd_path_file is None")
                return

            # ------------------- BDD TYPE -----------

            bdd_type = self.find_qm(qm_current=qm_model_current, column=self.bdd_type_col, value=True)

            if bdd_type is None:
                print("library -- WidgetLibraryTabManage -- library_used_clicked -- bdd_type is None")
                return

            self.library_model.setData(qm_used, QColor('#bad0e7'), Qt.BackgroundColorRole)

            self.widget_library.tab_add(title=title,
                                        bdd_path_file=bdd_path_file,
                                        bdd_type=bdd_type)

        else:

            icon = get_icon(off_icon)
            used_new_state = "off"

            tab_index_del = -1

            for index_tab in range(self.library_tabs.count()):
                if self.library_tabs.tabText(index_tab) == title:
                    tab_index_del = index_tab
                    break

            if tab_index_del == -1:
                return

            color = qm_title.data(Qt.BackgroundColorRole)
            self.library_model.setData(qm_used, color, Qt.BackgroundColorRole)

            self.library_tabs.removeTab(tab_index_del)
            self.widget_library.tab_redefine_shortcut()

            if self.library_tabs.currentIndex() != 0:
                self.library_tabs.setCurrentIndex(0)

        self.widget_library.change_made = True

        self.library_model.setData(qm_used, used_new_state)
        self.library_model.setData(qm_used, used_new_state, Qt.ToolTipRole)

        if button is not None:
            button.setIcon(icon)

        self.library_used_manage(used=used_new_state)
        self.library_save_config()

    def library_used_manage(self, used: str):

        if not isinstance(used, str):
            print("library -- WidgetLibraryTabManage -- library_used_manage -- not isinstance(used, str)")
            self.ui.library_del.setEnabled(False)
            return

        used_bool = used != "on"

        self.ui.library_del.setEnabled(used_bool)

    @staticmethod
    def a___________________library_help___________________():
        pass

    def library_help_show(self):

        help_xml_path = f"{asc_folder_path}help\\library - xml.pdf"
        help_excel_path = f"{asc_folder_path}help\\library - excel.pdf"

        if not os.path.exists(help_xml_path) and not os.path.exists(help_excel_path):
            msg(titre=self.widget_library.windowTitle(),
                message=self.tr("Aide non disponible."))
            return

        menu = MyContextMenu(self.asc)

        # ------------------
        # Ouvrir Dossier
        # ------------------

        menu.add_title(title=self.tr("Aide"))

        if os.path.exists(help_xml_path):
            menu.add_action(qicon=get_icon(pdf_icon),
                            title=self.tr("Comment créer une bible externe XML"),
                            action=lambda val=help_xml_path: open_file(val))

        menu.add_action(qicon=get_icon(pdf_icon),
                        title=self.tr("Comment créer une bible externe Excel"),
                        action=lambda val=help_excel_path: open_file(val))

        menu.exec_(find_global_point(self.ui.library_help))

    @staticmethod
    def a___________________library_menu___________________():
        pass

    def library_menu_show(self, point: QPoint):

        if (not self.ui.library_add.isEnabled() and
                not self.ui.library_modify.isEnabled() and
                not self.ui.library_del.isEnabled()):
            return

        # ------------------------------
        # menu
        # ------------------------------

        menu = MyContextMenu()

        menu.add_title(title=self.widget_library.windowTitle())

        qm_current = self.ui.library.selectionModel().currentIndex()

        # ------------------------------
        # Add
        # ------------------------------

        if self.ui.library_add.isEnabled():
            menu.add_action(qicon=get_icon(add_icon),
                            title=self.tr("Ajouter"),
                            action=self.library_add_clicked)

        if not qm_check(qm_current) and not menu.isEmpty():
            menu.exec_(self.ui.library.mapToGlobal(point))
            return

        # ------------------------------
        # Modify
        # ------------------------------

        if self.ui.library_modify.isEnabled():
            menu.add_action(qicon=get_icon(external_bdd_option_icon),
                            title=self.tr("Modifier"),
                            action=self.library_modify_clicked)

        # ------------------------------
        # delete
        # ------------------------------

        if self.ui.library_del.isEnabled():
            menu.add_action(qicon=get_icon(delete_icon),
                            title=self.tr("Supprimer"),
                            action=self.library_delete_clicked)

        # ------------------------------
        # Used
        # ------------------------------

        used = self.find_qm(qm_current=qm_current, column=self.used_col, value=True)

        if used is not None:

            if used == "on":
                menu.add_action(qicon=get_icon(on_icon),
                                title=self.tr("Ne plus utiliser"),
                                action=self.library_used_clicked)

            elif used == "off":
                menu.add_action(qicon=get_icon(off_icon),
                                title=self.tr("Utiliser"),
                                action=self.library_used_clicked)

        menu.addSeparator()

        # ------------------------------
        # tools
        # ------------------------------

        bdd_path = self.find_qm(qm_current=qm_current, column=self.bdd_path_col, value=True)

        if bdd_path is not None:

            bdd_folder_path: str = find_folder_path(bdd_path)

            if bdd_folder_path != "":

                if bdd_folder_path != "":

                    if os.path.exists(bdd_folder_path):
                        menu.add_action(qicon=get_icon(open_icon),
                                        title=self.tr("Ouvrir le dossier"),
                                        action=lambda: open_folder(bdd_folder_path))

                        menu.add_action(qicon=get_icon(copy_icon),
                                        title=self.tr("Copier le chemin dans le presse-papier"),
                                        action=lambda: copy_to_clipboard(bdd_folder_path, show_msg=True))

                    menu.addSeparator()

                    if os.path.exists(bdd_path) and bdd_path.endswith(openable_file_extension):
                        menu.add_action(qicon=get_icon(open_text_editor_icon),
                                        title=self.tr("Ouvrir le fichier"),
                                        action=lambda: open_file(bdd_path))

        menu.exec_(self.ui.library.mapToGlobal(point))

    @staticmethod
    def a___________________library_save___________________():
        pass

    def library_save_action(self):

        self.library_save_setting()
        self.library_save_config()

    def library_save_setting(self):

        datas_config = settings_read(file_name=library_setting_file)

        header = self.ui.library.horizontalHeader()

        if header is not None:
            datas_config["order"] = header.sortIndicatorOrder()
            datas_config["order_col"] = header.sortIndicatorSection()

        current_category = self.ui.category.currentIndex()

        if qm_check(current_category):
            datas_config["category"] = current_category.row()

        title = self.find_qm(qm_current=self.ui.library.currentIndex(), column=self.title_col, value=True)

        if title is not None:
            datas_config["title"] = title

        if self.widget_library.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self.widget_library)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True

                settings_save(file_name=library_setting_file, config_datas=datas_config)
                return

        datas_config["height"] = self.widget_library.size().height()
        datas_config["width"] = self.widget_library.size().width()
        datas_config["ismaximized_on"] = False

        settings_save(file_name=library_setting_file, config_datas=datas_config)

    def library_save_config(self):

        # ----------
        # Configs
        # ----------
        # if not self.widget_library.change_made:
        #     return

        if not self.initialize_ok:
            return

        library_datas = dict()

        for index_row in range(self.library_model.rowCount()):

            qm_current = self.library_model.index(index_row, 0)

            title = self.find_qm(qm_current=qm_current, column=self.title_col, value=True)

            if title is None:
                continue

            bdd_path_file = self.find_qm(qm_current=qm_current, column=self.bdd_path_col, value=True)

            if bdd_path_file is None:
                continue

            bdd_type = self.find_qm(qm_current=qm_current, column=self.bdd_type_col, value=True)

            if bdd_type is None:
                continue

            used = self.find_qm(qm_current=qm_current, column=self.used_col, value=True)

            if used != "on" and used != "off":
                continue

            if used == "on":
                tab_index = self.get_index_tab_by_name(title=title)
            else:
                tab_index = 0

            library_datas[title] = {"path": bdd_path_file,
                                    "type": bdd_type,
                                    "use": tab_index}

        settings_save(library_config_file, library_datas)

    def get_index_tab_by_name(self, title: str):
        for index in reversed(range(self.library_tabs.count())):
            if self.library_tabs.tabText(index) == title:
                return index
        return 0

    @staticmethod
    def a___________________find___________________():
        """ Partie réservée à la recherche des données"""
        pass

    @staticmethod
    def find_qm(qm_current: QModelIndex, column: int, value=False):

        if not qm_check(qm_current):
            return None

        current_row = qm_current.row()

        model = qm_current.model()

        if model is None:
            return None

        qm = model.index(current_row, column)

        if not qm_check(qm):
            return None

        txt = qm.data()

        if not isinstance(txt, str):
            return None

        if value:
            return txt

        return qm

    def find_qm_title(self, title: str):

        if not isinstance(title, str):
            print("library -- WidgetLibraryTabManage -- find_bdd_path_file -- not isinstance(title, str)")
            return

        search_start = self.library_model.index(0, self.title_col)

        search_title = self.library_model.match(search_start, Qt.DisplayRole, title, 1, Qt.MatchExactly)

        if len(search_title) == 0:
            print("library -- WidgetLibraryTabManage -- find_bdd_path_file -- len(search_title)")
            return

        qm_title = search_title[0]

        if qm_check(qm_title):
            return qm_title

        return None

    def find_bdd_path_file(self, title: str):

        qm_title = self.find_qm_title(title=title)

        return self.find_qm(qm_current=qm_title, column=self.bdd_path_col, value=True)

    @staticmethod
    def a___________________event______():
        pass

    def dragEnterEvent(self, event: QDragEnterEvent):

        if event.mimeData().hasUrls():

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.drop_check_valide_bdd(bdd_path_file=file_path, add=False):
                event.accept()
            else:
                event.ignore()

        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):

        if event.mimeData().hasUrls():

            event.setDropAction(Qt.CopyAction)

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.drop_check_valide_bdd(bdd_path_file=file_path, add=False):
                event.accept()
            else:
                event.ignore()

        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):

        if event.mimeData().hasUrls():

            event.setDropAction(Qt.CopyAction)

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()
            if self.drop_check_valide_bdd(bdd_path_file=file_path, add=True):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def drop_check_valide_bdd(self, bdd_path_file: str, add=False) -> bool:

        if not isinstance(bdd_path_file, str):
            return False

        bdd_path_file = bdd_path_file.replace("/", "\\")

        search_start = self.library_model.index(0, 2)

        search = self.library_model.match(search_start, Qt.DisplayRole, bdd_path_file, 1, Qt.MatchExactly)

        if len(search) != 0:
            self.library_select_row_by_qm(qm_model=search[0])
            return False

        detection_tool = BddTypeDetection()

        check = detection_tool.search_bdd_type(file_path=bdd_path_file)

        if not check:
            msg(titre=self.widget_library.windowTitle(),
                message=detection_tool.error_message,
                icone_critique=True)
            return False

        if add:
            self.library_add_drop(bdd_type=detection_tool.bdd_type,
                                  bdd_path_file=detection_tool.file_path,
                                  title=detection_tool.bdd_title)

        return True

    @staticmethod
    def a___________________end___________________():
        pass


class LibraryTab(QWidget):
    ajouter_signal = pyqtSignal(ClipboardDatas, ClipboardDatas)

    def __init__(self, widget_library: Library, bdd_type: str, bdd_path_file: str, title: str):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_LibraryTab()
        self.ui.setupUi(self)

        self.hierarchy: Hierarchy = self.ui.hierarchy

        self.hierarchy.cat_filter_1.set_custom_filter(search_number="", search_type=pattern_filter)

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.widget_library = widget_library

        self.asc = self.widget_library.asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.hierarchy_main: Hierarchy = self.asc.ui.hierarchy

        self.allplan: AllplanDatas = self.widget_library.allplan
        self.catalog: CatalogDatas = self.widget_library.catalog

        # -----------------------------------------------
        # LOADING WIDGET LOADING
        # -----------------------------------------------

        self.loading = self.asc.loading

        # -----------------------------------------------
        # LOADING WIDGET Update
        # -----------------------------------------------

        self.widget_synchro = LibrarySynchro(asc=self.asc)

        self.widget_synchro.library_synchro_siganl.connect(self.library_synchro_started)

        # ---------------------------------------
        # VARIABLES
        # ---------------------------------------

        self.current_qs = None

        self.current_mode = "Ajout"

        self.bdd_type = bdd_type
        self.bdd_path_file = bdd_path_file

        self.title = title

        self.close_ui = True

        self.folders_all_list = list()
        self.materials_all_list = list()
        self.component_all_list = list()

        self.folders_select_list = list()
        self.materials_select_list = list()
        self.component_select_list = list()

        self.details_select = False

        # ---------------------------------------
        # LOADING HIERARCHY
        # ---------------------------------------

        self.hierarchy.selectionModel().selectionChanged.connect(self.library_hierarchy_selection_changed)
        self.hierarchy.doubleClicked.connect(self.library_hierarchy_double_clicked)
        self.hierarchy.customContextMenuRequested.connect(self.library_hierarchy_menu_show)

        # ---------------------------------------
        # LOADING SIGNALS - REFRESH
        # ---------------------------------------

        self.ui.library_refresh.clicked.connect(self.library_refresh)

        # ---------------------------------------
        # LOADING SIGNALS - EXPAND / COLLAPSE
        # ---------------------------------------

        self.ui.library_expand_all.clicked.connect(self.expand_menu_show)
        self.ui.library_collapse_all.clicked.connect(self.collapse_menu_show)

        # ---------------------------------------
        # LOADING SIGNALS - SEARCH
        # ---------------------------------------

        self.search_filter_widget = SearchFiterWidget(asc=self.asc, filter_button=self.ui.search_bt)
        self.search_filter_widget.modify_search_filter.connect(self.search_filter_changed)
        self.search_filter_widget.cancel_search_filter.connect(self.search_clear)

        self.ui.search_line.textChanged.connect(self.search_line_changed)

        self.ui.search_bt.clicked.connect(self.search_filter_show)
        self.ui.search_bt.customContextMenuRequested.connect(self.search_filter_show)

        # =============================================================
        # LOADING DETAILS - Model
        # ---------------------------------------

        self.library_detail_model = QStandardItemModel()
        self.library_detail_titles_list = [self.tr("Numéro"), self.tr("Nom"), self.tr("Valeur")]
        self.library_detail_model.setHorizontalHeaderLabels(self.library_detail_titles_list)

        # ---------------------------------------
        # LOADING DETAILS - Widget
        # ---------------------------------------

        get_look_tableview(self.ui.library_details)

        self.ui.library_details.setModel(self.library_detail_model)

        self.ui.library_details.selectionModel().selectionChanged.connect(self.details_selected)
        self.ui.library_details.doubleClicked.connect(self.remplacer_choisir_attribut)

        header = self.ui.library_details.horizontalHeader()

        if header is not None:
            header.setFixedHeight(24)

        # ---------------------------------------
        # LOADING DETAILS - Menu
        # ---------------------------------------

        self.ui.library_details.customContextMenuRequested.connect(self.details_menu_show)

        # ---------------------------------------
        # LOADING SIGNALS - Buttons
        # ---------------------------------------

        self.ui.library_synchro.clicked.connect(self.library_synchro_clicked)

        self.ui.ok.clicked.connect(self.ajouter_datas)
        self.ui.quit.clicked.connect(self.widget_library.close)

    def mode_manage(self):

        if self.current_mode == "Ajout":

            # todo corriger bug + activer
            self.hierarchy.setDragEnabled(False)

            self.ui.ok.setToolTip(self.tr("Ajouter les éléments sélectionnés"))

            self.ui.library_synchro.setVisible(True)
            self.ui.library_synchro.setEnabled(self.hierarchy.cat_model.rowCount() != 0)

            self.ui.library_details.setSelectionMode(QAbstractItemView.ExtendedSelection)

            self.creation_bottom_message()
            self.manage_add_button()

        else:

            self.hierarchy.setDragEnabled(False)

            self.ui.ok.setText(self.tr("Choisir"))
            self.ui.ok.setToolTip(self.tr("Choisir un attribut"))

            self.ui.library_details.setSelectionMode(QAbstractItemView.SingleSelection)

            self.ui.add_possibilities_title.setVisible(False)

            self.ui.folder.setVisible(False)
            self.ui.material.setVisible(False)
            self.ui.component.setVisible(False)
            self.ui.attribute.setVisible(False)
            self.ui.none.setVisible(False)

            self.ui.library_synchro.setVisible(False)

        self.manage_add_button()

    def manage_add_button(self):

        if self.current_mode == "Ajout":

            if self.details_select:
                self.ui.ok.setEnabled(True)
                self.ui.ok.setText(self.tr("Ajouter attribut"))
                return

            verification = self.library_possible_to_add()
            self.ui.ok.setEnabled(verification)

            self.ui.ok.setText(self.tr("Ajouter"))
            return

        verification = self.remplacer_verif_possibilite()
        self.ui.ok.setEnabled(verification)

    def creation_bottom_message(self):

        if self.current_mode != "Ajout":
            return

        if self.current_qs == self.hierarchy_main.cat_model.invisibleRootItem():
            possibility = [folder_code]

        elif isinstance(self.current_qs, Folder):
            possibility = [folder_code, material_code]

        elif isinstance(self.current_qs, Material):
            possibility = [material_code, component_code, link_code, attribute_code]

        elif isinstance(self.current_qs, Component):
            possibility = [component_code, link_code, attribute_code]

        elif isinstance(self.current_qs, Link):
            possibility = [component_code, link_code]

        else:
            return

        self.ui.folder.setVisible(folder_code in possibility)
        self.ui.material.setVisible(material_code in possibility)
        self.ui.component.setVisible(component_code in possibility)
        self.ui.link.setVisible(link_code in possibility)
        self.ui.attribute.setVisible(attribute_code in possibility)
        self.ui.none.setVisible(len(possibility) == 0)

    def progression_show(self, message: str):

        move_window_tool(widget_parent=self.widget_library, widget_current=self.loading, always_center=True)

        self.loading.launch_show(message)

    @staticmethod
    def a___________________loading_model______():
        pass

    def loading_model(self):

        self.ui.library_refresh.setEnabled(False)
        self.ui.library_synchro.setEnabled(False)
        self.ui.ok.setEnabled(False)

        if self.bdd_type == bdd_type_xml:
            worker = CatalogLoad(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_fav:
            worker = ConvertFavorite(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_kukat:
            worker = ConvertKukat(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_excel:
            if self.bdd_path_file.lower().endswith(".xlsx"):
                worker = ConvertExcel(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)
            else:
                worker = ConvertCSV(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type in [bdd_type_bcm, bdd_type_allmetre_e, bdd_type_allmetre_a]:
            worker = ConvertBcmMaterial(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)
            worker.errors_signal.connect(self.library_error_show)

        elif self.bdd_type == bdd_type_bcm_c:
            worker = ConvertBcmComposants(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif (self.bdd_type == bdd_type_synermi or self.bdd_type == bdd_type_capmi or self.bdd_type == bdd_type_progemi
              or self.bdd_type == bdd_type_gimi or self.bdd_type == bdd_type_extern):

            worker = ConvertExtern(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_mxdb:

            worker = ConvertMXDB(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_nevaris:

            worker = ConvertNevarisXml(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_nevaris_xlsx:

            worker = ConvertNevarisExcel(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_xpwe:

            worker = ConvertXpwe(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_team_system_xml:

            worker = ConvertTeamSystemXml(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        elif self.bdd_type == bdd_type_team_system_xlsx:

            worker = ConvertTeamSystemXlsx(allplan=self.allplan, file_path=self.bdd_path_file, bdd_title=self.title)

        else:
            self.hierarchy.loading_model(QStandardItemModel(), list(), list())
            self.library_load_end()
            return

        worker.loading_completed.connect(self.hierarchy.loading_model)
        worker.loading_completed.connect(self.library_load_end)

        worker.errors_signal.connect(self.library_error_show)

        self.progression_show(self.tr("Chargement en cours ..."))

        worker.run()

    @staticmethod
    def a___________________model_activation______():
        pass

    def library_load_end(self):

        self.loading.hide()

        # --------------

        self.ui.library_refresh.setEnabled(True)
        self.ui.library_synchro.setEnabled(
            self.hierarchy.cat_model.rowCount() != 0 and self.hierarchy_main.cat_model.rowCount() != 0)

    def library_error_show(self, errors_list: list):

        if len(errors_list) == 0:
            return

        msg(titre=application_title,
            message=self.tr("Une ou des erreurs ont été détectées"),
            icone_avertissement=True,
            details=errors_list,
            afficher_details=True)

    @staticmethod
    def a___________________hierarchie_change______():
        pass

    def library_hierarchy_selection_changed(self):

        self.details_select = False

        self.hierarchy.selection_manage()

        self.library_hierarchy_selection_change()

    def library_hierarchy_selection_change(self):

        if self.library_detail_model.rowCount() != 0:
            self.details_reset()

        if self.hierarchy.cat_model.rowCount() == 0:
            return

        self.hierarchy.header_manage()

        print(self.library_possible_to_add())

        selection_qs_list = self.hierarchy.get_qs_selection_list()

        if len(selection_qs_list) != 1:
            self.manage_add_button()
            self.details_reset()
            return

        qs: MyQstandardItem = selection_qs_list[0]

        if not isinstance(qs, MyQstandardItem):
            self.manage_add_button()
            return

        if not isinstance(qs, Material) and not isinstance(qs, Component):
            self.manage_add_button()
            return

        attributes_count: int = qs.rowCount()

        current_list = list()
        datas_list = list()

        attrib_master = False

        for attribute_index in range(attributes_count):

            qs_value: QStandardItem = qs.child(attribute_index, col_cat_value)

            item_type: str = qs_value.data(user_data_type)

            if attribute_code not in item_type:
                break

            qs_number: QStandardItem = qs.child(attribute_index, col_cat_number)

            if not isinstance(qs_number, Info):
                print("library -- LibraryTab -- library_hierarchy_selection_change -- not isinstance(qs_number, Info)")
                continue

            number_str = qs_number.text()

            if number_str in current_list:
                continue

            if number_str == attribut_default_obj.current:
                attrib_master = True

            current_list.append(number_str)

            attribute_obj = self.allplan.attributes_dict.get(number_str)

            if not isinstance(attribute_obj, AttributeDatas):
                print("library -- LibraryTab -- library_hierarchy_selection_change -- "
                      "not isinstance(attribute_obj, AttributeDatas)")
                continue

            name = attribute_obj.name

            if not isinstance(name, str) or name == "":
                continue

            value = qs_value.text()

            datas_list.append([number_str, name, value])

        if not attrib_master:
            datas_list.append([attribut_default_obj.current, attribute_name_default_base, qs.text()])

        datas_list.sort(key=lambda x: int(x[0]))

        for number_str, name, value in datas_list:
            self.details_add(number_str, name, value)

        self.details_header_manage()

        self.manage_add_button()

    def library_possible_to_add(self) -> bool:
        return self.hierarchy.library_possible_to_add(library_treeview=self.hierarchy, qs_target=self.current_qs)

    @staticmethod
    def a___________________liste_detail______():
        pass

    def details_selected(self):

        selection_list = self.ui.library_details.selectionModel().selectedRows()

        selection_count = len(selection_list)

        if selection_count == 0:
            self.details_select = False
            self.manage_add_button()
            return

        details_list = list()

        for qm in selection_list:

            if not qm_check(qm):
                continue

            number = qm.data()

            if not isinstance(number, str):
                continue

            if number == attribut_default_obj.current:
                continue

            if isinstance(self.current_qs, Folder) and number != "207":
                self.details_select = False
                self.manage_add_button()
                return

            details_list.append(number)

        self.details_select = len(details_list) != 0
        self.manage_add_button()

    def details_reset(self):

        self.library_detail_model.clear()
        self.library_detail_model.setHorizontalHeaderLabels(self.library_detail_titles_list)

    def details_add(self, number, name, value):

        qs_value = QStandardItem(value)
        qs_value.setToolTip(value)

        self.library_detail_model.appendRow([QStandardItem(number), QStandardItem(name), qs_value])

    def details_header_manage(self):

        if self.ui.library_details.horizontalHeader() is None:
            return

        self.ui.library_details.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.ui.library_details.setColumnWidth(col_cat_number, 50)

        self.ui.library_details.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.library_details.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    @staticmethod
    def a___________________search______():
        pass

    def search_line_changed(self):

        if not self.ui.search_bt.isChecked():
            return

        text = self.ui.search_line.text()

        text = text.strip()

        if text != "" and len(text) > 1:
            self.search_action(update=True)
            return

        if text == "":
            self.search_clear()

    def search_action(self, update=False):

        if self.ui.search_bt.isChecked() and self.ui.search_line.text() != "":

            if not update:
                self.hierarchy.save_qm_model_expanded_list()

                self.ui.search_line.setStyleSheet("QLineEdit{padding-left:4px; "
                                                  "border: 2px solid orange;border-radius:5px; }")

                self.ui.search_bt.setIcon(get_icon(search_clear_icon))

                self.ui.search_bt.setToolTip(self.tr("Supprimer la recherche"))

            self.search_refresh()
            return

        self.search_clear()
        return

    def search_refresh(self):

        current_text = self.ui.search_line.text()

        if current_text == "":
            self.search_clear()
            return

        if not self.hierarchy.search_text(current_text=current_text,
                                          search_column=self.search_filter_widget.search_column,
                                          search_number=self.search_filter_widget.search_number,
                                          search_type=self.search_filter_widget.search_type,
                                          search_mode=self.search_filter_widget.search_mode,
                                          search_case=self.search_filter_widget.search_case):
            self.search_clear()
            return

        self.ui.search_bt.setChecked(True)

    @staticmethod
    def a___________________filter_setting_______________():
        pass

    def search_filter_show(self):

        if not self.ui.search_bt.isChecked():
            self.search_clear()
            return

        self.ui.search_bt.setChecked(False)

        self.hierarchy.save_qm_model_expanded_list()

        self.search_filter_widget.search_show(search_current=self.ui.search_line.text().strip())

    def search_filter_enter_pressed(self):

        if self.ui.search_bt.isChecked():
            return

        self.ui.search_bt.setChecked(True)

        self.search_filter_show()

    def search_filter_changed(self):

        update = self.hierarchy.cat_filter_1.filterRegExp().pattern() != pattern_filter

        self.ui.search_bt.setChecked(True)

        self.search_action(update=update)

    @staticmethod
    def a___________________search_clear_______________():
        pass

    def search_clear(self):

        self.details_reset()

        self.ui.search_bt.setChecked(False)

        self.ui.search_line.setStyleSheet("QLineEdit{padding-left:5px; border: 1px solid #8f8f91;border-radius:5px; }")

        self.ui.search_bt.setIcon(get_icon(search_icon))
        self.ui.search_bt.setToolTip(self.tr("Lancer la recherche"))

        # ----------------------------

        self.hierarchy.search_clear()

    @staticmethod
    def a___________________search_current_text_______________():
        pass

    def get_search_current_text(self):

        if self.ui.library_details.hasFocus():

            selected_items = self.ui.library_details.selectionModel().selectedRows(2)

            if len(selected_items) != 0:

                qm = selected_items[0]

                if qm_check(qm):

                    text_current = qm.data()

                    if isinstance(text_current, str) and text_current != "":
                        self.search_text(text_current=text_current)
                        return

        qm_filter_selection_list = self.hierarchy.get_qm_filter_selection_list()

        if len(qm_filter_selection_list) != 1:
            return

        qm: QModelIndex = qm_filter_selection_list[0]

        if not qm_check(qm):
            return

        text_current = qm.data()

        if not isinstance(text_current, str) or text_current == "":
            return

        self.search_text(text_current=text_current)

    def search_text(self, text_current: str):

        if not isinstance(text_current, str):
            return

        if text_current == "":
            return

        if self.ui.search_bt.isChecked():
            return

        self.hierarchy.save_qm_model_expanded_list()

        self.ui.search_line.setText(text_current)
        self.ui.search_bt.setChecked(True)
        self.search_filter_show()

    @staticmethod
    def a___________________ajouter_items______():
        pass

    def library_hierarchy_double_clicked(self):

        if not self.library_possible_to_add():

            qm: QModelIndex = self.hierarchy.selectionModel().currentIndex()

            if not qm_check(qm):
                return None

            column = qm.column()

            if column != col_cat_value:
                qm: QModelIndex = self.hierarchy.model().index(qm.row(), col_cat_value, qm.parent())

                if not qm_check(qm):
                    return None

            qs = self.hierarchy.get_qs_by_qm(qm=qm)

            if not isinstance(qs, MyQstandardItem):
                return

            if not isinstance(qs, Folder):

                children_list = qs.get_children_type_list()

                attributes_list = [attribute for attribute in children_list if attribute.startswith(attribute_code)]

                if len(children_list) == len(attributes_list):
                    if self.current_mode == "Ajout":
                        return

                    a = self.tr("Pour la fonction")
                    b = self.tr("Rechercher et Remplacer")
                    c = self.tr("il est nécessaire de choisir un attribut")

                    msg(titre=self.widget_library.windowTitle(),
                        message=f"{a} : '{b}'<br><b>{c}.",
                        icone_avertissement=True,
                        type_bouton=QMessageBox.Ok)
                    return

            if self.hierarchy.isExpanded(qm):
                self.hierarchy.collapse(qm)
            else:
                self.hierarchy.expand(qm)
                self.hierarchy.scrollTo(qm, QAbstractItemView.PositionAtCenter)

            return

        self.ajouter_datas_action()

    def remplacer_verif_possibilite(self) -> bool:

        if self.current_mode == "Ajout":
            return True

        selection_list = self.ui.library_details.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return False

        return True

    def ajouter_datas(self):

        if self.current_mode == "Ajout":

            self.ajouter_datas_action()

        else:
            if not self.remplacer_verif_possibilite():
                return

            self.remplacer_choisir_attribut()

    def ajouter_datas_action(self):

        if not self.details_select:

            if not self.library_possible_to_add():
                return

            self.add_items_action()

        else:

            self.add_attributes_action()

        if not self.close_ui:
            self.close_ui = True
            return

        self.catalog.change_made = True

    def add_items_action(self) -> bool:

        if not self.library_possible_to_add():
            print("library -- LibraryTab -- add_items_action -- not self.library_possible_to_add()")
            return False

        # -------------

        qs_selection_list = self.hierarchy.get_qs_selection_list()

        if len(qs_selection_list) == 0:
            print("library -- LibraryTab -- add_items_action -- len(qs_selection_list) == 0")
            return False

        qs_selection_list.sort()

        # -------------

        qs_first = qs_selection_list[0]

        if not isinstance(qs_first, (Folder, Material, Component, Link)):
            print("library -- LibraryTab -- add_items_action -- not isinstance(qs_first, MyQstandardItem)")
            return False

        item_type = qs_first.data(user_data_type)

        clipboard_datas = ClipboardDatas(item_type)

        # -------------

        for qs_value in qs_selection_list:

            if not isinstance(qs_value, MyQstandardItem):
                print("library -- LibraryTab -- add_items_action -- not isinstance(qs_value, MyQstandardItem)")
                continue

            # -------------

            title = qs_value.text()

            if not isinstance(title, str):
                print("library -- LibraryTab -- add_items_action -- not isinstance(title, str)")
                continue

            # -------------
            qs_parent = qs_value.parent()

            if not isinstance(qs_parent, QStandardItem):
                qs_parent = self.hierarchy.cat_model.invisibleRootItem()

            # -------------

            row_current = qs_value.row()

            # -------------

            qs_desc = qs_parent.child(row_current, col_cat_desc)

            if not isinstance(qs_desc, Info):
                print("library -- LibraryTab -- add_items_action -- not isinstance(qs_desc, Info)")
                continue

            # -------------

            qs_number = qs_parent.child(row_current, col_cat_number)

            if not isinstance(qs_number, Info):
                print("library -- LibraryTab -- add_items_action -- not isinstance(qs_desc, Info)")
                continue

            # -------------

            clipboard_datas.append(key=title, value=[qs_value, qs_desc, qs_number])

            # -------------

        self.ajouter_signal.emit(clipboard_datas, ClipboardDatas(item_type))

    def add_attributes_action(self):

        if not isinstance(self.current_qs, MyQstandardItem):
            return

        if isinstance(self.current_qs, Link):
            return

        selection_list: list = self.ui.library_details.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return False

        selection_list.sort()

        # ---------------------------

        hierarchy_selected_list: list = self.hierarchy.get_qm_filter_selection_list()

        if len(hierarchy_selected_list) != 1:
            return False

        hierarchy_qm = hierarchy_selected_list[0]

        if not qm_check(hierarchy_qm):
            return

        hierarchy_qs = self.hierarchy.get_qs_by_qm(qm=hierarchy_qm)

        if not isinstance(hierarchy_qs, (Folder, Material, Component)):
            return

        hierarchy_numbers_datas = hierarchy_qs.get_attribute_numbers_datas()

        if len(hierarchy_numbers_datas) == 0:
            return

        # ---------------------------

        layer_in = False
        fill_in = False
        room_in = False

        clipboard = ClipboardDatas(type_element=attribute_code)

        for qm_number in selection_list:

            if not isinstance(qm_number, QModelIndex):
                continue

            if not qm_check(qm_number):
                continue

            number = qm_number.data()

            if not isinstance(number, str):
                continue

            if number == attribute_default_base:
                continue

            if isinstance(self.current_qs, Folder) and number != "207":
                continue

            qm_value = self.library_detail_model.index(qm_number.row(), 2)

            if not qm_check(qm_value):
                continue

            value = qm_value.data()

            if not isinstance(value, str):
                continue

            if number in attribute_val_default_layer:

                if layer_in:
                    continue

                self.add_clipboard(title=self.tr("Groupe Layer"),
                                   defaut_dict=attribute_val_default_layer,
                                   hierarchy_datas=hierarchy_numbers_datas,
                                   clipboard=clipboard)

                layer_in = True

            elif number in attribute_val_default_fill:

                if fill_in:
                    continue

                self.add_clipboard(title=self.tr("Groupe Remplissage"),
                                   defaut_dict=attribute_val_default_fill,
                                   hierarchy_datas=hierarchy_numbers_datas,
                                   clipboard=clipboard)

                fill_in = True

            elif number in attribute_val_default_room:

                if room_in:
                    continue

                self.add_clipboard(title=self.tr("Groupe Pièce"),
                                   defaut_dict=attribute_val_default_room,
                                   hierarchy_datas=hierarchy_numbers_datas,
                                   clipboard=clipboard)

                room_in = True

            else:

                self.add_clipboard(title=f"{number} --  {value}",
                                   defaut_dict={number: value},
                                   hierarchy_datas=hierarchy_numbers_datas,
                                   clipboard=clipboard)

        self.catalog.attribute_paste_action(clipboard_attribute=clipboard, title="", id_ele="0")

        filter_selection_list = self.hierarchy_main.get_qm_filter_selection_list()

        if len(filter_selection_list) == 0:
            return

        self.hierarchy_main.select_list(selected_list=filter_selection_list, scrollto=False)

    def add_clipboard(self, title: str, defaut_dict: dict, hierarchy_datas: dict, clipboard: ClipboardDatas) -> bool:

        if (not isinstance(defaut_dict, dict) or not isinstance(hierarchy_datas, dict) or
                not isinstance(clipboard, ClipboardDatas)):
            return False

        global_qs_list = list()

        for number, value in defaut_dict.items():

            if number in hierarchy_datas:

                qs_list = hierarchy_datas[number]

                if not isinstance(qs_list, list):
                    return False

                if len(qs_list) != 3:
                    return False

                global_qs_list.extend(qs_list)

                continue

            if len(defaut_dict) == 1:
                return False

            qs_temp_list = self.allplan.creation.attribute_line(value=value, number_str=number)

            if not isinstance(qs_temp_list, list):
                return False

            if len(qs_temp_list) != 3:
                return False

            global_qs_list.extend(qs_temp_list)

        clipboard.append(key=title, value=global_qs_list)

        return True

    def remplacer_choisir_attribut(self):

        if self.current_mode == "Ajout":
            return

        selection_list = self.ui.library_details.selectionModel().selectedRows(0)

        if len(selection_list) != 1:
            return

        current_qm: QModelIndex = selection_list[0]

        current_row: int = current_qm.row()

        qm_number: QModelIndex = self.library_detail_model.index(current_row, 0)
        qm_value: QModelIndex = self.library_detail_model.index(current_row, 2)

        if not qm_check(qm_value) or not qm_check(qm_number):
            return

        value = qm_value.data()
        number = qm_number.data()

        self.widget_library.librairie_reception_valeur(number=number, value=value)
        self.widget_library.close()

    def link_copy_manage(self, qs_child: MyQstandardItem):

        current_txt = self.current_qs.text()
        link_text = qs_child.text()

        if not isinstance(current_txt, str) or not isinstance(link_text, str):
            return False

        link_text_upper = link_text.upper()

        if link_text_upper == current_txt.upper():
            print("Impossible : link_text_upper == current_txt")
            return False

        if link_text_upper not in material_upper_list:
            print(f"Impossible : L'ouvrage {link_text} n'existe pas")
            return False

        return True

    def formula_add(self, qs: MyQstandardItem):

        if not isinstance(qs, Component):
            return

        search_attribute = qs.get_attribute_value_by_number("267")

        if search_attribute is not None:
            return

        unit = qs.get_attribute_value_by_number("202")

        if unit is None:
            unit = "m²"

        unit = self.allplan.convert_unit(unit=unit)

        formula = self.allplan.recherche_formule_defaut(unit)

        qs_list = self.allplan.creation.attribute_line(value=formula, number_str="267")

        insert_index = qs.get_attribute_insertion_index("267")

        qs.insertRow(insert_index, qs_list)

    @staticmethod
    def a___________________refresh______():
        pass

    def library_refresh(self):
        self.search_clear()
        self.details_reset()
        self.loading_model()

    def get_attributes_all(self) -> dict:

        self.folders_all_list.clear()
        self.materials_all_list.clear()
        self.component_all_list.clear()

        attribut_all = dict()

        search_start = self.hierarchy.cat_model.index(0, 0)

        # --------------
        # Folder
        # --------------

        qm_folders_all_list = self.hierarchy.cat_model.match(search_start, user_data_type, folder_code, -1,
                                                             Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_folders_all_list) != 0:
            folders_list = self.get_attributes(search_list=qm_folders_all_list, item_type=folder_code)

            if len(folders_list) != 0:
                attribut_all[folder_code] = folders_list

        # --------------
        # Material
        # --------------

        qm_materials_all_list = self.hierarchy.cat_model.match(search_start, user_data_type, material_code, -1,
                                                               Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_materials_all_list) != 0:
            materials_list = self.get_attributes(search_list=qm_materials_all_list, item_type=material_code)

            if len(materials_list) != 0:
                attribut_all[material_code] = materials_list

        # --------------
        # Component
        # --------------

        qm_component_all_list = self.hierarchy.cat_model.match(search_start, user_data_type, component_code, -1,
                                                               Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_component_all_list) != 0:
            components_list = self.get_attributes(search_list=qm_component_all_list, item_type=component_code)

            if len(components_list) != 0:
                attribut_all[component_code] = components_list

        return attribut_all

    def get_attributes(self, search_list: list, item_type: str) -> list:

        final_list = list()

        if item_type == folder_code:
            current_list = self.folders_all_list
        elif item_type == material_code:
            current_list = self.materials_all_list
        elif item_type == component_code:
            current_list = self.component_all_list
        else:
            return list()

        for qm in search_list:

            qs = self.hierarchy.get_qs_by_qm(qm=qm)

            if not isinstance(qs, MyQstandardItem):
                continue

            current_list.append(qs)

            if item_type == folder_code:
                if "207" in final_list:
                    continue

                final_list.append("207")
                continue

            numbers_list = qs.get_attribute_numbers_list()

            for number in numbers_list:

                if number == "83":
                    continue

                if number not in final_list:
                    final_list.append(number)

        final_list.sort(key=int)

        return final_list

    def get_attributes_selection(self) -> dict:

        self.folders_select_list.clear()
        self.materials_select_list.clear()
        self.component_select_list.clear()

        attribut_select = dict()

        folders_list = list()
        materials_list = list()
        components_list = list()

        selection_list = self.hierarchy.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return attribut_select

        for qm in selection_list:

            if not qm_check(qm):
                continue

            qm: QModelIndex

            item_type = qm.data(user_data_type)

            if item_type != folder_code and item_type != material_code and item_type != component_code:
                continue

            qs_current = self.hierarchy.get_qs_by_qm(qm=qm)

            if not isinstance(qs_current, MyQstandardItem):
                continue

            self.get_attributes_child_selection(qs_current=qs_current,
                                                folders_list=folders_list,
                                                materials_list=materials_list,
                                                components_list=components_list)

        if len(folders_list) != 0:
            attribut_select[folder_code] = folders_list

        if len(materials_list) != 0:
            materials_list.sort(key=int)
            attribut_select[material_code] = materials_list

        if len(components_list) != 0:
            components_list.sort(key=int)
            attribut_select[component_code] = components_list

        return attribut_select

    def get_attributes_child_selection(self, qs_current: MyQstandardItem,
                                       folders_list: list,
                                       materials_list: list,
                                       components_list: list) -> None:

        if isinstance(qs_current, Folder):

            self.folders_select_list.append(qs_current)

            if "207" not in folders_list:
                folders_list.append("207")

            children_list = qs_current.get_children_qs(children=True, attributes=False)

            for qs_child_list in children_list:

                if len(qs_child_list) != 3:
                    continue

                qs_child = qs_child_list[col_cat_value]

                self.get_attributes_child_selection(qs_current=qs_child,
                                                    folders_list=folders_list,
                                                    materials_list=materials_list,
                                                    components_list=components_list)
            return

        if isinstance(qs_current, Material):

            self.materials_select_list.append(qs_current)

            numbers_list = qs_current.get_attribute_numbers_list()

            for number in numbers_list:

                if number == "83":
                    continue

                if number not in materials_list:
                    materials_list.append(number)
                    continue

            children_list = qs_current.get_children_qs(children=True, attributes=False)

            for qs_child_list in children_list:

                if len(qs_child_list) != 3:
                    continue

                qs_child = qs_child_list[col_cat_value]

                self.get_attributes_child_selection(qs_current=qs_child,
                                                    folders_list=folders_list,
                                                    materials_list=materials_list,
                                                    components_list=components_list)
            return

        if isinstance(qs_current, Component):

            self.component_select_list.append(qs_current)

            numbers_list = qs_current.get_attribute_numbers_list()

            for number in numbers_list:

                if number == "83":
                    continue

                if number not in components_list:
                    components_list.append(number)
                    continue

    @staticmethod
    def a___________________synchronisation______():
        pass

    def library_synchro_clicked(self):

        if self.hierarchy.cat_model.rowCount() == 0:
            return

        attributes_select = self.get_attributes_selection()
        attributes_all = self.get_attributes_all()

        if len(attributes_select) + len(attributes_all) == 0:
            return

        move_window_tool(widget_parent=self.widget_library, widget_current=self.widget_synchro, always_center=True)

        self.widget_synchro.show_synchro(attributes_select=attributes_select,
                                         attributes_all=attributes_all)

        return

    def library_synchro_started(self, selection: bool, folders_list: list, materials_list: list,
                                components_list: list, creation: bool):

        self.catalog.library_synchro_list = list()

        if selection:
            qm_folders_list = self.folders_select_list
            qm_materials_list = self.materials_select_list
            qm_components_list = self.component_select_list
        else:
            qm_folders_list = self.folders_all_list
            qm_materials_list = self.materials_all_list
            qm_components_list = self.component_all_list

        progress_text = self.tr("Synchronisation")

        self.progression_show(f"{progress_text} ...")

        synchro_count = 0

        if len(folders_list) != 0 and len(qm_folders_list) != 0:
            synchro_count += self.library_synchro_action(qs_list=qm_folders_list,
                                                         attributes_list=folders_list,
                                                         item_type=folder_code,
                                                         creation=creation)

        if len(materials_list) != 0 and len(qm_materials_list) != 0:
            synchro_count += self.library_synchro_action(qs_list=qm_materials_list,
                                                         attributes_list=materials_list,
                                                         item_type=material_code,
                                                         creation=creation)

        if len(components_list) != 0 and len(qm_components_list) != 0:
            synchro_count += self.library_synchro_action(qs_list=qm_components_list,
                                                         attributes_list=components_list,
                                                         item_type=component_code,
                                                         creation=creation)

        self.loading.hide()

        if synchro_count == 0:
            msg(titre=self.widget_synchro.windowTitle(),
                message=self.tr("Aucun élément a été synchronisé."),
                icone_valide=True,
                type_bouton=QMessageBox.Ok)
            return

        self.catalog.library_synchro_end()

        self.catalog.history_library_synchro()

        if synchro_count == 1:
            text = self.tr("élément à été synchronisé.")
        else:
            text = self.tr("éléments ont été actualisés.")

        msg(titre=self.widget_synchro.windowTitle(),
            message=f"{synchro_count} {text}",
            icone_valide=True,
            type_bouton=QMessageBox.Ok)

    def library_synchro_action(self, qs_list: list, attributes_list: list, item_type: str, creation: bool) -> int:

        checked_list = list()
        synchro_count = 0

        for qs in qs_list:

            if not isinstance(qs, (Folder, Material, Component)):
                continue

            row_count = qs.rowCount()

            code_current = qs.text()

            if not isinstance(code_current, str):
                continue

            if code_current in checked_list:
                continue

            checked_list.append(code_current)

            for index_row in range(row_count):

                qs_number = qs.child(index_row, col_cat_number)

                if not isinstance(qs_number, Info):
                    continue

                number = qs_number.text()

                if number not in attributes_list:
                    continue

                # --------------------

                qs_value = qs.child(index_row, col_cat_value)

                if not isinstance(qs_value, Attribute):
                    continue

                value = qs_value.text()

                if not isinstance(value, str):
                    continue

                # --------------------

                qs_index = qs.child(index_row, col_cat_index)

                if not isinstance(qs_index, Info):
                    continue

                index_value = qs_index.text()

                if not isinstance(index_value, str):
                    continue

                # --------------------

                synchro_count += self.catalog.library_synchro(code=code_current,
                                                              number=number,
                                                              value=value,
                                                              index_value=index_value,
                                                              item_type=item_type,
                                                              creation=creation)

        return synchro_count

    @staticmethod
    def a___________________menu_structure______():
        pass

    def library_hierarchy_menu_show(self, point: QPoint):

        self.details_select = False

        menu = MyContextMenu()

        if self.ui.ok.isEnabled():
            menu.add_title(title=self.tr("Ajouter"))

            menu.add_action(qicon=get_icon(expand_all_icon),
                            title=self.tr("Ajouter"),
                            action=self.ajouter_datas)

        menu.add_title(title=self.tr("Affichage"))

        # ------------------------------

        if self.ui.library_expand_all.isEnabled():
            expand_action = menu.add_action(qicon=get_icon(expand_all_icon),
                                            title=self.tr("Déplier"),
                                            tooltips=self.ui.library_expand_all.toolTip(),
                                            short_link=self.ui.library_expand_all.whatsThis())

            expand_action.setMenu(self.hierarchy.expand_menu_creation())

        # ------------------------------

        if self.ui.library_collapse_all.isEnabled():
            collapse_action = menu.add_action(qicon=get_icon(collapse_all_icon),
                                              title=self.tr("Replier"),
                                              tooltips=self.ui.library_collapse_all.toolTip(),
                                              short_link=self.ui.library_collapse_all.whatsThis())

            collapse_action.setMenu(self.hierarchy.collapse_menu_creation())

        # ------------------------------

        menu.exec_(self.hierarchy.mapToGlobal(point))

    @staticmethod
    def a___________________expand_buttons______():
        pass

    def expand_menu_show(self):

        expand_menu = self.hierarchy.expand_menu_creation()
        expand_menu.exec_(find_global_point(self.ui.library_expand_all))

    def expand_end(self):
        pass

    @staticmethod
    def a___________________collapse_buttons______():
        pass

    def collapse_menu_show(self):

        collapse_menu = self.hierarchy.collapse_menu_creation()
        collapse_menu.exec_(find_global_point(self.ui.library_collapse_all))

    def get_expanded_list(self):

        expanded_list = list()

        def recurse(qm_parent: QModelIndex):

            row_count = self.hierarchy.cat_filter_2.rowCount(qm_parent)

            for row_index in range(row_count):

                qm_category = self.hierarchy.cat_filter_2.index(row_index, col_cat_value, qm_parent)

                if not qm_check(qm_category):
                    continue

                ele_type = qm_category.data(user_data_type)

                if ele_type == component_code:
                    continue

                qm_model = self.hierarchy.map_to_model(qm=qm_category)

                if qm_model is None:
                    continue

                expanded_list.append(qm_model)

                if self.hierarchy.cat_filter_2.hasChildren(qm_category):
                    recurse(qm_parent=qm_category)

        recurse(QModelIndex())

        self.hierarchy.cat_model.invisibleRootItem()

        return expanded_list

    def restore_expanded_list(self, expanded_list: list):

        self.hierarchy.blockSignals(True)

        self.hierarchy.collapseAll()

        for qm_model in expanded_list:

            qm_filter = self.hierarchy.map_to_filter(qm=qm_model)

            if not qm_check(qm_filter):
                continue

            self.hierarchy.expand(qm_filter)

        self.hierarchy.blockSignals(False)

    @staticmethod
    def a___________________menu_details______():
        pass

    def details_menu_show(self, point: QPoint):

        index = self.ui.library_details.indexAt(point)

        point = QPoint(point.x(), point.y() + 35)

        if not index.isValid():
            return

        current_column = index.column()

        if current_column == 0:
            return

        current_txt: str = index.data()

        if current_txt == "":
            return

        if current_txt.startswith(self.tr("Issue du lien : ")):
            return

        menu = MyContextMenu()

        if self.details_select:
            menu.add_title(title=self.tr("Ajouter"))

            menu.add_action(qicon=get_icon(expand_all_icon),
                            title=self.tr("Ajouter"),
                            action=self.ajouter_datas)

        menu.add_title(title=self.tr("Options"))

        menu.add_action(qicon=get_icon(text_copy_icon),
                        title=self.tr("Copier la valeur dans le presse-papier"),
                        action=lambda: self.copier_la_valeur(index))

        menu.exec_(self.ui.library_details.mapToGlobal(point))

    def copier_la_valeur(self, index: QModelIndex):

        if not index.isValid():
            return

        QApplication.clipboard().setText(index.data())

        message = self.tr("est désormais dans votre presse-papier!")

        msg(titre=self.widget_library.windowTitle(),
            message=f"{index.data()} {message}",
            icone_valide=True)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Q:
            sizes_list = self.ui.bible_splitter.sizes()

            left_size = sizes_list[0] - 10
            right_size = sizes_list[1] + 10

            sizes_list = [left_size, right_size]

            self.ui.bible_splitter.setSizes(sizes_list)
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_D:
            sizes_list = self.ui.bible_splitter.sizes()

            left_size = sizes_list[0] + 10
            right_size = sizes_list[1] - 10

            sizes_list = [left_size, right_size]

            self.ui.bible_splitter.setSizes(sizes_list)
            return

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter and self.ui.search_line.hasFocus():
            self.search_filter_enter_pressed()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:

            if self.ui.search_bt.isChecked():
                return

            self.get_search_current_text()

    def dragEnterEvent(self, event: QDragEnterEvent):

        super().dragEnterEvent(event)

        if event.mimeData().hasUrls():

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            self.widget_library.tab_bar.setCurrentIndex(0)

            event.accept()
            return

        event.ignore()

    @staticmethod
    def a___________________end______():
        pass


class LibraryModify(QWidget):
    save_add = pyqtSignal(str, str, str)
    save_modifications = pyqtSignal(str, str, str, str)

    def __init__(self, widget_manage_tab: LibraryTabManage):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_LibraryModify()
        self.ui.setupUi(self)

        # -----------------------------------------------
        # PARENTS
        # -----------------------------------------------

        self.widget_manage_tab = widget_manage_tab

        self.asc = self.widget_manage_tab.asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.allplan: AllplanDatas = self.asc.allplan

        # -----------------------------------------------
        # WIDGET FORMAT
        # -----------------------------------------------

        self.widget_format = Formatting()
        self.widget_format.save_modif_formatage.connect(self.format_save)

        # -----------------------------------------------
        # VARIABLES
        # -----------------------------------------------

        self.original_title = ""
        self.default_path = ""
        self.bdd_type = ""

        self.old_bdd_path_file = ""
        self.old_url = ""

        self.titles_list = list()

        self.modification_mod = False
        self.used_bool = False

        self.change_made = False

        # -----------------------------------------------
        # SIGNALS
        # -----------------------------------------------

        self.ui.file_radio.clicked.connect(self.radio_file)
        self.ui.url_radio.clicked.connect(self.radio_url)

        self.ui.path.textChanged.connect(self.path_edit)
        self.ui.path.installEventFilter(self)

        self.ui.browser.clicked.connect(self.browser_show)

        self.ui.title.textChanged.connect(self.title_verification)

        self.ui.format_bt.clicked.connect(self.format_show)

        self.ui.verification.clicked.connect(self.verification_show)

        self.ui.ok.clicked.connect(self.save)
        self.ui.quit.clicked.connect(self.close)

    def tab_modify_show(self, bdd_type: str,
                        bdd_path_file: str,
                        title: str,
                        titles_list: list,
                        used_bool: bool,
                        default_path: str,
                        modification_mod=False):

        self.bdd_type = bdd_type
        self.modification_mod = modification_mod
        self.default_path = default_path

        self.original_title = title

        self.ui.title.setText(title)

        self.titles_list = titles_list

        self.used_bool = used_bool

        if self.modification_mod:
            self.setWindowTitle(self.tr("Modifier les paramètres"))

            used_bool = used_bool != "on"

            self.ui.file_radio.setEnabled(used_bool)
            self.ui.url_radio.setEnabled(used_bool)

            if bdd_path_file.startswith("http"):
                self.ui.url_radio.setChecked(True)
                self.radio_url()

            else:
                self.ui.file_radio.setChecked(True)
                self.radio_file()

            self.ui.path.blockSignals(True)
            self.ui.path.setText(bdd_path_file)
            self.ui.path.blockSignals(False)

            self.ui.ok.setText(self.tr("Modifier"))

        else:

            self.ui.file_radio.setEnabled(True)
            self.ui.url_radio.setEnabled(True)

            self.setWindowTitle(self.tr("Ajouter une bibliothèque externe"))
            self.ui.file_radio.setChecked(True)
            self.radio_file()
            self.ui.path.clear()
            self.title_verification()

            self.ui.ok.setText(self.tr("Ajouter"))

        self.change_made = False
        self.valid_button_manage()

        self.show()

    @staticmethod
    def a___________________radios______():
        pass

    def radio_file(self):

        self.ui.path.setReadOnly(True)

        current_path = self.ui.path.text()

        if current_path.startswith("http"):
            self.old_url = current_path

        if self.old_bdd_path_file != "":
            self.ui.path.setText(self.old_bdd_path_file)
        else:
            self.ui.path.clear()

        if self.modification_mod and self.used_bool:
            self.ui.path.setEnabled(False)
            self.ui.browser.setEnabled(False)
            self.ui.title.setFocus()

        else:
            self.ui.path.setEnabled(True)
            self.ui.browser.setEnabled(True)
            self.ui.browser.setFocus()

        self.change_made = True
        self.valid_button_manage()

    def radio_url(self):

        self.ui.path.setReadOnly(False)
        self.ui.browser.setEnabled(False)

        current_path = self.ui.path.text()

        if current_path.endswith(openable_file_extension):
            self.old_bdd_path_file = current_path

        if self.old_url != "":
            self.ui.path.setText(self.old_url)
        else:
            self.ui.path.clear()

        if self.modification_mod and self.used_bool:
            self.ui.path.setEnabled(False)
            self.ui.title.setFocus()
        else:
            self.ui.path.setEnabled(True)
            self.ui.path.setFocus()

        self.change_made = True
        self.valid_button_manage()

    @staticmethod
    def a___________________bouton_parcourir______():
        pass

    def browser_show(self):

        if self.modification_mod and self.used_bool:
            return

        extensions_list = [".xml", ".apn", ".prj", ".DBF", ".ARA", ".xlsx", ".csv", ".FIC", ".KAT", ".mxdb"]

        file_txt = self.tr("Fichier")
        favorite_txt = self.tr("Favori")
        cat_file_txt = self.tr("Fichier Catalogue")

        datas_filters = {self.tr("Fichier bibliothèque"): extensions_list,
                         cat_file_txt: [".xml", ".apn", ".prj"],
                         f"{file_txt} DBF": [".DBF"],
                         f"{file_txt} ARA": [".ARA"],
                         f"{file_txt} XSLX": [".xlsx"],
                         f"{file_txt} CSV": [".csv"],
                         f"{file_txt} FIC": [".FIC"],
                         f"{file_txt} KAT": [".KAT"],
                         f"{file_txt} MXDB": [".mxdb"],
                         f"{file_txt} XPWE": [".xpwe"]}

        dict_favorites_allplan = get_favorites_allplan_dict()

        for extension, title in dict_favorites_allplan.items():

            if f".{extension}" not in extensions_list:
                extensions_list.append(extension)

            datas_filters[f"{favorite_txt} {title}"] = [extension]

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.tmp_path]
        else:

            shortcuts_list = list()

        get_bdd_paths(shortcuts_list=shortcuts_list)

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[library_setting_file, "path_open"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters=datas_filters,
                                 current_path=self.ui.path.text(),
                                 default_path=self.default_path,
                                 use_setting_first=False)

        if file_path == "":
            return

        if file_path.endswith(".apn") or file_path.endswith(".prj"):

            # todo à modifier

            if "2024" in self.allplan.version_datas:
                version_obj = self.allplan.version_datas["2024"]

                if not isinstance(version_obj, AllplanPaths):
                    return

                chemin_prj = version_obj.prj_path

            elif "2025" in self.allplan.version_datas:

                version_obj = self.allplan.version_datas["2025"]

                if not isinstance(version_obj, AllplanPaths):
                    return

                chemin_prj = version_obj.prj_path

            else:
                return

            file_path = get_real_path_of_apn_file(file_path, chemin_prj, is_cat_folder=True)

            # self.allplan.allplan_paths

        default_path = find_folder_path(file_path)

        if default_path != "":
            self.default_path = default_path

        self.check_valide_bdd(bdd_path_file=file_path, add=True, message=True)

    def path_edit(self):

        if not self.ui.url_radio.isChecked():
            return

        if self.modification_mod and self.used_bool:
            return

        self.check_valide_bdd(bdd_path_file=self.ui.path.text(), add=True, message=True)

    @staticmethod
    def a___________________title______():
        pass

    def title_verification(self) -> str:

        current_text = self.ui.title.text().strip()

        linedit_style_ok = ("QLineEdit{padding-left: 5px; "
                            "border: 1px solid #8f8f91; "
                            "border-right-width: 0px; "
                            "border-top-left-radius:5px; "
                            "border-bottom-left-radius: 5px; }")

        linedit_style_error = ("QLineEdit{padding-left: 5px; "
                               "border: 2px solid orange; "
                               "border-top-left-radius:5px; "
                               "border-bottom-left-radius: 5px; }")

        if current_text == "":
            self.ui.verification.setIcon(get_icon(error_icon))
            self.ui.verification.setToolTip(self.tr("Vous ne pouvez pas laisser le titre vide."))

            self.ui.title.setStyleSheet(linedit_style_error)

            self.change_made = True
            self.valid_button_manage()

            return self.tr("Vous ne pouvez pas laisser le titre vide.")

        if current_text.upper() == self.original_title.upper() and self.modification_mod:
            self.ui.verification.setIcon(get_icon(valid_icon))
            self.ui.verification.setToolTip(self.tr("C'est tout bon!"))
            self.ui.ok.setEnabled(self.bdd_type != "")

            self.ui.title.setStyleSheet(linedit_style_ok)

            self.change_made = True
            self.valid_button_manage()

            return "Ok"

        if current_text.upper() in self.titles_list:
            self.ui.verification.setIcon(get_icon(error_icon))
            self.ui.verification.setToolTip(self.tr("Ce titre est déjà utilisé."))

            self.ui.title.setStyleSheet(linedit_style_error)

            self.change_made = True
            self.valid_button_manage()

            return self.tr("Ce titre est déjà utilisé.")

        self.ui.verification.setIcon(get_icon(valid_icon))
        self.ui.verification.setToolTip(self.tr("C'est tout bon!"))
        self.ui.ok.setEnabled(self.bdd_type != "")

        self.ui.title.setStyleSheet(linedit_style_ok)

        self.change_made = True
        self.valid_button_manage()

        return "Ok"

    def verification_show(self):

        tootltips = self.ui.verification.toolTip()
        icon_valid = tootltips == self.tr("C'est tout bon!")

        msg(titre=self.windowTitle(),
            message=tootltips,
            icone_valide=icon_valid,
            icone_avertissement=not icon_valid)

    def format_show(self):

        self.widget_format.formatting_show(current_parent=self.ui.format_bt,
                                           current_text=self.ui.title.text(),
                                           show_code=False, show_search=False)

    def format_save(self, new_text: str):

        if self.original_title == new_text:
            return

        self.ui.title.setText(new_text)

        self.change_made = True
        self.valid_button_manage()

    @staticmethod
    def a___________________valid_manage______():
        pass

    def valid_button_manage(self) -> bool:

        if self.ui.path.text() == "" or self.ui.verification.toolTip() != self.tr(
                "C'est tout bon!") or not self.change_made:
            self.ui.ok.setEnabled(False)
            return False

        self.ui.ok.setEnabled(True)
        return True

    @staticmethod
    def a___________________save______():
        pass

    def save(self):

        if not self.valid_button_manage():
            return

        if self.modification_mod:
            self.save_modifications.emit(self.bdd_type, self.ui.path.text(), self.ui.title.text(), self.original_title)
        else:
            self.save_add.emit(self.ui.title.text(), self.ui.path.text(), self.bdd_type)

        self.close()

    def save_settings(self):

        config_datas = settings_read(file_name=library_setting_file)

        if not isinstance(config_datas, dict):
            return

        # --------------------------------------------

        if self.bdd_type == bdd_type_xml and "path_cat" in config_datas:
            key = "path_cat"

        elif self.bdd_type == bdd_type_excel and "path_excel" in config_datas:
            key = "path_excel"

        elif self.bdd_type == bdd_type_fav and "path_favorites" in config_datas:
            key = "path_favorites"

        elif (self.bdd_type == bdd_type_bcm or self.bdd_type == bdd_type_bcm_c) and "path_bcm" in config_datas:
            key = "path_bcm"

        elif self.bdd_type == bdd_type_kukat and "path_kukat" in config_datas:
            key = "path_kukat"

        elif ((
                      self.bdd_type == bdd_type_allmetre_e or self.bdd_type == bdd_type_allmetre_a)
              and "path_alltop" in config_datas):
            key = "path_alltop"

        elif self.bdd_type == bdd_type_gimi and "path_gimi" in config_datas:
            key = "path_gimi"

        else:
            key = "path_open"

        folder_path = find_folder_path(file_path=self.ui.path.text())

        if not os.path.exists(folder_path):
            return

        config_datas[key] = folder_path

        settings_save(file_name=library_setting_file, config_datas=config_datas)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:

            self.save()

        elif event.key() == Qt.Key_Escape:

            self.close()

        super().keyPressEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if event.type() != QEvent.MouseButtonRelease:
            return super().eventFilter(obj, event)

        if obj != self.ui.path:
            return super().eventFilter(obj, event)

        if self.ui.url_radio.isChecked():
            return super().eventFilter(obj, event)

        if self.modification_mod and self.used_bool:
            return super().eventFilter(obj, event)

        self.browser_show()

        return super().eventFilter(obj, event)

    def dragEnterEvent(self, event: QDragEnterEvent):

        if self.modification_mod and self.used_bool:
            event.ignore()

        if event.mimeData().hasUrls():

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.check_valide_bdd(bdd_path_file=file_path, add=False):
                event.accept()
            else:
                event.ignore()

        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):

        if self.modification_mod and self.used_bool:
            event.ignore()

        if event.mimeData().hasUrls():

            event.setDropAction(Qt.CopyAction)

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()

            if self.check_valide_bdd(bdd_path_file=file_path, add=False):
                event.accept()
            else:
                event.ignore()

        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):

        if self.modification_mod and self.used_bool:
            event.ignore()

        if event.mimeData().hasUrls():

            event.setDropAction(Qt.CopyAction)

            urls = event.mimeData().urls()

            if len(urls) != 1:
                event.ignore()
                return

            url = urls[0]
            file_path = url.toLocalFile()
            if self.check_valide_bdd(bdd_path_file=file_path, add=True, message=False):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def check_valide_bdd(self, bdd_path_file: str, add=False, message=False) -> bool:

        if not isinstance(bdd_path_file, str):
            return False

        if bdd_path_file == "":
            return False

        if bdd_path_file.startswith("http"):
            bdd_path_file = bdd_path_file.replace("\\", "/")
        else:
            bdd_path_file = bdd_path_file.replace("/", "\\")

        search_path = self.widget_manage_tab.library_model.findItems(bdd_path_file, Qt.MatchExactly, 2)

        if len(search_path) != 0:

            filename = find_filename(bdd_path_file)
            already_exist_txt = self.tr("existe déjà")

            if self.default_path == bdd_path_file:
                return True

            if message:
                msg(titre=self.windowTitle(),
                    message=f"{filename} {already_exist_txt}",
                    icone_critique=True)
            return False

        detection_tool = BddTypeDetection()

        check = detection_tool.search_bdd_type(file_path=bdd_path_file)

        if not check:

            if message:
                msg(titre=self.windowTitle(),
                    message=detection_tool.error_message,
                    icone_critique=True)
                return False

        if add:
            self.bdd_type = detection_tool.bdd_type

            self.ui.path.setText(detection_tool.file_path)
            self.ui.title.setText(detection_tool.bdd_title)

            self.ui.title.setFocus()

            self.change_made = True
            self.valid_button_manage()

            self.save_settings()

        return True

    @staticmethod
    def a___________________end______():
        pass


class LibraryTabBar(QTabBar):
    del_signal = pyqtSignal(int)
    move_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

        self.tab_first_movable_pos = None
        self.tab_last_movable_pos = None
        self.decal_l = None
        self.decal_w = None
        self.index_start = None

        font = self.font()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.setFont(font)

        self.setMouseTracking(True)

        self.setIconSize(QSize(20, 20))
        self.setDocumentMode(True)
        self.setMovable(True)

        self.setStyleSheet(
            "QTabBar::tab {min-height: 30px ; padding-left: 10px; margin-bottom:1px; "
            "border: 1px solid #8f8f91; border-top-left-radius: 5px; border-top-right-radius: 5px; "
            "background-color: #FFFFFF; }\n"

            "QTabBar::tab:selected{"
            "border-bottom-color: #FFFFFF;"
            "background-color: #FFFFFF; }\n"

            "QTabBar::tab:!selected {"
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7)}\n"

            "QTabBar::tab:hover:!selected {"
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #8FADCC); }\n"

            "QTabBar::tab:first {margin-left: 15px}\n"

            "QTabBar::tab:only-one {margin-left: 15px}"
        )

    def del_tab(self, button: QPushButton):

        if not isinstance(button, QPushButton):
            return

        tab_count = self.count()

        for tab_index in range(1, tab_count):

            current_button = self.tabButton(tab_index, QTabBar.RightSide)

            if not isinstance(current_button, QPushButton):
                continue

            if current_button == button:
                self.del_signal.emit(tab_index)
                return

    @staticmethod
    def a___________________event______():
        pass

    def tabSizeHint(self, current_index: int):
        size = super().tabSizeHint(current_index)

        if size.width() < 110:
            size = QSize(110, size.height())

        return size

    def tabInserted(self, current_index: int):
        super().tabInserted(current_index)

        close_button = QPushButton(self)
        close_button.setFlat(True)
        close_button.setMinimumHeight(24)

        if current_index != 0:
            close_button.setIcon(get_icon(windows_close_hover_icon))
            close_button.setStyleSheet("QPushButton:hover {border: 1px solid #8f8f91; border-radius:5px; }")

            close_button.clicked.connect(lambda: self.del_tab(close_button))

        else:
            close_button.setMaximumWidth(5)
            close_button.setEnabled(False)

        self.setTabButton(current_index, QTabBar.RightSide, close_button)

    def mousePressEvent(self, event: QMouseEvent):

        super().mousePressEvent(event)

        if event.button() != Qt.LeftButton:
            return

        nb_tab = self.count()

        if nb_tab <= 2:
            return

        tab_first_movable_rect = self.tabRect(0)

        if not isinstance(tab_first_movable_rect, QRect):
            return

        tab_last_movable_rect = self.tabRect(nb_tab - 1)

        if not isinstance(tab_last_movable_rect, QRect):
            return

        tab_current_index = self.tabAt(event.pos())

        if tab_current_index == 0:
            return

        tab_current_rect = self.tabRect(tab_current_index)

        if not isinstance(tab_current_rect, QRect):
            return

        self.tab_first_movable_pos = tab_first_movable_rect.x() + tab_first_movable_rect.width()
        self.tab_last_movable_pos = tab_last_movable_rect.x() + tab_last_movable_rect.width()
        self.decal_l = event.pos().x() - tab_current_rect.x()
        self.decal_w = tab_current_rect.x() + tab_current_rect.width() - event.pos().x()

        self.index_start = tab_current_index

    def mouseMoveEvent(self, event: QMouseEvent):

        if event.buttons() != Qt.LeftButton:
            super().mouseMoveEvent(event)
            return

        if (self.tab_first_movable_pos is None or self.tab_last_movable_pos is None or self.decal_l is None or
                self.decal_w is None):
            return

        self.setTabEnabled(0, False)

        tab_moved_start = event.pos().x() - self.decal_l
        tab_moved_end = event.pos().x() + self.decal_w

        if tab_moved_start <= self.tab_first_movable_pos:
            return

        if tab_moved_end >= self.tab_last_movable_pos:
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)

        self.setTabEnabled(0, True)

        if not isinstance(self.index_start, int):
            return

        self.tab_first_movable_pos = None
        self.tab_last_movable_pos = None
        self.decal_l = None
        self.decal_w = None

        current_index_tab = self.tabAt(event.pos())
        if not isinstance(current_index_tab, int):
            self.index_start = None
            return

        if current_index_tab == self.index_start:
            self.index_start = None
            return

        self.move_signal.emit(self.index_start, current_index_tab)

        self.index_start = None

    @staticmethod
    def a___________________end______():
        pass


class LibrarySynchro(QWidget):
    library_synchro_siganl = pyqtSignal(bool, list, list, list, bool)

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_LibrarySynchro()
        self.ui.setupUi(self)

        get_look_treeview(widget=self.ui.synchro_tree)

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        # ---------------------------------------
        # SETTINGS
        # ---------------------------------------

        library_synchro_setting = settings_read(library_synchro_setting_file)

        self.ismaximized_on = library_synchro_setting.get("ismaximized_on",
                                                          library_synchro_setting_datas.get("ismaximized_on", False))

        if not self.ismaximized_on:
            largeur = library_synchro_setting.get("width", 800)
            hauteur = library_synchro_setting.get("height", 600)

            self.resize(largeur, hauteur)

        # ---------------------------------------

        import_path = library_synchro_setting.get("path_import", library_synchro_setting_datas.get("path_import", ""))

        if not isinstance(import_path, str):
            self.import_path = library_synchro_setting_datas.get("path_import", "")
        else:
            self.import_path = import_path

        # ---------------------------------------

        export_path = library_synchro_setting.get("path_export", library_synchro_setting_datas.get("path_export", ""))

        if not isinstance(export_path, str):
            self.export_path = library_synchro_setting_datas.get("path_export", "")
        else:
            self.export_path = export_path

        # ---------------------------------------

        creation = library_synchro_setting.get("creation", library_synchro_setting_datas.get("creation", True))

        if not isinstance(creation, bool):
            creation = library_synchro_setting_datas.get("creation", True)

        if creation:
            self.ui.synchro_creation.setChecked(True)

        # ---------------------------------------
        # VARIABLES
        # ---------------------------------------

        self.allplan: AllplanDatas = asc.allplan

        self.attributes_dict = dict()

        self.attributes_select = dict()
        self.attributes_all = dict()

        # ---------------------------------------
        # Model
        # ---------------------------------------

        self.synchro_model = QStandardItemModel()

        # ---------------------------------------
        # Tree
        # ---------------------------------------

        self.ui.synchro_tree.setModel(self.synchro_model)

        self.ui.synchro_tree.clicked.connect(self.synchro_tree_clicked)
        self.ui.synchro_tree.selectionModel().selectionChanged.connect(self.synchro_buttons_manage)
        self.ui.synchro_tree.doubleClicked.connect(self.synchro_tree_doubleclicked)
        self.ui.synchro_tree.customContextMenuRequested.connect(self.synchro_tree_menu)

        # ---------------------------------------
        # Button signals
        # ---------------------------------------

        self.ui.synchro_all.clicked.connect(self.synchro_all_clicked)
        self.ui.synchro_select.clicked.connect(self.synchro_select_clicked)

        self.ui.bt_import.clicked.connect(self.synchro_import_clicked)
        self.ui.bt_export.clicked.connect(self.synchro_export_clicked)

        self.ui.synchro_launch.clicked.connect(self.synchro_action)
        self.ui.synchro_quit.clicked.connect(self.close)

    @staticmethod
    def a___________________init______():
        pass

    def show_synchro(self, attributes_select: dict, attributes_all: dict) -> None:

        self.synchro_model.clear()

        self.attributes_select = attributes_select
        self.attributes_all = attributes_all

        select_count = len(attributes_select)

        if select_count == 0:
            self.ui.synchro_select.setEnabled(False)
            self.ui.synchro_all.setChecked(True)
            self.synchro_load_datas(datas_current=self.attributes_all, initialisation=True)
        else:
            self.ui.synchro_select.setEnabled(True)
            self.ui.synchro_select.setChecked(True)
            self.synchro_load_datas(datas_current=self.attributes_select, initialisation=True)

        self.show()

    @staticmethod
    def a___________________buttons_______________():
        pass

    def synchro_buttons_manage(self):

        nb_items_selected = len(self.ui.synchro_tree.selectionModel().selectedRows())
        selection_active = nb_items_selected != 0

        self.ui.synchro_launch.setEnabled(selection_active)
        self.ui.bt_export.setEnabled(selection_active)

    @staticmethod
    def a___________________tree______():
        pass

    def synchro_tree_clicked(self, qm_current: QModelIndex):

        if not qm_check(qm_current):
            self.synchro_buttons_manage()
            return

        qm_parent = qm_current.parent()

        qm_root = self.synchro_model.invisibleRootItem().index()

        if qm_parent != qm_root:
            self.synchro_buttons_manage()
            return

        row_count = self.synchro_model.rowCount(qm_current)

        for row_index in range(row_count):

            qm = self.synchro_model.index(row_index, 0, qm_current)

            if not qm_check(qm):
                continue

            self.ui.synchro_tree.selectionModel().select(qm, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.synchro_buttons_manage()

    def synchro_tree_doubleclicked(self, qm_current: QModelIndex):

        if not qm_check(qm_current):
            self.synchro_buttons_manage()
            return

        qm_parent = qm_current.parent()

        qm_root = self.synchro_model.invisibleRootItem().index()

        if qm_parent == qm_root:
            self.synchro_buttons_manage()
            return

        current_text = qm_current.data()

        search_start = self.synchro_model.index(0, 0)

        search = self.synchro_model.match(search_start, Qt.DisplayRole, current_text, -1,
                                          Qt.MatchExactly | Qt.MatchRecursive)

        if len(search) == 0:
            self.synchro_buttons_manage()
            return

        for qm in search:

            if not qm_check(qm):
                continue

            if qm == qm_current:
                continue

            self.ui.synchro_tree.selectionModel().select(qm, QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def synchro_tree_menu(self, point: QPoint):

        synchro_menu = MyContextMenu()

        synchro_menu.add_title(title=self.tr("Favoris"))

        synchro_menu.add_action(qicon=get_icon(favorite_open_icon),
                                title=self.tr("Charger favoris"),
                                action=self.synchro_import_clicked,
                                tooltips=self.ui.bt_import.toolTip())

        synchro_menu.add_action(qicon=get_icon(favorite_save_icon),
                                title=self.tr("Enregistrer favoris"),
                                action=self.synchro_export_clicked,
                                tooltips=self.ui.bt_export.toolTip())

        synchro_menu.exec_(self.ui.synchro_tree.mapToGlobal(point))

    @staticmethod
    def a___________________options______():
        pass

    def synchro_all_clicked(self):
        self.synchro_load_datas(datas_current=self.attributes_all, initialisation=False)

    def synchro_select_clicked(self):
        self.synchro_load_datas(datas_current=self.attributes_select, initialisation=False)

    @staticmethod
    def a___________________load_datas______():
        pass

    def synchro_load_datas(self, datas_current: dict, initialisation=False):

        if initialisation:
            selections_dict = self.synchro_read_selections()

        else:

            if self.ui.synchro_select.isEnabled():
                selections_dict = self.synchro_save_selections()
            else:
                selections_dict = library_synchro_config_datas

        self.synchro_model.clear()

        # ---------------------------------------
        # Folder
        # ---------------------------------------

        folders_list = datas_current.get(folder_code, list())

        if len(folders_list) != 0:
            self.synchro_add_type(type_current=folder_code, list_current=folders_list)

        # ---------------------------------------
        # Material
        # ---------------------------------------

        materials_list = datas_current.get(material_code, list())

        if len(materials_list) != 0:
            self.synchro_add_type(type_current=material_code, list_current=materials_list)

        # ---------------------------------------
        # Component
        # ---------------------------------------

        components_list = datas_current.get(component_code, list())

        if len(components_list) != 0:
            self.synchro_add_type(type_current=component_code, list_current=components_list)

        # ---------------------------------------

        self.ui.synchro_tree.expandAll()

        if len(selections_dict) != 0:
            self.synchro_restore_selections(selections_dict=selections_dict)

        self.synchro_buttons_manage()

        self.setFocus()

    def synchro_add_type(self, type_current: str, list_current: list):

        if len(list_current) != 0:

            if type_current == folder_code:
                qs_master = QStandardItem(get_icon(folder_icon), self.tr("Dossier"))
            elif type_current == material_code:
                qs_master = QStandardItem(get_icon(material_icon), self.tr("Ouvrage"))
            elif type_current == component_code:
                qs_master = QStandardItem(get_icon(component_icon), self.tr("Composant"))

            else:
                return

            qs_master.setData(type_current, user_data_type)
            qs_master.setSelectable(False)

            for number_str in list_current:

                if number_str in self.attributes_dict:

                    name = self.attributes_dict[number_str]

                else:

                    attribute_obj = self.allplan.attributes_dict.get(number_str)

                    if not isinstance(attribute_obj, AttributeDatas):
                        print("library -- LibrarySynchro -- synchro_add_type -- "
                              "not isinstance(attribute_obj, AttributeDatas)")
                        continue

                    name = attribute_obj.name

                    self.attributes_dict[number_str] = name

                if name == "":
                    continue

                title = f"{number_str} - {name}"

                qs = QStandardItem(get_icon(attribute_icon), title)
                qs.setData(type_current, user_data_type)
                qs.setData(number_str, user_data_number)

                qs_master.appendRow(qs)

            self.synchro_model.appendRow([qs_master])

    @staticmethod
    def a___________________selection______():
        pass

    def synchro_read_selections(self) -> dict:

        synchro_setting = settings_read(library_synchro_config_file)

        if not self.synchro_check_selection(synchro_setting):
            return library_synchro_config_datas

        return synchro_setting

    @staticmethod
    def synchro_check_selection(selections_dict: dict) -> bool:

        if not isinstance(selections_dict, dict):
            return False

        if ("folders_list" not in selections_dict or "materials_list" not in selections_dict or
                "components_list" not in selections_dict):
            return False

        folders_list = selections_dict.get("folders_list", list())

        if not isinstance(folders_list, list):
            return False

        materials_list = selections_dict.get("materials_list", list())

        if not isinstance(materials_list, list):
            return False

        components_list = selections_dict.get("components_list", list())

        if not isinstance(components_list, list):
            return False

        return True

    def synchro_save_selections(self) -> dict:

        folders_list = list()
        materials_list = list()
        components_list = list()

        selection_datas = {"folders_list": folders_list,
                           "materials_list": materials_list,
                           "components_list": components_list}

        selection_list = self.ui.synchro_tree.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return selection_datas

        for qm in selection_list:

            if not qm_check(qm):
                continue

            item_type = qm.data(user_data_type)
            number = qm.data(user_data_number)

            if not isinstance(number, str):
                continue

            if item_type == folder_code and number not in folders_list:
                folders_list.append(number)
                continue

            if item_type == material_code and number not in materials_list:
                materials_list.append(number)
                continue

            if item_type == component_code and number not in components_list:
                components_list.append(number)
                continue

        return selection_datas

    def synchro_restore_selections(self, selections_dict: dict):

        folders_list = selections_dict.get("folders_list", list())
        materials_list = selections_dict.get("materials_list", list())
        components_list = selections_dict.get("components_list", list())

        row_count = self.synchro_model.rowCount()

        for row_index in range(row_count):

            qm_master = self.synchro_model.index(row_index, 0)

            if not qm_check(qm_master):
                continue

            row_count_child = self.synchro_model.rowCount(qm_master)

            if row_count_child == 0:
                continue

            for row_index_child in range(row_count_child):

                qm_child = self.synchro_model.index(row_index_child, 0, qm_master)

                if not qm_check(qm_child):
                    continue

                item_type = qm_child.data(user_data_type)
                number = qm_child.data(user_data_number)

                if not isinstance(number, str):
                    continue

                if item_type == folder_code and number in folders_list:
                    self.ui.synchro_tree.selectionModel().select(qm_child,
                                                                 QItemSelectionModel.Select | QItemSelectionModel.Rows)
                    continue

                if item_type == material_code and number in materials_list:
                    self.ui.synchro_tree.selectionModel().select(qm_child,
                                                                 QItemSelectionModel.Select | QItemSelectionModel.Rows)
                    continue

                if item_type == component_code and number in components_list:
                    self.ui.synchro_tree.selectionModel().select(qm_child,
                                                                 QItemSelectionModel.Select | QItemSelectionModel.Rows)
                    continue

    @staticmethod
    def a___________________import_export______():
        pass

    def synchro_import_clicked(self):

        a = self.tr("Fichier")

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [asc_export_path,
                              self.allplan.allplan_paths.std_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.usr_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[library_synchro_setting_file, "path_import"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{a} INI": [".ini"]},
                                 current_path=self.import_path,
                                 default_path=asc_export_path,
                                 use_setting_first=False,
                                 use_save=False)

        if file_path == "":
            return

        try:

            with open(file_path, 'r', encoding="Utf-8") as file:

                selections_dict: dict = json.load(file)

        except Exception as erreur:
            print(f"library -- LibrarySynchro -- synchro_import_clicked -- {erreur}")
            return

        if not self.synchro_check_selection(selections_dict=selections_dict):
            return

        self.ui.synchro_tree.clearSelection()

        self.synchro_restore_selections(selections_dict=selections_dict)

    def synchro_export_clicked(self):

        selection_list = self.ui.synchro_tree.selectionModel().selectedRows()

        if len(selection_list) == 0:
            msg(titre=application_title,
                message=self.tr("Aucun élément à exporter."),
                icone_avertissement=True)
            return

        b = self.tr("Fichier")

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [asc_export_path,
                              self.allplan.allplan_paths.std_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.usr_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[library_synchro_setting_file, "path_export"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{b} INI": [".ini"]},
                                 current_path=self.export_path,
                                 default_path=asc_export_path,
                                 use_setting_first=False,
                                 use_save=True)
        if file_path == "":
            return

        selections_dict = self.synchro_save_selections()

        try:

            with open(file_path, 'w', encoding="Utf-8") as file:
                json.dump(selections_dict, file, ensure_ascii=False, indent=2)

        except Exception as error:
            msg(titre=application_title,
                message=self.tr("Une erreur est survenue."),
                details=error,
                icone_critique=True)
            return

    @staticmethod
    def a___________________save______():
        pass

    def synchro_action(self):

        selection_list = self.ui.synchro_tree.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return

        folders_list = list()
        materials_list = list()
        components_list = list()

        for qm in selection_list:

            if not qm_check(qm):
                print("library -- Library_update -- update_action -- not qm_check(qm)")
                continue

            ele_type = qm.data(user_data_type)

            if ele_type == folder_code:
                list_current = folders_list
            elif ele_type == material_code:
                list_current = materials_list
            elif ele_type == component_code:
                list_current = components_list
            else:
                print("library -- Library_update -- update_action -- ele_type not found")
                continue

            number = qm.data(user_data_number)

            if not isinstance(number, str):
                print("library -- Library_update -- update_action -- not isinstance(number, str)")
                continue

            if number in list_current:
                print("library -- Library_update -- update_action -- number in list_current")
                continue

            if number in attribute_val_default_layer:
                list_current.extend(list(attribute_val_default_layer.keys()))
                continue

            if number in attribute_val_default_fill:
                list_current.extend(list(attribute_val_default_fill.keys()))
                continue

            if number in attribute_val_default_room:
                list_current.extend(list(attribute_val_default_room.keys()))
                continue

            list_current.append(number)

        if len(folders_list) + len(materials_list) + len(components_list) == 0:
            return

        selection = self.ui.synchro_select.isChecked()
        creation = self.ui.synchro_creation.isChecked()

        self.close()

        self.library_synchro_siganl.emit(selection, folders_list, materials_list, components_list, creation)

    @staticmethod
    def a___________________settings______():
        pass

    def synchro_save_config(self):

        selections_list = self.synchro_save_selections()

        if len(selections_list) == 0:
            return

        settings_save(library_synchro_config_file, selections_list)

    def synchro_save_setting(self):

        datas_config = settings_read(file_name=library_synchro_setting_file)

        if not isinstance(datas_config, dict):
            return

        datas_config["path_import"] = self.import_path
        datas_config["path_export"] = self.export_path
        datas_config["creation"] = self.ui.synchro_creation.isChecked()

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True

                settings_save(file_name=library_synchro_setting_file, config_datas=datas_config)
                return

        datas_config["height"] = self.size().height()
        datas_config["width"] = self.size().width()
        datas_config["ismaximized_on"] = False

        settings_save(file_name=library_synchro_setting_file, config_datas=datas_config)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.synchro_action()

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):

        self.synchro_save_config()
        self.synchro_save_setting()

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass
