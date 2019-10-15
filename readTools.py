import nuke
import nukescripts

def newUserKnob(knob, value):
    knob.setValue(value)
    return knob

def allReads():
    readNodes = []
    for i in nuke.allNodes():
        if i.Class() == 'Read':
            readNodes.append(i)
    return readNodes

def selectRead():
    for i in allReads():
        i.knob('selected').setValue('True')

def setLocalize():
    p = nukescripts.PythonPanel('Change localization')
    p.nodesSelection = nuke.Enumeration_Knob('nodesSel', 'Nodes selections', ['All nodes', 'Selected nodes only', 'Exclude selected nodes'])
    p.checkboxKnob = nuke.Boolean_Knob('readOnly', 'Read nodes only', '1')
    p.readText = nuke.Text_Knob('text', '', 'ReadGeo for instance also has localizationPolicy')
    p.divText = nuke.Text_Knob('divText', '')
    p.localizationKnob = newUserKnob(nuke.Enumeration_Knob('localizationPol', 'Set localization policy', ['on', 'from auto-localize path', 'on demand', 'off']), 1)
    p.textKnob = nuke.Text_Knob('text', '', '"on demand" only available since nuke11.1')
    for k in (p.nodesSelection, p.checkboxKnob, p.readText, p.divText, p.localizationKnob, p.textKnob):
        k.setFlag(0x1000)
        p.addKnob(k)

    #show dialog
    if p.showModalDialog():
        if p.nodesSelection.value() == 'All nodes':
            #all nodes with localization knob
            Sel = [l for l in nuke.allNodes(recurseGroups=True) if nukescripts.searchreplace.__NodeHasKnobWithName(l, 'localizationPolicy')]
        elif p.nodesSelection.value() == 'Selected nodes only':
            Sel = nuke.selectedNodes()
        else:
            Sel = [l for l in nuke.allNodes(recurseGroups=True) if nukescripts.searchreplace.__NodeHasKnobWithName(l, 'localizationPolicy')]
            for i in nuke.selectedNodes():
                try:
                    Sel.remove(i)
                except ValueError:
                    pass

        for n in Sel:
            if p.checkboxKnob.value():
                if n.Class() == 'Read':
                    if not n['localizationPolicy'].setValue(int(p.localizationKnob.getValue())):
                        n['localizationPolicy'].setValue(2)
            else:
                if not n['localizationPolicy'].setValue(int(p.localizationKnob.getValue())):
                    n['localizationPolicy'].setValue(2)

def setFrameRange():
    f = nukescripts.PythonPanel('Set read nodes frame range')
    f.nodesSelection = nuke.Enumeration_Knob('nodesSel', 'Nodes selections', ['All read nodes', 'Selected nodes only', 'Exclude selected nodes'])
    f.divText = nuke.Text_Knob('divText', '')
    f.firstFrame = newUserKnob(nuke.Int_Knob('first_frame', 'frame range', 1), int(nuke.root().firstFrame()))
    f.before = nuke.Enumeration_Knob('before', '', ['hold', 'loop', 'bounce', 'black'])
    f.lastFrame = newUserKnob(nuke.Int_Knob('last_frame', '', 100), int(nuke.root().lastFrame()))
    f.after = nuke.Enumeration_Knob('after', '', ['hold', 'loop', 'bounce', 'black'])

    #Set nodes selection and after as end line
    for s in (f.nodesSelection, f.after):
        s.setFlag(0x2000)
    for k in (f.nodesSelection, f.divText, f.firstFrame, f.before, f.lastFrame, f.after):
        f.addKnob(k)

    #show dialog
    if f.showModalDialog():
        if f.nodesSelection.value() == 'All read nodes':
            Sel = allReads()
        elif f.nodesSelection.value() == 'Selected nodes only':
            Sel = nuke.selectedNodes()
        else:
            Sel = allReads()
            for i in nuke.selectedNodes():
                try:
                    Sel.remove(i)
                except ValueError:
                    pass

        for r in Sel:
            try:
                r['first'].setValue(f.firstFrame.value())
                r['before'].setValue(f.before.value())
                r['last'].setValue(f.lastFrame.value())
                r['after'].setValue(f.after.value())
            except ValueError:
                nuke.message('No nodes selected!')
            except NameError:
                pass

def setError():
    e = nukescripts.PythonPanel('Missing frames setting')
    e.nodesSelection = nuke.Enumeration_Knob('nodesSel', 'Nodes selections', ['All read nodes', 'Selected nodes only', 'Exclude selected nodes'])
    e.divText = nuke.Text_Knob('divText', '')
    e.onError = nuke.Enumeration_Knob('onError', 'missing frames', ['error', 'black', 'checkerboard', 'nearest frame'])
    e.reload = newUserKnob(nuke.Boolean_Knob('reload', 'Reload changed nodes', '0'), 0)
    for k in (e.nodesSelection, e.divText, e.onError, e.reload):
        k.setFlag(0x1000)
        e.addKnob(k)

    #show dialog
    if e.showModalDialog():
        if e.nodesSelection.value() == 'All read nodes':
            Sel = allReads()
        elif e.nodesSelection.value() == 'Selected nodes only':
            Sel = nuke.selectedNodes()
        else:
            Sel = allReads()
            for i in nuke.selectedNodes():
                try:
                    Sel.remove(i)
                except ValueError:
                    nuke.message('No nodes selected!')
                except NameError:
                    pass

        for r in Sel:
            try:
                r['on_error'].setValue(int(e.onError.getValue()))
                if e.reload.value():
                    r.knob('reload').execute()
            except ValueError:
                nuke.message('No nodes selected!')
            except NameError:
                pass


