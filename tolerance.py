# Tolerance Helper 
# @author: Andrew Thomas
# @date: 2023-12-13
# @description: A simple tool to help calculate tolerances and check if a measurement is within tolerance
# @license: GNU GPL v3
# @version: 1.1

import os, sys
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

basedir = os.path.dirname(__file__)  # set a path as the same directory as this file
os.chdir(basedir)  # change the working directory to the same directory as this file

# this block ensures that the ICON is displayed on the taskbar in Windows
try:
    from ctypes import windll

    my_appid = 'com.laserslayer.tolerancehelper.tolerancehelper.1.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_appid)
except ImportError:
    pass

class UiMainWindow(QMainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()
        ui = os.path.join(basedir, 'tolerance.ui') #set the path for the UI file
        uic.loadUi(ui, self) # load the UI file

        # Connect signals to slots
        self.upperTolLCD = self.findChild(QtWidgets.QLCDNumber, 'lower_tolerance_out')
        self.lowerTolLCD = self.findChild(QtWidgets.QLCDNumber, 'upper_tolerance_out')
        self.nominalLCD = self.findChild(QtWidgets.QLCDNumber, 'nominal_out')
        self.lowerTolInput = self.findChild(QtWidgets.QLineEdit, 'lower_tolerance_in')
        self.lowerTolInput.textChanged.connect(self.addLotTolNomTol)
        self.upperTolInput = self.findChild(QtWidgets.QLineEdit, 'upper_tolerance_in')
        self.upperTolInput.textChanged.connect(self.addUppTolNomTol)
        self.nominalInput = self.findChild(QtWidgets.QLineEdit, 'nominal_in')
        self.measurementInput = self.findChild(QtWidgets.QLineEdit, 'measurement_in')
        self.outputLabel = self.findChild(QtWidgets.QLabel, 'output_label')
        self.quitButton = self.findChild(QtWidgets.QPushButton, 'quitButton')
        self.quitButton.clicked.connect(self.quitAction)
        self.clearText = self.findChild(QtWidgets.QPushButton, 'clearTextButton')
        self.clearText.clicked.connect(self.clearTextAction)
        self.calculateButton = self.findChild(QtWidgets.QPushButton, 'calculateButton')
        self.calculateButton.clicked.connect(self.calculateTolerance)
        self.clearMeasurementButoon = self.findChild(QtWidgets.QPushButton, 'clearMeasurementButton')
        self.clearMeasurementButoon.clicked.connect(self.clearMeasurement)
        
    def addUppTolNomTol(self, text):
        if text.startswith("."):
            text = "0" + text
            self.upperTolInput.setText(text)
        try:
            addupper = float(text) + float(self.nominalInput.text())
            self.upperTolLCD.display(addupper)
            calcUpperTol = addupper
        except ValueError:
            pass

    def addLotTolNomTol(self, text):
        if text.startswith("."):
            text = "0" + text
            self.lowerTolInput.setText(text)
        try:
            addlower = float(self.nominalInput.text()) - float(text)
            self.lowerTolLCD.display(addlower)
            calcLowerTol = addlower
        except ValueError:
            pass

    def quitAction(self):
         QApplication.quit()
         return
    
    def resetLCDstyle(self):
        self.upperTolLCD.setStyleSheet("color: black")
        self.lowerTolLCD.setStyleSheet("color: black")
        self.nominalLCD.setStyleSheet("color: black")
        return
    
    def clearTextAction(self):
        self.upperTolInput.clear()
        self.lowerTolInput.clear()
        self.nominalInput.clear()
        self.measurementInput.clear()
        self.outputLabel.clear()
        self.resetLCDstyle()
        self.upperTolLCD.display(0)
        self.lowerTolLCD.display(0)
        self.nominalLCD.display(0)
        return     
    
    def clearMeasurement(self):
        self.measurementInput.clear()
        self.outputLabel.clear()
        self.resetLCDstyle()
        return

    def calculateTolerance(self):
        if (not self.upperTolInput.text() or not self.lowerTolInput.text() or not self.nominalInput.text() or not self.measurementInput.text()):
            self.outputLabel.setStyleSheet("color: black")
            self.outputLabel.setText('Please enter all values')
            return
        else:
            upperTolTotal = float(self.nominalInput.text()) + float(self.upperTolInput.text())
            lowerTolTotal = float(self.nominalInput.text()) - float(self.lowerTolInput.text())
            self.upperTolLCD.display(upperTolTotal)
            self.lowerTolLCD.display(lowerTolTotal)
            self.nominalLCD.display(self.nominalInput.text())
            
            # Check if the measurement is within the tolerance
            if float(self.measurementInput.text()) <= upperTolTotal and float(self.measurementInput.text()) >= lowerTolTotal:
                self.outputLabel.setStyleSheet("color: green")
                self.upperTolLCD.setStyleSheet("color: green")
                self.lowerTolLCD.setStyleSheet("color: green")
                self.outputLabel.setText('Measurement is within tolerance')
            else:
                self.outputLabel.setStyleSheet("color: red")
                self.outputLabel.setText('Measurement is NOT within tolerance')
                if float(self.measurementInput.text()) > upperTolTotal:
                    self.upperTolLCD.setStyleSheet("color: red")
                else:
                    self.upperTolLCD.setStyleSheet("color: green")
                if float(self.measurementInput.text()) < lowerTolTotal:
                    self.lowerTolLCD.setStyleSheet("color: red")
                else:
                    self.lowerTolLCD.setStyleSheet("color: green")
        return

app = QApplication(sys.argv)
window = UiMainWindow()
icon_1 = os.path.join(basedir, 'toleranceicon.png')
window.setWindowIcon(QIcon(icon_1))
window.show()
app.exec()