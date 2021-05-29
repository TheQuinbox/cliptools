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


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(
		gesture="kb:NVDA+e",
		# Translators: The description that's spoken when
		# the user presses the key in help mode.
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
		# For some reason, api.copyToClip doesn't copy if we pass a blank string, so pass a space. Need to fix this.
		api.copyToClip(" ")
