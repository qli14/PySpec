#! encoding = utf-8
''' Dialog windows for system menues '''


from PyQt5 import QtGui, QtCore
from api import general as api_gen
from api import synthesizer as api_syn
from api import lockin as api_lia
from gui import SharedWidgets as Shared
from pyqtgraph import siFormat


class SelInstDialog(QtGui.QDialog):
    '''
        Dialog window for instrument selection.
    '''

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setWindowTitle('Select Instrument')

        refreshButton = QtGui.QPushButton('Refresh Available Instrument List')
        acceptButton = QtGui.QPushButton(Shared.btn_label('confirm'))
        cancelButton = QtGui.QPushButton(Shared.btn_label('reject'))

        self.availableInst = QtGui.QLabel()
        instList, instStr = api_gen.list_inst()
        self.availableInst.setText(instStr)

        selInst = QtGui.QWidget()
        selInstLayout = QtGui.QFormLayout()
        self.selSyn = QtGui.QComboBox()
        self.selSyn.addItems(['N.A.'])
        self.selSyn.addItems(instList)
        self.selLockin = QtGui.QComboBox()
        self.selLockin.addItems(['N.A.'])
        self.selLockin.addItems(instList)
        self.selScope = QtGui.QComboBox()
        self.selScope.addItems(['N.A.'])
        self.selScope.addItems(instList)
        self.selMotor = QtGui.QComboBox()
        self.selMotor.addItems(['N.A.'])
        self.selMotor.addItems(instList)
        self.selPressure = QtGui.QComboBox()
        self.selPressure.addItems(['N.A.'])
        self.selPressure.addItems(instList)
        selInstLayout.addRow(QtGui.QLabel('Synthesizer'), self.selSyn)
        selInstLayout.addRow(QtGui.QLabel('Lock-in'), self.selLockin)
        selInstLayout.addRow(QtGui.QLabel('Oscilloscope'), self.selScope)
        selInstLayout.addRow(QtGui.QLabel('Step Motor'), self.selMotor)
        selInstLayout.addRow(QtGui.QLabel('CENTER TWO Pressure Readout'), self.selPressure)
        selInst.setLayout(selInstLayout)

        # Set main layout
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.availableInst, 0, 0, 1, 2)
        mainLayout.addWidget(refreshButton, 1, 0, 1, 2)
        mainLayout.addWidget(selInst, 2, 0, 1, 2)
        mainLayout.addWidget(cancelButton, 3, 0)
        mainLayout.addWidget(acceptButton, 3, 1)

        self.setLayout(mainLayout)

        refreshButton.clicked.connect(self.refresh)
        cancelButton.clicked.connect(self.reject)
        acceptButton.clicked.connect(self.accept)

    def refresh(self):
        ''' Refresh instrument list '''

        # refresh avaiable instrument list
        instList, instStr = api_gen.list_inst()
        self.availableInst.setText(instStr)

        # refresh QComboBoxes
        item_count = self.selSyn.count()
        # remove all items but the first one
        for i in range(item_count-1):
            # Because Qt automatically update the index, this loop needs to
            # keep deleting the 'second' item, whose index is 1
            self.selSyn.removeItem(1)
            self.selLockin.removeItem(1)
            self.selScope.removeItem(1)
            self.selMotor.removeItem(1)
            self.selPressure.removeItem(1)
        self.selSyn.addItems(instList)
        self.selLockin.addItems(instList)
        self.selScope.addItems(instList)
        self.selMotor.addItems(instList)
        self.selPressure.addItems(instList)

    def accept(self):

        # close old instrument handles
        api_gen.close_inst(self.parent.synHandle,
                           self.parent.liaHandle,
                           self.parent.pciHandle,
                           self.parent.motorHandle,
                           self.parent.pressureHandle)

        # open new instrument handles
        self.parent.synHandle = api_gen.open_inst(self.selSyn.currentText())
        self.parent.liaHandle = api_gen.open_inst(self.selLockin.currentText())
        self.parent.pciHandle = api_gen.open_inst(self.selScope.currentText())
        self.parent.motorHandle = api_gen.open_inst(self.selMotor.currentText())
        self.parent.pressureHandle = api_gen.open_inst(self.selPressure.currentText())

        self.done(True)


