import io
import sys
import time
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QListWidget, QListWidgetItem, QLineEdit, QTableWidget, QTableWidgetItem,
                             QProgressDialog, QFileDialog, QLabel, QMessageBox, QRadioButton)

from MHW.MHWData import PL_MAPPING
from ManagerCore import *



def formatPlInfo(pl_info):
    prefix, path = pl_info
    name = PL_MAPPING.get(path)
    if prefix == "f":
        name += "[女]"
    elif prefix == "m":
        name += "[男]"
    name += '(' + path + ')'
    return name


class EquipmentReplacementTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("装备替换工具")
        self.setGeometry(100, 100, 600, 500)

        self.zip_files = []
        self.rep_pl_path = None
        self.rep_pl_prefix = "m"  # Default to male equipment

        self.initUI()

    def initUI(self):
        # 主窗口部件
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # 上方 - ZIP文件列表
        self.zip_list_widget = QListWidget()
        self.zip_list_widget.setSelectionMode(QListWidget.MultiSelection)
        main_layout.addWidget(self.zip_list_widget)

        # ZIP文件选择按钮
        select_zip_button = QPushButton("选择ZIP文件")
        select_zip_button.clicked.connect(self.select_zip_files)
        main_layout.addWidget(select_zip_button)

        # separator
        main_layout.addWidget(QLabel(""))
        main_layout.addWidget(QLabel("选择目标装备"))

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("搜索...")
        self.search_bar.textChanged.connect(self.update_equipment_list)
        search_layout.addWidget(self.search_bar)
        main_layout.addLayout(search_layout)

        self.equipment_list_widget = QListWidget()
        self.equipment_list_widget.itemClicked.connect(self.on_equipment_selected)
        main_layout.addWidget(self.equipment_list_widget)

        # 单选按钮用于选择男装或女装
        radio_layout = QHBoxLayout()
        self.male_radio = QRadioButton("男装")
        self.female_radio = QRadioButton("女装")
        radio_layout.addWidget(self.male_radio)
        radio_layout.addWidget(self.female_radio)
        self.male_radio.setChecked(True)  # 默认选择男装
        self.male_radio.toggled.connect(self.update_equipment_list)
        self.female_radio.toggled.connect(self.update_equipment_list)
        main_layout.addLayout(radio_layout)

        # 选择导出文件夹
        export_layout = QHBoxLayout()
        self.export_folder = QLineEdit()
        self.export_folder.setReadOnly(True)
        export_layout.addWidget(self.export_folder)
        export_button = QPushButton("选择导出文件夹")
        export_button.clicked.connect(self.select_export_folder)
        export_layout.addWidget(export_button)
        main_layout.addLayout(export_layout)

        # 替换按钮和显示选定目标装备

        self.replace_button = QPushButton("替换并导出")
        self.replace_button.clicked.connect(self.replace_equipment)

        self.selected_equipment_label = QLabel("选定目标装备: 无")

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.selected_equipment_label)
        bottom_layout.addWidget(self.replace_button)

        main_layout.addLayout(bottom_layout)

        self.setCentralWidget(main_widget)

        self.update_equipment_list()

    def select_zip_files(self):
        zip_files, _ = QFileDialog.getOpenFileNames(self, "选择ZIP文件", "", "Zip Files (*.zip)")
        if not zip_files:
            return
        # add these files and deduplicate while keeping the order
        self.zip_files = list(dict.fromkeys(self.zip_files + zip_files))
        self.update_zip_list()
        # check if those zip files are in the same directory
        if not self.export_folder.text():
            folder = set(map(lambda x: os.path.dirname(x), zip_files)).pop()
            self.export_folder.setText(folder + "/out")

    def update_zip_list(self):
        self.zip_list_widget.clear()
        for zip_file in self.zip_files:
            self.zip_list_widget.addItem(zip_file)

    def select_export_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择导出文件夹")
        if folder:
            self.export_folder.setText(folder)

    @staticmethod
    def addToList(list_widget, key, value):
        from PyQt5.QtCore import Qt
        itm = QListWidgetItem(value)
        itm.setData(Qt.UserRole, key)
        list_widget.addItem(itm)

    def update_equipment_list(self):
        self.equipment_list_widget.clear()
        search_text = self.search_bar.text().lower()
        for path, name in PL_MAPPING.items():
            if search_text in name.lower():
                self.addToList(self.equipment_list_widget, path, name + ' (' + path + ')')

    def on_equipment_selected(self, item):
        self.rep_pl_path = item.data(Qt.UserRole)
        self.rep_pl_prefix = "m" if self.male_radio.isChecked() else "f"
        pl_info = (self.rep_pl_prefix, self.rep_pl_path)
        self.selected_equipment_label.setText(f"目标装备: {formatPlInfo(pl_info)}")

    def replace_equipment(self):
        if not self.zip_files or not self.rep_pl_path:
            QMessageBox.warning(self, "警告", "请先选择ZIP文件和目标装备！")
            return
        # check the export folder
        export_folder = self.export_folder.text()
        if not export_folder:
            QMessageBox.warning(self, "警告", "请先选择导出文件夹！")
            return
        # check the export folder does not contain any selected zip files
        for zip_file in self.zip_files:
            if Path(os.path.basename(zip_file)) == Path(export_folder):
                QMessageBox.warning(self, "警告", "请选择新的文件夹导出！")
                return

        os.makedirs(export_folder, exist_ok=True)

        progress_dialog = QProgressDialog("替换装备中...", "取消", 0, len(self.zip_files), self)
        progress_dialog.setWindowTitle("替换进度")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)

        for i, zip_file in enumerate(self.zip_files):
            if progress_dialog.wasCanceled():
                break
            progress_dialog.setValue(i + 1)

            progress_dialog.setLabelText(f"正在替换 {zip_file} 为 {self.rep_pl_path}")
            name = zip_file.split('/')[-1]
            out_file = os.path.join(export_folder, name)
            try:
                process_simple_pl_zip(zip_file, out_file, (self.rep_pl_prefix, self.rep_pl_path))
            except Exception as e:
                text = traceback.format_exc()
                QMessageBox.critical(self, "错误", "替换装备失败！\n" + text)

                break

        progress_dialog.setValue(len(self.zip_files))
        QMessageBox.information(self, "替换完成", "装备替换完成！")

        self.zip_files = []
        self.update_zip_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentReplacementTool()
    window.show()
    sys.exit(app.exec_())
