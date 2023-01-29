import os
import re
import nuke
from glob import glob
from nukescripts.version import version_get, version_set
from PySide2 import (QtUiTools, QtWidgets, QtCore)

class UpNodesToLatest(QtWidgets.QMainWindow):
    def __init__(self):
        super(UpNodesToLatest, self).__init__()
        self.load_ui()
        self.populate_table()
        self.connect_ui()

    def load_ui(self):
        loader = QtUiTools.QUiLoader()
        # ui_path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_path = "/home/jeangjenq/repository/read_tools/up_to_latest/form.ui"
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.table = self.ui.nodes_table
        
        # set window to use loaded ui file as central widget
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Upversion Nodes")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setFixedHeight(640)
        # self.setFixedWidth(480)
        self.setMinimumSize(self.table.sizeHint())

    def connect_ui(self):
        self.ui.buttonBox.accepted.connect(self.clickedOk)
        self.ui.buttonBox.rejected.connect(self.clickedCancel)

    def populate_table(self):
        # gather nodes
        nodes = nuke.allNodes("Read")
        for node in nodes:
            # create table items
            # get node basename only for ease of read
            node_file = nuke.filename(node)
            node_filename = os.path.basename(node_file)
            filename_widget = QtWidgets.QTableWidgetItem(node_filename)
            # get current version in nodegraph
            (prefix, v) = version_get(node_filename, 'v')
            c_version = "{}{}".format(prefix, v)
            c_version_widget = QtWidgets.QTableWidgetItem(c_version)
            # gather all available versions
            versions = self.detect_all_versions(node)
            versions_box = QtWidgets.QComboBox()
            if versions:
                versions_box.addItems(versions)
                versions_box.setCurrentText(versions[-1])
            else:
                versions_box.addItem(c_version)
            # create checkbox
            check = QtWidgets.QTableWidgetItem()
            check.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            check.setCheckState(QtCore.Qt.Checked)
            # add all to table
            # versions_box is a widget so use setCellWidget
            num_rows = self.table.rowCount()
            self.table.insertRow        (num_rows)
            self.table.setItem          (num_rows, 0, filename_widget)
            self.table.setItem          (num_rows, 1, c_version_widget)
            self.table.setCellWidget    (num_rows, 2, versions_box)
            self.table.setItem          (num_rows, 3, check)
        # auto stretch and resize
        # working together seem to break one or another at the moment
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.resizeColumnsToContents()

    def detect_all_versions(self, node):
        # detect all versions that exists in node folder
        # nukescripts.version_latest() contains similar function
        # but it's only friendly with v+1
        # so if there's a version skip it stops at a certain version
        # not my prefer method
        versions = []
        file = nuke.filename(node)
        # regex patterns to replace versions and frame paddings to *
        # we will use glob later to search for all files
        versions_pattern = [r"v-?\d+"]
        frame_paddings = [r"%\d+[dD]", r"\#+"]

        for pattern in versions_pattern + frame_paddings:
            file = re.sub(pattern, "*", file)
        
        # make sure all v### found in files are the same number
        # don't know under what occasion you might have 2 different versions
        # in same file path, don't know what to do about it
        def all_same(items):
            return all(x == items[0] for x in items)
        # glob returns list of files that matches the pattern
        # in this case probably all the individual frames
        files = glob(file)
        versions = []
        for file in files:
            find_version = re.findall(versions_pattern[0], file)
            if find_version and all_same(find_version):
                if find_version[0] not in versions:
                    versions.append(find_version[0])
        return versions

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
    

def UpNodesVersions():
    UpNodesVersions.UpVersionsPanel = UpNodesToLatest()
    UpNodesVersions.UpVersionsPanel.show()

    UpNodesVersions()