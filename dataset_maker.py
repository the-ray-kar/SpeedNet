'''
This file process the video file to create the dataset
'''
from video_utils import video_browser
import cv2
import numpy as np
import torch


class datasetmaker(video_browser):

    def __init__(self,filename,label_filename):
        super().__init__(filename)
        self.label_file = label_filename

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
    
    def load_label_data(self):
        labels = []
        with open(self.label_file, 'r') as file:
             for line in file:
                line.replace("\n","")
                labels.append(float(line))

        return labels

    def generate_tensor_data(self,points,batchsize=10,epochs=10,start_frame=1,end_frame=None):

        if end_frame ==None:
            end_frame =self.frame_count-2
        
        assert end_frame<=self.frame_count-2 and end_frame>5," end_frame value not in range"
        assert start_frame>=1 and start_frame<end_frame-10,"start frame out of range"
        
        labels = self.load_label_data()
        max_label = max(labels)
        width =  int(np.sum(np.sqrt( (points[0]-points[1]) **2) )) 
        height = int(np.sum(np.sqrt( (points[2]-points[1]) **2) ))
        

        for _ in range(epochs):
            random_selections = np.random.randint(1,self.frame_count-2,size=batchsize)
            batch = []
            label_batch = []
            for i in random_selections:
                old_frame = self.get_frame(i-1)
                old_pers = self.apply_perspective_transform(old_frame,points,width,height)
                mid_frame = self.get_frame(i)
                mid_pers = self.apply_perspective_transform(mid_frame,points,width,height)
                new_frame = self.get_frame(i+1)
                new_pers = self.apply_perspective_transform(new_frame,points,width,height)
                shape = new_pers.shape
                prev_next = np.zeros_like(new_pers,shape=(shape[0],shape[1],3))
                prev_next[:,:,0] = old_pers
                prev_next[:,:,1] = mid_pers
                prev_next[:,:,1] = new_pers

                batch.append(prev_next)
                label_batch.append(labels[i]*2/max_label-1)
            batch = np.array(batch)
            batch = torch.tensor(batch,dtype=torch.float32)
            batch = batch.permute(0,3,1,2) #format for CNN
            label_batch = np.array(label_batch)
            label_batch = torch.tensor(label_batch,dtype=torch.float32)
            yield batch,label_batch



    def generate_tensor_data_old(self,points):
        
        labels = self.load_label_data()
        max_label = max(labels)
        width =  int(np.sum(np.sqrt( (points[0]-points[1]) **2) )) 
        height = int(np.sum(np.sqrt( (points[2]-points[1]) **2) ))
        old_frame = self.get_frame(0)
        old_pers = self.apply_perspective_transform(old_frame,points,width,height)

        mid_frame = self.get_frame(1)
        mid_pers = self.apply_perspective_transform(mid_frame,points,width,height)
  

        for i in range(2,self.frame_count):
            new_frame = self.get_frame(i)
            new_pers = self.apply_perspective_transform(new_frame,points,width,height)
            #flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0) #calculate optic flow
            shape = new_pers.shape
            prev_next = np.zeros_like(new_pers,shape=(shape[0],shape[1],3)) #combine old , mid and new
            prev_next[:,:,0] = old_pers
            prev_next[:,:,1] = mid_pers
            prev_next[:,:,1] = new_pers
            prev_next_tensor = torch.tensor(prev_next,dtype=torch.float32)
            batch_tensor_image = prev_next_tensor.unsqueeze(0) 
            batch_tensor_image=batch_tensor_image.permute(0,3,1,2)
            #prev_next_tensor = transform(prev_next)
            old_pers = mid_pers
            mid_pers = new_pers
            label = torch.tensor(2*labels[i]/max_label-1, dtype=torch.float32)
            yield batch_tensor_image,label
'''
Visualize Perspective transformed road
'''

