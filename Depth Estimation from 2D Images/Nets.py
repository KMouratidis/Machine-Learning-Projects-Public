import keras
from keras.layers import (Conv2D, MaxPooling2D, AveragePooling2D, Dense,
                          Concatenate, Input, Dropout, BatchNormalization)
from keras.models import Model


# based on NYUDepth dataset
input_shape = (304,228,3)
output_shape = (74, 55, 1)


def get_models(input_shape=input_shape, output_shape=output_shape):
    inputs = Input(input_shape)

    ### Coarse model ###
    # strides 4 didn't provide correct output, so I changed to 2
    coarse_1a = Conv2D(96, (11,11), strides=2, bias_initializer="ones")(inputs)
    coarse_1b = BatchNormalization()(coarse_1a)
    coarse_1c = MaxPooling2D(padding='same')(coarse_1b)

    coarse_2a = Conv2D(256, (5,5), #activation='relu',
                      padding='same')(coarse_1c)
    # Added batch normalization because it seems to increase performance
    coarse_2b = BatchNormalization()(coarse_2a)

    # this also downsampled too much and concatenation sizes were inconsistent
    #coarse_2b = MaxPooling2D(padding='same')(coarse_2a)
    coarse_3a = Conv2D(384, (3,3), #activation='relu',
                     padding='same')(coarse_2b)
    coarse_3b = BatchNormalization()(coarse_3a)

    coarse_4a = Conv2D(384, (3,3), #activation='relu',
                     padding='same')(coarse_3b)
    coarse_4b = BatchNormalization()(coarse_4a)

    coarse_5 = Conv2D(256, (3,3), #activation='relu',
                     padding='same')(coarse_4b)

    coarse_6a = Dense(4096)(coarse_5)
    coarse_6b = Dropout(0.2)(coarse_6a)

    coarse_7 = Dense(1, activation="relu")(coarse_6b)

    model_coarse = Model(inputs, coarse_7)

    ### Fine model ###
    fine_1a = Conv2D(63, (9,9), strides=2,
                     activation='relu')(inputs)
    fine_1b = AveragePooling2D(padding='same')(fine_1a)
    fine_2 = Concatenate()([fine_1b, coarse_7])
    fine_3 = Conv2D(64, (5,5), padding='same',
                    activation='relu')(fine_2)
    fine_4 = Conv2D(1, (5,5), padding='same',
                   activation='relu')(fine_3)


    model_fine = Model(inputs, fine_4)

    return model_coarse, model_fine
