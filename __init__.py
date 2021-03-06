# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *
from anki.hooks import addHook
from aqt import gui_hooks

from . import pytesseract

import tempfile
import os
import platform
from pathlib import Path

DIR = Path(__file__).parent

def onStrike(editor):
    if editor.mw.app.clipboard().mimeData().hasImage():
        image = QImage(editor.mw.app.clipboard().mimeData().imageData())
        image.save("ocrtmp.png")
        path = os.path.abspath("ocrtmp.png")
        output = pytesseract.image_to_string(path).replace("\n", "<br>")
        editor.doPaste(output, internal=False, extended=False)
        os.remove(path)
    else:
        editor.onPaste()

def addMyButton(buttons, editor):
    editor._links['strike'] = onStrike
    key = QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_V)
    keyStr = key.toString(QKeySequence.NativeText)
    return buttons + [editor.addButton(
        icon=str(DIR / "clipboard.png"),
        func=onStrike,
        cmd="strike",
        tip="Paste image as text ({})".format(keyStr),
        keys=key.toString(QKeySequence.PortableText),
        disables=False)]

def path_to_tesseract():
    exec_data = {"Windows": str(DIR / "deps/win/tesseract/tesseract.exe"),
        "Darwin": "/usr/local/bin/tesseract",
        "Linux": "/usr/local/bin/tesseract"}
    platform_name = platform.system()  # E.g. 'Windows'
    return exec_data[platform_name]


addHook("setupEditorButtons", addMyButton)
pytesseract.pytesseract.tesseract_cmd=path_to_tesseract()