class view_perspective_transform:

    def __init__(self,video_file,points,width,height,grayscale=False,resize=(0,0)):
        self.filename = video_file
        self.points = points
        self.width = width
        self.height = height
        self.windowname = "warped perspective"
        self.cap = cv2.VideoCapture(video_file)
        self.videofile = video_file
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret,frame = self.cap.read()
        self.grayscale = grayscale
        self.resize = resize
        self.screen= self.apply_perspective_transform(frame,self.points,self.width,self.height)
        self.screen = self.resize_frame(self.screen,self.resize)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.track_position = 0
        self.play = False
        

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
    
    def on_trackbar(self,position):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        self.track_position = position
        ret,frame = self.cap.read()
        if ret:
            self.screen= self.apply_perspective_transform(frame,self.points,self.width,self.height)
            self.screen = self.resize_frame(self.screen,self.resize)
            if(self.grayscale):
                self.screen=cv2.cvtColor(self.screen, cv2.COLOR_BGR2GRAY)
                #self.screen = self.process_image(self.screen)
                cv2.imshow(self.windowname,self.screen)
    
    def process_image(self,frame:np.ndarray):
        #frame = cv2.equalizeHist(frame) #Histogram equilization for better contrast : Bad idea
        #frame = self.power_normalize(frame)
        frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize=11, C=2)
        return frame


    def power_normalize(self,frame:np.ndarray):
        frame = frame/255
        frame = np.power(frame,1.5)
        return np.uint8(frame*255)
        
    def release(self):
            self.cap.release() #Release the reader
            cv2.destroyAllWindows()

    def resize_frame(self,frame,resize=(0,0)):
        if(resize[0]!=0 and resize[1]!=0):
            shape =frame.shape
            dx = round(shape[1]*resize[0])
            dy = round(shape[0]*resize[1])
            return cv2.resize(frame,dsize=(dx,dy))
        
        return frame


    def view_result(self):
        cv2.namedWindow(self.windowname)
        cv2.createTrackbar('Framecount', self.windowname, 0, self.frame_count-1, self.on_trackbar)
        while True:
        

            cv2.imshow(self.windowname, self.screen)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'): #play and pause
                self.play = not self.play
            
            if (self.play):
                self.track_position+=1
                self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.track_position)
                ret,frame = self.cap.read()
                if ret:
                    self.screen = self.apply_perspective_transform(frame,self.points,self.width,self.height)
                    self.screen = self.resize_frame(self.screen,self.resize)
                    if(self.grayscale):
                        self.screen=cv2.cvtColor(self.screen, cv2.COLOR_BGR2GRAY)
                        #self.screen = self.process_image(self.screen)
                else:
                    break
            
        cv2.destroyAllWindows()
        self.cap.release()

    def generate_dataset(self,stackframes:int,labels:np.ndarray,savefolderlocation:str): #stack n gray frames 
        if(self.cap==None):
            self.cap = cv2.VideoCapture(self.video_file)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        
        count = 0
        frames =[]
        data_labels = []
        npframes = []
        while True:
            
            ret,frame =self.cap.read() #Read the frames
            if not ret:
                break
            frame = self.apply_perspective_transform(frame,self.points,self.width,self.height)
            frame = self.resize_frame(frame,self.resize)
            frame  =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #count         -> 0 1 2 3 4 5 6 7 8 9 10     11 12
            #len(frame)       0 1 2 3 4 5 6 7 8 9 10  0  1   2
            
            if count%stackframes==0 and count!=0:
                #stack the frames
                npframe = np.array(frames)
                npframes.append(npframe)
                speeds = labels[count-stackframes:count]
                mean_speed = np.mean(speeds)
                data_labels.append(mean_speed)
                frames = []
                if count%(stackframes*1000):
                    print(count/self.frame_count*100)
            
            frames.append(frame)
            
            count+=1

        data_labels = np.array(data_labels)
        labelfilename = savefolderlocation+"/meanlabels"+str(stackframes)+".npy"
        np.save(labelfilename,data_labels) #save the labels as well
        savefilename = savefolderlocation+"/framedata.npy"
        np.save(savefilename,npframes,allow_pickle=True)
        print("Dataset created with shape",npframe.shape,"And length ",len(data_labels),len(npframes))




'''

This class contains function to replay frames stored by numpy .npy files
These files are larger as they are uncompressed
'''
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

        
            
         
