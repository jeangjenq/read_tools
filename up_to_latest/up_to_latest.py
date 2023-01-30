import os
import re
import nuke
from glob import glob
from nukescripts.version import version_get, version_set
from PySide2 import QtUiTools, QtWidgets, QtCore, QtGui

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
        # populate table with all nodes and its latest version
        # include checkbox to determine whether to skip some nodes
        # color change on out of version nodes
        # gather nodes
        nodes = nuke.allNodes("Read")
        for node in nodes:
            # create table items

            # get node basename only for ease of read
            # attach node into the widget data for fetching later
            node_file = nuke.filename(node)
            node_filename = os.path.basename(node_file)
            filename_widget = QtWidgets.QTableWidgetItem()
            filename_widget.setText(node_filename)
            filename_widget.setData(QtCore.Qt.UserRole, node)

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

            # create update checkbox
            check_widget = QtWidgets.QTableWidgetItem("Update this node")
            check_widget.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            check_widget.setCheckState(QtCore.Qt.Checked)

            # create some action buttons
            focus_button = QtWidgets.QPushButton("Focus")
            openf_button = QtWidgets.QPushButton("Open Folder")
            focus_button.clicked.connect(self.focus_on_node)
            openf_button.clicked.connect(self.open_node_folder)
            actions_layout = QtWidgets.QHBoxLayout()
            for widget in [focus_button, openf_button]:
                widget.setSizePolicy(   QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
                widget.setMinimumSize(20, 20)
                actions_layout.addWidget(widget)
            actions_widget = QtWidgets.QWidget()
            actions_widget.setLayout(actions_layout)

            # change row color if version outdated
            if versions_box.currentText() != c_version:
                for item in [filename_widget, c_version_widget, check_widget]:
                    item.setForeground(QtCore.Qt.red)

            # add all to table
            # versions_box is a widget so use setCellWidget
            num_rows = self.table.rowCount()
            self.table.insertRow        (num_rows)
            filename =  self.table.setItem          (num_rows, 0, filename_widget)
            current =   self.table.setItem          (num_rows, 1, c_version_widget)
            latest =    self.table.setCellWidget    (num_rows, 2, versions_box)
            tickbox =   self.table.setItem          (num_rows, 3, check_widget)
            actions =   self.table.setCellWidget    (num_rows, 4, actions_widget)


        # auto stretch and resize
        # self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
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
        # set version if upversion checkbox is check
        up_nodes = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.item(row, self.table.columnCount()-1)
            checkstate = checkbox.checkState()
            if checkstate:
                node =      self.table.item(row, 0).data(QtCore.Qt.UserRole)
                current =   self.table.item(row, 1).text()[1:]
                set_to =    self.table.cellWidget(row, 2).currentText()[1:]
                node_data = {"node": node,
                             "current": current,
                             "set_to": set_to
                            }
                up_nodes.append(node_data)
        for data in up_nodes:
            print(data)
            node = data['node']
            current = data['current']
            set_to = data['set_to']
            orig_file = node['file'].value()
            new_file = version_set(orig_file, "v", int(current), int(set_to))
            node['file'].setValue(new_file)

    def focus_on_node(self):
        sender = self.sender()
        nuke.zoomToFitSelected()
        print(sender)

    def open_node_folder(self):
        sender = self.sender()
        print(sender)

    def clickedOk(self):
        self.up_selected_nodes()
        self.close()
    
    def clickedCancel(self):
        self.close()
    

def UpNodesVersions():
    UpNodesVersions.UpVersionsPanel = UpNodesToLatest()
    UpNodesVersions.UpVersionsPanel.show()

UpNodesVersions()