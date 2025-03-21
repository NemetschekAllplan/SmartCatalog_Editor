#!/usr/bin/python3
# -*- coding: utf-8 -*

"""Script pour le widget style de surface"""

from PyQt5.Qt import *

from allplan_manage import AllplanDatas
from main_datas import formula_setting_file, error_icon, valid_icon, get_icon
from tools import afficher_message as msg, qm_check
from tools import changer_selection_apparence, settings_save_value, settings_get, application_title
from tools import selectionner_parentheses, taille_police_menu, recherche_position_parentheses, recherche_couleur
from ui_autocompletion import Ui_Autocompletion

min_size = 10
max_size = 25


class ParenthesesHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, taille_police: int):
        super().__init__(parent)

        parent: QTextDocument
        self.format_txt = QTextCharFormat()
        self.font = self.format_txt.font()
        self.font.setPointSize(taille_police)
        self.font.setBold(True)
        self.format_txt.setFont(self.font)

    def highlightBlock(self, formule: str):
        parentheses_indices = recherche_position_parentheses(formule)
        index_parenthese = 1

        for open_idx, close_idx in parentheses_indices:
            self.format_txt.setForeground(recherche_couleur(index_parenthese))
            self.setFormat(open_idx, 1, self.format_txt)
            self.setFormat(close_idx, 1, self.format_txt)

            index_parenthese += 2

    @staticmethod
    def a___________________end______():
        pass


