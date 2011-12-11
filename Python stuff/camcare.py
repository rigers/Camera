#!/usr/bin/python
import urllib2
import sys
import time
from math import cos, sin
import math
import cv
import Cord_people as cord_p
from cv import *

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

        
        if  comp_rect[2]*comp_rect[3] > 7200: # reject very small components
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
            

            
            lm = cv.GetSize(img)
            
            if (lower_1 > lm[0]):
                lower_1 = lm[0]
            if(lower_1 < 0):
                lower_1 = 0
            if(lower_2 > lm[1]):
                lower_2 = lm[1]
            
                    
            if(lower_2 < 0):
                lower_2 = 0
            if (upper_1 > lm[0]):
                    upper_1 = lm[0]
            if(upper_1 < 0):
                upper_1 = 0
                    
            if(upper_2 < 0):
                upper_2 = 0
                
            if (upper_2 > lm[1]):
                upper_2 = lm[1]
        

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


            #cv.Rectangle(dst,(),cv.CV_RGB(255,155,0),1,8,0)
            global k
            global r
            global center_1x
            global center_1y
            global center_2x
            global center_2y 
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
               
                if(time_temp_2 - time_temp_1 > 0):
                    #print(center_2x,center_2y)
                    #print(center_1x,center_1y)
                    
                    dista =   math.sqrt(math.pow((center_1x - center_2x ),2)+ math.pow((center_1y - center_2y),2))
                    
                
                    speed = float (dista/(time_temp_2 - time_temp_1) )
                    
                    #print('speed =',speed)
                    global R
                    
                    
                  
                    center_R1 = cv.Round(R[0][0] + R[1][0] / 2)# try to set the ROI
                    center_R2 = cv.Round(R[0][1] + R[1][1] / 2)
                    dista_C =   math.sqrt(math.pow((center_R1 - center[0] ),2)+ math.pow((center_R2 - center[1]),2))

                   
                    print( dista_C)  # This will be the distace between the HOG center and the silueheta center of motion.
                    cv.Line(dst,(int (R[0][0]),int( R[0][1])),(center_R1,center_R2),color,3,cv.CV_AA,0)
                    
                    
                    
                    r= 0
                                  
                                    
                      
                       
                           
                         
            else:
                            
                                                   
                    center_1x =   center_2x
                    center_1y =   center_2y                          
                    time_temp_1 = timestamp             
                    r = r+1
                            
                     
                           

def hog_D(ima):
    global R

    def inside(r, q):
        (rx, ry), (rw, rh) = r
        (qx, qy), (qw, qh) = q
        return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


    storage = CreateMemStorage(0)
    #capture = CaptureFromCAM(-1)
    
    while True:
       
           
        NamedWindow("people detection demo", 1)
    
       
     
        found = list(HOGDetectMultiScale(ima, storage, win_stride=(8,8),
            padding=(32,32), scale=1.05, group_threshold=2))
        found_filtered = []
        for r in found:
            insidef = False
            for q in found:
                if inside(r, q):
                    insidef = True
                    break
            if not insidef:
                found_filtered.append(r)
        for r in found_filtered:
            (rx, ry), (rw, rh) = r
            #print(rx, ry, rw, rh)
       
            tl = (rx + int(rw*0.1), ry + int(rh*0.07))
            br = (rx + int(rw*0.9), ry + int(rh*0.87))
            
            R = (tl,br)
           
            Rectangle(ima, tl, br, (0, 255, 0), 1)
            
        ShowImage("people detection demo", ima)


        c = WaitKey(1)
        if c == 'q':
            break
        return
                       
                  
                  
                  
                   
              
           
            
            
            
            




            

if __name__ == "__main__":
    motion = 0
    capture = 0
    center_1x =   0
    center_1y =  0
    center_2x =   0
    center_2y =  0
    time_temp_1  =0
    time_temp_2 =0
    R = (0,0,0,0)
    r = 0
    k =2   

    if len(sys.argv)==1:
        capture = cv.CaptureFromCAM(0)
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
        #################################################################################




        ##################################################################################
        
        img = cv.QueryFrame(capture)
       
       
           
   
        image = cv.CreateMat(240,320,cv.CV_8UC3)
##        img3 = cv.CreateMat(240,320,cv.CV_8UC3)

        cv.PyrDown(img,image)
##        cv.PyrDown(image,img3)



        
        if(image):
            if(not motion):
                    motion = cv.CreateImage((image.width, image.height), 8, 3)
                    cv.Zero(motion)
                    #motion.origin = image.origin
            hog_D(image)
            
            update_mhi(image, motion, 30)
           
            
            cv.ShowImage("Motion", motion)
            cv.ShowImage( "RealImage", img );
            if(cv.WaitKey(10) != -1):
                break
        else:
            break
    cv.DestroyWindow("Motion")

















    
