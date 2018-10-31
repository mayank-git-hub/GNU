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
from lms_ff import lms_ff
import numpy as np
class qa_lms_ff (gr_unittest.TestCase):

	def setUp (self):
		self.tb = gr.top_block ()

	def tearDown (self):
		self.tb = None

	def test_001_t (self):
		# set up fg
		train_size = 10000
		test_size = 5000
		amplitude = [0.5, 0.25, 0.3, 1]

		expected = np.load('training.npy')
		test_expected = np.load('testing.npy')

		expected = np.concatenate((expected, test_expected), axis=0)

		one_shift = np.zeros([train_size+test_size])
		one_shift[1:] = expected[:-1]

		two_shift = np.zeros([train_size+test_size])
		two_shift[2:] = expected[:-2]

		three_shift = np.zeros([train_size+test_size])
		three_shift[3:] = expected[:-3]

		four_shift = np.zeros([train_size+test_size])
		four_shift[4:] = expected[:-4]

		multipath_model = expected + amplitude[0]*one_shift + amplitude[1]*two_shift + amplitude[2]*three_shift + amplitude[3]*four_shift

		src = blocks.vector_source_f(multipath_model)
		mult = lms_ff(num_taps=10, train_size=10000)
		snk = blocks.vector_sink_f()
		self.tb.connect (src, mult)
		self.tb.connect (mult, snk)
		self.tb.run ()
		result_data = np.array(snk.data())

		# print(result_data, expected)

		# print(result_data)

		np.save('output', result_data)
		np.save('true', expected)

		print(result_data[-10:], 'result_data')
		print(expected[-10:], 'expected')
		print(multipath_model[-10:], 'multipath_model')

		print(np.mean((result_data[train_size:]==expected[train_size:]).astype(np.float32)), " Is the accuracy")

		# check data


if __name__ == '__main__':
	gr_unittest.run(qa_lms_ff, "qa_lms_ff.xml")
