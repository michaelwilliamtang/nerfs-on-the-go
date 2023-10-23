# NeRFs on the Go: ARCam → Instant-NGP

<img src="assets/app_layout.png" width="450"/> <img src="assets/fox.gif" width="225"/>

A concise pipeline for using outputs from the ARCam capture app to train NeRFs using Instant-NGP.

We adapt the PyTorch implementation of Instant-NGP from [here](https://github.com/ashawkey/torch-ngp).

# Setup
Create a conda environment with Python 3.7.16, and install dependencies:
```
conda create -n ngp python=3.7.16
conda activate ngp
conda install pip
pip install -r requirements.txt
```
Note that we specified dearpygui 1.9.0 in the requirements, as other versions do not work on Della.

# Capture + train
To capture and process the captured data:
1. Use capture app *in the portrait orientatin* to capture some pictures of the scene - each shutter press generates a new frame.
2. The raw scene captures will be available in a newly created bundle subdirectory titled `bundle-[date and time]/` under the ARCam directory in the Files app on the iPhone. Transfer (e.g. AirDrop) this new subdirectory under the `data_ARCam/` repository directory, and rename it into something of the form `data_[scene_name_here]/`.
3. Run `bash process.sh [scene_name_here]` to generate processed NeRF-formatted data, which will be available at `data_processed_ARCam/data_processed_[scene_name_here]`.

You may then run any downstream tasks on the data. For example, to train and evaluate an InstantNGP on this scene for 200 iterations:
```
python main_nerf.py data_processed_ARCam/data_processed_[scene_name_here] --workspace [output_directory_name_here] --iters 200
```

To do *just evaluation / rendering* on an existing trained NeRF, run:
```
python main_nerf.py data_processed_ARCam/data_processed_[scene_name_here] --workspace [output_directory_name_here] -O --test
```

Other Instant-NGP and NeRF-related functionality are listed in the main README linked [here](https://github.com/ashawkey/torch-ngp#usage), and also provided in the file `readme_torch_ngp.md`.
