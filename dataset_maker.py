'''
This file process the video file to create the dataset
'''
from video_utils import video_browser


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