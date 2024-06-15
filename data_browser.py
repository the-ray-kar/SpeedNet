'''
This file contains function to replay frames stored by numpy .npy files
These files are larger as they are uncompressed
'''
import cv2
import numpy as np

class data_browser:

    def __init__(self,filename:str,windowname="window"):
        self.filename = filename
        self.cap = cv2.VideoCapture(filename)
        assert '.npy' in filename,"Not an npy file"
        self.frames = np.load(filename) #load the .npy file
        self.screen = self.frames[0].copy() #the drawings which would be used
        self.frame_count = len(self.frames)
        self.windowname = windowname
       


        # Callback function for the trackbar
    def on_trackbar(self,position):
        self.screen = self.frames[position]
        

        
    def release(self):
            self.cap.release() #Release the reader
            cv2.destroyAllWindows()

    def view_result(self):
        cv2.namedWindow(self.windowname)
        cv2.createTrackbar('Framecount', self.windowname, 0, self.frame_count-1, self.on_trackbar)
        while True:
      
            cv2.imshow(self.windowname, self.screen)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    
    '''
    destructor
    '''
    def __del__(self):
        self.release()

    '''
    Generator to get frames from position 1 to position 2
    '''

    def frame_generator(self,position1=0,position2=None):
        if position2==None:
            position2 = self.frame_count-1
        assert position1>=0,"invalid position 1"
        assert position2<self.frame_count,"position2 is more than frame count"
        datasize = position2-position1
        print("% completed: ")
        for i in range(position1,position2):

       
            completion = i/datasize*100
            if(completion%2==0):
                print(completion," ",end="")
            yield self.frames[i]
    '''
    Get specific frame
    '''
    def get_frame(self,position):
        assert position>=0 and position<self.frame_count,"Position not in frame range"
        return self.frames[position]

        
            
         
