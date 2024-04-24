import base64

def encode(data):
    try:
        # Standard Base64 Encoding
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        return str(encodedBytes, "utf-8")
    except:
        return ""
    
def decode(data):
    try:
        message_bytes = base64.b64decode(data)
        return message_bytes.decode('utf-8')
    except:
        return ""

code = encode(r"""
                         
import os, sys
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox)

basedir = os.path.dirname(__file__)  # set a path as the same directory
os.chdir(basedir)  # change the working directory to the same directory

# this block ensures that the ICON is displayed on the taskbar in Windows
try:
    from ctypes import windll
    my_appid = 'com.asteng88.tolerancehelper.tolerancehelper.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_appid)
except ImportError:
    pass

class UiMainWindow(QMainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()
        ui = os.path.join(basedir, 'tolerance.ui') #set the path for the UI file
        uic.loadUi(ui, self) # load the UI file

        # Connect signals to slots
        self.aboutButton = self.findChild(QtWidgets.QToolButton, 'aboutButton')
        self.upperTolLCD = self.findChild(QtWidgets.QLCDNumber, 'lower_tolerance_out')
        self.lowerTolLCD = self.findChild(QtWidgets.QLCDNumber, 'upper_tolerance_out')
        self.nominalLCD = self.findChild(QtWidgets.QLCDNumber, 'nominal_out')
        self.lowerTolInput = self.findChild(QtWidgets.QLineEdit, 'lower_tolerance_in')
        self.lowerTolInput.textChanged.connect(self.addLowTolNomTol)
        self.upperTolInput = self.findChild(QtWidgets.QLineEdit, 'upper_tolerance_in')
        self.upperTolInput.textChanged.connect(self.addUppTolNomTol)
        self.nominalInput = self.findChild(QtWidgets.QLineEdit, 'nominal_in')
        self.nominalInput.textChanged.connect(self.enterNominal)
        self.measurementInput = self.findChild(QtWidgets.QLineEdit, 'measurement_in')
        self.outputLabel = self.findChild(QtWidgets.QLabel, 'output_label')
        self.quitButton = self.findChild(QtWidgets.QPushButton, 'quitButton')
        self.quitButton.clicked.connect(self.quitAction)
        self.clearText = self.findChild(QtWidgets.QPushButton, 'clearTextButton')
        self.clearText.clicked.connect(self.clearTextAction)
        self.calculateButton = self.findChild(QtWidgets.QPushButton, 'calculateButton')
        self.calculateButton.clicked.connect(self.calculateTolerance)
        self.aboutButton.clicked.connect(self.aboutAction)
        self.clearMeasurementButoon = self.findChild(QtWidgets.QPushButton, 'clearMeasurementButton')
        self.clearMeasurementButoon.clicked.connect(self.clearMeasurement)
        
    
    def enterNominal(self, text):
        try:
            if text.startswith("."):
                text = "0" + text
                self.nominalInput.setText(text)
            else:
                text = str(round(float(text), 3))  # Round the text to 3 decimal places
                self.nominalLCD.display(text)
                return
        except ValueError:
            return
    
    def addUppTolNomTol(self, text):
        try:
            if text.startswith("."):
                text = "0" + text
                round(float(text),3)
                self.upperTolInput.setText(text)  
            else:
                addUpper = round(float(self.nominalInput.text()) + float(text),3)
                self.upperTolLCD.display(addUpper)
                return
        except ValueError:
            return
            
    def addLowTolNomTol(self, text):
        try:
            if text.startswith("."):
                text = "0" + text
                round(float(text),3)
                self.lowerTolInput.setText(text)
            else:
                addLower = round(float(self.nominalInput.text()) - float(text),3)
                self.lowerTolLCD.display(addLower)
                return
        except ValueError:
            return
    
    def quitAction(self):
         QApplication.quit()
         return
    
    def resetStyle(self):
        for lcd in (self.upperTolLCD, self.lowerTolLCD, self.nominalLCD):
            lcd.setStyleSheet("color: black; background-color: lightgrey")
        for inputs in (self.upperTolInput, self.lowerTolInput, self.nominalInput, self.measurementInput, self.outputLabel):
            inputs.setStyleSheet("color: black; background-color: white")
        return
    
    def clearTextAction(self):
        for inputs in (self.upperTolInput, self.lowerTolInput, self.nominalInput, self.measurementInput):
            inputs.setText("")
        self.outputLabel.clear()
        self.resetStyle()
        for lcd in (self.upperTolLCD, self.lowerTolLCD, self.nominalLCD):
            lcd.display(0)
        self.nominalInput.setFocus()
        return     
    
    def clearMeasurement(self):
        self.measurementInput.clear()
        self.outputLabel.clear()
        self.resetStyle()
        self.measurementInput.setFocus()
        return

    def aboutAction(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Tolerance Helper V1.0")
        msg.setInformativeText('This is a simple tolerance calculator that \nchecks if a measurement is within tolerance.\n\nWritten by Andrew Thomas. \n\nPlease report or fix any bugs at: \nhttps://github.com/asteng88/tolerance_helper.')
        msg.setWindowTitle("About Tolerance Helper")
        msg.setWindowIcon(QIcon(icon_1))
        msg.exec()
        return

    def calculateTolerance(self):
        try:
            upperTolTotal = round(float(self.nominalInput.text()) + float(self.upperTolInput.text()), 3)
            lowerTolTotal = round(float(self.nominalInput.text()) - float(self.lowerTolInput.text()), 3)
            self.upperTolLCD.display(upperTolTotal)
            self.lowerTolLCD.display(lowerTolTotal)
            self.nominalLCD.display(self.nominalInput.text())
        
            # Check if the measurement is within the tolerance
            measurement = round(float(self.measurementInput.text()), 3)
            if measurement <= upperTolTotal and measurement >= lowerTolTotal:
                for setGreen in (self.outputLabel, self.upperTolLCD, self.lowerTolLCD, self.measurementInput):
                    setGreen.setStyleSheet("color: black; background-color: lightgreen")
                self.outputLabel.setText('Measurement is within tolerance')
            else:
                self.outputLabel.setStyleSheet("color: black; background-color: pink")
                self.outputLabel.setText('Measurement is NOT within tolerance')
                self.measurementInput.setStyleSheet("color: black; background-color: pink")
                if measurement > upperTolTotal:
                    self.upperTolLCD.setStyleSheet("color: black; background-color: pink")
                else:
                    self.upperTolLCD.setStyleSheet("color: black; background-color: lightgreen")
                if measurement < lowerTolTotal:
                    self.lowerTolLCD.setStyleSheet("color: black; background-color: pink")
                else:
                    self.lowerTolLCD.setStyleSheet("color: black; background-color: lightgreen")
            #return
    
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText('Please ensure ALL fields are complete and are numeric')
            msg.setWindowTitle("Error: Input Error")
            msg.setWindowIcon(QIcon(icon_1))
            msg.exec()
        return

app = QApplication(sys.argv)
window = UiMainWindow()
icon_1 = os.path.join(basedir, 'toleranceicon.png')
window.setWindowIcon(QIcon(icon_1))
window.show()
app.exec()

""")
exec(decode(code))
