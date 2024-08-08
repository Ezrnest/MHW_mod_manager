from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTableWidget with Validation")
        self.resize(400, 300)

        # Create a QTableWidget
        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])


        # Populate the table with some data
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f"Item {row+col}")
                item.setData(Qt.UserRole, row+col)
                self.table.setItem(row, col, item)

        self.table.itemChanged.connect(self.validate_item)
        # Connect the itemChanged signal to the validation slot
        # block the signal of itemChanged
        self.table.blockSignals(True)
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f"Item {row+col}")
                item.setData(Qt.UserRole, row+col)
                self.table.setItem(row, col, item)
        self.table.blockSignals(False)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def validate_item(self, item):
        # Example validation: only allow integers as valid input
        try:
            new_value = int(item.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer.")
            # Restore the old value if the new one is invalid
            item.setText(str(item.data(Qt.UserRole)))
            return

        # Save the new value as valid by storing it in UserRole
        item.setData(Qt.UserRole, new_value)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
