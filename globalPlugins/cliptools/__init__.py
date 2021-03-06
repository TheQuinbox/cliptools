# A part of cliptools.
# Copyright (C) 2021-2022, Quin Marilyn. All rights reserved.
# This code is GPL. See NVDA's license.
# All of NVDA's license and copying conditions apply here,
# including the warranty disclosure.
#
# Some GUI code adapted from the Tip-of-the-day add-on by Derek Riemer.

import globalPluginHandler
from scriptHandler import script
import gui
import ui
import wx
import tones
import config
from gui import guiHelper, settingsDialogs
from . import clip_handler

confspec = {
	"beeps": "boolean(default=False)"
}
config.conf.spec["cliptools"] = confspec


class CliptoolsPanel(gui.SettingsPanel):
	# Translators: The title of the Cliptools settings dialog.
	title = _("Cliptools")

	def makeSettings(self, sizer):
		helper = guiHelper.BoxSizerHelper(self, sizer=sizer)
		# Translators: The title of the check box for beeps in Cliptools.
		self.smBeeps = helper.addItem(wx.CheckBox(self, label=_("&Beep when certain events are preformed")))
		self.smBeeps.SetValue(config.conf["cliptools"]["beeps"])

	def onSave(self):
		config.conf["cliptools"]["beeps"] = self.smBeeps.IsChecked()


class ClipboardEditorDialog(wx.Dialog):
	def __init__(self):
		# Translators: The title of the dialog that pops up when the user presses NVDA+E.
		super(ClipboardEditorDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title=_("Cliptools"))
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
		item = wx.Button(panel, wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON, self.onCancel, item)
		mainSizer.Add(buttonSizer, border=20, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM)
		mainSizer.Fit(panel)
		self.SetSizer(mainSizer)
		self.edit.SetFocus()
		# Translators: The title of the text field that contains the clipboard content.
		self.title.SetLabel(_("Clipboard text."))
		self.edit.SetValue(clip_handler.get_text())

	def onOk(self, evt):
		beeps = config.conf["cliptools"]["beeps"]
		self.Hide()
		clip_handler.set_text(self.edit.GetValue())
		if beeps:
			tones.beep(350, 75)
		# Translators: The message spoken when the clipboard content is set successfully.
		ui.message(_("Text set!"))

	def onCancel(self, evt):
		beeps = config.conf["cliptools"]["beeps"]
		self.Hide()
		# Translators: The message spoken when clipboard editing is canceled.
		if beeps:
			tones.beep(150, 75)
		ui.message(_("Canceled."))
		return


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
		d = ClipboardEditorDialog()
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
		if clip_handler.get_text() != "":
			clip_handler.set_text("")
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
