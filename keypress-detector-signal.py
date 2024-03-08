# -*- coding: utf-8 -*-

# Example code combining PySide Qt event loop with pynput keyboard input event loop

# Using Signal to enable pynput thread to communicate events to PyQt threads

# Originally derived from:
# MacOS crash when starting pynput keyboard listener after qt6
# Link: https://github.com/moses-palmer/pynput/issues/511


from pynput import keyboard
from PySide6 import QtWidgets, QtCore


class KeySignal(QtCore.QObject):
    '''
    Signal class to communicate pynput keyboard detection thread events to
    QT GUI thread process methods, while avoiding hangups and errors due to
    direct calls from one type of thread to another.
    '''
    pressed = QtCore.Signal(str)   # Note: this is a class variable

    def __init__(self):
        # Initialize KeySignal as QObject
        QtCore.QObject.__init__(self)
    
    def press(self, sigstr):
        ''' Emits signal for key press event '''
        self.pressed.emit(sigstr)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
    
        # Create minimal GUI to test that keypresses can affect GUI state & methods
        #
        self.setWindowTitle("Qt App Demo w/Keypress Detector")
        self.label = QtWidgets.QLabel()
        self.label.setText("This label will indicate which key is pressed")
        self.setCentralWidget(self.label)
        self.show()

        # Setup signal/slot connection
        self.key_signal = KeySignal()
        self.key_signal.pressed.connect(self.key_pressed)
    
    def key_pressed(self, msg):
       '''
       Respond to key pressed by displaying a message in the Qt label,
       Use a QTimer delay to demo thread conflict problem.
       '''
       QtCore.QTimer.singleShot(200, lambda : self.set_label(msg))
       #self.set_label(msg)

    def set_label(self, msg):
        self.label.setText(f"Pressed event, key={msg}")


    def setup_keypress_listener(self, ks_callback):

        self.ks_callback = ks_callback

        def on_press(key):
            try:
                dummy = key.char  # Causes exception for special keypresses
                self.ks_callback(key.char)
            except AttributeError:
                # Note: handle special keys here (ctrl, shift, etc.)
                self.ks_callback(f"{key}")

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
    main.setup_keypress_listener(ks_callback=main.key_signal.press)
    app.exec()

