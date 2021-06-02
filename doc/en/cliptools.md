# Cliptools - Readme.

## Introduction.

Cliptools is an NVDA add-on that allows you to manage your clipboard in various ways. A lot is planned for this add-on, and I'm always looking for suggestions!

### Current features.

Currently, cliptools can do the following:

* Clear the clipboard of all it's content
* Edit the text currently on your clipboard.

### Keys

* NVDA + E: Edit the text that's currently on your clipboard. To abort, press escape. When done, press the OK button.
* NVDA + Shift + C: Clear the text currently on your clipboard. If your clipboard is already empty, you are told.

## Configuration

* Beep when certain events are preformed: Beeps when clearing the clipboard. If it's already cleared, the beep you hear is lower pitched.

## Contributing

I welcome all contributions. It is prefered that you open an issue before filing pull requests, but I won't require it. A template for pull requests and issues should be coming soon!

### Linting your changes.

Before submitting pull requests, please run the following

```batch
flake8 --config=flake8.ini globalPlugins/cliptools/__init__.py
```

If you get no errors, feel free to push!
