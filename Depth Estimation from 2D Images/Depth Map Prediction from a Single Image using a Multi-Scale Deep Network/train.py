# For reproducability
import numpy as np
np.random.seed(3)

import keras
from keras.optimizers import SGD, Adam
from nets import get_models
from loss_functions import SIMSE
import matplotlib.pyplot as plt
import os
from PIL import Image

# based on NYUDepth dataset, modified
input_shape = (304,228,3)
output_shape = (63, 44, 1)

# Other params
visualize = True
save = True
batch_size = 16
epochs_coarse = 5
epochs_fine = 20
optimizer_coarse = Adam() # SGD(lr=0.001, momentum=0.9)
optimizer_fine = optimizer_coarse

# load images and depths, and squeeze in [0,1]
imgs = np.array([np.array(Image.open("depth_dataset/rgb_data/"+i))/255.
                for i in os.listdir("depth_dataset/rgb_data")]).astype(np.float32)
depths = np.array([np.array(Image.open("depth_dataset/depth_target/"+i).convert("L"))/255.
        for i in os.listdir("depth_dataset/depth_target")]).reshape((imgs.shape[0],
                                                                     output_shape[0],
                                                                     output_shape[1],
                                                                     1)).astype(np.float32)

# Load models
model_coarse, model_fine = get_models(input_shape, output_shape)

# Compile; SIMSE seems to be working better than SILoss
model_coarse.compile(optimizer_coarse, loss=SIMSE)
model_fine.compile(optimizer_fine, loss=SIMSE)

# Train coarse model
h1 = model_coarse.fit(imgs, depths, batch_size=batch_size, epochs=epochs_coarse)

# Train fine model
h2 = model_fine.fit(imgs, depths, batch_size=batch_size, epochs=epochs_fine)

if visualize:

    preds = model_coarse.predict(imgs[:1].reshape((1,
                                                   input_shape[0],
                                                   input_shape[1],
                                                   input_shape[2])))
    preds2 = model_fine.predict(imgs[:1].reshape((1,
                                                   input_shape[0],
                                                   input_shape[1],
                                                   input_shape[2])))

    fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(1,5, )#figsize=(16,12))

    ax0.imshow(imgs[0])
    ax0.set_title("Input image")
    ax1.imshow(preds[0].reshape(output_shape[0:2]), cmap='gray')
    ax1.set_title("Coarse prediction")
    ax2.imshow(preds2[0].reshape(output_shape[0:2]), cmap='gray')
    ax2.set_title("Fine prediction")
    ax3.imshow(depths[0].reshape(output_shape[0:2]), cmap='gray')
    ax3.set_title("Ground truth")
    ax4.plot(h1.history["loss"], label='Coarse model loss', c='blue')
    ax4.plot(h2.history["loss"], label='Fine model loss', c='red')
    ax4.set_title("Loss")
    ax4.legend()

    plt.show()

if save:
    model_fine.save("fine.h5")
    model_coarse.save("coarse.h5")
