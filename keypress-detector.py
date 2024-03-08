# -*- coding: utf-8 -*-

# Example code combining PySide QTimer thread with pynput keyboard input event
# handler, resulting in the following error:
# 
# QObject::startTimer: Timers can only be used with threads started with QThread
#
# To make the error go away, swap comments on lines 36 & 37.
#
# Originally derived from pynput author's example code
# Source: MacOS crash when starting pynput keyboard listener after qt6
# Link: https://github.com/moses-palmer/pynput/issues/511


from pynput import keyboard
from PySide6 import QtWidgets, QtCore

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
    
        # Create minimal GUI to test keypresses affecting GUI state
        #
        self.setWindowTitle("Qt App Demo w/Keypress Detector")
        self.label = QtWidgets.QLabel()
        self.label.setText("This label will indicate which key is pressed")
        self.setCentralWidget(self.label)
        self.show()
        self.setup_keypress_listener()
    
    def key_pressed(self, msg):
       '''
       Respond to key pressed by displaying a message in the Qt label,
       Use a QTimer delay to demo thread conflict problem.
       '''
       QtCore.QTimer.singleShot(100, lambda : self.set_label(msg))
       #self.set_label(msg)

    def set_label(self, msg):
        self.label.setText(msg)

    def setup_keypress_listener(self):

        def on_press(key):
            try:
                dummy = key.char  # Causes exception for special keypresses
                self.key_pressed(f'basic key {key} pressed\n')
            except AttributeError:
                self.key_pressed(f'special key {key} pressed\n')

        def on_release(key):
            pass    # Ignore key releases for now

        self.listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        self.listener.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main = Main()
    app.exec()

