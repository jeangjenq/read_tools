import nuke
import nukescripts
import re



def setLocalize():

	p = nukescripts.PythonPanel('Change localization')
	p.checkboxKnob = nuke.Boolean_Knob('readOnly', 'Read nodes only', '1')
	p.localizationKnob = nuke.Enumeration_Knob('localizationPol', 'Set localization policy', ['on', 'from auto-localize path', 'on demand', 'off'])
	p.textKnob = nuke.Text_Knob('text', '', '"on demand" only available since nuke11.1')
	for k in (p.checkboxKnob, p.localizationKnob, p.textKnob):
		p.addKnob(k)

	if p.showModalDialog():
		if p.localizationKnob.value() == 'on':
			c = 0
		if p.localizationKnob.value() == 'from auto-localize path':
			c = 1
		if p.localizationKnob.value() == 'on demand':
			c = 2
		if p.localizationKnob.value() == 'off':
			c = 3

		#all nodes with the localization knob
		locNodes = [l for l in nuke.allNodes(recurseGroups=True) if nukescripts.searchreplace.__NodeHasKnobWithName(l, 'localizationPolicy')]

		for n in locNodes:
			if p.checkboxKnob.value():
				if n.Class() == 'Read':
					if not n['localizationPolicy'].setValue(c):
						n['localizationPolicy'].setValue(2)
			else:
				if not n['localizationPolicy'].setValue(c):
					n['localizationPolicy'].setValue(2)

#add 'Read localization to Auto' function to Nuke menu
nodeMenu = nuke.menu('Nuke').findItem('Edit/Node')
nodeMenu.addCommand('Custom/Set nodes localization', 'setLocalize.setLocalize()')
