import cv2
import numpy as np
from dataset_maker import datasetmaker





if __name__ == '__main__':

    datamaker  = datasetmaker("../sp_data/train.mp4")
    points = datamaker.get_points_video()
    perspective_frames = datamaker.generate_perspective_data(points)
    print("Processed frames",len(perspective_frames))

    

    
