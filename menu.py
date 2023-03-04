import readTools

# load versions table
nuke.pluginAddPath("./versions_table")
import nodes_set_version

#Create toolbar with icon
toolbar = nuke.menu('Nodes').addMenu('jj_tools', icon='icon_JJ.png')

#Python menu
read_tools_menu = toolbar.addMenu('Read Tools')
read_tools_menu.addCommand('Select Read Nodes', 'readTools.selectRead()', index=0)
read_tools_menu.addCommand('Set nodes localization', 'readTools.setLocalize()')
read_tools_menu.addCommand('Set read nodes frame range', 'readTools.setFrameRange()')
read_tools_menu.addCommand('Missing frames setting', 'readTools.setError()')
read_tools_menu.addCommand('Reload selected reads', 'readTools.refreshReads()')
read_tools_menu.addCommand('Nodes version', 'versions_table.NodesVersions()')
read_tools_menu.addCommand('Delete Files', 'readTools.deleteFiles()')