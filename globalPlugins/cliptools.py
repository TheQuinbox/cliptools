# A part of cliptools.
# Copyright (C) 2021, Quin Marilyn. All rights reserved.
# GPL3 License.

import globalPluginHandler
from scriptHandler import script
import api
import wx

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(gesture="kb:NVDA+e", description="View and edit the current clipboard content.")
	def script_editClipboardText(self, gesture):
		api.copyToClip("test.")
