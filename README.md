# cliptools

An NVDA add-on for managing the clipboard.

## Keys

* NVDA+E: Bring up the clipboard editor. From here, you can read and edit the text on your clipboard. When done, press the OK button.
* NVDA+shift+c: Clear the clipboard of all it's content. Because of a bug in NVDA, this currently coppies a single space to the  clipboard, but it's still empty for all means and purposes. This will be fixed later.

## Todo

* Add automatic reading of clipboard content changes.
* Reimplement clipcopy directly into this addon.
* Figure out why api.copyToClip doesn't copy if you just pass a blank string.
