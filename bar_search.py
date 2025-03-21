#!/usr/bin/python3
# -*- coding: utf-8 -*

from bar_search_filter import SearchFiterWidget
from catalog_manage import *
from search_replace import Replace

search_completer_max_items = 10


class SearchBar(QObject):

    def __init__(self, asc):
        super().__init__()

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.asc = asc
        self.ui: Ui_MainWindow = self.asc.ui
        self.hierarchy: Hierarchy = self.ui.hierarchy

        self.catalog: CatalogDatas = self.asc.catalog
        self.allplan: AllplanDatas = self.asc.allplan

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        # -----------------------------------------------
        # search_filter_widget
        # -----------------------------------------------

        self.search_filter_widget = SearchFiterWidget(asc=asc, filter_button=self.ui.search_bt)
        self.search_filter_widget.modify_search_filter.connect(self.search_filter_changed)
        self.search_filter_widget.cancel_search_filter.connect(self.search_clear)

        # -----------------------------------------------
        # replace_widget
        # -----------------------------------------------

        self.replace_widget = Replace(self.asc,
                                      self.catalog,
                                      self.asc.library_widget)

        # -----------------------------------------------
        # Completer
        # -----------------------------------------------

        self.search_recent_model = QStringListModel(self.asc.search_recent)

        # -----------------------------------------------
        # Completer
        # -----------------------------------------------

        self.search_qcompleter = QCompleter(self.search_recent_model)
        self.search_qcompleter.setFilterMode(Qt.MatchContains)
        self.search_qcompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_qcompleter.setModelSorting(QCompleter.CaseInsensitivelySortedModel)

        self.ui.search_line.setCompleter(self.search_qcompleter)

        # -----------------------------------------------
        # Signals
        # -----------------------------------------------

        self.ui.search_line.textChanged.connect(self.search_line_changed)

        self.ui.search_bt.clicked.connect(self.search_filter_show)
        self.ui.search_bt.customContextMenuRequested.connect(self.search_filter_show)

        self.ui.search_replace_bt.clicked.connect(self.asc.formula_widget_close)
        self.ui.search_replace_bt.clicked.connect(self.replace_widget.replace_show)

        self.ui.search_error_bt.clicked.connect(self.search_error_clicked)

    @staticmethod
    def a___________________search_______________():
        pass

    def search_line_changed(self):

        if not self.ui.search_bt.isChecked():
            return

        self.asc.formula_widget_close()

        text = self.ui.search_line.text()

        text = text.strip()

        if text != "":
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

            self.ui.search_error_bt.setEnabled(False)
            self.ui.search_replace_bt.setEnabled(False)

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

        self.asc.bouton_expand_collapse()

    @staticmethod
    def a___________________filter_setting_______________():
        pass

    def search_filter_show(self):

        self.asc.formula_widget_close()

        if not self.ui.search_bt.isChecked():
            self.search_clear()
            return

        self.ui.search_bt.setChecked(False)

        self.hierarchy.save_qm_model_expanded_list()

        self.search_recent_add_text()
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

        self.asc.formula_widget_close()

        self.ui.attributes_detail.clear()

        self.ui.search_bt.setChecked(False)

        self.ui.search_line.setStyleSheet("QLineEdit{padding-left:5px; border: 1px solid #8f8f91;border-radius:5px; }")

        self.ui.search_bt.setIcon(get_icon(search_icon))
        self.ui.search_bt.setToolTip(self.tr("Lancer la recherche"))

        # ----------------------------

        self.ui.search_error_bt.setChecked(False)
        self.ui.search_error_bt.setText("")
        self.ui.search_error_bt.setToolTip(self.tr("Lancer la recherche des Formules contenant des erreurs"))

        # ----------------------------

        self.ui.search_line.setEnabled(True)
        self.ui.search_bt.setEnabled(True)
        self.ui.search_error_bt.setEnabled(True)
        self.ui.search_replace_bt.setEnabled(True)

        self.hierarchy.search_clear()

    @staticmethod
    def a___________________search_recent_list_______________():
        pass

    def search_recent_add_text(self):

        if not isinstance(self.asc.search_recent, list):
            return

        text = self.ui.search_line.text().strip()

        if text == "":
            return

        if text in self.asc.search_recent:
            return

        items_count = len(self.asc.search_recent)

        if items_count > search_completer_max_items:
            self.asc.search_recent.pop()

        self.asc.search_recent.insert(0, text)

        self.search_recent_model.setStringList(self.asc.search_recent)

    @staticmethod
    def a___________________search_error______():
        pass

    def search_error_clicked(self):

        self.asc.formula_widget_close()

        if not self.ui.search_error_bt.isChecked():
            self.search_clear()
            return

        if not self.hierarchy.search_formula_with_error():
            msg(titre=application_title,
                message=self.tr("Aucune formule avec erreur trouvée!"),
                icone_valide=True)
            self.search_clear()
            return

        # ----------------------------

        self.hierarchy.save_qm_model_expanded_list()

        # ------------
        # First filter
        # ------------

        if self.hierarchy.cat_filter_1.filterKeyColumn != col_cat_value:
            self.hierarchy.cat_filter_1.setFilterKeyColumn(col_cat_value)

        if self.hierarchy.cat_filter_1.filterRole != user_formule_ok:
            self.hierarchy.cat_filter_1.setFilterRole(user_formule_ok)

        self.hierarchy.cat_filter_1.setFilterRegExp(r"^.*\S+.*$")

        # row_count = self.catalog.cat_filter.rowCount()

        # ------------
        # Second filter
        # ------------

        if debug:

            if self.hierarchy.cat_filter_2.filterRegExp().pattern() != "":
                self.hierarchy.cat_filter_2.setFilterRegExp("")

        else:

            if self.hierarchy.cat_filter_2.filterRegExp().pattern() != pattern_filter:
                self.hierarchy.cat_filter_2.setFilterRegExp(pattern_filter)

        # row_count_2 = self.hierarchy.cat_filter_2.rowCount()

        # ----------------------------

        if self.hierarchy.cat_filter_2.rowCount() == 0:
            self.search_clear()

            msg(titre=application_title,
                message=self.tr("Aucune formule avec erreur trouvée!"),
                icone_valide=True)
            return

        # ----------------------------

        self.hierarchy.blockSignals(True)
        self.hierarchy.expandAll()
        self.hierarchy.blockSignals(False)

        # ----------------------------

        self.ui.search_line.setEnabled(False)
        self.ui.search_bt.setEnabled(False)
        self.ui.search_replace_bt.setEnabled(False)

        self.ui.search_error_bt.setToolTip(self.tr("Arrêter la recherche des Formules contenant des erreurs"))
        self.ui.search_error_bt.setText(self.tr("Arrêter"))

        self.catalog.select_first_formula_error()

        self.hierarchy.header_manage()

    @staticmethod
    def a___________________end______():
        pass
