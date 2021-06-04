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
import tones
import config
from gui import guiHelper, settingsDialogs
from . import pyperclip
import speech
from logHandler import log

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
		self.edit.SetValue(pyperclip.paste())

	def onOk(self, evt):
		beeps = config.conf["cliptools"]["beeps"]
		self.Hide()
		pyperclip.copy(self.edit.GetValue())
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
		self.lastSpeech = "This is a test"
		self.oldSpeak = speech.speak
		speech.speak = self.mySpeak

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
		speech.speak = self.oldSpeak

	@script(
		gesture="kb:f12",
		# Translators: The description spoken when f12 is pressed in input help mode.")
		description=_("Coppies the last spoken text to the clipboard.")
	)
	def script_copyLast(self, gesture):
		pyperclip.copy(self.lastSpeech)
		log.debugWarning(f"This should've worked? lastSpeech = {self.lastSpeech}.")
		tones.beep(1500, 120)

	def mySpeak(self, text, *args, **kwargs):
		self.lastSpeech = text
		self.oldSpeak(text, *args, **kwargs)
