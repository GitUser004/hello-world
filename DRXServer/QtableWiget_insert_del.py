import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt


class testWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.table = QTableWidget(self)
        self.table.move(20, 20)
        self.table.setColumnCount(3)
        self.table.setFixedHeight(300)
        self.table.setFixedWidth(500)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格的选取方式是行选取
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置选取方式为单个选取
        self.table.setHorizontalHeaderLabels(["标记ID", "标记名称", "标记初始坐标"])  # 设置行表头
        self.table.verticalHeader().setVisible(False)  # 隐藏列表头

        self.table_insert()

        self.table.itemChanged.connect(self.table_update)

        self.delete_button = QPushButton(self)
        self.delete_button.move(230, 350)
        self.delete_button.setFixedWidth(100)
        self.delete_button.setFixedHeight(32)
        self.delete_button.clicked.connect(self.table_delete)
        self.delete_button.setText("Delete")

        self.dadd_button = QPushButton(self)
        self.dadd_button.move(330, 350)
        self.dadd_button.setFixedWidth(100)
        self.dadd_button.setFixedHeight(32)
        self.dadd_button.clicked.connect(self.table_insert)
        self.dadd_button.setText("add")

        self.update_button = QPushButton(self)
        self.update_button.move(130, 350)
        self.update_button.setFixedWidth(100)
        self.update_button.setFixedHeight(32)
        self.update_button.clicked.connect(self.table_update)
        self.update_button.setText("update")

        self.setGeometry(200, 200, 570, 400)
        self.show()

    # insert,只是简单插入一个固定数据
    def table_insert(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_id = QTableWidgetItem("1")
        item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        item_name = QTableWidgetItem("door")  # 我们要求它可以修改，所以使用默认的状态即可
        item_pos = QTableWidgetItem("(1,2)")
        item_pos.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择

        self.table.setItem(row, 0, item_id)
        self.table.setItem(row, 1, item_name)
        self.table.setItem(row, 2, item_pos)
        # 以下可以加入保存数据到数据的操作

    # update
    def table_update(self):
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        new_name = row_select[1].text()
        print("id: {}, save_name: {}".format(id, new_name))
        # 以下可以加入保存数据到数据的操作
        '''
        eg. update {table} set name = "new_name" where id = "id"
        '''
        row_select[1].setText('11111111111')

    # delete
    def table_delete(self):
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))

        row = row_select[0].row()
        self.table.removeRow(row)
        # 以下可以加入保存数据到数据的操作
        '''
        eg. delete from {table} where id = "id"
        '''


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = testWindow()
    sys.exit(app.exec_())