import keras
import keras.backend as K

n = 75 * 55 # output size, flattened, since metrics work pixel-wise
lamda = 0.5 # the λ normalizing constant, as defined in the paper
e = 1e-6 # for numerical stability

# Scale-Invariant Mean Squared Error
def SIMSE(y_true, y_pred):
    s = K.log(y_pred+e) - K.log(y_true+e) + K.sum(K.log(y_true+e) - K.log(y_pred+e)) / n
    return K.sum(K.pow(s, 2)) / (2*n)

# Scale-Invariant Loss
def SILoss(y_true, y_pred):
    l2 = K.sum((K.log(y_pred + e) - K.log(y_true + e))**2) / n
    reg = (lamda/n**2) * (K.sum(K.log(y_pred + e) - K.log(y_true + e)))**2
    return  l2 - reg + e
