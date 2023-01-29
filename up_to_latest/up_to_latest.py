import os
from PySide2 import (QtUiTools, QtWidgets, QtCore)
try:
    import nuke
    standalone = False
except ModuleNotFoundError:
    import sys
    standalone = True

class UpNodesToLatest(QtWidgets.QMainWindow):
    def __init__(self):
        super(UpNodesToLatest, self).__init__()
        self.load_ui()
        self.populate_table()
        self.connect_ui()

    def load_ui(self):
        loader = QtUiTools.QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "form.ui")
        # ui_path = "/home/jeangjenq/repository/read_tools/up_to_latest/form.ui"
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.table = self.ui.nodes_table
        
        # set window to use loaded ui file as central widget
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Upversion Nodes")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedHeight(640)
        self.setFixedWidth(480)

    def connect_ui(self):
        self.ui.buttonBox.accepted.connect(self.clickedOk)
        self.ui.buttonBox.rejected.connect(self.clickedCancel)

    def populate_table(self):
        # gather nodes
        nodes = ["A", "B", "C"]
        for node in nodes:
            # create table items
            node_filename = QtWidgets.QTableWidgetItem(node)
            c_version = QtWidgets.QTableWidgetItem("v001")
            # gather all available versions
            versions = ["v001", "v002", "v014"]
            versions_box = QtWidgets.QComboBox()
            versions_box.addItems(versions)
            versions_box.setCurrentText(versions[-1])
            # create checkbox
            check = QtWidgets.QTableWidgetItem()
            check.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            check.setCheckState(QtCore.Qt.Checked)

            num_rows = self.table.rowCount()
            self.table.insertRow        (num_rows)
            self.table.setItem          (num_rows, 0, node_filename)
            self.table.setItem          (num_rows, 1, c_version)
            self.table.setCellWidget    (num_rows, 2, versions_box)
            self.table.setItem          (num_rows, 3, check)


    def up_selected_nodes(self):
        up_nodes = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.item(row, self.table.columnCount()-1)
            checkstate = checkbox.checkState()
            if checkstate:
                up_nodes.append(self.table.item(row, 0).text())
        print(up_nodes)

    def clickedOk(self):
        self.up_selected_nodes()
        self.close()
    
    def clickedCancel(self):
        self.close()
    

if not standalone:
    def UpNodesVersions():
        UpNodesVersions.UpVersionsPanel = UpNodesToLatest()
        UpNodesVersions.UpVersionsPanel.show()
    UpNodesVersions()
else:
    app = QtWidgets.QApplication(sys.argv)
    window = UpNodesToLatest()
    window.show()
    app.exec_()