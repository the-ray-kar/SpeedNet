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
         cv2.createTrackbar('Framecount', self.windowname, 0, int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))-1, self.on_trackbar)
         cv2.setMouseCallback(self.windowname, self.select_points)

         while True:
      
            cv2.imshow(self.windowname, self.screen)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or len(self.points)==self.point_counts:
                break

         self.release()

         return self.points #return the points

            
         
