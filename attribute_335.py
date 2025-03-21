#!/usr/bin/python3
# -*- coding: utf-8 -*
import os.path

from allplan_manage import AllplanDatas, AllplanPaths, AttributeDatas
from hierarchy import MyQstandardItem
from history_manage import AttributeModifyData
from main_datas import *
from tools import MyContextMenu, set_appareance_button, find_global_point
from tools import afficher_message as msg
from tools import get_lastest_used, get_most_used, move_widget_ss_bouton, browser_file
from ui_attribute_335 import Ui_Attribute335


class Attribute335(QWidget):
    attribute_changed_signal = pyqtSignal(str, list, str, dict)

    def __init__(self, asc, qs_value: MyQstandardItem, attribute_obj: AttributeDatas):
        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_Attribute335()
        self.ui.setupUi(self)

        set_appareance_button(widget=self.ui.browser_bt)
        set_appareance_button(widget=self.ui.preview_bt)

        # ----------------------------------

        if isinstance(attribute_obj, AttributeDatas):
            self.ui.num_attrib.setText(attribute_obj.number)

            self.ui.name_attrib.setText(attribute_obj.name)
            self.ui.name_attrib.setToolTip(attribute_obj.tooltips)

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------
        self.asc = asc
        self.allplan: AllplanDatas = self.asc.allplan

        if self.allplan.allplan_paths is None:
            self.design_std_path = ""
        else:
            self.design_std_path = f"{self.allplan.allplan_paths.std_path}Design\\"

        self.design_prj_path = f"{self.allplan.catalog_user_path}design\\"

        self.qs_value = qs_value
        self.ui.value_attrib.setText(self.qs_value.text())

        self.allplan.surface_list.sort(key=locale.strxfrm)

        # -----------------------------------------------
        # Completer
        # -----------------------------------------------

        lineedit_qcompleter = QCompleter(self.allplan.surface_list)
        lineedit_qcompleter.setFilterMode(Qt.MatchContains)
        lineedit_qcompleter.setCaseSensitivity(Qt.CaseInsensitive)
        lineedit_qcompleter.setModelSorting(QCompleter.CaseInsensitivelySortedModel)

        self.ui.value_attrib.setCompleter(lineedit_qcompleter)

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.value_attrib.textChanged.connect(self.surface_path_changed)
        self.ui.value_attrib.editingFinished.connect(self.surface_path_editing_finished)

        self.ui.value_attrib.installEventFilter(self)

        self.ui.browser_bt.clicked.connect(self.surface_menu_show)
        self.ui.browser_bt.customContextMenuRequested.connect(self.surface_menu_show)

        self.ui.preview_bt.clicked.connect(self.preview_show)

        # -----------------------------------------------
        # Loading
        # -----------------------------------------------

        self.surface_load_picture()

        # -----------------------------------------------

    @staticmethod
    def a___________________surface_path_changed______():
        pass

    def surface_path_changed(self):
        self.verification_surface_path(surface_path=self.ui.value_attrib.text(), msg_show=False)

    def surface_path_editing_finished(self):
        self.surface_set_new_path(surface_path=self.ui.value_attrib.text())

    def surface_set_new_path(self, surface_path: str):

        surface_path = self.surface_path_convert(surface_path=surface_path)

        self.verification_surface_path(surface_path=surface_path, msg_show=True)

        self.ui.value_attrib.setText(surface_path)
        self.surface_load_picture()
        self.surface_update()

        if surface_path not in self.allplan.surface_list:
            self.allplan.surface_list.append(surface_path)

        if surface_path not in self.allplan.recent_icons_list:
            self.allplan.recent_icons_list.append(surface_path)

        self.allplan.surface_all_list.append(surface_path)

    def surface_update(self):

        value_current = self.qs_value.text()
        value_new = self.ui.value_attrib.text()

        if value_current == value_new:
            return

        self.qs_value.setText(value_new)

        # -------------

        number_current = self.ui.num_attrib.text()

        value_dict = {number_current: [value_current, value_new]}

        # -------------

        qs_parent = self.qs_value.parent()

        if not isinstance(qs_parent, QStandardItem):
            print("attribute_335 -- surface_update -- not isinstance(qs_parent, QStandardItem)")
            return

        # -------------

        guid_parent = qs_parent.data(user_guid)

        if not isinstance(guid_parent, str):
            print("attribute_335 -- surface_update -- not isinstance(guid_parent, str)")
            return

        # -------------

        parent_name = qs_parent.text()

        if not isinstance(parent_name, str):
            print("attribute_335 -- surface_update -- not isinstance(parent_name, str)")
            return

        # -------------

        data = AttributeModifyData(number_current=number_current, value_new=value_current)

        attribute_data = [data]

        self.attribute_changed_signal.emit(guid_parent, attribute_data, parent_name, value_dict)

    @staticmethod
    def a___________________verification______():
        pass

    def verification_surface_path(self, surface_path: str, msg_show=False) -> bool:

        if surface_path == "":
            return self.verification_define_appareance(is_ok=True, msg_show=msg_show)

        if not surface_path.endswith(".surf"):
            return self.verification_define_appareance(is_ok=False, msg_show=msg_show)

        surface_path = surface_path.replace("\\\\", "\\")

        if os.path.exists(surface_path):
            return self.verification_define_appareance(is_ok=True, msg_show=msg_show)

        chemin_tps = f"{self.design_prj_path}{surface_path}"

        if os.path.exists(chemin_tps):
            return self.verification_define_appareance(is_ok=True, msg_show=msg_show)

        chemin_tps = f"{self.design_std_path}{surface_path}"

        if os.path.exists(chemin_tps):
            return self.verification_define_appareance(is_ok=True, msg_show=msg_show)

        return self.verification_define_appareance(is_ok=False, msg_show=msg_show)

    def verification_define_appareance(self, is_ok: bool, msg_show=False):

        self.ui.preview_bt.setVisible(is_ok)

        if is_ok:
            self.ui.value_attrib.setStyleSheet("QLineEdit{padding-left: 5px; "
                                               "border: 1px solid #8f8f91; "
                                               "border-right-width: 0px; "
                                               "border-top-left-radius:5px; "
                                               "border-bottom-left-radius: 5px; }")
            return True

        self.ui.value_attrib.setStyleSheet("QLineEdit{padding-left: 5px; "
                                           "border: 2px solid orange; "
                                           "border-top-left-radius:5px; "
                                           "border-bottom-left-radius: 5px; }")

        if msg_show:
            self.verification_show_msg()

        return False

    def verification_show_msg(self):

        msg(titre=application_title,
            message=self.tr("La texture choisie ne semble pas exister"),
            icone_avertissement=True,
            type_bouton=QMessageBox.Ok)

    @staticmethod
    def a___________________menu______():
        pass

    def surface_menu_show(self):

        self.asc.formula_widget_close()

        menu = MyContextMenu()  # No help

        point = find_global_point(self.ui.browser_bt)

        menu.add_title(title=self.tr("Choisir texture"))

        menu.add_action(qicon=get_icon(browser_icon),
                        title=self.tr("Parcourir texture"),
                        action=self.surface_browser)

        if len(self.allplan.surface_list) == 0:
            menu.exec_(point)
            return

        recent_list = get_lastest_used(current_list=self.allplan.recent_icons_list)
        recent_dict = dict()

        for surface_name in recent_list:

            surface_full_path = self.get_surface_path(surface_name)

            if surface_full_path == "":
                continue

            recent_dict[surface_name] = surface_full_path

        recent_count = len(recent_dict)

        most_used_list = get_most_used(current_list=self.allplan.surface_all_list)
        most_used_dict = dict()

        for surface_name in most_used_list:

            surface_full_path = self.get_surface_path(surface_name)

            if surface_full_path == "":
                continue

            most_used_dict[surface_name] = surface_full_path

        most_used_count = len(most_used_dict)

        if recent_count + most_used_count != 0:
            menu.addSeparator()

        if most_used_count != 0:

            most_used_menu = MyContextMenu(title=self.tr("Les plus utilisés"),
                                           qicon=get_icon(attribute_model_show_icon))

            menu.addMenu(most_used_menu)

            for surface_name, surface_full_path in most_used_dict.items():
                most_used_menu.add_action(qicon=QIcon((picture_loading(surface_path=surface_full_path))),
                                          title=surface_name,
                                          action=lambda val=surface_name: self.surface_set_new_path(surface_path=val))

        if recent_count != 0:

            recent_menu = MyContextMenu(title=self.tr("Les plus récents"),
                                        qicon=get_icon(recent_icon))

            menu.addMenu(recent_menu)

            for surface_name, surface_full_path in recent_dict.items():
                recent_menu.add_action(qicon=QIcon((picture_loading(surface_path=surface_full_path))),
                                       title=surface_name,
                                       action=lambda val=surface_name: self.surface_set_new_path(surface_path=val))

        menu.exec_(point)

    @staticmethod
    def a___________________browser______():
        pass

    def surface_browser(self):

        self.asc.formula_widget_close()

        surface_path_choose = self.design_prj_path
        filename = ""

        if self.ui.value_attrib.text() != "":

            surface_path_current = self.ui.value_attrib.text().replace("\\\\", "\\")
            surface_folder = os.path.dirname(surface_path_current)

            filename = os.path.basename(surface_path_current)

            full_path_prj = self.design_prj_path + surface_folder

            if not full_path_prj.endswith("\\"):
                full_path_prj = self.design_prj_path + surface_folder + "\\"

            full_path_std = self.design_std_path + surface_folder

            if not full_path_std.endswith("\\"):
                full_path_std = self.design_std_path + surface_folder + "\\"

            if os.path.exists(full_path_prj):
                surface_path_choose = full_path_prj

            elif os.path.exists(full_path_std):
                surface_path_choose = full_path_std

        file_txt = self.tr("Fichier")

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            shortcuts_list = [self.allplan.allplan_paths.std_design_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.tmp_path]

            if self.allplan.catalog_user_path != self.allplan.allplan_paths.std_design_path:

                design = f"{self.allplan.catalog_user_path}Design\\"

                if os.path.exists(design):
                    shortcuts_list.append(design)

        else:

            shortcuts_list = list()

        file_path = browser_file(parent=self,
                                 title=application_title,
                                 registry=[attribute_setting_file, "path_surface"],
                                 shortcuts_list=shortcuts_list,
                                 datas_filters={f"{file_txt} SURF": [".surf"]},
                                 current_path=surface_path_choose,
                                 default_path="",
                                 file_name=filename,
                                 use_setting_first=False)

        if file_path == "":
            return

        self.surface_set_new_path(surface_path=file_path)

    def surface_path_convert(self, surface_path: str) -> str:

        surface_path = surface_path.replace("/", "\\")

        surface_path_lower = surface_path.lower()

        if surface_path_lower.startswith(self.design_prj_path.lower()):
            surface_path = surface_path[len(self.design_prj_path):]

        elif surface_path_lower.startswith(self.design_std_path.lower()):
            surface_path = surface_path[len(self.design_std_path):]

        surface_path = surface_path.replace("\\\\", "\\")

        surface_path = surface_path.replace("\\", "\\\\")

        return surface_path

    def get_current_surface_path(self) -> str:
        return self.get_surface_path(surface_path=self.ui.value_attrib.text())

    def get_surface_path(self, surface_path: str) -> str:

        surface_path = surface_path.replace("\\\\", "\\")

        prj_path = f"{self.design_prj_path}{surface_path}"
        std_path = f"{self.design_std_path}{surface_path}"

        if surface_path == "":
            return ""

        if not surface_path.endswith(".surf"):
            return ""

        if os.path.exists(surface_path):
            return surface_path

        if os.path.exists(prj_path):
            return prj_path

        if os.path.exists(std_path):
            return std_path

        return ""

    def surface_load_picture(self):

        surface_path = self.get_current_surface_path()

        self.verification_surface_path(surface_path=self.ui.value_attrib.text(), msg_show=False)

        if surface_path == "":
            return

        self.ui.preview_bt.setIcon(QIcon(picture_loading(surface_path=surface_path)))

    def preview_show(self):

        self.asc.formula_widget_close()

        surface_path = self.get_current_surface_path()

        if surface_path == "":
            return

        widget_popup = WidgetApercu(parent_actuel=self, chemin=surface_path)

        widget_popup.show()

        move_widget_ss_bouton(button=self.ui.preview_bt, widget=widget_popup)

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj != self.ui.value_attrib:
            return super().eventFilter(obj, event)

        if event.type() == QEvent.MouseButtonDblClick:
            self.surface_browser()
            return super().eventFilter(obj, event)

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass


class WidgetApercu(QWidget):

    def __init__(self, parent_actuel, chemin):
        super().__init__(parent=parent_actuel)

        self.setWindowFlags(Qt.Popup)

        self.setGeometry(100, 100, 150, 150)

        label = QLabel()
        pixmap = picture_loading(chemin)
        pixmap = pixmap.scaled(150, 150)
        label.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def applymask(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    @staticmethod
    def a___________________event______():
        pass

    def resizeEvent(self, event: QResizeEvent):
        self.applymask()
        super().resizeEvent(event)

    def showEvent(self, event: QShowEvent):
        self.applymask()
        super().showEvent(event)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(QPen(QColor(178, 178, 178), 2))
        painter.setBrush(QBrush(QColor(248, 248, 248)))

        painter.drawRoundedRect(self.rect(), 10, 10)

        super().paintEvent(event)

    @staticmethod
    def a___________________end______():
        pass


def picture_loading(surface_path: str) -> QPixmap:
    if surface_path == "":
        return QPixmap()

    try:
        image = QImage(surface_path, "TIFF")

        image = image.convertToFormat(QImage.Format_RGBA8888)
        qpixmap = QPixmap.fromImage(image)

        return qpixmap

    except Exception:
        return QPixmap()
