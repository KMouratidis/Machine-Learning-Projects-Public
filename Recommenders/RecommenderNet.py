import tensorflow as tf
import keras
from keras.layers import Dense, Dropout, Input, Concatenate
from keras.models import Sequential, Model
from keras.optimizers import SGD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from utilities import load_dataset

def train(epochs=100, batch_size=512, validation_split=0.1,
          drop_probability=0.5, extra_training=True, save=False):
    # These take some time to load, and need at least 650 MB of memory
    print("Loading dataset...")
    Y, features = load_dataset()

    print("Saving item list...")
    with open("anime_list.txt", 'w') as f:
        for anime in list(Y.columns):
            f.write(anime+"\n")

    print("Creating feature and target data...")
    # This mask drops (with 50% probability) values across our dataset
    mask = np.random.randint(1//drop_probability+1, size=Y.shape)
    X = Y * mask
    # Convert user's item-ratings to user's features
    X = X @ features
    # normalizea
    X = X.apply(lambda x: x / x.max(), axis=1)

    print("Defining model...")
    ## Model definition and training
    inp = Input(shape =(X.shape[1],))
    x = Dense(64, activation='relu')(inp)
    x = Dense(128, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    out = Dense(Y.shape[1], activation='linear')(x)
    model = Model(inp, out)
    print(model.summary())
    model.compile(SGD(lr=0.01, momentum=0.9, decay=1e-2), loss='mse')

    print("Training model...")
    h = model.fit(X, Y, batch_size, epochs=epochs,
                  validation_split=validation_split)

    plt.figure(figsize=(12,8))
    plt.plot(np.arange(0,100), h.history['loss'],
             label="train_loss", color='blue')
    plt.plot(np.arange(0,100), h.history['val_loss'],
             label='val_loss', color='orange')

    if extra_training:
        print("Extra model training...")
        model.compile(SGD(lr=0.001, momentum=0.9, decay=1e-3), loss='mse')
        h2 = model.fit(X, Y, batch_size//2, epochs=epochs//5,
                       validation_split=validation_split)

        plt.plot(np.arange(100,120), h2.history['loss'], color='blue')
        plt.plot(np.arange(100,120), h2.history['val_loss'], color='orange')

    plt.legend()
    plt.show()

    if save:
        print("Saving model...")
        model.save('weights/'+save)

if __name__ == "__main__":
    train(save="anime_model.h5")
