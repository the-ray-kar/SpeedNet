import cv2
import numpy as np
from dataset_maker import datasetmaker





if __name__ == '__main__':

    datamaker  = datasetmaker()
    datamaker.process_input_video("../sp_data/train.mp4")
    

    
