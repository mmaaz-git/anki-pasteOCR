# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
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

# Function to be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)

# # create a new menu item, "test"
# action = QAction("test", mw)
# # set it to call testFunction when it's clicked
# action.triggered.connect(testFunction)
# # and add it to the tools menu
# mw.form.menuTools.addAction(action)

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

    # editor.doPaste("Maaz is cool", internal=False, extended=False)
    #editor.web.eval("wrap('<del>', '</del>');")

def addMyButton(buttons, editor):
    editor._links['strike'] = onStrike
    key = QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_V)
    keyStr = key.toString(QKeySequence.NativeText)
    return buttons + [editor.addButton(
        icon=str(DIR / "clipboard.png"),
        func=onStrike,
        cmd="strike", # link name
        tip="Paste image as text ({})".format(keyStr),
        keys=key.toString(QKeySequence.PortableText),
        disables=False)]

def path_to_tesseract():
    exec_data = {"Windows": str(DIR / "deps/win/tesseract/tesseract.exe"),
        "Darwin": "/usr/local/bin/tesseract",
        "Linux": "/usr/local/bin/tesseract"}
    platform_name = platform.system()  # E.g. 'Windows'
    return exec_data[platform_name]
# def addMyShortcut(cuts, editor):
#     editor.cuts.append(("Ctrl+Shift+V", onStrike))


addHook("setupEditorButtons", addMyButton)
pytesseract.pytesseract.tesseract_cmd=path_to_tesseract()
# gui_hooks.editor_did_init_shortcuts.append(addMyShortcut)