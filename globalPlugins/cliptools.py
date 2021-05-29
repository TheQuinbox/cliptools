# A part of cliptools.
# Copyright (C) 2021, Quin Marilyn. All rights reserved.
# This code is GPL. See NVDA's license.
# All of NVDA's license and copying conditions apply here,
# including the waranty disclosure.
#
# Some GUI code adapted from the Tip-of-the-day add-on by Derek Riemer.

import globalPluginHandler
from scriptHandler import script
from .gui import editorGui


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
