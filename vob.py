#!/usr/bin/python3
# -*- coding: utf-8 -*
import glob
import os.path
import re
import shutil
from datetime import datetime

from PyQt5.Qt import *

from allplan_manage import AllplanDatas, AllplanPaths, AttributeDatas
from formula_manage import WidgetAutocompletion
from main_datas import application_title, vob_setting_file, vob_setting_datas, language_icons, get_icon, refresh_icon, \
    language_extension_3
from main_datas import browser_icon, paste_icon, valid_icon, error_icon, liste_caracteres_fin
from main_datas import open_text_editor_icon
from main_datas import user_formule_ok, open_icon, save_icon, save_as_icon, add_icon, delete_icon, copy_icon
from tools import MyContextMenu, find_global_point, selectionner_parentheses
from tools import ValidatorModel, settings_read, settings_save, make_backup, find_folder_path, find_filename
from tools import open_folder, open_file, copy_to_clipboard
from tools import read_file_to_list, get_look_tableview, get_look_combobox, qm_check, afficher_message, browser_file
from ui_vob import Ui_VOB

col_vob_trade = 0
col_vob_object = 1
col_vob_unit = 2
col_vob_method = 3
col_vob_formula = 4
col_vob_comment = 5

col_vob_count = 6


class VobFileData(QObject):

    def __init__(self, file_path: str, verif_strict=True):
        super().__init__()

        self.file_path = file_path

        self.is_valid = False

        self.verif_strict = verif_strict

        # --------

        self.folder_path = ""
        self.file_name = ""
        self.language = ""
        self.extension = ""

        # --------- Title ---------

        self.title = ""

        self.file_name_ext = ""

        # --------- Country ---------

        self.country = ""

        # --------- Menu ---------

        self.icon = QIcon()
        self.tooltips = ""
        self.last_changed = ""

        # --------- Creation ---------

        self.create_object()

        # -------------

    def create_object(self):

        # --------- exist ---------

        if not isinstance(self.file_path, str):
            print("vob -- VobFileData -- not isinstance(file_path, str)")
            return

        if not os.path.exists(self.file_path):
            print("vob -- VobFileData -- not os.path.exists(file_path)")
            return

        # --------- Folder_path ---------

        self.folder_path = find_folder_path(file_path=self.file_path)

        # --------- file_name is valid ---------

        self.file_name = find_filename(file_path=self.file_path)

        if self.verif_strict:

            if len(self.file_name) != 7:
                print("vob -- VobFileData -- len(file_name) != 7")
                return

            file_name_valid = bool(re.match(r"^vo[b2]_[a-zA-Z]{3}$", self.file_name))

            if not file_name_valid:
                print("vob -- VobFileData -- not file_name_valid")
                return

        # --------- Language ---------

        self.language = self.file_path[-3:]  # current language

        if self.language.lower() not in language_icons:
            print("vob -- VobFileData -- self.language.lower() not in language_icons")
            return

        self.extension = self.language

        # --------- Title ---------

        self.title = f"{self.file_name}.{self.language}"

        self.file_name_ext = self.title

        # --------- Country ---------

        self.country = self.file_name[-3:]

        if self.country.lower() not in language_icons:

            if self.verif_strict:
                print("vob -- VobFileData -- self.country.lower() not in language_icons")
                return

            self.country = ""

        # --------- Icon ---------

        if self.country != "":
            icon_code = language_icons.get(self.country)

            self.icon = get_icon(icon_path=f":/Images/{icon_code}.png")

        # --------- Tootips ---------

        country_txt = self.tr("Pays")
        langue_txt = self.tr("Langue")

        if self.country == "":
            self.tooltips = (f"<p style='white-space:pre'>{self.file_path}<br>"
                             f"<b>{country_txt} = {self.country} // {langue_txt} = {self.language}")
        else:
            self.tooltips = f"<p style='white-space:pre'>{self.file_path}"

        # --------- Datas ---------

        seconds = os.path.getmtime(self.file_path)
        date_complet_modif = datetime.fromtimestamp(seconds)

        self.last_changed = date_complet_modif.strftime("%d-%m-%Y - %H:%M:%S")

        # --------- Datas ---------

        datas = read_file_to_list(file_path=self.file_path)

        if len(datas) == 0:
            return

        first_line = datas[0]

        if not isinstance(first_line, str):
            print("vob -- VobFileData -- not isinstance(first_line, str)")
            return

        first_line = first_line.strip()

        if first_line.startswith("//") or first_line.startswith("#"):
            self.is_valid = True

    def refresh_last_change(self):
        self.last_changed = datetime.now().strftime("%d-%m-%Y - %H:%M:%S")


