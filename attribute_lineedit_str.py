#!/usr/bin/python3
# -*- coding: utf-8 -*
from allplan_manage import AttributeDatas
from formatting_widget import Formatting
from hierarchy import MyQstandardItem, Material, Info
from main_datas import *
from history_manage import AttributeModifyData
from tools import set_appareance_button, set_appearance_number, set_appearence_type
from ui_attribute_lineedit_str import Ui_AttributeLineeditStr


class AttributeLineeditStr(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict)
    link_desc_changed_signal = pyqtSignal(str, str)

    def __init__(self, allplan_version: str,
                 qs_value: MyQstandardItem,
                 qs_desc: MyQstandardItem,
                 attribute_obj: AttributeDatas,
                 listwidgetitem: QListWidgetItem,
                 is_material=False):

        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeLineeditStr()
        self.ui.setupUi(self)

        set_appareance_button(self.ui.formatting_bt)

        self.allplan_version = allplan_version

        self.ui.value_attrib.setViewportMargins(0, 0, 0, -3)

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.code_title = QLabel("")

        self.max_row = 7
        self.adjust_height_active = False
        self.adjust_height_action = False

        self.current_text = ""

        self.listwidgetitem = listwidgetitem

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.qs_value = qs_value
        self.ui.value_attrib.setPlainText(self.qs_value.text())

        self.qs_desc = qs_desc

        # ----------------------------------

        if isinstance(attribute_obj, AttributeDatas):

            if is_material:
                min_value = attribute_obj.min_val
                max_value = attribute_obj.max_val
                # max_value = "2048"

            else:

                min_value = "0"
                max_value = "2048"

            self.ui.num_attrib.setText(attribute_obj.number)

            self.ui.name_attrib.setText(attribute_obj.name)
            self.ui.name_attrib.setToolTip(attribute_obj.tooltips)

        else:

            self.attrib_option = code_attr_str

            self.unit_attrib = ""

            min_value = "0"
            max_value = "2048"

        # ----------------------------------

        if not isinstance(min_value, str):

            self.min_value = None

        else:

            try:

                self.min_value = int(min_value)

            except Exception:

                self.min_value = None

        # ----------------------------------

        if not isinstance(max_value, str):

            self.max_value = None

        else:

            try:

                self.max_value = int(max_value)

            except Exception:

                self.max_value = None

        # -----------------------------------------------
        # Formatting
        # -----------------------------------------------

        self.formatting_widget = Formatting()
        self.formatting_widget.save_modif_formatage.connect(self.formatting_changed)

        # ----------------------------------

        self.ui.type_attrib.installEventFilter(self)

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.value_attrib.textChanged.connect(self.lineedit_changed)

        self.ui.value_attrib.installEventFilter(self)

        self.ui.formatting_bt.clicked.connect(self.formatting_show)

        # -----------------------------------------------

    @staticmethod
    def a___________________lineedit_height______():
        pass

    def adjust_height(self):

        self.adjust_height_action = True

        if self.adjust_height_active:
            self.adjust_height_action = False
            return

        font = self.ui.value_attrib.document().defaultFont()
        fontmetrics = QFontMetrics(font)
        espace = fontmetrics.lineSpacing()
        border = 9

        row_count = round(self.ui.value_attrib.document().size().height())

        if row_count == 1:

            self.ui.label.setVisible(False)

            self.ui.formatting_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; "
                                                "border-left-width: 0px; padding-left: 1px; "
                                                "border-top-right-radius: 5px ; "
                                                "border-bottom-right-radius: 5px; "
                                                "background-color:#FFFFFF; }\n"
                                                "QPushButton:hover{border-left-width: 1px; "
                                                "padding: 0px; "
                                                "background-color: "
                                                "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                                                "stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
                                                "QPushButton:pressed{border-left-width: 1px; "
                                                "padding: 0px; background-color: "
                                                "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                                                "stop:0 #8FADCC, stop:1 #F8F8F8); }")

        else:

            self.ui.label.setVisible(True)

            self.ui.formatting_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; "
                                                "border-left-width: 0px; "
                                                "padding-left: 1px; "
                                                "border-bottom-width: 0px; "
                                                "padding-bottom: 1px; "
                                                "border-top-right-radius: 5px ; "
                                                "background-color:#FFFFFF; }\n"
                                                "QPushButton:hover{border-left-width: 1px; "
                                                "border-bottom-width: 1px; padding: 0px; "
                                                "background-color: qlineargradient(spread:pad, x1:0, "
                                                "y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
                                                "QPushButton:pressed{border-left-width: 1px; "
                                                "border-bottom-width: 1px; padding: 0px; "
                                                "background-color: qlineargradient(spread:pad, x1:0, y1:0,"
                                                " x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")

        if row_count <= self.max_row:

            if self.ui.value_attrib.verticalScrollBarPolicy() != Qt.ScrollBarAlwaysOff:
                self.ui.value_attrib.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.ui.value_attrib.verticalScrollBar().setValue(0)

        else:

            row_count = self.max_row

            self.ui.value_attrib.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # ------------------------------

        height_plaintext = (row_count * espace) + border

        height_widget = height_plaintext + 14

        if height_widget < 40:
            height_widget = 40

        # ------------------------------

        self.ui.value_attrib.setFixedHeight(height_plaintext)

        if row_count > 1:
            self.update()

            label_height = height_plaintext - self.ui.formatting_bt.height()
            self.ui.label.setFixedHeight(label_height)

        # ------------------------------

        self.listwidgetitem.setSizeHint(self.sizeHint())

        try:
            self.listwidgetitem.setSizeHint(QSize(self.width(), height_widget))

        except Exception:
            pass

        self.adjust_height_action = False

    def adjust_width(self):

        if not self.isVisible():
            return

        self.adjustSize()

    @staticmethod
    def a___________________lineedit_loading______():
        pass

    def lineedit_loading(self):

        set_appearance_number(self.ui.num_attrib)
        set_appearence_type(self.ui.type_attrib, code_attr_str)

        self.adjust_height()

    @staticmethod
    def a___________________changement______():
        pass

    def lineedit_changed(self):

        self.ui.formatting_bt.setEnabled(self.ui.value_attrib.toPlainText().strip() != "")

        current_text = self.ui.value_attrib.toPlainText()
        current_text_count = len(current_text)

        if "\n" in current_text:

            cursor = self.ui.value_attrib.textCursor()

            position = cursor.position()

            new_text = current_text.replace("\n", "")

            decalage = current_text_count - len(new_text)

            self.ui.value_attrib.blockSignals(True)

            self.ui.value_attrib.setPlainText(new_text)

            self.ui.value_attrib.blockSignals(False)

            cursor.setPosition(position - decalage)

            self.ui.value_attrib.setTextCursor(cursor)

        elif self.max_value is not None:

            if current_text_count > self.max_value:

                cursor = self.ui.value_attrib.textCursor()

                position = cursor.position()

                if self.current_text == "":
                    self.current_text = current_text[:self.max_value]
                    decalage = self.max_value
                else:
                    decalage = current_text_count - len(self.current_text)

                self.ui.value_attrib.blockSignals(True)

                self.ui.value_attrib.setPlainText(self.current_text)

                self.ui.value_attrib.blockSignals(False)

                cursor.setPosition(position - decalage)

                self.ui.value_attrib.setTextCursor(cursor)

        self.current_text = self.ui.value_attrib.toPlainText()

        self.adjust_height()

    def lineedit_update(self):

        value_current = self.qs_value.text()
        value_new = self.ui.value_attrib.toPlainText()

        if value_new != value_new.strip():
            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setPlainText(value_new.strip())
            self.ui.value_attrib.blockSignals(False)
            value_new = value_new.strip()

        if value_current == value_new:
            return

        # -------------

        self.qs_value.setText(value_new)

        # -------------

        qs_parent = self.qs_value.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_lineedit_str -- lineedit_update -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_lineedit_str -- lineedit_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_lineedit_str -- lineedit_update -- not isinstance(parent_name, str)")
            return

        # -------------
        number_current = self.ui.num_attrib.text()

        if number_current == "207" and isinstance(self.qs_desc, Info):

            self.qs_desc.setText(value_new)

            if isinstance(qs_parent, Material):
                self.link_desc_changed_signal.emit(self.code_title.text(), value_new)

            # -------------

            guid_desc = self.qs_desc.data(user_guid)

            if not isinstance(guid_desc, str):
                print("attribute_lineedit_str -- lineedit_update -- not isinstance(guid_desc, str)")
                return

        else:

            guid_desc = None

        # -------------

        value_dict = {number_current: [value_current, value_new]}

        # -------------

        data = AttributeModifyData(number_current=number_current, value_new=value_current, guid_desc=guid_desc)

        attribute_data = [data]

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict)

    @staticmethod
    def a___________________formatting______():
        pass

    def formatting_show(self):

        self.formatting_widget.formatting_show(current_parent=self.ui.formatting_bt,
                                               current_code=self.code_title.text(),
                                               current_text=self.ui.value_attrib.toPlainText())

    def formatting_changed(self, new_text: str):

        self.ui.value_attrib.setPlainText(new_text)
        self.lineedit_update()

    @staticmethod
    def a___________________event______():
        pass

    def resizeEvent(self, event):

        super().resizeEvent(event)

        if not self.isVisible():
            return

        if not self.adjust_height_action:
            self.adjust_height()

    def eventFilter(self, obj: QWidget, event: QEvent):

        if not self.isVisible():
            return super().eventFilter(obj, event)

        if event.type() == QEvent.MouseButtonDblClick and obj == self.ui.type_attrib:
            self.ui.value_attrib.setPlainText(self.code_title.text())
            self.ui.value_attrib.setFocus()

            self.lineedit_update()

            return super().eventFilter(obj, event)

        if obj != self.ui.value_attrib:
            return super().eventFilter(obj, event)

        if event.type() == event.KeyPress:

            event: event.KeyPress

            if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right,
                               Qt.Key_Up, Qt.Key_Down, Qt.Key_Home, Qt.Key_End):
                return super().eventFilter(obj, event)

            current_text = self.ui.value_attrib.toPlainText()
            current_text_count = len(current_text)

            if self.max_value is not None:

                if current_text_count > self.max_value:
                    event.ignore()
                    return True

            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                event.ignore()
                return True

        if event.type() == QEvent.FocusOut:
            self.lineedit_update()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
