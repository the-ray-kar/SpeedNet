'''
This file process the video file to create the dataset
'''
from video_utils import video_browser
import cv2
import numpy as np


class datasetmaker:

    def __init__(self):
        pass

    '''
    This function process the video to get points for perspective transform
    '''
    def process_input_video(self,filename:str):
        browser = video_browser(filename)
        points = browser.collect_points()
        print(points)
        return points

    def apply_perspective_transform(frame, points):
        
        assert len(points)==4,"no of points not equal to 4"

        # Define the destination points for the perspective transform
        width = np.sqrt((points[0]-points[1])**2)
        height = np.sqrt((points[2]-points[1]**2))
        
        dst_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

        # Convert points to numpy array format
        src_points = np.float32(points)

        # Compute the perspective transform matrix
        Mat = cv2.getPerspectiveTransform(src_points, dst_points)

        # Apply the perspective transform to the frame
        warped_image = cv2.warpPerspective(frame, Mat, (width, height))

        return warped_image