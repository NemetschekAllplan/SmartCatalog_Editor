#!/usr/bin/python3
# -*- coding: utf-8 -*
import ctypes
import locale
import os
import re
import sys
import winreg
from ctypes.wintypes import MAX_PATH

from PyQt5.Qt import *

# ---------------------------------------

debug = False

special_version = False
help_mode = False
debug_tooltips = False

# ---------------------------------------

if special_version:
    application_version = "2025.0.2.100"
else:
    application_version = "2026.0.0.400"

application_name = "Allplan - SmartCatalog"
application_title = "Allplan - SmartCatalog Editor"

# ---------------------------------------


def find_app_path():
    """
    Recherche le chemin de l'application
    :return: chemin de l'application
    :rtype: str
    """

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)

        if not application_path.endswith("\\"):
            application_path += "\\"

    elif __file__:
        application_path = os.path.dirname(__file__)

        if not application_path.endswith("\\"):
            application_path += "\\"

    else:
        application_path = f"C:\\Program Files (x86)\\Allplan - SmartCatalog\\"

    application_path.replace("/", "\\")

    return application_path


# --------------------------------------------------------------

def get_documents_path():
    try:
        my_docs = os.path.expanduser(f'~\\Documents\\')

        if not isinstance(my_docs, str):
            return get_documents_path_1()

        nemetchek_folder = f"{my_docs}Nemetschek\\Allplan\\"

        if os.path.exists(nemetchek_folder):
            return my_docs

    except Exception:
        pass

    return get_documents_path_1()


def get_documents_path_1():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders') as key:

            my_docs, _ = winreg.QueryValueEx(key, 'Personal')

        my_docs = os.path.expandvars(my_docs)

        if not isinstance(my_docs, str):
            return get_documents_path_2()

        if not my_docs.endswith("\\"):
            my_docs += "\\"

        nemetchek_folder = f"{my_docs}Nemetschek\\Allplan\\"

        if os.path.exists(nemetchek_folder):
            return my_docs

    except Exception:
        pass

    return get_documents_path_2()


def get_documents_path_2() -> str:
    try:
        buf = ctypes.create_unicode_buffer(MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 1, buf)
        my_docs = buf.value

        if not isinstance(my_docs, str):
            return get_documents_path_3()

        if not my_docs.endswith("\\"):
            my_docs += "\\"

        nemetchek_folder = f"{my_docs}Nemetschek\\Allplan\\"

        if os.path.exists(nemetchek_folder):
            return my_docs

    except Exception:
        pass

    return get_documents_path_3()


def get_documents_path_3() -> str:
    try:
        my_docs = os.getenv('USERPROFILE')

        if not isinstance(my_docs, str):
            print(f"main_datas -- get_documents_path_3 -- not isinstance(my_docs, str)")
            return ""

        if not my_docs.endswith("\\"):
            my_docs += "\\"

        my_docs += "Documents\\"

        nemetchek_folder = f"{my_docs}Nemetschek\\Allplan\\"

        if os.path.exists(nemetchek_folder):
            return my_docs

    except Exception:
        pass

    return ""


# --------------------------------------------------------------

def get_asc_user_path(allplan_docs_path: str) -> str:
    if allplan_docs_path == "":
        allplan_docs_path = os.path.expanduser(f'~\\Documents\\')

    else:

        if not os.path.exists(allplan_docs_path):
            allplan_docs_path = os.path.expanduser(f'~\\Documents\\')

    if not os.path.exists(allplan_docs_path):
        return ""

    nemetchek_folder = f"{allplan_docs_path}Nemetschek\\Allplan\\"

    if not os.path.exists(nemetchek_folder):
        return ""

    asc_user_folder = f"{nemetchek_folder}SmartCatalog\\"

    if not os.path.exists(asc_user_folder):

        try:
            os.mkdir(asc_user_folder)

        except Exception as error:
            print(f"main_datas -- get_asc_user_path -- error : {error}")
            return ""

    return asc_user_folder


def get_asc_settings_path(asc_user_folder: str):
    if asc_user_folder == "":
        print(f"main_datas -- get_asc_settings_path -- asc_user_path is empty")
        return ""

    asc_settings_folder = f"{asc_user_folder}settings\\"

    if not os.path.exists(asc_settings_folder):
        try:
            os.mkdir(asc_settings_folder)

        except Exception as error:
            print(f"main_datas -- get_asc_settings_path -- error : {error}")
            return ""

    return asc_settings_folder


def get_asc_export_path(asc_user_folder: str):
    if asc_user_folder == "":
        print(f"main_datas -- get_asc_export_path -- asc_user_path is empty")
        return ""

    asc_export_folder = f"{asc_user_folder}export\\"

    if not os.path.exists(asc_export_folder):
        try:
            os.mkdir(asc_export_folder)

        except Exception as error:
            print(f"main_datas -- get_asc_export_path -- error : {error}")
            return ""

    return asc_export_folder


asc_folder_path = find_app_path()

if asc_folder_path == "C:\\Stockage\\GIT\\GitHub\\smartest2\\":
    asc_exe_path = f"C:\\Program Files (x86)\\Allplan - Smart-Catalogue\\Allplan - Smart-Catalogue.exe"

else:

    if special_version:
        asc_exe_path = f"{asc_folder_path}Allplan - Smart-Catalogue.exe"

    else:
        asc_exe_path = f"{asc_folder_path}Allplan - SmartCatalog.exe"

icons_path = f"{asc_folder_path}icons\\"

asc_old_path = "C:\\Program Files (x86)\\Allplan - Smart-Catalogue\\"
icons_old_path = f"{asc_folder_path}icones ASC\\"

allplan_docs = get_documents_path()  # C:\Users\jmauger\Documents\ where is Nemetschek\Allplan\2025\Usr\Local

asc_user_path = get_asc_user_path(allplan_docs_path=allplan_docs)

asc_settings_path = get_asc_settings_path(asc_user_folder=asc_user_path)
asc_export_path = get_asc_export_path(asc_user_folder=asc_user_path)

# ---------------------------------------

first_allplan_version = "2022"
first_allplan_version_int = 2022

# ---------------- Folder ----------------

# todo traduction

folder_code = "Folder"
folder_code_list = ["dossier", "folder", "ordner", "cartella", "carpetas", "mapa", "director", "Папка".lower(),
                    "složka"]
folder_icon = ":/Images/folder.png"

# ---------------- Material ----------------

# todo traduction

material_code = "Material"
material_code_list = ["ouvrage", "material", "arbeiten", "lavoro", "tipologia", "trabajar", "mатериал", "materiál"]
material_icon = ":/Images/material.png"
bold_font = QStandardItem().font()
bold_font.setBold(True)

# ---------------- Component ----------------

# todo traduction

component_code = "Component"
component_code_list = ["composant", "component", "komponente", "articolo", "articoli" "componente",
                       "komponenta", "element", "kомпонент", "element"]
component_icon = ":/Images/component.png"

italic_font = QStandardItem().font()
italic_font.setItalic(True)

# ---------------- Link ----------------

# todo traduction

link_code = "Link"
link_code_list = ["link", "lien", "verknüpfung", "collegamento", "enlace", "cсылка", "odkaz", "povezava"]
link_icon = ":/Images/link.png"

# ---------------- Attribute ----------------

# todo traduction

attribute_code = "Attribute"
attribute_code_list = ["attribut", "attribute", "attributo", "attributi", "atributo", "atribut", "aтрибут"]
attribute_icon = ":/Images/attribute.png"

info_code = "Info"

if debug:
    pattern_filter = ""
else:
    pattern_filter = f"^({folder_code}|{material_code}|{component_code}|{link_code})"

# ---------------------------------------
# Icons
# ---------------------------------------

# --------------------------------------- A --------

add_icon = ":/Images/add.svg"
allplan_icon = ":/Images/allplan.svg"
attribute_add_icon = ":/Images/attribute_add.png"
attribute_add_auto_icon = ":/Images/attribute_add_auto.png"
attribute_model_show_icon = ":/Images/attribute_model_show.svg"
attribute_editable_icon = ":/Images/attribute_editable.svg"
attribute_model_save_icon = ":/Images/attribute_model_save.svg"
asc_icon = ":/Images/asc.svg"

