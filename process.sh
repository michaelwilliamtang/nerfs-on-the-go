#!/bin/bash
python convert_binaries.py -d data_ARCam/data_$1
python arcam_to_nerf.py data_processed_ARCam/data_processed_$1/

