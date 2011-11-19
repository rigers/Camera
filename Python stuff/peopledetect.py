import sys
from cv import *
import Image
##import cv

def inside(r, q):
    (rx, ry), (rw, rh) = r
    (qx, qy), (qw, qh) = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

##try:

storage = CreateMemStorage(0)
capture = CaptureFromCAM(0)
while True:
    img = QueryFrame(capture)
    ##img = LoadImage("human.jpg")
    ##except:
    ##    try:
    ##        f = open(sys.argv[1], "rt")
    ##    except:
    ##        print "cannot read " + sys.argv[1]
    ##        sys.exit(-1)
    ##    imglist = list(f.readlines())
    ##else:
    ##    imglist = [sys.argv[1]]
    ##
##    NamedWindow("original image",1)
##    ShowImage("original image", img)
    NamedWindow("people detection demo", 2)
    ##ShowImage("people detection demo", img)
    ##storage = CreateMemStorage(0)

    ##for name in imglist:
    ##    n = name.strip()
    ##    print n
    ##    try:
    ##        img = LoadImage(n)
    ##    except:
    ##        continue
        
        ##ClearMemStorage(storage)

##    print GetSize(img)
##    Smooth( img, img, CV_GAUSSIAN, 11, 11 )

    img2 = CreateMat(240, 320, CV_8UC3)


    PyrDown(img, img2)

##    data = np.asarray(img2)
##    blue, green, red = data.T
##
##    res = (green > (_RED_DIFF + red)) & (green > (_BLU_DIFF + blue))
##    res = res.astype(np.uint16) * 255
##
##    res = fromarray(res)


    
    found = list(HOGDetectMultiScale(img2, storage, win_stride=(8,8),
        padding=(32,32), scale=.8, group_threshold=1))
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
        tl = (rx + int(rw*0.1), ry + int(rh*0.07))
        br = (rx + int(rw*0.9), ry + int(rh*0.87))
        Rectangle(img2, tl, br, (0, 255, 0), 3)
            
    ShowImage("people detection demo", img2)
##    c = WaitKey(0)
    ##if c == ord('q'):
    ##    break
    if WaitKey(10) == 27:
        break
