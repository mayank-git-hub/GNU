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
from dfe import dfe
import numpy as np
class qa_dfe (gr_unittest.TestCase):

	def setUp (self):
		self.tb = gr.top_block ()

	def tearDown (self):
		self.tb = None

	def get_expected(self):

		f = open(self.training_path, 'rb')
		for i in f:
			string_format = str([str(i)])

		return np.array(string_format[2:-2].split('\\x0')[1:]).astype(np.float32)

	def test_001_t (self):
		# set up fg

<<<<<<< HEAD
		self.training_path = '/home/mayank/Desktop/GitRepos/GNU/gr-equalizer_dfe/Testing_tool_kit/training'
		train_size = 4000
=======
		self.training_path = '/home/vaibhav/GNU/gr-equalizer_dfe/Testing_tool_kit/training'
		train_size = 10000
>>>>>>> ef1272cda8eef6b8994d0d433c9c0e34ab46aa37
		self.train_size = train_size
		test_size = 5000
		amplitude = [1, 1, 1, 1]

<<<<<<< HEAD
		expected = np.zeros([self.train_size+test_size])
		expected_temp = self.get_expected()
		expected[0:self.train_size] = expected_temp[0:self.train_size]
		expected[self.train_size:] = expected_temp[10000:]
		# print(expected.shape)
		# test_expected = np.load('testing.npy')
=======
		expected = self.get_expected()
>>>>>>> ef1272cda8eef6b8994d0d433c9c0e34ab46aa37

		# Creating the multipath model

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
		mult = dfe(num_taps=100, train_size=self.train_size, training_path=self.training_path)
		snk = blocks.vector_sink_f()
		self.tb.connect (src, mult)
		self.tb.connect (mult, snk)
		self.tb.run ()
		result_data = np.array(snk.data())

		print(result_data[-100:], 'result_data')
		print(expected[-100:], 'expected')
		print(multipath_model[-10:], 'multipath_model')

		print(np.mean((result_data[train_size:]==expected[train_size:]).astype(np.float32)), " Is the accuracy")

		# check data


if __name__ == '__main__':
	gr_unittest.run(qa_dfe, "qa_dfe.xml")
