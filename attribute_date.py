#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from allplan_manage import AttributeDatas
from catalog_manage import MyQstandardItem
from history_manage import AttributeModifyData
from main_datas import user_guid
from tools import ValidatorDate, move_widget_ss_bouton, set_appearance_number, date_formatting
from ui_attribute_date import Ui_AttributeDate
from ui_calendar import Ui_Calendar


class AttributeDate(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict)

    def __init__(self, qs_value: MyQstandardItem, language, attribute_obj: AttributeDatas):
        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeDate()
        self.ui.setupUi(self)

        # ----------------------------------

        if isinstance(attribute_obj, AttributeDatas):

            self.ui.num_attrib.setText(attribute_obj.number)

            self.ui.name_attrib.setText(attribute_obj.name)
            self.ui.name_attrib.setToolTip(attribute_obj.tooltips)

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.qs_value = qs_value
        self.ui.value_attrib.setText(self.qs_value.text())

        # -----------------------------------------------
        # Calendar
        # -----------------------------------------------

        self.calendar_widget = WidgetCalendar(parent_widget=self, language=language)
        self.calendar_widget.date_changed.connect(self.date_changed)

        # -----------------------------------------------
        # Validator
        # -----------------------------------------------

        self.ui.value_attrib.setValidator(ValidatorDate())

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.calendar_bt.clicked.connect(self.calendar_show)
        self.ui.value_attrib.editingFinished.connect(self.date_update)

        # -----------------------------------------------

    @staticmethod
    def a___________________date_loading______():
        pass

    def date_loading(self):

        set_appearance_number(self.ui.num_attrib)

    @staticmethod
    def a___________________date_changed______():
        pass

    def date_changed(self, new_date: str):

        self.ui.value_attrib.setText(new_date)
        self.ui.value_attrib.setFocus()

        self.date_update()

    def date_update(self):

        new_date = self.ui.value_attrib.text()
        value_new = date_formatting(new_date)

        value_current = self.qs_value.text()

        # -------------

        if value_new == "":
            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(value_current)
            self.ui.value_attrib.blockSignals(False)
            return

        # -------------

        if value_new != new_date:
            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(value_new)
            self.ui.value_attrib.blockSignals(False)

        if value_current == value_new:
            return

        # -------------

        self.qs_value.setText(value_new)

        # -------------

        number_current = self.ui.num_attrib.text()

        value_dict = {number_current: [value_current, value_new]}

        # -------------

        qs_parent = self.qs_value.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_date -- date_update -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_date -- date_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_date -- date_update -- not isinstance(parent_name, str)")
            return

        # -------------

        data = AttributeModifyData(number_current=number_current, value_new=value_current)

        attribute_data = [data]

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict)

    @staticmethod
    def a___________________dalendar_show______():
        pass

    def calendar_show(self):

        move_widget_ss_bouton(button=self.ui.calendar_bt, widget=self.calendar_widget)

        self.calendar_widget.calendar_loading(current_date=self.ui.value_attrib.text())

    @staticmethod
    def a___________________end______():
        pass


class WidgetCalendar(QWidget):
    date_changed = pyqtSignal(str)

    def __init__(self, parent_widget, language: str):
        super().__init__(parent=parent_widget)

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_Calendar()
        self.ui.setupUi(self)

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------
        self.current_date = ""

        if language != "FR":
            self.date_format = "MM/dd/yyyy"
        else:
            self.date_format = "dd/MM/yyyy"

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.today.clicked.connect(self.calendar_select_today)
        self.installEventFilter(self)

    def calendar_loading(self, current_date: str):

        self.current_date = current_date
        self.ui.calendar_widget.setSelectedDate(QDate.fromString(self.current_date, self.date_format))
        self.ui.calendar_widget.setFocus()
        self.show()

    def calendar_select_today(self):

        self.ui.calendar_widget.setSelectedDate(QDate.currentDate())

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        current_date = self.ui.calendar_widget.selectedDate().toString(self.date_format)

        if current_date != self.current_date:
            self.date_changed.emit(current_date)

        super().closeEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if event.type() == QEvent.MouseButtonRelease:
            self.close()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
