# clip_handler
# Read and set the clipboard text natively on Windows, no third-party libraries required.
#
# Copyright (C) 2022, Quin Marilyn. All rights reserved.
# GPL license.
#
# Originally a part of Cliptools.

import ctypes

strcpy = ctypes.cdll.msvcrt.strcpy
OpenClipboard = ctypes.windll.user32.OpenClipboard
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
GetClipboardData = ctypes.windll.user32.GetClipboardData
SetClipboardData = ctypes.windll.user32.SetClipboardData
CloseClipboard = ctypes.windll.user32.CloseClipboard
GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock

GMEM_DDESHARE = 0x2000
CF_TEXT = 1


def get_text():
	OpenClipboard(None)
	pcontents = GetClipboardData(CF_TEXT)
	data = ctypes.c_char_p(pcontents).value
	CloseClipboard()
	if data is None: data = ""
	try:
		return data.decode()
	except UnicodeDecodeError:
		return data.decode("raw_unicode_escape")


def set_text(data):
	OpenClipboard(None)
	EmptyClipboard()
	hdata = GlobalAlloc(GMEM_DDESHARE, len(bytes(data, "ascii")) + 1)
	pch_data = GlobalLock(hdata)
	strcpy(ctypes.c_char_p(pch_data), bytes(data, "ascii"))
	GlobalUnlock(hdata)
	SetClipboardData(1, hdata)
	CloseClipboard()
