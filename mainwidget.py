from PySide import QtGui
from PySide import QtCore
import sys
import winCom
import ctypes

SetParent = ctypes.windll.user32.SetParent
SetWindowLong = ctypes.windll.user32.SetWindowLongW
GWL_STYLE = -16
WS_CHILD = 0x40000000
WS_CLIPCHILDREN = 0x02000000
WS_CLIPSIBLINGS = 0x04000000
GetWindowRect = ctypes.windll.user32.GetWindowRect

def get_hwnd_from_qt_widget(widget):
    ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    wdgt_ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(widget.winId())
    return wdgt_ptr

class MainWidget(QtGui.QWidget):
    def __init__(self, *args,**kwargs):
        super(MainWidget, self).__init__(*args,**kwargs)
        self.setLayout(QtGui.QHBoxLayout())
        self.bkg_wdgt = QtGui.QWidget()
        self.layout().addWidget(self.bkg_wdgt)
        self.bkg_wdgt.setLayout(QtGui.QHBoxLayout())
        self.btn = QtGui.QPushButton("hallo")
        self.bkg_wdgt.layout().addWidget(self.btn)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.btn.clicked.connect(self.on_btn_clicked)

        # self.parent_hwnd = None

    def on_btn_clicked(self):
        print "clicked"

    def paintEvent(self, event):
        # This is a hacky way to make sure input detection (clicking)
        # is in-sync with what is drawn, by forcing qt to update the
        # geometry.
        self._update_bounds()
        event.accept()

    def _update_bounds(self):
        # if not self.parent_hwnd:
        #     return
        # rect = ctypes.wintypes.RECT()
        # rectl = ctypes.byref(rect)
        # GetWindowRect( self.parent_hwnd, rectl)
        # self.move(rect.top, rect.left)
        self.move(0, 0)

    def closeEvent(self, event):
        print "closing qt widget"
        event.accept()

# Create the qt widget
qtwdgt = MainWidget()
qtwdgt.move(0, 0)

# Create a native 3dsMax dialog window
import MaxPlus
mxs = """
rollout parent_dialog "Parent" --define a rollout and create a dialog
(
	on parent_dialog close do print "PARENT Closed!"
)

createDialog parent_dialog pos:[0,0] style:#(
	#style_titlebar, #style_border, #style_sysmenu, #style_minimizebox,
	#style_resizing)

parent_dialog.hwnd
"""

mx_hwnd = MaxPlus.Core.EvalMAXScript(mxs)
mx_hwnd = mx_hwnd.Get()

qtwdgt_hwnd = get_hwnd_from_qt_widget(qtwdgt)
print "mx_hwnd: {mx_hwnd}, qt_hwnd: {qt_hwnd}".format(
    mx_hwnd=mx_hwnd, qt_hwnd=qtwdgt_hwnd)


# Parent the qt widget to the native max dialog window
SetParent(qtwdgt_hwnd, mx_hwnd)

# Make the qt widget behave like a client widget
SetWindowLong(qtwdgt_hwnd, GWL_STYLE, WS_CHILD | WS_CLIPSIBLINGS)

qtwdgt.show()
