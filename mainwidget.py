from PySide import QtGui
from PySide import QtCore
import sys
import winCom
import ctypes

SetParent = ctypes.windll.user32.SetParent

def get_hwnd_from_qt_widget(widget):
    ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    wdgt_ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(widget.winId())
    # wdgt_ptr_df = ctypes.cast(wdgt_ptr, ctypes.LP_c_long)
    # print type(wdgt_ptr_df.contents)
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

        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.show()


app = QtGui.QApplication(sys.argv)
wdgt = MainWidget()

wnd = winCom.get_window_by_title("Unbenannt - Editor")
wnd = wnd.get_child_window(cls = "Edit")
wnd.set_text("horst horst horst")
#wnd.set_text("horst)")

#wnd2 = winCom.get_window_by_title("test.txt - Editor")

max_wnd = winCom.get_window_by_title(r"Autodesk 3ds Max")

wdgt_hwnd = get_hwnd_from_qt_widget(wdgt)
wdgt_win = winCom.Window(wdgt_hwnd)
wdgt_win.set_text("hurtz)")

btn_hwnd = get_hwnd_from_qt_widget(wdgt.bkg_wdgt)
wdgt.show()

#SetParent(wnd2.hwnd, wnd.hwnd)
#SetParent(wnd.hwnd, wdgt_hwnd)
#SetParent(btn_hwnd, wnd.hwnd)
SetParent(wdgt_hwnd, max_wnd.hwnd)

sys.exit(app.exec_())
