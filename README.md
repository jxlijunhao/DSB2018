# Description

Kaggle 2018 Data Science Bowl: find the nuclei in divergent images to advance medical discovery

## Development Plan:

* Platform and framework
  - [x] PyTorch
  - [x] macOS
  - [x] Ubuntu
* Explore model architecture
  - [x] UNet
  - [x] Dropout
  - [x] Batch normalization
  - [ ] Transfer learning
* Hyper-parameter tunning
  - [ ] Learning rate
  - [ ] Input size
  - [ ] Confidence level threshold
  - [ ] ...
* Data argument
  - [x] Random crop
  - [x] Random horizontal and vertical flip
  - [x] Random aspect resize
  - [ ] Random rotate
  - [ ] Random color adjustment
* Preprocess
  - [x] Input normalization
  - [x] Binarize label
  - [ ] Cross-validation split
* Computation performance
  - [x] CPU
  - [x] GPU 
  - [x] Multiple subprocess workers (IPC) 
  - [x] Pretech / cache images
* Statistics and error analysis
  - [x] Mini-batch time cost (IO and compute)
  - [x] Mini-batch loss
  - [x] Mini-batch IOU
  - [x] Visualize prediction result
  - [ ] Visualize log summary in TensorBoard
  - [ ] Graph visualization
  - [ ] Running length output

## Setup development environment

* Install Python 3.5 and pip
* Install [PyTorch](http://pytorch.org/)
    ```
    // macOS
    $ pip3 install http://download.pytorch.org/whl/torch-0.3.0.post4-cp35-cp35m-macosx_10_6_x86_64.whl 
    $ pip3 install torchvision 
    // Ubuntu
    $ pip3 install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp35-cp35m-linux_x86_64.whl 
    $ pip3 install torchvision
    ```

* Install dependency python packages
    ```
    $ pip3 install -r requirements.txt
    ```

## Prepare data

[Download](https://www.kaggle.com/c/data-science-bowl-2018) and uncompress to `data` folder as below structure,

```
.
├── README.md
├── config.py
├── data
    ├── noisy_label.txt
    ├── stage1_test
    │   ├── 0114f484a16c152baa2d82fdd43740880a762c93f436c8988ac461c5c9dbe7d5
    │   └── ...
    └── stage1_train
        ├── 00071198d059ba7f5914a526d124d28e6d010c92466da21d4a04cd5413362552
        └── ...
```

## Command line usage

* Train model
    ```
    $ python3 train.py
        usage: train.py [-h] [--resume] [--no-resume] [--cuda] [--no-cuda] [--epoch EPOCH]

        Grand new training ...
        Training started...
        // Iteration        Mini-batch elapsed time     Mini-batch loss         Mini-batch IoU 
        Epoch: [1][0/67]    Time: 0.928 (io: 0.374)	    Loss: 0.6101 (0.6101)   IoU: 0.000 (0.000)	
        Epoch: [1][10/67]   Time: 0.140 (io: 0.051)	    Loss: 0.4851 (0.5816)   IoU: 0.000 (0.000)
        ...
        Epoch: [10][60/67]  Time: 0.039 (io: 0.002)	    Loss: 0.1767 (0.1219)   IoU: 0.265 (0.296)
        Training finished...
        ...
    
    // automatically save checkpoint every 10 epochs
    $ ls checkpoint
        current.json   ckpt-10.pkl
    ```

* Evaluate test dataset, will show side-by-side images on screen
    ```
    $ python3 valid.py
    ```

## Known Issues

* Error: multiprocessing.managers.RemoteError: AttributeError: Can't get attribute 'PngImageFile'  
    ```
    Reproduce rate: 1/10  
    Root cause: PyTorch subprocess workers failed to communicate shared memory.  
    Workaround: Ignore and issue command again
    ```
