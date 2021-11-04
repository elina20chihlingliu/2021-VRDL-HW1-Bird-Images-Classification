# 2021-VRDL-HW1

## ✓ ML Code Completeness Checklist

The ML Code Completeness Checklist consists of six items:

1. **Requirements**
2. **Files** 
3. **Training code + Evaluation code** 
4. **Evaluation code + Load the models**
5. **ResNet152V2 and Xception load links**
6. **code_explanation**


## Requirements

To install requirements:

```setup
pip install -r requirements.txt
```

>📋  requirements.txt contains all python packages we need in the project.

## Files 

>📋  Please put the following files in the same directory.
1. [training_images]
2. [testing_images]
3. [models]
4. [code_explanation]
5. classes.txt
6. testing_img_order.txt
7. training_labels.txt
8. 310706002_main.py
9. 310706002_eval_loadmodels.py

## Training code + Evaluation code

To train the model(s) in the paper, run this command:

```train
python 310706002_main.py
```
>📋  **310706002_main.py** is full code containing data pre-process, training phase, testing phase and generate answer.txt.\
>If you want to retrain models, just run 310706002_main.py (ex: python 310706002_main.py) and you can get answer.txt.\
It may take 1.5~2.5 hours to run 310706002_main.py.
    
## Evaluation code + Load the models 

To evaluate and produce answer.txt without training model again, run:

```eval
python 310706002_eval_loadmodels.py
```

>📋  **310706002_eval_loadmodels.py** only has testing phase to produce answer.txt. It has to load pretrained models in models file.\
In the models file, there are five models parameters that I pretrained and saved which I used to achieve the baseline.\
If you want to evaluate test data without training model again, run 310706002_eval_loadmodels.py (ex: python 310706002_eval_loadmodels.py) and you can get answer.txt.\
It may take 1~2 hours to run 310706002_eval_loadmodels.py.\

The following is what models file looks like:\
\[models]\
---[my_model0]\
---[my_model1]\
---[my_model2]\
---[my_model3]\
---[my_model4]
    
```eval
python eval.py --model-file mymodel.pth --benchmark imagenet
```
    
## ResNet152V2 and Xception models weight download links

>📋  Here are the weight download links of ResNet152V2 and Xception models. When running 310706002_main.py or 310706002_eval_loadmodels.py, its will be downloaded automatically.

```pretrained_models
Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet152v2_weights_tf_dim_ordering_tf_kernels_notop.h5
\Downloading data from https://storage.googleapis.com/tensorflow/keras-applications/xception/xception_weights_tf_dim_ordering_tf_kernels_notop.h5
```
## code_explanation

[code_explanation]\
---feature_extraction_used_pretained_models.py\
---predict.py\
---read_image.py\
---training_phase.py\

>📋  code_explanation file includes each segments of the code in 310706002_main.py. 
In order to explain the code more detail, I separated the code into four segments and each of them were saved as python file.
Those python files cannot be executed, because they are only for reading the code in detail including some programming notes.
If you wanna know more about the code, you can check code_explanation file.
