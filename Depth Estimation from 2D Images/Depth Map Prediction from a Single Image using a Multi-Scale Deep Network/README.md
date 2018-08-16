## Depth Map Prediction from a Single Image using a Multi-Scale Deep Network

This is a rough implementation of the [homonymous paper](https://arxiv.org/abs/1406.2283) that takes the idea and metric suggested, 
modifying some layer parameters. More specifically, it increases the number of filters, swaps a maxpolling layer with a convolutional
layer in the coarse model, and adds another convolutional layer in the fine model. The main motivation behind this was that only a 
subset of the data mentioned in the paper were used, and without performing any augmentation. Experimental results show that with 
careful initialization, sufficient (for my purposes) performance can be achieved within ~10-20 minutes of training, or roughly
30 passes of the NYU data, using ~1300 images. 

You can find the data I used [in this folder](https://github.com/KMouratidis/Machine-Learning-Projects-Public/tree/master/Depth%20Estimation%20from%202D%20Images/Depth%20Map%20Prediction%20from%20a%20Single%20Image%20using%20a%20Multi-Scale%20Deep%20Network/depth_dataset) (~50 MB).
If you're interested in the original dataset, rather than this subset, you can find it [here](https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html) (~2.8 GB).

After grabbing the full dataset, if you want to quickly reproduce the results, run:

1. Create the folders and separate the data: `data_preprocessing.py`
2. Test the loss functions: `loss_functions.py`
3. Train the model (modify any parameters/configurations within the file): `train.py`


### Example output:
<img src="https://github.com/KMouratidis/Machine-Learning-Projects-Public/blob/master/Depth%20Estimation%20from%202D%20Images/Depth%20Map%20Prediction%20from%20a%20Single%20Image%20using%20a%20Multi-Scale%20Deep%20Network/train_set_prediction.png">
<img src="https://github.com/KMouratidis/Machine-Learning-Projects-Public/blob/master/Depth%20Estimation%20from%202D%20Images/Depth%20Map%20Prediction%20from%20a%20Single%20Image%20using%20a%20Multi-Scale%20Deep%20Network/test_set_prediction.png">
