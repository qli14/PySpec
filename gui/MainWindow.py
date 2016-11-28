#! encoding = utf-8
''' Main GUI Window '''

from PyQt4 import QtCore, QtGui
import datetime
from gui import SharedWidgets as Shared
from gui import Panels
from gui import Dialogs
from daq import ScanLockin
from api import general as apigen


class MainWindow(QtGui.QMainWindow):
    '''
        Implements the main window
    '''
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)

        self.title_text = 'Yo!'

        # Set global window properties
        self.setWindowTitle(self.title_text)
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)

        # Initiate pyvisa instrument objects
        self.synHandle = None
        self.lcHandle = None
        self.pciHandle = None
        self.motorHandle = None

        # Set menu bar actions
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcuts(['Ctrl+Q', 'Esc'])
        exitAction.setStatusTip('Exit program')
        exitAction.triggered.connect(self.on_exit)

        instSelAction = QtGui.QAction('Select Instrument', self)
        instSelAction.setShortcut('Ctrl+Shift+I')
        instSelAction.setStatusTip('Select instrument')
        instSelAction.triggered.connect(self.on_sel_inst)

        instStatViewAction = QtGui.QAction('View Instrument Status', self)
        instStatViewAction.setShortcut('Ctrl+Shift+V')
        instStatViewAction.setStatusTip('View status of currently connected instrument')
        instStatViewAction.triggered.connect(self.on_view_inst_stat)

        instCloseAction = QtGui.QAction('Close Instrument', self)
        instCloseAction.setStatusTip('Close individual instrument')
        instCloseAction.triggered.connect(self.on_close_sel_inst)

        scanJPLAction = QtGui.QAction('JPL Scanning Routine', self)
        scanJPLAction.setShortcut('Ctrl+Shift+J')
        scanJPLAction.setStatusTip('Use the scanning style of the JPL scanning routine')
        scanJPLAction.triggered.connect(self.on_scan_jpl)

        scanPCIAction = QtGui.QAction('PCI Oscilloscope', self)
        scanPCIAction.setShortcut('Ctrl+Shift+P')
        scanPCIAction.setStatusTip("Use the scanning style of Brian's NIPCI card routine")
        scanPCIAction.triggered.connect(self.on_scan_pci)

        scanCavityAction = QtGui.QAction('Cavity Enhanced', self)
        scanCavityAction.setShortcut('Ctrl+Shift+C')
        scanCavityAction.setStatusTip('Use cavity enhanced spectroscopy')
        scanCavityAction.triggered.connect(self.on_scan_cavity)

        testAction = QtGui.QAction('Test Widget', self)
        testAction.setShortcut('Ctrl+T')
        testAction.triggered.connect(self.on_test)

        # Set menu bar
        self.statusBar()

        menuFile = self.menuBar().addMenu('&File')
        menuFile.addAction(exitAction)
        menuInst = self.menuBar().addMenu('&Instrument')
        menuInst.addAction(instSelAction)
        menuInst.addAction(instStatViewAction)
        menuInst.addAction(instCloseAction)
        menuScan = self.menuBar().addMenu('&Scan')
        menuScan.addAction(scanJPLAction)
        menuScan.addAction(scanPCIAction)
        menuScan.addAction(scanCavityAction)
        menuTest = self.menuBar().addMenu('&Test')
        menuTest.addAction(testAction)

        # Set main window widgets
        self.synStatus = Panels.SynStatus(self)
        self.lcStatus = Panels.LockinStatus(self)
        self.scopeStatus = Panels.ScopeStatus(self)
        self.synCtrl = Panels.SynCtrl(self)
        self.lcCtrl = Panels.LockinCtrl(self)
        self.scopeCtrl = Panels.ScopeCtrl(self)
        self.motorCtrl = Panels.MotorCtrl(self)
        self.scopeMonitor = Panels.ScopeMonitor(self)
        self.lcMonitor = Panels.LockinMonitor(self)
        self.specMonitor = Panels.SpectrumMonitor(self)

        # Set main window layout
        self.mainLayout = QtGui.QGridLayout()
        self.mainLayout.setSpacing(6)
        self.mainLayout.addWidget(self.synStatus, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.lcStatus, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.scopeStatus, 2, 0, 1, 2)
        self.mainLayout.addWidget(self.synCtrl, 0, 2, 1, 2)
        self.mainLayout.addWidget(self.lcCtrl, 1, 2, 1, 2)
        self.mainLayout.addWidget(self.scopeCtrl, 2, 2, 1, 2)
        self.mainLayout.addWidget(self.motorCtrl, 3, 2, 1, 2)
        self.mainLayout.addWidget(self.scopeMonitor, 0, 4, 1, 4)
        self.mainLayout.addWidget(self.lcMonitor, 1, 4, 1, 4)
        self.mainLayout.addWidget(self.specMonitor, 2, 4, 1, 4)

        # Enable main window
        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    def refresh_syn(self):

        self.synCtrl.check()
        self.synStatus.update()

    def refresh_lockin(self):
        self.lcStatus.update()
        self.lcCtrl.check()

    def refresh_scope(self):

        self.scopeStatus.update()
        self.scopeCtrl.check()

    def refresh_motor(self):

        self.motorCtrl.check()

    def on_exit(self):
        self.close()

    def on_sel_inst(self):
        d = Dialogs.SelInstDialog(self)
        result = d.exec_()

        print(result)
        if result:
            self.refresh_syn()
            self.refresh_lockin()
            self.refresh_scope()
            self.refresh_motor()
        else:
            pass

    def on_view_inst_stat(self):
        d = Dialogs.ViewInstDialog(self)
        d.show()

    def on_close_sel_inst(self):
        d = Dialogs.CloseSelInstDialog(self)
        d.exec_()

        self.refresh_syn()
        self.refresh_lockin()
        self.refresh_scope()
        self.refresh_motor()

    def on_scan_jpl(self):

        dconfig = ScanLockin.JPLScanConfig(self)
        entry_settings = None
        result = dconfig.exec_()

        # this loop makes sure the config dialog does not disappear
        # unless the settings are all valid / or user hits cancel
        while result:  # if dialog accepted
            entry_settings, filename = dconfig.get_settings()
            if entry_settings:
                total_time = Shared.jpl_scan_time(entry_settings)
                now = datetime.datetime.today()
                length = datetime.timedelta(seconds=total_time)
                then = now + length
                text = 'This batch job is estimated to take {:s}.\nIt is expected to finish at {:s}.'.format(str(length), then.strftime('%I:%M %p, %m-%d-%Y (%a)'))
                q = Shared.MsgInfo(self, 'Time Estimation', text)
                q.addButton(QtGui.QMessageBox.Cancel)
                qres = q.exec_()
                if qres == QtGui.QMessageBox.Ok:
                    result = False
                else:
                    result = dconfig.exec_()
            else:
                result = dconfig.exec_()

        if entry_settings:
            dscan = ScanLockin.JPLScanWindow(self, entry_settings, filename)
            dscan.exec_()
        else:
            pass

    def on_scan_pci(self):
        d = Dialogs.ViewPG(self)
        d.exec_()

    def on_scan_cavity(self):
        pass

    def on_test(self):
        ''' Test developing widget. Modify the widget when necessary '''

        entry_settings = [(6, 12, 1, 1, 0, 0, 1000), (30, 50, 3, 3, 2, 2, 1000)]
        dscan = ScanLockin.JPLScanWindow(self, entry_settings, '')
        dscan.exec_()

    def closeEvent(self, event):
        q = QtGui.QMessageBox.question(self, 'Quit?',
                       'Are you sure to quit?', QtGui.QMessageBox.Yes |
                       QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if q == QtGui.QMessageBox.Yes:
            status = apigen.close_inst(self.synHandle, self.lcHandle,
                                       self.pciHandle, self.motorHandle)
            if not status:    # safe to close
                self.close()
            else:
                qq = QtGui.QMessageBox.question(self, 'Error',
                        '''Error in disconnecting instruments.
                        Are you sure to force quit?''', QtGui.QMessageBox.Yes |
                        QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if qq == QtGui.QMessageBox.Yes:
                    self.close()
                else:
                    event.ignore()
        else:
            event.ignore()
