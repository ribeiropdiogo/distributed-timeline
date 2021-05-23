#!/bin/bash

export PYTHONPATH='tests:storage'
python3 -m unittest test_storage
