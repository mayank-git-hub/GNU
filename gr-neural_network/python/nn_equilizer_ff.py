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
from net import feed_forward

class nn_equilizer_ff(gr.sync_block):
    """
    docstring for block nn_equilizer_ff
    """
    def __init__(self, batch_size, learning_rate, epochs, total_data):
        gr.sync_block.__init__(self,
            name="nn_equilizer_ff",
            in_sig=[np.float32],
            out_sig=[np.float32])

        #total_data = 10000

        self.total_data = total_data
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = learning_rate
        self.current_count = 0
        self.training_sequence = np.load('training_seq.npy')      # Will have to change it to something specific
        self.what_we_got = np.zeros(total_data)
        self.past_len_data = 10
        self.model = feed_forward()
        self.buffer = np.zeros(self.past_len_data)
        self.current_buffer = 0
        self.opt = torch.optim.Adam(self.parameters(), lr=config['lr'])
        self.loss = torch.nn.MSELoss()
        self.graph = []
        

    def train(self):

        idx = np.arange(self.total_data)[self.past_len_data:]

        self.model.train()

        self.opt.zero_grad()

        for epoch_i in range(self.epochs):

            for no in range(self.total_data//self.batch_size):

                random_idx = np.random.choice(idx, self.batch_size, replace=False)

                data = np.zeros([self.batch_size, self.past_len_data])

                for i in range(data.shape[0]):
                    data[i] = self.what_we_got[random_idx[i]-self.past_len_data:random_idx[i]]

                target = self.training_sequence[random_idx]

                data, target = Variable(torch.FloatTensor(data)), Variable(torch.FloatTensor(target)).unsqueeze(1)

                if torch.cuda.is_available():

                    data, target = data.cuda(), target.cuda()

                predicted = self.model(data)

                loss = self.loss(predicted, target)

                loss.backward()

                self.opt.step()

                self.opt.zero_grad()

                self.graph.append(loss.data.cpu().numpy())

        return np.sum(np.array(self.graph)*np.arange(len(self.graph)))/np.sum(np.arange(len(self.graph))) # return moving(weighted) average of the loss

    def test(self):
        #Predicting the current input after seeing the buffer

        data = Variable(torch.FloatTensor(np.vstack((self.buffer[self.current_buffer:], self.biffer[:self.current_buffer])))).unsqueeze(0)
        if torch.cuda.is_available():
            data = data.cuda()

        predicted = self.model(data).data.cpu().numpy()[0]

        return predicted    

    def work(self, input_items, output_items):

        in0 = input_items[0]
        out = output_items[0]

        self.buffer[self.current_buffer] = in0
        self.current_buffer = self.current_buffer%self.past_len_data

        if self.current_count<self.total_data:
            self.what_we_got[current_count] = in0
            out[:] = 0
            self.current_count += 1
        elif self.current_count == self.total_data:
            loss = self.train()
            self.model.test()
            self.current_count += 1
            out[:] = 0
        else:
            out[:] = self.test()

        return len(output_items[0])

