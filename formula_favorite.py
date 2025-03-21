#!/usr/bin/python3
# -*- coding: utf-8 -*
import os

from PyQt5.Qt import *

from allplan_manage import AllplanDatas, col_favoris_formule_titre, col_favoris_formule_famille, AllplanPaths
from allplan_manage import col_favoris_formule_formule
from catalog_manage import CatalogDatas
from formatting_widget import Formatting
from main_datas import attribute_model_show_icon, icons_path, paste_icon
from main_datas import delete_icon, valid_icon, error_icon, windows_close_hover_icon, get_icon
from main_datas import formula_fav_setting_file, app_setting_file, formula_fav_config_file, add_icon, options_icon
from models import ModelsTabDel
from tools import afficher_message as msg
from tools import qm_check, find_new_title, move_window_tool, recherche_image, application_title, MyContextMenu
from tools import settings_save, get_look_tableview, settings_read, browser_file
from ui_formula_favorite import Ui_FormulaFavorite
from ui_formula_favorite_modify import Ui_FormulaFavoriteModify
from ui_formula_favorite_tab import Ui_FormulaFavoriteTab


class FormulaFavorite(QWidget):

    def __init__(self, asc):
        super().__init__()

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_FormulaFavorite()
        self.ui.setupUi(self)
        self.ui.onglet.setTabBar(FormulaFavoriteTabBar())

        # -----------------------------------------------
        # Settings
        # -----------------------------------------------

        formula_fav = settings_read(formula_fav_setting_file)

        self.ismaximized_on = formula_fav.get("ismaximized_on", False)

        if not isinstance(self.ismaximized_on, bool):
            self.ismaximized_on = False

        width = formula_fav.get("width", 800)

        if not isinstance(width, int):
            width = 800

        height = formula_fav.get("height", 600)

        if not isinstance(height, int):
            width = 800

        self.resize(width, height)

        # -----------------------------------------------

        self.formulas_fav_model = QStandardItemModel()

        self.tabs_list = list()

        # -----------------------------------------------
        # Allplan datas
        # -----------------------------------------------

        self.allplan: AllplanDatas = self.asc.allplan

        # -----------------------------------------------
        # Widget modifier un onglet
        # -----------------------------------------------

        self.widget_tab_modify = FormulaFavoriteModify(self.ui.onglet, self.allplan)

        self.widget_tab_modify.appliquer_modifications.connect(self.onglet_renommer_action)

        self.asc.langue_change.connect(
            lambda main=self.widget_tab_modify: self.widget_tab_modify.ui.retranslateUi(main))

        # -----------------------------------------------
        # Widget supprimer un onglet
        # -----------------------------------------------

        self.widget_tab_del = ModelsTabDel(self.ui.onglet)
        self.widget_tab_del.validation_supprimer.connect(self.onglet_suppression_action)

        # -----------------------------------------------
        # Signaux onglet
        # -----------------------------------------------

        self.ui.onglet.tabBarClicked.connect(self.onglet_clic)
        self.ui.onglet.tabBarDoubleClicked.connect(self.onglet_double_clic)

        tab_bar: FormulaFavoriteTabBar = self.ui.onglet.tabBar()
        tab_bar.del_signal.connect(self.onglet_suppression)

        tab_bar.move_signal.connect(self.onglet_deplacement)

        # -----------------------------------------------
        # Autres boutons
        # -----------------------------------------------

        self.ui.bt_enregistrer.clicked.connect(self.enregistrer)
        self.ui.bt_quitter.clicked.connect(self.close)

        self.change_made = False

        self.ui.onglet.customContextMenuRequested.connect(self.onglet_afficher_menu)

    @staticmethod
    def a___________________chargement______():
        pass

    def formula_fav_personnaliser(self, parent_actuel: QWidget, nom_onglet="", formula_name=""):

        self.onglets_chargement()

        self.change_made = False

        if nom_onglet == "" or nom_onglet not in self.tabs_list:
            self.formula_fav_show(parent_actuel=parent_actuel)
            return

        index_onglet = self.tabs_list.index(nom_onglet)
        self.ui.onglet.setCurrentIndex(index_onglet)

        current_widget: FormulaFavoriteTab = self.ui.onglet.widget(index_onglet)

        if not isinstance(current_widget, FormulaFavoriteTab):
            self.formula_fav_show(parent_actuel=parent_actuel)
            return

        current_widget.gestion_header()

        if formula_name != "":
            current_widget.formula_select(formula_name=formula_name)

        current_widget.ui.titre.setFocus()

        self.formula_fav_show(parent_actuel=parent_actuel)

    def formula_fav_show(self, parent_actuel):

        move_window_tool(widget_parent=parent_actuel, widget_current=self)

        if self.ismaximized_on:
            self.showMaximized()
        else:
            self.show()

    @staticmethod
    def a___________________onglet_chargement_______________():
        pass

    def onglets_chargement(self):

        print("WidgetFormulaFavorite -- onglets_chargement -- dbu")

        self.formulas_fav_model.clear()

        self.ui.onglet.blockSignals(True)
        self.ui.onglet.clear()

        self.tabs_list.clear()

        self.onglet_ajouter_button_add()
        self.ui.onglet.blockSignals(False)

        dict_elements = settings_read(formula_fav_config_file)

        if len(dict_elements) == 0:
            dict_elements = self.formula_initialization()

        for nom_onglet, family_datas in dict_elements.items():
            nom_onglet = find_new_title(base_title=nom_onglet, titles_list=self.tabs_list)

            family_datas: dict

            icone_onglet = family_datas.get("icon", "")

            icone_onglet = recherche_image(image_name=icone_onglet, image_default="attribute_model_show.svg")

            formulas_dict: dict = family_datas.get("formulas", dict())

            self.onglet_ajouter_action(nom_onglet, icone_onglet, formulas_dict=formulas_dict)

        formula_fav = settings_read(formula_fav_setting_file)

        tab_index = formula_fav.get("tab_index", 0)

        if not isinstance(tab_index, int):

            self.ui.onglet.setCurrentIndex(0)

        elif tab_index < 0:

            self.ui.onglet.setCurrentIndex(0)

        else:

            self.ui.onglet.setCurrentIndex(tab_index)

        formula_name = formula_fav.get("formula_name", "")

        if not isinstance(formula_name, str):
            return

        if formula_name == "":
            return

        widget = self.ui.onglet.widget(tab_index)

        if not isinstance(widget, FormulaFavoriteTab):
            self.change_made = False
            return

        widget.formula_select(formula_name=formula_name)

        self.change_made = False

    def formula_initialization(self) -> dict:
        nom_onglet = self.onglet_recherche_titre()
        formula_name = self.formulas_recherche_titre(nom_onglet="")
        formula_txt = "@99@"

        formulas_dict = {formula_name: formula_txt}

        datas = {nom_onglet: {"icon": attribute_model_show_icon,
                              "formulas": formulas_dict}}

        settings_save(formula_fav_config_file, datas)

        return datas

    @staticmethod
    def a___________________model_gestion______():
        pass

    def favoris_fav_model_add(self, nom_onglet: str, formula_name="", formula="", save=False) -> str:

        if formula_name == "":
            formula_name = self.formulas_recherche_titre(nom_onglet=nom_onglet)

        self.formulas_fav_model.appendRow([QStandardItem(formula_name),
                                           QStandardItem(formula),
                                           QStandardItem(nom_onglet)])

        self.formulas_fav_model.sort(col_favoris_formule_titre)

        if not save:
            return formula_name

        self.enregistrer_config()
        return formula_name

    def favoris_fav_model_del_family(self, nom_onglet: str) -> bool:

        recherche = self.favoris_model_find_familly(nom_onglet=nom_onglet, reverse=True)

        if len(recherche) == 0:
            return False

        for qs_titre in recherche:

            if not isinstance(qs_titre, QStandardItem):
                print("WidgetFormulaFavorite -- onglet_renommer_model -- not isinstance(qs_titre, QStandardItem)")
                continue

            row_actuel = qs_titre.row()

            self.formulas_fav_model.takeRow(row_actuel)

        return True

    def favoris_model_rename_familly(self, ancien_titre: str, nouveau_titre: str) -> bool:

        recherche = self.favoris_model_find_familly(nom_onglet=ancien_titre)

        if len(recherche) == 0:
            return False

        for qs_titre in recherche:

            if not isinstance(qs_titre, QStandardItem):
                print("WidgetFormulaFavorite -- onglet_renommer_model -- not isinstance(qs_titre, QStandardItem)")
                continue

            qs_titre.setText(nouveau_titre)

        return True

    def favoris_model_find_familly(self, nom_onglet: str, reverse=False) -> list:

        recherche = self.formulas_fav_model.findItems(nom_onglet, Qt.MatchExactly, col_favoris_formule_famille)

        if len(recherche) == 0:
            print(f"WidgetFormulaFavorite -- favoris_model_find_familly -- le titre {nom_onglet} n'a pas été trouvé !")
            return list()

        recherche.sort(reverse=reverse)

        return recherche

    @staticmethod
    def a___________________onglet_menu______():
        pass

    def onglet_afficher_menu(self, point: QPoint):

        index_onglet = self.ui.onglet.tabBar().tabAt(point)

        if index_onglet == -1:
            menu = MyContextMenu(tooltips_visible=False)

            menu.add_title(title=self.windowTitle())

            menu.add_action(qicon=get_icon(add_icon),
                            title=self.tr('Nouveau'),
                            action=self.onglet_ajouter)

            menu.exec_(self.ui.onglet.mapToGlobal(point))

            return

        widget_onglet = self.ui.onglet.widget(index_onglet)

        if self.ui.onglet.currentIndex() != index_onglet:
            self.ui.onglet.setCurrentIndex(index_onglet)

        if not isinstance(widget_onglet, FormulaFavoriteTab):
            print("WidgetFormulaFavorite -- onglet_afficher_menu -- "
                  "not isinstance(widget_onglet, WidgetFormulaFavoriteTab)")
            return

        menu = MyContextMenu(tooltips_visible=False)

        menu.add_title(title=self.windowTitle())

        menu.add_action(qicon=get_icon(add_icon),
                        title=self.tr('Nouveau'),
                        action=self.onglet_ajouter)

        menu.add_action(qicon=get_icon(options_icon),
                        title=self.tr('Éditer'),
                        action=lambda: self.onglet_renommer_afficher(index_onglet=index_onglet,
                                                                     widget_onglet=widget_onglet))

        menu.add_action(qicon=get_icon(delete_icon),
                        title=self.tr('Supprimer'),
                        action=lambda: self.onglet_suppression_action(current_index=index_onglet))

        menu.exec_(self.ui.onglet.mapToGlobal(point))

    @staticmethod
    def a___________________onglet_ajouter_______________():
        pass

    def onglet_ajouter_button_add(self):
        self.ui.onglet.addTab(QWidget(), get_icon(add_icon), "")

    def onglet_ajouter(self):

        icone_onglet = ":/Images/attribute_model_show.svg"
        formulas_dict = dict()
        index_insertion = - 1

        nom_onglet = self.onglet_ajouter_action(title="",
                                                icone_onglet=icone_onglet,
                                                formulas_dict=formulas_dict,
                                                tab_index=index_insertion)

        self.onglet_ajouter_afficher_menu(nom_onglet=nom_onglet,
                                          icone_onglet=icone_onglet,
                                          index_insertion=index_insertion)

    def onglet_ajouter_afficher_menu(self, nom_onglet: str, icone_onglet: str, index_insertion: int):

        # Définition de l'index d'insertion dans la liste
        if index_insertion == -1:
            index_insertion = self.ui.onglet.count() - 1

        self.onglet_placement_widget(index_insertion, self.widget_tab_modify)
        self.widget_tab_modify.formulas_fav_personnaliser(nom_onglet=nom_onglet,
                                                          icone_onglet=icone_onglet,
                                                          liste_onglets=self.tabs_list)

    def onglet_ajouter_action(self, title="", icone_onglet="", formulas_dict=None, tab_index=-1) -> str:

        if title == "":
            title = self.onglet_recherche_titre()

        if icone_onglet == "":
            icone_onglet = attribute_model_show_icon
        else:
            icone_onglet = recherche_image(image_name=icone_onglet, image_default=attribute_model_show_icon)

        # Définition de l'index d'insertion dans la liste
        if tab_index == -1:
            tab_index = len(self.tabs_list)

        if formulas_dict is None:
            formulas_dict = dict()

        if len(formulas_dict) == 0:
            self.favoris_fav_model_add(nom_onglet=title)

        else:

            formula_titles_list = self.formulas_lister_titre()

            for formula_name, formula in formulas_dict.items():
                formula_name = find_new_title(base_title=formula_name, titles_list=formula_titles_list)

                self.favoris_fav_model_add(nom_onglet=title,
                                           formula_name=formula_name,
                                           formula=formula)

                formula_titles_list.append(formula_name)

        # Mise à jour de la liste des onglets
        self.tabs_list.insert(tab_index, title)

        # Création d'un nouvel onglet
        tab = FormulaFavoriteTab(asc=self.asc,
                                 widget_onglet=self,
                                 nom_onglet=title,
                                 icone_onglet=icone_onglet)

        self.onglet_update_combo()

        self.asc.langue_change.connect(lambda main=tab: tab.ui.retranslateUi(main))

        tab.famille_change.connect(self.formula_changement_famille)

        # Ajout de l'onglet
        self.ui.onglet.insertTab(tab_index, tab, get_icon(icone_onglet), title)

        if tab_index <= 6:
            self.ui.onglet.setTabToolTip(tab_index, f"{title} (F{tab_index + 6})")
        else:
            self.ui.onglet.setTabToolTip(tab_index, title)

        # Définition du nouvel onglet comme l'onglet utilisé
        self.ui.onglet.setCurrentIndex(tab_index)

        self.change_made = True
        return title

    def onglet_recherche_titre(self) -> str:

        titre_base = self.tr("Favoris")

        return find_new_title(base_title=titre_base, titles_list=self.tabs_list)

    @staticmethod
    def a___________________onglet_supprimer_______________():
        pass

    def onglet_suppression(self, current_index: int):
        """ Gestion de la suppression d'un onglet
        :param current_index: information envoyée par le programme informant l'index de l'onglet qui sera supprimé
        :return: None
        """

        if self.ui.onglet.count() <= 1:
            return

        # Définition du titre de l'onglet
        nom_onglet = self.ui.onglet.tabText(current_index)

        if nom_onglet not in self.tabs_list:
            print("WidgetFormulaFavorite -- suppression_onglet -- titre_onglet not in self.liste_onglets")
            return

        self.onglet_placement_widget(current_index, self.widget_tab_del)
        self.widget_tab_del.del_ask_show(tab_index=current_index)

    def onglet_suppression_action(self, current_index):

        nom_onglet = self.ui.onglet.tabText(current_index)

        if not self.favoris_fav_model_del_family(nom_onglet=nom_onglet):
            return

            # Mise à jour de la liste des onglets
        self.tabs_list.remove(nom_onglet)

        # Suppression de la onglet
        self.ui.onglet.blockSignals(True)
        self.ui.onglet.removeTab(current_index)
        self.ui.onglet.blockSignals(False)

        if current_index == self.ui.onglet.count() - 1:
            self.ui.onglet.setCurrentIndex(self.ui.onglet.count() - 2)

        self.onglet_update_combo()

        self.tab_redefine_shortcut()

        self.change_made = True

    @staticmethod
    def a___________________onglet_renommer_______________():
        pass

    def onglet_placement_widget(self, current_index: int, widget):

        point: QPoint = self.ui.onglet.tabBar().tabRect(current_index).bottomRight()
        global_point: QPoint = self.ui.onglet.tabBar().mapToGlobal(point)

        largeur_onglet = self.ui.onglet.tabBar().tabRect(current_index).width()
        largeur_widget = widget.size().width()

        position_max = self.size().width()
        position_fin = largeur_widget + point.x()

        if position_fin < position_max:
            widget.move(global_point - QPoint(largeur_onglet, 0))
        else:
            widget.move(global_point - QPoint(largeur_widget, 0))

    def onglet_renommer_action(self, ancien_titre: str, title: str, nouvelle_icone: str):

        tab_index = self.ui.onglet.currentIndex()
        ancien_index = self.tabs_list.index(ancien_titre)

        widget_tab = self.ui.onglet.currentWidget()

        if not isinstance(widget_tab, FormulaFavoriteTab):
            print("WidgetFormulaFavorite -- onglet_renommer_action -- "
                  "not isinstance(widget, WidgetFormulaFavoriteTab)")
            return

        if ancien_titre != title:

            formula_name = widget_tab.current_formula_find()

            if not self.favoris_model_rename_familly(ancien_titre, title):
                return

            self.tabs_list[ancien_index] = title

            self.ui.onglet.setTabText(tab_index, title)

            if tab_index <= 6:
                self.ui.onglet.setTabToolTip(tab_index, f"{title} (F{tab_index + 6})")
            else:
                self.ui.onglet.setTabToolTip(tab_index, title)

            widget_tab.nom_onglet = title

            widget_tab.onglet_renamed(title, formula_name)

            self.onglet_update_combo(ancien_titre, title)

            self.change_made = True

        icone_actuelle = widget_tab.icone_onglet

        if icone_actuelle != nouvelle_icone:
            widget_tab.icone_onglet = nouvelle_icone

            self.ui.onglet.setTabIcon(tab_index, get_icon(nouvelle_icone))

            self.change_made = True

    def onglet_renommer_afficher(self, index_onglet: int, widget_onglet):

        if not isinstance(widget_onglet, FormulaFavoriteTab):
            return

        if self.ui.onglet.currentIndex() != index_onglet:
            self.ui.onglet.setCurrentIndex(index_onglet)

        self.onglet_placement_widget(index_onglet, self.widget_tab_modify)

        self.widget_tab_modify.formulas_fav_personnaliser(nom_onglet=widget_onglet.nom_onglet,
                                                          icone_onglet=widget_onglet.icone_onglet,
                                                          liste_onglets=self.tabs_list)

    @staticmethod
    def a___________________onglet_gestion_combo_familles_______________():
        pass

    def onglet_update_combo(self, ancien_titre="", nouveau_titre=""):

        for index_tab in range(self.ui.onglet.count()):

            widget_tab = self.ui.onglet.widget(index_tab)

            if not isinstance(widget_tab, FormulaFavoriteTab):
                continue

            widget_tab.combo_families_load(ancien_titre, nouveau_titre)

    @staticmethod
    def a___________________onglet_deplacement_______________():
        pass

    def onglet_deplacement(self, _, index_arrivee: int):

        # Définition du titre de l'onglet
        titre_onglet = self.ui.onglet.tabText(index_arrivee)

        # Vérification que le titre de l'onglet est bien dans le datas des onglets
        if titre_onglet not in self.tabs_list:
            return

        self.tabs_list.remove(titre_onglet)

        self.tabs_list.insert(index_arrivee, titre_onglet)

        self.onglet_update_combo()

        self.tab_redefine_shortcut()

        self.change_made = True

    def tab_redefine_shortcut(self):
        tabs_count = self.ui.onglet.count()

        for tab_index in range(1, tabs_count):
            title = self.ui.onglet.tabText(tab_index)

            if tab_index <= 6:
                self.ui.onglet.setTabToolTip(tab_index, f"{title} (F{tab_index + 6})")
            else:
                self.ui.onglet.setTabToolTip(tab_index, title)

    @staticmethod
    def a___________________onglet_clic_______________():
        pass

    def onglet_clic(self, current_index: int):

        last_tab = self.ui.onglet.count() - 1

        if current_index == last_tab:
            self.onglet_ajouter()
            return

        widget: FormulaFavoriteTab = self.ui.onglet.widget(current_index)

        if not isinstance(widget, FormulaFavoriteTab):
            return

        widget.gestion_header()

    def onglet_double_clic(self, index_onglet: int):
        """Gestion du double clic sur le ui.onglet
        :param index_onglet: information envoyée par le programme informant l'index du double clic -> -1 si aucun onglet
        :return: None
        """

        # Vérification si aucun onglet n'a été double cliqué
        if index_onglet == -1:
            self.onglet_ajouter()
            return

        widget = self.ui.onglet.currentWidget()

        if not isinstance(widget, FormulaFavoriteTab):
            return

        self.onglet_renommer_afficher(index_onglet=index_onglet, widget_onglet=widget)

    @staticmethod
    def a___________________formulas_______________():
        pass

    def formulas_lister_titre(self, upper=True) -> list:

        nb_items = self.formulas_fav_model.rowCount()

        formula_titles_list = list()

        for index_item in range(nb_items):

            qs_formula_title = self.formulas_fav_model.item(index_item, col_favoris_formule_titre)

            if not isinstance(qs_formula_title, QStandardItem):
                continue

            formula_titre = qs_formula_title.text()

            if not isinstance(formula_titre, str):
                continue

            if upper:
                formula_titre = formula_titre.upper()

            formula_titles_list.append(formula_titre)

        return formula_titles_list

    def formulas_recherche_titre(self, nom_onglet: str) -> str:

        formula_titles_list = self.formulas_lister_titre()

        if nom_onglet != "":
            titre_base = nom_onglet
        else:

            titre_base = self.tr("Formule")
            titre_base = f"{titre_base} 01"

        if len(formula_titles_list) == 0:
            return titre_base

        return find_new_title(base_title=titre_base, titles_list=formula_titles_list)

    @staticmethod
    def formulas_recup_datas(widget_tab):

        formulas_dict = dict()

        if not isinstance(widget_tab, FormulaFavoriteTab):
            return formulas_dict

        nb_item = widget_tab.filtre_famille.rowCount()

        for index_row in range(nb_item):

            qm_titre = widget_tab.filtre_famille.index(index_row, col_favoris_formule_titre)

            if not qm_check(qm_titre):
                continue

            qm_formule = widget_tab.filtre_famille.index(index_row, col_favoris_formule_formule)

            if not qm_check(qm_titre):
                continue

            formula_titre = qm_titre.data()
            formula_actuel = qm_formule.data()

            formulas_dict[formula_titre] = formula_actuel

        return formulas_dict

    def formula_changement_famille(self, index_tab: int, formula_name: str):

        self.ui.onglet.setCurrentIndex(index_tab)

        widget_tab = self.ui.onglet.widget(index_tab)

        if not isinstance(widget_tab, FormulaFavoriteTab):
            return

        widget_tab.recherche_formule_titre(formula_name=formula_name)

    @staticmethod
    def a___________________sauvegarde_fichier_config_______________():
        pass

    def enregistrer_recherche_modifs(self) -> bool:

        if self.change_made:
            return True

        for index_tab in range(self.ui.onglet.count()):

            widget: FormulaFavoriteTab = self.ui.onglet.widget(index_tab)

            if not isinstance(widget, FormulaFavoriteTab):
                continue

            widget.ui.titre.setFocus()

            if widget.modification_en_cours:
                return True

        return False

    def enregistrer(self):

        self.enregistrer_setting(saved=True)
        self.enregistrer_config()

        self.change_made = False

        self.close()

    def enregistrer_setting(self, saved: bool):

        datas_config = settings_read(file_name=formula_fav_setting_file)

        if saved:

            tab_index = self.ui.onglet.currentIndex()

            datas_config["tab_index"] = tab_index

            datas_config["formula_name"] = ""

            widget_tab = self.ui.onglet.widget(tab_index)

            if isinstance(widget_tab, FormulaFavoriteTab):

                qm = widget_tab.ui.liste_formule.currentIndex()

                if qm_check(qm):

                    formula_name = qm.data()

                    if isinstance(formula_name, str):
                        datas_config["formula_name"] = qm.data()

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True

                settings_save(file_name=formula_fav_setting_file, config_datas=datas_config)
                return

        datas_config["height"] = self.size().height()
        datas_config["width"] = self.size().width()
        datas_config["ismaximized_on"] = False

        settings_save(file_name=formula_fav_setting_file, config_datas=datas_config)

    def enregistrer_config(self):

        datas_elements = dict()

        for index_tab in range(self.ui.onglet.count()):

            widget: FormulaFavoriteTab = self.ui.onglet.widget(index_tab)

            if not isinstance(widget, FormulaFavoriteTab):
                continue

            nom_onglet = widget.nom_onglet
            icone_onglet = self.icone_supprimer_path(widget.icone_onglet)
            formulas_dict = self.formulas_recup_datas(widget_tab=widget)

            datas_elements[nom_onglet] = {"icon": icone_onglet, "formulas": formulas_dict}

            widget.modification_en_cours = False

        settings_save(formula_fav_config_file, datas_elements)

    @staticmethod
    def a___________________icone_gestion_______________():
        pass

    @staticmethod
    def icone_supprimer_path(icone_onglet: str) -> str:

        if icone_onglet.startswith(":/Images/"):
            icone_onglet = icone_onglet.replace(":/Images/", "")
            return icone_onglet

        if icone_onglet.startswith(icons_path):
            icone_onglet = icone_onglet.replace(icons_path, "")
            return icone_onglet

        return icone_onglet

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_N:
            self.onglet_ajouter()
            return

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            self.enregistrer()
            return

        if event.key() == Qt.Key_F2:
            current_index = self.ui.onglet.currentIndex()

            if current_index == 0 or current_index == 1:
                return

            self.onglet_double_clic(self.ui.onglet.currentIndex())
            return

        if event.key() == Qt.Key_Escape:
            self.close()

        shortcuts = [Qt.Key_F6, Qt.Key_F7, Qt.Key_F8, Qt.Key_F9, Qt.Key_F10, Qt.Key_F11, Qt.Key_F12]

        tab_count = self.ui.onglet.count()

        if event.key() not in shortcuts:
            return

        tab_index = shortcuts.index(event.key())

        if tab_index == -1 or tab_index >= tab_count - 1:
            return

        self.ui.onglet.setCurrentIndex(tab_index)

    def changeEvent(self, event: QEvent):

        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.ismaximized_on = True

            else:
                self.ismaximized_on = False
                move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent):

        saved = True

        if self.enregistrer_recherche_modifs():
            if msg(titre=self.windowTitle(),
                   message=self.tr("Voulez-vous enregistrer les modifications?"),
                   type_bouton=QMessageBox.Ok | QMessageBox.No,
                   defaut_bouton=QMessageBox.Ok,
                   icone_sauvegarde=True) == QMessageBox.Ok:
                self.enregistrer_config()

            else:
                saved = False

        self.enregistrer_setting(saved=saved)

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class FormulaFavoriteTab(QWidget):
    famille_change = pyqtSignal(int, str)

    def __init__(self, asc, widget_onglet: FormulaFavorite, nom_onglet: str, icone_onglet: str):

        super().__init__()

        # Création de l'interface
        self.ui = Ui_FormulaFavoriteTab()
        self.ui.setupUi(self)

        self.asc = asc
        self.allplan: AllplanDatas = self.asc.allplan
        self.catalogue: CatalogDatas = self.asc.catalog
        self.widget_onglet = widget_onglet

        self.widget_options = Formatting()
        self.widget_options.save_modif_formatage.connect(self.options_retour_datas)

        self.ui.format_bt.clicked.connect(self.options_afficher)

        # self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))
        # self.ui.valeur_attr.chargement(self.allplan)

        # Définition des variables
        self.nom_onglet = nom_onglet
        self.icone_onglet = icone_onglet

        self.formulas_fav_model = self.widget_onglet.formulas_fav_model

        # -----------------------------------------------
        #  model
        # -----------------------------------------------

        self.filtre_famille = QSortFilterProxyModel()
        self.filtre_famille.setSourceModel(self.formulas_fav_model)
        self.filtre_famille.setFilterKeyColumn(col_favoris_formule_famille)
        self.filtre_famille.setSortLocaleAware(True)
        self.filtre_famille.setFilterRegExp(nom_onglet)

        self.ui.liste_formule.setModel(self.filtre_famille)

        self.gestion_header()

        get_look_tableview(self.ui.liste_formule)

        self.ui.liste_formule.selectionModel().selectionChanged.connect(self.changement_selection)
        self.ui.liste_formule.setCurrentIndex(self.filtre_famille.index(0, col_favoris_formule_titre))

        self.ui.liste_formule.customContextMenuRequested.connect(self.liste_formule_menu_afficher)

        # -----------------------------------------------
        # titre
        # -----------------------------------------------

        self.ui.titre.textChanged.connect(self.verification)
        self.ui.titre.editingFinished.connect(self.texte_finish)
        self.ui.bt_verif_titre.clicked.connect(self.afficher_message)

        # -----------------------------------------------
        # liste noms familles
        # -----------------------------------------------

        self.ui.combo_famille.addItems(self.widget_onglet.tabs_list)
        self.ui.combo_famille.setCurrentText(nom_onglet)
        self.ui.combo_famille.currentTextChanged.connect(self.changement_famille)

        self.ui.combo_famille.installEventFilter(self)

        # changer_apparence_combobox(self.ui.combo_famille)

        # -----------------------------------------------
        # formule
        # -----------------------------------------------

        self.ui.bt_formule_couleur.clicked.connect(self.catalogue.change_highlighter)
        self.catalogue.formula_color_change_signal.connect(self.ui.valeur_attr.change_highlighter_action)

        self.ui.valeur_attr.chargement(self.allplan)
        self.ui.valeur_attr.textChanged.connect(self.changement_formule)

        self.ui.valeur_attr.size_change.connect(self.catalogue.formula_size_change_signal.emit)
        self.catalogue.formula_size_change_signal.connect(self.ui.valeur_attr.setsize)
        self.catalogue.formula_size_change_signal.connect(self.translate_formula_change_size)

        # ---------------------------------------

        self.widget_creation_formule = self.asc.formula_editor_widget
        self.widget_formule_visible = False

        self.ui.bt_editeur.clicked.connect(self.ouvrir_createur_formule)

        self.widget_creation_formule.modif_formule.connect(self.retour_widget_formule)
        self.widget_creation_formule.close_event.connect(self.fermeture_formule)

        # -----------------------------------------------
        # bouton ajouter / supprimer
        # -----------------------------------------------

        self.ui.bt_ajouter.clicked.connect(self.ajouter_formule)
        self.ui.bt_supprimer.clicked.connect(self.supprimer_formule)

        self.changement_selection()

        self.modification_en_cours = False

    @staticmethod
    def a___________________nettoyage_______________():
        pass

    def nettoyage(self):
        self.ui.titre.blockSignals(True)
        self.ui.titre.clear()
        self.ui.titre.blockSignals(False)

        self.ui.valeur_attr.blockSignals(True)
        self.ui.valeur_attr.clear()
        self.ui.valeur_attr.blockSignals(False)

        self.ui.formule_convertie.clear()
        self.ui.nb_char.clear()

    def activation(self, activer: bool):
        self.ui.titre.setEnabled(activer)
        self.ui.combo_famille.setEnabled(activer)
        self.ui.valeur_attr.setEnabled(activer)
        self.ui.bt_supprimer.setEnabled(activer)
        self.ui.bt_verif.setEnabled(activer)
        self.ui.bt_verif_titre.setEnabled(activer)
        self.ui.bt_formule_couleur.setEnabled(activer)
        self.ui.bt_editeur.setEnabled(activer)

    def gestion_header(self):

        self.ui.liste_formule.setColumnHidden(col_favoris_formule_formule, True)
        self.ui.liste_formule.setColumnHidden(col_favoris_formule_famille, True)

    def current_formula_find(self) -> str:

        qm_formule = self.recherche_current_qmodelindex(mapping=True)

        if qm_formule is None:
            return ""

        formula_name = qm_formule.data()

        if formula_name is None:
            return ""

        return formula_name

    def onglet_renamed(self, nouveau_titre: str, formula_name: str):

        self.filtre_famille.setFilterRegExp(nouveau_titre)

        self.recherche_formule_titre(formula_name=formula_name)

    def combo_families_load(self, ancien_titre: str, nouveau_titre: str):

        current_text = self.ui.combo_famille.currentText()

        if current_text == ancien_titre:
            current_text = nouveau_titre

        self.ui.combo_famille.blockSignals(True)
        self.ui.combo_famille.clear()
        self.ui.combo_famille.addItems(self.widget_onglet.tabs_list)

        self.ui.combo_famille.setCurrentText(current_text)
        self.ui.combo_famille.blockSignals(False)

    @staticmethod
    def a___________________changement_titre_______________():
        pass

    def verification(self) -> bool:

        nouveau_texte = self.ui.titre.text()

        if nouveau_texte == "":
            self.ui.titre.setStyleSheet("QLineEdit{border: 2px solid orange; "
                                        "border-top-left-radius: 5px;  "
                                        "border-bottom-left-radius: 5px; "
                                        "padding-left: 5px; }")

            self.ui.bt_verif_titre.setIcon(get_icon(error_icon))
            self.ui.bt_verif_titre.setToolTip(self.tr("Impossible de laisser ce titre sans texte."))
            return False

        current_index: QModelIndex = self.ui.liste_formule.currentIndex()
        current_texte = current_index.data()

        recherche = self.formulas_fav_model.findItems(nouveau_texte, Qt.MatchContains, col_favoris_formule_titre)

        filtereditems = [item for item in recherche if item.text().lower() == nouveau_texte.lower()]

        if len(filtereditems) != 0:

            if current_texte != nouveau_texte:
                self.ui.titre.setStyleSheet("QLineEdit{border: 2px solid orange; "
                                            "border-top-left-radius: 5px;  "
                                            "border-bottom-left-radius: 5px; "
                                            "padding-left: 5px; }")

                self.ui.bt_verif_titre.setIcon(get_icon(error_icon))
                self.ui.bt_verif_titre.setToolTip(self.tr("Ce titre est déjà utilisé."))
                return False

        self.ui.titre.setStyleSheet("QLineEdit{border: 1px solid #8f8f91; "
                                    "border-right-width: 0px; "
                                    "border-top-left-radius: 5px;  "
                                    "border-bottom-left-radius: 5px; "
                                    "padding-left: 5px; }")

        self.ui.bt_verif_titre.setIcon(get_icon(valid_icon))
        self.ui.bt_verif_titre.setToolTip(self.tr("C'est tout bon!"))
        return True

    def texte_finish(self):

        texte = self.ui.titre.text()

        current_index: QModelIndex = self.recherche_current_qmodelindex()

        if current_index is None:
            return

        current_texte = current_index.data()

        if texte == current_texte:
            return

        valide = self.verification()

        if valide:
            self.filtre_famille.setData(current_index, texte)
        else:
            self.ui.titre.blockSignals(True)
            self.ui.titre.setText(current_texte)

            self.ui.titre.setStyleSheet("QLineEdit{border: 1px solid #8f8f91; "
                                        "border-right-width: 0px; "
                                        "border-top-left-radius: 5px;  "
                                        "border-bottom-left-radius: 5px; "
                                        "padding-left: 5px; }")

            self.ui.bt_verif_titre.setIcon(get_icon(valid_icon))
            self.ui.bt_verif_titre.setToolTip(self.tr("C'est tout bon!"))

            self.ui.titre.blockSignals(False)

        self.modification_en_cours = True

    def afficher_message(self):

        tooltip = self.ui.bt_verif_titre.toolTip()

        if tooltip == self.tr("C'est tout bon!"):

            msg(titre=application_title,
                message=self.tr("Ce titre est correct, pas de soucis!"),
                icone_valide=True)

        else:

            msg(titre=application_title,
                message=f"{tooltip}",
                icone_critique=True)

    def options_afficher(self):

        self.widget_options.formatting_show(current_parent=self.ui.format_bt,
                                            current_text=self.ui.titre.text(),
                                            show_code=False)

    def options_retour_datas(self, nouveau_texte: str):

        self.ui.titre.setText(nouveau_texte)
        self.verification()

    @staticmethod
    def a___________________changement_selection_______________():
        pass

    def changement_selection(self):

        qmodelindex_titre: QModelIndex = self.recherche_current_qmodelindex()

        if qmodelindex_titre is None:
            self.activation(False)
            self.nettoyage()
            return

        self.activation(True)

        titre = qmodelindex_titre.data()

        qmodelindex_famille = self.recherche_qmodelindex(qmodelindex_titre, col_favoris_formule_famille)

        if qmodelindex_famille is None:
            return

        famille = qmodelindex_famille.data()

        qmodelindex_formule = self.recherche_qmodelindex(qmodelindex_titre, col_favoris_formule_formule)

        if qmodelindex_formule is None:
            return

        formule = qmodelindex_formule.data()

        self.ui.titre.blockSignals(True)
        self.ui.titre.setText(titre)
        self.verification()
        self.ui.titre.blockSignals(False)

        current_famille = self.ui.combo_famille.currentText()

        if current_famille != famille:
            self.ui.combo_famille.blockSignals(True)
            self.ui.combo_famille.setCurrentText(famille)
            self.ui.combo_famille.blockSignals(False)

        self.ui.valeur_attr.blockSignals(True)
        self.ui.valeur_attr.setPlainText(formule)
        self.actualisation_formule()
        self.ui.valeur_attr.blockSignals(False)

        self.ui.bt_verif.verification(texte=formule, allplan=self.allplan)

    def formula_select(self, formula_name: str):

        search_start = self.ui.liste_formule.model().index(0, col_favoris_formule_titre)

        search = self.ui.liste_formule.model().match(search_start, Qt.DisplayRole, formula_name, -1, Qt.MatchExactly)

        if len(search) == 0:
            return

        qm = search[0]

        if qm is None:
            return

        self.ui.liste_formule.setCurrentIndex(qm)

    @staticmethod
    def a___________________changement_famille_______________():
        pass

    def changement_famille(self):

        if not self.isVisible():
            return

        qm_famille_actuelle = self.recherche_current_qmodelindex(colonne=col_favoris_formule_famille)

        if qm_famille_actuelle is None:
            return

        qm_formula_actuel = self.recherche_current_qmodelindex()

        if qm_famille_actuelle is None:
            return

        formula_actuel = qm_formula_actuel.data()

        famille_actuelle: str = qm_famille_actuelle.data()

        famille_future: str = self.ui.combo_famille.currentText()

        if famille_actuelle == famille_future:
            return

        self.filtre_famille.setData(qm_famille_actuelle, famille_future)

        liste_onglets = self.widget_onglet.tabs_list

        if famille_future not in liste_onglets:
            return

        index_famille = liste_onglets.index(famille_future)

        self.famille_change.emit(index_famille, formula_actuel)

    @staticmethod
    def a___________________changement_formule_______________():
        pass

    def changement_formule(self):

        if not self.isVisible():
            return

        formule_future = self.ui.valeur_attr.toPlainText()
        self.actualisation_formule()

        qm_formule_actuelle = self.recherche_current_qmodelindex(col_favoris_formule_formule)

        if qm_formule_actuelle is None:
            return

        formule_actuelle = qm_formule_actuelle.data()

        if formule_actuelle == formule_future:
            return

        self.filtre_famille.setData(qm_formule_actuelle, formule_future)

        self.modification_en_cours = True

    def actualisation_formule(self):

        formula = self.ui.valeur_attr.toPlainText()

        self.ui.bt_verif.verification(texte=formula, allplan=self.allplan)

        if self.ui.bt_verif.isvalid:

            self.ui.valeur_attr.setStyleSheet("QPlainTextEdit {border: 1px solid #8f8f91; "
                                              "border-right-width: 0px; "
                                              "padding-left: 5px; "
                                              "padding-right: 5px; "
                                              "padding-top: 1px; "
                                              "padding-bottom: 1px; "
                                              "border-top-left-radius: 5px; "
                                              "border-bottom-left-radius: 5px; }")

        else:

            self.ui.valeur_attr.setStyleSheet("QPlainTextEdit {border: 2px solid orange; "
                                              "padding-left: 4px; "
                                              "padding-right: 3px; "
                                              "padding-top: 0px; "
                                              "padding-bottom: 0px; "
                                              "border-top-left-radius: 5px; "
                                              "border-bottom-left-radius: 5px; }")

        formula_converted = self.allplan.traduction_formule_allplan(formula=formula, format_on=False)

        self.ui.formule_convertie.setText(formula_converted)

        self.translate_formula_change_size(self.ui.valeur_attr.currentsize)

        nb_char = len(formula)

        if nb_char < 2:
            a = self.tr("caractère")
            self.ui.nb_char.setText(f'{nb_char} {a}')
        else:
            a = self.tr("caractères")
            self.ui.nb_char.setText(f'{nb_char} {a}')

    def retour_widget_formule(self, value_widget: QPlainTextEdit, formule: str, position_cursor: int):

        if value_widget != self.ui.valeur_attr:
            return

        self.ui.valeur_attr.setPlainText(formule)

        self.ui.valeur_attr.setFocus()

        cursor = self.ui.valeur_attr.textCursor()
        cursor.setPosition(position_cursor, QTextCursor.MoveAnchor)
        self.ui.valeur_attr.setTextCursor(cursor)

    def liste_formule_menu_afficher(self, point: QPoint):

        menu = MyContextMenu(tooltips_visible=False)

        menu.add_title(title=self.ui.titre_formule.text())

        menu.add_action(qicon=get_icon(add_icon),
                        title=self.tr('Nouveau'),
                        action=self.ajouter_formule)

        liste_selection = self.ui.liste_formule.selectionModel().selectedRows(0)

        nb_element = self.ui.liste_formule.model().rowCount()

        if len(liste_selection) != 0 and nb_element > 1:
            menu.add_action(qicon=get_icon(delete_icon),
                            title=self.tr('Supprimer'),
                            action=self.supprimer_formule)

            menu.add_action(qicon=get_icon(paste_icon),
                            title=self.tr('Dupliquer'),
                            action=self.dupliquer_formule)

        menu.exec_(self.ui.liste_formule.mapToGlobal(point))

    @staticmethod
    def a___________________creation_formule_______________():
        pass

    def ajouter_formule(self):

        famille = self.nom_onglet
        formule = ""

        titre = self.widget_onglet.favoris_fav_model_add(nom_onglet=famille,
                                                         formula_name="",
                                                         formula=formule)

        depart = self.filtre_famille.index(0, col_favoris_formule_titre)

        recherche = self.filtre_famille.match(depart, Qt.DisplayRole, titre, -1, Qt.MatchExactly)

        if len(recherche) != 1:
            return

        qmodelindex_filtre = recherche[0]

        if qmodelindex_filtre.isValid():
            self.ui.liste_formule.setCurrentIndex(qmodelindex_filtre)

        self.modification_en_cours = True

    @staticmethod
    def a___________________gestion_createur_formule______():
        pass

    def ouvrir_createur_formule(self):

        self.widget_creation_formule.show_formula(value_widget=self.ui.valeur_attr,
                                                  parent_actuel=self,
                                                  bt_favoris=False)

        self.widget_formule_visible = True

    def fermeture_formule(self):
        self.ui.valeur_attr.autocompletion.hide()
        self.widget_formule_visible = False

    @staticmethod
    def a___________________supprimer_formule_______________():
        pass

    def supprimer_formule(self):

        current_index = self.recherche_current_qmodelindex(mapping=True)

        if current_index is None:
            return

        current_row = current_index.row()

        if msg(titre=application_title,
               message=self.tr("Voulez-vous supprimer ce favoris formule?"),
               type_bouton=QMessageBox.Ok | QMessageBox.Cancel,
               defaut_bouton=QMessageBox.Ok,
               icone_question=True) == QMessageBox.Cancel:
            return

        self.formulas_fav_model.takeRow(current_row)

        self.modification_en_cours = True

    @staticmethod
    def a___________________dupliquer_formule_______________():
        pass

    def dupliquer_formule(self):

        current_index = self.recherche_current_qmodelindex(mapping=False)

        if current_index is None:
            return

        current_row = current_index.row()

        qm_title = self.filtre_famille.index(current_row, col_favoris_formule_titre)

        if not qm_check(qm_title):
            return

        qm_family = self.filtre_famille.index(current_row, col_favoris_formule_famille)

        if not qm_check(qm_family):
            return

        qm_formula = self.filtre_famille.index(current_row, col_favoris_formule_formule)

        if not qm_check(qm_formula):
            return

        title = qm_title.data()

        if not isinstance(title, str):
            return

        family = qm_family.data()

        if not isinstance(family, str):
            return

        formula = qm_formula.data()

        if not isinstance(formula, str):
            return

        formula_titles_list = self.widget_onglet.formulas_lister_titre(upper=True)

        if not isinstance(formula_titles_list, list):
            return

        title = find_new_title(base_title=title, titles_list=formula_titles_list)

        self.widget_onglet.favoris_fav_model_add(nom_onglet=family,
                                                 formula_name=title,
                                                 formula=formula)

        search_start = self.filtre_famille.index(0, col_favoris_formule_titre)

        search = self.filtre_famille.match(search_start, Qt.DisplayRole, title, -1, Qt.MatchExactly)

        if len(search) != 1:
            return

        qmodelindex_filtre = search[0]

        if qmodelindex_filtre.isValid():
            self.ui.liste_formule.setCurrentIndex(qmodelindex_filtre)

        self.modification_en_cours = True

    @staticmethod
    def a___________________outils_______________():
        pass

    def translate_formula_change_size(self, current_size: int):

        current_font = self.ui.formule_convertie.font()
        current_font.setPointSize(current_size)
        self.ui.formule_convertie.setFont(current_font)

    def recherche_current_qmodelindex(self, colonne=col_favoris_formule_titre, mapping=False):

        liste_selection = self.ui.liste_formule.selectionModel().selectedRows(colonne)

        if len(liste_selection) == 0:
            return None

        qmodelindex: QModelIndex = liste_selection[0]

        if not qm_check(qmodelindex):
            return None

        if not mapping:
            return qmodelindex

        model_actuel = qmodelindex.model()

        if model_actuel == self.formulas_fav_model:
            return qmodelindex

        qmodelindex_model = self.filtre_famille.mapToSource(qmodelindex)

        if not qm_check(qmodelindex_model):
            return None

        return qmodelindex_model

    def recherche_qmodelindex(self, qmodelindex: QModelIndex, colonne: int):

        if not qm_check(qmodelindex):
            return None

        current_row: int = qmodelindex.row()

        qm_actuelle: QModelIndex = self.filtre_famille.index(current_row, colonne)

        if not qm_check(qm_actuelle):
            return None

        return qm_actuelle

    def recherche_formule_titre(self, formula_name: str, selectionner=True):

        start = self.filtre_famille.index(0, col_favoris_formule_titre)

        if formula_name == "":
            if selectionner:
                self.ui.liste_formule.setCurrentIndex(start)
            return start

        recherche = self.filtre_famille.match(start, Qt.DisplayRole, formula_name, -1, Qt.MatchExactly)

        if len(recherche) == 0:
            if selectionner:
                self.ui.liste_formule.setCurrentIndex(start)
            return start

        if selectionner:
            self.ui.liste_formule.setCurrentIndex(recherche[0])

        return recherche[0]

    @staticmethod
    def a___________________event______():
        pass

    def paintEvent(self, event: QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

        super().paintEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj != self.ui.combo_famille:
            return super().eventFilter(obj, event)

        if event.type() == QEvent.Wheel:
            if not self.ui.combo_famille.hasFocus():
                event.ignore()
                return True
            else:
                event.accept()
                return super().eventFilter(obj, event)

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass


class FormulaFavoriteModify(QWidget):
    appliquer_modifications = pyqtSignal(str, str, str)

    def __init__(self, parent_actuel, allplan: AllplanDatas):
        super().__init__(parent=parent_actuel)

        # Définition du widget en popup
        self.setWindowFlags(Qt.Popup)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        # Création de l'interface
        self.ui = Ui_FormulaFavoriteModify()
        self.ui.setupUi(self)

        # Définition des variables
        self.liste_onglets = list()
        self.ancien_titre = str()

        self.allplan = allplan
        self.icone_actuel = str()

        self.choix_icone_actif = False

        self.ui.onglet_texte.textEdited.connect(self.verification)

        self.ui.icone.clicked.connect(self.choisir_icone)
        self.ui.icone_clear.clicked.connect(self.supprimer_icone)

        self.ui.bt_enregistrer.clicked.connect(self.enregistrer)
        self.ui.bt_quitter.clicked.connect(self.close)

    def formulas_fav_personnaliser(self, nom_onglet: str, icone_onglet: str, liste_onglets: list):

        self.ancien_titre = nom_onglet
        self.ui.onglet_texte.setText(nom_onglet)

        self.icone_actuel = icone_onglet
        self.ui.icone.setIcon(get_icon(icone_onglet))

        self.liste_onglets = liste_onglets

        self.show()

        self.verification()

        self.ui.onglet_texte.selectAll()
        self.ui.onglet_texte.setFocus()

    def verification(self):
        """ Vérification si le nouveau titre de l'onglet est valide
        :return: Si Valide => True sinon False
        """

        # Définition du nouveau titre de l'onglet
        nouveau_texte = self.ui.onglet_texte.text()

        # Si le nouveau titre est différent de l'ancien
        if nouveau_texte != self.ancien_titre:

            if nouveau_texte.strip() == "":
                tooltips = self.tr("Vous ne pouvez pas laisser le titre vide.")

                self.ui.onglet_texte.setStyleSheet("QLineEdit{"
                                                   "border: 1px solid #8f8f91; "
                                                   "border-radius:5px ; "
                                                   "background-color: orange;}")

                self.ui.bt_enregistrer.setToolTip(tooltips)
                self.ui.bt_enregistrer.setEnabled(False)
                return False

            if nouveau_texte in self.liste_onglets:
                tooltips = self.tr("Ce titre est déjà utilisé.")

                self.ui.onglet_texte.setStyleSheet("QLineEdit{"
                                                   "border: 1px solid #8f8f91; "
                                                   "border-radius:5px ; "
                                                   "background-color: orange;}")

                self.ui.bt_enregistrer.setToolTip(tooltips)
                self.ui.bt_enregistrer.setEnabled(False)
                return False

        self.ui.onglet_texte.setStyleSheet("QLineEdit{"
                                           "border: 1px solid #8f8f91; "
                                           "border-radius:5px ; "
                                           "background-color: #FFFFFF}")

        self.ui.bt_enregistrer.setToolTip("")
        self.ui.bt_enregistrer.setEnabled(True)

        return True

    def choisir_icone(self):
        """ Permet de choisir une icone pour l'onglet
        :return:
        """

        # Information que l'utilisateur est en train de choisir une icone -> conservation des données
        self.choix_icone_actif = True

        nom_fichier = os.path.basename(self.icone_actuel)

        if self.icone_actuel.startswith(":/Images/"):
            icone = icons_path
        else:
            icone = self.icone_actuel

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [icons_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path]
        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[app_setting_file, "path_icons"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={self.tr("Fichier image"): [".png", ".jpg"]},
                                 current_path=icone,
                                 default_path="",
                                 file_name=nom_fichier,
                                 use_setting_first=False)

        # # Information que l'utilisateur a choisi une icone ou quitter le menu
        self.choix_icone_actif = False

        if file_path == "":
            return

        # Définition de la nouvelle icone
        self.icone_actuel = file_path

        # Affichage de la nouvelle icone.
        self.ui.icone.setIcon(get_icon(file_path))

    def supprimer_icone(self):
        """Permet de supprimer l'icone choisie"""

        # Définition de la nouvelle icone
        self.icone_actuel = ""

        # Affichage de la nouvelle icone.
        self.ui.icone.setIcon(QIcon())

    def enregistrer(self):
        """Envoi des informations"""

        # Vérification que le titre soit valide
        if self.verification():
            nouveau_texte = self.ui.onglet_texte.text()

            # Envoi de informations
            self.appliquer_modifications.emit(self.ancien_titre, nouveau_texte, self.icone_actuel)

            # Fermeture de la fenêtre
            self.close()

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:

            self.enregistrer()

        elif event.key() == Qt.Key_Escape:

            self.close()

    def closeEvent(self, event: QEvent):

        if self.choix_icone_actif:
            event.ignore()
            return

        else:
            self.ancien_titre = str()
            self.icone_actuel = str()
            self.ui.onglet_texte.setStyleSheet("")
            self.ui.onglet_texte.setToolTip(self.tr("Titre valide"))

        super().closeEvent(event)


class FormulaFavoriteTabBar(QTabBar):
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

        nb_tab = self.count()

        for index_tab in range(nb_tab - 1):

            current_button = self.tabButton(index_tab, QTabBar.RightSide)

            if not isinstance(current_button, QPushButton):
                continue

            if current_button == button:
                self.del_signal.emit(index_tab)
                return

    def gestion_first_button(self):

        bouton = self.tabButton(0, QTabBar.RightSide)

        if not isinstance(bouton, QPushButton):
            return

        nb_tab = self.count()

        if nb_tab <= 2:
            bouton.setEnabled(False)
        else:
            bouton.setEnabled(True)

    @staticmethod
    def a___________________event______():
        pass

    def tabSizeHint(self, current_index: int):
        size = super().tabSizeHint(current_index)

        if current_index == self.count() - 1:
            return QSize(40, size.height())

        elif size.width() < 110:
            size = QSize(110, size.height())

        return size

    def tabInserted(self, current_index: int):
        super().tabInserted(current_index)

        nb_tab = self.count()

        if current_index == nb_tab - 1:
            return

        bouton = self.tabButton(0, QTabBar.RightSide)

        if isinstance(bouton, QPushButton):
            bouton.setEnabled(True)

        close_button = QPushButton(self)
        close_button.setFlat(True)
        close_button.setMinimumHeight(24)

        close_button.setIcon(get_icon(windows_close_hover_icon))
        close_button.setStyleSheet("QPushButton:hover {border: 1px solid #8f8f91; border-radius:5px; }")

        close_button.clicked.connect(lambda: self.del_tab(close_button))

        self.setTabButton(current_index, QTabBar.RightSide, close_button)

    def tabRemoved(self, current_index: int):
        super().tabRemoved(current_index)
        self.gestion_first_button()

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

        if tab_current_index in [nb_tab - 1]:
            return

        tab_current_rect = self.tabRect(tab_current_index)

        if not isinstance(tab_current_rect, QRect):
            return

        self.tab_first_movable_pos = tab_first_movable_rect.x() + 15
        self.tab_last_movable_pos = tab_last_movable_rect.x()
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

        self.setTabVisible(self.count() - 1, False)

        tab_moved_start = event.pos().x() - self.decal_l
        tab_moved_end = event.pos().x() + self.decal_w

        if tab_moved_start <= self.tab_first_movable_pos:
            return

        if tab_moved_end >= self.tab_last_movable_pos:
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):

        super().mouseReleaseEvent(event)

        self.setTabVisible(self.count() - 1, True)

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
