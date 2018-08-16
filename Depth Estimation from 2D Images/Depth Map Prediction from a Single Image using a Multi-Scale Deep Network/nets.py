import keras
from keras.layers import (Conv2D, MaxPooling2D, AveragePooling2D, Dense,
                          Concatenate, Input, Dropout, BatchNormalization)
from keras.models import Model


# based on NYUDepth dataset, modified
input_shape = (304,228,3)
output_shape = (63, 44, 1)


def get_models(input_shape=input_shape, output_shape=output_shape):
    inputs = Input(input_shape)

    ### Coarse model ###
    coarse_1a = Conv2D(128, (7,7), strides=2, bias_initializer="ones")(inputs)
    coarse_1b = MaxPooling2D(padding='same')(coarse_1a)

    coarse_1c = Conv2D(128, (5,5))(coarse_1b)

    coarse_2 = Conv2D(512, (3,3), activation='relu',
                      padding='valid')(coarse_1c)


    coarse_3 = Conv2D(512, (3,3), activation='relu',
                     padding='valid')(coarse_2)

    coarse_4 = Conv2D(512, (3,3), activation='relu',
                     padding='valid')(coarse_3)

    coarse_5 = Conv2D(512, (3,3), activation='relu',
                     padding='valid')(coarse_4)

    coarse_6a = Dense(4096)(coarse_5)
    coarse_6b = Dropout(0.2)(coarse_6a)

    coarse_7 = Dense(1, activation="relu")(coarse_6b)

    model_coarse = Model(inputs, coarse_7)


    ### Fine model ###
    fine_1a = Conv2D(63, (9,9), strides=2,
                 activation='relu')(inputs)
    fine_1b = AveragePooling2D()(fine_1a)

    fine_2 = Conv2D(63, (7,7), activation='relu')(fine_1b)

    fine_3 = Conv2D(128, (6,6), activation='relu')(fine_2)

    fine_4 = Concatenate()([fine_3, coarse_7])

    fine_5 = Dense(1, activation='relu')(fine_4)

    model_fine = Model(inputs, fine_5)


    return model_coarse, model_fine
