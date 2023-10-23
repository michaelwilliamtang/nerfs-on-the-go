import math
import os
import json
import argparse

import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('data', help='data directory')
args = parser.parse_args()

dirname = args.data

# create image dir
if not os.path.exists(dirname + 'images'):
    os.mkdir(dirname + 'images')
    
# read all frames
fname = dirname + "frame_bundle.npz"
bundle = np.load(fname, allow_pickle=True)
num_frames = int((len(bundle.keys()) - 1) / 4)

# utilities
# from colmap script
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()
def sharpness(imagePath):
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    return fm

def np_to_lst_of_lsts(arr):
    return [[arr[i][j] for j in range(4)] for i in range(4)]

def get_tree(bundle, num_frames):
    # depth = bundle['depth_{0}'.format(0)] # lidar depth in meters, numpy array
    
    # save imgs as jpgs (assumes img directory has been created)
    for frame in range(num_frames):
        img = bundle['img_{0}'.format(frame)] # camera image, numpy array
        im = Image.fromarray(img)
        image_path = dirname + 'images/{:04d}.jpg'.format(frame+1) # 1-indexed
        if not os.path.exists(image_path):
            im.save(image_path)
    
    # compute various values
    info = bundle['info_{0}'.format(0)].item() # pose + camera information, dictionary
    intrinsics = info['intrinsics'].astype('float64') # is given in float32, which is not json serializable
    (fl_x, shear, cx) = intrinsics[0]
    (_, fl_y, cy) = intrinsics[1]
    camera_angle_x = fl_x * math.pi/180
    camera_angle_y = fl_y * math.pi/180
    # w = cx * 2
    # h = cy * 2
    w = 1440
    h = 1920
    k1 = 0
    k2 = 0
    p1 = 0
    p2 = 0
    
    # create transforms dict
    frames = []
    for frame in range(num_frames):
        image_path = dirname + 'images/{:04d}.jpg'.format(frame+1) # 1-indexed
        info = bundle['info_{0}'.format(frame)].item() # pose + camera information, dictionary
        camera_to_world = np.linalg.inv(info['world_to_camera'].astype('float64')) # is given in float32, which is not json serializable
        frames.append({
            'file_path': 'images/{:04d}.jpg'.format(frame+1), # 1-indexed
            'sharpness': sharpness(image_path),
            'transform_matrix': np_to_lst_of_lsts(camera_to_world),
        })
    return {
        'camera_angle_x': camera_angle_x,
        'camera_angle_y': camera_angle_y,
        'fl_x': fl_x,
        'fl_y': fl_y,
        'k1': k1,
        'k2': k2,
        'p1': p1,
        'p2': p2,
        'cx': cx,
        'cy': cy,
        'w': w,
        'h': h,
        'aabb_scale': 4,
        'frames': frames,
    }

# compute and save transforms
root = get_tree(bundle, num_frames)
with open(dirname + 'transforms.json', 'w') as f:
    json.dump(root, f)
