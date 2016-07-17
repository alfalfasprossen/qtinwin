"""This is a quite well working experiment of setting the **owner**
(not the **parent**) of the qt widget to be the 3dsMax main window.

Effectively the qt widget will behave like a natively spawned window,
with correct z-order behaviour concerning its sibling windows.
"""

import ctypes

from PySide import QtGui
from PySide import QtCore
import MaxPlus

GWL_HWNDPARENT = -8
SetWindowLongPtr = ctypes.windll.user32.SetWindowLongPtrW

class FocusFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        # TODO: fix focus filter not releasing on defocus
        MaxPlus.CUI.DisableAccelerators()
        return False

class MaxWidget(QtGui.QWidget):
    def __init__(self, title):
        super(MaxWidget, self).__init__(None)
        self.parent_hwnd = MaxPlus.Win32.GetMAXHWnd()
        self.hwnd = self.get_hwnd()
        self._parent_to_main_window()
        self.show()
        app = QtGui.QApplication.instance()
        self._focus_filter = FocusFilter()
        self.event_filter = app.installEventFilter(self._focus_filter)

    def get_hwnd(self):
        """Get the HWND window handle from this QtWidget."""
        ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
        wdgt_ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
        return wdgt_ptr

    def _parent_to_main_window(self):
        """ Parent the widget to the 3dsMax main window.

        Technically this is NOT setting the **parent** of the window,
        but the **owner**.
        There is a huge difference, that is hardly documented in the
        win32 API.
        https://msdn.microsoft.com/en-us/library/windows/desktop/ms644898(v=vs.85).aspx  # noqa
        Setting the parent would make this a child or mdi-
        child window. Setting the owner, makes this a top-level,
        overlapped window that is controlled by the main window, but
        not confined to its client area.
        http://stackoverflow.com/questions/133122/
        """
        SetWindowLongPtr(self.hwnd, GWL_HWNDPARENT, self.parent_hwnd)

    def closeEvent(self, event):
        app = QtGui.QApplication.instance()
        app.removeEventFilter(self.event_filter)
        event.accept()
