#!/bin/bash

source activate $PYTHON_ENV
service supervisord start
service nginx start
