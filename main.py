##########################
# "The Count" for MIPS   #
# A small MIPS assembler #
# By iamkillroy (Lucas F)#
#    MIT License 2.0     #
##########################

###########
# MODULES #
###########
import sys
from PySide6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton
import mipsconvert

class Window:
    def __init__(self) -> None:
        """Creates a Window object"""
        self.app = QApplication(sys.argv)

        #define window parent behavior
        self.window = QWidget()
        self.window.setWindowTitle("The Count! for MIPS")
        self.window.show()

        #input box
        self.mipsInputBox = QTextEdit()
        self.mipsInputBox.setPlaceholderText("Put MIPS here!")

        #convert button
        self.convertButton = QPushButton("Convert to hex!")
        self.convertButton.clicked.connect(self.convertUpdate)
        #input box
        self.hexOutputBox = QTextEdit()
        self.hexOutputBox.setPlaceholderText("Output will be here...")

        #Add GUI elements
        layout = QVBoxLayout()
        layout.addWidget(self.mipsInputBox)
        layout.addWidget(self.convertButton)
        layout.addWidget(self.hexOutputBox)
        self.window.setLayout(layout)
        sys.exit(self.app.exec())
    def convertUpdate(self):
        """Converts the input to MIPS assembly"""
        commandsInString = self.mipsInputBox.toPlainText()
        commandsInList = commandsInString.split("\n")
        newOutputString = ""
        for command in commandsInList:
            if len(command) == 0:
                continue
            hexOut = mipsconvert.convert(command)
            newOutputString = newOutputString + f"0x{hexOut:08x}" + "\n"


        self.hexOutputBox.setText(newOutputString)
Window()