class ViewInstDialog(QtGui.QDialog):
    '''
        Dialog window for instrument status view
    '''

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setWindowTitle('View Instrument Status')


class CloseSelInstDialog(QtGui.QDialog):
    '''
        Dialog window for closing selected instrument.
    '''

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setWindowTitle('Close Instrument')

        inst = QtGui.QWidget()
        self.synToggle = QtGui.QCheckBox()
        self.liaToggle = QtGui.QCheckBox()
        self.pciToggle = QtGui.QCheckBox()
        self.motorToggle = QtGui.QCheckBox()
        self.pressureToggle = QtGui.QCheckBox()

        instLayout = QtGui.QFormLayout()
        instLayout.addRow(QtGui.QLabel('Instrument'), QtGui.QLabel('Status'))
        # only list currently connected instruments
        if self.parent.synHandle:
            self.synToggle.setCheckState(True)
            instLayout.addRow(QtGui.QLabel('Synthesizer'), self.synToggle)
        else:
            self.synToggle.setCheckState(False)

        if self.parent.liaHandle:
            self.liaToggle.setCheckState(True)
            instLayout.addRow(QtGui.QLabel('Lockin'), self.liaToggle)
        else:
            self.liaToggle.setCheckState(False)

        if self.parent.pciHandle:
            self.pciToggle.setCheckState(True)
            instLayout.addRow(QtGui.QLabel('Oscilloscope'), self.pciToggle)
        else:
            self.pciToggle.setCheckState(False)

        if self.parent.motorHandle:
            self.motorToggle.setCheckState(True)
            instLayout.addRow(QtGui.QLabel('Motor'), self.motorToggle)
        else:
            self.motorToggle.setCheckState(False)

        if self.parent.pressureHandle:
            self.pressureToggle.setCheckState(True)
            instLayout.addRow(QtGui.QLabel('Pressure Readout'), self.pressureToggle)
        else:
            self.pressureToggle.setCheckState(False)

        inst.setLayout(instLayout)

        okButton = QtGui.QPushButton(Shared.btn_label('complete'))
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(inst)
        mainLayout.addWidget(QtGui.QLabel('No command will be sent before you hit the accept button'))
        mainLayout.addWidget(okButton)
        self.setLayout(mainLayout)

        okButton.clicked.connect(self.accept)

    def close_inst_handle(self, inst_handle, check_state):

        if check_state and inst_handle:
            api_gen.close_inst(inst_handle)
            return None
        else:
            return inst_handle

    def accept(self):

        self.parent.synHandle = self.close_inst_handle(self.parent.synHandle,
                                                       self.synToggle.isChecked())
        self.parent.liaHandle = self.close_inst_handle(self.parent.liaHandle,
                                                       self.liaToggle.isChecked())
        self.parent.pciHandle = self.close_inst_handle(self.parent.pciHandle,
                                                       self.pciToggle.isChecked())
        self.parent.motorHandle = self.close_inst_handle(self.parent.motorHandle,
                                                         self.motorToggle.isChecked())
        self.parent.pressureHandle = self.close_inst_handle(self.parent.pressureHandle,
                                                            self.pressureToggle.isChecked())
        self.close()


