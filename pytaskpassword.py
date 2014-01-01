from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSystemTrayIcon, QIcon, QAction, QMenu
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import subprocess
import sys
class Test(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Password")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.line1 = QLabel("Passsord", self)
        self.line2 = QLabel("Username", self)
        self.textUsername = QtGui.QLineEdit(self)
        self.textPassword = QtGui.QLineEdit(self)
        self.textPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.loginbuton = QtGui.QPushButton('Login', self)
        self.loginbuton.clicked.connect(self.Login)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.line2)
        layout.addWidget(self.textUsername)
        layout.addWidget(self.line1)
        layout.addWidget(self.textPassword)
        layout.addWidget(self.loginbuton)
        self._want_to_close = False
        
    def exitEvent(self):
        self.exitOnClose = True
        self.close()
    def closeEvent(self, evnt):
        if self._want_to_close:
            super(Test, self).closeEvent(evnt)
        else:
            evnt.ignore()
            pass

    def Login(self):
        if (self.textUsername.text() == 'admin' and
            self.textPassword.text() == 'password'):
            self.accept()
        else:
            QtGui.QMessageBox.warning(
                self, 'Access Denied', 'Incorrect user or password')
    def keyPressEvent(self, e):
        if e.key() in (QtCore.Qt.Key_Super_L, QtCore.Qt.Key_Super_R):
            pass
        if e.key() == QtCore.Qt.Key_Escape:
            pass
class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(.9)
        self.setStyleSheet("QMainWindow { background: 'black'}");        


def Main():
    app = QtGui.QApplication(sys.argv)
    myapp = MyWindow()
    myapp.setGeometry(app.desktop().screenGeometry())
    myapp.show()
    
    if Test().exec_() == QtGui.QDialog.Accepted:
            myapp.hide()
            

if __name__ == '__main__':
    Main()
