#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/vaibhav/GNU/gr-equalizer_dfe/python
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/vaibhav/GNU/gr-equalizer_dfe/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/vaibhav/GNU/gr-equalizer_dfe/build/swig:$PYTHONPATH
/usr/bin/python2 /home/vaibhav/GNU/gr-equalizer_dfe/python/qa_dfe.py 
