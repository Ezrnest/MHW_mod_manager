import time

from PyQt5.QtWidgets import QApplication, QProgressDialog, QListWidget, QVBoxLayout, QWidget

app = QApplication([])

progress_dialog = QProgressDialog("Operation in progress...", "Cancel", 0, 100)
progress_dialog.setWindowTitle("Progress Dialog with Details")
progress_dialog.setMinimumDuration(0)
# progress_dialog.forceShow()

list_widget = QListWidget()

layout = QVBoxLayout()
layout.addWidget(list_widget)

widget = QWidget()
widget.setLayout(layout)
print(progress_dialog.layout())
progress_dialog
# progress_dialog.setLayout(layout)

# progress_dialog.setCentralWidget(widget)
progress_dialog.ad
# 模拟进度和详情更新
for i in range(100):
    progress_dialog.setValue(i)
    if progress_dialog.wasCanceled():
        break
    time.sleep(0.1)
    list_widget.addItem(f"Processing item {i+1}")
    list_widget.scrollToBottom()

progress_dialog.setValue(100)
progress_dialog.show()
app.exec_()
