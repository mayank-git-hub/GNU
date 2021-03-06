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

import numpy as np
from gnuradio import gr

class dfe(gr.sync_block):
	"""
	docstring for block dfe
	"""
	def __init__(self, num_taps, train_size, training_path):
		gr.sync_block.__init__(self,
			name="dfe",
			in_sig=[np.float32],
			out_sig=[np.float32])

		self.training_path = training_path # Path where the file is stored
		self.current_count = 0 # keeps track of how much data has arrived
		self.num_taps = num_taps # Number of input samples to use for predicting the current symbol
		self.train_size = train_size # Number of samples to use for training
		self.weights = np.zeros([self.num_taps, 1]) # parameters of the feedforward LMS
		self.weights1 = np.zeros([self.num_taps, 1]) # parameters of the feedback LMS
		self.store_training = np.zeros([self.train_size]) # This is where we store the incoming training values
		self.get_expected() # Loading the training sequence in the beginning ( Target )
		self.buffer = np.zeros([self.num_taps - 1]) # Buffer for keeping the input to the feedforward(Remembering just the last few inputs)
		self.buffer_count = 0 # Keeps track of the position in the buffer
		self.buffer1 = np.zeros([self.num_taps]) # Buffer for keeping the input to the feedback loop
		self.buffer1_count = 0 # Keeps track of the position in the buffer for feedback
		self.lms = False # Flag to convert DFE to LMS

	def get_expected(self): # Program to get the expected training samples

		f = open(self.training_path, 'rb') #opening the training file in byte mode
		for i in f: #iterating over the file
			string_format = str([str(i)]) #Some ghapla because of python2
		self.expected = np.array(string_format[2:-2].split('\\x0')[1:]).astype(np.float32)[0:self.train_size] # Another ghapla to get the training sequence to train on

	def train(self):

		print('In training')

		self.training_data = np.zeros([self.train_size-self.num_taps+1, self.num_taps]) # Initialising the training matrix
		self.training_label = np.zeros([self.train_size-self.num_taps+1]) # Initialising the labels for the training matrix
		
		for i in range(self.num_taps-1, self.train_size):
			self.training_data[i-self.num_taps+1] = self.store_training[i-self.num_taps+1:i+1] # Converting the store_training to trainable matrix
			self.training_label[i-self.num_taps+1] = self.expected[i] # Corresponding labels

		self.weights = np.matmul(np.matmul(np.linalg.inv(np.matmul(np.transpose(self.training_data), self.training_data)), np.transpose(self.training_data)), self.training_label) # Here is where the magic is happening. (Training)

		if not self.lms:

			self.training_label_feedback = (self.training_label - np.matmul(self.training_data, self.weights))[1:] # Expected for feedback = Actual Expected - output of Feedforward LMS
			self.training_data = np.zeros([self.train_size-self.num_taps, self.num_taps])# Initialising the training matrix for feedback
			for i in range(self.num_taps, self.train_size):
				self.training_data[i-self.num_taps] = self.expected[i - self.num_taps:i] # Converting the expected to train matrix

			self.weights1 = np.matmul(np.matmul(np.linalg.inv(np.matmul(np.transpose(self.training_data), self.training_data)), np.transpose(self.training_data)), self.training_label_feedback)

	def test(self, input):

		print('In testing')
		# Converting the input array to format in which we can get the output Y = XW

		test_input = np.zeros([input.shape[0], self.num_taps])
		
		for i in range(input.shape[0]):
			if i - self.num_taps<0:
				test_input[i][0:self.num_taps - 1 - i] = self.buffer[i:]
				test_input[i][self.num_taps - 1 - i:] = input[0:i+1]
			else:
				test_input[i] = input[i-self.num_taps+1:i+1]

		self.buffer = input[-self.num_taps+1:]

		if self.lms:

			to_send = np.matmul(test_input, self.weights)

			for i in range(to_send.shape[0]):
				if to_send[i] <0.5:
					to_send[i] = 0 
				else:
					to_send[i] = 1

		else:

			

			to_send_first = np.matmul(test_input, self.weights)
			to_send = np.zeros_like(input)

			test_input_feedback = np.zeros([input.shape[0], self.num_taps])
			
			for i in range(input.shape[0]):
				if i - self.num_taps<0:
					test_input_feedback[i][0:self.num_taps - i] = self.buffer1[i:]
					test_input_feedback[i][self.num_taps - i:] = to_send[0:i]
					feedback_output_i = np.matmul(test_input_feedback[i], self.weights1)
					to_send[i] = to_send_first[i] + feedback_output_i
					if to_send[i] < 0.5:
						to_send[i] = 0
					else:
						to_send[i] = 1
				else:
					test_input_feedback[i] = to_send[i-self.num_taps:i]
					feedback_output_i = np.matmul(test_input_feedback[i], self.weights1)
					to_send[i] = to_send_first[i] + feedback_output_i
					if to_send[i] < 0.5:
						to_send[i] = 0
					else:
						to_send[i] = 1


			self.buffer1 = to_send[-self.num_taps:]

		return to_send

	def work(self, input_items, output_items):
		
		in0 = input_items[0]
		out = output_items[0]

		# Logic for handling multiple input samples in a single run

		if self.current_count + in0.shape[0]>self.train_size and self.current_count<self.train_size:
			self.store_training[self.current_count:] = in0[0:self.train_size - self.current_count]
			self.train()
			out[0:self.train_size - self.current_count] = 0
			out[self.train_size - self.current_count:] = self.test(in0[self.train_size - self.current_count:])
			self.current_count += in0.shape[0]
		elif self.current_count + in0.shape[0]<self.train_size:
			self.store_training[self.current_count:self.current_count+in0.shape[0]] = in0
			self.current_count += in0.shape[0]
			out[:] = 0
		else:
			out[:] = self.test(in0)

		return len(output_items[0])