class SynInfoDialog(QtGui.QDialog):
    '''
        Dialog window for displaying full synthesizer settings.
    '''

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.setMinimumWidth(800)
        self.setMinimumHeight(400)
        self.setWindowTitle('Synthesizer Settings')

        self.instGroup = QtGui.QGroupBox()
        self.rfGroup = QtGui.QGroupBox()
        self.modGroup = QtGui.QGroupBox()

        self.instGroup.setTitle('Instrument Session')
        self.instNameLabel = QtGui.QLabel()
        self.instInterfaceLabel = QtGui.QLabel()
        self.instInterfaceNumLabel = QtGui.QLabel()
        self.instRemoteDispLabel = QtGui.QLabel()
        instGroupLayout = QtGui.QFormLayout()
        instGroupLayout.addRow(QtGui.QLabel('Instrument Name'), self.instNameLabel)
        instGroupLayout.addRow(QtGui.QLabel('Interface Type'), self.instInterfaceLabel)
        instGroupLayout.addRow(QtGui.QLabel('Interface Number'), self.instInterfaceNumLabel)
        instGroupLayout.addRow(QtGui.QLabel('Remote Display'), self.instRemoteDispLabel)
        self.instGroup.setLayout(instGroupLayout)

        self.rfGroup.setTitle('RF Settings')
        self.rfOutputLabel = QtGui.QLabel()
        self.modOutputLabel = QtGui.QLabel()
        self.synFreqLabel = QtGui.QLabel()
        rfGroupLayout = QtGui.QGridLayout()
        rfGroupLayout.addWidget(QtGui.QLabel('RF Output'), 0, 0)
        rfGroupLayout.addWidget(self.rfOutputLabel, 0, 1)
        rfGroupLayout.addWidget(QtGui.QLabel('Synth Frequency'), 0, 2)
        rfGroupLayout.addWidget(self.synFreqLabel, 0, 3)
        rfGroupLayout.addWidget(QtGui.QLabel('Modulation Output'), 0, 4)
        rfGroupLayout.addWidget(self.modOutputLabel, 0, 5)
        self.rfGroup.setLayout(rfGroupLayout)

        self.modGroup.setTitle('Modulation Settings')
        self.am1StateLabel = QtGui.QLabel()
        self.am2StateLabel = QtGui.QLabel()
        self.fm1StateLabel = QtGui.QLabel()
        self.fm2StateLabel = QtGui.QLabel()
        self.pm1StateLabel = QtGui.QLabel()
        self.pm2StateLabel = QtGui.QLabel()
        self.lfStateLabel = QtGui.QLabel()
        self.am1DepthLabel = QtGui.QLabel()
        self.am2DepthLabel = QtGui.QLabel()
        self.fm1DevLabel = QtGui.QLabel()
        self.fm2DevLabel = QtGui.QLabel()
        self.pm1DevLabel = QtGui.QLabel()
        self.pm2DevLabel = QtGui.QLabel()
        self.lfVolLabel = QtGui.QLabel()
        self.am1SrcLabel = QtGui.QLabel()
        self.am2SrcLabel = QtGui.QLabel()
        self.fm1SrcLabel = QtGui.QLabel()
        self.fm2SrcLabel = QtGui.QLabel()
        self.pm1SrcLabel = QtGui.QLabel()
        self.pm2SrcLabel = QtGui.QLabel()
        self.lfSrcLabel = QtGui.QLabel()
        self.am1FreqLabel = QtGui.QLabel()
        self.am2FreqLabel = QtGui.QLabel()
        self.fm1FreqLabel = QtGui.QLabel()
        self.fm2FreqLabel = QtGui.QLabel()
        self.pm1FreqLabel = QtGui.QLabel()
        self.pm2FreqLabel = QtGui.QLabel()
        self.am1WaveLabel = QtGui.QLabel()
        self.am2WaveLabel = QtGui.QLabel()
        self.fm1WaveLabel = QtGui.QLabel()
        self.fm2WaveLabel = QtGui.QLabel()
        self.pm1WaveLabel = QtGui.QLabel()
        self.pm2WaveLabel = QtGui.QLabel()

        modGroupLayout = QtGui.QGridLayout()
        modGroupLayout.addWidget(QtGui.QLabel('Channel'), 0, 0)
        modGroupLayout.addWidget(QtGui.QLabel('Source'), 0, 1)
        modGroupLayout.addWidget(QtGui.QLabel('State'), 0, 2)
        modGroupLayout.addWidget(QtGui.QLabel('Depth/Dev'), 0, 3)
        modGroupLayout.addWidget(QtGui.QLabel('Rate'), 0, 4)
        modGroupLayout.addWidget(QtGui.QLabel('Waveform'), 0, 5)
        modGroupLayout.addWidget(QtGui.QLabel('AM1'), 1, 0)
        modGroupLayout.addWidget(self.am1StateLabel, 1, 1)
        modGroupLayout.addWidget(self.am1SrcLabel, 1, 2)
        modGroupLayout.addWidget(self.am1DepthLabel, 1, 3)
        modGroupLayout.addWidget(self.am1FreqLabel, 1, 4)
        modGroupLayout.addWidget(self.am1WaveLabel, 1, 5)
        modGroupLayout.addWidget(QtGui.QLabel('AM2'), 2, 0)
        modGroupLayout.addWidget(self.am2StateLabel, 2, 1)
        modGroupLayout.addWidget(self.am2SrcLabel, 2, 2)
        modGroupLayout.addWidget(self.am2DepthLabel, 2, 3)
        modGroupLayout.addWidget(self.am2FreqLabel, 2, 4)
        modGroupLayout.addWidget(self.am2WaveLabel, 2, 5)
        modGroupLayout.addWidget(QtGui.QLabel('FM1'), 3, 0)
        modGroupLayout.addWidget(self.fm1StateLabel, 3, 1)
        modGroupLayout.addWidget(self.fm1SrcLabel, 3, 2)
        modGroupLayout.addWidget(self.fm1DevLabel, 3, 3)
        modGroupLayout.addWidget(self.fm1FreqLabel, 3, 4)
        modGroupLayout.addWidget(self.fm1WaveLabel, 3, 5)
        modGroupLayout.addWidget(QtGui.QLabel('FM2'), 4, 0)
        modGroupLayout.addWidget(self.fm2StateLabel, 4, 1)
        modGroupLayout.addWidget(self.fm2SrcLabel, 4, 2)
        modGroupLayout.addWidget(self.fm2DevLabel, 4, 3)
        modGroupLayout.addWidget(self.fm2FreqLabel, 4, 4)
        modGroupLayout.addWidget(self.fm2WaveLabel, 4, 5)
        modGroupLayout.addWidget(QtGui.QLabel('φM1'), 5, 0)
        modGroupLayout.addWidget(self.pm1StateLabel, 5, 1)
        modGroupLayout.addWidget(self.pm1SrcLabel, 5, 2)
        modGroupLayout.addWidget(self.pm1DevLabel, 5, 3)
        modGroupLayout.addWidget(self.pm1FreqLabel, 5, 4)
        modGroupLayout.addWidget(self.pm1WaveLabel, 5, 5)
        modGroupLayout.addWidget(QtGui.QLabel('φM2'), 6, 0)
        modGroupLayout.addWidget(self.pm2StateLabel, 6, 1)
        modGroupLayout.addWidget(self.pm2SrcLabel, 6, 2)
        modGroupLayout.addWidget(self.pm2DevLabel, 6, 3)
        modGroupLayout.addWidget(self.pm2FreqLabel, 6, 4)
        modGroupLayout.addWidget(self.pm2WaveLabel, 6, 5)
        modGroupLayout.addWidget(QtGui.QLabel('LF OUT'), 7, 0)
        modGroupLayout.addWidget(self.lfStateLabel, 7, 1)
        modGroupLayout.addWidget(self.lfSrcLabel, 7, 2)
        modGroupLayout.addWidget(self.lfVolLabel, 7, 3)
        self.modGroup.setLayout(modGroupLayout)

        self.acceptButton = QtGui.QPushButton(Shared.btn_label('accept'))

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.instGroup, 0, 0, 1, 5)
        mainLayout.addWidget(self.rfGroup, 1, 0, 1, 5)
        mainLayout.addWidget(self.modGroup, 2, 0, 1, 5)
        mainLayout.addWidget(self.acceptButton, 3, 2, 1, 1)
        self.setLayout(mainLayout)

        self.acceptButton.clicked.connect(self.accept)

    def display(self):

        self.acceptButton.setText(Shared.btn_label('accept'))

        if self.parent.synHandle:
            self.update()
            self.instGroup.show()
            self.rfGroup.show()
            self.modGroup.show()
        else:
            self.instGroup.hide()
            self.rfGroup.hide()
            self.modGroup.hide()

        self.exec_()

    def update(self):

        # update instrument panel
        self.instNameLabel.setText(self.parent.synHandle.resource_name)
        self.instInterfaceLabel.setText(str(self.parent.synHandle.interface_type))
        self.instInterfaceNumLabel.setText(str(self.parent.synHandle.interface_number))
        self.instRemoteDispLabel.setText('ON' if api_syn.read_remote_disp(self.parent.synHandle) else 'OFF')

        # update RF setting panel
        self.rfOutputLabel.setText('ON' if api_syn.read_power_toggle(self.parent.synHandle) else 'OFF')
        self.modOutputLabel.setText('ON' if api_syn.read_mod_toggle(self.parent.synHandle) else 'OFF')
        self.synFreqLabel.setText('{:.12f} MHz'.format(api_syn.read_syn_freq(self.parent.synHandle)))

        # update modulation setting panel
        self.am1StateLabel.setText('ON' if api_syn.read_am_state(self.parent.synHandle, 1) else 'OFF')
        self.am1SrcLabel.setText(api_syn.read_am_source(self.parent.synHandle, 1))
        self.am1DepthLabel.setText('{:.1f} % ({:.0f} dB)'.format(*api_syn.read_am_depth(self.parent.synHandle, 1)))
        self.am1FreqLabel.setText(siFormat(api_syn.read_am_freq(self.parent.synHandle, 1), suffix='Hz'))
        self.am1WaveLabel.setText(api_syn.read_am_waveform(self.parent.synHandle, 1))

        self.am2StateLabel.setText('ON' if api_syn.read_am_state(self.parent.synHandle, 2) else 'OFF')
        self.am2SrcLabel.setText(api_syn.read_am_source(self.parent.synHandle, 2))
        self.am2DepthLabel.setText('{:.1f} % ({:.0f} dB)'.format(*api_syn.read_am_depth(self.parent.synHandle, 2)))
        self.am2FreqLabel.setText(siFormat(api_syn.read_am_freq(self.parent.synHandle, 2), suffix='Hz'))
        self.am2WaveLabel.setText(api_syn.read_am_waveform(self.parent.synHandle, 2))

        self.fm1StateLabel.setText('ON' if api_syn.read_fm_state(self.parent.synHandle, 1) else 'OFF')
        self.fm1SrcLabel.setText(api_syn.read_fm_source(self.parent.synHandle, 1))
        self.fm1DevLabel.setText(siFormat(api_syn.read_fm_dev(self.parent.synHandle, 1), suffix='Hz'))
        self.fm1FreqLabel.setText(siFormat(api_syn.read_fm_freq(self.parent.synHandle, 1), suffix='Hz'))
        self.fm1WaveLabel.setText(api_syn.read_fm_waveform(self.parent.synHandle, 1))

        self.fm2StateLabel.setText('ON' if api_syn.read_fm_state(self.parent.synHandle, 2) else 'OFF')
        self.fm2SrcLabel.setText(api_syn.read_fm_source(self.parent.synHandle, 2))
        self.fm2DevLabel.setText(siFormat(api_syn.read_fm_dev(self.parent.synHandle, 2), suffix='Hz'))
        self.fm2FreqLabel.setText(siFormat(api_syn.read_fm_freq(self.parent.synHandle, 2), suffix='Hz'))
        self.fm2WaveLabel.setText(api_syn.read_fm_waveform(self.parent.synHandle, 2))

        self.pm1StateLabel.setText('ON' if api_syn.read_pm_state(self.parent.synHandle, 1) else 'OFF')
        self.pm1SrcLabel.setText(api_syn.read_pm_source(self.parent.synHandle, 1))
        self.pm1DevLabel.setText(siFormat(api_syn.read_pm_dev(self.parent.synHandle, 1), suffix='rad'))
        self.pm1FreqLabel.setText(siFormat(api_syn.read_pm_freq(self.parent.synHandle, 1), suffix='Hz'))
        self.pm1WaveLabel.setText(api_syn.read_pm_waveform(self.parent.synHandle, 1))

        self.pm2StateLabel.setText('ON' if api_syn.read_pm_state(self.parent.synHandle, 2) else 'OFF')
        self.pm2SrcLabel.setText(api_syn.read_pm_source(self.parent.synHandle, 2))
        self.pm2DevLabel.setText(siFormat(api_syn.read_pm_dev(self.parent.synHandle, 2), suffix='rad'))
        self.pm2FreqLabel.setText(siFormat(api_syn.read_pm_freq(self.parent.synHandle, 2), suffix='Hz'))
        self.pm2WaveLabel.setText(api_syn.read_pm_waveform(self.parent.synHandle, 2))

        lf_vol, lf_status = api_syn.read_lf(self.parent.synHandle)
        self.lfStateLabel.setText('ON' if lf_status else 'OFF')
        self.lfSrcLabel.setText(api_syn.read_lf_source(self.parent.synHandle))
        self.lfVolLabel.setText(siFormat(lf_vol, suffix='V'))