# --------------------------------------- B --------

browser_icon = ":/Images/browse.svg"

# --------------------------------------- C --------

catalog_icon = ":/Images/catalog.svg"
collapse_all_icon = ":/Images/collapse_all.png"
convert_bdd_icon = ":/Images/convert_bdd.svg"
copy_icon = ":/Images/copy.svg"
cut_icon = f":/Images/cut.svg"

# --------------------------------------- D --------

delete_icon = ":/Images/delete.svg"
description_off_icon = ":/Images/description_off.svg"
description_on_icon = ":/Images/description_on.svg"
detail_hide_icon = ":/Images/detail_hide.svg"
detail_show_icon = ":/Images/detail_show.svg"

# --------------------------------------- E --------

empty_icon = ":/Images/empty.png"
error_icon = ":/Images/error.png"

excel_icon = ":/Images/excel.svg"

expand_all_icon = ":/Images/expand_all.png"

exit_icon = ":/Images/exit.png"

# --------------------------------------- External --------

external_bdd_acca_icon = ":/Images/external_bdd_acca.png"
external_bdd_option_icon = ":/Images/external_bdd_option.svg"
external_bdd_all_icon = ":/Images/external_bdd_all.png"
external_bdd_aj_soft_icon = ":/Images/external_bdd_aj_soft.png"
external_bdd_allmetre_icon = ":/Images/external_bdd_allmetre.png"
external_bdd_bcm_icon = ":/Images/external_bdd_bcm.png"
external_bdd_bcm_c_icon = ":/Images/external_bdd_bcm_c.png"
external_bdd_capmi_icon = ":/Images/external_bdd_capmi.png"
external_bdd_component_url_icon = ":/Images/external_bdd_component_url.png"
external_bdd_gimi_icon = ":/Images/external_bdd_gimi.png"
external_bdd_material_url_icon = ":/Images/external_bdd_material_url.png"
external_bdd_nevaris_icon = ":/Images/external_bdd_nevaris.png"
external_bdd_progemi_icon = ":/Images/external_bdd_progemi.png"
external_bdd_show_icon = ":/Images/external_bdd_show.svg"
external_bdd_synermi_icon = ":/Images/external_bdd_synermi.png"
external_bdd_ts_icon = ":/Images/external_bdd_ts.png"
external_bdd_mxdb_icon = ":/Images/external_bdd_mxdb.png"
external_bdd_frilo = ":/Images/external_bdd_frilo.png"
external_bdd_bimplus_icon = ":/Images/external_bdd_bimplus.png"

# --------------------------------------- F --------

formula_icon = ":/Images/formula.svg"

function_icon = ":/Images/function.png"

formula_favorite_icon = ":/Images/formula_favorite.svg"

favorite_open_icon = ":/Images/favorite_open.svg"
favorite_save_icon = ":/Images/favorite_save.svg"

# --------------------------------------- H --------

help_icon = ":/Images/help.png"

hierarchy_show_item_icon = ":/Images/hierarchy_show_item.svg"

# --------------------------------------- I --------

information_icon = ":/Images/information.svg"

# --------------------------------------- L --------

layer_icon = ":/Images/layer.png"

lock_icon = ":/Images/lock.svg"

# --------------------------------------- M --------

merge_icon = ":/Images/merge.png"
move_down_icon = ":/Images/move_down.svg"
move_up_icon = ":/Images/move_up.svg"

# --------------------------------------- N --------

none_icon = ":/Images/none.svg"

# --------------------------------------- O --------

off_icon = f":/Images/off.svg"
on_icon = f":/Images/on.svg"
open_icon = ":/Images/open.svg"
open_text_editor_icon = ":/Images/open_text_editor.svg"
open_catalog_icon = ":/Images/open_catalog.svg"
options_icon = ":/Images/options.svg"
outlook_icon = ":/Images/email.png"

order_az = ":/Images/az.png"
order_za = ":/Images/za.png"
order_19 = ":/Images/19.png"
order_91 = ":/Images/91.png"

# --------------------------------------- P --------

paste_icon = f":/Images/paste.svg"
pdf_icon = ":/Images/pdf.png"

# --------------------------------------- R --------

refresh_icon = ":/Images/refresh.png"
recent_icon = ":/Images/recent.svg"
rename_icon = ":/Images/rename.svg"
reset_icon = ":/Images/reset.svg"

# --------------------------------------- S --------

save_icon = ":/Images/save.svg"
save_as_icon = ":/Images/save_as.svg"
select_all_icon = ":/Images/select_all.svg"
select_none_icon = ":/Images/select_none.svg"
search_icon = ":/Images/search.svg"
search_clear_icon = ":/Images/search_clear.svg"
search_replace_icon = ":/Images/search_replace.svg"
style_icon = ":/Images/style"

# --------------------------------------- T --------

text_copy_icon = ":/Images/text_copy.svg"
tool_icon = ":/Images/tool.svg"

# --------------------------------------- U --------

update_cat_icon = ":/Images/update_cat.svg"
update_app_icon = ":/Images/update.png"

# --------------------------------------- V --------

valid_icon = ":/Images/valid.svg"

# --------------------------------------- W --------

warning_icon = ":/Images/warning.svg"

windows_close_hover_icon = ":/Images/windows_close_hover.png"

# ---------------------------------------

icons_dict = dict()


def get_icon(icon_path: str) -> QIcon:
    # return None

    if icon_path in icons_dict:
        return icons_dict[icon_path]

    icon = QIcon(icon_path)

    icons_dict[icon_path] = icon

    return icon


# todo traduction
dict_langues = {"FR": "_fr.xml",
                "EN": "_en.xml",
                "DE": "_de.xml",
                "IT": "_it.xml",
                "ES": "_es.xml",
                "HR": "_hr.xml",
                "RO": "_ro.xml",
                "RU": "_ru.xml",
                "CS": "_cs.xml",
                "SL": "_sl.xml",
                "SK": "_sk.xml"}

# --------------------------------------- FLAGS --------

# todo traduction
language_title = {"CS": "Čeština",
                  "DE": "Deutsch",
                  "EN": "English",
                  "ES": "Español",
                  "FR": "Français",
                  "HR": "Hrvatski",
                  "IT": "Italiano",
                  "RO": "Română",
                  "RU": "Русский",
                  "SK": "Slovenčina",
                  "SL": "Slovenščina"}

# todo tranduction C:\ProgramData\Nemetschek\Allplan\2024\Etc\SPR_ZUO.DAT
language_code = {"FR": "1036",
                 "EN": "1033",
                 "DE": "1031",
                 "IT": "1040",
                 "ES": "1034",
                 "HR": "1050",
                 "RO": "1048",
                 "RU": "1049",
                 "CZ": "1029",
                 "SL": "1060",
                 "SK": "64539"}

# todo tranduction
language_extension_3 = {"FR": "fra",
                        "EN": "eng",
                        "DE": "deu",
                        "IT": "ita",
                        "ES": "spa",
                        "HR": "hrv",
                        "RO": "rum",
                        "RU": "rus",
                        "CS": "tch",
                        "SL": "svn",
                        "SK": "slk"}

# todo tranduction
language_icons = {"fra": "FR",
                  "eng": "EN",
                  "deu": "DE",
                  "ita": "IT",
                  "spa": "ES",
                  "hrv": "HR",
                  "rum": "RO",
                  "rus": "RU",
                  "tch": "CS",
                  "svn": "SL",
                  "slk": "SK",
                  "swi": "CH",
                  "aus": "AU",
                  "can": "CA"}
# ---------------------------------------
#  ATTRIBUTS XML ALLPLAN
# ---------------------------------------


code_xml_number = "Ifnr"
code_xml_text = "Text"
code_xml_value = "Value"
code_xml_datatype = "Datatype"
code_xml_group = "Group"
code_xml_option = "Option"
code_xml_unit = "Unit"
code_xml_modify = "Modify"
code_xml_visible = "Visible"
code_xml_enumeration = "Enumeration"
code_xml_uid = "Uid"
code_xml_min = "MinValue"
code_xml_max = "MaxValue"

