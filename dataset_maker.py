'''
This file process the video file to create the dataset
'''
from video_utils import video_browser
import cv2
import numpy as np


class datasetmaker(video_browser):

    def __init__(self,filename):
        super().__init__(filename)

    '''
    This function process the video to get points for perspective transform
    '''
    def get_points_video(self):
        points = self.collect_points()
        points = np.array(points)
        return points

    def apply_perspective_transform(self,frame, points,width,height):
        
        assert len(points)==4,"no of points not equal to 4"

        # Define the destination points for the perspective transform
        
        
        dst_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

        # Convert points to numpy array format
        src_points = np.float32(points)

        # Compute the perspective transform matrix
        Mat = cv2.getPerspectiveTransform(src_points, dst_points)

        # Apply the perspective transform to the frame
        warped_image = cv2.warpPerspective(frame, Mat, (width, height))

        return warped_image
    
    def generate_perspective_data(self,points):
        print("Generating perspective transformed data for",self.frame_count,"images")
        width =  int(np.sum(np.sqrt( (points[0]-points[1]) **2) )) 
        height = int(np.sum(np.sqrt( (points[2]-points[1]) **2) ))
        per_frames = []
        for frame in self.frame_generator():
            transformed_frame = self.apply_perspective_transform(frame,points,width,height)
            per_frames.append(transformed_frame)

        return per_frames