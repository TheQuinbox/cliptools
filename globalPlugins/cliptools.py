# A part of cliptools.
# Copyright (C) 2021, Quin Marilyn. All rights reserved.
# This code is GPL. See NVDA's license.
# All of NVDA's license and copying conditions apply here, including the waranty disclosure.

import globalPluginHandler
from scriptHandler import script
import api
import wx
import gui


class ClipDialog(wx.Dialog):
	def __init__(self):
		super(ClipDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title="Cliptools")
		self.panel  = panel = wx.Panel(self, wx.ID_ANY)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		clipSizer = wx.BoxSizer(wx.VERTICAL)
		self.title = item = wx.StaticText(panel)
		clipSizer.Add(item)
		self.edit = item = wx.TextCtrl(panel, size = (500,500), style=wx.TE_MULTILINE)
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
		self.edit.SetValue(api.getClipData())

	def onOk(self, evt):
		self.Hide()
		api.copyToClip(self.edit.GetValue())


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