# ---------------------------------------
#  ATTRIBUTS MODEL ALLPLAN
# ---------------------------------------

col_attr_number = 0
col_attr_name = 1
col_attr_datatype = 2
col_attr_group = 3

col_enum_index = 0
col_enum_valeur = 1

code_attr_str = "Texte"
code_attr_int = "Nombre entier"
code_attr_dbl = "Nombre décimal"
code_attr_date = "Date"
code_attr_chk = "CheckBox"

code_attr_combo_str_edit = "ComboBox éditable - Texte"
code_attr_combo_float_edit = "ComboBox éditable - Nombre décimal"
code_attr_combo_int_edit = "ComboBox éditable - Nombre entier"

code_attr_combo_int = "ComboBox non modifiable - Nombre entier"

code_attr_formule_str = "Texte - Formule"
code_attr_formule_int = "Nombre entier - Formule"
code_attr_formule_float = "Nombre décimal - Formule"

# ---------------------------------------
#  MODEL CATALOGUE
# ---------------------------------------

col_cat_value = 0
col_cat_desc = 1
col_cat_index = 1
col_cat_number = 2
col_cat_count = 3

# ---------------------------------------
#  CATALOGUE - MODEL - TYPE
# ---------------------------------------

user_data_number = Qt.UserRole + 2
type_nom = "Nom"
type_lien = "Lien"
type_code = "Code"
type_ligne = "Ligne"
type_ligne_str = "Ligne_str"
type_formule = "Formule"
type_combo = "Combo"
type_checkbox = "Checkbox"
type_date = "Date"
type_texture = "Texture"
type_layer = "Layer"
type_fill = "Remplissage"
type_room = "Piece"
type_unknown = "Unknown"
type_title = "title"

# ---------------------------------------
#  CATALOGUE - SAUVEGARDE
# ---------------------------------------

liste_attributs_with_no_val_no_save = ["207", "252", "111", "336", "346", "345", "347"]

# ---------------------------------------
#  CATALOGUE - ATTRIBUTE DEFAULT
# ---------------------------------------


class AttributeDefault:

    def __init__(self):
        super().__init__()

        self.base = "83"

        self.current = "83"

        self.valid_list = ["83", "507", "508", "570", "571", "574", "575", ""]

        self.valid_count = len(self.valid_list)

    def set_current(self, number: str):

        self.current = self.check_number(number=number)

    def check_number(self, number: str) -> str:

        if not isinstance(number, str):
            print("main_datas -- AttributeDefault -- check_value -- not isinstance(value, int)")
            return self.base

        number = number.strip()

        if number in self.valid_list:
            return number

        for number in self.valid_list:

            if number.startswith(number):
                return number

        return self.base

    def get_value(self, index: int) -> str:

        if not isinstance(index, int):
            print("main_datas -- AttributeDefault -- get_value -- not isinstance(index, int)")
            return self.base

        if index < 0:
            print("main_datas -- AttributeDefault -- get_value -- index < 0")
            return self.base

        if index >= self.valid_count:
            print("main_datas -- AttributeDefault -- get_value -- index >= self.valid_count")
            return self.base

        return self.valid_list[index]


attribut_default_obj = AttributeDefault()

attribute_default_base = "83"
attribute_name_default_base = "code"

attribute_default_list = ["83", "507", "508", "570", "571", "574", "575", ""]

# ---------------------------------------
#  ATTRIBUTS GROUPES
# ---------------------------------------

attribut_val_defaut_defaut = {"207": "", "110": "100", "120": "1", "202": "1", "209": "0"}

attribute_val_default_layer = {"141": "0", "349": "0", "346": "1", "345": "1", "347": "1"}
attribute_val_default_layer_first = "141"
attribute_val_default_layer_last = "347"

attribute_val_default_fill = {"118": "0", "111": "0", "252": "-1", "336": ""}
attribute_val_default_fill_first = "118"
attribute_val_default_fill_last = "336"

attribute_val_default_room = {"231": "R",
                              "235": "SU",
                              "232": "N",
                              "266": "1,000", "233": "0", "264": "1,000"}

attribute_val_default_room_first = "231"
attribute_val_default_room_last = "264"

liste_attributs_ordre = ["207"]
liste_attributs_ordre.extend(list(attribute_val_default_layer))
liste_attributs_ordre.extend(list(attribute_val_default_fill))
liste_attributs_ordre.extend(list(attribute_val_default_room))

formula_list_attributes = ["76", "96", "180", "267"]

formula_piece_dict = {"MT_Boden(": "Obj_Floor(",
                      'MT_Decke(': 'Obj_Ceiling(',
                      'MT_Seite(': 'Obj_VSurface(',
                      'MT_Leiste(': 'Obj_Baseboard(',
                      'MT_Material(': 'Obj_Material(',
                      "MT_Fenster(": "Obj_WindowOpening(",
                      "MT_Fenstertuer(": "Obj_FrenchWindowOpening(",
                      "MT_Dachfenster(": "Obj_RoofWindowOpening(",
                      "MT_Tuer(": "Obj_DoorOpening(",
                      "MT_Nische(": "Obj_Niche(",
                      "MT_Wand(": "Obj_Wall(",
                      "MT_Raum(": "Obj_Room(",
                      "MT_Stuetze(": "Obj_Column(",
                      "MT_Fenstermakro(": "Obj_WindowSmartSymbol(",
                      "MT_Tuermakro(": "Obj_DoorSmartSymbol(",
                      "MT_RoofWindow(": "Obj_RoofWindow(",
                      "MT_Window(": "Obj_Window(",
                      "MT_Door(": "Obj_Door(",
                      "MT_Roof(": "Obj_Roof(",
                      "MT_RoofLayer(": "Obj_RoofLayer(",
                      "VOB_Fläche": "@81@"}

formula_piece_pattern = '|'.join(map(re.escape, formula_piece_dict.keys()))

fonction_list = ['_IF_', '_ELSE_', '_ELSE__IF_',
                 'ABS', 'SQRT', 'SQR', 'PI', 'LN', 'LOG', 'RCP', 'EXP', 'SGN',
                 'SIN', 'COS', 'TAN', 'ASIN', 'ACOS', 'ATAN', 'SINH', 'COSH', 'TANH',
                 'NINT', 'INT', 'CEIL',
                 'GRA', 'RAD', 'GON', 'RAG', 'AVG', 'MIN', 'MAX',
                 'FLAG', 'ROUND', 'ELE', 'VALUE', 'MID', 'FORMAT',
                 'PARENT', 'CHILD', 'GROUP',
                 'MT_Boden', 'Obj_Floor',
                 'MT_Decke', 'Obj_Ceiling',
                 'MT_Seite', 'Obj_VSurface',
                 'MT_Leiste', 'Obj_Baseboard',
                 'MT_Material', 'Obj_Material',
                 'Obj_WindowOpening', 'Obj_FrenchWindowOpening', 'Obj_Roof_Opening', 'Obj_DoorOpening',
                 'Obj_Niche', 'Obj_Wall', 'Obj_Room', 'Obj_Column', 'Obj_WindowSmartSymbol',
                 'Obj_DoorSmartSymbol', 'Obj_RoofWindow', 'Obj_Window', 'Obj_Door', 'Obj_Roof',
                 'Obj_RoofLayer', 'TOPOLOGY', 'PARENTPRECAST', 'IMPRRE', 'FIXTURECOUNT',
                 "@OBJ@", "@VOB@", "QT",
                 "p:", "v:", "x:",
                 "SOMME", "SUM", "SUMME", "TOTALE", "TOTAL", "Group", "Openingmacrocount"
                 ]

# ---------------------------------------
#  UNITE
# ---------------------------------------

material_upper_list = list()
material_list = list()
link_list = list()
material_with_link_list = list()

# ---------------------------------------
#  UNITE
# ---------------------------------------

dict_formules_by_unite = ["@223@", "@229@", "@220@", "1", "1"]