class TextFormule(QPlainTextEdit):
    size_change = pyqtSignal(int)
    editingFinished = pyqtSignal()

    def __init__(self, _):
        super().__init__(parent=None)

        # ---------------------------------------
        # autocompletion
        # ---------------------------------------

        self.autocompletion = None
        self.allplan = None
        self.highlighter = None

        self.font = self.font()
        self.currentsize = taille_police_menu

    def chargement(self, allplan: AllplanDatas):

        self.allplan = allplan

        # ---------------------------------------
        # autocompletion
        # ---------------------------------------

        self.autocompletion = WidgetAutocompletion(allplan=self.allplan, widget=self)

        # ---------------------------------------
        # ATTRIBUT FORMULE - SIGNAUX
        # ---------------------------------------

        self.textChanged.connect(self.changement)
        self.selectionChanged.connect(self.selection_change)

        # -----------------------------------
        # highlighter
        # ---------------------------------------

        size = settings_get(file_name=formula_setting_file, info_name="font_height")
        self.highlighter = None

        self.setsize(size)

        # self.autocompletion.show()

    @staticmethod
    def a___________________changement______():
        pass

    def changement(self):

        self.formula_format_check()

        self.allplan.gestion_tooltip_formule(self)

        modifiers = QApplication.keyboardModifiers()

        if self.hasFocus() and modifiers != Qt.ControlModifier:
            self.autocompletion.gestion_widget()

    def formula_format_check(self):

        formula_current = self.toPlainText()

        quote_count = formula_current.count('"')

        if quote_count % 2 != 0:
            return

        formula_format = self.allplan.formula_format(formula=formula_current)

        if formula_current == formula_format:
            return

        self.formula_change_text(new_formula=formula_format)

    def formula_convert_name_to_number(self):

        formula_current = self.toPlainText()

        if self.allplan is None:
            return

        if not self.allplan.formula_convert_name:
            return

        formula_format = self.allplan.formula_replace_all_name(formula=formula_current)

        if formula_current == formula_format:
            return

        self.formula_change_text(new_formula=formula_format)

    def formula_change_text(self, new_formula: str):

        cursor = self.textCursor()
        position = cursor.position()

        self.setPlainText(new_formula)

        cursor.setPosition(position)
        self.setTextCursor(cursor)

    @staticmethod
    def a___________________changement_selection______():
        pass

    def selection_change(self):

        self.allplan.gestion_tooltip_formule(self)
        selectionner_parentheses(self)

    def change_highlighter_action(self):

        if self.autocompletion is None or self.highlighter is None:
            return

        self.blockSignals(True)
        self.autocompletion.hide()

        if self.allplan.formula_color:

            self.highlighter = ParenthesesHighlighter(self.document(), self.currentsize)

        else:

            self.highlighter.deleteLater()

        self.autocompletion.hide()

        self.blockSignals(False)

    def zoom_in(self):
        if self.currentsize < min_size:
            return

        self.currentsize += 1
        self.setsize(self.currentsize)
        self.size_change.emit(self.currentsize)
        settings_save_value(file_name=formula_setting_file, key_name="font_height", value=self.currentsize)

    def zoom_out(self):

        if self.currentsize > max_size:
            return

        self.currentsize -= 1
        self.setsize(self.currentsize)
        self.size_change.emit(self.currentsize)
        settings_save_value(file_name=formula_setting_file, key_name="font_height", value=self.currentsize)

    def reset_font_size(self):
        self.currentsize = taille_police_menu
        self.setsize(self.currentsize)
        self.size_change.emit(self.currentsize)
        settings_save_value(file_name=formula_setting_file, key_name="font_height", value=self.currentsize)

    def setsize(self, font_size: int):

        if font_size is None:
            self.currentsize = taille_police_menu

        elif not isinstance(font_size, int):
            self.currentsize = taille_police_menu

        elif font_size > max_size:
            self.currentsize = max_size

        elif font_size < min_size:
            self.currentsize = min_size

        else:

            self.currentsize = font_size

        self.font.setPointSize(self.currentsize)
        self.setFont(self.font)

        if self.allplan.formula_color:
            self.highlighter = ParenthesesHighlighter(self.document(), self.currentsize)

        elif self.highlighter is not None:
            self.highlighter.deleteLater()

        else:
            self.highlighter = None

    @staticmethod
    def a___________________event______():
        pass

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MidButton:
            self.reset_font_size()

        super().mousePressEvent(event)

    def wheelEvent(self, event: QWheelEvent):

        super().wheelEvent(event)

        if not self.hasFocus():
            return

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier:

            delta = event.angleDelta().y()

            if delta > 0:
                self.zoom_in()

            elif delta < 0:
                self.zoom_out()

    def focusOutEvent(self, event: QFocusEvent):

        if isinstance(self.autocompletion, WidgetAutocompletion):
            if self.autocompletion.isVisible():
                super().focusOutEvent(event)
                return

        if self.allplan.formula_convert_name:
            self.formula_convert_name_to_number()

        self.editingFinished.emit()
        super().focusOutEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class WidgetAutocompletion(QWidget):

    def __init__(self, allplan: AllplanDatas, widget: QPlainTextEdit):
        super().__init__()

        self.allplan: AllplanDatas = allplan

        self.allplan.autocompletion_refresh_signal.connect(self.autocompletion_refresh)

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_Autocompletion()
        self.ui.setupUi(self)

        self.widget = widget
        self.position_cursor = 0
        self.len_position = 1

        self.liste_keys = ["+", "-", "*", "/", " ", "@", ";", '"', "_", "&", "|", "=", ">", "<", "<>", ">=", "<=",
                           "!", "^", ")", "("]

        self.liste_keys_stop = ["+", "-", "*", "/", ";", "&", "|", "=", ">", "<", "<>", ">=", "<=", "!", "^", ")", "("]

        self.filtre_liste = QSortFilterProxyModel()
        self.filtre_liste.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_liste.setSourceModel(self.allplan.model_autocompletion)
        self.filtre_liste.setSortLocaleAware(True)

        self.ui.liste.setModel(self.filtre_liste)

        self.ui.liste.doubleClicked.connect(self.ajouter_element)

        self.gestion_header()

        changer_selection_apparence(self.ui.liste)

    def personnaliser(self):
        """

        :return:
        """

        # print("Autocompletion -- personnaliser -- chargement")

        self.placement_autocompletion()

        self.ui.liste.setCurrentIndex(self.ui.liste.model().index(0, 0))
        self.ui.liste.scrollTo(self.ui.liste.currentIndex())

        self.show()

        # print("Autocompletion -- personnaliser -- chargement -- fin")

    def autocompletion_refresh(self):

        self.filtre_liste.setSourceModel(self.allplan.model_autocompletion)
        self.ui.liste.setModel(self.filtre_liste)

    def gestion_header(self):

        if self.allplan.model_autocompletion.rowCount() == 0:
            return

        self.ui.liste.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.liste.setColumnWidth(0, round(self.ui.liste.width() / 2))
        self.ui.liste.setColumnWidth(1, round(self.ui.liste.width() / 2))

    def ajouter_element(self, qmodelindex: QModelIndex):
        """
        Permet d'ajouter l'élément selectionné
        :param qmodelindex: qmodelindex de l'élément selectionné
        :return: None
        """

        # print("Autocompletion -- ajouter_element -- chargement")

        if not qm_check(qmodelindex):
            # print("Autocompletion -- ajouter_element -- qmodelindex is None")
            self.hide()
            return

        row_actuel = qmodelindex.row()

        qm_choix = self.filtre_liste.index(row_actuel, 0)

        if not qm_check(qm_choix):
            self.hide()
            return

        choix = qm_choix.data()

        if not isinstance(choix, str):
            # print(f"Autocompletion -- ajouter_element - choix is None")
            self.hide()
            return

        if not choix.startswith("@") or choix.startswith("@OBJ@="):
            choix: str = self.filtre_liste.index(row_actuel, 1).data()

        texte = self.widget.toPlainText()
        if len(texte) < self.position_cursor:
            # print("Autocompletion -- ajouter_element -- len(texte) < self.position_cursor")
            return

        position_dbu_texte = self.position_cursor - self.len_position

        if position_dbu_texte < 0:
            # print(f"Autocompletion -- ajouter_element --  {self.position_cursor} - {self.len_position} < 0 ")
            return

        debut_txt = texte[:position_dbu_texte]

        debut_txt_arrobase_count = debut_txt.count("@")

        if debut_txt.endswith("@") and debut_txt_arrobase_count % 2 != 0:
            debut_txt = debut_txt[:-1]

            position_dbu_texte -= 1

        fin_txt = texte[self.position_cursor:]

        fin_txt_arrobase_count = fin_txt.count("@")

        if fin_txt.startswith("@") and fin_txt_arrobase_count % 2 != 0:
            fin_txt = fin_txt[1:]

        if fin_txt == "@":
            texte_final = f"{debut_txt}{choix}"

        else:
            texte_final = f"{debut_txt}{choix}{fin_txt}"

        # --------

        nouvelle_position: int = position_dbu_texte + len(choix)

        # --------

        error_dict = {"_ELSE__IF_ELSE__IF_(": "_ELSE__IF_(",
                      "_ELSE__ELSE__IF_(": "_ELSE__IF_(",
                      "_IF_IF_(": "_IF_("}

        for value_error, value_new in error_dict.items():

            if value_error not in texte_final:
                continue

            texte_final = texte_final.replace(value_error, value_new)

            nouvelle_position -= len(value_error) - len(value_new)

        # --------

        self.widget.setPlainText(texte_final)

        # print(f"Autocompletion -- ajouter_element -- replacement cursor "
        #       f" pos :{self.position_cursor} -- len_pos :  {self.len_position} -- len(choix) : {len(choix)} -- "
        #       f"new_pos :{nouvelle_position}")

        text_cursor = self.widget.textCursor()
        text_cursor.setPosition(nouvelle_position)

        self.widget.setTextCursor(text_cursor)

        self.hide()

        # print("Autocompletion -- ajouter_element -- chargement -- fin")

    def gestion_widget(self):
        """

        :return:
        """

        # ---------------------------------------
        # GESTION DU WIDGET AUTOCOMPLETION
        # ---------------------------------------
        # print("-----------------------------------------------")

        if self.isVisible():
            self.hide()

        nb_char = len(self.widget.toPlainText())

        if nb_char == 0:
            self.hide()
            self.widget.setFocus()
            return

        # print("widget_autocompletion -- gestion_widget -- gestion autocompletion")

        self.position_cursor = self.widget.textCursor().position()

        # print(f"widget_autocompletion -- gestion_widget"
        #       f" -- position_cursor = {self.position_cursor} / {len(self.widget.toPlainText())}")

        texte = self.widget.toPlainText()

        texte_partiel = texte[:self.position_cursor]
        # print(f"widget_autocompletion -- gestion_widget -- texte_partiel = {texte_partiel}")

        if self.position_cursor > 1:
            texte_actuel = texte[self.position_cursor - 1]
            # print(f"widget_autocompletion -- gestion_widget -- texte_actuel = {texte_actuel}")

            if texte_actuel == "(" or texte_actuel == ")":
                self.hide()
                self.widget.setFocus()
                return

        texte_analyse = ancien_texte_analyse = ""
        recherche_ok = False

        # print("widget_autocompletion -- gestion_widget -- recherche texte")
        nb_lettres = len(texte_partiel)

        for position, lettre_analysee in enumerate(reversed(texte_partiel)):

            if lettre_analysee in self.liste_keys_stop:
                ancien_texte_analyse = texte_analyse
                recherche_ok = True
                break

            if lettre_analysee == "_":
                if nb_lettres - position - 6 >= 0:

                    test_else = texte_partiel[nb_lettres - position - 6:nb_lettres - position]
                    test_else = test_else.upper()

                    if test_else == "_ELSE_":
                        ancien_texte_analyse = texte_analyse
                        recherche_ok = True
                        break

            texte_analyse = f"{lettre_analysee.upper()}{texte_analyse}"

            # print(f"widget_autocompletion -- gestion_widget -- {texte_analyse}")

            recherche: list = self.allplan.model_autocompletion.findItems(texte_analyse, Qt.MatchContains, 0)

            if len(recherche) == 0:
                # print(f"widget_autocompletion -- gestion_widget -- len(recherche) == 0 -- break")
                break

            else:
                # print(f"widget_autocompletion -- gestion_widget -- "
                #       f"len(recherche) > 0 -- ancien_texte_analyse: {ancien_texte_analyse}"
                #       f" -- ancien_texte_analyse: {texte_analyse}")
                ancien_texte_analyse = texte_analyse
                recherche_ok = True

                if texte_analyse == "_":
                    break

        # print(f"widget_autocompletion -- gestion_widget -- recherche texte -- fin -- {ancien_texte_analyse}")

        if not recherche_ok:
            self.len_position = 1
            self.hide()

            # print("widget_autocompletion -- gestion_widget -- not recherche_ok --
            # cacher widget autocompletion -- fin")
            return

        ancien_texte_analyse = ancien_texte_analyse.strip()

        if len(ancien_texte_analyse) == 0:
            self.len_position = 1
        else:
            self.len_position = len(ancien_texte_analyse)

        # print(f"widget_autocompletion -- gestion_widget -- "
        #       f"filtrage du model : {ancien_texte_analyse} -- len_pos : {self.len_position}")

        self.filtre_liste.setFilterFixedString(ancien_texte_analyse)

        # print(self.filtre_liste.rowCount())

        # print(f"widget_autocompletion -- gestion_widget -- gestion affichage widget autocompletion")

        if self.filtre_liste.rowCount() > 0 and (
                ancien_texte_analyse != "" or (texte_analyse != "" and self.position_cursor == 1)):

            self.personnaliser()

            # print("widget_autocompletion -- gestion_widget -- affichage widget autocompletion")

        else:

            self.hide()

            # print("widget_autocompletion -- gestion_widget -- cacher widget autocompletion")

        self.widget.setFocus()
        # print("widget_autocompletion -- gestion_widget -- gestion affichage widget autocompletion -- fin")

    def placement_autocompletion(self):
        """
        Permet de positionner le widget en fonction de la position du curseur
        :return: None
        """

        position_curseur: QRect = self.widget.cursorRect()

        position_x = position_curseur.x()

        if position_x + self.width() < self.widget.width():
            largeur = 10
        else:
            largeur = self.width() - 10

        point = self.widget.mapToGlobal(QPoint(0, 0))

        point = QPoint(point.x() + position_curseur.x() - largeur,
                       point.y() + position_curseur.y() + 20)

        position_y = point.y() + self.height()

        if position_y > 1080:
            point = QPoint(point.x(), point.y() - self.height() - position_curseur.y() - 20)

        self.move(point)

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if not isinstance(self.widget, TextFormule):
            return

        if event.key() == Qt.Key_Up:

            row_actuel = self.ui.liste.currentIndex().row() - 1

            if row_actuel < 0:
                row_actuel = 0

            self.ui.liste.setCurrentIndex(self.ui.liste.model().index(row_actuel, 0))

            # print(f"Autocompletion -- keyPressEvent -- key_event.key() == Qt.Key_Up -- "
            #       f"{self.ui.liste.currentIndex().data()}")

            event.accept()

            return

        if event.key() == Qt.Key_Down:

            row_actuel = self.ui.liste.currentIndex().row() + 1

            if row_actuel >= self.filtre_liste.rowCount():
                row_actuel = self.filtre_liste.rowCount() - 1

            self.ui.liste.setCurrentIndex(self.ui.liste.model().index(row_actuel, 0))

            # print(f"Autocompletion -- keyPressEvent -- key_event.key() == Qt.Key_Down -- "
            #       f"{self.ui.liste.currentIndex().data()}")

            event.accept()

            return

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return or event.key() == Qt.Key_Tab:
            # print("Autocompletion -- keyPressEvent -- "
            #       "key_event.key() == Qt.Key_Enter or key_event.key() == Qt.Key_Return")

            self.ajouter_element(self.ui.liste.currentIndex())

            event.accept()

            return

        if event.text().isalnum() or event.text() in self.liste_keys:
            # print("Autocompletion -- keyPressEvent -- "
            #       "key_event.text().isalnum() or key_event.text() in self.liste_keys")
            try:
                self.widget.keyPressEvent(event)
            except Exception:
                return

            self.gestion_widget()
            event.accept()

            return

        self.hide()

        self.widget.setFocus()

        try:
            self.widget.keyPressEvent(event)
        except Exception:
            return
        # print("Autocompletion -- keyPressEvent -- chargement -- fin")

        event.accept()

    @staticmethod
    def a___________________end______():
        pass


