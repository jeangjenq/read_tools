import nuke

def selectRead():
    n = nuke.allNodes()
    for i in n:
        if i.Class() == 'Read':
            i.knob('selected').setValue('True')

#add 'select read nodes' function to Nuke menu
nodeMenu = nuke.menu('Nuke').findItem('Edit/Node')
nodeMenu.addCommand('Custom/Select Read Nodes', 'selectRead.selectRead()')
