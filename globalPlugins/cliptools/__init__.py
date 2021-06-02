# A part of cliptools.
# Copyright (C) 2021, Quin Marilyn. All rights reserved.
# This code is GPL. See NVDA's license.
# All of NVDA's license and copying conditions apply here,
# including the waranty disclosure.
#
# Some GUI code adapted from the Tip-of-the-day add-on by Derek Riemer.

import globalPluginHandler
from scriptHandler import script
import gui
import ui
import wx
from . import pyperclip
import tones
import config
from gui import guiHelper, settingsDialogs

confspec = {
	"beeps": "boolean(default=False)"
}
config.conf.spec["cliptools"] = confspec


class CliptoolsPanel(gui.SettingsPanel):
	# Translators: The title of the Cliptools settings dialog.
	title = _("Cliptools")

	def makeSettings(self, sizer):
		helper = guiHelper.BoxSizerHelper(self, sizer=sizer)
		self.smBeeps = helper.addItem(
			# Translators: The title of the check box for beeps in Cliptools.
			wx.CheckBox(self, label=_("&Beep when certain events are preformed"))
		)
		self.smBeeps.SetValue(config.conf["cliptools"]["beeps"])

	def onSave(self):
		config.conf["cliptools"]["beeps"] = self.smBeeps.IsChecked()


class ClipDialog(wx.Dialog):
	def __init__(self):
		# Translators: The title of the dialog that pops up when the user presses NVDA+E.
		super(ClipDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title=_("Cliptools"))
		self.panel = panel = wx.Panel(self, wx.ID_ANY)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		clipSizer = wx.BoxSizer(wx.VERTICAL)
		self.title = item = wx.StaticText(panel)
		clipSizer.Add(item)
		self.edit = item = wx.TextCtrl(panel, size=(500, 500), style=wx.TE_MULTILINE)
		clipSizer.Add(item)
		mainSizer.Add(clipSizer, border=20, flag=wx.LEFT | wx.RIGHT | wx.TOP)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		item = wx.Button(panel, wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onOk, item)
		buttonSizer.Add(item)
		mainSizer.Add(buttonSizer, border=20, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM)
		mainSizer.Fit(panel)
		self.SetSizer(mainSizer)
		self.edit.SetFocus()
		# Translators: The title of the text field that contains the clipboard content.
		self.title.SetLabel(_("Clipboard text."))
		self.edit.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.edit.SetValue(pyperclip.paste())

	def onOk(self, evt):
		self.Hide()
		pyperclip.copy(self.edit.GetValue())

	def onKeyDown(self, evt):
		# Adapted from source/gui/logViewer.py.
		key = evt.GetKeyCode()
		if key == wx.WXK_ESCAPE:
			self.Hide()
			return
		evt.Skip()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(globalPluginHandler.GlobalPlugin, self).__init__(*args, **kwargs)
		settingsDialogs.NVDASettingsDialog.categoryClasses.append(CliptoolsPanel)

	@script(
		gesture="kb:NVDA+e",
		# Translators: The help message to be spoken for pressing NVDA+E in input help mode.
		description=_("View and edit the current clipboard content.")
	)
	def script_editClipboardText(self, gesture):
		d = ClipDialog()
		gui.mainFrame.prePopup()
		d.Raise()
		d.Maximize()
		d.Show()
		gui.mainFrame.postPopup()

	@script(
		gesture="kb:NVDA+shift+c",
		# Translators: The help message to be spoken when NVDA+Shift+C is pressed in input help.
		description=_("Clears the clipboard of all it's content.")
	)
	def script_clearClipboard(self, gesture):
		beeps = config.conf["cliptools"]["beeps"]
		if pyperclip.paste() != "":
			pyperclip.copy("")
			if beeps:
				tones.beep(350, 75)
			# Translators: The message to be spoken when the clipboard is cleared.
			ui.message(_("Clipboard cleared."))
		else:
			if beeps:
				tones.beep(150, 75)
			# Translators: The message to be spoken if the clipboard is already empty.
			ui.message(_("The clipboard is already empty."))

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		settingsDialogs.NVDASettingsDialog.categoryClasses.remove(CliptoolsPanel)
