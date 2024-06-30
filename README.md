# SpeedNet
## Computing Vehicle Speed using Dashcam video
![Speed Computation using Video](https://github.com/the-ray-kar/SpeedNet/blob/8862e644a07d6e337ca2b60dd4a941e81e55bd8c/diagrams/ModelRun5500.gif)
<br>
This project is on computing Vehicle Speed from DashCam Video. The dataset is taken from the [CommaAI Speed Challenge](https://github.com/commaai/speedchallenge). The dataset consists of 20400 frames with 20fps and Corresponding speed labels. You can obtain the data from [here](https://github.com/commaai/speedchallenge/tree/master/data).
<br>

## Methodology
I wanted not to intentionally use Optic Flow or Flow Nets but rather design the Neural Network architecture bymyself as a learning experience.
I came up with the following technique.
Input Video --> Select Relevant Road Profile --> Perspective Transform --> 3D Convolution Neural Network --> Exponential Smoothening --> Speed.
<br>
My idea was to the Neural net to pick the lane markings and compute speed. There is 10x7 kernel in neural net to gather spatial difference in features. The process is as per the .ipynb files naming.


## Neural Network Architure
![Architecture and Process](https://github.com/the-ray-kar/SpeedNet/blob/c3208e1976b19eec7599ca11bec42d2f12b5d4b1/SpeedNet.drawio.svg)

### Problems and Learnings
1. Brightness / Illumination Variation affects model output severly <br>
2. High output variance, I used exponent smoothing ;) but will fix it later <br>
3. Dependence of lane marking is a bad idea as some parts do not have lanes.<br>

### TODO for next version
1. Illumination invariance <br>
2. Reduce Neural net depth and increase features.
3. Indpendence from lane marking rather use road surface.