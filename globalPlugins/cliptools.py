# A part of cliptools.
# Copyright (C) 2021, Quin Marilyn. All rights reserved.
# This code is GPL. See NVDA's license.
# All of NVDA's license and copying conditions apply here,
# including the waranty disclosure.
#
# Some GUI code adapted from the Tip-of-the-day add-on by Derek Riemer.

import globalPluginHandler
from scriptHandler import script
from .interface import editorGui
import gui
import api
import ui
from logHandler import log


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(
		gesture="kb:NVDA+e",
		description=_("View and edit the current clipboard content.")
	)
	def script_editClipboardText(self, gesture):
		d = editorGui.ClipDialog()
		gui.mainFrame.prePopup()
		d.Raise()
		d.Maximize()
		d.Show()
		gui.mainFrame.postPopup()

	@script(gesture="kb:NVDA+shift+c", description="Clears the clipboard of all it's content.")
	def script_clearClipboard(self, gesture):
		if api.getClipData() != "":
			ui.message("Clipboard cleared.")
			api.copyToClip(" ")
		else:
			ui.message("Clipboard already empty.")
