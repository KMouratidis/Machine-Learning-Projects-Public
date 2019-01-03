## Multi-task, Multilabel InceptionV3 & SSGAN 

This project is about creating a Generative Adversarial Network where the discriminator was an InceptionV3 model and the 
dataset was CIFAR-100. The generator part was mostly taken from <a href="https://github.com/samrussell/ssgan">
Sam Russell's SSGAN implementation</a>.  One of the changes was the use of additional upsampling layers since CIFAR-100 images
have size 32x32. The project also used <a href="https://github.com/Hyperparticle/one-pixel-attack-keras">Dan Kondratyuk's 
implementation of the one-pixel-attack</a>. Code is private; commission via Upwork.

### Model outline:
<img width=85% src="https://github.com/KMouratidis/Machine-Learning-Projects-Public/blob/master/Multilabel%2C%20Multitask%20InceptionV3%20%26%20GAN/Iv3_GAN-1.jpg">

### GAN generator:
<img height=30% width=50% src="https://github.com/KMouratidis/Machine-Learning-Projects-Public/blob/master/Multilabel%2C%20Multitask%20InceptionV3%20%26%20GAN/Generator_GAN.jpg">

