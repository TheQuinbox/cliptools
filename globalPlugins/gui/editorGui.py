# A part of cliptools.
# Copyright (C) 2021, Quin Marilyn. All rights reserved.
# This code is GPL. See NVDA's license.
# All of NVDA's license and copying conditions apply here,
# including the waranty disclosure.
#
# Some GUI code adapted from the Tip-of-the-day add-on by Derek Riemer.

import wx
import gui
import api


class ClipDialog(wx.Dialog):
	def __init__(self):
		super(ClipDialog, self).__init__(
			gui.mainFrame,
			wx.ID_ANY,
			# Translators: The title of the main cliptools dialog.
			title=_("Cliptools")
		)
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
		self.edit.SetValue(api.getClipData())
		self.title.SetLabel(
			# Translators: The title of the text field
			# that contains the content of the users clipboard.
			_("Clipboard text.")
		)

	def onOk(self, evt):
		self.Hide()
		api.copyToClip(self.edit.GetValue())