# ---------------------------------------
#  HTML
# ---------------------------------------

dict_html = {'&': "&amp;",
             ">": "&gt;",
             "<": "&lt;",
             '"': "&quot;",
             "'": "&apos;",
             "©": "&copy;",
             "®": "&reg;",
             "€": "&euro;"}

# ---------------------------------------
#  ALLPLAN BCM
# ---------------------------------------

# todo traduction

liste_obj = ["@76@", "Filtre_d_objets", "Object filter", "Objektfilter", "Filtro_oggetto", "Filtro de objetos",
             "Filtar objekata", "Filtru_obiecte", "Фильтр_объекта", "Filtr objektů", "Filter objektov"]

liste_mat = ["@96@", "Matériau_dyn", "Dyn_material", "Dyn_Materiale", "Material_Dyn",
             "Dyn_materijal", "Dyn_Material", "Дин_материал", "Dyn_materiál", "Din_material"]

liste_qte = ["@215@", "Quantité", "Piece", "Stück", "Pezzi", "Komad", "Bucati", "штук", "Kusy", "Kosov"]

liste_for = ["@267@", "Formule_de_métré", "Quantity_formula", "Mengenformel", "Formula_quantità",
             "Fórmula_medición", "Formula_količine", "Formula_cantitati", "Расчетная_формула", "Vzorec_výměry",
             "Formula količin"]

# ---------------------------------------
#  FORMULE
# ---------------------------------------

liste_caracteres_fin = ["=", "+", "-", "*", "/", ">", "<", "&", "|", ",", ";", "("]

# ---------------------------------------
#  FORMULE - FAVORIS
# ---------------------------------------

fichier_favoris_formule = "favoris_formule_config"

col_favoris_formule_titre = 0
col_favoris_formule_formule = 1
col_favoris_formule_famille = 2

user_data_type = Qt.UserRole + 1
user_guid = Qt.UserRole + 2
user_formule_ok = Qt.UserRole + 3
user_unknown = Qt.UserRole + 4

# ---------------------------------------
#  BIBLE
# ---------------------------------------

bdd_type_xml = "Allplan - SmartCatalog"
bdd_type_fav = "Allplan - Favorites"
bdd_type_kukat = "Allplan - Kukat"

bdd_type_bcm = "Allplan - BCM"
bdd_type_bcm_c = "Allplan - BCM - Component"

bdd_type_nevaris = "Nevaris"
bdd_type_nevaris_xlsx = "Nevaris - Excel"

bdd_type_excel = "Excel"
bdd_type_csv = "Csv"

bdd_type_gimi = "Euriciel - Gimi"
bdd_type_allmetre_e = "Euriciel - Allmétré"

bdd_type_allmetre_a = "Ajsoft - Allmétré"

bdd_type_synermi = "Synermi"
bdd_type_capmi = "Capmi"
bdd_type_progemi = "Progemi"

bdd_type_mxdb = "SQL"

bdd_type_xpwe = "XPWE"

bdd_type_team_system_xml = "teamsystem_xml"
bdd_type_team_system_xlsx = "teamsystem_xlsx"

bdd_type_extern = "Extern"

# -------------

categories_bcm = [bdd_type_bcm, bdd_type_bcm_c]

categories_excel = [bdd_type_excel, bdd_type_csv]

categories_nevaris = [bdd_type_nevaris, bdd_type_nevaris_xlsx]

categories_extern = [bdd_type_synermi, bdd_type_capmi, bdd_type_progemi, bdd_type_extern,
                     bdd_type_gimi, bdd_type_allmetre_e, bdd_type_allmetre_a,
                     bdd_type_mxdb, bdd_type_xpwe, bdd_type_team_system_xml, bdd_type_team_system_xlsx]

# -------------

openable_file_extension = (".xml", ".KAT", '.sgsfnfx', '.rkfanfx', '.scfanfx', '.swefnfx', '.spafnfx', '.dhfanfx',
                           '.defanfx', '.ibtfnfx', '.sabfnfx', '.szafnfx', '.skbfnfx', '.gafanfx', '.srfanfx',
                           '.wafanfx', '.spffnfx', '.sspfnfx', '.rafanfx', '.bffanfx', '.sffanfx', '.lefanfx',
                           '.dffanfx', '.spofnfx', '.stfanfx', '.uzfanfx', '.pfufnfx', '.aufanfx', '.efufnfx',
                           '.sbafnfx', '.akfanfx', 'xlsx')

importable_file_extension = (".xml", ".dbf", ".apn", ".prj", ".xlsx", ".kat")

# ---------------------------------------
#  old
# ---------------------------------------


type_composant_url = "Base Composants - Url"
type_composant_chemin = "Base Composants - Chemin"
type_ouvrage_url = "Base Ouvrages - Url"
type_ouvrage_chemin = "Base Ouvrages - Chemin"

# ---------------------------------------
#  icones
# ---------------------------------------

bdd_icons_dict = {bdd_type_xml: catalog_icon,
                  bdd_type_fav: attribute_model_show_icon,

                  bdd_type_nevaris: external_bdd_nevaris_icon,
                  bdd_type_nevaris_xlsx: external_bdd_nevaris_icon,

                  bdd_type_bcm: external_bdd_bcm_icon,
                  bdd_type_bcm_c: external_bdd_bcm_c_icon,

                  bdd_type_kukat: allplan_icon,
                  bdd_type_excel: excel_icon,

                  bdd_type_gimi: external_bdd_gimi_icon,
                  bdd_type_allmetre_e: external_bdd_allmetre_icon,
                  bdd_type_allmetre_a: external_bdd_aj_soft_icon,
                  bdd_type_synermi: external_bdd_synermi_icon,
                  bdd_type_capmi: external_bdd_capmi_icon,
                  bdd_type_progemi: external_bdd_progemi_icon,

                  bdd_type_mxdb: external_bdd_mxdb_icon,

                  bdd_type_xpwe: external_bdd_acca_icon,

                  bdd_type_team_system_xlsx: external_bdd_ts_icon,
                  bdd_type_team_system_xml: external_bdd_ts_icon,

                  bdd_type_extern: external_bdd_show_icon}

# ---------------------------------------
#  SETTINGS
# ---------------------------------------

# ===================================================
#               Default Language
# ===================================================

if special_version:
    language_default = "FR"
else:
    language_default = "EN"

try:
    windows_language = locale.getdefaultlocale()[0]

    for language_ in language_code.keys():

        if language_ in windows_language.upper():
            language_default = language_
            break

except Exception:
    pass

# ===================================================
#                       APPLICATION
# ===================================================

app_setting_file = "app_setting"

app_setting_datas = {"actionbar_size": "2",
                     "attributes_order": 0,
                     "attributes_order_col": 0,
                     "attributes_order_custom": False,
                     "brackets_color_on": True,
                     "description_show": True,
                     "height": 875,
                     "ismaximized_on": False,
                     "language": language_default,
                     "message": "",

                     "search_recent": list(),

                     "path_catalog": "",

                     "path_catalog_apn": "",
                     "path_catalog_import": "",
                     "path_catalog_open": "",
                     "path_catalog_prj": "",
                     "path_catalog_save": "",
                     "path_message": "",

                     "path_icons": "",

                     "posx": 0,
                     "posy": 0,

                     "tab_index": 0,
                     "width": 1275}

app_setting_conv = {"brackets_color_on": "formule_couleur",
                    "description_show": "description",
                    "height": "Hauteur",
                    "ismaximized_on": "isMaximized",
                    "language": "Langue",

                    "path_catalog": "catalogue",

                    "path_catalog_apn": "chemin_apn_cat",
                    "path_catalog_import": "chemin_import_bdd",
                    "path_catalog_open": "chemin_ouvrir_catalogue",
                    "path_catalog_prj": "chemin_prj",

                    "path_icons": "chemin_icone",

                    "posx": "position_ecran_x",
                    "posy": "position_ecran_y",

                    "tab_index": "onglet",
                    "width": "Largeur"}

# ===================================================
#                       ATTRIBUTES
# ===================================================

attribute_setting_file = "attribute_setting"

