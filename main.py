import cv2
import numpy as np
from dataset_maker import datasetmaker,data_browser
import os



if __name__ == '__main__':
    try:
        dbrowser = data_browser("../sp_data/train.npy","transformed")
        dbrowser.view_result()
        
    except:
        datamaker  = datasetmaker("../sp_data/train.mp4")
        points = datamaker.get_points_video()
        perspective_frames = datamaker.generate_perspective_data(points)
        print("Processed frames",len(perspective_frames))
        np.save("../sp_data/train.npy",perspective_frames)
        del perspective_frames #release the memory
        print("Stored the data")
        dbrowser = data_browser("../sp_data/train.npy","transformed")
        dbrowser.view_result()

    

    
