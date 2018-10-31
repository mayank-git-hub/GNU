#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from nn_equilizer_ff import nn_equilizer_ff

class qa_nn_equilizer_ff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up fg
        testing_seq = np.vstack((np.load('training_seq.npy'), np.random.normal(size=1000)))
        expected_output = something # think more about the testing_seq
        src = blocks.vector_source_f(self.testing_seq)
        nn_equi = nn_equilizer_ff(batch_size=100, learning_rate=0.0001, epochs=30, total_data=10000)
        snk = blocks.vector_sink_f()
        self.tb.connect (src, nn_equi)
        self.tb.connect (nn_equi, snk)
        self.tb.run ()
        result_data = np.array(snk.data())

        loss_training = np.mean(np.square(result_data[0:10000] - expected_output[0:10000]))
        loss_testing = np.mean(np.square(result_data[10000:] - expected_output[10000:]))
        print(loss_testing, loss_training)
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_nn_equilizer_ff, "qa_nn_equilizer_ff.xml")
