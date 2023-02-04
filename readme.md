# Style Transfer 
This repository is our implementation of [A Neural Algorithm of Artistic Style](https://arxiv.org/abs/1508.06576) paper, that adds an interactive drag & drop GUI for the ease of use.

## Results 

|Original Image|Style Image|Transfer Results|
| ------ | ------ | ------ |
|<img src="https://github.com/SzymonOzog/StyleTransfer/blob/main/StyleTransfer/StyleTransfer/Results/silly_shiba.jpg?raw=true" width="200" height="200">|<img src="https://github.com/SzymonOzog/StyleTransfer/blob/main/StyleTransfer/StyleTransfer/Results/s2.jpg?raw=true" width="200" height="200">|<img src="https://github.com/SzymonOzog/StyleTransfer/blob/main/StyleTransfer/StyleTransfer/Results/TransferedShiba.png?raw=true"width="200" height="200">|

## Tech
The style gradients were calculated and applied using PyTorch 
The GUI was created with PyQt 
Image reading and resizing is a courtesy of OpenCV