attribute_setting_datas = {"height": 600,
                           "ismaximized_on": False,
                           "order": 0,
                           "order_col": 0,
                           "path_bitmap_area": "",
                           "path_export": "",
                           "path_import": "",
                           "path_surface": "",
                           "width": 800}

attribute_setting_conv = {"path_bitmap_area": "chemin_surface_image",
                          "path_import": "attribut_importer_favoris",
                          "path_surface": "chemin_texture"}

# ---------------------------------------

attribute_config_file = "attribute_config"

attribute_config_datas = {"material": ["110", "118", "120", "141", "202", "209", "335", "506", "684"],
                          "component": ["96", "120", "202", "209", "267"],
                          "formula": ["99", "220", "221", "222", "223", "229"]}

# ===================================================
#                       CAT LIST
# ===================================================

cat_list_file = "cat_open_list"
cat_list_datas = list()

recent_config_file = "recent_config"

recent_config_dict = {"etc": True,
                      "std": True,
                      "demo": True,
                      "other": True,
                      "2022": True,
                      "2023": True,
                      "2024": True,
                      "2025": True,
                      "2026": True}

# ===================================================
#                       FORMULA FAVORITES
# ===================================================

formula_fav_setting_file = "formula_fav_setting"

formula_fav_setting_datas = {"height": 600,
                             "ismaximized_on": False,
                             "formula_name": "",
                             "path_export": "",
                             "path_import": "",
                             "tab_index": 0,
                             "width": 800}

# ---------------------------------------

formula_fav_config_file = "formula_fav_config"

formula_fav_config_datas = {}

# ===================================================
#                       FORMULA
# ===================================================

formula_setting_file = "formula_setting"

formula_setting_datas = {"font_height": 13,
                         "height": 600,
                         "ismaximized_on": False,
                         "path_export": "",
                         "path_import": "",

                         "order": 0,
                         "order_col": 0,

                         "function_height": 500,
                         "function_ismaximized_on": False,
                         "function_order": 0,
                         "function_order_col": 0,
                         "function_select": "",
                         "function_width": 500,

                         "finishing_attribute_select": "209",
                         "finishing_layer_select": ["0"],
                         "finishing_select": 0,

                         "trade_height": 500,
                         "trade_ismaximized_on": False,
                         "trade_order": 0,
                         "trade_order_col": 0,
                         "trade_select": "",
                         "trade_width": 500,

                         "object_height": 500,
                         "object_ismaximized_on": False,
                         "object_order": 0,
                         "object_order_col": 0,
                         "object_select": "",
                         "object_width": 500,

                         "width": 800}

formula_setting_conv = {"height": "Hauteur_formule",
                        "ismaximized_on": "isMaximized_formule",
                        "width": "Largeur_formule"}

# ===================================================
#                       Help
# ===================================================

help_setting_file = "help_setting"

help_setting_datas = {"height": 800,
                      "ismaximized_on": False,
                      "current_article": "",
                      "width": 600}

# ===================================================
#                       LIBRARY
# ===================================================

library_setting_file = "library_setting"

library_setting_datas = {"category": 0,
                         "height": 600,
                         "ismaximized_on": False,
                         "order": 0,
                         "order_col": 1,
                         "path_alltop": "",
                         "path_bcm": "",
                         "path_cat": "",
                         "path_excel": "",
                         "path_favorites": "",
                         "path_gimi": "",
                         "path_kukat": "",
                         "path_open": "",
                         "tab_index": 0,
                         "title": "",
                         "width": 800}

library_setting_conv = {"path_alltop": "chemin_alltop",
                        "path_open": "chemin_ouvrir_bible",
                        "tab_index": "onglet_bible_ext"}

# ---------------------------------------

library_config_file = "library_config"

library_config_datas = {}

# ---------------------------------------

library_synchro_setting_file = "library_synchro_setting"

library_synchro_setting_datas = {"height": 600,
                                 "ismaximized_on": False,
                                 "path_import": "",
                                 "path_export": "",
                                 "creation": True,
                                 "width": 400}

# ---------------------------------------

library_synchro_config_file = "library_synchro_config"

library_synchro_config_datas = {folder_code: ["207"],
                                material_code: ["207"],
                                component_code: ["207"]}

# ===================================================
#                       MODEL
# ===================================================

model_setting_file = "model_setting"

model_setting_datas = {"height": 600,
                       "clipboard": list(),
                       "ismaximized_on": False,
                       "path_export": "",
                       "path_import": "",
                       "tab_index": 0,
                       "width": 800}

model_setting_conv = {"height": "Hauteur_options",
                      "ismaximized_on": "isMaximized_options",
                      "models": "models",
                      "path_export": "",
                      "path_import": "",
                      "tab_index": "onglet_option",
                      "width": "Largeur_options"}

# ---------------------------------------

model_config_file = "model_config"

model_config_datas = {"Material": {"icon": material_icon,
                                   "order": 0,
                                   "order_col": 0,
                                   "type": "material",
                                   "attributes": ["120", "202"]},

                      "Component": {"icon": component_icon,
                                    "order": 0,
                                    "order_col": 0,
                                    "type": "component",
                                    "attributes": ["120", "202", "267"]}}

# ===================================================
#                       NUMBER
# ===================================================

number_setting_file = "number_setting"

number_setting_datas = {"height": 500,
                        "ismaximized_on": False,
                        "width": 500,
                        "number": 1,
                        "description": True,
                        "separator": "|"}

# ===================================================
#                       REPLACE
# ===================================================

replace_setting_file = "replace_setting"

replace_setting_datas = {"height": 600,
                         "ismaximized_on": False,
                         "width": 450,
                         "replace_by": "",
                         "ele_type": material_code,
                         "attribute": "83",
                         "attributes_list": ["83", "207"]}

# ===================================================
#                       SEARCH
# ===================================================

search_setting_file = "search_setting"

search_setting_datas = {"attributes_list": [attribute_default_base, "207"],
                        "ele_type": [True, True, True, True],
                        "path_export": asc_export_path,
                        "path_import": asc_export_path,
                        "search_case": False,
                        "search_mode": 0,
                        "search_number": attribute_default_base,
                        "search_option": 0}

# ===================================================
#                       STRUCTURE
# ===================================================

structure_setting_file = "structure_setting"

structure_setting_datas = {"height": 600,
                           "ismaximized_on": False,
                           "width": 800}

# ===================================================
#                       Order
# ===================================================

order_setting_file = "order_setting"

order_setting_datas = {"height": 600,
                       "ismaximized_on": False,
                       "path_import": "",
                       "path_export": "",
                       "other": 0,
                       "width": 544}

# ---------------------------------------

order_config_file = "order_config"

order_config_datas = ["207", "120", "202", "209", "110",
                      attribute_val_default_fill_first,
                      attribute_val_default_layer_first,
                      attribute_val_default_room_first]

# ===================================================
#                       ROOM
# ===================================================
room_attributes_list = ["231", "235", "232", "266", "233", "264"]

room_config_file = "room_config"

aeration_index = 0
air_frais_index = 1
bain_index = 2
balcon_index = 3
bureau_index = 4
chauffage_index = 5
comble_index = 6
couloir_index = 7
cour_index = 8
debarras_index = 9
escalier_index = 10
hall_index = 11
loggias_index = 12
sejour_index = 13

# -------------------------------------

# todo traduction

unit_dict = {'FR': ['m³', 'm²', 'm', 'Qt', 'kg'],
             'EN': ['m³', 'm²', 'm', 'Pc', 'kg'],
             'DE': ['m³', 'm²', 'm', 'St', 'kg'],
             'IT': ['m³', 'm²', 'm', 'Pz', 'kg'],
             'ES': ['m³', 'm²', 'm', 'Pzs', 'kg'],
             'HR': ['m3', 'm2', 'm', 'Kom', 'kg'],
             'RO': ['m3', 'm2', 'm', 'Buc', 'kg'],
             'RU': ['м3', 'м2', 'м', 'Шт', 'кг'],
             'CS': ['m³', 'm²', 'm', 'Ks', 'kg'],
             'SL': ['m3', 'm2', 'm', 'Kos', 'kg'],
             'SK': ['m³', 'm²', 'm', 'Ks', 'kg']}

