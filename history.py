#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from history_manage import ActionInfo, index_action
from tools import changer_selection_apparence, taille_police_menu, menu_ht_ligne


class WidgetHistory(QListWidget):

    undo_selection_signal = pyqtSignal(list)
    redo_selection_signal = pyqtSignal(list)

    def __init__(self, parent_actuel, mode_current: str):
        super().__init__(parent=parent_actuel)

        self.setGeometry(100, 100, 300, 300)

        self.setWindowFlags(Qt.Popup)

        self.mode_current = mode_current

        self.selected_events = list()

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.MultiSelection)

        self.setIconSize(QSize(20, 20))
        self.setGridSize(QSize(self.gridSize().width(), menu_ht_ligne))

        self.setMouseTracking(True)
        self.itemEntered.connect(self.item_hovered)
        self.itemPressed.connect(self.item_selected)

        changer_selection_apparence(self)

        self.installEventFilter(self)

    def chargement(self, dict_actions: dict):

        self.clear()

        for event, action in reversed(dict_actions.items()):

            if not isinstance(action, ActionInfo):
                continue

            qlistwidgetitem = QListWidgetItem(action.action_name)
            qlistwidgetitem.setData(index_action, event)

            font = qlistwidgetitem.font()
            font.setPointSize(taille_police_menu)
            qlistwidgetitem.setFont(font)

            qlistwidgetitem.setIcon(action.action_icon)

            qlistwidgetitem.setToolTip(action.action_tooltips)

            self.addItem(qlistwidgetitem)

    def item_hovered(self, item: QListWidgetItem):

        index_actuel = self.indexFromItem(item).row()

        for index_item in range(self.count()):
            item = self.item(index_item)

            item.setSelected(index_item <= index_actuel)

    def item_selected(self):

        self.selected_events = list()

        for index_item in range(self.count()):

            item = self.item(index_item)

            self.selected_events.append(item.data(index_action))

            if not item.isSelected():
                break

        if self.mode_current == "undo":
            self.undo_selection_signal.emit(self.selected_events)

        elif self.mode_current == "redo":
            self.redo_selection_signal.emit(self.selected_events)

        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj == self.verticalScrollBar() or obj == self.horizontalScrollBar():
            return super().eventFilter(obj, event)

        if event.type() == QEvent.MouseButtonRelease:
            self.hide()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
