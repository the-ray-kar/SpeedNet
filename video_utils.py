import cv2
import numpy as np

class video_browser:

    def __init__(self,filename:str,windowname="window",point_counts = 4):
        self.filename = filename
        self.cap = cv2.VideoCapture(filename)
        ret, frame = self.cap.read()
        self.screen = frame.copy() #the drawings which would be used
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.points = [] #points appended as clicked
        self.windowname = windowname
        self.point_counts = point_counts


        # Callback function for the trackbar
    def on_trackbar(self,position):
    
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        ret, frame = self.cap.read()
        if not ret:
            return
        self.screen = frame
        
    # Mouse callback function to select points
    def select_points(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) < self.point_counts:
                self.points.append((x, y))
                print(f"Point {len(self.points)} selected: ({x}, {y})")
                cv2.circle(self.screen, (x,y), 5, (0, 255, 0), -1) #Draw the point

        
    def release(self):
            self.cap.release() #Release the reader
            cv2.destroyAllWindows()

    
    def collect_points(self):
         cv2.namedWindow(self.windowname)
         cv2.createTrackbar('Framecount', self.windowname, 0, self.frame_count-1, self.on_trackbar)
         cv2.setMouseCallback(self.windowname, self.select_points)

         while True:
      
            cv2.imshow(self.windowname, self.screen)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or len(self.points)==self.point_counts:
                cv2.imshow(self.windowname, self.screen)
                break

         return self.points #return the points
    
    '''
    destructor
    '''
    def __del__(self):
        self.release()

    '''
    Generator to get frames from position 1 to position 2
    '''

    def frame_generator(self,is_gray_scale=True,position1=0,position2=None):
        if position2==None:
            position2 = self.frame_count-1
        assert position1>=0,"invalid position 1"
        assert position2<self.frame_count,"position2 is more than frame count"
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position1) #set the cap position to beginining
        datasize = position2-position1
        print("% completed: ")
        for i in range(position1,position2):
            ret, frame = self.cap.read()
            if(is_gray_scale):
                frame  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            if not ret:
                return
            completion = i/datasize*100
            if(completion%2==0):
                print(completion," ",end="")
            yield frame

            

    '''
    Get specific frame
    '''
    def get_frame(self,position):
        assert position>=0 and position<self.frame_count,"Position not in frame range"
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        ret, frame = self.cap.read()
        return frame

        
            
         
