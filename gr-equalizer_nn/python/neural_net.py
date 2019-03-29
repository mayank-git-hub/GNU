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
import torch
from torch.autograd import Variable
import torch.nn as nn

class feed_forward(nn.Module):

    def __init__(self, input, output, hidden_nodes):

        super(feed_forward, self).__init__()

        self.lin1 = nn.Linear(input, hidden_nodes)
        self.act1 = nn.ReLU()
        self.lin2 = nn.Linear(hidden_nodes, output)


    def forward(self, data):

        data = self.lin1(data)
        data = self.act1(data)
        data = self.lin2(data)

        return data

class neural_net(gr.sync_block):
    """
    docstring for block neural_net
    """
    def __init__(self, seed, num_taps, batch_size, learning_rate, hidden_nodes, epochs, train_size, training_path):
        gr.sync_block.__init__(self,
            name="neural_net",
            in_sig=[np.float32],
            out_sig=[np.float32])


        self.seed = seed
        self.hidden_nodes = hidden_nodes
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        self.training_path = training_path
        self.current_count = 0
        self.num_taps = num_taps
        self.train_size = train_size
        self.store_training = np.zeros([self.train_size])
        self.get_expected() # TODO - What should be the true value?
        self.buffer = np.zeros([self.num_taps - 1])
        self.buffer_count = 0
        self.buffer1 = np.zeros([self.num_taps])
        self.buffer1_count = 0
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = learning_rate
        self.model = feed_forward(input=self.num_taps, output=1, hidden_nodes = self.hidden_nodes)
        self.cuda = torch.cuda.is_available() and False
        if self.cuda:
            self.model = self.model.cuda()
        
        self.opt = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss = torch.nn.MSELoss()
        self.graph = []

    def get_expected(self):

        f = open(self.training_path, 'rb')
        for i in f:
            string_format = str([str(i)])
        self.expected = np.array(string_format[2:-2].split('\\x0')[1:]).astype(np.float32)[0:self.train_size]
        
    def train(self):

        print('In training')

        self.training_data = np.zeros([self.train_size-self.num_taps+1, self.num_taps])
        self.training_label = np.zeros([self.train_size-self.num_taps+1])
        
        for i in range(self.num_taps-1, self.train_size):
            self.training_data[i-self.num_taps+1] = self.store_training[i-self.num_taps+1:i+1]
            self.training_label[i-self.num_taps+1] = self.expected[i]

        self.idx_size = self.training_label.shape[0]

        self.training_data = Variable(torch.FloatTensor(self.training_data))
        self.training_label = Variable(torch.FloatTensor(self.training_label))

        if self.cuda:
            self.training_label = self.training_label.cuda()
            self.training_data = self.training_data.cuda()

        self.model.train()

        self.opt.zero_grad()

        for epoch_i in range(self.epochs):

            for no in range(self.train_size//self.batch_size):

                random_idx = torch.LongTensor(np.random.choice(self.idx_size, self.batch_size, replace=False)).cuda()
                data, target = self.training_data[random_idx], self.training_label[random_idx]
                
                if self.cuda:

                    data, target = data.cuda(), target.cuda()

                predicted = self.model(data).squeeze()

                loss = self.loss(predicted, target)

                loss.backward()

                self.opt.step()

                self.opt.zero_grad()

                self.graph.append(loss.data.cpu().numpy())

        return np.sum(np.array(self.graph)*np.arange(len(self.graph)))/np.sum(np.arange(len(self.graph))) # return moving(weighted) average of the loss

    def test(self, input):
        #Predicting the current input after seeing the buffer

        print('In testing')

        test_input = np.zeros([input.shape[0], self.num_taps])
        
        for i in range(input.shape[0]):
            if i - self.num_taps<0:
                test_input[i][0:self.num_taps - 1 - i] = self.buffer[i:]
                test_input[i][self.num_taps - 1 - i:] = input[0:i+1]
            else:
                test_input[i] = input[i-self.num_taps+1:i+1]

        self.buffer = input[-self.num_taps+1:]

        data = Variable(torch.FloatTensor(test_input))
        if self.cuda:
            data = data.cuda()

        to_send = self.model(data).squeeze().data.cpu().numpy()

        for i in range(to_send.shape[0]):
            if to_send[i] <0.5:
                to_send[i] = 0 
            else:
                to_send[i] = 1

        return to_send   

    def work(self, input_items, output_items):
        
        in0 = input_items[0]
        out = output_items[0]

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

