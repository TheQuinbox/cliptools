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


class ClipDialog(wx.Dialog):
	def __init__(self):
		super(ClipDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title="Cliptools")
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
		self.title.SetLabel("Clipboard text.")
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
	@script(
		gesture="kb:NVDA+e",
		description="View and edit the current clipboard content."
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
		description="Clears the clipboard of all it's content."
	)
	def script_clearClipboard(self, gesture):
		if pyperclip.paste() != "":
			pyperclip.copy("")
			ui.message("Clipboard cleared.")
		else:
			ui.message("The clipboard is already empty.")
