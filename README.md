# pasteOCR - an Anki addon

This is an addon for the flashcard program Anki which allows you to paste images as text using optical character recognition (OCR).

It makes using screenshots of lecture slides or textbooks to make cards a breeze!

## Usage

Once installed, you will notice a button on the left.

![showingbutton](readmefiles/showingbutton.png)

If you have an image in your clipboard, say after taking a screenshot, clicking the button will extract text from the image and paste it. 

You can also use the keyboard shortcut for convenience: `Ctrl + Alt + V` on Windows or `Cmd + Alt + V` on Mac.

## Installation

pasteOCR uses the Tesseract OCR engine, a powerful OCR engine currently maintained by Google. More on Tesseract [here](https://opensource.google/projects/tesseract).

If you are using Windows, the Tesseract binaries are included with the addon.

If you are using Mac OSX, you will have to install Tesseract to your computer. The easiest way to do this is to install Homebrew. Open the terminal and run the following command:

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`

Once that's installed, run the following command:

`brew install tesseract`

Once Tesseract is ready to go, you can install the addon to Anki within the program, using the installation code: `1746010116`.

## Attributions

- This addon depends on the Tesseract engine, distributed under the Apache 2.0 license. [Link](https://github.com/tesseract-ocr/tesseract).
- I benefitted enormously from the code provided by Chris Culhane for his AnkiOCR addon ([github](https://github.com/cfculhane/AnkiOCR)) while figuring out some quirks with Tesseract.
- The icon for the button is courtesy of [Flaticon.com](flaticon.com).

## License

This code is distributed under the GNU General Public License v3.0.