import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QTableView, QHeaderView, QAbstractItemView, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class DraggableTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Enable dragging and dropping of rows using the vertical header
        self.verticalHeader().setSectionsMovable(True)
        self.verticalHeader().setDragEnabled(True)
        self.verticalHeader().setDragDropMode(QAbstractItemView.InternalMove)
        self.verticalHeader().setDropIndicatorShown(True)

        # Enable sorting by clicking the horizontal header
        self.horizontalHeader().setSectionsClickable(True)
        self.horizontalHeader().setSortIndicatorShown(True)

        # Disable horizontal dragging and dropping
        self.horizontalHeader().setSectionsMovable(False)

        # Track the original order before sorting
        self._original_order = []
        self._sorted_column = None
        self._sort_order = None

        # Connect the header click signal to the sorting method
        self.horizontalHeader().sectionClicked.connect(self.sortByColumn)

    def dropEvent(self, event):
        """Override dropEvent to handle the row moving logic"""
        source_row = self.currentRow()
        target_row = self.rowAt(event.pos().y())

        if target_row != -1 and source_row != -1 and source_row != target_row:
            # Move the row to the new position
            self.insertRow(target_row)
            for col in range(self.columnCount()):
                self.setItem(target_row, col, self.takeItem(source_row + 1, col))
            self.removeRow(source_row + 1)

        super().dropEvent(event)

    def sortByColumn(self, column, order=None):
        """Sort the table by the clicked column"""
        if self._sorted_column == column:
            if self._sort_order == Qt.AscendingOrder:
                self._sort_order = Qt.DescendingOrder
            elif self._sort_order == Qt.DescendingOrder:
                self._sort_order = None  # Reset to original order
            else:
                self._sort_order = Qt.AscendingOrder
        else:
            self._sort_order = Qt.AscendingOrder
            self._sorted_column = column

        if self._sort_order is None:
            self.resetToOriginalOrder()
        else:
            self.sortItemsWithHeaders(column, self._sort_order)

    def setRowCount(self, rows):
        """Override setRowCount to track the original order of rows"""
        super().setRowCount(rows)
        self._original_order = list(range(rows))


    def resetToOriginalOrder(self):
        """Reset the table to its original order before any sorting"""
        for original_row, current_row in enumerate(self._original_order):
            for col in range(self.columnCount()):
                self.setItem(original_row, col, self.takeItem(current_row, col))
            self.setVerticalHeaderItem(original_row, QTableWidgetItem(str(original_row + 1)))
        self._sorted_column = None
        self._sort_order = None

    def sortItemsWithHeaders(self, column, order):
        """Sort the table by the specified column and move row headers accordingly"""
        row_data = []
        for row in range(self.rowCount()):
            items = [self.item(row, col) for col in range(self.columnCount())]
            row_data.append((items, self.verticalHeaderItem(row).text()))
        # self.sortItems()
        # Sort based on the specified column and order
        row_data.sort(key=lambda x: x[0][column], reverse=(order == Qt.DescendingOrder))

        # Apply sorted data back to the table
        for row, (items, header) in enumerate(row_data):
            for col, item in enumerate(items):
                self.setItem(row, col, QTableWidgetItem(item))
            self.setVerticalHeaderItem(row, QTableWidgetItem(header))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    table = DraggableTable()
    table.resize(800,800)
    table.setRowCount(5)
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["A","B","C"])
    table.setVerticalHeaderLabels(["1","2","3","4","5"])
    for row in range(5):
        for col in range(3):
            table.setItem(row, col, QTableWidgetItem(f"{row+1}"))
    table.setItem(3,2,QTableWidgetItem("0"))
    table.setRowHidden(2,True)
    print(table.rowCount())
    table.show()
    sys.exit(app.exec_())
