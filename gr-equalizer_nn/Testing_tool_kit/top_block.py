#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Nov  5 02:59:47 2018
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import equalizer_nn
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 80000

        ##################################################
        # Blocks
        ##################################################
        self.equalizer_nn_neural_net_0 = equalizer_nn.neural_net(1, 10, 100, 0.001, 10, 10000, '/home/allai/Desktop/Study/Comm/Lab_comm/Project/gr-equalizer_nn/Testing_tool_kit/training')
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/allai/Desktop/Study/Comm/Lab_comm/Project/gr-equalizer_nn/Testing_tool_kit/training', False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/allai/Desktop/Study/Comm/Lab_comm/Project/gr-equalizer_nn/Testing_tool_kit/training_output', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_2 = blocks.delay(gr.sizeof_float*1, 3)
        self.blocks_delay_1 = blocks.delay(gr.sizeof_float*1, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 2)
        self.blocks_add_xx_0_0 = blocks.add_vff(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0_0, 0), (self.equalizer_nn_neural_net_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_xx_0_0, 2))
        self.connect((self.blocks_delay_1, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_delay_2, 0), (self.blocks_add_xx_0_0, 3))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_delay_1, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_delay_2, 0))
        self.connect((self.equalizer_nn_neural_net_0, 0), (self.blocks_float_to_uchar_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()