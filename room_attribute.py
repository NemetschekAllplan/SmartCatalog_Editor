#!/usr/bin/python3
# -*- coding: utf-8 -*
from history_manage import AttributeModifyData
from tools import settings_read, settings_save, move_window_tool, get_room_defaut_dict
from ui_attribute_room import Ui_AttributeRoom
from room import *


class AttributeRoom(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict, str)

    def __init__(self, asc):
        super().__init__()

        # Chargement du widget + setup
        self.ui = Ui_AttributeRoom()
        self.ui.setupUi(self)

        self.asc = asc

        self.allplan: AllplanDatas = asc.allplan

        self.langue = self.asc.langue.lower()

        if self.asc.langue not in dict_langues:
            self.fichier_config = f"{room_config_file}_en"
        else:
            self.fichier_config = f"{room_config_file}_{self.asc.langue.lower()}"

        self.type_element = "type_piece"

        # ---------------------------------------
        # Favoris
        # ---------------------------------------
        a = self.tr("Nom favoris")

        self.liste_titres = [f'{a} : ',
                             f"{self.ui.titre_231.text()} (231) : ",
                             f"{self.ui.titre_235.text()} (235) : ",
                             f"{self.ui.titre_232.text()} (232) : ",
                             f"{self.ui.titre_266.text()} (266) : ",
                             f"{self.ui.titre_233.text()} (233) : ",
                             f"{self.ui.titre_264.text()} (264) : "]

        self.model_room_favoris = QStandardItemModel()

        self.room_favoris_lecture()

        self.widget_room = WidgetRoom(self.allplan, self.liste_titres)

        self.widget_room.save_favoris.connect(self.favoris_enregistrement)
        self.widget_room.modif_termine.connect(self.update_datas)

        self.filtre_favoris = QSortFilterProxyModel()
        self.filtre_favoris.setSourceModel(self.model_room_favoris)
        self.filtre_favoris.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_fav.setModel(self.model_room_favoris)

        qcompleter_favoris = QCompleter()
        qcompleter_favoris.setModel(self.filtre_favoris)
        qcompleter_favoris.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_favoris.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_fav.setCompleter(qcompleter_favoris)

        self.ui.valeur_fav.currentIndexChanged.connect(self.favoris_change)
        self.ui.formatting_bt.clicked.connect(self.favoris_ouvrir_aide)
        self.ui.formatting_2_bt.clicked.connect(self.favoris_ouvrir_aide)

        get_look_combobox(self.ui.valeur_fav)

        self.ui.valeur_fav.installEventFilter(self)

        # ---------------------------------------
        # 231 - Pourtour de salle
        # ---------------------------------------

        self.ui_231 = WidgetAttribute231(self, self.allplan.langue)
        self.ui_231.modif_termine.connect(self.ui.valeur_231.setCurrentText)
        self.ui_231.modif_termine.connect(self.change_231)
        self.ui_231.modif_termine.connect(self.ui.valeur_231.setFocus)

        self.qs_231_ind = QStandardItem()
        self.qs_231_val = QStandardItem()

        self.filtre_231 = QSortFilterProxyModel()
        self.filtre_231.setSourceModel(self.allplan.model_231)
        self.filtre_231.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_231.setFilterKeyColumn(1)

        self.ui.valeur_231.setModel(self.allplan.model_231)
        self.ui.valeur_231.setModelColumn(1)

        qcompleter_231 = QCompleter()
        qcompleter_231.setModel(self.filtre_231)
        qcompleter_231.setCompletionColumn(1)
        qcompleter_231.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_231.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_231.setCompleter(qcompleter_231)

        self.ui.valeur_231.currentIndexChanged.connect(self.change_231)
        self.ui.valeur_231.lineEdit().textEdited.connect(self.filtre_231.setFilterFixedString)

        self.ui.valeur_231.installEventFilter(self)

        get_look_combobox(self.ui.valeur_231)

        self.ui.bt_231.clicked.connect(self.afficher_ui_231)

        # ---------------------------------------
        # 235 - Type utlisation
        # ---------------------------------------

        self.ui_235 = WidgetAttribute235(self, self.allplan.langue)
        self.ui_235.modif_termine.connect(self.ui.valeur_235.setCurrentText)
        self.ui_235.modif_termine.connect(self.change_235)
        self.ui_235.modif_termine.connect(self.ui.valeur_235.setFocus)

        self.qs_235_ind = QStandardItem()
        self.qs_235_val = QStandardItem()

        self.filtre_235 = QSortFilterProxyModel()
        self.filtre_235.setSourceModel(self.allplan.model_235)
        self.filtre_235.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_235.setFilterKeyColumn(1)

        self.ui.valeur_235.setModel(self.allplan.model_235)
        self.ui.valeur_235.setModelColumn(1)

        qcompleter_235 = QCompleter()
        qcompleter_235.setModel(self.filtre_235)
        qcompleter_235.setCompletionColumn(1)
        qcompleter_235.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_235.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_235.setCompleter(qcompleter_235)

        self.ui.valeur_235.currentIndexChanged.connect(self.change_235)
        self.ui.valeur_235.lineEdit().textEdited.connect(self.filtre_235.setFilterFixedString)

        self.ui.valeur_235.installEventFilter(self)

        get_look_combobox(self.ui.valeur_235)

        self.ui.bt_235.clicked.connect(self.afficher_ui_235)

        # ---------------------------------------
        # 232 - Type de surface
        # ---------------------------------------

        self.ui_232 = WidgetAttribute232(parent_current=self, allplan=self.allplan)
        self.ui_232.modif_termine.connect(self.ui.valeur_232.setCurrentText)
        self.ui_232.modif_termine.connect(self.change_232)
        self.ui_232.modif_termine.connect(self.ui.valeur_232.setFocus)

        self.qs_232_ind = QStandardItem()
        self.qs_232_val = QStandardItem()

        self.filtre_232 = QSortFilterProxyModel()
        self.filtre_232.setSourceModel(self.allplan.model_232)
        self.filtre_232.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_232.setFilterKeyColumn(1)

        self.ui.valeur_232.setModel(self.allplan.model_232)
        self.ui.valeur_232.setModelColumn(1)

        qcompleter_232 = QCompleter()
        qcompleter_232.setModel(self.filtre_232)
        qcompleter_232.setCompletionColumn(1)
        qcompleter_232.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_232.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_232.setCompleter(qcompleter_232)

        self.ui.valeur_232.currentIndexChanged.connect(self.change_232)
        self.ui.valeur_232.lineEdit().textEdited.connect(self.filtre_232.setFilterFixedString)

        self.ui.valeur_232.installEventFilter(self)

        get_look_combobox(self.ui.valeur_232)

        self.ui.bt_232.clicked.connect(self.afficher_ui_232)

        # ---------------------------------------
        # 266 - Facteur Din
        # ---------------------------------------

        self.qs_266 = QStandardItem()

        self.ui.valeur_266.setValidator(ValidatorDouble())

        self.ui.valeur_266.editingFinished.connect(self.change_266)

        # ---------------------------------------
        # 233 - Type surface hab
        # ---------------------------------------

        self.ui_233 = WidgetAttribute233(self, self.allplan.langue)
        self.ui_233.modif_termine.connect(self.ui.valeur_233.setCurrentText)
        self.ui_233.modif_termine.connect(self.change_233)
        self.ui_233.modif_termine.connect(self.ui.valeur_233.setFocus)

        self.qs_233_ind = QStandardItem()
        self.qs_233_val = QStandardItem()

        self.filtre_233 = QSortFilterProxyModel()
        self.filtre_233.setSourceModel(self.allplan.model_233)
        self.filtre_233.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_233.setFilterKeyColumn(1)

        self.ui.valeur_233.setModel(self.allplan.model_233)
        self.ui.valeur_233.setModelColumn(1)

        qcompleter_233 = QCompleter()
        qcompleter_233.setModel(self.filtre_233)
        qcompleter_233.setCompletionColumn(1)
        qcompleter_233.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_233.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_233.setCompleter(qcompleter_233)

        self.ui.valeur_233.currentIndexChanged.connect(self.change_233)
        self.ui.valeur_233.lineEdit().textEdited.connect(self.filtre_233.setFilterFixedString)

        self.ui.valeur_233.installEventFilter(self)

        get_look_combobox(self.ui.valeur_233)

        self.ui.bt_233.clicked.connect(self.afficher_ui_233)

        # ---------------------------------------
        # 264 - Facteur de surface habitable
        # ---------------------------------------

        self.qs_264 = QStandardItem()

        self.ui.valeur_264.setValidator(ValidatorDouble())

        self.ui.valeur_264.editingFinished.connect(self.change_264)

    @staticmethod
    def a___________________chargement______():
        pass

    def chargement(self):

        valeur_231 = self.qs_231_val.text()
        valeur_231_ind = self.qs_231_ind.text()

        valeur_235 = self.qs_235_val.text()
        valeur_235_ind = self.qs_235_ind.text()

        valeur_232 = self.qs_232_val.text()
        valeur_232_ind = self.qs_232_ind.text()

        valeur_266 = self.qs_266.text()

        valeur_233 = self.qs_233_val.text()
        valeur_233_ind = self.qs_233_ind.text()

        valeur_264 = self.qs_264.text()

        nom_favoris = self.rechercher_favoris("", valeur_231, valeur_235, valeur_232, valeur_266, valeur_233,
                                              valeur_264)

        self.set_current_texte(self.ui.valeur_fav, nom_favoris, True)

        self.set_current_texte(self.ui.valeur_231, valeur_231, True)
        self.ui.numero_231.setText(valeur_231_ind)

        self.set_current_texte(self.ui.valeur_235, valeur_235, True)
        self.ui.numero_235.setText(valeur_235_ind)

        self.set_current_texte(self.ui.valeur_232, valeur_232, True)
        self.ui.numero_232.setText(valeur_232_ind)

        self.ui.valeur_266.setText(valeur_266)

        self.set_current_texte(self.ui.valeur_233, valeur_233, True)
        self.ui.numero_233.setText(valeur_233_ind)

        self.ui.valeur_264.setText(valeur_264)

        qstandarditem_fav = QStandardItem("")

        font = QStandardItem().font()
        font.setFamily("Segoe UI")
        font.setPointSize(taille_police)
        qstandarditem_fav.setFont(font)

        qstandarditem_fav.setToolTip(self.creation_tooltips("", valeur_231, valeur_235, valeur_232,
                                                            valeur_266, valeur_233, valeur_264))

        self.model_room_favoris.insertRow(0, [qstandarditem_fav, QStandardItem(valeur_231), QStandardItem(valeur_235),
                                              QStandardItem(valeur_232), QStandardItem(valeur_266),
                                              QStandardItem(valeur_233),
                                              QStandardItem(valeur_264)])

    @staticmethod
    def set_current_texte(widget_combo: QComboBox, valeur_recherche: str, blocksignal=False, object_numero=None) -> int:
        index_item = widget_combo.findText(valeur_recherche, Qt.MatchExactly)

        widget_combo.blockSignals(blocksignal)

        widget_combo.setCurrentIndex(index_item)

        if isinstance(object_numero, QLabel):
            object_numero.setText(f"{index_item}")

        widget_combo.blockSignals(False)
        return index_item

    @staticmethod
    def a___________________favoris_fichier______():
        """ Partie réservée aux traitements des fichiers xml à charger"""
        pass

    def room_favoris_lecture(self):

        font = QStandardItem().font()
        font.setFamily("Segoe UI")
        font.setPointSize(taille_police)

        if not os.path.exists(f"{asc_settings_path}{self.fichier_config}.ini"):
            datas = get_room_defaut_dict(langue=self.asc.langue)
        else:
            datas = settings_read(self.fichier_config)

            if len(datas) == 0:
                datas = get_room_defaut_dict(langue=self.asc.langue)

        a = self.tr("Nom favoris")

        for title, attribute_datas in datas.items():

            if not isinstance(title, str):
                continue

            title = title.strip()

            if title == "":
                continue

            if not isinstance(attribute_datas, dict):
                continue

            if len(attribute_datas) != 6:
                continue

            qstandarditem_fav = QStandardItem(title)
            qstandarditem_fav.setFont(font)

            liste_tooltips = [f'{a} : <b>{title}</b><br>']
            liste_ajouter = [qstandarditem_fav]

            for number in room_attributes_list:
                value = attribute_datas.get(number, "")

                value = value.upper().strip()

                qs_value = QStandardItem(value)

                liste_ajouter.append(qs_value)

                liste_tooltips.append(f"{number} : <b>{value}</b>")

            qstandarditem_fav.setToolTip("<br>".join(liste_tooltips))

            self.model_room_favoris.appendRow(liste_ajouter)

    @staticmethod
    def a___________________favoris_chargement______():
        pass

    def chargement_favoris(self, value_new_231: str, value_new_235: str, value_new_232: str, value_new_266: str,
                           value_new_233: str, value_new_264: str):

        print("widget_type_piece -- favoris chargement")

        if not self.ui.valeur_fav.isVisible():
            return

        # -------------

        qs_parent = self.qs_231_val.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("room_attribute -- chargement_favoris -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("room_attribute -- chargement_favoris -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("room_attribute -- chargement_favoris -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = list()
        value_dict = dict()

        # ------------- 231

        value_current_231 = self.qs_231_val.text()
        value_index_current_231 = self.qs_231_ind.text()

        self.set_current_texte(self.ui.valeur_231, value_new_231, True, self.ui.numero_231)

        self.mise_a_jour_combo(qs_val=self.qs_231_val,
                               qs_ind=self.qs_231_ind,
                               number_current="231",
                               widget_combo=self.ui.valeur_231,
                               widget_index=self.ui.numero_231,
                               maj=False)

        if value_current_231 != value_new_231:

            attribute_data.append(AttributeModifyData(number_current="231",
                                                      value_new=value_current_231,
                                                      value_index_new=value_index_current_231))

            value_dict["231"] = [value_current_231, value_new_231]

        # ------------- 235

        value_current_235 = self.qs_235_val.text()
        value_index_current_235 = self.qs_235_ind.text()

        self.set_current_texte(self.ui.valeur_235, value_new_235, True, self.ui.numero_235)

        self.mise_a_jour_combo(qs_val=self.qs_235_val,
                               qs_ind=self.qs_235_ind,
                               number_current="235",
                               widget_combo=self.ui.valeur_235,
                               widget_index=self.ui.numero_235,
                               maj=False)

        if value_current_235 != value_new_235:

            attribute_data.append(AttributeModifyData(number_current="235",
                                                      value_new=value_current_235,
                                                      value_index_new=value_index_current_235))

            value_dict["235"] = [value_current_235, value_new_235]

        # ------------- 232

        value_current_232 = self.qs_232_val.text()
        value_index_current_232 = self.qs_232_ind.text()

        self.set_current_texte(self.ui.valeur_232, value_new_232, True, self.ui.valeur_232)

        self.mise_a_jour_combo(qs_val=self.qs_232_val,
                               qs_ind=self.qs_232_ind,
                               number_current="232",
                               widget_combo=self.ui.valeur_232,
                               widget_index=self.ui.numero_232,
                               maj=False)

        if value_current_232 != value_new_232:

            attribute_data.append(AttributeModifyData(number_current="232",
                                                      value_new=value_current_232,
                                                      value_index_new=value_index_current_232))

            value_dict["232"] = [value_current_232, value_new_232]

        # ------------- 266

        value_current_266 = self.qs_266.text()

        self.ui.valeur_266.setText(value_new_266)

        self.mise_a_jour_lineedit(qs_val=self.qs_266,
                                  number_current="266",
                                  widget_lineedit=self.ui.valeur_266,
                                  maj=False)

        self.set_current_texte(self.ui.valeur_233, value_new_233, True, self.ui.valeur_233)

        if value_current_266 != value_new_266:

            attribute_data.append(AttributeModifyData(number_current="266",
                                                      value_new=value_current_266))

            value_dict["266"] = [value_current_266, value_new_266]

        # ------------- 233

        value_current_233 = self.qs_233_val.text()
        value_index_current_233 = self.qs_233_ind.text()

        self.mise_a_jour_combo(qs_val=self.qs_233_val,
                               qs_ind=self.qs_233_ind,
                               number_current="233",
                               widget_combo=self.ui.valeur_233,
                               widget_index=self.ui.numero_233,
                               maj=False)

        if value_current_233 != value_new_233:

            attribute_data.append(AttributeModifyData(number_current="233",
                                                      value_new=value_current_233,
                                                      value_index_new=value_index_current_233))

            value_dict["233"] = [value_current_233, value_new_233]

        # ------------- 264

        value_current_264 = self.qs_264.text()

        self.ui.valeur_264.setText(value_new_264)

        self.mise_a_jour_lineedit(qs_val=self.qs_264,
                                  number_current="264",
                                  widget_lineedit=self.ui.valeur_264,
                                  maj=False)

        if value_current_264 != value_new_264:

            attribute_data.append(AttributeModifyData(number_current="264",
                                                      value_new=value_current_264))

            value_dict["264"] = [value_current_264, value_new_264]

        # ------------- signal

        if len(value_dict) != 0:

            self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict,
                                               self.tr("Groupe Pièce"))

    def recherche_favoris_auto(self):

        print("widget_type_piece -- recherche_favoris_auto")
        valeur_fav = self.ui.valeur_fav.currentText()

        valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264 = self.recherche_valeurs()

        nom_favoris = self.rechercher_favoris(valeur_fav, valeur_231, valeur_235, valeur_232, valeur_266, valeur_233,
                                              valeur_264)

        if nom_favoris == valeur_fav:
            return

        self.set_current_texte(self.ui.valeur_fav, nom_favoris)

        return

    def rechercher_favoris(self, nom_favoris: str, valeur_231: str, valeur_235: str, valeur_232: str, valeur_266: str,
                           valeur_233: str, valeur_264: str):

        if nom_favoris != "":
            qs_row = self.ui.valeur_fav.findText(nom_favoris)

            data_231 = self.model_room_favoris.item(qs_row, col_231).text()
            data_235 = self.model_room_favoris.item(qs_row, col_235).text()
            data_232 = self.model_room_favoris.item(qs_row, col_232).text()
            data_266 = self.model_room_favoris.item(qs_row, col_266).text()
            data_233 = self.model_room_favoris.item(qs_row, col_233).text()
            data_264 = self.model_room_favoris.item(qs_row, col_264).text()

            if data_231 == valeur_231 and data_235 == valeur_235 and data_232 == valeur_232 and data_266 == valeur_266 \
                    and data_233 == valeur_233 and data_264 == valeur_264:
                return nom_favoris

        print("widget_type_piece -- recherche_favoris")

        for qs_row in range(1, self.model_room_favoris.rowCount()):

            nom_favoris = self.model_room_favoris.item(qs_row, col_favoris).text()
            data_231 = self.model_room_favoris.item(qs_row, col_231).text()

            if data_231 != valeur_231:
                continue

            data_235 = self.model_room_favoris.item(qs_row, col_235).text()

            if data_235 != valeur_235:
                continue

            data_232 = self.model_room_favoris.item(qs_row, col_232).text()

            if data_232 != valeur_232:
                continue

            data_266 = self.model_room_favoris.item(qs_row, col_266).text()

            if data_266 != valeur_266:
                continue

            data_233 = self.model_room_favoris.item(qs_row, col_233).text()

            if data_233 != valeur_233:
                continue

            data_264 = self.model_room_favoris.item(qs_row, col_264).text()

            if data_264 != valeur_264:
                continue

            return nom_favoris

        index_item = 0

        tooltips = self.creation_tooltips("", valeur_231, valeur_235, valeur_232, valeur_266, valeur_233,
                                          valeur_264)
        # ----------

        qs_fav = self.model_room_favoris.item(index_item, col_favoris)

        if not isinstance(qs_fav, QStandardItem):
            return ""

        qs_fav.setToolTip(tooltips)

        # ------------

        qs_231 = self.model_room_favoris.item(index_item, col_231)

        if not isinstance(qs_231, QStandardItem):
            return ""

        qs_231.setText(valeur_231)

        # ------------

        qs_232 = self.model_room_favoris.item(index_item, col_232)

        if not isinstance(qs_232, QStandardItem):
            return ""

        qs_232.setText(valeur_232)

        # ------------

        qs_233 = self.model_room_favoris.item(index_item, col_233)

        if not isinstance(qs_233, QStandardItem):
            return ""

        qs_233.setText(valeur_233)

        # ------------

        qs_235 = self.model_room_favoris.item(index_item, col_235)

        if not isinstance(qs_235, QStandardItem):
            return ""

        qs_235.setText(valeur_235)

        # ------------

        qs_264 = self.model_room_favoris.item(index_item, col_266)

        if not isinstance(qs_264, QStandardItem):
            return ""

        qs_264.setText(valeur_264)

        # ------------

        qs_266 = self.model_room_favoris.item(index_item, col_266)

        if not isinstance(qs_266, QStandardItem):
            return ""

        qs_266.setText(valeur_266)

        # ------------

        return ""

    def recherche_valeurs(self) -> tuple:

        valeur_231 = self.ui.valeur_231.currentText()
        valeur_235 = self.ui.valeur_235.currentText()
        valeur_232 = self.ui.valeur_232.currentText()
        valeur_266 = self.ui.valeur_266.text()
        valeur_233 = self.ui.valeur_233.currentText()
        valeur_264 = self.ui.valeur_264.text()

        return valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264

    @staticmethod
    def a___________________favoris_changement______():
        pass

    def creation_tooltips(self, nom_favoris: str, valeur_231: str, valeur_235: str, valeur_232: str, valeur_266: str,
                          valeur_233: str, valeur_264: str):
        a = self.tr("Nom favoris")
        return (f'{a} : <b>{nom_favoris}</b><br><br>'
                f"231 : <b>{valeur_231}</b><br>"
                f"235 : <b>{valeur_235}</b><br>"
                f"232 : <b>{valeur_232}</b><br>"
                f"266 : <b>{valeur_266}</b><br>"
                f"233 : <b>{valeur_233}</b><br>"
                f"264 : <b>{valeur_264}</b>")

    def favoris_change(self):

        if self.ui.valeur_fav.view().isVisible():
            return

        current_row: int = self.ui.valeur_fav.currentIndex()
        current_text: str = self.ui.valeur_fav.currentText()

        if current_row == -1:
            return

        print(f"widget_type_piece -- favoris_change -- {current_text} --> {current_row}")

        valeur_231 = self.model_room_favoris.index(current_row, col_231).data()
        valeur_235 = self.model_room_favoris.index(current_row, col_235).data()
        valeur_232 = self.model_room_favoris.index(current_row, col_232).data()
        valeur_266 = self.model_room_favoris.index(current_row, col_266).data()
        valeur_233 = self.model_room_favoris.index(current_row, col_233).data()
        valeur_264 = self.model_room_favoris.index(current_row, col_264).data()

        self.chargement_favoris(valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264)

    def favoris_ouvrir_aide(self):

        self.asc.formula_widget_close()

        self.copie_model1_to_model2(self.model_room_favoris, self.widget_room.model_room_favoris)

        self.widget_room.chargement(self.ui.valeur_fav.currentText(),
                                    self.ui.valeur_231.currentText(),
                                    self.ui.valeur_235.currentText(),
                                    self.ui.valeur_232.currentText(),
                                    self.ui.valeur_266.text(),
                                    self.ui.valeur_233.currentText(),
                                    self.ui.valeur_264.text())

        move_window_tool(widget_parent=self.asc, widget_current=self.widget_room, always_center=True)

        self.widget_room.show()

    @staticmethod
    def a___________________favoris_enregistrement______():
        pass

    def favoris_enregistrement(self):
        self.copie_model1_to_model2(self.widget_room.model_room_favoris, self.model_room_favoris)
        self.copie_model_to_fichier()

    @staticmethod
    def copie_model1_to_model2(model1: QStandardItemModel, model2: QStandardItemModel) -> QStandardItemModel:

        print(f"widget_type_piece -- copie_model1_to_model2")

        font = QStandardItem().font()
        font.setFamily("Segoe UI")
        font.setPointSize(taille_police)

        model2.clear()

        for index_item in range(model1.rowCount()):
            val_fav = model1.item(index_item, col_favoris).text()
            tooltips = model1.item(index_item, col_favoris).toolTip()

            val_231 = model1.item(index_item, col_231).clone()
            val_235 = model1.item(index_item, col_235).clone()
            val_232 = model1.item(index_item, col_232).clone()
            val_266 = model1.item(index_item, col_266).clone()
            val_233 = model1.item(index_item, col_233).clone()
            val_264 = model1.item(index_item, col_264).clone()

            qstandarditem_favoris = QStandardItem(val_fav)
            qstandarditem_favoris.setFont(font)
            qstandarditem_favoris.setToolTip(tooltips)

            model2.appendRow([qstandarditem_favoris, val_231, val_235, val_232, val_266, val_233, val_264])

        return model2

    def copie_model_to_fichier(self):

        print(f"widget_type_piece -- copie_model_to_fichier")

        datas = dict()

        for index_qstandarditem in range(1, self.model_room_favoris.rowCount()):
            val_fav = self.model_room_favoris.item(index_qstandarditem, col_favoris).text()

            if val_fav == "":
                continue

            datas[val_fav] = {"231": self.model_room_favoris.item(index_qstandarditem, col_231).text(),
                              "235": self.model_room_favoris.item(index_qstandarditem, col_235).text(),
                              "232": self.model_room_favoris.item(index_qstandarditem, col_232).text(),
                              "266": self.model_room_favoris.item(index_qstandarditem, col_266).text(),
                              "233": self.model_room_favoris.item(index_qstandarditem, col_233).text(),
                              "264": self.model_room_favoris.item(index_qstandarditem, col_264).text()}

        settings_save(self.fichier_config, datas)

    @staticmethod
    def a___________________231_pourtour_de_salle______():
        pass

    def change_231(self):
        self.verification_datas(qs_val=self.qs_231_val,
                                qs_ind=self.qs_231_ind,
                                numero="231",
                                widget_combo=self.ui.valeur_231,
                                widget_index=self.ui.numero_231)

    def afficher_ui_231(self):
        self.charger_gestion_surfaces(self.ui_231, self.ui.bt_231, self.ui.valeur_231.currentText())

    @staticmethod
    def a___________________235_type_utilisation______():
        pass

    def change_235(self):
        self.verification_datas(qs_val=self.qs_235_val,
                                qs_ind=self.qs_235_ind,
                                numero="235",
                                widget_combo=self.ui.valeur_235,
                                widget_index=self.ui.numero_235)

    def afficher_ui_235(self):
        self.charger_gestion_surfaces(self.ui_235, self.ui.bt_235, self.ui.valeur_235.currentText())

    @staticmethod
    def a___________________232_type_surface______():
        pass

    def change_232(self):
        self.verification_datas(qs_val=self.qs_232_val,
                                qs_ind=self.qs_232_ind,
                                numero="232",
                                widget_combo=self.ui.valeur_232,
                                widget_index=self.ui.numero_232)

    def afficher_ui_232(self):
        self.charger_gestion_surfaces(self.ui_232, self.ui.bt_232, self.ui.valeur_232.currentText())

    @staticmethod
    def a___________________266_facteur_din______():
        pass

    def change_266(self):

        valeur = texte_actuel = self.ui.valeur_266.text()

        if "," in valeur:
            valeur = valeur.replace(",", ".")

        try:
            valeur_decimal = float(valeur)
            valeur = f"{valeur_decimal:.3f}"
        except ValueError:

            pass

        valeur = valeur.replace(".", ",")

        if texte_actuel == valeur:
            return

        print("widget_type_piece -- change_266")

        self.ui.valeur_266.setText(valeur)

        self.mise_a_jour_lineedit(qs_val=self.qs_266,
                                  number_current="266",
                                  widget_lineedit=self.ui.valeur_266)

        self.recherche_favoris_auto()

    @staticmethod
    def a___________________233_type_surface_hab______():
        pass

    def change_233(self):
        self.verification_datas(qs_val=self.qs_233_val,
                                qs_ind=self.qs_233_ind,
                                numero="233",
                                widget_combo=self.ui.valeur_233,
                                widget_index=self.ui.numero_233)

    def afficher_ui_233(self):
        self.charger_gestion_surfaces(self.ui_233, self.ui.bt_233, self.ui.valeur_233.currentText())

    @staticmethod
    def a___________________264_facteur_hab______():
        pass

    def change_264(self):

        valeur = texte_actuel = self.ui.valeur_264.text()

        if "," in valeur:
            valeur = valeur.replace(",", ".")

        try:
            valeur_decimal = float(valeur)
            valeur = f"{valeur_decimal:.3f}"
        except ValueError:

            pass

        valeur = valeur.replace(".", ",")

        if texte_actuel == valeur:
            return

        print("widget_type_piece -- change_264")

        self.ui.valeur_264.setText(valeur)

        self.mise_a_jour_lineedit(qs_val=self.qs_264,
                                  number_current="264",
                                  widget_lineedit=self.ui.valeur_264)

        self.recherche_favoris_auto()

    @staticmethod
    def a___________________datas______():
        pass

    def update_datas(self, valeur_fav: str, valeur_231: str, valeur_235: str, valeur_232: str, valeur_266: str,
                     valeur_233: str, valeur_264: str):

        self.set_current_texte(self.ui.valeur_fav, valeur_fav)
        self.chargement_favoris(valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264)

    def verification_datas(self, qs_val: QStandardItem, qs_ind: QStandardItem,
                           numero: str, widget_combo: QComboBox, widget_index: QLabel):

        texte = widget_combo.currentText()
        index_row = widget_combo.currentIndex()

        if widget_combo.view().isVisible():
            return

        if texte == qs_val.text() and qs_ind.text() == f"{index_row}":
            return

        print(f"widget_type_piece -- verification_datas -- {numero}")

        if index_row == -1 or texte == "":
            self.set_current_texte(widget_combo, "", True)
            widget_index.setText("-1")

            self.mise_a_jour_combo(qs_val=qs_val,
                                   qs_ind=qs_ind,
                                   number_current=numero,
                                   widget_combo=widget_combo,
                                   widget_index=widget_index)

            self.recherche_favoris_auto()
            return

        recherche = widget_combo.findText(texte, Qt.MatchExactly)

        if recherche == -1:
            self.set_current_texte(widget_combo, qs_val.text(), True)
            widget_index.setText(qs_ind.text())

            self.recherche_favoris_auto()
            return

        if recherche != index_row:
            numero_element = widget_combo.model().index(recherche, 0).data(Qt.DisplayRole)

        else:
            numero_element = widget_combo.model().index(index_row, 0).data(Qt.DisplayRole)

        widget_index.setText(numero_element)

        self.mise_a_jour_combo(qs_val=qs_val,
                               qs_ind=qs_ind,
                               number_current=numero,
                               widget_combo=widget_combo,
                               widget_index=widget_index)

        self.recherche_favoris_auto()

    def mise_a_jour_combo(self, qs_val: QStandardItem, qs_ind: QStandardItem,
                          number_current: str, widget_combo: QComboBox, widget_index: QLabel, maj=True):

        value_current = qs_val.text()
        value_new = widget_combo.currentText()

        value_index_current = qs_ind.text()
        value_index_new = widget_index.text()

        if value_current == value_new and value_index_current == value_index_new:
            return

        if not widget_combo.isVisible():
            return

        qs_val.setText(value_new)
        qs_ind.setText(value_index_new)

        if not maj:
            return

        qs_parent = self.qs_231_val.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("room_attribute -- mise_a_jour_combo -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("room_attribute -- mise_a_jour_combo -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("room_attribute -- mise_a_jour_combo -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = [AttributeModifyData(number_current=number_current,
                                              value_new=value_current,
                                              value_index_new=value_index_current)]

        value_dict = {number_current: [value_current, value_new]}

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, "")

    def mise_a_jour_lineedit(self, qs_val: QStandardItem, number_current: str, widget_lineedit: QLineEdit, maj=True):

        value_current = qs_val.text()
        value_new = widget_lineedit.text()

        if value_current == value_new:
            return

        if not widget_lineedit.isVisible():
            return

        qs_val.setText(value_new)

        if not maj:
            return

        qs_parent = self.qs_231_val.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("room_attribute -- mise_a_jour_lineedit -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("room_attribute -- mise_a_jour_lineedit -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("room_attribute -- mise_a_jour_lineedit -- not isinstance(parent_name, str)")
            return

        # -------------

        attribute_data = [AttributeModifyData(number_current=number_current, value_new=value_current)]

        value_dict = {number_current: [value_current, value_new]}

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict, "")

    @staticmethod
    def a___________________ui_annexe______():
        pass

    def charger_gestion_surfaces(self,
                                 widget_popup: Union[WidgetAttribute231,
                                 WidgetAttribute232,
                                 WidgetAttribute233,
                                 WidgetAttribute235],
                                 bouton: QPushButton, valeur: str):

        self.asc.formula_widget_close()

        widget_popup.valeur_actuelle = valeur

        move_widget_ss_bouton(bouton, widget_popup)

        widget_popup.personnaliser()

        widget_popup.show()

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj == self.ui.valeur_fav:

            if event.type() == QEvent.FocusOut:
                self.favoris_change()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_fav.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

            return super().eventFilter(obj, event)

        if obj == self.ui.valeur_231:

            if event.type() == QEvent.FocusOut:
                self.change_231()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_231.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

            return super().eventFilter(obj, event)

        if obj == self.ui.valeur_235:

            if event.type() == QEvent.FocusOut:
                self.change_235()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_235.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

            return super().eventFilter(obj, event)

        if obj == self.ui.valeur_232:

            if event.type() == QEvent.FocusOut:
                self.change_232()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_232.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

            return super().eventFilter(obj, event)

        if obj == self.ui.valeur_233:

            if event.type() == QEvent.FocusOut:
                self.change_233()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_233.hasFocus():
                    event.ignore()
                    return True
                else:
                    event.accept()
                    return super().eventFilter(obj, event)

            if event.type() != QEvent.KeyPress:
                return super().eventFilter(obj, event)

            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
                event.ignore()
                return True

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