class BoutonVerif(QPushButton):

    def __init__(self, _):
        super().__init__(parent=None)

        self.clicked.connect(self.afficher_message)

        self.isvalid = True

    def verification(self, texte: str, allplan: AllplanDatas):

        texte = texte.strip()

        message = allplan.verification_formule(formula=texte)

        if message != "":
            self.isvalid = False
            self.setIcon(get_icon(error_icon))
            self.setToolTip(message)

        else:
            self.isvalid = True
            self.setIcon(get_icon(valid_icon))
            self.setToolTip(self.tr("C'est tout bon!"))

    def afficher_message(self):

        tooltip = self.toolTip()

        if tooltip == self.tr("C'est tout bon!"):

            msg(titre=application_title,
                message=self.tr("Cette formule paraît correcte !"),
                icone_valide=True)

        elif tooltip == self.tr("Formule à modifier directement depuis Allplan"):

            a = self.tr("Cette formule est une formule 'Utilisateur'.\n")
            c = self.tr("Pour la modifier, il faudra le faire depuis Allplan.")

            msg(titre=application_title,
                message=f"{a}\n{c}",
                icone_lock=True)

        else:
            msg(titre=application_title,
                message=f"{tooltip}",
                icone_critique=True)

    @staticmethod
    def a___________________end______():
        pass
