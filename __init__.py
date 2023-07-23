# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *
from anki.hooks import addHook
from aqt import gui_hooks

from . import pytesseract
#from .PIL import Image

import subprocess
import tempfile
import os
import platform
from pathlib import Path

DIR = Path(__file__).parent

def onStrike(editor):
    if editor.mw.app.clipboard().mimeData().hasImage():
        image = QImage(editor.mw.app.clipboard().mimeData().imageData())
        path = str(DIR / "ocrtemp.png")
        image.save(path)
        output = pytesseract.image_to_string(path, config=tesseract_config()).replace("\n", "<br>")
        os.remove(path)
        #pil_image = Image.fromqpixmap(image)
        #output = pytesseract.image_to_string(pil_image).replace("\n", "<br>")
        editor.doPaste(output, internal=False, extended=False)
    else:
        editor.onPaste()

def addMyButton(buttons, editor):
    editor._links['strike'] = onStrike
    key = QKeySequence(Qt.Modifier.CTRL | Qt.Modifier.ALT | Qt.Key.Key_V)
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
        "Darwin": str(DIR / "deps/mac/tesseract/4.1.1/bin/tesseract"),
        "Linux": "/usr/local/bin/tesseract"}
    platform_name = platform.system()  # E.g. 'Windows'
    return exec_data[platform_name]

def set_tesseract_exe_permission():
    if platform.system() == "Darwin":
        subprocess.Popen(["chmod", "+x", path_to_tesseract()])

def tesseract_config():
    config = ''
    if platform.system() == "Darwin":
        path = str(DIR / "deps/mac/tesseract/4.1.1/share/tessdata")
        config = f'--tessdata-dir "{path}"'
    return config

addHook("setupEditorButtons", addMyButton)
pytesseract.pytesseract.tesseract_cmd=path_to_tesseract()
set_tesseract_exe_permission()
