from gui import UserInterface
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
ui = UserInterface()
sys.exit(app.exec_())

