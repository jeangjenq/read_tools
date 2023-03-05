'''
readTools v2.2
Written by Jeang Jenq Loh
Latest update: 22 May 2022

A compilation of scripts that modify multiple read nodes at once
# Select all read nodes
# Set localization settings
# Set frame range
# Set missing frames settings
# Refresh selected read nodes
'''
import nuke
import nukescripts
from nukescripts.searchreplace import __NodeHasKnobWithName as NodeHasKnobWithName
import os
import re
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
    from PySide import QtUiTools
else:
    from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools


def selectRead():
    '''
    deselect any selected nodes
    select all reads
    '''
    for n in nuke.allNodes():
        n['selected'].setValue('False')
    for n in nuke.allNodes('Read'):
        n.['selected'].setValue('True')


def refreshReads():
    '''
    refresh selected nodes
    '''
    for node in nuke.selectedNodes():
        if node['reload']:
            node['reload'].execute()


def deleteFiles():
    '''
    delete node's files
    popup dialog to confirm
    '''
    #gather a list of all selected read nodes and filter out non-read nodes
    all = nuke.selectedNodes()
    for node in all:
        if not node.Class() == 'Read':
            all.remove(node)
    files = []

    #get a list of files to be deleted
    for n in all:
        #get file path while replacing the hashes with %0#d
        path = nukescripts.replaceHashes(nuke.filename(n))
        padd = re.search(r'%.*d', path)
        framerange = range(n['first'].value(), n['last'].value() + 1)
        for index in framerange:
            if padd:
                fra = (padd.group(0)) % index
                name = str(re.sub(r'%.*d', str(fra), path))
            elif not padd:
                name = path
            if name not in files:
                files.append(name)

    #list of node names about to be deleted
    nodesToDelete = []
    for na in all:
        nodesToDelete.append(na['name'].value())

    #Confirm files deletion
    if nodesToDelete:
        if nuke.ask('About to delete files from: ' + '\n' + str(nodesToDelete) + '\n' + "Confirm?"):
            for e in files:
                try:
                    os.remove(e)
                except:
                    pass
        else:
            pass


class ReadKnobs(QtWidgets.QMainWindow):
    '''
    read ui file for modifying read knobs
    adjust ui according to user selection:
    1. localization policy
    2. frame range
    3. missing frames policy
    '''
    def __init__(self, knob_select, parent=None):
        '''
        set up an intvalidator as it will be used often
        change policy label and combobox
        populate comboboxes according to knob
        '''
        super(ReadKnobs, self).__init__(parent)

        # determine what function is called
        # need to write this
        
    def collect_nodes(self):
        self.nodes = nuke.selectedNodes()



class setLocalize_panel(QtWidgets.QMainWindow):
    # PySide2 panel to set localization policy on all nodes
    def __init__(self, parent=None):
        super(setLocalize_panel, self).__init__(parent)

        nodeSelectionLabel = QtWidgets.QLabel("Nodes selection")
        self.nodeSelection = QtWidgets.QComboBox()
        selections = ['All nodes', 'Selected nodes', 'Exclude selected']
        self.nodeSelection.addItems(selections)

        self.readNodesOnlyCheck = QtWidgets.QCheckBox("Read nodes only")
        self.readNodesOnlyCheck.setChecked(True)
        self.readNodesOnlyCheck.setToolTip("Untick checkbox if you want to include ReadGeo!")
        
        policyLabel = QtWidgets.QLabel("Set localization policy")
        policies = ['on', 'from auto-localize path', 'on demand', 'off']
        self.policyDropdown = QtWidgets.QComboBox()
        self.policyDropdown.addItems(policies)
        if nuke.NUKE_VERSION_MAJOR < 11:
            self.policyDropdown.removeItem("on demand")
        
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.clickedOk)
        self.buttonBox.rejected.connect(self.clickedCancel)

        masterLayout = QtWidgets.QGridLayout()
        masterLayout.addWidget(nodeSelectionLabel, 0,0)
        masterLayout.addWidget(self.nodeSelection, 0,1)
        masterLayout.addWidget(self.readNodesOnlyCheck, 1,1)
        masterLayout.addWidget(policyLabel, 3,0)
        masterLayout.addWidget(self.policyDropdown, 3,1)
        masterLayout.addWidget(self.buttonBox)
        self.setLayout(masterLayout)
        self.setWindowTitle("Set Localization Policy")

    def clickedOk(self):
        selection = self.nodeSelection.currentText()
        readOnly = self.readNodesOnlyCheck.isChecked()
        policy = self.policyDropdown.currentIndex()
        if selection == 'All nodes':
            #all nodes with localization knob
            Sel = [l for l in nuke.allNodes(recurseGroups=True) if NodeHasKnobWithName(l, 'localizationPolicy')]
            # pass
        elif self.nodeSelection.currentText() == 'Selected nodes only':
            Sel = nuke.selectedNodes()
        else:
            Sel = [l for l in nuke.allNodes(recurseGroups=True) if NodeHasKnobWithName(l, 'localizationPolicy')]
            # pass
            for i in nuke.selectedNodes():
                try:
                    Sel.remove(i)
                except ValueError:
                    pass

        for n in Sel:
            if readOnly:
                if n.Class() == 'Read':
                    n['localizationPolicy'].setValue(policy)
            else:
                n['localizationPolicy'].setValue(policy)
        self.close()
        return True
        
    def clickedCancel(self):
        self.close()

def setLocalize():
    # summon localization popup
    setLocalize.setLocalizePanel = setLocalize_panel()
    setLocalize.setLocalizePanel.show()


