#!/usr/bin/python
import urllib2
import sys
import time
from math import cos, sin
from math import sqrt,pow
import cv

CLOCKS_PER_SEC = 1.0
MHI_DURATION = 1
MAX_TIME_DELTA = 0.5
MIN_TIME_DELTA = 0.05
N = 4
buf = range(10) 
last = 0
mhi = None # MHI
orient = None # orientation
mask = None # valid orientation mask
mhi_2 = None # MHI
orient_2 = None # orientation
mask_2 = None # valid orientation mask
segmask = None # motion segmentation map
storage = None # temporary storage


def update_mhi(img, dst, diff_threshold):
    global last
    global mhi
    global storage
    global mask
    global orient
    global segmask
    
    center_2x = 0
    center_2y = 0 
    
    timestamp = time.clock() / CLOCKS_PER_SEC # get current time in seconds
    size = cv.GetSize(img) # get current frame size
    idx1 = last
    if not mhi or cv.GetSize(mhi) != size:
        for i in range(N):
            buf[i] = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
            cv.Zero(buf[i])
        mhi = cv.CreateImage(size,cv. IPL_DEPTH_32F, 1)
        cv.Zero(mhi) # clear MHI at the beginning
        orient = cv.CreateImage(size,cv. IPL_DEPTH_32F, 1)
        segmask = cv.CreateImage(size,cv. IPL_DEPTH_32F, 1)
        mask = cv.CreateImage(size,cv. IPL_DEPTH_8U, 1)
    
    cv.CvtColor(img, buf[last], cv.CV_BGR2GRAY) # convert frame to grayscale
    idx2 = (last + 1) % N # index of (last - (N-1))th frame
    last = idx2
    silh = buf[idx2]
    cv.AbsDiff(buf[idx1], buf[idx2], silh) # get difference between frames
    cv.Threshold(silh, silh, diff_threshold, 1, cv.CV_THRESH_BINARY) # and threshold it
    cv.UpdateMotionHistory(silh, mhi, timestamp, MHI_DURATION) # update MHI
    cv.CvtScale(mhi, mask, 255./MHI_DURATION,
                (MHI_DURATION - timestamp)*255./MHI_DURATION)
    cv.Zero(dst)
    cv.Merge(mask, None, None, None, dst)
    cv.CalcMotionGradient(mhi, mask, orient, MAX_TIME_DELTA, MIN_TIME_DELTA, 3)
    if not storage:
        storage = cv.CreateMemStorage(0)
    seq = cv.SegmentMotion(mhi, segmask, storage, timestamp, MAX_TIME_DELTA)


    
    for (area, value, comp_rect) in seq:

        
        if  comp_rect[2]*comp_rect[3] > 32000: # reject very small components
            color = cv.CV_RGB(255, 0,0)
            silh_roi = cv.GetSubRect(silh, comp_rect)
            mhi_roi = cv.GetSubRect(mhi, comp_rect)
            orient_roi = cv.GetSubRect(orient, comp_rect)
            mask_roi = cv.GetSubRect(mask, comp_rect)
            angle = 360 - cv.CalcGlobalOrientation(orient_roi, mask_roi, mhi_roi, timestamp, MHI_DURATION)

           




            

           
                    
            count = cv.Norm(silh_roi, None, cv.CV_L1, None) # calculate number of points within silhouette ROI
            
            if count < (comp_rect[2] * comp_rect[3] * 0.05):
                continue

                   
            center = ((comp_rect[0] + comp_rect[2] / 2), (comp_rect[1] + comp_rect[3] / 2))

            lower_1 = cv.Round(((2*center[0]- comp_rect[2])/2))
            lower_2 = cv.Round((2*center[1] -comp_rect[3])/2 + (0.29*comp_rect[3]))
            #upper_1 = int((2*center[0]+ comp_rect[2])/2 )
            #upper_2 = int((2*center[1] + comp_rect[3])/2)
            upper_1 = cv.Round((lower_1+ comp_rect[2]) )
            upper_2 = cv.Round((lower_2 - 0.29*comp_rect[3]))
            

            
            
           
            if (lower_1 > 640):
                ower_1 = 639
            if(lower_1 < 0):
                lower_1 = 0
            if(lower_2 > 480):
                lower_2 = 479
                    
            if(upper_2 < 0):
                upper_2 = 0
                    
            if(lower_2 < 0):
                lower_2 = 0
            if (upper_1 > 640):
                    upper_1 = 639
            if(upper_1 < 0):
                upper_1 = 0
            if (upper_2 > 480):
                upper_2 = 479
        

            cord = (lower_1,lower_2,upper_1,upper_2)
      
           
            cv.ResetImageROI( mhi )
            cv.ResetImageROI( mask )
            cv.ResetImageROI( silh )
            cv.ResetImageROI( orient )

             
            
            silh_2 = cv.CloneImage(silh)
            cv.SetImageROI(silh_2,cord)
            
            mid_1 = cv.Round((comp_rect[2] + comp_rect[0]))
            mid_2 = cv.Round((comp_rect[3]/2 +comp_rect[1]))
            
            
            count_2 = cv.Norm(silh_2, None, cv.CV_L1, None)         #counter_2
             
           
            cv.ResetImageROI( silh_2 )
            mask_2 = cv.CloneImage(mask)
            mhi_2 = cv.CloneImage(mhi)
            orient_2 = cv.CloneImage(orient)
            
            cord2 = (comp_rect[0],comp_rect[1],mid_1, mid_2)    
            
            cv.SetImageROI(mask_2,cord2)
            cv.SetImageROI(orient_2,cord2)
            cv.SetImageROI(mhi_2,cord2)
           
                 
          
            angle_2 =  360 - cv.CalcGlobalOrientation(orient_2, mask_2, mhi_2, timestamp, MHI_DURATION)

        

            
            #print('count =', angle)                #angle
            #print('count =', angle_2)              #angle
           

     
          
            
            cv.Line(dst,(lower_1,lower_2),(upper_1,upper_2),color,3,cv.CV_AA,0)
            
            cv.Line(dst,(mid_1,mid_2),(comp_rect[0],comp_rect[1]),color,3,cv.CV_AA,0)
                
                         
            cv.Rectangle(dst,((2*center[0]- comp_rect[2])/2  ,(2*center[1] -comp_rect[3])/2),
                                                 ((2*center[0]+ comp_rect[2])/2  ,(2*center[1]
                                                + comp_rect[3])/2),cv.CV_RGB(255,155,0),1,8,0)
            global k
            global r
            global center_1x
            global center_1y 
            global time_temp_1
            global time_temp_2
            
            if( k == 2):
                #print(timestamp)     
                center_1x =   comp_rect[0]
                center_1y =   comp_rect[1]
                time_temp_1 = timestamp
                            
                k=0      


            elif (r >= 1 ):
                       
                            
                center_2x =   comp_rect[0]
                center_2y =   comp_rect[1] 
                time_temp_2 = timestamp
                if(time_temp_2 - time_temp_1):
                    
                    dista = sqrt(pow((center_1x - center_2x),2) + pow((center_1y - center_2y),2) )
                
                    speed = float (dista/(time_temp_2 - time_temp_1) ) 
                    print(speed)
                    
                r= 0
                                  
                                    
                      
                       
                           
                         
            else:
                            
                                                   
                    center_1x =   center_2x
                    center_1y =   center_2y                          
                    time_temp_1 = timestamp             
                    r = r+1
                            
                     
                           
                       
                  
                  
                  
                   
              
           
            
            
            
            




            

if __name__ == "__main__":
    motion = 0
    capture = 0
    center_1x =   0
    center_1y =  0
    time_temp_1  =0
    time_temp_2 =0
    r = 0
    k =2   

    if len(sys.argv)==1:
        capture = cv.CreateCameraCapture(0)
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = cv.CreateCameraCapture(int(sys.argv[1]))
    elif len(sys.argv)==2:
        capture = cv.CreateFileCapture(sys.argv[1]) 

    if not capture:
        print "Could not initialize capturing..."
        sys.exit(-1)
        
    cv.NamedWindow("Motion", 1)
    cv.NamedWindow( "RealImage", 1 );
    while True:
        image = cv.QueryFrame(capture)
        if(image):
            if(not motion):
                    motion = cv.CreateImage((image.width, image.height), 8, 3)
                    cv.Zero(motion)
                    #motion.origin = image.origin
            update_mhi(image, motion, 30)

            

       







            
            cv.ShowImage("Motion", motion)
            cv.ShowImage( "RealImage", image );
            if(cv.WaitKey(10) != -1):
                break
        else:
            break
    cv.DestroyWindow("Motion")
