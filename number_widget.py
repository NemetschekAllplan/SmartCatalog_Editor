#!/usr/bin/python3
# -*- coding: utf-8 -*


from PyQt5.Qt import *

from hierarchy import material_code
from main_datas import number_setting_file, number_setting_datas, component_code
from tools import settings_read, settings_save, move_window_tool
from ui_number import Ui_Number

nb_max_txt = 20


class SeparatorHighlighter(QSyntaxHighlighter):
    def __init__(self, separator, parent=None):
        super().__init__(parent)

        self.separator = separator

    def highlightBlock(self, text):

        if self.separator == "":
            return

        separator_format_before = QTextCharFormat()
        separator_format_before.setForeground(QColor("blue"))
        separator_format_after = QTextCharFormat()
        separator_format_after.setForeground(QColor("orange"))

        if self.separator in text:
            index = text.index(self.separator)
            self.setFormat(0, index, separator_format_before)
            self.setFormat(index + 1, len(text) - index - 1, separator_format_after)
        else:
            self.setFormat(0, len(text), separator_format_before)

    def update_separator(self, separator):
        self.separator = separator
        self.rehighlight()


class WidgetNumber(QWidget):
    save_item = pyqtSignal(list, str, str)

    def __init__(self):
        super().__init__()

        # Création de l'interface
        self.ui = Ui_Number()
        self.ui.setupUi(self)
        self.type_element = material_code
        self.nom_onglet = ""

        self.ui.spin.setMaximum(nb_max_txt)

        # -----------------------------------------------
        # Settings
        # -----------------------------------------------

        number_datas = settings_read(number_setting_file)

        self.ismaximized_on = number_datas.get("ismaximized_on", False)

        if not isinstance(self.ismaximized_on, bool):
            self.ismaximized_on = False

        width = number_datas.get("width", number_setting_datas["width"])

        if not isinstance(width, int):
            width = number_setting_datas["width"]

        height = number_datas.get("height", number_setting_datas["height"])

        if not isinstance(height, int):
            width = number_setting_datas["height"]

        self.resize(width, height)

        # -----------------------------------------------

        number = number_datas.get("number", number_setting_datas["number"])

        if not isinstance(number, str):
            number = number_setting_datas["number"]

        self.ui.spin.setValue(number)

        # -----------------------------------------------

        description = number_datas.get("description", number_setting_datas["description"])

        if not isinstance(description, str):
            description = number_setting_datas["number"]

        self.ui.description_chk.setChecked(description)

        # -----------------------------------------------

        separator = number_datas.get("separator", number_setting_datas["separator"])

        if not isinstance(separator, str):
            separator = number_setting_datas["separator"]

        self.ui.separator.setText(separator)
        self.highlighter = SeparatorHighlighter(separator, self.ui.titles.document())

        # -----------------------------------------------

        self.ui.titles.textChanged.connect(self.gestion_titres)

        self.ui.description_chk.clicked.connect(self.description_option_changed)
        self.ui.separator.textEdited.connect(self.separator_changed)

        self.ui.bt_valider.clicked.connect(self.save)
        self.ui.bt_quitter.clicked.connect(self.close)

    def personnaliser(self, type_element: str, nom_onglet=""):

        self.ui.spin.setValue(1)
        self.ui.titles.clear()

        self.type_element = type_element
        self.nom_onglet = nom_onglet

        self.ui.spin.setFocus()
        self.ui.spin.selectAll()

        self.show()

    def gestion_titres(self):

        texte = self.ui.titles.toPlainText().strip()

        if texte == "":
            self.ui.spin.setEnabled(True)
            return

        self.ui.spin.setEnabled(False)

        if "\n" not in texte:
            self.ui.spin.setValue(1)
            return

        liste_texte = self.creation_liste()

        nb_texte = len(liste_texte)

        self.ui.spin.setValue(nb_texte)

        if nb_texte > nb_max_txt:
            self.ui.spin.setValue(nb_max_txt)
            self.ui.titles.blockSignals(True)
            self.ui.titles.setPlainText("\n".join(liste_texte[:nb_max_txt]))
            self.ui.titles.blockSignals(False)
            self.ui.titles.moveCursor(QTextCursor.End)
        else:
            self.ui.spin.setValue(nb_texte)

    def creation_liste(self) -> list:

        texte = self.ui.titles.toPlainText().strip()

        liste = texte.split("\n")

        liste_upper = list()
        liste_clean = list()

        separator = self.ui.separator.text()

        if not self.ui.description_chk.isChecked():
            separator = ""

        for title in liste:

            title_upper = title.strip().upper()
            description = ""

            if title_upper == "":
                continue

            # --------------------------------------

            if separator == "" or separator not in title:
                if self.type_element != component_code and title_upper not in liste_upper:
                    liste_clean.append([title, description])
                    liste_upper.append(title_upper)
                    continue

                if self.type_element == component_code:
                    liste_clean.append([title, description])
                    continue

                continue

            # --------------------------------------

            title_datas = title.split(separator, maxsplit=1)

            if len(title_datas) != 2:

                if self.type_element != component_code and title_upper not in liste_upper:
                    liste_clean.append([title, description])
                    liste_upper.append(title_upper)
                    continue

                if self.type_element == component_code:
                    liste_clean.append([title, description])
                    continue

                continue

            # --------------------------------------

            title, description = title_datas

            if not isinstance(title, str):
                continue

            if not isinstance(description, str):
                description = ""

            title = title.strip()
            description = description.strip()

            title_upper = title.upper()

            if self.type_element != component_code and title_upper in liste_upper:
                continue

            liste_clean.append([title, description])
            liste_upper.append(title_upper)

        return liste_clean

    def save(self):

        nombre = self.ui.spin.value()
        self.close()

        texte = self.ui.titles.toPlainText().strip()

        if texte == "":
            liste = ["" for _ in range(nombre)]
        else:
            liste = self.creation_liste()

        self.save_item.emit(liste, self.type_element, self.nom_onglet)

    def number_settings_save(self):

        datas_config = settings_read(file_name=number_setting_file)

        # -----------------------------------------------

        datas_config["number"] = self.ui.spin.value()
        datas_config["description"] = self.ui.description_chk.isChecked()
        datas_config["separator"] = self.ui.separator.text()

        # -----------------------------------------------

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True

                settings_save(file_name=number_setting_file, config_datas=datas_config)
                return

        datas_config["height"] = self.size().height()
        datas_config["width"] = self.size().width()
        datas_config["ismaximized_on"] = False

        # -----------------------------------------------

        settings_save(file_name=number_setting_file, config_datas=datas_config)

    @staticmethod
    def a___________________description______():
        pass

    def description_option_changed(self):

        self.ui.separator.setEnabled(self.ui.description_chk.isChecked())

        if self.ui.description_chk.isChecked():
            self.highlighter.update_separator(self.ui.separator.text())
        else:
            self.highlighter.update_separator("")

    def separator_changed(self):
        self.highlighter.update_separator(self.ui.separator.text())

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.hide()

        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.save()

        super().keyPressEvent(event)

    def changeEvent(self, event: QEvent):

        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.ismaximized_on = True

            else:
                self.ismaximized_on = False
                move_window_tool(widget_parent=self, widget_current=self)

        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent):

        self.number_settings_save()

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass
