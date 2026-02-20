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
from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("My First PySide6 App")
window.resize(400, 300)
window.show()

sys.exit(app.exec())