class LockinInfoDialog(QtGui.QDialog):
    '''
        Dialog window for displaying full lockin settings.
    '''

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.setWindowTitle('Lockin Amplifier Settings')

        self.instGroup = QtGui.QGroupBox()
        self.refGroup = QtGui.QGroupBox()
        self.inputGroup = QtGui.QGroupBox()
        self.gainGroup = QtGui.QGroupBox()
        self.outputGroup = QtGui.QGroupBox()

        self.instGroup.setTitle('Instrument Session')
        self.instNameLabel = QtGui.QLabel()
        self.instInterfaceLabel = QtGui.QLabel()
        self.instInterfaceNumLabel = QtGui.QLabel()
        instGroupLayout = QtGui.QFormLayout()
        instGroupLayout.addRow(QtGui.QLabel('Instrument Name'), self.instNameLabel)
        instGroupLayout.addRow(QtGui.QLabel('Interface Type'), self.instInterfaceLabel)
        instGroupLayout.addRow(QtGui.QLabel('Interface Number'), self.instInterfaceNumLabel)
        self.instGroup.setLayout(instGroupLayout)

        self.refGroup.setTitle('Reference and Phase')
        self.refSrcLabel = QtGui.QLabel()
        self.refFreqLabel = QtGui.QLabel()
        self.refHarmLabel = QtGui.QLabel()
        self.refPhaseLabel = QtGui.QLabel()
        refGroupLayout =  QtGui.QFormLayout()
        refGroupLayout.addRow(QtGui.QLabel('Reference Source'), self.refSrcLabel)
        refGroupLayout.addRow(QtGui.QLabel('Reference Freq'), self.refFreqLabel)
        refGroupLayout.addRow(QtGui.QLabel('Harmonics'), self.refHarmLabel)
        refGroupLayout.addRow(QtGui.QLabel('Phase'), self.refPhaseLabel)
        self.refGroup.setLayout(refGroupLayout)

        self.inputGroup.setTitle('Input and Filter')
        self.inputConfigLabel = QtGui.QLabel()
        self.inputGroundingLabel = QtGui.QLabel()
        self.inputCouplingLabel = QtGui.QLabel()
        self.inputFilterLabel = QtGui.QLabel()
        inputGroupLayout = QtGui.QFormLayout()
        inputGroupLayout.addRow(QtGui.QLabel('Input Config'), self.inputConfigLabel)
        inputGroupLayout.addRow(QtGui.QLabel('Input Grounding'), self.inputGroundingLabel)
        inputGroupLayout.addRow(QtGui.QLabel('Input Coupling'), self.inputCouplingLabel)
        inputGroupLayout.addRow(QtGui.QLabel('Input Filter'), self.inputFilterLabel)
        self.inputGroup.setLayout(inputGroupLayout)

        self.gainGroup.setTitle('Gain')
        self.gainSensLabel = QtGui.QLabel()
        self.gainReserveLabel = QtGui.QLabel()
        self.gainTCLabel = QtGui.QLabel()
        self.gainFilterLabel = QtGui.QLabel()
        gainGroupLayout = QtGui.QFormLayout()
        gainGroupLayout.addRow(QtGui.QLabel('Sensitivity'), self.gainSensLabel)
        gainGroupLayout.addRow(QtGui.QLabel('Time Constant'), self.gainTCLabel)
        gainGroupLayout.addRow(QtGui.QLabel('Reserve'), self.gainReserveLabel)
        gainGroupLayout.addRow(QtGui.QLabel('Low-pass Filter Slope'), self.gainFilterLabel)
        self.gainGroup.setLayout(gainGroupLayout)

        self.outputGroup.setTitle('Display and Output')
        self.outputDisp1Label = QtGui.QLabel()
        self.outputDisp2Label = QtGui.QLabel()
        self.outputFront1Label = QtGui.QLabel()
        self.outputFront2Label = QtGui.QLabel()
        self.outputSRateLabel = QtGui.QLabel()
        outputGroupLayout = QtGui.QGridLayout()
        outputGroupLayout.addWidget(QtGui.QLabel('Chanel 1'), 0, 1)
        outputGroupLayout.addWidget(QtGui.QLabel('Chanel 2'), 0, 2)
        outputGroupLayout.addWidget(QtGui.QLabel('Display Output'), 1, 0)
        outputGroupLayout.addWidget(self.outputDisp1Label, 1, 1)
        outputGroupLayout.addWidget(self.outputDisp2Label, 1, 2)
        outputGroupLayout.addWidget(QtGui.QLabel('Front Panel Output'), 2, 0)
        outputGroupLayout.addWidget(self.outputFront1Label, 2, 1)
        outputGroupLayout.addWidget(self.outputFront2Label, 2, 2)
        outputGroupLayout.addWidget(QtGui.QLabel('Sampling Rate'), 3, 0)
        outputGroupLayout.addWidget(self.outputSRateLabel, 3, 1, 1, 2)
        self.outputGroup.setLayout(outputGroupLayout)

        self.acceptButton = QtGui.QPushButton(Shared.btn_label('accept'))

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.instGroup, 0, 0, 1, 6)
        mainLayout.addWidget(self.inputGroup, 1, 0, 1, 3)
        mainLayout.addWidget(self.outputGroup, 1, 3, 1, 3)
        mainLayout.addWidget(self.refGroup, 2, 0, 1, 3)
        mainLayout.addWidget(self.gainGroup, 2, 3, 1, 3)
        mainLayout.addWidget(self.acceptButton, 3, 2, 1, 2)
        self.setLayout(mainLayout)

        self.acceptButton.clicked.connect(self.accept)

    def display(self):

        self.acceptButton.setText(Shared.btn_label('accept'))

        if self.parent.liaHandle:
            self.update()
            self.instGroup.show()
            self.refGroup.show()
            self.gainGroup.show()
            self.inputGroup.show()
            self.outputGroup.show()
        else:
            self.instGroup.hide()
            self.refGroup.hide()
            self.gainGroup.hide()
            self.inputGroup.hide()
            self.outputGroup.hide()

        self.exec_()

    def update(self):

        # update instrument panel
        self.instNameLabel.setText(self.parent.liaHandle.resource_name)
        self.instInterfaceLabel.setText(str(self.parent.liaHandle.interface_type))
        self.instInterfaceNumLabel.setText(str(self.parent.liaHandle.interface_number))

        # update ref group
        self.refSrcLabel.setText(api_lia.read_ref_source(self.parent.liaHandle))
        self.refFreqLabel.setText(siFormat(api_lia.read_freq(self.parent.liaHandle), suffix='Hz'))
        self.refHarmLabel.setText('{:d}'.format(api_lia.read_harm(self.parent.liaHandle)))
        self.refPhaseLabel.setText('{:.2f} deg'.format(api_lia.read_phase(self.parent.liaHandle)))

        # update input group
        self.inputConfigLabel.setText(api_lia.read_input_config(self.parent.liaHandle))
        self.inputGroundingLabel.setText(api_lia.read_input_grounding(self.parent.liaHandle))
        self.inputCouplingLabel.setText(api_lia.read_couple(self.parent.liaHandle))
        self.inputFilterLabel.setText(api_lia.read_input_filter(self.parent.liaHandle))

        # update gain group
        self.gainSensLabel.setText(Shared.LIASENSLIST[api_lia.read_sens(self.parent.liaHandle)])
        self.gainTCLabel.setText(Shared.LIATCLIST[api_lia.read_tc(self.parent.liaHandle)])
        self.gainReserveLabel.setText(api_lia.read_reserve(self.parent.liaHandle))
        self.gainFilterLabel.setText(api_lia.read_lp_slope(self.parent.liaHandle))

        # update output group
        disp1, disp2 = api_lia.read_disp(self.parent.liaHandle)
        self.outputDisp1Label.setText(disp1)
        self.outputDisp2Label.setText(disp2)
        front1, front2 = api_lia.read_front_panel(self.parent.liaHandle)
        self.outputFront1Label.setText(front1)
        self.outputFront2Label.setText(front2)
        self.outputSRateLabel.setText(api_lia.read_sample_rate(self.parent.liaHandle))
