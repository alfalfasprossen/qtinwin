from PySide import QtGui

import maxparenting
reload(maxparenting)

class ExampleWidget(maxparenting.MaxWidget):
    """This is a test that ui interaction works correctly with a more
    or less complex ui.
    """
    def __init__(self):
        super(ExampleWidget, self).__init__("Example Widget")
        self.build_ui()
        self.connect_ui()

    def build_ui(self):
        self.setLayout(QtGui.QVBoxLayout())
        self.label = QtGui.QLabel("some label")
        self.btn = QtGui.QPushButton("button")
        self.lineedit = QtGui.QLineEdit()
        self.textedit = QtGui.QTextEdit()

        self.grp = QtGui.QGroupBox("group box grid layout")
        self.grp.setLayout(QtGui.QGridLayout())
        self.chkbx_1 = QtGui.QCheckBox("chkbx_1")
        self.chkbx_2 = QtGui.QCheckBox("chkbx_2l")
        self.chkbx_2.setDisabled(True)
        self.chkbx_3 = QtGui.QCheckBox("chkbx_2r")
        self.chkbx_4 = QtGui.QCheckBox("chkbx_3")
        self.chkbx_5 = QtGui.QCheckBox("chkbx_4")
        self.grp.layout().addWidget(self.chkbx_1, 0, 0)
        self.grp.layout().addWidget(self.chkbx_2, 1, 0)
        self.grp.layout().addWidget(self.chkbx_3, 1, 1)
        self.grp.layout().addWidget(self.chkbx_4, 2, 0)
        self.grp.layout().addWidget(self.chkbx_5, 3, 0)
        self.grp.layout().setColumnStretch(2,1)

        self.lrbox = QtGui.QHBoxLayout()
        self.lrbox.addWidget(self.textedit)
        self.lrbox.addWidget(self.grp)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.btn)
        self.layout().addWidget(self.lineedit)
        self.layout().addLayout(self.lrbox)

    def connect_ui(self):
        self.btn.clicked.connect(self.on_btn_clicked)

    def on_btn_clicked(self):
        print "btn clicked"

global qtwdgt
qtwdgt = ExampleWidget()
