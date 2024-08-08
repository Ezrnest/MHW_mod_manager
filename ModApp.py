import io
import os.path
import random
import sys
import time
import traceback

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QCheckBox, QHeaderView, QMessageBox, QToolBar,
                             QAction, QFileDialog, QDialog, QLineEdit, QListWidget, QPushButton,
                             QHBoxLayout, QProgressBar, QProgressDialog, QMenu, QListWidgetItem, QRadioButton, QLabel,
                             QTextEdit, QSizePolicy, QMenuBar)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint

import MHWData
from QialogWindows import SelectorDialog, InputDialog, SelectorDetailedListDialog, LoadedModsDetailDialog, \
    ModEditorWindow, CheckboxTableWidgetItem, buildPlSelectionDialog, ModMixerWindow, buildPresetSelectionDialog
from ModManagerCore import ManagerCore, 部位ID_路径_map, 部位ID_名称_map, ppInfoDecode, ppInfoEncode

# noinspection PyUnresolvedReferences
import resources_rc


class ModManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = None
        self.search_bar = None
        self.context_menu = None
        self.setWindowTitle("MHW 外观模组工具 by mart.")
        self.window_mod_mixer = None
        self.window_loaded_mods_detail = None
        self.resize(600, 600)

        self.core = ManagerCore()

        self.initUI()

    def closeEvent(self, a0):
        self.core.save_config()
        super().closeEvent(a0)

    def initUI(self):
        self.create_toolbar()
        self.create_mod_table()
        self.create_context_menu()

    def create_toolbar(self):
        menuBar = self.menuBar()
        # self.ad(toolbar)

        menu_setting = QMenu("设置", self)
        menuBar.addMenu(menu_setting)
        action_set_game_root = QAction("设置游戏路径", self)
        action_set_game_root.triggered.connect(self.set_game_path)
        menu_setting.addAction(action_set_game_root)

        # create a menu
        menu_mod = QMenu("模组导入", self)
        add_mod_action = QAction("添加模组zip", self)
        add_mod_action.triggered.connect(self.add_mod)
        menu_mod.addAction(add_mod_action)

        action_add_mod_folder = QAction("扫描狩技盒子文件夹", self)
        action_add_mod_folder.triggered.connect(self.scan_mod_folder)
        menu_mod.addAction(action_add_mod_folder)

        menu_mod.addSeparator()

        action_detail = QAction("已加载模组详情", self)
        action_detail.triggered.connect(self.show_loaded_mods_detail)
        menu_mod.addAction(action_detail)

        del_mod_action = QAction("删除选中的模组", self)
        del_mod_action.triggered.connect(self.delete_mod)
        menu_mod.addAction(del_mod_action)

        menuBar.addMenu(menu_mod)

        menu_export = QMenu("模组导出", self)
        menuBar.addMenu(menu_export)

        action_export = QAction("导出选中的模组", self)
        action_export.triggered.connect(self.export_mod)
        menu_export.addAction(action_export)

        action_mix = QAction("模组混合", self)
        action_mix.triggered.connect(self.show_mod_mixer)
        menu_export.addAction(action_mix)

        action_refresh = QAction("刷新列表", self)
        action_refresh.triggered.connect(self.refreshModList)
        menuBar.addAction(action_refresh)

        # action_test = QAction("测试", self)
        # action_test.triggered.connect(self.show_test_window)
        # toolbar.addAction(action_test)

    def show_test_window(self):
        try:
            dialog = SelectorDetailedListDialog([("k", "测试", "详情信息\n详情信息\n详情信息")])
            dialog.exec_()
        except Exception as e:
            traceback.print_exc()

    def create_mod_table(self):

        table = QTableWidget()
        self.table = table
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["加载", "模组名", "替换装备", "备注", ])
        table.setColumnWidth(0, 50)
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        header = table.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        # set the context menu
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_context_menu)

        # set sorting counter
        table.setSortingEnabled(True)
        table.itemChanged.connect(self.mod_list_item_modified)
        table.cellDoubleClicked.connect(self.mod_table_double_clicked)

        # Create a search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("筛选模组名称")
        self.search_bar.textChanged.connect(self.filter_mod_list)

        # main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.table)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # refresh the mod list
        self.refreshModList()
        table.resizeColumnToContents(1)
        self.table.setColumnWidth(0, 35)
        self.table.setColumnWidth(2, 200)
        table.sortByColumn(0, Qt.AscendingOrder)

    def refreshModList(self):
        try:

            man = self.core
            mods = self.core.getModDict()
            table = self.table
            # clear the table
            table.clearContents()
            table.setSortingEnabled(False)
            table.blockSignals(True)

            table.setRowCount(len(mods))
            for i, en in enumerate(mods.items()):
                name, mod = en
                replacements = mod["pl_info"]["rep"].values()
                from ModManagerCore import ppInfoDecode
                replacements = [ppInfoDecode(text) for text in replacements]
                if len(set([(x[0], x[1]) for x in replacements])) == 1:
                    pl_info_text = man.formatPlInfo(replacements[0][:2], details=False)
                else:
                    pl_info_text = " ".join([man.formatPPInfo(pp, details=False) for pp in replacements])

                checkbox = QCheckBox()
                checkbox.setChecked(mod.get("loaded", False))
                checkbox.toggled.connect(
                    lambda state, box=checkbox, mod_name=name: self.toggle_mod(mod_name, box, state))
                table.setCellWidget(i, 0, checkbox)
                table.cellWidget(i, 0).setStyleSheet("margin-left:10")

                self.table.setItem(i, 0, CheckboxTableWidgetItem(checkbox))
                it1 = QTableWidgetItem(name)
                it1.setData(Qt.UserRole, name)
                self.table.setItem(i, 1, it1)
                it = QTableWidgetItem(pl_info_text)
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(i, 2, it)
                self.table.setItem(i, 3, QTableWidgetItem(mod.get("comments", "")))
            table.setSortingEnabled(True)
            table.blockSignals(False)
            self.filter_mod_list()
        except Exception as e:
            QMessageBox.information(self, "刷新模组列表", traceback.format_exc())

    def filter_mod_list(self):
        search_text = self.search_bar.text().lower()

        for row in range(self.table.rowCount()):
            mod_name = self.table.item(row, 1).text().lower()
            mod_comment = self.table.item(row, 3).text().lower()

            if search_text in mod_name or search_text in mod_comment:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def mod_list_item_modified(self, item):
        row, col = item.row(), item.column()
        if col == 1:
            name = item.text()
            if name == item.data(Qt.UserRole):
                return
            if self.core.modExists(name):
                QMessageBox.information(self, "模组名", "模组名冲突")
                item.setText(item.data(Qt.UserRole))
                return
            else:
                self.core.modRename(item.data(Qt.UserRole), name)
                item.setData(Qt.UserRole, name)
        elif col == 3:
            mod_name = self.table.item(row, 1).text()
            comments = item.text()
            self.core.modGetInfo(mod_name)["comments"] = comments

    def mod_table_double_clicked(self,row,col):
        if col != 2:
            return
        self.set_target_selected_mods()

    def add_mod(self):
        # allow user to select multiple files, zip, 7z,rar
        mod_files, _ = QFileDialog.getOpenFileNames(self, "选择模组压缩文件（可多选）", "", "Zip Files (*.zip *.7z)")
        if not mod_files:
            return
        # 做一个progress bar
        progress_dialog = QProgressDialog("加载中...", "取消", 0, len(mod_files), self)
        progress_dialog.setWindowTitle("加载模组")
        progress_dialog.setMinimumDuration(0)
        progress_dialog.resize(300, 100)
        # progress_dialog.setGeometry(300, 300, 400, 100)
        progress_dialog.setWindowModality(Qt.WindowModal)

        print(mod_files)
        info_io = io.StringIO()
        for i, mod_file in enumerate(mod_files):
            progress_dialog.setValue(i)
            progress_dialog.setLabelText(f"正在加载：{mod_file}")
            if progress_dialog.wasCanceled():
                break
            try:
                self.core.modAddFromFile(mod_file, replace=False, output_io=info_io)
            except Exception as e:
                traceback.print_exc(file=info_io)

        progress_dialog.setValue(len(mod_files))
        QMessageBox.information(self, "加载情况", info_io.getvalue())
        self.refreshModList()

    def scan_mod_folder(self):
        # get a folder path
        root_folder = QFileDialog.getExistingDirectory(self, "选择狩技盒子文件夹")
        if not root_folder:
            return
        from ModManagerCore import find_mods_from_shouji
        mod_infos = find_mods_from_shouji(root_folder)
        text = f"找到{len(mod_infos)}个模组：\n"
        for name, folder in mod_infos:
            text += f"{name}, "
        text += "\n是否加载？"
        dialog = QMessageBox(QMessageBox.Question, "扫描结果", text, QMessageBox.Yes | QMessageBox.No)
        if dialog.exec_() != QMessageBox.Yes:
            return

        # 做一个progress bar
        progress_dialog = QProgressDialog("Loading mod...", "Cancel", 0, len(mod_infos), self)
        progress_dialog.setWindowTitle("Loading Mod")
        progress_dialog.setMinimumDuration(0)
        progress_dialog.resize(200, 100)
        # progress_dialog.setGeometry(300, 300, 400, 100)
        progress_dialog.setWindowModality(Qt.WindowModal)

        info_io = io.StringIO()
        for i, (name, folder) in enumerate(mod_infos):
            progress_dialog.setValue(i)
            progress_dialog.setLabelText(f"正在加载：{name}")
            if progress_dialog.wasCanceled():
                break
            try:
                self.core.modAddFromFile(folder, name, output_io=info_io)
            except Exception as e:
                traceback.print_exc(file=info_io)

        progress_dialog.setValue(len(mod_infos))
        QMessageBox.information(self, "加载情况", info_io.getvalue())
        self.refreshModList()

    def delete_mod(self):
        mod_names = self.get_selected_mod_names()
        if not mod_names:
            QMessageBox.information(self, "导出模组", "请选中需要删除的模组")
            return
        name_list = "\n".join(mod_names)
        confirm = QMessageBox.question(self, "删除模组", f"确认删除选中的模组？\n{name_list}",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.No:
            return
        info_io = io.StringIO()
        for mod_name in mod_names:
            self.core.modDelete(mod_name, output_io=info_io)
        QMessageBox.information(self, "删除模组", info_io.getvalue())
        self.refreshModList()

    def export_mod(self):
        mod_names = self.get_selected_mod_names()
        if not mod_names:
            QMessageBox.information(self, "导出模组", "请选中要导出的模组")
            return
        mod_path = QFileDialog.getExistingDirectory(self, "选择导出文件夹(将覆盖已有文件)")
        if not mod_path:
            return
        info_io = io.StringIO()

        progress_dialog = QProgressDialog("导出模组...", "取消", 0, len(mod_names), self)
        progress_dialog.setWindowTitle("导出模组")
        progress_dialog.setWindowModality(Qt.WindowModal)

        for i, mod_name in enumerate(mod_names):
            progress_dialog.setValue(i)
            progress_dialog.setLabelText(f"导出中：{mod_name}")
            if progress_dialog.wasCanceled():
                break
            try:
                self.core.modExport(mod_name, mod_path, output_io=info_io)
            except Exception as e:
                traceback.print_exc(file=info_io)
            print("", file=info_io)

        progress_dialog.setValue(len(mod_names))
        QMessageBox.information(self, "导出模组", info_io.getvalue())

    def show_loaded_mods_detail(self):
        if self.window_loaded_mods_detail is None:
            self.window_loaded_mods_detail = LoadedModsDetailDialog(self.core)
        self.window_loaded_mods_detail.show()

    def show_mod_mixer(self):
        try:
            if self.window_mod_mixer is None:
                self.window_mod_mixer = ModMixerWindow(self.core, main_window=self)
            self.window_mod_mixer.show()
        except Exception as e:
            traceback.print_exc()

    def edit_mod(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "编辑模组", "请选中要编辑的模组")
            return
        row = selected_items[0].row()
        mod_name = self.table.item(row, 1).text()
        dialog = ModEditorWindow(mod_name, self.core)
        if dialog.exec_() == QDialog.Accepted:
            self.refreshModList()
            self.reload_selected_mods([mod_name])
        return


    def set_game_path(self):
        game_path = QFileDialog.getExistingDirectory(self, "选择游戏根目录",directory=self.core.config.get("game_root"))
        if game_path:
            try:
                if self.core.is_game_root_valid(game_path):
                    self.core.set_game_root(game_path)
                    QMessageBox.information(self, "提示", "游戏路径设置成功")
                else:
                    QMessageBox.information(self, "提示", "游戏路径不正确，请重新选择")
            except Exception as e:
                traceback.print_exc()

    def toggle_mod(self, name, box, state):
        if state == self.core.modIsLoaded(name):
            return
        output = io.StringIO()
        try:
            if state:
                self.core.modLoad(name, output_io=output)
                # cancel the loading if the mod is not loaded
            else:
                self.core.modUnload(name, output_io=output)
        except Exception as e:
            traceback.print_exc(file=output)
        QMessageBox.information(self, "模组", output.getvalue())
        box.setChecked(self.core.modIsLoaded(name))

    def create_context_menu(self):
        self.context_menu = QMenu(self)
        load_action = QAction("加载", self)
        load_action.triggered.connect(self.load_selected_mods)
        self.context_menu.addAction(load_action)

        unload_action = QAction("卸载", self)
        unload_action.triggered.connect(self.unload_selected_mods)
        self.context_menu.addAction(unload_action)

        self.context_menu.addSeparator()

        set_target_action = QAction("设置替换", self)
        set_target_action.triggered.connect(self.set_target_selected_mods)
        self.context_menu.addAction(set_target_action)

        set_preset_action = QAction("预设替换", self)
        set_preset_action.triggered.connect(self.set_preset_selected_mods)
        self.context_menu.addAction(set_preset_action)

        edit_action = QAction("详情/编辑", self)
        edit_action.triggered.connect(self.edit_mod)
        self.context_menu.addAction(edit_action)

        # add a separator
        self.context_menu.addSeparator()

        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self.delete_mod)
        self.context_menu.addAction(delete_action)

        export_action = QAction("导出", self)
        export_action.triggered.connect(self.export_mod)
        self.context_menu.addAction(export_action)

    def show_context_menu(self, pos):
        self.context_menu.exec_(self.table.viewport().mapToGlobal(pos))

    def get_selected_mod_names(self):
        selected_items = self.table.selectedItems()
        selected_rows = {item.row() for item in selected_items}
        mod_names = [self.table.item(row, 1).text() for row in selected_rows]
        return mod_names

    def load_selected_mods(self):
        mod_names = self.get_selected_mod_names()

        progress_dialog = QProgressDialog("Loading mod...", "Cancel", 0, len(mod_names), self)
        progress_dialog.setWindowTitle("Loading Mod")
        progress_dialog.setMinimumDuration(2)
        progress_dialog.resize(400, 100)
        progress_dialog.setWindowModality(Qt.WindowModal)

        info_io = io.StringIO()
        for i, mod_name in enumerate(mod_names):
            progress_dialog.setValue(i)
            progress_dialog.setLabelText(f"加载中： {mod_name}")
            if progress_dialog.wasCanceled():
                break
            try:
                self.core.modLoad(mod_name, output_io=info_io)
            except Exception as e:
                traceback.print_exc(file=info_io)

        self.refreshModList()
        progress_dialog.setValue(len(mod_names))
        QMessageBox.information(self, "加载模组", info_io.getvalue())

    def unload_selected_mods(self):
        mod_names = self.get_selected_mod_names()

        info_io = io.StringIO()
        for mod_name in mod_names:
            self.core.modUnload(mod_name, output_io=info_io)

        self.refreshModList()
        QMessageBox.information(self, "卸载模组", info_io.getvalue())

    def reload_selected_mods(self, mod_names=None):

        if mod_names is None:
            mod_names = self.get_selected_mod_names()
        mod_names = [name for name in mod_names if self.core.modIsLoaded(name)]
        if not mod_names:
            return

        progress_dialog = QProgressDialog("Loading mod...", "Cancel", 0, len(mod_names), self)
        progress_dialog.setWindowTitle("Loading Mod")
        progress_dialog.setMinimumDuration(2)
        progress_dialog.resize(400, 100)
        progress_dialog.setWindowModality(Qt.WindowModal)

        info_io = io.StringIO()
        for i, mod_name in enumerate(mod_names):
            progress_dialog.setValue(i)
            progress_dialog.setLabelText(f"加载中： {mod_name}")
            if progress_dialog.wasCanceled():
                break
            if not self.core.modIsLoaded(mod_name):
                continue
            try:
                self.core.modUnload(mod_name, output_io=None)
                self.core.modLoad(mod_name, force_load=True, output_io=info_io)
                # info_io.write(f"<{mod_name}>已更新\n")
            except Exception as e:
                traceback.print_exc(file=info_io)
        progress_dialog.setValue(len(mod_names))

        self.refreshModList()
        QMessageBox.information(self, "加载模组", info_io.getvalue())

    def set_target_selected_mods(self):
        try:
            dialog = buildPlSelectionDialog(self.core)
            if dialog.exec_() != QDialog.Accepted:
                return
            sel_pl = dialog.selected_list
            print(sel_pl)
            self.core.addRecentPl(sel_pl)
            mod_names = self.get_selected_mod_names()
            text = io.StringIO()
            self.core.modSetTarget(mod_names, sel_pl, info_io=text)
            QMessageBox.information(self, "设置替换装备", text.getvalue())
            self.refreshModList()
            self.reload_selected_mods(mod_names)
        except:
            traceback.print_exc()

    def set_preset_selected_mods(self):
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
            pp_info_dict = {pp[2]: pp for pp in pp_info_list}
            print(pp_info_dict)
            mod_names = self.get_selected_mod_names()
            text = io.StringIO()
            self.core.modsSetPPTarget(mod_names, pp_info_dict, info_io=text)
            QMessageBox.information(self, "设置预设", text.getvalue())
            self.refreshModList()
            self.reload_selected_mods(mod_names)
        except Exception as e:
            traceback.print_exc()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/Miyu.ico"))
    main_window = ModManagerApp()
    main_window.show()
    sys.exit(app.exec_())