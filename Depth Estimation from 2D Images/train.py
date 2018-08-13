import keras
from keras.optimizers import SGD, Adam
from nets import get_models
from loss_functions import SIMSE
import matplotlib.pyplot as plt

# based on NYUDepth dataset
input_shape = (304,228,3)
output_shape = (74, 55, 1)

# Other params
visualize = True
batch_size = 16
epochs = 10
optimizer1 = SGD(lr=0.001, momentum=0.9)
optimizer2 = Adam()

# load images and depths, and squeeze in [0,1]
imgs = np.array([np.array(Image.open("depth_dataset/rgb_data/"+i))/255.
        for i in os.listdir("depth_dataset/rgb_data")]).astype(np.float32)
depths = np.array([np.array(Image.open("depth_dataset/depth_target/"+i).convert("L"))/255.
        for i in os.listdir("depth_dataset/depth_target")]).reshape((imgs.shape[0], 74, 55, 1)).astype(np.float32)

# Load models
model_coarse, model_fine = get_models(input_shape, output_shape)

# Compile; SIMSE seems to be working better than SILoss
model_coarse.compile(optimizer, loss=SIMSE)
model_fine.compile(optimizer, loss=SIMSE)

# Train coarse model
h1 = model_coarse.fit(imgs, depths, batch_size=batch_size, epochs=epochs)

# Freeze coarse and train fine model
model_coarse.trainable = False
h2 = model_fine.fit(imgs, depths, batch_size=batch_size, epochs=epochs)

if visualize:

    preds = model_coarse.predict(imgs[:1].reshape((1,74, 55, 1)))
    preds2 = model_fine.predict(imgs[:1].reshape((1,74, 55, 1)))

    fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(1,5, )#figsize=(16,12))

    ax0.imshow(imgs[0])
    ax0.set_title("Input image")
    ax1.imshow(preds[0].reshape((74,55)), cmap='gray')
    ax1.set_title("Coarse prediction")
    ax2.imshow(preds2[0].reshape((74,55)), cmap='gray')
    ax2.set_title("Fine prediction")
    ax3.imshow(depths[0].reshape((74,55)), cmap='gray')
    ax3.set_title("Ground truth")
    ax4.plot(h1.history["loss"], label='Coarse model loss', c='blue')
    ax4.plot(h2.history["loss"], label='Fine model loss', c='red')
    ax4.set_title("Loss")
    ax4.legend()

    plt.show()
