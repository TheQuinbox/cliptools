# cliptools

An NVDA add-on for managing the clipboard.

## Building

Simply compress to a zip, and rename to .nvda-addon.

## Building documentation

```batch
cd doc
cd en
pandoc -d options.yaml
```

## Todo

* Add automatic reading of clipboard content changes.
* Reimplement clipcopy directly into this addon.
* Add messages after pressing the OK button in the editor.
