import io
import os
import traceback

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QMessageBox, QPushButton, QHBoxLayout, QTextEdit, QLabel, QLineEdit, QVBoxLayout, QDialog, \
    QTableWidgetItem, QListWidgetItem, QListWidget, QRadioButton, QTableWidget, QWidget, QHeaderView, QMenu, QAction, \
    QFileDialog, QSizePolicy, QCheckBox

import MHWData
from ManagerCore import ManagerCore, ppInfoDecode, ppInfoEncode
from Utils import getConfigGeo, setConfigGeo


class InputDialog(QDialog):
    def __init__(self, title, details=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.initUI(title, details)
        self.text = None

    def initUI(self, title, details=None):
        layout = QVBoxLayout()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(title)
        layout.addWidget(self.edit)
        if details:
            layout.addWidget(QLabel(details))
        button_layout = QHBoxLayout()
        confirm_button = QPushButton("确认")
        confirm_button.clicked.connect(self.confirm)
        button_layout.addStretch()
        button_layout.addWidget(confirm_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def confirm(self):
        text = self.edit.text()
        if text:
            self.text = text
            self.accept()
        else:
            QMessageBox.warning(self, "错误", "名称不能为空")


def mergeTableCells(table):
    table.clearSpans()
    rows = table.rowCount()
    cols = table.columnCount()

    for col in range(cols):
        start_row = 0
        for row in range(1, rows):
            current_item = table.item(row, col)
            previous_item = table.item(start_row, col)

            if current_item.text() == previous_item.text() != "":
                continue  # 如果值相同，继续合并
            else:
                if start_row != row - 1:
                    table.setSpan(start_row, col, row - start_row, 1)
                start_row = row

        # 检查最后一组单元格是否需要合并
        if start_row != rows - 1:
            table.setSpan(start_row, col, rows - start_row, 1)


class SelectorDialog(QDialog):
    def __init__(self, selection_terms, core: ManagerCore = None, title="选择", after_selection=None):
        super().__init__()
        self.setWindowTitle(title)
        self.selection_terms = selection_terms
        self.selection_widgets = []
        self.selected_list = None
        self.after_selection = after_selection
        self.initUI()
        if core is not None:
            self.core = core
            g = getConfigGeo(core, "ui", "selector", "geo")
            if g:
                self.setGeometry(g)

    def closeEvent(self, a0):
        setConfigGeo(self.core, self.geometry(), "ui", "selector", "geo")
        super().closeEvent(a0)

    @staticmethod
    def addToList(list_widget, key, value):
        itm = QListWidgetItem(value)
        itm.setData(Qt.UserRole, key)
        list_widget.addItem(itm)

    @staticmethod
    def filter_list(text, qlist):
        for i in range(qlist.count()):
            item = qlist.item(i)
            if text in item.text():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def addSelectList(self, items, layout):
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("搜索")
        list_widget = QListWidget(self)
        search_bar.textChanged.connect(lambda text, lst=list_widget: SelectorDialog.filter_list(text, list_widget))
        for k, v in items:
            SelectorDialog.addToList(list_widget, k, v)
        if items:
            list_widget.setCurrentRow(0)

        layout.addWidget(search_bar)
        layout.addWidget(list_widget)

        self.selection_widgets.append(list_widget)

    def addSelectRadio(self, items, layout):
        radio_layout = QHBoxLayout()
        radio_list = []
        for _, name in items:
            radio = QRadioButton(name, self)
            radio_list.append(radio)
            radio_layout.addWidget(radio)
        radio_list[0].setChecked(True)
        layout.addLayout(radio_layout)
        self.selection_widgets.append(radio_list)

    def initUI(self):
        layout = QVBoxLayout()
        for name, tp, items in self.selection_terms:
            lab = QLabel(name)
            layout.addWidget(lab)
            if tp == "list":
                self.addSelectList(items, layout)
            elif tp == "radio":
                self.addSelectRadio(items, layout)

        button_layout = QHBoxLayout()
        select_button = QPushButton("确认", self)
        # noinspection PyUnresolvedReferences
        select_button.clicked.connect(self.get_select)
        button_layout.addWidget(select_button)

        cancel_button = QPushButton("取消", self)
        # noinspection PyUnresolvedReferences
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_select(self):
        selected_list = []
        for (name, tp, items), w in zip(self.selection_terms, self.selection_widgets):
            if tp == "list":
                selected_list.append(w.currentItem().data(Qt.UserRole))
            elif tp == "radio":
                for i, radio in enumerate(w):
                    if radio.isChecked():
                        selected_list.append(items[i][0])
                        break
        self.selected_list = selected_list
        if self.after_selection is not None:
            self.after_selection(selected_list)
        self.accept()


class SelectorDetailedListDialog(QDialog):

    def __init__(self, item_list, title="选择"):
        super().__init__()
        self.button_delete = None
        self.setWindowTitle(title)
        self.list: QListWidget = None
        self.item_list = item_list
        self.selected = None
        self.new_list = [k for k, _, _ in item_list]
        self.initUI()
        self.initList()

    def initUI(self):
        layout = QVBoxLayout()

        h_layout = QHBoxLayout()

        list_layout = QVBoxLayout()
        if len(self.item_list) == 0:
            list_layout.addWidget(QLabel("(请在模组的详情/编辑界面设置预设套装)"))
        else:
            list_layout.addWidget(QLabel("预设套装"))
        list_widget = QListWidget(self)
        self.list = list_widget
        list_widget.itemClicked.connect(self.show_details)
        list_layout.addWidget(list_widget)
        h_layout.addLayout(list_layout)

        detail_layout = QVBoxLayout()
        detail_layout.addWidget(QLabel("详情"))
        detail_widget = QTextEdit(self)
        detail_widget.setReadOnly(True)
        detail_layout.addWidget(detail_widget)
        button_delete = QPushButton("删除选中", self)
        button_delete.setEnabled(False)
        button_delete.clicked.connect(self.delete_item)
        self.button_delete = button_delete
        detail_layout.addWidget(button_delete)

        h_layout.addLayout(detail_layout)

        layout.addLayout(h_layout)

        button_layout = QHBoxLayout()
        select_button = QPushButton("确认", self)
        select_button.clicked.connect(self.get_select)
        button_layout.addWidget(select_button)
        # set the focus to the select button

        cancel_button = QPushButton("取消", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.detail_widget = detail_widget
        select_button.setFocus()

    def initList(self):
        for k, v, d in self.item_list:
            item = QListWidgetItem(v)
            item.setData(Qt.UserRole, (k, d))
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.list.addItem(item)
        # show the details when an item is clicked
        # self.list.itemClicked.connect(self.show_details)

    def show_details(self, item):
        k, d = item.data(Qt.UserRole)
        self.detail_widget.setText(d)
        self.button_delete.setEnabled(True)

    def delete_item(self):
        if self.list.currentItem() is None:
            return
        self.list.takeItem(self.list.currentRow())
        self.new_list.pop(self.list.currentRow())
        self.button_delete.setEnabled(False)

    def get_select(self):
        if self.list.currentItem() is None:
            return
        k, d = self.list.currentItem().data(Qt.UserRole)
        self.selected = k
        new_list = []
        for i in range(self.list.count()):
            item = self.list.item(i)
            t = item.data(Qt.UserRole)[0]
            t['name'] = item.text()
            new_list.append(t)
        self.new_list = new_list
        self.accept()




class LoadedModsDetailDialog(QWidget):
    def __init__(self, core: ManagerCore, parent=None):
        super().__init__(parent)
        self.core = core
        self.setWindowTitle("模组详情")
        self.resize(600, 400)

        self.initUI()
        g = getConfigGeo(core, "ui", "mod_detail", "geo")
        if g:
            self.setGeometry(g)

    def closeEvent(self, a0):
        setConfigGeo(self.core, self.geometry(), "ui", "mod_detail", "geo")
        super().closeEvent(a0)

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["模组名", "部位", "替换目标"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # set the second column to fit the content
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)
        self.setLayout(layout)
        try:
            self.populateTable()
        except:
            traceback.print_exc()
        mergeTableCells(self.table)
        self.table.setSortingEnabled(True)

        self.table.horizontalHeader().sortIndicatorChanged.connect(lambda _: mergeTableCells(self.table))

    def populateTable(self):
        loaded_mods = self.core.getModDict()
        table = self.table
        for mod_name, mod_info in loaded_mods.items():
            pl_info_dict = mod_info['pl_info']
            for s in pl_info_dict['source']:
                pp_info = ppInfoDecode(s)

                rep_info = pl_info_dict['rep'].get(s)
                row = table.rowCount()

                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(mod_name))
                table.setItem(row, 1, QTableWidgetItem(MHWData.部位ID_名称_map[pp_info[2]]))
                if rep_info is None:
                    rep_info = "无"
                else:
                    rep_info = self.core.formatPPInfo(ppInfoDecode(rep_info))
                table.setItem(row, 2, QTableWidgetItem(rep_info))


def buildPlSelectionDialog(core: ManagerCore, title="选择替换装备"):
    pl_table = [(k, f"{v}({k})") for k, v in MHWData.PL_MAPPING.items()]
    recent_pl = core.getRecentPl()
    pl_table_head = []
    for pre, adr in recent_pl:
        pl_table_head.append((adr, f"{MHWData.PL_MAPPING[adr]}({adr})"))
    pl_table = pl_table_head + pl_table

    term_gender = [("m", "男"), ("f", "女")]
    if len(recent_pl) > 0 and recent_pl[0][0] == "f":
        term_gender = list(reversed(term_gender))
    sel_terms = [("性别", "radio", term_gender), ("替换装备", "list", pl_table)]
    dialog = SelectorDialog(sel_terms, core, title, after_selection=lambda sel, c=core: c.addRecentPl(sel))
    return dialog


def buildPresetSelectionDialog(core: ManagerCore, title="选择预设"):
    presets = core.getPresetSuite()
    item_list = []
    for t in presets:
        name = t.get("name", "未命名")
        target_list = [ppInfoDecode(pp) for pp in t["target"]]
        detail_text = "\n".join([f"{MHWData.部位ID_名称_map[pp[2]]}：{core.formatPPInfo(pp)}" for pp in target_list])
        item_list.append((t, name, detail_text))
    dialog = SelectorDetailedListDialog(item_list, title)
    return dialog


class ModEditorWindow(QDialog):
    def __init__(self, mod_name: str, core: ManagerCore, parent=None):
        super().__init__(parent)
        self.table = None
        self.other_info_edit = None
        self.setWindowTitle("编辑模组")
        # self.resize(400, 400)

        self.name_edit = None
        self.mod_name = mod_name
        self.core = core

        self.initUI()
        self.create_context_menu()
        self.adjustSize()
        g = getConfigGeo(core, "ui", "mod_editor", "geo")
        if g:
            self.setGeometry(g)

    def closeEvent(self, a0):
        setConfigGeo(self.core, self.geometry(), "ui", "mod_editor", "geo")
        super().closeEvent(a0)

    def initUI(self):
        info = self.core.modGetInfo(self.mod_name)
        layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        # 模组名称
        name_label = QLabel("名称:")
        self.name_edit = QLineEdit(self.mod_name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["部位", "替换目标"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table = table
        self.populateTable()
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.adjustSize()

        layout.addWidget(table)

        layout_preset = QHBoxLayout()
        layout_preset.addStretch(2)
        load_preset_button = QPushButton("加载预设")
        load_preset_button.clicked.connect(self.load_preset)
        layout_preset.addWidget(load_preset_button)
        add_preset_button = QPushButton("保存为预设")
        add_preset_button.clicked.connect(self.add_preset)
        layout_preset.addWidget(add_preset_button)
        layout.addLayout(layout_preset)

        # create a setting

        # 模组安装日期
        date_label = QLabel(f"安装日期: {info.get('date', '')}")
        layout.addWidget(date_label)

        # 其他模组信息
        other_info_label = QLabel("备注:")
        layout.addWidget(other_info_label)
        other_info_edit = QTextEdit()
        other_info_edit.setPlaceholderText("请输入备注信息")
        other_info_edit.setText(info.get('comments', ''))
        # other_info_edit.adjustSize()
        other_info_edit.setFixedHeight(100)
        self.other_info_edit = other_info_edit
        layout.addWidget(other_info_edit)

        # 确认按钮
        button_layout = QHBoxLayout()
        confirm_button = QPushButton("确认")
        confirm_button.clicked.connect(self.confirm_edit)
        button_layout.addStretch()
        button_layout.addWidget(confirm_button)
        layout.addLayout(button_layout)

        layout.setStretch(1, 10)
        self.setLayout(layout)

    def populateTable(self):
        mod_info = self.core.modGetInfo(self.mod_name)
        pl_info_dict = mod_info['pl_info']
        table = self.table
        for src_pp_encoded in pl_info_dict['source']:
            src_pp_info = ppInfoDecode(src_pp_encoded)

            rep_pp_en = pl_info_dict['rep'].get(src_pp_encoded)
            row = table.rowCount()

            table.insertRow(row)
            item0 = QTableWidgetItem(MHWData.部位ID_名称_map[src_pp_info[2]])
            item0.setFlags(item0.flags() & ~Qt.ItemIsEditable)
            item0.setData(Qt.UserRole, src_pp_info)
            table.setItem(row, 0, item0)
            if rep_pp_en is None:
                rep_display = ""
                item = QTableWidgetItem(rep_display)
            else:
                rep_pp = ppInfoDecode(rep_pp_en)
                rep_display = self.core.formatPPInfo(ppInfoDecode(rep_pp_en))
                item = QTableWidgetItem(rep_display)
                item.setData(Qt.UserRole, rep_pp)
            table.setItem(row, 1, item)

        # resize the table

    def create_context_menu(self):
        table = self.table
        # add a context menu to the table
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_context_menu)

        self.context_menu = menu = QMenu(self)
        add_action = QAction("设置", self)
        add_action.triggered.connect(self.set_target)
        menu.addAction(add_action)
        clear_action = QAction("清空", self)
        clear_action.triggered.connect(self.clear_table)
        menu.addAction(clear_action)

        # set the double click event
        table.cellDoubleClicked.connect(self.set_target)

    def show_context_menu(self, pos: QPoint):
        self.context_menu.exec_(self.table.viewport().mapToGlobal(pos))

    def set_target_rep(self, selected_col, selected_rows):
        if len(selected_rows) == 1:
            row = next(iter(selected_rows))
            part = self.table.item(row, 0).data(Qt.UserRole)[2]
            table = [(k, f"{v}({k})") for k, v in MHWData.PP_MAPPING[part].items()]
            selection_items = [("性别", "radio", [("m", "男"), ("f", "女")]),
                               (f"替换{MHWData.部位ID_名称_map[part]}", "list", table)]
            dialog = SelectorDialog(selection_items, self.core, "选择替换装备")
        else:
            dialog = buildPlSelectionDialog(self.core)
        if dialog.exec_() != QDialog.Accepted:
            return
        sel_pre, sel_adr = dialog.selected_list
        for row in selected_rows:
            part_id = self.table.item(row, 0).data(Qt.UserRole)[2]
            pp_info = (sel_pre, sel_adr, part_id)
            text = self.core.formatPPInfo(pp_info)
            item = QTableWidgetItem(text)
            item.setData(Qt.UserRole, pp_info)
            # print(pp_info)
            self.table.setItem(row, selected_col, item)
        # mergeTableCells(self.table)

    def add_preset(self):
        try:
            core = self.core
            target = []
            for i in range(self.table.rowCount()):
                pp_info = self.table.item(i, 1).data(Qt.UserRole)
                if pp_info is not None:
                    target.append(pp_info)
            print(target)
            # a dialog to input the name
            detail_text = "\n".join([f"{MHWData.部位ID_名称_map[pp[2]]}：{core.formatPPInfo(pp)}" for pp in target])
            dialog = InputDialog("输入预设保存名称", details=detail_text)
            if dialog.exec_() != QDialog.Accepted:
                return
            name = dialog.text
            core.getPresetSuite().append({"name": name, "target": [ppInfoEncode(pp) for pp in target]})
        except Exception as e:
            traceback.print_exc()

    def load_preset(self):
        core = self.core
        dialog = buildPresetSelectionDialog(self.core)
        dialog.exec_()
        new_presets = dialog.new_list
        core.setPredefinedSuite(new_presets)
        sel = dialog.selected
        if sel is None:
            return
        pp_info_list = [ppInfoDecode(pp_text) for pp_text in sel["target"]]
        for part_id in range(5):
            for pp in pp_info_list:
                if pp[2] != part_id:
                    continue
                item = QTableWidgetItem(core.formatPPInfo(pp))
                item.setData(Qt.UserRole, pp)
                self.table.setItem(part_id, 1, item)
                break

    def set_target(self):
        table = self.table
        # get the selected column and row
        selected_items = table.selectedItems()
        if not selected_items:
            return
        selected_col = selected_items[0].column()
        if selected_col != 1:
            return
        # get the rows with the same column
        selected_rows = {item.row() for item in selected_items if item.column() == selected_col}
        self.set_target_rep(selected_col, selected_rows)

    def clear_table(self):
        sel = self.table.selectedItems()
        for item in sel:
            if item.column() != 1:
                continue
            item.setText("")
            item.setData(Qt.UserRole, None)

    def confirm_edit(self):
        # 获取用户编辑的模组名称
        edited_name = self.name_edit.text()
        info_text = io.StringIO()
        self.core.modRename(self.mod_name, edited_name, info_text)
        mod_info = self.core.modGetInfo(edited_name)
        pl_info_dict = mod_info['pl_info']
        rep_dict = pl_info_dict['rep']
        for r in range(self.table.rowCount()):
            src_pp_de = self.table.item(r, 0).data(Qt.UserRole)
            tar_pp_de = self.table.item(r, 1).data(Qt.UserRole)
            src_pp_en = ppInfoEncode(src_pp_de)
            if tar_pp_de is None:
                rep_dict.pop(src_pp_en, None)
                continue
            tar_pp_en = ppInfoEncode(tar_pp_de)
            rep_dict[src_pp_en] = tar_pp_en
        comments = self.other_info_edit.toPlainText()
        mod_info['comments'] = comments
        # QMessageBox.information(self, "编辑完成", info_text.getvalue())
        self.accept()


class ModMixerWindow(QWidget):
    def __init__(self, core: ManagerCore, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.name_edit = None
        self.core = core
        self.table: QTableWidget = None
        self.context_menu = None
        self.export_folder = None
        self.setWindowTitle("模组自定义导出")

        self.initUI()
        self.create_context_menu()

        g = getConfigGeo(core, "ui", "mod_mixer", "geo")
        if g:
            self.setGeometry(g)

    def closeEvent(self, a0):
        setConfigGeo(self.core, self.geometry(), "ui", "mod_mixer", "geo")
        super().closeEvent(a0)

    def initUI(self):
        main_layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        # 模组名称
        name_label = QLabel("名称:")
        import random
        self.name_edit = QLineEdit(f"自定义_{random.randint(1000, 9999)}")
        self.name_edit.textChanged.connect(self.name_edited)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        main_layout.addLayout(name_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["部位", "源模组", "替换目标"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # set the second column to fit the content
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table = self.table
        # make the table read only
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setRowCount(len(MHWData.部位ID_名称_map))
        # do not show the row number
        table.verticalHeader().setVisible(False)
        for i, v in MHWData.部位ID_名称_map.items():
            item = QTableWidgetItem(v)
            table.setItem(i, 0, item)
            table.setItem(i, 1, QTableWidgetItem(""))
            table.setItem(i, 2, QTableWidgetItem(""))

        main_layout.addWidget(self.table)
        layout_buttons = QHBoxLayout()
        # set them aligned to the right
        layout_buttons.addStretch()
        load_button = QPushButton("加载预设")
        load_button.clicked.connect(self.load_preset)
        layout_buttons.addWidget(load_button)
        add_button = QPushButton("保存为预设")
        add_button.clicked.connect(self.add_preset)
        layout_buttons.addWidget(add_button)
        main_layout.addLayout(layout_buttons)

        export_layout = QHBoxLayout()
        checkbox_export = QCheckBox("导出到:")
        checkbox_export.setChecked(True)
        self.checkbox_export = checkbox_export
        export_layout.addWidget(checkbox_export)
        self.export_folder = QLineEdit()
        self.export_folder.setReadOnly(True)
        self.export_folder.setText("out")
        export_layout.addWidget(self.export_folder)
        export_button = QPushButton("选择文件夹")
        export_button.clicked.connect(self.select_export_folder)
        export_layout.addWidget(export_button)
        checkbox_export.toggled.connect(lambda checked: self.export_folder.setEnabled(checked))
        main_layout.addLayout(export_layout)

        layout_rep = QHBoxLayout()
        # add a checkbox for saving
        checkbox_save = QCheckBox("添加到模组列表")
        checkbox_save.setChecked(True)
        self.checkbox_save = checkbox_save
        layout_rep.addWidget(checkbox_save)
        replace_button = QPushButton("导出")
        replace_button.clicked.connect(self.export)
        layout_rep.addWidget(replace_button)
        main_layout.addLayout(layout_rep)

        self.setLayout(main_layout)

    def create_context_menu(self):
        table = self.table
        # add a context menu to the table
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_context_menu)

        self.context_menu = menu = QMenu(self)
        add_action = QAction("设置", self)
        add_action.triggered.connect(self.set_target)
        menu.addAction(add_action)
        clear_action = QAction("清空", self)
        clear_action.triggered.connect(self.clear_table)
        menu.addAction(clear_action)

        # set the double click event
        table.cellDoubleClicked.connect(self.set_target)

    def show_context_menu(self, pos: QPoint):
        self.context_menu.exec_(self.table.viewport().mapToGlobal(pos))

    def name_edited(self):
        name = self.name_edit.text()
        pass

    def select_export_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择导出文件夹")
        if folder:
            self.export_folder.setText(folder)

    def set_target_mod(self, selected_col, selected_rows):
        table = [(mod_name, mod_name) for mod_name in self.core.getModDict().keys()]
        if len(selected_rows) == 1:
            part = next(iter(selected_rows))
            name = f"替换{MHWData.部位ID_名称_map[part]}"
            # for name, info in self.core.getModDict().items():
            #     sources = info['pl_info']['source']
            #     if len(sources) == 1:
            #         table.append((sources[0], name))
            #     else:
            #         tabl
        else:
            name = "替换装备"
        selection_items = [(name, "list", table)]
        dialog = SelectorDialog(selection_items, self.core, "选择源模组")
        if dialog.exec_() != QDialog.Accepted:
            return
        selection = dialog.selected_list
        mod_name = selection[0]
        for row in selected_rows:
            item = QTableWidgetItem(mod_name)
            self.table.setItem(row, selected_col, item)
        # mergeTableCells(self.table)

    def set_target_rep(self, selected_col, selected_rows):
        if len(selected_rows) == 1:
            part = next(iter(selected_rows))
            table = [(k, f"{v}({k})") for k, v in MHWData.PP_MAPPING[part].items()]
            selection_items = [("性别", "radio", [("m", "男"), ("f", "女")]),
                               (f"替换{MHWData.部位ID_名称_map[part]}", "list", table)]
            dialog = SelectorDialog(selection_items, self.core, "选择替换装备")
        else:
            dialog = buildPlSelectionDialog(self.core)
        if dialog.exec_() != QDialog.Accepted:
            return
        sel_pre, sel_adr = dialog.selected_list
        for row in selected_rows:
            pp_info = (sel_pre, sel_adr, row)
            text = self.core.formatPPInfo(pp_info)
            item = QTableWidgetItem(text)
            item.setData(Qt.UserRole, pp_info)
            self.table.setItem(row, selected_col, item)

        # mergeTableCells(self.table)

    def set_target(self):
        table = self.table
        # get the selected column and row
        selected_items = table.selectedItems()
        if not selected_items:
            return
        selected_col = selected_items[0].column()
        if selected_col not in (1, 2):
            return
        # get the rows with the same column
        selected_rows = {item.row() for item in selected_items if item.column() == selected_col}
        if selected_col == 1:
            self.set_target_mod(selected_col, selected_rows)
        else:
            self.set_target_rep(selected_col, selected_rows)

    def add_preset(self):
        try:
            core = self.core
            target = []
            for i in range(self.table.rowCount()):
                pp_info = self.table.item(i, 2).data(Qt.UserRole)
                if pp_info is not None:
                    target.append(pp_info)
            # print(target)
            # a dialog to input the name
            detail_text = "\n".join([f"{MHWData.部位ID_名称_map[pp[2]]}：{core.formatPPInfo(pp)}" for pp in target])
            dialog = InputDialog("输入预设保存名称", details=detail_text)
            if dialog.exec_() != QDialog.Accepted:
                return
            name = dialog.text
            core.getPresetSuite().append({"name": name, "target": [ppInfoEncode(pp) for pp in target]})
        except:
            traceback.print_exc()

    def load_preset(self):
        try:
            core = self.core
            dialog = buildPresetSelectionDialog(self.core)
            dialog.exec_()
            new_presets = dialog.new_list
            core.setPredefinedSuite(new_presets)
            sel = dialog.selected
            if sel is None:
                return
            pp_info_list = [ppInfoDecode(pp_text) for pp_text in sel["target"]]
            for part_id in range(5):
                for pp in pp_info_list:
                    if pp[2] != part_id:
                        continue
                    item = QTableWidgetItem(core.formatPPInfo(pp))
                    item.setData(Qt.UserRole, pp)
                    self.table.setItem(part_id, 2, item)
                    break
        except Exception as e:
            traceback.print_exc()
        pass

    def clear_table(self):
        sel = self.table.selectedItems()
        for item in sel:
            item.setText("")
            item.setData(Qt.UserRole, None)

    def export(self):
        export_file = self.checkbox_export.isChecked()
        save_mod = self.checkbox_save.isChecked()
        name = self.name_edit.text()
        if not name:
            QMessageBox.warning(self, "错误", "请先输入模组名称")
            return
        if save_mod and self.core.modExists(name):
            QMessageBox.warning(self, "错误", "模组名称已存在")
            return

        export_folder = self.export_folder.text()
        if export_file and not export_folder:
            QMessageBox.warning(self, "错误", "请先选择导出文件夹")
            return
        try:
            export_filename = os.path.join(export_folder, f"{name}.zip")
            mixture_info = []
            for r in range(self.table.rowCount()):
                mod_name = self.table.item(r, 1).text()
                rep_info = self.table.item(r, 2).data(Qt.UserRole)
                if len(mod_name) > 0 and rep_info is not None:
                    mixture_info.append((mod_name, rep_info))
            self.core.modMixtureExport(mixture_info, name, save=save_mod, export_file=export_filename)
            QMessageBox.information(self, "导出", f"模组已导出")
            if self.main_window:
                self.main_window.refreshModList()
        except Exception as e:
            QMessageBox.critical(self, "错误", "导出失败！\n" + traceback.format_exc())
