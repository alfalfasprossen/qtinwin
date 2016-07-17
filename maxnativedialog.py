"""This is a hacky experiment of placing a qt widget as a child-window
inside a native 3dsMax dialog window.

Since the native dialog window behaves correctly in terms of z-ordering
the most annoying part of working with qt widgets in 3dsMax is solved.
Of course other problems occur, like correctly updating the widget when
the parent dialog has moved, resizing, closing and probably other
messages that won't get into the qt message queue.

I tried replacing the WndProc function of the native dialog with one
written in pyhon, catching any interesting messages and then passing
everything on to the original function, but it only caused the main
application to hang.
"""
import ctypes

from PySide import QtGui
from PySide import QtCore
import MaxPlus

SetParent = ctypes.windll.user32.SetParent
SetWindowLong = ctypes.windll.user32.SetWindowLongW
GWL_STYLE = -16
WS_CHILD = 0x40000000
WS_CLIPSIBLINGS = 0x04000000
GetWindowRect = ctypes.windll.user32.GetWindowRect
GetWindowLong = ctypes.windll.user32.GetWindowLongW
SetWindowLongPtr = ctypes.windll.user32.SetWindowLongPtrW
GetWindowLongPtr = ctypes.windll.user32.GetWindowLongPtrW
GWL_WNDPROC = -4
CallWindowProc = ctypes.windll.user32.CallWindowProcW

class FocusFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        MaxPlus.CUI.DisableAccelerators()
        return False

class MaxWidget(QtGui.QWidget):
    def __init__(self, title):
        super(MaxWidget, self).__init__(None)
        self.parent_hwnd = self._create_native_window(title)
        self.hwnd = self.get_hwnd()
        self._parent_to_native_window()
        self.show()
        app = QtGui.QApplication.instance()
        self.focus_filter = FocusFilter()
        self.event_filter = app.installEventFilter(self.focus_filter)
        # self.installEventFilter(self)

        # self.old_window_proc
        # replace_wnd_proc(self)

    def focusChanged(self, old, new):
        print 'focus changed'
        print old
        print new

    def eventFilter(self, obj, event):
        if obj != self:
            print 'obj is not self'
        if event.type() == QtCore.QEvent.Type.FocusIn:
            print 'gained focus'
        elif event.type() == QtCore.QEvent.Type.FocusOut:
            print 'lost focus'
        else:
            print event.type()


    def _create_native_window(self, title):
        """Create a native 3dsMax dialog window."""
        mxs = (
        """
            rollout parent_dialog "{title}"
            (
            )

            createDialog parent_dialog pos:[0,0] style:#(
                #style_titlebar,
                #style_border,
                #style_sysmenu,
                #style_minimizebox,
                #style_resizing)

            parent_dialog.hwnd -- return the hwnd of the dialog
        """
        ).format(title=title)

        mx_hwnd_fpval = MaxPlus.Core.EvalMAXScript(mxs)
        return mx_hwnd_fpval.Get()

    def get_hwnd(self):
        """Get the HWND window handle from this QtWidget."""
        ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
        wdgt_ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
        return wdgt_ptr

    def _parent_to_native_window(self):
        """ Parent the qt widget to the native parent_hwnd window.
        Make the qt widget behave and look like a client widget.
        """
        SetWindowLongPtr(self.hwnd, GWL_STYLE, WS_CHILD | WS_CLIPSIBLINGS)
        SetParent(self.hwnd, self.parent_hwnd)

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

    # TODO:
    # overwrite the positioning and resizing funcs. try to use the native
    # message queue first (redirecting wndproc if possible)
    # otherwise, overwrite move() etc. to make sure they move the parent
    # widget first. This will probably require to backup these functions
    # as _move() etc. to make sure the widget is not offset within its
    # parent.
    # register an event filter to catch all user input into the widget
    # otherwise editing text etc is captured already by the max main
    # window.
    # If possible detect if the parent widget has been closed and
    # delete the qtwidget then as well.

    def closeEvent(self, event):
        print "closing qt widget"
        event.accept()