# todo traduction

translation_room = {"FR": ["Aération", "Air frais", "Bain", "Balcon", "Bureau", "Chauffage", "Comble", "Couloir",
                           "Cour", "Débarras", "Escalier", "Hall", "Loggia", "Séjour"],

                    "EN": ['Ventilation', 'Fresh air', 'Bath', 'Balcony', 'Office', 'Heating', 'Attic', 'Hall',
                           'Air well', 'Storage', 'Stair', 'Lobby', 'Loggia', 'Living'],

                    "DE": ['Lüftung', 'Frischluft', 'Bad', 'Balkon', 'Büro', 'Heizung', 'Dachboden', 'Flur',
                           'Lichthof', 'Abstell', 'Treppe', 'Halle', 'Loggia', 'Wohnen'],

                    "IT": ['Ventilazione', 'Aria fresca', 'Bagno', 'Balcone', 'Ufficio', 'Riscaldamento',
                           'Mansarda', 'Corridoio', 'Cortile', 'Soffitta', 'Scala', 'Atrio', 'Loggia', 'Stanza'],

                    "ES": ['Ventilación', 'Aire frío', 'Baño', 'Balcón', 'Estudio', 'Calefacción', 'Àtico',
                           'Pasillo', 'Patio interior', 'Deducción', 'Escalera', 'Vestíbulo', 'Loggia', 'Habitación'],

                    "HR": ['Ventilacija', 'Zvježi zrak', 'Kupaonica', 'Balkon', 'Ured', 'Grijanje', 'Potkrovlje',
                           'Hodnik', 'Izvor zraka', 'Spremište', 'Stubište', 'Čekaonica', 'Loggia', 'Dnevna'],

                    "RO": ['Ventilatie', 'Sera', 'Baie', 'Balcon', 'Birou', 'Incalzire', 'Atic', 'Hol', 'Curte',
                           'Depozit', 'Scara', 'Lobby', 'Logie', 'Locuinta'],

                    "RU": ['Вентиляция', 'Св. возд', 'Ванна', 'Балкон', 'Бюро', 'Отопление', 'Чердачный этаж',
                           'Прихожая', 'Патио', 'Хранилище', 'Лестница', 'Зал', 'Лодж', 'Жилая'],

                    "CS": ["Klimatizace", "Exteriér", "Koupelna", "Balkón", "Kancelář", "Kotelna", "Podkroví", "Chodba",
                           "Světlík", "Komora", "Schodiště", "Hala", "Lodžie", "Bydlní"],

                    "SL": ["Strojne nap.", "Sveži zrak", "Kopalni.", "Balkon", "Pisarna", "Elektro nap.", "Podstrešje",
                           "Hodnik", "Dvorišče", "Shramba", "Stopnice", "Veža", "Loža", "Bivalni prostor"],

                    "SK": ["Klimatizace", "Exteriér", "Koupelna", "Balkón", "Kancelář", "Kotelna", "Podkroví", "Chodba",
                           "Světlík", "Komora", "Schodiště", "Hala", "Lodžie", "Bydlní"]
                    }

translation_room_count = len(translation_room["FR"])

# -------------------------------------

# todo traduction

translation_231 = {"FR": ["R", "S", "a", "b", "c", "bc"],
                   "EN": ["R", "S", "a", "b", "c", "bc"],
                   "DE": ["R", "S", "a", "b", "c", "bc"],
                   "IT": ["R", "S", "a", "b", "c", "bc"],
                   "ES": ["R", "S", "a", "b", "c", "bc"],
                   "HR": ["R", "S", "a", "b", "c", "bc"],
                   "RO": ["R", "S", "a", "b", "c", "bc"],
                   "RU": ["R", "S", "a", "b", "c", "bc"],
                   "CS": ["R", "S", "a", "b", "c", "bc"],
                   "SL": ["R", "S", "a", "b", "c", "bc"],
                   "SK": ["R", "S", "a", "b", "c", "bc"]}

translation_231_count = len(translation_231["FR"])

# -------------------------------------

# todo traduction
translation_232 = {"FR": ["N", "M", "L"],
                   "EN": ["N", "M", "L"],
                   "DE": ["N", "M", "L"],
                   "IT": ["N", "M", "L"],
                   "ES": ["N", "M", "L"],
                   "HR": ["N", "M", "D"],
                   "RO": ["N", "M", "L"],
                   "RU": ["Н", "M", "Л"],
                   "CS": ["N", "M", "L"],
                   "SL": ["N", "M", "L"],
                   "SK": ["N", "M", "L"]}

# todo traduction
translation_232_combo = {"FR": ["N = Surface nette de la pièce et vol",
                                "M = vol. net pl. étages, sans SHON",
                                "L = espace vide, ni SHON ni vol. net"],

                         "EN": ["N = net room area and NRV",
                                "M = multistory NRV, no NRA",
                                "L = empty, neither NRA nor NRV"],

                         "DE": ["M = Nettoraumfläche und NRI",
                                "M = Mehrgeschossiger NRI, keine NRF",
                                "L = Leerraum, weder NRF noch NRI"],

                         "IT": ["N = superficie vano netta e CBN",
                                "M = più piani CBN, nessuna SVN",
                                "L vano vuoto, né SVN né CBN"],

                         "ES": ["N = Superficie neta de local y VNL",
                                "M = VNL de varias plantas, sin SNL",
                                "L = Espacio libre, no parte de SNL n"],

                         "HR": ["N = Pripada neto površini",
                                "M = NP u više katova, bez NKP",
                                "D = nekorišteno, nije neto površina"],

                         "RO": ["N = Arii si volume utile",
                                "M = Volum util etahe, fara suprafete",
                                "L = Liber, nu apartine supraf. utile"],

                         "RU": ["Н = площ. помещения нетто и ООН",
                                "M = ООН нескольких этажей, без ППН",
                                "Л = пустое помещ., без ППН и ООН"],

                         "CS": ["N = netto plocha místnosti a NOM",
                                "M = vícepodlažní NOM, bez NZP",
                                "L = prázdna, kromě NZP ještě NOM"],

                         "SL": ["N = neto tlorisna površina in NVP",
                                "M = večetažna NVP, brez NTP",
                                "L = prazen prostor, ni NTP niti NVP"],

                         "SK": ["N = netto plocha místnosti a NOM",
                                "M = vícepodlažní NOM, bez NZP",
                                "L = prázdna, kromě NZP ještě NOM"]}

translation_232_count = len(translation_232["FR"])

# -------------------------------------

# todo traduction

translation_233 = {"FR": ["SH", "SA", "SE", "NH"],
                   "EN": ["LI", "SS", "ES", "NL"],
                   "DE": ["WO", "ZU", "WI", "KW"],
                   "IT": ["WO", "ZU", "WI", "KW"],
                   "ES": ["SH", "SA", "SU", "SS"],
                   "HR": ["PP", "DP", "EP", "NP"],
                   "RO": ["SL", "SA", "SC", "SN"],
                   "RU": ["ЖП", "ДП", "ХП", "НЖ"],
                   "CS": ["OP", "PP", "HP", "BP"],
                   "SL": ["SP", "DP", "NS", "KP"],
                   "SK": ["OP", "PP", "HP", "BP"]}

translation_233_count = len(translation_233["FR"])

# -------------------------------------

# todo traduction

