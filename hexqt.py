# hexqt.py -- HexQT a pretty QT hext editor.

import sys, os
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QAction, QMainWindow, QFileDialog, QGridLayout, QGroupBox, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, pyqtSlot

class FileSelector(QFileDialog):
    def __init__(self):
        super().__init__()

        self.selectFile()      
        self.show()

    def selectFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Directory View", "","All Files (*)", options=options)
        
        self.fileName = fileName
        

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window options!
        self.title = 'HexQT'
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 480
        self.initUI()

    def readFile(self, fileName):
        fileData = ''
        
        with open(fileName, 'r') as fileObj:
            fileData = fileObj.read()

        options = {
            'rowSpacing': 4,
            'rowLength': 16
        }

        text = generateView(fileData, options)
        
        self.textArea.setText(text)

    def openFile(self):
        fileSelect = FileSelector()
        fileName = fileSelect.fileName

        self.readFile(fileName)

    def createMainView(self):
        self.textArea = QTextEdit()

        return self.textArea

    def initUI(self):
        # Initialize basic window options.
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar() # Creates a menu bar, (file, edit, options, etc...)

        # Menus for window.
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        helpMenu = mainMenu.addMenu('Help')

        # Open menu.
        openButton = QAction(QIcon(), 'Open', self)
        openButton.setShortcut('Ctrl+O')
        openButton.setStatusTip('Open file')
        openButton.triggered.connect(self.openFile)

        # Optional exit stuff.
        exitButton = QAction(QIcon(), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        
        fileMenu.addAction(openButton)
        fileMenu.addAction(exitButton)

        # Creating a groupbox layout.
        
        gBox = QGroupBox()

        qLayout = QHBoxLayout()
        qLayout.addWidget(self.createMainView())
        
        gBox.setLayout(qLayout)
        self.setCentralWidget(gBox)

        # Show our masterpiece.
        self.show()

# generateView ... Generates text view for hexdump likedness.
def generateView(text, options):
    space = ' ' * 4
    offset = 0x00000000
    newText = format(offset, '08x') + space # Format to print hex properly.
    asciiText = ''

    rowSpacing = options['rowSpacing']
    rowLength = options['rowLength']

    for chars in range(0, len(text)):
        char = text[chars]
        newText += format((ord(char)), '02x') +  '  ' # Format the hex to maintain max of 0x00 and 0xff.

        if char is ' ':
            asciiText += '.'
        
        else:
            asciiText += repr(char).replace('\'', '')

        if (chars + 1) % rowSpacing is 0:
            newText += '  '

        if (chars + 1) % rowLength is 0:
            offset += rowLength
            newText += space + asciiText + '\n\n' + format(offset, '08x') + space
            
            asciiText = ''

    return newText

# setStyle ... Sets the style of the QT Application.
def setStyle(qApp):
    qApp.setStyle("Fusion")

    dark_palette = QPalette()

    white = QColor(255, 255, 255)
    red = QColor(255, 0, 0)
    black = QColor(0, 0, 0)

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.white)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    font = QFont("DejaVu Sans Mono", 12, QFont.Normal, True)

    qApp.setFont(font)
    qApp.setPalette(dark_palette)

    qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

def main():
    app = QApplication(sys.argv)
    setStyle(app)
    
    hexqt = App()
    sys.exit(app.exec_())

# Initialize the brogram.
if __name__ == '__main__':
    main()