class VobWidget(QWidget):

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # Interface
        # ---------------------------------------

        self.ui = Ui_VOB()
        self.ui.setupUi(self)

        # ---------------------------------------
        # Variables
        # ---------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.allplan: AllplanDatas = self.asc.allplan

        self.vob_file_obj = None
        self.change_made = False

        self.defaut_text = self.tr("Défaut")

        self.row_current = -1
        self.qm_current = None

        # -----

        self.trade_dict = {"  -1": self.defaut_text}
        self.trade_list = [self.defaut_text]
        self.vob_trade_model = QStandardItemModel()

        self.object_dict = {"   -1": self.defaut_text}
        self.object_list = [self.defaut_text]
        self.vob_object_model = QStandardItemModel()

        self.unit_dict = {"-1": self.defaut_text, "00": "m3", "01": "m2", "02": "m", "05": "geo"}
        self.unit_list = [f"{number} = {value}" for number, value in self.unit_dict.items()]
        self.vob_unit_model = QStandardItemModel()

        self.method_dict = {"-1": self.defaut_text}
        self.method_list = [self.defaut_text]
        self.vob_method_model = QStandardItemModel()

        # ---------------------------------------

        self.vob_model = QStandardItemModel()

        self.header_title = [self.tr("Métier"), self.tr("Objet"), self.tr("Unité"), self.tr("Méthode de calcul"),
                             self.tr("Formule"), self.tr("Commentaire")]

        self.vob_filter = QSortFilterProxyModel()
        self.vob_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.vob_filter.setSortLocaleAware(True)
        self.vob_filter.setSourceModel(self.vob_model)

        self.ui.vob_table.setModel(self.vob_filter)

        # ---------------------------------------
        # Settings
        # ---------------------------------------

        vob_setting = settings_read(vob_setting_file)

        self.ismaximized_on = vob_setting.get("ismaximized_on", vob_setting_datas.get("ismaximized_on", False))

        if not self.ismaximized_on:
            width = vob_setting.get("width", vob_setting_datas.get("width", 800))
            height = vob_setting.get("height", vob_setting_datas.get("height", 600))

            self.resize(width, height)

        # ---------------

        self.splitter_ratio = vob_setting.get("splitter", vob_setting_datas.get("splitter", 75))

        if not isinstance(self.splitter_ratio, int):
            self.splitter_ratio = 75
        elif self.splitter_ratio > 80:
            self.splitter_ratio = 80
        elif self.splitter_ratio < 30:
            self.splitter_ratio = 30

        # ---------------

        vob_save_folder = vob_setting.get("save", vob_setting_datas.get("save", ""))

        if not isinstance(vob_save_folder, str):
            vob_save_folder = ""
        elif not os.path.exists(vob_save_folder):
            vob_save_folder = ""

        self.vob_save_folder = vob_save_folder

        # ---------------

        header = self.ui.vob_table.horizontalHeader()

        if header is not None:

            order = vob_setting.get(f"order", vob_setting_datas.get("order", 0))

            if order not in [0, 1]:
                order = 0

            # -------

            order_col = vob_setting.get(f"order_col", vob_setting_datas.get("order_col", 0))

            if not isinstance(order_col, int):
                order_col = 0
            elif order_col > col_vob_comment:
                order_col = 0
            elif order_col < 0:
                order_col = 0

            header.setSortIndicator(order_col, order)
            self.ui.vob_table.sortByColumn(order_col, order)

            header.sortIndicatorChanged.connect(self.vob_sort_indicator_changed)

        # ---------------------------------------

        filter_index = vob_setting.get('filter', vob_setting_datas.get("filter", 0))

        if not isinstance(filter_index, int):
            filter_index = 0
        elif filter_index > col_vob_comment:
            filter_index = 0
        elif filter_index < 0:
            filter_index = 0

        self.ui.search_filter_combo.setCurrentIndex(filter_index)

        # ---------------------------------------

        self.clipboard_trade = ""
        self.clipboard_object = ""
        self.clipboard_unit = ""
        self.clipboard_method = ""
        self.clipboard_formula = ""
        self.clipboard_comment = ""

        # ---------------------------------------

        self.ui.open_file_bt.clicked.connect(self.vob_open_file_clicked)
        self.ui.save_file_bt.clicked.connect(self.vob_save_file_clicked)
        self.ui.save_as_file_bt.clicked.connect(self.vob_save_as_file_clicked)

        # ---------------------------------------

        self.ui.add_bt.clicked.connect(self.vob_add)
        self.ui.delete_bt.clicked.connect(self.vob_delete)
        self.ui.copy_bt.clicked.connect(self.vob_copy)
        self.ui.paste_bt.clicked.connect(self.vob_paste)

        # ---------------------------------------

        self.ui.tools_reset_bt.clicked.connect(self.vob_restore_original)
        self.ui.tools_bt.clicked.connect(self.vob_tools_clicked)

        # ---------------------------------------

        get_look_combobox(widget=self.ui.search_filter_combo)

        self.ui.search_filter_combo.currentIndexChanged.connect(self.vob_search_filter_changed)
        self.ui.search.textChanged.connect(self.vob_search_changed)
        self.ui.search_clear.clicked.connect(self.vob_search_clear)

        self.ui.search_formula.clicked.connect(self.vob_search_formula_clicked)

        # ---------------------------------------

        get_look_tableview(widget=self.ui.vob_table)

        self.ui.vob_table.selectionModel().selectionChanged.connect(self.vob_table_selection_changed)
        self.ui.vob_table.customContextMenuRequested.connect(self.vob_table_menu_show)

        # ---------------------------------------
        # Trade
        # ---------------------------------------

        get_look_combobox(self.ui.trade_combo)

        # -----

        self.vob_trade_filter = QSortFilterProxyModel()
        self.vob_trade_filter.setSortLocaleAware(True)
        self.vob_trade_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.vob_trade_filter.setSourceModel(self.vob_trade_model)

        # -----

        self.ui.trade_combo.setModel(self.vob_trade_model)

        # -----

        self.vob_trade_completer = QCompleter()
        self.vob_trade_completer.setModel(self.vob_trade_filter)
        self.vob_trade_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.vob_trade_completer.setCaseSensitivity(Qt.CaseInsensitive)

        # -----

        self.ui.trade_combo.setCompleter(self.vob_trade_completer)
        self.ui.trade_combo.lineEdit().textEdited.connect(self.vob_trade_filter.setFilterFixedString)

        self.ui.trade_combo.currentIndexChanged.connect(self.vob_trade_changed)
        self.ui.trade_combo.setValidator(ValidatorModel(model=self.ui.trade_combo.model(), column_index=0))
        self.ui.trade_combo.installEventFilter(self)

        # ---------------------------------------
        # object
        # ---------------------------------------

        get_look_combobox(self.ui.object_combo)

        # -----

        self.vob_object_filter = QSortFilterProxyModel()
        self.vob_object_filter.setSortLocaleAware(True)
        self.vob_object_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.vob_object_filter.setSourceModel(self.vob_object_model)

        # -----

        self.ui.object_combo.setModel(self.vob_object_model)

        # -----

        self.vob_object_completer = QCompleter()
        self.vob_object_completer.setModel(self.vob_object_filter)
        self.vob_object_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.vob_object_completer.setCaseSensitivity(Qt.CaseInsensitive)

        # -----

        self.ui.object_combo.setCompleter(self.vob_object_completer)
        self.ui.object_combo.lineEdit().textEdited.connect(self.vob_object_filter.setFilterFixedString)

        self.ui.object_combo.currentIndexChanged.connect(self.vob_object_changed)
        self.ui.object_combo.setValidator(ValidatorModel(model=self.ui.object_combo.model(), column_index=0))
        self.ui.object_combo.installEventFilter(self)

        # ---------------------------------------
        # unit
        # ---------------------------------------

        get_look_combobox(self.ui.unit_combo)

        # -----

        self.vob_unit_filter = QSortFilterProxyModel()
        self.vob_unit_filter.setSortLocaleAware(True)
        self.vob_unit_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.vob_unit_filter.setSourceModel(self.vob_unit_model)

        # -----

        self.ui.unit_combo.setModel(self.vob_unit_model)

        # -----

        self.vob_unit_completer = QCompleter()
        self.vob_unit_completer.setModel(self.vob_unit_filter)
        self.vob_unit_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.vob_unit_completer.setCaseSensitivity(Qt.CaseInsensitive)

        # -----

        self.ui.unit_combo.setCompleter(self.vob_unit_completer)
        self.ui.unit_combo.lineEdit().textEdited.connect(self.vob_unit_filter.setFilterFixedString)

        self.ui.unit_combo.currentIndexChanged.connect(self.vob_unit_changed)
        self.ui.unit_combo.setValidator(ValidatorModel(model=self.ui.unit_combo.model(), column_index=0))
        self.ui.unit_combo.installEventFilter(self)

        # ---------------------------------------
        # method
        # ---------------------------------------

        get_look_combobox(self.ui.method_combo)

        # -----

        self.vob_method_filter = QSortFilterProxyModel()
        self.vob_method_filter.setSortLocaleAware(True)
        self.vob_method_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.vob_method_filter.setSourceModel(self.vob_method_model)

        # -----

        self.ui.method_combo.setModel(self.vob_method_model)

        # -----

        self.vob_method_completer = QCompleter()
        self.vob_method_completer.setModel(self.vob_method_filter)
        self.vob_method_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.vob_method_completer.setCaseSensitivity(Qt.CaseInsensitive)

        # -----

        self.ui.method_combo.setCompleter(self.vob_method_completer)
        self.ui.method_combo.lineEdit().textEdited.connect(self.vob_method_filter.setFilterFixedString)

        self.ui.method_combo.currentIndexChanged.connect(self.vob_method_changed)
        self.ui.method_combo.setValidator(ValidatorModel(model=self.ui.method_combo.model(), column_index=0))
        self.ui.method_combo.installEventFilter(self)

        # ---------------------------------------
        # CREATEUR DE FORMULES
        # ---------------------------------------

        self.widget_creation_formule = self.asc.formula_editor_widget

        self.ui.formula_editor_bt.clicked.connect(self.vob_formula_editor_show)
        self.widget_creation_formule.modif_formule.connect(self.vob_formula_editor_changed)
        self.widget_creation_formule.close_event.connect(self.vob_formula_editor_closed)

        self.widget_formule_visible = False

        # ---------------------------------------
        # Formula
        # ---------------------------------------

        self.ui.value_attrib.chargement(self.allplan)

        self.autocompletion = WidgetAutocompletion(allplan=self.allplan, widget=self)

        self.ui.value_attrib.textChanged.connect(self.vob_formula_changed)
        self.ui.value_attrib.selectionChanged.connect(self.vob_formula_selection_changed)

        self.ui.formula_verification_bt.clicked.connect(self.vob_formula_clicked)

        # -----

        self.ui.value_attrib.editingFinished.connect(self.vob_formula_finished)
        self.ui.value_attrib.installEventFilter(self)

        # ---------------------------------------
        # Comment
        # ---------------------------------------

        self.ui.comment_clear_bt.clicked.connect(self.vob_comment_clear_clicked)

        # -----

        self.ui.comment_line.editingFinished.connect(self.vob_comment_changed)
        self.ui.comment_line.installEventFilter(self)

        # ---------------------------------------

        self.ui.delete_all_bt.clicked.connect(self.vob_delete_all_clicked)

        # ---------------------------------------

        self.ui.save_bt.clicked.connect(self.vob_save_file_clicked)
        self.ui.save_bt.clicked.connect(self.close)

        self.ui.quit_bt.clicked.connect(self.close)

        # ---------------------------------------

    @staticmethod
    def a___________________vob_show______():
        pass

    def vob_show(self, file_path: str):

        self.vob_translate_datas()

        self.vob_file_obj = VobFileData(file_path=file_path)

        # ---------------------------------------

        if self.vob_file_obj.is_valid:

            self.vob_table_load()
            self.vob_table_select(self.vob_filter.index(0, col_vob_trade))

        else:

            if not self.vob_browse_clicked():
                return

                # ---------------------------------------

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

        splitter_sizes = self.ui.splitter.sizes()

        if not isinstance(splitter_sizes, list):
            print("vob -- VobWidget -- vob_show -- not isinstance(splitter_sizes, list)")
            return

        if len(splitter_sizes) != 2:
            print("vob -- VobWidget -- vob_show -- len(splitter_sizes) != 2")
            return

        splitter_x1, splitter_x2 = splitter_sizes

        splitter_size = splitter_x1 + splitter_x2

        try:
            splitter_x1 = round(splitter_size * self.splitter_ratio / 100)
            splitter_x2 = splitter_size - splitter_x1

            self.ui.splitter.setSizes([splitter_x1, splitter_x2])

        except Exception as error:
            print(f"vob -- VobWidget -- vob_show -- error: {error}")
            return

    def vob_open_file_clicked(self) -> bool:

        vob_files_list = self.vob_get_files()

        if len(vob_files_list) == 0:
            self.vob_browse_clicked()
            return

        vob_menu = MyContextMenu(tooltips_visible=True)

        vob_menu.add_action(qicon=get_icon(browser_icon),
                            title=self.tr("Parcourir"),
                            action=self.vob_browse_clicked)

        vob_menu.addSeparator()

        for vob_file_obj in vob_files_list:

            if not isinstance(vob_file_obj, VobFileData):
                continue

            vob_menu.add_action(qicon=vob_file_obj.icon,
                                title=vob_file_obj.title,
                                tooltips=vob_file_obj.tooltips,
                                action=lambda val=vob_file_obj: self.vob_open_file(vob_file_obj=val))

        vob_menu.exec_(find_global_point(self.ui.open_file_bt))

    def vob_browse_clicked(self) -> bool:

        current_folder = self.allplan.allplan_paths.etc_path
        file_ext = language_icons.get(self.allplan.langue, "eng")
        filename = f"vob_{file_ext}.{file_ext}"

        # --------

        a = self.tr("Fichier")

        extention_valid = [f".{extension}" for extension in language_extension_3.values()]

        # --------

        if isinstance(self.vob_file_obj, VobFileData):
            if self.vob_file_obj.is_valid:
                filename = self.vob_file_obj.file_name_ext
                file_ext = self.vob_file_obj.extension
                current_folder = self.vob_file_obj.folder_path

        # --------

        datas_filters = {f"{a} VOB": extention_valid,
                         f"{a} VOB {file_ext.upper()}": [f".{file_ext}"]}

        for ext in language_extension_3.values():

            title = f"{a} VOB {ext.upper()}"

            if title in datas_filters:
                continue

            datas_filters[title] = [f".{ext}"]

        # --------

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [self.allplan.allplan_paths.etc_path, current_folder, self.vob_save_folder]

        else:

            shortcuts_list = [current_folder, self.vob_save_folder]

        # --------

        file_path = browser_file(parent=self,
                                 title=self.tr("Ouvrir le fichier"),
                                 registry=[],
                                 datas_filters=datas_filters,
                                 shortcuts_list=shortcuts_list,
                                 current_path=current_folder,
                                 file_name=filename)

        if file_path == "":
            return False

        # --------------

        vob_file_obj = VobFileData(file_path=file_path, verif_strict=False)

        if not vob_file_obj.is_valid:
            afficher_message(titre=application_title,
                             message=self.tr("Ce format de fichier n'est pas pris en charge."))
            return False

        return self.vob_open_file(vob_file_obj=vob_file_obj)

    def vob_open_file(self, vob_file_obj: VobFileData) -> bool:

        # --------------

        self.vob_save_ask()

        # --------------
        self.vob_file_obj = vob_file_obj
        return self.vob_table_load()

    def vob_translate_datas(self):

        self.header_title = [self.tr("Métier"), self.tr("Objet"), self.tr("Unité"), self.tr("Méthode de calcul"),
                             self.tr("Formule"), self.tr("Commentaire")]

        self.vob_model.setHorizontalHeaderLabels(self.header_title)

        # ---------------------------------------
        # Trade
        # ---------------------------------------

        attribute_obj = self.allplan.attributes_dict.get("209")

        if not isinstance(attribute_obj, AttributeDatas):
            print("vob -- VobWidget -- vob_translate_datas -- not isinstance(attribute_obj, AttributeDatas) 4")
            return

        if isinstance(attribute_obj.enumeration, QStandardItemModel):

            self.trade_dict = {"  -1": self.defaut_text}

            for index_item in range(attribute_obj.enumeration.rowCount()):

                qs_index = attribute_obj.enumeration.index(index_item, 0)
                qs_trade = attribute_obj.enumeration.index(index_item, 1)

                number = qs_index.data()
                code = qs_trade.data()

                if code == "":
                    continue

                try:
                    number_int = int(number)
                except Exception:
                    print("vob -- VobWidget --  vob_translate_datas -- bad number")
                    continue

                number = f"{number_int}".zfill(3)

                self.trade_dict[number] = code

            self.trade_list = [f"{number} = {value}" for number, value in self.trade_dict.items()]
            self.trade_list.sort()

            self.ui.trade_combo.blockSignals(True)

            self.vob_trade_model.clear()

            for text in self.trade_list:
                self.vob_trade_model.appendRow([QStandardItem(text)])

            self.ui.trade_combo.blockSignals(False)

        else:

            print("vob -- VobWidget -- vob_translate_datas -- not isinstance(trade_model, QStandardItemModel)")

        # ---------------------------------------
        # Objects
        # ---------------------------------------

        objects_list = self.allplan.get_object_datas()

        if len(objects_list) != 0:

            self.object_dict = {"   -1": self.defaut_text}

            for code, number_int in objects_list:
                number = f"{number_int}".zfill(4)
                self.object_dict[number] = code

            self.object_list = [f"{number} = {value}" for number, value in self.object_dict.items()]
            self.object_list.sort()

            self.ui.object_combo.blockSignals(True)

            self.vob_object_model.clear()

            for text in self.object_list:
                self.vob_object_model.appendRow([QStandardItem(text)])

            self.ui.object_combo.blockSignals(False)

        else:

            print("vob -- VobWidget -- vob_translate_datas -- len(objects_list) == 0")

        # ---------------------------------------
        # units
        # ---------------------------------------

        self.ui.unit_combo.blockSignals(True)

        self.vob_unit_model.clear()

        for text in self.unit_list:
            self.vob_unit_model.appendRow([QStandardItem(text)])

        self.ui.unit_combo.blockSignals(False)

        # ---------------------------------------
        # Methode
        # ---------------------------------------

        self.method_dict = {"-1": self.defaut_text,
                            "01": self.tr("Volume"),
                            "02": self.tr("Surface"),
                            "03": self.tr("Sol"),
                            "04": self.tr("Plafond"),
                            "05": self.tr("Surface latérale"),
                            "06": self.tr("Surface médiane"),
                            "13": "?"}

        self.method_list = [f"{number} = {value}" for number, value in self.method_dict.items()]

        self.ui.method_combo.blockSignals(True)

        self.vob_method_model.clear()

        for text in self.method_list:
            self.vob_method_model.appendRow([QStandardItem(text)])

        self.ui.method_combo.blockSignals(False)

    def vob_sort_indicator_changed(self):

        self.ui.vob_table.setFocus()

        qm_filter_list = self.ui.vob_table.selectionModel().selectedRows()

        if len(qm_filter_list) != 1:
            print(f"vob -- VobWidget -- vob_sort_indicator_changed -- len(qm_filter_list) != 1")
            return

        qm_filter = qm_filter_list[0]

        if not qm_check(qm_filter):
            print(f"vob -- VobWidget -- vob_sort_indicator_changed -- {qm_filter.row()}")
            return

        self.row_current = qm_filter.row()

        self.ui.vob_table.scrollTo(qm_filter, QAbstractItemView.PositionAtCenter)

    def vob_load_window_title(self):

        self.setWindowTitle(f"{application_title} -- VOB Manager -- {self.vob_file_obj.file_path} -- "
                            f"{self.vob_file_obj.last_changed}")

    @staticmethod
    def a___________________buttons______():
        pass

    def vob_buttons_manage(self):

        file_loaded = isinstance(self.vob_file_obj, VobFileData)

        self.ui.save_file_bt.setEnabled(file_loaded)
        self.ui.save_as_file_bt.setEnabled(file_loaded)

        self.ui.tools_reset_bt.setEnabled(file_loaded)
        self.ui.tools_bt.setEnabled(file_loaded)

        # ---------

        self.ui.save_bt.setEnabled(file_loaded)

        # ---------

        if not file_loaded:

            self.ui.add_bt.setEnabled(False)

            self.ui.delete_bt.setEnabled(False)
            self.ui.copy_bt.setEnabled(False)
            self.ui.paste_bt.setEnabled(False)

            # ---------

            self.ui.search.setEnabled(False)
            self.ui.search_filter_combo.setEnabled(False)
            self.ui.search_clear.setEnabled(False)
            self.ui.search_formula.setEnabled(False)

            # ---------

            self.vob_buttons_info_manage(enable=False)

            # ---------

            self.ui.delete_all_bt.setEnabled(False)

        else:

            selection_on = len(self.ui.vob_table.selectionModel().selectedRows()) != 0

            search_text_on = self.ui.search.text() != ""
            search_formula_on = self.ui.formula_verification_bt.isChecked()
            search_on = search_text_on or search_formula_on

            # ---------

            self.ui.add_bt.setEnabled(not search_on)
            self.ui.delete_bt.setEnabled(selection_on)
            self.ui.copy_bt.setEnabled(selection_on)
            self.ui.paste_bt.setEnabled(self.clipboard_trade != "" and not search_on)

            # ---------

            self.ui.search_filter_combo.setEnabled(not search_formula_on)
            self.ui.search.setEnabled(not search_formula_on)
            self.ui.search_clear.setEnabled(not search_formula_on)

            self.ui.search_formula.setEnabled(not search_text_on)

            # ---------

            self.vob_buttons_info_manage(enable=selection_on)

            # ---------

            self.ui.delete_all_bt.setEnabled(self.vob_model.rowCount() != 0)

    def vob_buttons_info_manage(self, enable: bool):

        if not isinstance(self.vob_file_obj, VobFileData):
            enable = False

        self.ui.trade_combo.setEnabled(enable)
        self.ui.object_combo.setEnabled(enable)
        self.ui.unit_combo.setEnabled(enable)
        self.ui.method_combo.setEnabled(enable)

        # ---------

        self.ui.value_attrib.setEnabled(enable)
        self.ui.formula_editor_bt.setEnabled(enable)
        self.ui.formula_verification_bt.setEnabled(enable)

        # ---------

        self.ui.comment_line.setEnabled(enable)
        self.ui.comment_clear_bt.setEnabled(enable)

    @staticmethod
    def a___________________edition______():
        pass

    def vob_add(self):

        self.vob_search_clear()

        # ----------

        self.vob_table_add_line(vob_trade=self.trade_list[0],
                                vob_object=self.object_list[0],
                                vob_unit=self.unit_list[0],
                                vob_method=self.method_list[0],
                                vob_formula="",
                                vob_comment="",
                                select=True)

    def vob_delete(self) -> bool:

        qs_select_list = self.ui.vob_table.selectionModel().selectedRows()

        if len(qs_select_list) != 1:
            print("vob -- VobWidget -- vob_delete -- len(qs_select_list) != 1")
            return False

        qm_current = qs_select_list[0]

        if not qm_check(qm_current):
            print("vob -- VobWidget -- vob_delete -- not qm_check(qm_current)")
            return False

        qm_model = self.vob_filter.mapToSource(qm_current)

        if not qm_check(qm_model):
            print("vob -- VobWidget -- vob_delete -- not qm_check(qm_model)")
            return False

        row_filter = qm_current.row()
        row_model = qm_model.row()

        qs_list = self.vob_model.takeRow(row_model)

        self.change_made = True

        # ----------

        if row_filter > self.vob_filter.rowCount() - 1:
            row_filter = self.vob_filter.rowCount() - 1

        qm_filter = self.vob_filter.index(row_filter, col_vob_trade)

        if qm_check(qm_filter):
            self.vob_table_select(qm=qm_filter)
            self.ui.vob_table.scrollTo(qm_filter, QAbstractItemView.PositionAtCenter)

        return len(qs_list) == col_vob_count

    def vob_delete_all_clicked(self):

        if afficher_message(titre=self.tr("Tous supprimer"),
                            message=self.tr("Voulez-vous vraiment supprimer ces éléments?"),
                            icone_question=True,
                            type_bouton=QMessageBox.Ok | QMessageBox.Cancel,
                            defaut_bouton=QMessageBox.Cancel) == QMessageBox.Cancel:
            return False

        self.vob_model.clear()
        self.change_made = True

        self.vob_table_selection_changed()
        return True

    def vob_copy(self):

        # --------------
        # Trade
        # --------------

        trade_value = self.ui.trade_combo.currentText()

        if not isinstance(trade_value, str):
            print("vob -- VobWidget -- vob_copy -- not isinstance(trade_value, str)")
            return False

        # --------------
        # Object
        # --------------

        object_value = self.ui.object_combo.currentText()

        if not isinstance(object_value, str):
            print("vob -- VobWidget -- vob_copy -- not isinstance(object_value, str)")
            return False

        # --------------
        # Unit
        # --------------

        unit_value = self.ui.unit_combo.currentText()

        if not isinstance(unit_value, str):
            print("vob -- VobWidget -- vob_copy -- not isinstance(unit_value, str)")
            return False

        # --------------
        # method
        # --------------

        method_value = self.ui.method_combo.currentText()

        if not isinstance(method_value, str):
            print("vob -- VobWidget -- vob_copy -- not isinstance(method_value, str)")
            return False

        # --------------
        # formula
        # --------------

        formula_value = self.ui.value_attrib.toPlainText()

        if not isinstance(formula_value, str):
            print("vob -- VobWidget -- vob_copy -- not isinstance(formula_value, str)")
            return False

        formula_value = formula_value.strip()

        # --------------
        # comment
        # --------------

        comment_value = self.ui.comment_line.text()

        if not isinstance(comment_value, str):
            print("vob -- VobWidget -- vob_copy -- not isinstance(comment_value, str)")
            return False

        comment_value = comment_value.strip()

        self.clipboard_trade = trade_value
        self.clipboard_object = object_value
        self.clipboard_unit = unit_value
        self.clipboard_method = method_value
        self.clipboard_formula = formula_value
        self.clipboard_comment = comment_value

        self.ui.paste_bt.setToolTip(f"{self.ui.trade_title.text()} = {trade_value}\n"
                                    f"{self.ui.object_title.text()} = {object_value}\n"
                                    f"{self.ui.unit_title.text()} = {unit_value}\n"
                                    f"{self.ui.method_title.text()} = {method_value}\n"
                                    f"{self.ui.formula_title.text()} = {formula_value}\n"
                                    f"{self.ui.comment_title.text()} = {comment_value}")

        self.vob_buttons_manage()

    def vob_paste(self):

        if not self.ui.paste_bt.isEnabled():
            return

        self.vob_search_clear()

        # ----------

        self.vob_table_add_line(vob_trade=self.clipboard_trade,
                                vob_object=self.clipboard_object,
                                vob_unit=self.clipboard_unit,
                                vob_method=self.clipboard_method,
                                vob_formula=self.clipboard_formula,
                                vob_comment=self.clipboard_comment,
                                select=True)

    @staticmethod
    def a___________________tools______():
        pass

    def vob_tools_clicked(self):

        if not isinstance(self.vob_file_obj, VobFileData):
            return

        vob_menu = MyContextMenu(tooltips_visible=False)

        vob_menu.add_action(qicon=get_icon(refresh_icon),
                            title=self.tr("Rafraichir"),
                            action=self.vob_tools_refresh_data)

        vob_menu.addSeparator()

        vob_menu.add_action(qicon=get_icon(open_icon),
                            title=self.tr("Ouvrir le dossier"),
                            action=self.vob_tools_open_folder)

        vob_menu.add_action(qicon=get_icon(open_text_editor_icon),
                            title=self.tr("Ouvrir le fichier"),
                            action=self.vob_tools_open_file)

        vob_menu.exec_(find_global_point(self.ui.tools_bt))

    def vob_tools_refresh_data(self):

        if not isinstance(self.vob_file_obj, VobFileData):
            print("vob -- VobWidget -- vob_tools_refresh_data -- not isinstance(self.vob_file_obj, VobFileData)")
            return

        if not self.vob_save_ask():
            return False

        self.vob_translate_datas()
        self.vob_table_load()

    def vob_tools_open_folder(self):

        if not isinstance(self.vob_file_obj, VobFileData):
            print("vob -- VobWidget -- vob_tools_open_folder -- not isinstance(self.vob_file_obj, VobFileData)")
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.vob_file_obj.folder_path, show_msg=True)
            return

        open_folder(folder_path=self.vob_file_obj.folder_path)

    def vob_tools_open_file(self):

        if not isinstance(self.vob_file_obj, VobFileData):
            print("vob -- VobWidget -- vob_tools_open_folder -- not isinstance(self.vob_file_obj, VobFileData)")
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            copy_to_clipboard(value=self.vob_file_obj.file_path, show_msg=True)
            return

        open_file(file_path=self.vob_file_obj.file_path)

    @staticmethod
    def a___________________search______():
        pass

    def vob_search_filter_changed(self):

        current_index = self.ui.search_filter_combo.currentIndex()

        self.vob_filter.setFilterKeyColumn(current_index)

        self.vob_table_selection_changed()

    def vob_search_changed(self):

        current_text = self.ui.search.text()

        if current_text == "":
            self.ui.search.setStyleSheet("QLineEdit{padding-left: 5px; "
                                         "border: 1px solid #8f8f91; "
                                         "border-left-width: 0px; }")

        else:
            self.ui.search.setStyleSheet("QLineEdit{padding-left: 4px; "
                                         "border: 2px solid orange; "
                                         "border-left-width: 0px; }")

        self.vob_filter.setFilterRegExp(current_text)

        self.vob_table_selection_changed()

    def vob_search_clear(self):
        self.ui.search.clear()
        self.vob_search_changed()

    def vob_search_formula_clicked(self):

        search_formula_on = self.ui.search_formula.isChecked()

        if search_formula_on:
            self.vob_search_clear()

            self.vob_filter.setFilterRole(user_formule_ok)
            self.vob_filter.setFilterKeyColumn(col_vob_formula)
            self.vob_filter.setFilterRegExp("no")

            if self.vob_filter.rowCount() == 0:
                afficher_message(titre=application_title,
                                 message=self.tr("Aucune formule avec erreur trouvée!"),
                                 icone_valide=True)

                self.vob_search_reset_filter()
                return

            qm_filter = self.vob_filter.index(0, col_vob_trade)
            self.vob_table_select(qm_filter)
            self.ui.vob_table.scrollTo(qm_filter, QAbstractItemView.PositionAtCenter)

        else:

            self.vob_search_reset_filter()

    def vob_search_reset_filter(self):

        self.vob_filter.setFilterRole(Qt.DisplayRole)
        self.vob_filter.setFilterKeyColumn(self.ui.search_filter_combo.currentIndex())
        self.vob_filter.setFilterRegExp(self.ui.search.text())

        # -------------

        if self.ui.search_formula.isChecked():
            self.ui.search_formula.setChecked(False)

            self.vob_search_restore_current()

        self.vob_table_selection_changed()

    def vob_search_save_current(self) -> bool:

        qm_filter = self.ui.vob_table.selectionModel().currentIndex()

        if not qm_check(qm_filter):
            print("vob -- VobWidget -- vob_search_save_current -- not qm_check(qm_filter)")
            return False

        qm_model = self.vob_filter.mapToSource(qm_filter)

        if not qm_check(qm_model):
            print("vob -- VobWidget -- vob_search_save_current -- not qm_check(qm_model)")
            return False

        self.qm_current = qm_model

        return True

    def vob_search_restore_current(self) -> bool:

        if not qm_check(self.qm_current):
            print("vob -- VobWidget -- vob_search_restore_current -- not qm_check(self.qm_current)")
            return False

        qm_filter = self.vob_filter.mapFromSource(self.qm_current)

        if not qm_check(qm_filter):
            print("vob -- VobWidget -- vob_search_restore_current -- not qm_check(qm_filter)")
            return False

        self.vob_table_select(qm=qm_filter)
        self.ui.vob_table.scrollTo(qm_filter, QAbstractItemView.PositionAtCenter)
        return True

    @staticmethod
    def a___________________table______():
        pass

    def vob_table_load(self, datas=None) -> bool:

        if not isinstance(self.vob_file_obj, VobFileData):
            print("vob -- VobWidget -- vob_table_load -- not isinstance(self.vob_file_obj, VobFileData)")
            self.vob_buttons_manage()
            return False

        if not self.vob_make_backup_original():
            print("vob -- VobWidget -- vob_table_load -- not self.vob_make_backup_original(self.vob_file_obj)")
            self.vob_buttons_manage()
            return False

        self.vob_load_window_title()
        self.vob_table_clear()
        self.vob_information_clear()

        # ------------ read file ------------

        if not isinstance(datas, list):
            datas = read_file_to_list(file_path=self.vob_file_obj.file_path)

        if len(datas) == 0:
            self.vob_buttons_manage()
            return True

        # ------------ read line ------------

        for line in datas:

            if not isinstance(line, str):
                print("vob -- VobWidget -- vob_table_load -- not isinstance(line, str)")
                continue

            # ------------ ignore comment ------------

            line = line.strip()

            if line == "":
                continue

            if not line.startswith("#"):
                continue

            # ------------ check line ------------

            separator_count = line.count("#")

            if separator_count != 5:
                print("vob -- VobWidget -- vob_table_load -- separator_count != 5")
                continue

            line = line.replace("#", "", 1)

            # ------------ read line datas ------------

            sub_datas = line.split("#", 4)

            if len(sub_datas) != 5:
                print("vob -- VobWidget -- vob_table_load -- len(sub_datas) != 5")
                continue

            # ------------ Trade ------------

            vob_trade = sub_datas[0]

            if not isinstance(vob_trade, str):
                print("vob -- VobWidget -- vob_table_loadd -- not isinstance(vob_trade, str)")
                continue

            vob_trade = vob_trade.strip()

            if vob_trade != "-1":
                vob_trade = vob_trade.zfill(3)
            else:
                vob_trade = "  -1"

            if vob_trade in self.trade_dict:
                vob_trade = f"{vob_trade} = {self.trade_dict[vob_trade]}"
            else:
                vob_trade = f"{vob_trade} = ?"
                print("vob -- VobWidget -- vob_table_loadd -- vob_trade not in self.trade_dict")

            # ------------ Object ------------

            vob_object = sub_datas[1]

            if not isinstance(vob_object, str):
                print("vob -- VobWidget -- vob_table_load -- not isinstance(vob_object, str)")
                continue

            vob_object = vob_object.strip()

            if vob_object != "-1":
                vob_object = vob_object.zfill(4)
            else:
                vob_object = "   -1"

            if vob_object in self.object_dict:
                vob_object = f"{vob_object} = {self.object_dict[vob_object]}"
            else:
                vob_object = f"{vob_object} = ?"
                print("vob -- VobWidget -- vob_table_loadd -- vob_object not in self.object_dict")

            # ------------ Unit ------------

            vob_unit = sub_datas[2]

            if not isinstance(vob_unit, str):
                print("vob -- VobWidget -- vob_table_load -- not isinstance(vob_unit, str)")
                continue

            vob_unit = vob_unit.strip()

            if vob_unit != "-1":
                vob_unit = vob_unit.zfill(2)

            if vob_unit in self.unit_dict:
                vob_unit = f"{vob_unit} = {self.unit_dict[vob_unit]}"
            else:
                vob_unit = f"{vob_unit} = ?"
                print("vob -- VobWidget -- vob_table_loadd -- vob_unit not in self.unit_dict")

            # ------------ Method ------------

            vob_method = sub_datas[3]

            if not isinstance(vob_method, str):
                print("vob -- VobWidget -- vob_table_load -- not isinstance(vob_method, str)")
                continue

            vob_method = vob_method.strip()

            if vob_method != "-1":
                vob_method = vob_method.zfill(2)

            if vob_method in self.method_dict:
                vob_method = f"{vob_method} = {self.method_dict[vob_method]}"
            else:
                vob_method = f"{vob_method} = ?"
                print("vob -- VobWidget -- vob_table_loadd -- vob_method not in self.method_dict")

            # ------------ Formula ------------

            vob_formula = sub_datas[4]

            if not isinstance(vob_formula, str):
                print("vob -- VobWidget -- vob_table_load -- not isinstance(vob_formula, str)")
                continue

            vob_formula = vob_formula.strip()

            # ------------ comment ------------

            vob_comment = ""

            if ";" in vob_formula:
                formula_split = vob_formula.split(";", 1)

                if len(formula_split) != 2:
                    print("vob -- VobWidget -- vob_table_load -- len(formula_split) != 2")
                    continue

                vob_formula, vob_comment = formula_split

                vob_formula = vob_formula.strip()
                vob_comment = vob_comment.replace("//", "").strip()

            if "//" in vob_formula:
                formula_split = vob_formula.split("//", 1)

                if len(formula_split) != 2:
                    print("vob -- VobWidget -- vob_table_load -- len(formula_split) != 2")
                    continue

                vob_formula, vob_comment = formula_split

                vob_formula = vob_formula.strip()
                vob_comment = vob_comment.strip()

            self.vob_table_add_line(vob_trade=vob_trade,
                                    vob_object=vob_object,
                                    vob_unit=vob_unit,
                                    vob_method=vob_method,
                                    vob_formula=vob_formula,
                                    vob_comment=vob_comment)

        self.vob_table_header_manage()
        self.change_made = False
        self.vob_buttons_manage()
        return True

    def vob_table_selection_changed(self):

        self.autocompletion.hide()

        qs_select_list = self.ui.vob_table.selectionModel().selectedRows()

        self.vob_buttons_manage()

        if len(qs_select_list) != 1:
            self.row_current = -1
            self.vob_information_clear()

            return

        self.vob_information_load(qm=qs_select_list[0])

    def vob_table_select(self, qm: QModelIndex) -> bool:

        self.autocompletion.hide()

        if not qm_check(qm):
            print("vob -- VobWidget -- vob_table_select -- not qm_check(qm)")
            return False

        if qm.model() == self.vob_model:
            qm = self.vob_filter.mapFromSource(qm)

            if not qm_check(qm):
                print("vob -- VobWidget -- vob_table_select -- not qm_check(qm) -- 2")
                return False

        self.ui.vob_table.scrollTo(qm, QAbstractItemView.PositionAtCenter)
        self.ui.vob_table.clearSelection()
        self.ui.vob_table.selectionModel().select(qm, QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def vob_table_header_manage(self):

        header = self.ui.vob_table.horizontalHeader()

        if header is None:
            return

        for column_index in range(self.vob_model.columnCount() - 1):
            header.setSectionResizeMode(column_index, QHeaderView.ResizeToContents)

    def vob_table_clear(self):
        self.vob_model.clear()
        self.vob_model.setHorizontalHeaderLabels(self.header_title)

    def vob_table_add_line(self, vob_trade: str, vob_object: str, vob_unit: str,
                           vob_method: str, vob_formula: str, vob_comment="", row_index=-1, select=False) -> list:

        vob_formula_valid = self.vob_formula_check(formula_current=vob_formula, update_icon=False)

        qs_formula = QStandardItem(vob_formula)
        if vob_formula_valid:
            qs_formula.setData("ok", user_formule_ok)
        else:
            qs_formula.setData("no", user_formule_ok)

        qs_list = [QStandardItem(vob_trade),
                   QStandardItem(vob_object),
                   QStandardItem(vob_unit),
                   QStandardItem(vob_method),
                   qs_formula,
                   QStandardItem(vob_comment)]

        if row_index == -1:
            self.vob_model.appendRow(qs_list)
        else:
            self.vob_model.insertRow(row_index, qs_list)

        if not select:
            return qs_list

        qm_model = qs_formula.index()

        if not qm_check(qm_model):
            print("vob -- VobWidget -- vob_add -- not qm_check(qm_model)")
            return

        qm_filter = self.vob_filter.mapFromSource(qm_model)

        if not qm_check(qm_filter):
            print("vob -- VobWidget -- vob_add -- not qm_check(qm_filter)")
            return

        self.vob_table_select(qm=qm_filter)
        self.ui.vob_table.scrollTo(qm_filter, QAbstractItemView.PositionAtCenter)

        # ----------

        self.ui.trade_combo.setFocus()

        # ----------

        self.change_made = True

        return qs_list

    def vob_table_menu_show(self, point: QPoint):

        vob_menu = MyContextMenu(tooltips_visible=False)

        vob_menu.add_title(title=self.tr("Fichier"))

        vob_menu.add_action(qicon=get_icon(open_icon),
                            title=self.tr("Ouvrir"),
                            action=self.vob_open_file_clicked,
                            tooltips=self.ui.open_file_bt.toolTip(),
                            short_link=self.ui.open_file_bt.whatsThis())

        vob_menu.add_action(qicon=get_icon(save_icon),
                            title=self.tr("Enregistrer"),
                            action=self.vob_save_file_clicked,
                            tooltips=self.ui.save_bt.toolTip(),
                            short_link=self.ui.save_bt.whatsThis())

        vob_menu.add_action(qicon=get_icon(save_as_icon),
                            title=self.tr("Enregistrer sous"),
                            action=self.vob_save_as_file_clicked,
                            tooltips=self.ui.save_as_file_bt.toolTip(),
                            short_link=self.ui.save_as_file_bt.whatsThis())

        vob_menu.add_title(title=self.tr("Édition"))

        vob_menu.add_action(qicon=get_icon(add_icon),
                            title=self.tr("Ajouter"),
                            action=self.vob_add,
                            tooltips=self.ui.add_bt.toolTip(),
                            short_link=self.ui.add_bt.whatsThis())

        if self.ui.delete_bt.isEnabled():
            vob_menu.add_action(qicon=get_icon(delete_icon),
                                title=self.tr("Supprimer"),
                                action=self.vob_delete,
                                tooltips=self.ui.delete_bt.toolTip(),
                                short_link=self.ui.delete_bt.whatsThis())

        if self.ui.copy_bt.isEnabled():
            vob_menu.add_action(qicon=get_icon(copy_icon),
                                title=self.tr("Copier"),
                                action=self.vob_copy,
                                tooltips=self.ui.copy_bt.toolTip(),
                                short_link=self.ui.copy_bt.whatsThis())

        if self.ui.paste_bt.isEnabled():
            vob_menu.add_action(qicon=get_icon(paste_icon),
                                title=self.tr("Coller"),
                                action=self.vob_paste,
                                tooltips=self.ui.paste_bt.toolTip(),
                                short_link=self.ui.paste_bt.whatsThis())

        vob_menu.exec_(self.ui.vob_table.mapToGlobal(point))

    @staticmethod
    def a___________________informations______():
        pass

    def vob_information_load(self, qm: QModelIndex) -> bool:

        if not isinstance(qm, QModelIndex):
            self.row_current = -1
            self.vob_information_clear()
            self.vob_buttons_info_manage(enable=False)
            return False

        self.vob_buttons_info_manage(enable=True)

        self.row_current = qm.row()

        # ------------
        # Trade
        # ------------

        trade_value = self.vob_get_data(row_index=self.row_current,
                                        column_index=col_vob_trade,
                                        model=self.vob_filter)

        # ------------
        # object
        # ------------

        object_value = self.vob_get_data(row_index=self.row_current,
                                         column_index=col_vob_object,
                                         model=self.vob_filter)

        # ------------
        # unit
        # ------------

        unit_value = self.vob_get_data(row_index=self.row_current,
                                       column_index=col_vob_unit,
                                       model=self.vob_filter)

        # ------------
        # method
        # ------------

        method_value = self.vob_get_data(row_index=self.row_current,
                                         column_index=col_vob_method,
                                         model=self.vob_filter)

        # ------------
        # formula
        # ------------

        formula_value = self.vob_get_data(row_index=self.row_current,
                                          column_index=col_vob_formula,
                                          model=self.vob_filter)

        # ------------
        # comment
        # ------------

        comment_value = self.vob_get_data(row_index=self.row_current,
                                          column_index=col_vob_comment,
                                          model=self.vob_filter)

        # ------------
        # Trade
        # ------------

        if trade_value in self.trade_list:
            trade_index = self.trade_list.index(trade_value)

            self.ui.trade_combo.setCurrentIndex(trade_index)
        else:
            print(f"vob -- VobWidget -- vob_information_load -- {trade_value} not in self.trade_list")

        # ------------
        # object
        # ------------

        if object_value in self.object_list:

            object_index = self.object_list.index(object_value)

            self.ui.object_combo.setCurrentIndex(object_index)
        else:
            print(f"vob -- VobWidget -- vob_information_load -- {object_value} not in self.object_list")

        # ------------
        # unit
        # ------------

        if unit_value in self.unit_list:

            unit_index = self.unit_list.index(unit_value)

            self.ui.unit_combo.setCurrentIndex(unit_index)
        else:
            print(f"vob -- VobWidget -- vob_information_load -- {unit_value} not in self.unit_list")

        # ------------
        # method
        # ------------

        if method_value in self.method_list:

            method_index = self.method_list.index(method_value)

            self.ui.method_combo.setCurrentIndex(method_index)
        else:
            print(f"vob -- VobWidget -- vob_information_load -- {method_value} not in self.method_list")

        # ------------
        # formula
        # ------------

        self.ui.value_attrib.setPlainText(formula_value)

        # ------------
        # comment
        # ------------

        self.ui.comment_line.setText(comment_value)

        # ------------
        # Translation
        # ------------

        self.vob_translation()

        return True

    def vob_information_clear(self):

        self.ui.trade_combo.blockSignals(True)
        self.ui.trade_combo.setCurrentIndex(0)
        self.ui.trade_combo.blockSignals(False)

        self.ui.object_combo.blockSignals(True)
        self.ui.object_combo.setCurrentIndex(0)
        self.ui.object_combo.blockSignals(False)

        self.ui.unit_combo.blockSignals(True)
        self.ui.unit_combo.setCurrentIndex(0)
        self.ui.unit_combo.blockSignals(False)

        self.ui.method_combo.blockSignals(True)
        self.ui.method_combo.setCurrentIndex(0)
        self.ui.method_combo.blockSignals(False)

        self.ui.value_attrib.blockSignals(True)
        self.ui.value_attrib.clear()
        self.ui.value_attrib.blockSignals(False)

        self.ui.comment_line.blockSignals(True)
        self.ui.comment_line.clear()
        self.ui.comment_line.blockSignals(False)

        self.ui.translation.clear()

    @staticmethod
    def a___________________info_bt______():
        pass

    def vob_trade_changed(self) -> bool:

        if not self.ui.trade_combo.isEnabled():
            return True

        return self.vob_combo_changed(combo=self.ui.trade_combo,
                                      column_index=col_vob_trade,
                                      datas_list=self.trade_list)

    def vob_object_changed(self) -> bool:

        if not self.ui.object_combo.isEnabled():
            return True

        return self.vob_combo_changed(combo=self.ui.object_combo,
                                      column_index=col_vob_object,
                                      datas_list=self.object_list)

    def vob_unit_changed(self) -> bool:

        if not self.ui.unit_combo.isEnabled():
            return True

        return self.vob_combo_changed(combo=self.ui.unit_combo,
                                      column_index=col_vob_unit,
                                      datas_list=self.unit_list)

    def vob_method_changed(self) -> bool:

        if not self.ui.method_combo.isEnabled():
            return True

        return self.vob_combo_changed(combo=self.ui.method_combo,
                                      column_index=col_vob_method,
                                      datas_list=self.method_list)

    def vob_comment_changed(self) -> bool:

        if not self.ui.comment_line.isEnabled():
            return True

        return self.vob_item_changed(current_value=self.ui.comment_line.text(), column_index=col_vob_comment)

    def vob_combo_changed(self, combo: QComboBox, column_index: int, datas_list: list):

        if not self.isVisible() or not combo.isEnabled():
            return True

        if not isinstance(combo, QComboBox):
            print("vob -- VobWidget -- vob_combo_changed -- not isinstance(combo, QComboBox)")
            return False

        combo_model = combo.model()

        if not isinstance(combo_model, QStandardItemModel):
            print("vob -- VobWidget -- vob_combo_changed -- not isinstance(combo_model, QStandardItemModel)")
            return False

        current_text = combo.currentText()

        search = combo_model.findItems(current_text, Qt.MatchExactly, 0)

        if len(search) != 0:
            return self.vob_item_changed(current_value=current_text, column_index=column_index)

        search = combo_model.findItems(current_text, Qt.MatchContains, 0)

        if len(search) == 0:
            combo.setCurrentIndex(0)
            print("vob -- VobWidget -- vob_combo_changed -- not isinstance(old_value, str)")
            return False

        qs_value = search[0]

        if not isinstance(qs_value, QStandardItem):
            combo.setCurrentIndex(0)
            print("vob -- VobWidget -- vob_combo_changed -- not isinstance(qs_value, QStandardItem)")
            return False

        value = qs_value.text()

        if value not in datas_list:
            combo.setCurrentIndex(0)
            print("vob -- VobWidget -- vob_combo_changed -- value not in datas_list")
            return False

        new_index = datas_list.index(value)
        combo.setCurrentIndex(new_index)

        self.vob_translation()
        return False

    def vob_item_changed(self, current_value: str, column_index: int) -> bool:

        if not self.isVisible():
            return True

        old_value = self.vob_get_data(row_index=self.row_current, column_index=column_index, model=self.vob_filter)

        if not isinstance(current_value, str) or not isinstance(old_value, str):
            print("vob -- VobWidget -- vob_item_changed -- not isinstance(current_value, str)")
            return False

        if current_value == old_value:
            return True

        qm = self.vob_filter.index(self.row_current, column_index)

        if not qm_check(qm):
            print("vob -- VobWidget -- vob_item_changed -- not qm_check(qm)")
            return False

        self.vob_filter.setData(qm, current_value)
        self.change_made = True

        self.vob_translation()
        return True

    def vob_comment_clear_clicked(self):

        self.ui.comment_line.clear()
        self.vob_comment_changed()

    @staticmethod
    def a___________________translation______():
        pass

    def vob_translation(self):

        text = "<p style='white-space:pre'>"

        # -----------
        # Object
        # -----------

        object_value = self.ui.object_combo.currentText().strip()

        if object_value.startswith("-1"):
            text += "<b>"
            text += self.tr("Pour tous les types d'objets")
            text += "</b>,<br>"
        else:
            object_value = object_value[7:]
            text += self.tr("Pour les objets de type")
            text += f": <b>{object_value}</b>,<br>"

        # -----------
        # Trade
        # -----------

        trade_value = self.ui.trade_combo.currentText().strip()

        if trade_value.startswith("-1"):

            text += "<b>"
            text += self.tr("Avec n'importe quel métier")
            text += "</b>,<br>"
        else:
            trade_value = trade_value[6:]
            text += self.tr("Avec un métier")
            text += f": <b>{trade_value}</b>,<br>"

        # -----------
        # Unit
        # -----------

        unit_value = self.ui.unit_combo.currentText().strip()

        if unit_value.startswith("-1"):
            text += "<b>"
            text += self.tr("Et avec n'importe quelle unité")
            text += "</b>,<br>"
        else:
            unit_value = unit_value[5:]
            text += self.tr("Et avec une unité")
            text += f" : <b>{unit_value}</b>,<br>"

        # -----------
        # Method
        # -----------

        # method_value = self.ui.method_combo.currentText()

        # -----------
        # Formula
        # -----------

        formula_value = self.ui.value_attrib.toPlainText().strip()

        formula_value_tmp = formula_value.replace(" ", "")

        if formula_value_tmp == "0" or formula_value_tmp == "1=0" or formula_value == "0=1":
            text += "<b>"
            text += self.tr("Cet objet sera toujours ignoré du quantitatif")
            text += "</b>,<br>"

        elif formula_value_tmp == "1" or formula_value_tmp == "1=1" or formula_value_tmp == "0=0":
            text += "<b>"
            text += self.tr("Le calcul sera toujours effectué")
            text += "</b>,<br>"

        else:

            formula_translated = self.allplan.traduction_formule_allplan(formula=formula_value, format_on=False)

            text += self.tr("Le calcul sera effectué si")
            text += f": <b>{formula_translated}</b>,<br>"
            text += self.tr("Sinon, cet objet sera ignoré du quantitatif.")

        self.ui.translation.clear()
        self.ui.translation.appendHtml(text)

    @staticmethod
    def a___________________formula______():
        pass

    def vob_formula_selection_changed(self):
        self.allplan.gestion_tooltip_formule(self.ui.value_attrib)
        selectionner_parentheses(self)

    def vob_formula_changed(self):

        if not self.isVisible():
            return

        modifiers = QApplication.keyboardModifiers()

        if self.hasFocus() and modifiers != Qt.ControlModifier:
            self.autocompletion.gestion_widget()

        is_valid = self.vob_formula_check(formula_current=self.ui.value_attrib.toPlainText(), update_icon=True)

        qm = self.vob_filter.index(self.row_current, col_vob_formula)

        if not qm_check(qm):
            print("vob -- VobWidget -- vob_formula_changed -- not qm_check(qm)")
            return

        qm_model = self.vob_filter.mapToSource(qm)

        if not qm_check(qm_model):
            print("vob -- VobWidget -- vob_formula_changed -- not qm_check(qm_model)")
            return

        self.qm_current = qm_model

        if is_valid:
            self.vob_filter.setData(qm, "ok", user_formule_ok)
        else:
            self.vob_filter.setData(qm, "no", user_formule_ok)

        if self.vob_filter.rowCount() == 0:
            self.vob_search_reset_filter()

    def vob_formula_finished(self) -> bool:
        if not self.ui.value_attrib.isEnabled():
            return True

        return self.vob_item_changed(current_value=self.ui.value_attrib.toPlainText(), column_index=col_vob_formula)

    def vob_formula_check(self, formula_current: str, update_icon=True) -> bool:

        if formula_current == "":
            if update_icon:
                self.vob_formula_valid(error="")
            return True

        # Vérification si formule = "1" ==> "1"
        try:
            int(formula_current)

            if update_icon:
                self.vob_formula_valid(error="")

            return True
        except ValueError:
            pass

        error_message = list()
        check_word = True

        # -------------------
        # Check quote
        # -------------------

        if '"' in formula_current:

            if not formula_current.count('"') % 2 == 0:

                formula_without_quotes = formula_current
                error_message.append(self.tr("le nombre de guillemets n'est pas correct"))
                check_word = False

            else:

                formula_without_quotes = re.sub(r'"[^"]*"', '', formula_current)

        else:
            formula_without_quotes = formula_current

        # -------------------
        # Check @@
        # -------------------

        if "@" in formula_current:

            errors_list = self.allplan.is_formula_valid(formula=formula_current)

            if not formula_current.count("@") % 2 == 0:

                formula_without_attrib = formula_without_quotes
                error_message.append(self.tr("le nombre de '@' n'est pas correct"))
                check_word = False

            elif len(errors_list) != 0:

                formula_without_attrib = formula_without_quotes
                error_message.extend(errors_list)
                check_word = False

            else:

                formula_without_attrib = re.sub(r'@\d+@', '', formula_without_quotes)

                formula_without_space = formula_without_quotes.replace(" ", "")

                matches = re.finditer(r"@(.*?)@", formula_without_space)

                text_part_1 = self.tr("La syntaxe est invalide")

                unknown_txt = self.tr("Attribut inconnu")
                unknown_attributes = list()

                special_attributes = ["@OBJ@", "@VOB@", "@GW@"]
                symbol_valid_befor = ["&", "|", "+", "-", "*", "/", "=", ">", "<", "!", "(", ")", "_", ""]
                symbol_valid_after = ["&", "|", "+", "-", "*", "/", "=", ">", "<", ")", ";", "^", "_", ""]

                for match in matches:

                    attribute = match.group()

                    start, end = match.span()

                    before = formula_without_space[start - 1] if start > 0 else ''

                    after = formula_without_space[end] if end < len(formula_without_space) else ''

                    if before not in symbol_valid_befor:
                        error_message.append(f"{text_part_1} : {before}{attribute}")

                    if after not in symbol_valid_after:
                        error_message.append(f"{text_part_1} : {attribute}{after}")

                    if attribute.upper() in special_attributes:
                        formula_without_attrib = formula_without_attrib[:start] + formula_without_attrib[end:]
                        continue

                    number = attribute.replace("@", "")

                    if number in unknown_attributes:
                        continue

                    if number in self.allplan.attributes_dict:
                        continue

                    if not isinstance(number, str):
                        continue

                    if not number.isdigit():
                        convert = self.allplan.formula_match_name(name=number)

                        if convert != "":
                            continue

                    unknown_attributes.append(number)
                    error_message.append(f"{unknown_txt} : @{number}@")

        else:

            formula_without_attrib = formula_without_quotes

        # -------------------
        # Check parenthesis
        # -------------------

        if not formula_current.count("(") == formula_current.count(")"):
            error_message.append(self.tr("le nombre de parenthèses n'est pas correct"))

        # -------------------
        # Check classic error
        # -------------------

        for word in ["IF", "ELSE"]:

            if word in formula_without_attrib.upper():
                error_message.append(word + " " + self.tr("n'est pas correct"))

        for caractere in liste_caracteres_fin:
            if formula_current.endswith(caractere):
                error_message.append(self.tr("La formule se termine par un caractère non valide"))
                break

        # -------------------
        # Check bad syntaxe
        # -------------------

        if check_word:
            words = re.findall(r'\b\w+\b', formula_without_attrib)

            for word in words:

                if not isinstance(word, str):
                    continue

                if word.isdigit():
                    continue

                error_message.append(word + " " + self.tr("n'est pas correct"))

                if len(error_message) > 20:
                    error_message.append("...")
                    break

        # -------------------
        # Define message
        # -------------------

        if len(error_message) == 0:
            if update_icon:
                self.vob_formula_valid(error="")
            return True

        if update_icon:
            error = "- " + "\n- ".join(error_message)
            self.vob_formula_valid(error=error)

        return False

    def vob_formula_valid(self, error: str):

        if error == "":
            self.ui.formula_verification_bt.setIcon(get_icon(valid_icon))
            self.ui.formula_verification_bt.setToolTip(self.tr("C'est tout bon!"))

            # ----------

            self.ui.value_attrib.setStyleSheet("QPlainTextEdit{"
                                               "border: 1px solid #8f8f91; "
                                               "border-right-width: 0px; "
                                               "padding-left: 5px; "
                                               "padding-right: 5px; "
                                               "padding-top: 1px; "
                                               "padding-bottom: 1px; "
                                               "border-top-left-radius: 5px; "
                                               "border-bottom-left-radius: 5px; "
                                               "background-color: #FFFFFF; }")

            return

        self.ui.formula_verification_bt.setIcon(get_icon(error_icon))
        self.ui.formula_verification_bt.setToolTip(error)

        # ----------

        self.ui.value_attrib.setStyleSheet("QPlainTextEdit{"
                                           "border: 2px solid orange; "
                                           "border-right-width: 0px; "
                                           "padding-left: 4px; "
                                           "padding-right: 4px; "
                                           "padding-top: 1px; "
                                           "padding-bottom: 1px; "
                                           "border-top-left-radius: 5px; "
                                           "border-bottom-left-radius: 5px; "
                                           "background-color: #FFFFFF; }")

    def vob_formula_clicked(self):

        tooltip = self.ui.formula_verification_bt.toolTip()

        if tooltip == self.tr("C'est tout bon!"):

            afficher_message(titre=application_title,
                             message=self.tr("Cette formule paraît correcte !"),
                             icone_valide=True)

        else:
            afficher_message(titre=application_title,
                             message=f"{tooltip}",
                             icone_critique=True)

    @staticmethod
    def a___________________formula_tool______():
        pass

    def vob_formula_editor_show(self):

        self.widget_creation_formule.show_formula(value_widget=self.ui.value_attrib,
                                                  parent_actuel=self,
                                                  number="-1",
                                                  bt_favoris=False)

        self.widget_formule_visible = True

    def vob_formula_editor_changed(self, value_widget: QPlainTextEdit, formule: str, position_cursor: int):

        if value_widget != self.ui.value_attrib:
            return

        self.ui.value_attrib.setPlainText(formule)
        self.vob_formula_finished()

        self.ui.value_attrib.setFocus()

        cursor = self.ui.value_attrib.textCursor()
        cursor.setPosition(position_cursor, QTextCursor.MoveAnchor)
        self.ui.value_attrib.setTextCursor(cursor)

    def vob_formula_editor_closed(self):
        self.ui.value_attrib.autocompletion.hide()
        self.widget_formule_visible = False

    @staticmethod
    def a___________________tools_method______():
        pass

    @staticmethod
    def vob_get_data(row_index: int, column_index: int, model: QStandardItemModel | QSortFilterProxyModel) -> str:

        qm = model.index(row_index, column_index)

        if not qm_check(qm):
            print("vob -- VobWidget -- vob_get_data -- not qm_check(qm)")
            return ""

        text = qm.data()

        if not isinstance(text, str):
            print("vob -- VobWidget -- vob_get_data -- not isinstance(text, str)")
            return ""

        return text

    @staticmethod
    def vob_get_index(value: str) -> str:

        if " = " not in value:
            print(f"vob -- VobWidget -- vob_get_index -- ' = ' not in value")
            return "-1"

        data = value.split(" = ", 1)

        if len(data) != 2:
            print(f"vob -- VobWidget -- vob_get_index -- len(data) != 2")
            return "-1"

        index_current = data[0]

        index_current = index_current.strip()

        if index_current == "":
            return "-1"

        return index_current

    def vob_get_files(self) -> list:

        vob_files_list = list()

        allplan_paths = self.allplan.allplan_paths

        if isinstance(allplan_paths, AllplanPaths):
            etc_path = allplan_paths.etc_path
        elif isinstance(self.vob_file_obj, VobFileData):
            etc_path = find_folder_path(self.vob_file_obj.folder_path)
        else:
            print("vob -- VobWidget -- vob_get_files -- not path")
            return vob_files_list

        if not os.path.exists(etc_path):
            print("vob -- VobWidget -- vob_get_files -- not os.path.exists(etc_path)")
            return vob_files_list

        files_list = glob.glob(f"{etc_path}vo*")

        # ----------

        for file_path in files_list:

            if not os.path.isfile(file_path):
                continue

            vob_file_obj = VobFileData(file_path=file_path)

            if not vob_file_obj.is_valid:
                # print("vob -- VobWidget -- vob_get_files --  not vob_file_obj.is_valid")
                continue

            vob_files_list.append(vob_file_obj)

        return vob_files_list

    @staticmethod
    def vob_file_path_isvalid(file_path) -> VobFileData:
        return VobFileData(file_path=file_path)

    @staticmethod
    def a___________________backup_orginal______():
        pass

    def vob_make_backup_original(self) -> bool:

        if not isinstance(self.vob_file_obj, VobFileData):
            print("vob -- VobWidget -- vob_make_backup_original --  not isinstance(vob_file_obj, VobFileData)")
            return False

        backup_folder = f"{self.vob_file_obj.folder_path}Backup\\"
        backup_path = f"{backup_folder}{self.vob_file_obj.file_name_ext}.original"

        if not os.path.exists(backup_folder):
            try:
                os.mkdir(backup_folder)
            except Exception as error:

                afficher_message(titre=self.tr("Sauvegarde : le fichier original"),
                                 message=self.tr("Une erreur est survenue."),
                                 icone_critique=True,
                                 details=f"{error}",
                                 afficher_details=True)
                return False
        #  --------------------------

        if os.path.exists(backup_path):
            return True

        try:
            shutil.copy(self.vob_file_obj.file_path, backup_path)
            print("vob -- VobWidget -- vob_make_backup_original -- original backup == Ok")
            return True

        except Exception as error:
            afficher_message(titre=self.tr("Sauvegarde : le fichier original"),
                             message=self.tr("Une erreur est survenue."),
                             icone_critique=True,
                             details=f"{error}",
                             afficher_details=True)
        return False

    def vob_restore_original(self) -> bool:

        if not isinstance(self.vob_file_obj, VobFileData):
            print("vob -- VobWidget -- vob_restore_original --  not isinstance(vob_file_obj, VobFileData)")
            return False

        if not self.vob_save_ask():
            return False

        backup_path = f"{self.vob_file_obj.folder_path}Backup\\{self.vob_file_obj.file_name_ext}.original"

        if not os.path.exists(backup_path):
            afficher_message(titre=self.tr("Restaurer fichier VOB"),
                             message=self.tr("Le fichier VOB n'a pas été trouvé."),
                             icone_critique=True)
            return False

        datas = read_file_to_list(file_path=backup_path)

        if len(datas) == 0:
            return False

        self.vob_table_load(datas=datas)
        self.change_made = True

        return True

    @staticmethod
    def a___________________save______():
        pass

    def vob_save_ask(self) -> bool:

        if not isinstance(self.vob_file_obj, VobFileData):
            return False

        self.setFocus()

        if not self.change_made:
            return True

        response = afficher_message(titre=application_title,
                                    message=self.tr("Voulez-vous enregistrer les modifications?"),
                                    type_bouton=QMessageBox.Ok | QMessageBox.No,
                                    defaut_bouton=QMessageBox.Ok,
                                    icone_question=True)

        if response == QMessageBox.Cancel:
            return False

        if response == QMessageBox.No:
            return True

        return self.vob_save_datas(file_path=self.vob_file_obj.file_path)

    def vob_save_file_clicked(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            self.vob_save_settings()
            return True

        if not isinstance(self.vob_file_obj, VobFileData):
            return False

        self.vob_save_datas(file_path=self.vob_file_obj.file_path)

        self.change_made = False

    def vob_save_as_file_clicked(self):

        if not isinstance(self.vob_file_obj, VobFileData):
            return False

        a = self.tr("Fichier")
        extention_valid = [f".{extension}" for extension in language_extension_3.values()]

        # --------

        filename = self.vob_file_obj.file_name_ext
        file_ext = self.vob_file_obj.extension
        current_folder = self.vob_file_obj.folder_path

        # --------

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [self.allplan.allplan_paths.etc_path, current_folder, self.vob_save_folder]

        else:

            shortcuts_list = [current_folder, self.vob_save_folder]

        # --------

        datas_filters = {f"{a} VOB {file_ext.upper()}": [f".{file_ext}"],
                         f"{a} VOB": extention_valid}

        for ext in language_extension_3.values():

            title = f"{a} VOB {ext.upper()}"

            if title in datas_filters:
                continue

            datas_filters[title] = [f".{ext}"]

        # --------

        file_path = browser_file(parent=self,
                                 title=self.tr("Enregistrer sous"),
                                 registry=[],
                                 datas_filters=datas_filters,
                                 shortcuts_list=shortcuts_list,
                                 current_path=current_folder,
                                 file_name=filename,
                                 use_save=True)

        if file_path == "":
            return

        self.vob_save_folder = find_folder_path(file_path=file_path)

        # --------------

        self.vob_save_datas(file_path=file_path)

    def vob_save_settings(self):

        vob_settings = settings_read(file_name=vob_setting_file)

        # -----------------

        vob_settings["splitter"] = self.vob_save_splitter()

        # -----------------

        header = self.ui.vob_table.horizontalHeader()

        if header is not None:
            vob_settings["order"] = header.sortIndicatorOrder()
            vob_settings["order_col"] = header.sortIndicatorSection()

        # -----------------

        if self.vob_save_folder != "":
            vob_settings["save"] = self.vob_save_folder

        # -----------------

        vob_settings["filter"] = self.ui.search_filter_combo.currentIndex()

        # -----------------

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                vob_settings["height"] = screen.height()
                vob_settings["width"] = screen.width()
                vob_settings["ismaximized_on"] = True

                settings_save(file_name=vob_setting_file, config_datas=vob_settings)
                return

        vob_settings["height"] = self.size().height()
        vob_settings["width"] = self.size().width()
        vob_settings["ismaximized_on"] = False

        settings_save(file_name=vob_setting_file, config_datas=vob_settings)

    def vob_save_splitter(self) -> int:

        splitter_sizes = self.ui.splitter.sizes()

        if not isinstance(splitter_sizes, list):
            print(f"vob -- VobWidget -- vob_save_splitter -- not isinstance(splitter_sizes, list)")
            return vob_setting_datas.get("splitter", 75)

        if len(splitter_sizes) != 2:
            print(f"vob -- VobWidget -- vob_save_splitter -- len(splitter_sizes) != 2")
            return vob_setting_datas.get("splitter", 75)

        splitter_x1, splitter_x2 = splitter_sizes

        splitter_size = splitter_x1 + splitter_x2

        try:
            splitter_ratio = splitter_x1 * 100 / splitter_size
        except Exception as error:
            print(f"vob -- VobWidget -- vob_save_splitter -- error : {error}")
            return vob_setting_datas.get("splitter", 75)

        splitter_ratio = round(splitter_ratio)

        return splitter_ratio

    def vob_save_datas(self, file_path: str):

        if not isinstance(self.vob_file_obj, VobFileData):
            print(f"vob -- VobWidget -- vob_save_datas -- not isinstance(self.vob_file_obj, VobFileData)")
            return False

        if not make_backup(chemin_dossier=self.vob_file_obj.folder_path,
                           fichier=self.vob_file_obj.file_name,
                           extension=self.vob_file_obj.extension,
                           dossier_sauvegarde=f"{self.vob_file_obj.folder_path}Backup\\",
                           nouveau=False):
            print(f"vob -- VobWidget -- vob_save_datas -- not make_backup")
            return False

        row_count = self.vob_model.rowCount()

        datas = list()

        for row_index in range(row_count):

            # ------------
            # Trade
            # ------------

            trade_value = self.vob_get_data(row_index=row_index, column_index=col_vob_trade, model=self.vob_model)

            if not isinstance(trade_value, str):
                print(f"vob -- VobWidget -- vob_save_datas -- not isinstance(trade_value, str)")
                continue

            trade_index = self.vob_get_index(value=trade_value)

            if trade_index == "-1":
                trade_index = " -1"

            # ------------
            # object
            # ------------

            object_value = self.vob_get_data(row_index=row_index, column_index=col_vob_object, model=self.vob_model)

            if not isinstance(object_value, str):
                print(f"vob -- VobWidget -- vob_save_datas -- not isinstance(object_value, str)")
                continue

            object_index = self.vob_get_index(value=object_value)

            if object_index == "-1":
                object_index = "  -1"

            # ------------
            # unit
            # ------------

            unit_value = self.vob_get_data(row_index=row_index, column_index=col_vob_unit, model=self.vob_model)

            if not isinstance(unit_value, str):
                print(f"vob -- VobWidget -- vob_save_datas -- not isinstance(unit_value, str)")
                continue

            unit_index = self.vob_get_index(value=unit_value)

            # ------------
            # method
            # ------------

            method_value = self.vob_get_data(row_index=row_index, column_index=col_vob_method, model=self.vob_model)

            if not isinstance(method_value, str):
                print(f"vob -- VobWidget -- vob_save_datas -- not isinstance(method_value, str)")
                continue

            method_index = self.vob_get_index(value=method_value)

            # ------------
            # formula
            # ------------

            formula_value = self.vob_get_data(row_index=row_index, column_index=col_vob_formula, model=self.vob_model)

            if not isinstance(formula_value, str):
                print(f"vob -- VobWidget -- vob_save_datas -- not isinstance(formula_value, str)")
                continue

            formula_value = formula_value.strip()

            # ------------
            # comment
            # ------------

            comment_value = self.vob_get_data(row_index=row_index, column_index=col_vob_comment, model=self.vob_model)

            if not isinstance(comment_value, str):
                print(f"vob -- VobWidget -- vob_save_datas -- not isinstance(comment_value, str)")
                continue

            comment_value = comment_value.strip()

            # ------------

            datas.append([trade_index, object_index, unit_index, method_index, formula_value, comment_value])

        # ------------
        # Write file
        # ------------

        try:
            sorted_data = sorted(datas, key=lambda row: tuple(row[:3]))

            date_actuelle = datetime.now()
            date_formatee = date_actuelle.strftime("%d-%m-%Y - %H:%M:%S")

            module_txt = self.tr("listes, rapports, définition des quantités")
            title_txt = self.tr("Définition des quantités conforme au norme VOB")

            begin_text = ("//COMPANY=NEMETSCHEK\n"
                          "//PRODUCT=ALLPLAN\n"
                          f"//MODULE={module_txt}\n"
                          f"//TITLE={title_txt}\n"
                          f"//VERSION={date_formatee}\n"
                          f"//COUNTRY={self.vob_file_obj.country.upper()}\n"
                          f"//LANGUAGE={self.vob_file_obj.language.upper()}\n"
                          "//description:\n"

                          f"//1. -> {self.ui.trade_title.text()}\n"

                          f"//2. -> {self.ui.object_title.text()} (-1 == {self.defaut_text}))\n"

                          f"//3. -> {self.ui.unit_title.text()} "
                          f"(0 = m3 / 1 = m2 / 2 = m / 5 = {self.unit_dict['05']} / -1 = {self.defaut_text})\n"

                          f"//4. -> {self.ui.method_title.text()} ("
                          f"-1={self.defaut_text}), "
                          f"1={self.method_dict['01']}, "
                          f"2={self.method_dict['02']}, "
                          f"3={self.method_dict['03']}, "
                          f"4={self.method_dict['04']}, "
                          f"5={self.method_dict['05']}, "
                          f"6={self.method_dict['06']})\n"

                          f"//5. -> {self.ui.formula_title.text()}\n"

                          f"//6. -> {self.ui.comment_title.text()}\n")

            with open(file_path, "w", encoding="cp1252") as file:

                file.write(begin_text)

                trade_index_current = ""

                for data in sorted_data:

                    if len(data) != col_vob_count:
                        print(f"vob -- VobWidget -- vob_save_datas -- len(data) != col_vob_count")
                        continue

                    # ------------------

                    trade_index, object_index, unit_index, method_index, formula_value, comment_value = data

                    # ------------------

                    if trade_index != trade_index_current:
                        trade_name = self.trade_dict.get(trade_index.strip(), "")

                        trade_index_current = trade_index

                        file.write("// ================================================================\n"
                                   f"// {trade_name}\n"
                                   "// ================================================================\n")

                    # ------------------

                    line_text = f"#{trade_index}#{object_index}#{unit_index}#{method_index}#{formula_value};"

                    char_count = len(line_text)

                    tab_needed = 50 - char_count

                    line_text += f"{' ' * tab_needed}//{comment_value}\n"

                    # ------------------

                    file.write(line_text)

        except Exception as error:
            print(f"vob -- VobWidget -- vob_save_datas -- error : {error}")
            return False

        if file_path == self.vob_file_obj.file_path:
            self.vob_file_obj.refresh_last_change()
            self.vob_load_window_title()
            self.change_made = False

        return True

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        self.vob_save_settings()

        if not self.vob_save_ask():
            event.ignore()
            return

        super().closeEvent(event)

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

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

    def eventFilter(self, obj: QWidget, event: QEvent):

        if event.type() == QEvent.FocusOut:

            if obj == self.ui.trade_combo:
                self.vob_trade_changed()
                return super().eventFilter(obj, event)

            if obj == self.ui.object_combo:
                self.vob_object_changed()
                return super().eventFilter(obj, event)

            if obj == self.ui.unit_combo:
                self.vob_unit_changed()
                return super().eventFilter(obj, event)

            if obj == self.ui.method_combo:
                self.vob_method_changed()
                return super().eventFilter(obj, event)

            if obj == self.ui.value_attrib:
                self.vob_formula_finished()
                return super().eventFilter(obj, event)

            if obj == self.ui.comment_line:
                self.vob_comment_changed()
                return super().eventFilter(obj, event)

        elif isinstance(obj, QComboBox):

            if obj.view().isVisible():
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:

                if not obj.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            # noinspection PyUnresolvedReferences
            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