translation_235 = {"FR": ["SU", "SIT", "SD", "SU 1", "SU 2", "SU 3", "SU 4", "SU 5", "SU 6", "SU 7",
                          "SU", "SU 1", "SU 2", "SU 3", "SU 4", "SU 5", "SU 6", "SU 7"],

                   "EN": ["USA", "TA", "CA", "USA 1", "USA 2", "USA 3", "USA 4", "USA 5", "USA 6", "USA 7",
                          "UA", "UA 1", "UA 2", "UA 3", "UA 4", "UA 5", "UA 6", "UA 7"],

                   "DE": ["NUF", "TF", "VF", "NUF 1", "NUF 2", "NUF 3", "NUF 4", "NUF 5", "NUF 6", "NUF 7",
                          "NF", "NF 1", "NF 2", "NF 3", "NF 4", "NF 5", "NF 6", "NF 7"],

                   "IT": ["SPU", "ST", "SC", "SPU 1", "SPU 2", "SPU 3", "SPU 4", "SPU 5", "SPU 6", "SPU 7",
                          "SU", "SU 1", "SU 2", "SU 3", "SU 4", "SU 5", "SU 6", "SU 7"],

                   "ES": ["SU", "SF", "ST", "SU 1", "SU 2", "SU 3", "SU 4", "SU 5", "SU 6", "SU 7",
                          "SN", "SUP 1", "SUP 2", "SUP 3", "SUP 4", "SUP 5", "SUP 6", "SUP 7"],

                   "HR": ["NUF", "UP", "TP", "NUF 1", "NUF 2", "NUF 3", "NUF 4", "NUF 5", "NUF 6", "NUF 7",
                          "NP", "GKP 1", "GKP 2", "GKP 3", "GKP 4", "GKP 5", "GKP 6", "GKP 7"],

                   "RO": ["AE", "ST", "CI", "AE 1", "AE 2", "AE 3", "AE 4", "AE 5", "AE 6", "AE 7",
                          "SL", "ZFP 1", "ZFP 2", "ZFP 3", "ZFP 4", "ZFP 5", "ZFP 6", "ZFP 7"],

                   "RU": ["ПОП", "ТП", "ПД", "ПОП 1", "ПОП 2", "ПОП 3", "ПОП 4", "ПОП 5", "ПОП 6", "ПОП 7",
                          "ХП", "ПП 1", "ПП 2", "ПП 3", "ПП 4", "ПП 5", "ПП 6", "ПП 7"],

                   "CS": ["NUP", "TP", "DP", "NUP 1", "NUP 2", "NUP 3", "NUP 4", "NUP 5", "NUP 6", "NUP 7",
                          "UP", "UP1", "UP2", "UP3", "UP4", "UP5", "UP6", "UP7"],

                   "SL": ["UP", "TP", "KP", "UP 1", "UP 2", "UP 3", "UP 4", "UP 5", "UP 6", "UP 7",
                          "GUP", "GUP1", "GUP2", "GUP3", "GUP4", "GUP5", "GUP6", "GUP7"],

                   "SK": ["NUP", "TP", "DP", "NUP 1", "NUP 2", "NUP 3", "NUP 4", "NUP 5", "NUP 6", "NUP 7",
                          "UP", "UP1", "UP2", "UP3", "UP4", "UP5", "UP6", "UP7"]}

translation_235_count = len(translation_235["FR"])

# -------------------------------------

room_config_index_231 = 0
room_config_index_232 = 1
room_config_index_233 = 2
room_config_index_235 = 3
room_config_index_264 = 4
room_config_index_266 = 5

room_config_list = [[1, 0, 3, 1, 1.00, 1.00],  # Aération
                    [1, 0, 3, 0, 1.00, 1.00],  # Air frais
                    [0, 0, 0, 0, 1.00, 1.00],  # Bain
                    [1, 0, 0, 0, 0.25, 1.00],  # Balcon
                    [0, 0, 3, 0, 1.00, 1.00],  # Bureau
                    [0, 0, 1, 1, 1.00, 1.00],  # Chauffage
                    [1, 0, 0, 0, 0.25, 1.00],  # Comble
                    [0, 0, 0, 2, 1.00, 1.00],  # Couloir
                    [1, 0, 3, 1, 1.00, 1.00],  # Cour
                    [1, 0, 1, 0, 0.25, 1.00],  # Débarras
                    [1, 0, 3, 2, 1.00, 1.00],  # Escalier
                    [1, 0, 3, 2, 1.00, 1.00],  # Hall
                    [1, 0, 0, 0, 0.25, 1.00],  # Loggia
                    [0, 0, 0, 0, 1.00, 1.00]]  # Séjour

room_config_count = len(room_config_list)
room_sub_config_count = len(room_config_list[0])

# ===================================================
#                       UNIT LIST
# ===================================================

# todo traduction

unit_list_file = "unit_list"
unit_list_datas = ["m³", "m²", "m", "Pc", "kg"]

# ===================================================
#                       UPDATE LIST
# ===================================================

update_setting_file = "update_setting"
update_setting_datas = {"height": 500,
                        "ismaximized_on": False,
                        "catalog": "",
                        "search": "",
                        "order": 0,
                        "width": 400}

update_config_file = "update_config"
update_config_datas = dict()

# ===================================================
#                       VOB
# ===================================================

vob_setting_file = "vob_setting"

vob_setting_datas = {"filter": 0,
                     "height": 500,
                     "ismaximized_on": False,
                     "order": 0,
                     "order_col": 0,
                     "save": "",
                     "splitter": 75,
                     "width": 400}

# ===================================================
#                       WARNING
# ===================================================

warning_setting_file = "warning_setting"

warning_setting_datas = {"attributes_update": 0,
                         "catalogs_updated": 0,
                         "hierarchy_delete_item": 0}

warning_setting_conv = {"attributes_update": "Avertissement_maj_attribut",
                        "catalogs_updated": "Avertissement_sauvegarder_tout_ok",
                        "hierarchy_delete_item": "Avertissement_suppression_hierarchie"}

# ===================================================
#                       CAT LIST
# ===================================================

settings_names = {app_setting_file: app_setting_datas,

                  attribute_setting_file: attribute_setting_datas,
                  attribute_config_file: attribute_config_datas,

                  cat_list_file: cat_list_datas,
                  recent_config_file: recent_config_dict,

                  formula_setting_file: formula_setting_datas,

                  formula_fav_setting_file: formula_fav_setting_datas,
                  formula_fav_config_file: formula_fav_config_datas,

                  help_setting_file: help_setting_datas,

                  library_setting_file: library_setting_datas,
                  library_config_file: library_config_datas,

                  library_synchro_setting_file: library_synchro_setting_datas,
                  library_synchro_config_file: library_synchro_config_datas,

                  model_setting_file: model_setting_datas,
                  model_config_file: model_config_datas,

                  number_setting_file: number_setting_datas,
                  replace_setting_file: replace_setting_datas,
                  structure_setting_file: structure_setting_datas,

                  unit_list_file: unit_list_datas,

                  search_setting_file: search_setting_datas,

                  update_setting_file: update_setting_datas,
                  update_config_file: update_config_datas,

                  vob_setting_file: vob_setting_datas,

                  warning_setting_file: warning_setting_datas}

# ===================================================
#                       Last Save
# ===================================================

last_save_list = ["dernier enregistrement", "last save",
                  "letzte speicherung", "neueste aufnahme",
                  "ultimo salvataggio", "ultima registrazione",
                  "ùltima grabación",
                  "zadnje spremanje", "ultima salvare", "Последняя резервная копия"]

# ===================================================
#                       Help
# ===================================================


# ----------------------------
# Interface
# ----------------------------

help_interface_presentat = "ASC8756"
help_interface_actionbar = "ASC8757"
help_interface_hierarchy = "ASC8758"
help_interface_attribute = "ASC8759"
help_interface_langue = "ASC8746"

# ----------------------------
# Allplan
# ----------------------------

help_allplan_connect_prj = "ASC8743"
help_allplan_display = "ASC8744"
help_allplan_material = "ASC8832"
help_allplan_report = "ASC8833"
help_allplan_refresh = "ASC8760"
help_allplan_error = "ASC8761"

# ----------------------------
# Catalogue
# ----------------------------

help_cat_what = "ASC8762"
help_cat_new_cat = "ASC8745"
help_cat_convert = "ASC8763"
help_cat_open_cat = "ASC8747"
help_cat_settings = "ASC8749"
help_cat_recent = "ASC8748"
help_cat_save = "ASC8750"
help_cat_save_as = "ASC8751"
help_cat_update = "ASC8764"
help_cat_restore = "ASC8752"

# ----------------------------
# Folder
# ----------------------------

