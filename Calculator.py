import sys
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from functools import partial

ERROR_MSG = 'ERROR'


class PyCalculatorUi(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dev Calculator")
        self.setFixedSize(250, 250)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        # Create Display widget
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
    # Positions of buttons on layout
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                   }
    # Create the Buttons and add items to grid layout
        for btn, pos in buttons.items():
            self.buttons[btn] = QPushButton(btn)
            self.buttons[btn].setFixedSize(40, 40)
            buttonsLayout.addWidget(self.buttons[btn], pos[0], pos[1])
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)      # .setText displays text
        self.display.setFocus()

    def displayText(self):
        return self.display.text()       # .text gives the text written in field

    def clearDisplay(self):
        self.setDisplayText('')


class PyCalculatorControl:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignals()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        # building an expression in string to later evaluate
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        for btntext, btn in self._view.buttons.items():
            if btntext not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btntext))
            self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
            self._view.buttons['='].clicked.connect(self._calculateResult)
            self._view.display.returnPressed.connect(self._calculateResult)


def evaluateExpression(expression):

    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


pycalc = QApplication(sys.argv)
view = PyCalculatorUi()
view.show()
model = evaluateExpression
PyCalculatorControl(model=model, view=view)

sys.exit(pycalc.exec_())
