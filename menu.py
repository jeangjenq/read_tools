import selectRead
import setLocalize

#Create toolbar with icon
toolbar = nuke.menu('Nodes').addMenu('jj_tools', icon='icon_JJ.png')

#Python menu
Pytmenu = toolbar.addMenu('Python')
Pytmenu.addCommand('Set nodes localization', 'setLocalize.setLocalize()')
Pytmenu.addCommand('Select Read Nodes', 'selectRead.selectRead()')
