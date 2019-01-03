import keras
import keras.backend as K
import tensorflow as tf
import cv2
import numpy as np

n = 75 * 55 # output size, flattened, since metrics work pixel-wise
lamda = 0.5 # the λ normalizing constant, as defined in the paper
e = 1e-7 # for numerical stability

# Scale-Invariant Mean Squared Error
def SIMSE(y_true, y_pred):
    alpha = K.sum(K.log(y_true+e) - K.log(y_pred+e)) / n
    s = K.log(y_pred+e) - K.log(y_true+e) + alpha
    return K.sum(K.pow(s, 2)) / (2*n)

# Scale-Invariant Loss
def SILoss(y_true, y_pred):
    l2 = K.sum((K.log(y_pred + e) - K.log(y_true + e))**2) / n
    reg = (lamda/n**2) * (K.sum(K.log(y_pred + e) - K.log(y_true + e)))**2
    return  l2 - reg

if __name__ == "__main__":

    img1 = cv2.imread("depth_dataset/rgb_data/img_1.jpg")
    img2 = cv2.imread("depth_dataset/rgb_data/img_2.jpg")
    img1b = img1.copy()
    img1b[0, 0:2] = 0. # set two top pixels to zero

    print("Testing...")
    with tf.Session() as sess:
        same_simse = sess.run(SIMSE(img1, img1))
        same_siloss = sess.run(SILoss(img1, img1))
        two_pix_simse = sess.run(SIMSE(img1, img1b))
        two_pix_siloss = sess.run(SILoss(img1, img1b))
        different_simse = sess.run(SIMSE(img1, img2))
        different_siloss = sess.run(SILoss(img1, img2))

    print("Testing Scale-Invariant MSE with the same images:",same_simse)
    print("Testing Scale-Invariant MSE with different images:",different_simse)
    print()
    print("Testing Scale-Invariant Loss with the same images:",same_siloss)
    print("Testing Scale-Invariant Loss with different images:",different_siloss)
    print()
    print("Testing Scale-Invatiant MSE, same image, 2 blackened pixels:", two_pix_simse)
    print("Testing Scale-Invatiant LOSS, same image, 2 blackened pixels:", two_pix_siloss)
