import readTools

#Create toolbar with icon
toolbar = nuke.menu('Nodes').addMenu('jj_tools', icon='icon_JJ.png')

#Python menu
Pytmenu = toolbar.addMenu('Python/Read Tools')
Pytmenu.addCommand('Select Read Nodes', 'readTools.selectRead()', index=0)
Pytmenu.addCommand('Set nodes localization', 'readTools.setLocalize()')
Pytmenu.addCommand('Set read nodes frame range', 'readTools.setFrameRange()')
Pytmenu.addCommand('Missing frames setting', 'readTools.setError()')
