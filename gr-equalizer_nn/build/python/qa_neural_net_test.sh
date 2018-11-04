#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/allai/Desktop/Study/Comm/Lab_comm/Project/gr-equalizer_nn/python
export PATH=/home/allai/Desktop/Study/Comm/Lab_comm/Project/gr-equalizer_nn/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/allai/Desktop/Study/Comm/Lab_comm/Project/gr-equalizer_nn/build/swig:$PYTHONPATH
/usr/bin/python2 /home/allai/Desktop/Study/Comm/Lab_comm/Project/gr-equalizer_nn/python/qa_neural_net.py 