help_folder_what = "ASC8765"
help_folder_new = "ASC8766"
help_folder_del = "ASC8767"
help_folder_copy = "ASC8768"
help_folder_paste = "ASC8769"
help_folder_icon = "ASC8831"

# ----------------------------
# Material
# ----------------------------

help_material_what = "ASC8770"
help_material_new = "ASC8771"
help_material_del = "ASC8772"
help_material_copy = "ASC8773"
help_material_paste = "ASC8774"

# ----------------------------
# Component
# ----------------------------

help_component_what = "ASC8775"
help_component_new = "ASC8776"
help_component_del = "ASC8777"
help_component_copy = "ASC8778"
help_component_paste = "ASC8779"

# ----------------------------
# Link
# ----------------------------

help_link_what = "ASC8780"
help_link_new = "ASC8781"
help_link_del = "ASC8782"
help_link_copy = "ASC8783"
help_link_paste = "ASC8784"

# ----------------------------
# Attribute
# ----------------------------

help_attribute_what = "ASC8785"
help_attribute_new = "ASC8786"
help_attribute_fav = "ASC8787"
help_attribute_del = "ASC8788"
help_attribute_copy = "ASC8789"
help_attribute_paste = "ASC8790"
help_attribute_order = "ASC8791"

# ----------------------------
# Formula
# ----------------------------

help_formula_what = "ASC8792"
help_formula_editor = "ASC8793"
help_formula_new = "ASC8794"
help_formula_search = "ASC8795"
help_formula_function = "ASC8796"
help_formula_attribute = "ASC8797"
help_formula_door = "ASC8798"

# ----------------------------
# Formula favorites
# ----------------------------

help_formula_fav_save = "ASC8799"
help_formula_fav_use = "ASC8800"
help_formula_fav_manage = "ASC8801"

# ----------------------------
# Search
# ----------------------------

help_search_cat = "ASC8802"
help_search_filter = "ASC8803"

# ----------------------------
# Search and replace
# ----------------------------

help_replace_cat = "ASC8804"

# ----------------------------
# Models
# ----------------------------

help_model_what = "ASC8805"
help_model_new = "ASC8806"
help_model_manage = "ASC8807"
help_model_modify = "ASC8808"
help_model_import = "ASC8809"

# ----------------------------
# Libraries
# ----------------------------

help_library_what = "ASC8810"
help_library_new = "ASC8811"
help_library_manage = "ASC8812"
help_library_import = "ASC8813"
help_library_sync = "ASC8814"

# ===================================================
#                       icones
# ===================================================
datas_icons = {'Cuisine': 'icon_1', 'aide': 'icon_2', 'aménagement ext': 'icon_3', 'annexe': 'icon_4',
               'annotation': 'icon_5', 'appui de fenêtre': 'icon_6', 'aspirateur': 'icon_7', 'attention': 'icon_8',
               'attribut': 'icon_9', 'attribut_2': 'icon_10', "baie d'angle": 'icon_11', 'bardage': 'icon_12',
               'bâtiment': 'icon_13', 'caisse à outils': 'icon_14', 'caisson de store': 'icon_15',
               'carrelage': 'icon_16', 'cercle': 'icon_17', 'cercle 3d': 'icon_18', 'chambre': 'icon_19',
               'charpente': 'icon_20', 'chauffage': 'icon_21', 'chauffage 2': 'icon_22', 'cheminée': 'icon_23',
               'chevron': 'icon_24', 'chevêtre': 'icon_25', 'climatisation': 'icon_26', 'composant': 'icon_27',
               'couleur': 'icon_28', 'couleur_2': 'icon_29', 'coupole': 'icon_30', 'couverture': 'icon_31',
               'couverture 1': 'icon_32', 'cylindre': 'icon_33', 'dalle': 'icon_34', 'domotique': 'icon_35',
               'dossier': 'icon_36', 'ellipse': 'icon_37', 'entrait moisé': 'icon_38', 'entrait simple': 'icon_39',
               'escalier': 'icon_40', 'escalier 2': 'icon_41', 'escalier 3': 'icon_42', 'faux': 'icon_43',
               'favoris_2': 'icon_44', 'façade': 'icon_45', 'fenêtre': 'icon_46', 'fenêtre de toit': 'icon_47',
               'fenêtre de toit smartpart': 'icon_48', 'fenêtre smartpart': 'icon_49', 'ferraillage': 'icon_50',
               'feuillure': 'icon_51', 'garage': 'icon_52', 'garde-corps': 'icon_53', 'grille': 'icon_54',
               'gros oeuvre': 'icon_55', 'hachurage': 'icon_56', 'image': 'icon_57', 'incendie': 'icon_58',
               'information': 'icon_59', 'installation perso': 'icon_60', 'ligne 2d': 'icon_61', 'ligne 3d': 'icon_62',
               'linteau': 'icon_63', 'lucarne': 'icon_64', 'légende': 'icon_65', 'macro': 'icon_66',
               'macro 2': 'icon_67', 'menuiserie ext': 'icon_68', 'mesure': 'icon_69', 'mesure aire': 'icon_70',
               'mesure coordonnées': 'icon_71', 'mesure distance': 'icon_72', 'mesure volume': 'icon_73',
               'mise en page': 'icon_74', 'motif': 'icon_75', 'mt3d': 'icon_76', 'mur': 'icon_77',
               'mur polygonal': 'icon_78', 'mur profil': 'icon_79', 'métier': 'icon_80', 'niche': 'icon_81',
               'noue': 'icon_82', 'objet': 'icon_83', 'options': 'icon_84', 'ossature': 'icon_85',
               'ossature 2': 'icon_86', 'ouvrage': 'icon_87', 'palette': 'icon_88', 'palette couleur': 'icon_89',
               'panne': 'icon_90', 'pannes-chevron': 'icon_91', 'parallélépipède': 'icon_92', 'pare-soleil': 'icon_93',
               'patch': 'icon_94', 'peinture': 'icon_95', 'piscine': 'icon_96', 'pièce': 'icon_97',
               'plafond': 'icon_98', 'plan de référence': 'icon_99', 'plan de toiture': 'icon_100',
               'plan de toiture 2': 'icon_101', 'plantations': 'icon_102', 'plantes': 'icon_103', 'plinthe': 'icon_104',
               'plomberie': 'icon_105', 'plume': 'icon_106', 'polygone': 'icon_107', 'polyligne': 'icon_108',
               'porte': 'icon_109', 'porte 2': 'icon_110', 'porte 3': 'icon_111', 'poteau': 'icon_112',
               'poteau 2': 'icon_113', 'poutre': 'icon_114', 'poêle': 'icon_115', 'pt basculante': 'icon_116',
               'pt levante': 'icon_117', 'pt sectionnelle': 'icon_118', 'pt smartpart': 'icon_119',
               'pyramide': 'icon_120', 'radier': 'icon_121', 'rapport': 'icon_122', 'rectangle': 'icon_123',
               'revêtement de sol': 'icon_124', 'revêtement latéral': 'icon_125', 'réseau': 'icon_126',
               'salle de bains': 'icon_127', 'sanitaire': 'icon_128', 'second-oeuvre': 'icon_129',
               'second_oeuvre': 'icon_130', 'semelle filante': 'icon_131', 'semelle ponctuelle': 'icon_132',
               'smartpart': 'icon_133', 'solive': 'icon_134', 'sphère': 'icon_135', 'spline': 'icon_136',
               'spline 3d': 'icon_137', 'style': 'icon_138', 'surface 3d': 'icon_139', 'surveillance': 'icon_140',
               'tableau': 'icon_141', 'talon': 'icon_142', 'terrassement': 'icon_143', 'thermique': 'icon_144',
               'toile tendue': 'icon_145', 'trait': 'icon_146', 'trémie': 'icon_147', 'ventilation': 'icon_148',
               'verifier': 'icon_149', 'vide': 'icon_150', 'volet': 'icon_151', 'électricité': 'icon_152',
               'électricité 2': 'icon_153', 'élément architectural perso': 'icon_154', 'étage': 'icon_155',
               'étanchéité': 'icon_156'}
