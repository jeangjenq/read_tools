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
        self.connect_ui()

    def load_ui(self):
        loader = QtUiTools.QUiLoader()
        # ui_path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_path = "/home/jeangjenq/repository/JJRepo/nuke/JJ-tools/read_tools/uptolatest/form.ui"
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        # set window to use loaded ui file as central widget
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Upversion Nodes")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedHeight(640)
        self.setFixedWidth(480)

    def connect_ui(self):
        self.ui.buttonBox.accepted.connect(self.clickedOk)
        self.ui.buttonBox.rejected.connect(self.clickedCancel)

    def up_selected_nodes():
        pass

    def clickedOk(self):
        self.close()
    
    def clickedCancel(self):
        self.close()
    

if not standalone:
    def UpNodesVersions():
        UpNodesVersions.UpVersionsPanel = UpNodesToLatest()
        # UpNodesVersions.UpVersionsPanel.show()
    UpNodesVersions()
else:
    app = QtWidgets.QApplication(sys.argv)
    window = UpNodesToLatest()
    window.show()
    app.exec_()