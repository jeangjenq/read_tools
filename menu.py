# load read knobs
nuke.pluginAddPath("./read_knobs")
import read_knobs

# load versions table
nuke.pluginAddPath("./versions_table")
import nodes_set_version

#Create toolbar with icon
toolbar = nuke.menu('Nodes').addMenu('jj_tools', icon='icon_JJ.png')

#Python menu
read_tools_menu = toolbar.addMenu('Read Tools')
read_tools_menu.addCommand('Select Read Nodes', 'read_knobs.selectRead()', index=0)
read_tools_menu.addCommand('Set nodes localization', 'read_knobs.ReadKnobs("localization")')
read_tools_menu.addCommand('Set read nodes frame range', 'read_knobs.ReadKnobs("framerange)')
read_tools_menu.addCommand('Missing frames setting', 'read_knobs.ReadKnobs("error")')
read_tools_menu.addCommand('Reload selected reads', 'read_knobs.refreshReads()')
read_tools_menu.addCommand('Nodes version', 'versions_table.NodesVersions()')
read_tools_menu.addCommand('Delete Files', 'read_knobs.deleteFiles()')