class setFrameRange_Panel(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(setFrameRange_Panel, self).__init__(parent)

        nodeSelectionLabel = QtWidgets.QLabel("Nodes selection")
        self.nodeSelection = QtWidgets.QComboBox()
        selections = ['All read nodes', 'Selected nodes only', 'Exclude selected nodes']
        self.nodeSelection.addItems(selections)

        nodeSelectionWidget = QtWidgets.QWidget()
        nodeSelectionLayout = QtWidgets.QHBoxLayout()
        nodeSelectionLayout.addWidget(nodeSelectionLabel)
        nodeSelectionLayout.addWidget(self.nodeSelection)
        nodeSelectionWidget.setLayout(nodeSelectionLayout)

        frameRangeLabel = QtWidgets.QLabel("frame range")
        self.first_frame = QtWidgets.QLineEdit()
        self.first_frame.setText(str(int(nuke.Root()['first_frame'].value())))
        self.before = QtWidgets.QComboBox()
        self.last_frame = QtWidgets.QLineEdit()
        self.last_frame.setText(str(int(nuke.Root()['last_frame'].value())))
        framesValidator = QtGui.QIntValidator()
        self.first_frame.setValidator(framesValidator)
        self.last_frame.setValidator(framesValidator)
        self.after = QtWidgets.QComboBox()
        frame_mode = ['hold', 'loop', 'bounce', 'black']
        self.before.addItems(frame_mode)
        self.after.addItems(frame_mode)

        frameRangeWidget = QtWidgets.QWidget()
        frameRangeLayout = QtWidgets.QHBoxLayout()
        for widget in [frameRangeLabel, self.first_frame, self.before, self.last_frame, self.after]:
            frameRangeLayout.addWidget(widget)
        frameRangeWidget.setLayout(frameRangeLayout)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.clickedOk)
        self.buttonBox.rejected.connect(self.clickedCancel)

        masterLayout = QtWidgets.QVBoxLayout()
        masterSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        masterSplitter.addWidget(nodeSelectionWidget)
        masterSplitter.addWidget(frameRangeWidget)
        masterLayout.addWidget(masterSplitter)
        masterLayout.addWidget(self.buttonBox)
        self.setLayout(masterLayout)
        self.setWindowTitle("Set read nodes frame range")

    def clickedOk(self):
        nodeSelection = self.nodeSelection.currentText()
        first = int(self.first_frame.text())
        before = self.before.currentIndex()
        last = int(self.last_frame.text())
        after = self.after.currentIndex()
    
        if nodeSelection == 'All read nodes':
            Sel = nuke.allNodes('Read')
        elif nodeSelection == 'Selected nodes only':
            Sel = nuke.selectedNodes()
        else:
            Sel = nuke.allNodes('Read')
            for i in nuke.selectedNodes():
                try:
                    Sel.remove(i)
                except ValueError:
                    pass

        for r in Sel:
            try:
                r['first'].setValue(first)
                r['before'].setValue(before)
                r['last'].setValue(last)
                r['after'].setValue(after)
            except ValueError:
                nuke.message('No nodes selected!')
            except NameError:
                pass
        self.close()
        return True

    def clickedCancel(self):
        self.reject()

def setFrameRange():
    setFrameRange.setFrameRangePanel = setFrameRange_Panel()
    setFrameRange.setFrameRangePanel.show()


class setError_Panel(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(setError_Panel, self).__init__(parent)

        nodeSelectionLabel = QtWidgets.QLabel("Nodes selection")
        self.nodeSelection = QtWidgets.QComboBox()
        selections = ['All read nodes', 'Selected nodes only', 'Exclude selected nodes']
        self.nodeSelection.addItems(selections)

        errorLabel = QtWidgets.QLabel("missing frames")
        self.onError = QtWidgets.QComboBox()
        errors = ['error', 'black', 'checkerboard', 'nearest frame']
        self.onError.addItems(errors)
        self.reloadCheck = QtWidgets.QCheckBox("Reload changed nodes")

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.clickedOk)
        buttonBox.rejected.connect(self.clickedCancel)

        masterLayout = QtWidgets.QGridLayout()
        masterLayout.addWidget(nodeSelectionLabel, 0,0)
        masterLayout.addWidget(self.nodeSelection, 0,1)
        masterLayout.addWidget(errorLabel, 1,0)
        masterLayout.addWidget(self.onError, 1,1)
        masterLayout.addWidget(self.reloadCheck, 2,1)
        masterLayout.addWidget(buttonBox, 3,1)
        self.setLayout(masterLayout)
        self.setWindowTitle("Missing frames settings")

    def clickedOk(self):
        nodeSelection = self.nodeSelection.currentText()
        onError = self.onError.currentIndex()
        reloadCheck = self.reloadCheck.isChecked()

        if nodeSelection == 'All read nodes':
            Sel = nuke.allNodes('Read')
        elif nodeSelection == 'Selected nodes only':
            Sel = nuke.selectedNodes()
        else:
            Sel = nuke.allNodes('Read')
            for i in nuke.selectedNodes():
                try:
                    Sel.remove(i)
                except ValueError:
                    nuke.message('No nodes selected!')
                except NameError:
                    pass

        for r in Sel:
            try:
                r['on_error'].setValue(onError)
                if reloadCheck:
                    r.knob('reload').execute()
            except ValueError:
                nuke.message('No nodes selected!')
            except NameError:
                pass
        self.close()
        return True
    
    def clickedCancel(self):
        self.reject()

def setError():
    setError.setErrorPanel = setError_Panel()
    setError.setErrorPanel.show()
