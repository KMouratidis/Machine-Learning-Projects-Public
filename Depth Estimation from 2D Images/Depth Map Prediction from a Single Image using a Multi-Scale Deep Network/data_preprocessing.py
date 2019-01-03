import os
import numpy as np
import h5py
import cv2
import matplotlib.pyplot as plt


file = "nyu_depth_v2_labeled.mat" # data
img_folder = "depth_dataset/rgb_data"
dep_folder = "depth_dataset/depth_target"

input_shape = (304,228,3)
output_shape = (63, 44, 1)

# if the directories don't  exist, create them
if not os.path.exists(img_folder):
    os.makedirs(img_folder)
if not os.path.exists(dep_folder):
    os.makedirs(dep_folder)

# load the data
f = h5py.File(file)

# save an example input image
fig = plt.figure(figsize=(14,11))
plt.imshow(f["images"][0].reshape((640,480,3)))
fig.savefig("input_data_example.jpg")

# save an example output image
fig = plt.figure(figsize=(14,11))
plt.imshow(f['depths'][0].reshape((640,480))) # optionally: cmap='gray'
fig.savefig("output_data_example.jpg")

# Save images in folders
# Adapted from: https://github.com/gautam678/Pix2Depth/blob/master/save_all_images.py
def save_image_dep(i, ret=False, input_shape=input_shape, output_shape=output_shape):

    img = f['images'][i]
    depth = f['depths'][i]

    img_ = np.empty(input_shape)
    img_[:,:,0] = cv2.resize(img[2,:,:].T, input_shape[:2][::-1])
    img_[:,:,1] = cv2.resize(img[1,:,:].T, input_shape[:2][::-1])
    img_[:,:,2] = cv2.resize(img[0,:,:].T, input_shape[:2][::-1])

    depth_ = np.empty(input_shape)
    depth_[:,:,0] = cv2.resize(depth[:,:].T, input_shape[:2][::-1])
    depth_[:,:,1] = cv2.resize(depth[:,:].T, input_shape[:2][::-1])
    depth_[:,:,2] = cv2.resize(depth[:,:].T, input_shape[:2][::-1])

    depth_ = 255.*cv2.normalize(depth_, 0, 255, cv2.NORM_MINMAX)
    depth_ = cv2.resize(depth_, output_shape[:2][::-1])

    if ret:
        img_ = img_/255.0
        return img_
    else:
        cv2.imwrite(os.path.join(img_folder,'img_{}.jpg'.format(i)), img_)
        cv2.imwrite(os.path.join(dep_folder,'dep_{}.jpg'.format(i)), depth_)


if __name__ == "__main__":

    for i in range(len(f['images'])):
        save_image_dep(i)
