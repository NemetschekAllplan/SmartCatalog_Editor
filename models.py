#!/usr/bin/python3
# -*- coding: utf-8 -*

import os.path

from allplan_manage import *
from attribute_add import AttributesWidget
from hierarchy import material_code, component_code, attribute_code
from tools import find_folder_path, get_look_tableview, qm_check, MyContextMenu, read_file_to_text
from tools import model_verification, settings_save, move_window_tool, find_new_title, favorites_import_verification
from tools import recherche_image, make_backup, settings_get, find_filename, settings_read, browser_file
from ui_model import Ui_Model
from ui_model_modify import Ui_ModelModify
from ui_model_tab import Ui_ModelTab
from ui_model_tab_del import Ui_ModelTabDel

col_opt_numero = 0
col_opt_nom = 1
depart_onglet = 2

prefix = "attributs_"
extension = ".csv"


class Models(QWidget):

    def __init__(self, asc):
        super().__init__()

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------
        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        # -----------------------------------------------
        # Création de l'interface
        # -----------------------------------------------
        self.ui = Ui_Model()
        self.ui.setupUi(self)

        self.ui.onglet.setTabBar(ModelsTabBar())

        # -----------------------------------------------
        # read settings
        # -----------------------------------------------

        model_settings = settings_read(model_setting_file)

        self.ismaximized_on = model_settings.get("ismaximized_on", model_setting_datas.get("ismaximized_on", False))

        if not isinstance(self.ismaximized_on, bool):
            self.ismaximized_on = model_setting_datas.get("ismaximized_on", False)

        width = model_settings.get("width", model_setting_datas.get("width", 800))

        if not isinstance(width, int):
            width = model_setting_datas.get("width", 800)

        height = model_settings.get("height", model_setting_datas.get("height", 800))

        if not isinstance(height, int):
            height = model_setting_datas.get("height", 800)

        self.resize(width, height)

        model_clipboard = model_settings.get("clipboard", list())

        if not isinstance(model_clipboard, list):
            self.model_clipboard = list()
        else:
            self.model_clipboard = self.attribute_list_analyse(model_clipboard)

        # -----------------------------------------------

        self.liste_onglets = list()

        # -----------------------------------------------
        # Allplan datas
        # -----------------------------------------------

        self.allplan: AllplanDatas = self.asc.allplan

        # -----------------------------------------------
        # Widget modifier un onglet
        # -----------------------------------------------

        self.model_tab_modify = ModelsTabModify(self.ui.onglet, self.allplan)

        self.model_tab_modify.appliquer_modifications.connect(self.onglet_renommer_action)

        self.asc.langue_change.connect(
            lambda main=self.model_tab_modify: self.model_tab_modify.ui.retranslateUi(main))

        # -----------------------------------------------
        # Widget supprimer un onglet
        # -----------------------------------------------

        self.model_tab_del = ModelsTabDel(self.ui.onglet)
        self.model_tab_del.validation_supprimer.connect(self.onglet_suppression_action)

        # -----------------------------------------------
        # Signaux onglet
        # -----------------------------------------------

        self.ui.onglet.tabBarClicked.connect(self.onglet_simple_clic)
        self.ui.onglet.tabBarDoubleClicked.connect(self.onglet_double_clic)
        tab_bar: ModelsTabBar = self.ui.onglet.tabBar()

        tab_bar.del_signal.connect(self.onglet_suppression)
        tab_bar.move_signal.connect(self.onglet_deplacement)

        # -----------------------------------------------
        # Autres boutons
        # -----------------------------------------------

        self.ui.bt_enregistrer.clicked.connect(self.model_save)
        self.ui.bt_quitter.clicked.connect(self.close)

        self.change_made = False

        self.ui.onglet.customContextMenuRequested.connect(self.onglet_afficher_menu)

    @staticmethod
    def a___________________loading______():
        pass

    def model_personnaliser(self, type_element=None, nom_onglet=""):

        """Permet de selectionner le type de pourtour de salle"""

        # self.add_tab_button.setText(self.tr(' Nouveau'))

        self.ui.onglet.blockSignals(True)

        self.ui.onglet.clear()
        self.liste_onglets.clear()

        self.ui.onglet.blockSignals(False)

        self.onglets_chargement()

        tab_index = settings_get(model_setting_file, "tab_index")

        if not isinstance(tab_index, int):
            tab_index = 0

        if tab_index < 0:
            tab_index = 0

        nb_tab = self.ui.onglet.count()

        if type_element == component_code:
            default_tab = 1
        else:
            default_tab = 0

        if nb_tab == 3:
            tab_index = default_tab

        elif tab_index < 0:
            tab_index = default_tab

        if tab_index > self.ui.onglet.count() - 2:
            tab_index = self.ui.onglet.count() - 2

        if nom_onglet != "" and nom_onglet in self.liste_onglets:
            tab_index = self.liste_onglets.index(nom_onglet)

        self.ui.onglet.setCurrentIndex(tab_index)

        move_window_tool(widget_parent=self.asc, widget_current=self)

        if self.ismaximized_on:

            self.showMaximized()
        else:
            self.show()

    @staticmethod
    def a___________________onglet_menu______():
        pass

    def onglet_afficher_menu(self, point: QPoint):

        index_onglet = self.ui.onglet.tabBar().tabAt(point)

        if index_onglet == self.ui.onglet.count() - 1:
            return

        if index_onglet == 0 or index_onglet == 1 or index_onglet == -1:
            menu = MyContextMenu()

            menu.add_title(title=self.windowTitle())

            menu.add_action(qicon=get_icon(add_icon),
                            title=self.tr('Nouveau'),
                            action=self.onglet_ajouter)

            menu.exec_(self.ui.onglet.mapToGlobal(point))

            return

        widget_onglet = self.ui.onglet.widget(index_onglet)

        if self.ui.onglet.currentIndex() != index_onglet:
            self.ui.onglet.setCurrentIndex(index_onglet)

        if not isinstance(widget_onglet, ModelsTab):
            print("WidgetModels -- onglet_afficher_menu -- not isinstance(widget_onglet, WidgetModelsTab)")
            return

        menu = MyContextMenu()
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
    def a___________________config_chargement_______________():
        pass

    def model_config_chargement(self):

        config = settings_read(model_config_file)

        dict_elements = dict(settings_names.get(model_config_file, dict()))

        for nom_onglet_original, data_onglet in config.items():

            if not isinstance(nom_onglet_original, str) or not isinstance(data_onglet, dict):
                continue

            if nom_onglet_original != material_code and nom_onglet_original != component_code:

                type_onglet: str = data_onglet.get("type", "")

                if type_onglet.capitalize() != material_code and type_onglet.capitalize() != component_code:
                    continue

                icone_onglet: str = recherche_image(data_onglet.get("icon", ""), f"{type_onglet.lower()}.png")

                order = data_onglet.get("order", 0)
                order_col = data_onglet.get("order_col", 0)

                liste_attributs = self.attribute_list_analyse(data_onglet.get("attributes"))

                dict_elements[nom_onglet_original] = {"icon": icone_onglet,
                                                      "type": type_onglet.capitalize(),
                                                      "order": order,
                                                      "order_col": order_col,
                                                      "attributes": liste_attributs}
            else:

                liste_attributs = self.attribute_list_analyse(data_onglet.get("attributes"))

                if nom_onglet_original == material_code:
                    nom_onglet = self.tr("Ouvrage")

                elif nom_onglet_original == component_code:
                    nom_onglet = self.tr("Composant")

                else:
                    continue

                if nom_onglet in dict_elements:
                    dict_elements[nom_onglet]["attributes"] = liste_attributs
                    continue

                if nom_onglet_original in dict_elements:
                    dict_elements[nom_onglet_original]["attributes"] = liste_attributs
                    dict_elements[nom_onglet] = dict_elements.pop(nom_onglet_original)

        return dict_elements

    @staticmethod
    def a___________________onglet_chargement_______________():
        pass

    def onglet_ajouter_button_add(self):
        self.ui.onglet.addTab(QWidget(), get_icon(add_icon), "")

    def onglets_chargement(self):

        dict_elements = self.model_config_chargement()

        self.onglet_ajouter_button_add()

        for nom_onglet, data_onglet in dict_elements.items():
            icone_onglet: str = data_onglet.get("icon", "")
            type_onglet: str = data_onglet.get("type", "")
            order: int = data_onglet.get("order", 0)
            order_col: int = data_onglet.get("order_col", 0)
            liste_attributs = data_onglet.get("attributes")

            self.ajouter_onglet_action(title=nom_onglet,
                                       icone_onglet=icone_onglet,
                                       type_onglet=type_onglet,
                                       liste_attributs=liste_attributs,
                                       tab_index=-1,
                                       order=order,
                                       order_col=order_col,
                                       save=False)

        self.change_made = False

    @staticmethod
    def a___________________onglet_ajouter_______________():
        pass

    def onglet_ajouter(self):

        nom_onglet = ""
        icone_onglet = material_icon
        type_onglet = material_code
        index_insertion = - 1

        nom_onglet = self.ajouter_onglet_action(title=nom_onglet,
                                                icone_onglet=icone_onglet,
                                                type_onglet=type_onglet,
                                                liste_attributs=[],
                                                tab_index=index_insertion,
                                                order=0,
                                                order_col=0,
                                                save=False)

        self.onglet_ajouter_afficher_menu(nom_onglet=nom_onglet,
                                          icone_onglet=icone_onglet,
                                          type_onglet=type_onglet,
                                          index_insertion=index_insertion)

    def onglet_ajouter_afficher_menu(self, nom_onglet: str, icone_onglet: str, type_onglet: str,
                                     index_insertion: int):

        # Définition de l'index d'insertion dans la liste
        if index_insertion == -1:
            index_insertion = self.ui.onglet.count() - 2

        self.onglet_placement_widget(index_insertion, self.model_tab_modify)
        self.model_tab_modify.model_modifier_personnaliser(nom_onglet=nom_onglet,
                                                           icone_onglet=icone_onglet,
                                                           type_onglet=type_onglet,
                                                           liste_onglets=self.liste_onglets)

    def ajouter_onglet_action(self, title="", icone_onglet="", type_onglet="", liste_attributs=None,
                              tab_index=-1, order=0, order_col=0, save=True) -> str:

        if title == "":
            title = self.tr("Modèle")

        title = find_new_title(base_title=title, titles_list=self.liste_onglets)

        if type_onglet == "":
            type_onglet = material_code

        if icone_onglet == "":
            icone_onglet = f":/Images/{type_onglet.lower()}.png"
        else:
            icone_onglet = recherche_image(icone_onglet, f"{type_onglet.lower()}.png")

        # Définition de l'index d'insertion dans la liste
        if tab_index == -1:
            tab_index = len(self.liste_onglets)

        if liste_attributs is None:
            liste_attributs = list()

        # Création d'un nouvel onglet
        tab = ModelsTab(asc=self.asc,
                        widget_onglet=self,
                        nom_onglet=title,
                        icone_onglet=icone_onglet,
                        type_onglet=type_onglet,
                        attributes_list=liste_attributs,
                        order=order,
                        order_col=order_col)

        self.asc.langue_change.connect(lambda main=tab: tab.ui.retranslateUi(main))

        # Ajout de l'onglet
        self.ui.onglet.insertTab(tab_index, tab, get_icon(icone_onglet), title)

        if tab_index <= 6:
            self.ui.onglet.setTabToolTip(tab_index, f"{title} (F{tab_index + 6})")
        else:
            self.ui.onglet.setTabToolTip(tab_index, title)

        # Définition du nouvel onglet comme l'onglet utilisé
        self.ui.onglet.setCurrentIndex(tab_index)

        # Mise à jour de la liste des onglets
        self.liste_onglets.insert(tab_index, title)

        if not save:
            self.change_made = True
            return title

        if self.isVisible():
            self.change_made = True
        else:
            self.model_save()

        return title

    @staticmethod
    def a___________________onglet_supprimer_______________():
        pass

    def onglet_suppression(self, current_index: int):
        """ Gestion de la suppression d'un onglet
        :param current_index: information envoyée par le programme informant l'index de l'onglet qui sera supprimé
        :return: None
        """

        if self.ui.onglet.count() <= 3:
            return

        # Définition du titre de l'onglet
        titre_onglet = self.ui.onglet.tabText(current_index)

        if titre_onglet not in self.liste_onglets:
            print("widget_model -- suppression_onglet -- titre_onglet not in self.liste_onglets")
            return

        self.onglet_placement_widget(current_index, self.model_tab_del)
        self.model_tab_del.del_ask_show(tab_index=current_index)

    def onglet_suppression_action(self, current_index):

        nom_onglet = self.ui.onglet.tabText(current_index)

        self.liste_onglets.remove(nom_onglet)

        self.ui.onglet.removeTab(current_index)

        if self.ui.onglet.currentIndex() == self.ui.onglet.count() - 1:
            self.ui.onglet.setCurrentIndex(self.ui.onglet.count() - 2)

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

    def onglet_renommer_action(self, ancien_titre: str, title: str, nouvelle_icone: str, type_onglet: str):

        tab_index = self.ui.onglet.currentIndex()
        ancien_index = self.liste_onglets.index(ancien_titre)

        widget = self.ui.onglet.currentWidget()

        if not isinstance(widget, ModelsTab):
            return

        if ancien_titre != title:
            self.liste_onglets[ancien_index] = title

            self.ui.onglet.setTabText(tab_index, title)

            if tab_index <= 6:
                self.ui.onglet.setTabToolTip(tab_index, f"{title} (F{tab_index + 6})")
            else:
                self.ui.onglet.setTabToolTip(tab_index, title)

            widget.nom_onglet = title

            self.change_made = True

        icone_actuelle = widget.icone_onglet

        if icone_actuelle != nouvelle_icone:
            widget.icone_onglet = nouvelle_icone

            self.ui.onglet.setTabIcon(tab_index, get_icon(nouvelle_icone))

            self.change_made = True

        type_actuelle = widget.type_onglet

        if type_actuelle != type_onglet:
            widget.type_onglet = type_onglet

            self.change_made = True

    def onglet_renommer_afficher(self, index_onglet: int, widget_onglet):

        if not isinstance(widget_onglet, ModelsTab):
            return

        if self.ui.onglet.currentIndex() != index_onglet:
            self.ui.onglet.setCurrentIndex(index_onglet)

        self.onglet_placement_widget(index_onglet, self.model_tab_modify)

        self.model_tab_modify.model_modifier_personnaliser(nom_onglet=widget_onglet.nom_onglet,
                                                           icone_onglet=widget_onglet.icone_onglet,
                                                           type_onglet=widget_onglet.type_onglet,
                                                           liste_onglets=self.liste_onglets)

    @staticmethod
    def a___________________onglet_deplacement_______________():
        pass

    def onglet_deplacement(self, _, index_arrivee: int):

        # Définition du titre de l'onglet
        titre_onglet = self.ui.onglet.tabText(index_arrivee)

        # Vérification que le titre de l'onglet est bien dans le datas des onglets
        if titre_onglet not in self.liste_onglets:
            return

        self.liste_onglets.remove(titre_onglet)

        self.liste_onglets.insert(index_arrivee, titre_onglet)

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

    def onglet_simple_clic(self, current_index: int):

        last_tab = self.ui.onglet.count() - 1

        if current_index == last_tab:
            self.onglet_ajouter()
            return

        self.ui.onglet.setMovable(current_index != 0 and current_index != 1)

        widget: ModelsTab = self.ui.onglet.widget(current_index)

        if not isinstance(widget, ModelsTab):
            return

        widget.gestion_header()
        widget.gestion_bouton()

    def onglet_double_clic(self, index_onglet: int):
        """Gestion du double clic sur le ui.onglet
        :param index_onglet: information envoyée par le programme informant l'index du double clic -> -1 si aucun onglet
        :return: None
        """

        # Vérification si aucun onglet n'a été double cliqué
        if index_onglet == -1:
            self.onglet_ajouter()
            return

        # Vérification que l'onglet double cliqué n'est pas un onglet protégé -> return
        if index_onglet < depart_onglet:
            return

        widget = self.ui.onglet.currentWidget()

        if not isinstance(widget, ModelsTab):
            return

        self.onglet_renommer_afficher(index_onglet=index_onglet, widget_onglet=widget)

    @staticmethod
    def a___________________outils_______________():
        pass

    def recherche_type_element(self, type_element: str):

        config = self.model_config_chargement()

        titre_sans_attribut = self.tr("Sans attribut")
        titre_liste = self.tr("Liste des attributs")
        dict_elements = dict()

        if type_element != attribute_code:
            dict_elements[titre_sans_attribut] = none_icon, self.tr("Aucun attribut")

        for nom_onglet, data_onglet in config.items():

            type_onglet: str = data_onglet.get("type", material_code)

            type_onglet = type_onglet.capitalize()

            if type_element != attribute_code and type_element != type_onglet:
                continue

            icone_onglet: str = recherche_image(data_onglet.get("icon", ""), f"{type_onglet.lower()}.png")

            liste_attributs = self.attribute_list_analyse(data_onglet.get("attributes"))

            if len(liste_attributs) != 0:
                tooltips = "\n".join(liste_attributs)
                tooltips = f"{titre_liste} :\n{tooltips}"

            else:
                none_txt = self.tr("Aucun attribut")
                tooltips = f"{titre_liste} : {none_txt}"

            dict_elements[nom_onglet] = icone_onglet, tooltips

        return dict_elements

    @staticmethod
    def attribute_list_analyse(attributes_list: list):

        if not isinstance(attributes_list, list):
            return list()

        if len(attributes_list) == 0:
            return list()

        new_attributes_list = list()

        for number in attributes_list:

            try:
                number = str(int(number))
            except Exception:
                continue

            if number in new_attributes_list:
                continue

            if len(number) > 5:
                continue

            if number in ["0", "83", "207"]:
                continue

            if number in attribute_val_default_layer:
                new_attributes_list.extend(list(attribute_val_default_layer))
                continue

            if number in attribute_val_default_fill:
                new_attributes_list.extend(list(attribute_val_default_fill))
                continue

            if number in attribute_val_default_room:
                new_attributes_list.extend(list(attribute_val_default_room))
                continue

            new_attributes_list.append(number)

        return new_attributes_list

    def creation_liste_attributs(self, tab_name: str) -> list:

        if tab_name == self.tr("Sans attribut"):
            return list()

        model_datas = self.model_config_chargement()

        tab_datas = model_datas.get(tab_name, dict())

        if len(tab_datas) == 0:
            return list()

        attributes_list = tab_datas.get("attributes", list())

        return attributes_list

    @staticmethod
    def a___________________sauvegarde_fichier_config_______________():
        pass

    def model_save_check(self) -> bool:

        if self.change_made:
            return True

        for index_tab in range(self.ui.onglet.count()):

            widget: ModelsTab = self.ui.onglet.widget(index_tab)

            if not isinstance(widget, ModelsTab):
                continue

            if widget.modification_en_cours:
                return True

        return False

    def model_save(self):

        self.model_save_setting(saved=True)
        self.model_save_config()

        self.change_made = False

        self.close()

    def model_save_setting(self, saved: bool):

        datas_config = settings_read(file_name=model_setting_file)

        if saved:
            datas_config["tab_index"] = self.ui.onglet.currentIndex()

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True
                datas_config["clipboard"] = self.model_clipboard

                settings_save(file_name=model_setting_file, config_datas=datas_config)
                return

        datas_config["height"] = self.size().height()
        datas_config["width"] = self.size().width()
        datas_config["ismaximized_on"] = False
        datas_config["clipboard"] = self.model_clipboard

        settings_save(file_name=model_setting_file, config_datas=datas_config)

    def model_save_config(self):

        datas_elements = dict()

        for index_tab in range(self.ui.onglet.count()):

            widget: ModelsTab = self.ui.onglet.widget(index_tab)

            if not isinstance(widget, ModelsTab):
                continue

            nom_onglet = widget.nom_onglet

            if nom_onglet == self.tr("Ouvrage"):
                nom_onglet = material_code
                icone_onglet = "material.png"
            elif nom_onglet == self.tr("Composant"):
                nom_onglet = component_code
                icone_onglet = "component.png"
            else:
                icone_onglet = self.icone_supprimer_path(widget.icone_onglet)

            type_onglet = widget.type_onglet
            liste_attributs = widget.creation_liste_model()

            order = widget.order
            order_col = widget.order_col

            datas_elements[nom_onglet] = {"icon": icone_onglet,
                                          "order": order,
                                          "order_col": order_col,
                                          "type": type_onglet,
                                          "attributes": liste_attributs}

            widget.modification_en_cours = False

        settings_save(model_config_file, datas_elements)

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
            self.model_save()
            return

        if event.key() == Qt.Key_F2:
            current_index = self.ui.onglet.currentIndex()

            if current_index == 0 or current_index == 1:
                return

            self.onglet_double_clic(self.ui.onglet.currentIndex())
            return

        if event.key() == Qt.Key_Escape:
            self.close()
            return

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

        if self.model_save_check():
            if msg(titre=self.windowTitle(),
                   message=self.tr("Voulez-vous enregistrer les modifications?"),
                   type_bouton=QMessageBox.Ok | QMessageBox.No,
                   defaut_bouton=QMessageBox.Ok,
                   icone_sauvegarde=True) == QMessageBox.Ok:
                self.model_save_config()
            else:
                saved = False

        self.model_save_setting(saved=saved)

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class ModelsTab(QWidget):

    def __init__(self, asc, widget_onglet, nom_onglet: str, icone_onglet: str, type_onglet: str,
                 attributes_list: list, order=0, order_col=0):

        super().__init__()

        # Création de l'interface
        self.ui = Ui_ModelTab()
        self.ui.setupUi(self)

        get_look_tableview(self.ui.liste_items)

        self.asc = asc
        self.allplan: AllplanDatas = self.asc.allplan
        self.widget_models: Models = widget_onglet

        self.widget_attribut: AttributesWidget = self.asc.attributes_widget

        self.nom_onglet = nom_onglet
        self.icone_onglet = icone_onglet
        self.type_onglet = type_onglet

        self.order = order
        self.order_col = order_col

        # -----------------------------------------------
        #  model
        # -----------------------------------------------

        self.tab_attributes_model = QStandardItemModel()

        self.attributes_filter = QSortFilterProxyModel()
        self.attributes_filter.setSourceModel(self.tab_attributes_model)
        self.attributes_filter.setSortLocaleAware(True)
        self.attributes_filter.setSortRole(Qt.UserRole)
        self.attributes_filter.setSortCaseSensitivity(Qt.CaseInsensitive)

        self.ui.liste_items.setModel(self.attributes_filter)

        self.charger_model(numbers_list=attributes_list)

        # -----------------------------------------------
        #  Boutons
        # -----------------------------------------------

        self.ui.bt_attributs.clicked.connect(self.ouvrir_attributs)

        self.ui.bt_supprimer.clicked.connect(self.supprimer)

        self.ui.copy_bt.clicked.connect(self.model_copy_attribute)
        self.ui.paste_bt.clicked.connect(self.model_paste_attribute)

        self.ui.bt_exporter.clicked.connect(self.favoris_exporter)

        self.ui.bt_importer.clicked.connect(self.favoris_importer)

        self.ui.liste_items.selectionModel().selectionChanged.connect(self.gestion_bouton)

        self.ui.liste_items.customContextMenuRequested.connect(self.afficher_menu)

        header = self.ui.liste_items.horizontalHeader()

        if header is not None:
            header.sortIndicatorChanged.connect(self.order_changed)

        # -----------------------------------------------
        # connexion ajout attribut
        # -----------------------------------------------

        self.widget_attribut.add_options.connect(self.model_ajouter_attribut)

        self.modification_en_cours = False

        self.gestion_bouton()

    @staticmethod
    def a___________________chargement_donnees______():
        pass

    def charger_model(self, numbers_list: list, reset_model=True):

        list_number_add = list()

        numbers_list = self.widget_models.attribute_list_analyse(numbers_list)

        if reset_model:
            self.tab_attributes_model.clear()
            self.tab_attributes_model.setHorizontalHeaderLabels([self.tr('Numéro'), self.tr('Nom')])
            self.attributes_filter.setSourceModel(self.tab_attributes_model)

        else:

            for index_row in range(self.tab_attributes_model.rowCount()):

                qs = self.tab_attributes_model.item(index_row, col_opt_numero)

                if not isinstance(qs, QStandardItem):
                    continue

                number = qs.text()

                if number is None:
                    continue

                list_number_add.append(number)

        for number in numbers_list:

            if number in list_number_add:
                continue

            list_number_add.append(number)

            qs_list = self.creation_line(number_str=number)

            if len(qs_list) == 0:
                continue

            self.tab_attributes_model.appendRow(qs_list)

        if self.order == 1:
            order = Qt.DescendingOrder
        else:
            order = Qt.AscendingOrder

        self.gestion_header()

        header = self.ui.liste_items.horizontalHeader()

        if header is not None:
            header.setSortIndicator(self.order_col, order)
            self.ui.liste_items.sortByColumn(self.order_col, order)

    def gestion_header(self):
        """

        :return:
        """

        self.ui.bt_exporter.setEnabled(not self.tab_attributes_model.rowCount() == 0)

        header = self.ui.liste_items.horizontalHeader()

        if header is None:
            return

        if header.height() != 24:
            header.setFixedHeight(24)

        header.setSectionResizeMode(col_opt_numero, QHeaderView.ResizeToContents)

    @staticmethod
    def a___________________gestion_menu______():
        pass

    def afficher_menu(self, point: QPoint):

        menu = MyContextMenu()

        # ------------------------------
        # Edition
        # ------------------------------

        if self.ui.bt_attributs.isEnabled() or self.ui.bt_supprimer.isEnabled():
            menu.add_title(title=self.tr("Édition"))

        if self.ui.bt_attributs.isEnabled():
            menu.add_action(qicon=get_icon(attribute_add_icon),
                            title=self.tr("Ajouter attribut"),
                            action=self.ouvrir_attributs)

        if self.ui.bt_supprimer.isEnabled():
            menu.add_action(qicon=get_icon(delete_icon),
                            title=self.tr("Supprimer attribut"),
                            action=self.supprimer)

        if self.ui.copy_bt.isEnabled():
            menu.add_action(qicon=get_icon(copy_icon),
                            title=self.tr("Copier attribut"),
                            action=self.model_copy_attribute)

        if self.ui.paste_bt.isEnabled():
            menu.add_action(qicon=get_icon(paste_icon),
                            title=self.tr("Coller attribut"),
                            action=self.model_paste_attribute)

        # ------------------------------
        # Import/Export
        # ------------------------------

        if self.ui.bt_importer.isEnabled() or self.ui.bt_exporter.isEnabled():
            menu.add_title(title=self.tr("Import / Export"))

        if self.ui.bt_importer.isEnabled():
            menu.add_action(qicon=get_icon(favorite_open_icon),
                            title=self.tr("Importer favoris"),
                            action=self.favoris_importer)

        if self.ui.bt_exporter.isEnabled():
            menu.add_action(qicon=get_icon(favorite_save_icon),
                            title=self.tr("Exporter favoris"),
                            action=self.favoris_exporter)

        menu.exec_(self.ui.liste_items.mapToGlobal(point))

    @staticmethod
    def a___________________gestion_boutons_supprimer______():
        pass

    def gestion_bouton(self):
        """
        Permet de gérer le bouton supprimer d'un ouvrage
        :return: None
        """

        selected_list = self.ui.liste_items.selectionModel().selectedRows()

        if len(selected_list) > 0:
            self.ui.bt_supprimer.setEnabled(True)
            self.ui.copy_bt.setEnabled(True)

        else:
            self.ui.bt_supprimer.setEnabled(False)
            self.ui.copy_bt.setEnabled(False)

        self.ui.bt_exporter.setEnabled(self.ui.liste_items.model().rowCount() > 0)

        paste_txt = self.tr("Coller (CTRL+ V)")

        if len(self.widget_models.model_clipboard) > 0:
            attributes_list_txt = "\n".join(self.widget_models.model_clipboard)

            self.ui.paste_bt.setEnabled(True)
            self.ui.paste_bt.setToolTip(f"{paste_txt}\n{attributes_list_txt}")

        else:

            self.ui.paste_bt.setEnabled(False)
            self.ui.paste_bt.setToolTip(f"{paste_txt}")

    @staticmethod
    def a___________________widget_attributs______():
        pass

    def ouvrir_attributs(self):
        """
        Permet d'ouvrir le widget d'ajout d'attribut
        :return: None
        """

        self.widget_attribut.attribute_show(current_mod="Model",
                                            attributes_list=self.creation_liste_model(),
                                            current_widget=self.widget_models)

    def model_ajouter_attribut(self, numbers_list: list):
        """
        Permet d'ajouter un attribut
        :param numbers_list: liste des numéros attribut à ajouter
        :return: None
        """

        if not self.isVisible():
            return

        if len(numbers_list) == 0:
            return

        self.charger_model(numbers_list=numbers_list, reset_model=False)

        self.modification_en_cours = True

    def creation_line(self, number_str: str) -> list:

        attribute_obj = self.allplan.attributes_dict.get(number_str)

        if not isinstance(attribute_obj, AttributeDatas):
            print("models -- ModelsTab -- creation_line -- not isinstance(attribute_obj, AttributeDatas)")
            return list()

        if attribute_obj.name == "":
            print("models -- ModelsTab -- creation_line -- attribute_obj.name == empty")
            return list()

        try:
            number_attribute_int = int(number_str)
        except Exception:
            print("models -- ModelsTab -- creation_line -- number_str isn't numeric")
            return list()

        qs_number = QStandardItem(number_str)
        qs_number.setData(number_attribute_int, Qt.UserRole)

        qs_name = QStandardItem(attribute_obj.name)
        qs_name.setData(attribute_obj.name, Qt.UserRole)

        return [qs_number, qs_name]

    @staticmethod
    def a___________________suppression_attribut______():
        pass

    def supprimer(self):

        self.ui.liste_items.setFocus()

        qm_selection_list = self.ui.liste_items.selectionModel().selectedRows(0)

        numbers_list = [qm.data() for qm in qm_selection_list if qm_check(qm)]

        for number in numbers_list:

            if number in attribute_val_default_layer:

                for number_sub in attribute_val_default_layer.keys():

                    if number_sub not in numbers_list:
                        numbers_list.append(number_sub)

            if number in attribute_val_default_fill:

                for number_sub in attribute_val_default_fill.keys():

                    if number_sub not in numbers_list:
                        numbers_list.append(number_sub)

            if number in attribute_val_default_room:

                for number_sub in attribute_val_default_room.keys():

                    if number_sub not in numbers_list:
                        numbers_list.append(number_sub)

        for number in numbers_list:

            search_number = self.tab_attributes_model.findItems(number, Qt.MatchExactly, col_opt_numero)

            if len(search_number) == 0:
                continue

            qs = search_number[0]

            if qs is None:
                continue

            current_row = qs.row()

            self.tab_attributes_model.removeRow(current_row)

        self.ui.liste_items.setFocus()

        self.modification_en_cours = True

    @staticmethod
    def a___________________copy_attribute______():
        pass

    def model_copy_attribute(self):

        selected_list = self.ui.liste_items.selectionModel().selectedRows()

        if len(selected_list) == 0:
            return

        self.widget_models.model_clipboard.clear()

        for qm in selected_list:

            if not qm_check(qm):
                continue

            number = qm.data()

            self.widget_models.model_clipboard.append(number)

        self.gestion_bouton()

    @staticmethod
    def a___________________paste_attribute______():
        pass

    def model_paste_attribute(self):

        if len(self.widget_models.model_clipboard) == 0:
            return

        self.model_ajouter_attribut(self.widget_models.model_clipboard)

    @staticmethod
    def a___________________order_change______():
        pass

    def order_changed(self, order_col: int, order: int):

        if not isinstance(order, int) or not isinstance(order_col, int):
            return

        if order_col != col_attr_number and order_col != col_opt_nom:
            return

        if order == Qt.DescendingOrder:
            order_code = 1
        else:
            order_code = 0

        self.order_col = order_col
        self.order = order_code

    @staticmethod
    def a___________________favoris_import______():
        pass

    def favoris_importer(self):

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
                                 registry=[model_setting_file, "path_import"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{a} CSV": [".csv"]},
                                 current_path="",
                                 default_path=asc_export_path,
                                 use_setting_first=True)

        if file_path == "":
            return

        if self.favoris_lecture(file_path):
            msg(titre=self.widget_models.windowTitle(),
                message=self.tr("L'import s'est correctement déroulé!"),
                icone_valide=True)

        self.modification_en_cours = True

    def favoris_lecture(self, file_path: str):
        """
        Permet de lire le fichier option et de le copier dans le self.model_attributs option correspondant
        :return: None
        """

        if not os.path.exists(file_path):
            return False

        content = read_file_to_text(file_path=file_path)

        if "," not in content:
            return False

        attributes_list = model_verification(content.split(", "), False)

        if len(attributes_list) == 0:
            return False

        self.charger_model(numbers_list=attributes_list, reset_model=True)

        self.modification_en_cours = True
        return True

    @staticmethod
    def a___________________favoris_export______():
        pass

    def favoris_exporter(self):

        liste = self.creation_liste_model()

        if len(liste) == 0:
            msg(titre=self.widget_models.windowTitle(),
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
                                 registry=[model_setting_file, "path_export"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{b} CSV": [".csv"]},
                                 current_path=asc_export_path,
                                 default_path="",
                                 file_name=f"{self.nom_onglet}{extension}",
                                 use_setting_first=True,
                                 use_save=True)
        if file_path == "":
            return

        dossier = find_folder_path(file_path)

        fichier = find_filename(file_path)

        backup = f"{dossier}backup\\"

        if dossier == "" or fichier == "" or backup == "":
            return

        make_backup(chemin_dossier=dossier,
                    fichier=fichier,
                    extension=extension,
                    dossier_sauvegarde=backup,
                    nouveau=False)

        liste_element = self.creation_liste_model()

        try:
            with open(file_path, "w") as file:
                file.writelines(", ".join(liste_element))

        except Exception as error:

            msg(titre=self.widget_models.windowTitle(),
                message=self.tr("Une erreur est survenue."),
                details=error,
                icone_critique=True)

            return False
        return True

    def creation_liste_model(self) -> list:

        numbers_list = list()

        for row_index in range(self.tab_attributes_model.rowCount()):
            number = self.tab_attributes_model.index(row_index, col_opt_numero).data()

            if isinstance(number, str):
                numbers_list.append(f"{number}")

        final_list = [number for number in liste_attributs_ordre if number in numbers_list]
        final_list += [number for number in numbers_list if number not in final_list]

        return final_list

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

            if favorites_import_verification(file_path=file_path):
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

            if favorites_import_verification(file_path=file_path):
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

            if favorites_import_verification(file_path=file_path):

                self.favoris_lecture(file_path)
                event.accept()

            else:
                event.ignore()
        else:
            event.ignore()

    def paintEvent(self, event: QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

        super().paintEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class ModelsTabModify(QWidget):
    appliquer_modifications = pyqtSignal(str, str, str, str)

    def __init__(self, parent_actuel, allplan):
        super().__init__(parent=parent_actuel)

        # Définition du widget en popup
        self.setWindowFlags(Qt.Popup)

        # Création de l'interface
        self.ui = Ui_ModelModify()
        self.ui.setupUi(self)

        self.allplan = allplan

        # Définition des variables
        self.liste_onglets = list()
        self.ancien_titre = str()
        self.icone_actuel = ""

        self.choix_icone_actif = False

        # -----------------------------------------------
        #  onglet_texte
        # -----------------------------------------------

        self.ui.onglet_texte.textEdited.connect(self.verification)

        # -----------------------------------------------
        #  Boutons
        # -----------------------------------------------

        self.ui.icone.clicked.connect(self.choisir_icone)
        self.ui.icone_clear.clicked.connect(self.supprimer_icone)

        self.ui.ouvrage.clicked.connect(self.changer_icone)
        self.ui.composant.clicked.connect(self.changer_icone)

        self.ui.bt_enregistrer.clicked.connect(self.enregistrer)
        self.ui.bt_quitter.clicked.connect(self.close)

    def model_modifier_personnaliser(self, nom_onglet: str, icone_onglet: str, type_onglet: str, liste_onglets: list):

        self.ancien_titre = nom_onglet
        self.ui.onglet_texte.setText(nom_onglet)

        self.icone_actuel = icone_onglet
        self.ui.icone.setIcon(get_icon(icone_onglet))

        self.ui.composant.setChecked(type_onglet == component_code)
        self.ui.ouvrage.setChecked(type_onglet == material_code)

        self.liste_onglets = liste_onglets

        self.show()

        self.verification()

        self.ui.onglet_texte.selectAll()
        self.ui.onglet_texte.setFocus()

    def verification(self):
        """ Vérification si le nouveau titre de l'onglet est valide
        :return: Si Valide => True sinon False
        """

        if not self.isVisible():
            return True

        # Définition du nouveau titre de l'onglet
        nouveau_texte = self.ui.onglet_texte.text()

        # Si le nouveau titre est différent de l'ancien
        if nouveau_texte != self.ancien_titre:

            if nouveau_texte.strip() == "":
                tooltips = self.tr("Vous ne pouvez pas laisser le titre vide.")

                self.ui.onglet_texte.setStyleSheet("QLineEdit{"
                                                   "border: 1px solid #8f8f91; "
                                                   "border-right-width: 0px; "
                                                   "border-top-left-radius:5px ; "
                                                   "border-bottom-left-radius:5px; "
                                                   "background-color: orange;}")

                self.ui.bt_enregistrer.setToolTip(tooltips)
                self.ui.bt_enregistrer.setEnabled(False)
                return False

            titre_sans_attribut = self.tr("Sans attribut")

            if (nouveau_texte == titre_sans_attribut or
                    nouveau_texte in material_code_list or nouveau_texte in component_code_list):
                tooltips = self.tr("Ce titre est protégé.")

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

    def changer_icone(self):

        if self.icone_actuel.endswith("material.png") and self.ui.composant.isChecked():

            icone = self.icone_actuel.replace("material.png", "component.png")

            if not icone.startswith(":/Images/"):
                if not os.path.exists(icone):
                    return

            self.icone_actuel = icone
            self.ui.icone.setIcon(get_icon(icone))
            return

        if self.icone_actuel.endswith("component.png") and self.ui.ouvrage.isChecked():

            icone = self.icone_actuel.replace("component.png", "material.png")

            if not icone.startswith(":/Images/"):
                if not os.path.exists(icone):
                    return

            self.icone_actuel = icone
            self.ui.icone.setIcon(get_icon(icone))
            return

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

        chemin_fichier = browser_file(parent=self,
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

        if chemin_fichier == "":
            return

        # Définition de la nouvelle icone
        self.icone_actuel = chemin_fichier

        # Affichage de la nouvelle icone.
        self.ui.icone.setIcon(get_icon(chemin_fichier))

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

            if self.ui.ouvrage.isChecked():

                type_onglet = "material"
            else:
                type_onglet = "component"

            nouveau_texte = self.ui.onglet_texte.text()

            # Envoi de informations
            self.appliquer_modifications.emit(self.ancien_titre, nouveau_texte, self.icone_actuel, type_onglet)

            # Fermeture de la fenêtre
            self.close()

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:

            self.enregistrer()

        elif event.key() == Qt.Key_Escape:

            self.close()

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):

        if self.choix_icone_actif:
            event.ignore()
            return

        else:
            self.ancien_titre = str()
            self.icone_actuel = str()
            self.ui.onglet_texte.setStyleSheet("")
            self.ui.onglet_texte.setToolTip(self.tr("Titre valide"))

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class ModelsTabDel(QWidget):
    validation_supprimer = pyqtSignal(int)

    def __init__(self, parent_actuel):
        super().__init__(parent=parent_actuel)

        # Définition du widget en popup
        self.setWindowFlags(Qt.Popup)

        # Création de l'interface
        self.ui = Ui_ModelTabDel()
        self.ui.setupUi(self)

        self.tab_index = -1

        self.ui.bt_supprimer.clicked.connect(self.bt_supprimer_clicked)
        self.ui.bt_annuler.clicked.connect(self.close)

    def del_ask_show(self, tab_index: int):
        self.tab_index = tab_index
        self.show()
        self.ui.bt_supprimer.setFocus()

    def bt_supprimer_clicked(self):
        self.close()
        self.validation_supprimer.emit(self.tab_index)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.bt_supprimer_clicked()

        elif event.key() == Qt.Key_Escape:
            self.close()


class ModelsTabBar(QTabBar):
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
        )

    def del_tab(self, button: QPushButton):

        if not isinstance(button, QPushButton):
            return

        nb_tab = self.count()

        for index_tab in range(2, nb_tab - 1):

            current_button = self.tabButton(index_tab, QTabBar.RightSide)

            if not isinstance(current_button, QPushButton):
                continue

            if current_button == button:
                self.del_signal.emit(index_tab)
                return

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

        close_button = QPushButton(self)
        close_button.setFlat(True)
        close_button.setMinimumHeight(24)

        if current_index not in [0, 1]:
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

        if nb_tab <= 3:
            return

        tab_first_movable_rect = self.tabRect(1)

        if not isinstance(tab_first_movable_rect, QRect):
            return

        tab_last_movable_rect = self.tabRect(nb_tab - 1)

        if not isinstance(tab_last_movable_rect, QRect):
            return

        tab_current_index = self.tabAt(event.pos())

        if tab_current_index in [0, 1, nb_tab - 1]:
            return

        tab_current_rect = self.tabRect(tab_current_index)

        if not isinstance(tab_current_rect, QRect):
            return

        self.tab_first_movable_pos = tab_first_movable_rect.x() + tab_first_movable_rect.width()
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

        self.setTabEnabled(0, False)
        self.setTabEnabled(1, False)
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

        self.setTabEnabled(0, True)
        self.setTabEnabled(1, True)
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
