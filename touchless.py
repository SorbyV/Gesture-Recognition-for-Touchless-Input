
import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
import screen_brightness_control as sbc 
import winv
import pyautogui as at
import os
import psutil
import pandas as pd

frame1_isset = False
frame2_isset = False
frame3_isset = False
custom_counter = 0
final_box = 9999
roi_finger = None
menu = [0]*6
box_num = 0
framecount = 0
screenwidth, screenheight = at.size()
widthfact = screenwidth/400
heightfact = screenheight/240
file1 = '"D:\\Work\Sublime Text 3\sublime_text.exe"'
file2 = '"C:\\Users\sorby\Desktop\SaurabhVaid.pdf"'
file3 = '"D:\College\Fall Semester 20-21\IWP\iwp_proj\york.jpg"'

def count_finger(thresholded, segmented):
    chull = cv2.convexHull(segmented)
    extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left   = tuple(chull[chull[:, :, 0].argmin()][0])
    extreme_right  = tuple(chull[chull[:, :, 0].argmax()][0])
    cX = int((extreme_left[0] + extreme_right[0]) / 2)
    cY = int((extreme_top[1] + extreme_bottom[1]) / 2)
    cY = cY + 20
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]
    radius = int(0.7 * maximum_distance)
    
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")	
   
    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)
    cv2.circle(frame, (cX+200, cY), 1, 255, 1)
    
    cv2.circle(frame, (cX + 200, cY), radius, 255, 1)
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)
    (cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    count = 0
    cv2.imshow("Circular ROI", circular_roi)
    keypress = cv2.waitKey(1) & 0xFF
    if keypress == ord("q"):
        cv2.destroyWindow("Circular ROI")
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        #if ((cY + (cY * 0.4)) > (y + h)) and ((circumference * 0.4) > c.shape[0]):
        count += 1
    count -= 1
    
    
    
    if box_num == 1:
        if count == 1:
            winv.set_volume(7)
        elif count == 2:
            winv.set_volume(30)
        elif count == 3:
            winv.set_volume(54)
        elif count == 4:
            winv.set_volume(77)
        elif count == 5:
            winv.set_volume(100)
    if box_num == 2:
        sbc.set_brightness(count*20)
    if box_num == 3:
        cv2.circle(frame, (extreme_top[0] + 200, extreme_top[1]), 2, (0, 255, 255), 5)
        at.PAUSE = 0.1
        at.moveTo(extreme_left[0]*widthfact, extreme_left[1]*heightfact, duration=0.04)
        
        if count == 4:
            at.PAUSE = 2
            at.click(button='LEFT')
        if count == 5:
            at.PAUSE = 2
            at.click(button='RIGHT')
        
    global custom_counter, frame1_isset, frame2_isset, frame3_isset
    global custom_counter
    
    if box_num == 4:
        if count == 5:
            if custom_counter == 0:
                image = at.screenshot()
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imshow("Screenshot", image)
                custom_counter = 1
        elif count == 2:
            cv2.destroyWindow("Screenshot")
            custom_counter = 0
        
    
    if box_num == 5:
        cv2.circle(frame, (extreme_left[0] + 200, extreme_left[1]), 2, (0, 0, 255), 5)  
        
        #print(framecount, startingframes1, startingframes2, startingframes3)
        startingframes1 = 0
        startingframes2 = 0
        startingframes3 = 0
        
        if frame1_isset == False:
            startingframes1 = framecount
        if frame2_isset == False:
            startingframes2 = framecount
        if frame3_isset == False:
            startingframes3 = framecount
        
        
        if extreme_top[0] in range(0, int(400/3)+1):            
            #cv2.putText(frame, str(startingframes1), (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            if frame1_isset == False:
                startingframes1 = framecount
                frame1_isset = True
                frame2_isset = False
                frame3_isset = False
            if framecount > startingframes1 + 72:
                os.system(file1)
                
                
        elif extreme_top[0] in range(int(400/3), int(400*2/3)+1):
            #cv2.putText(frame, str(startingframes2), (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if frame2_isset == False:
                startingframes2 = framecount
                frame2_isset = True
                frame1_isset = False
                frame3_isset = False
            if framecount > startingframes2 + 72:
                os.system(file2)
                
                
        elif extreme_top[0] in range(int(400*2/3), 400+1):
            #cv2.putText(frame, str(startingframes3), (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if frame3_isset == False:
                startingframes3 = framecount
                frame3_isset = True
                frame1_isset = False
                frame2_isset = False
            if framecount > startingframes3 + 72:
                os.system(file3)
    return count

def coordinate_menu(segmented):
    chull = cv2.convexHull(segmented)
    extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
    return extreme_top

def count_menu(extreme_top):
     
    cv2.circle(frame, (extreme_top[0], extreme_top[1]), 2, (0, 0, 255), 5)
    
    global box_num
    global framecount
    global final_box
    
    final_box = 9999
    if extreme_top[0] <= int(width/4):
        if box_num != 0:
            if extreme_top[1] in range(menu[box_num-1], menu[box_num]):
                framecount += 1
            else:
                for i in range(1, 6):
                    if extreme_top[1] in range(menu[i-1], menu[i]):
                        box_num = i
                        framecount = 0
                        break
        else:
            for i in range(1, 6):
                if extreme_top[1] in range(menu[i-1], menu[i]):
                    box_num = i
                    framecount = 0
                    break
    if framecount >= 72:
        
        final_box = box_num
    if final_box != 0:
        roi_function(gray_finger, bg_finger, 1)


#---------------------ROI FUNCTION---------------------------------------------
def roi_function(gray, bg, num):
    if num == 0:
        hand_menu = None
        diff_menu = cv2.absdiff(bg.astype("uint8"), gray)
        thresholded_menu = cv2.threshold(diff_menu, 25, 255, cv2.THRESH_BINARY)[1]
        (cnts_menu, _) = cv2.findContours(thresholded_menu.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts_menu) == 0:
            cv2.putText(frame, 'No hand found', (200, 230), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
        else:
            segmented_menu = max(cnts_menu, key=cv2.contourArea)
            hand_menu = (thresholded_menu, segmented_menu)
        if hand_menu is not None:
                (thresholded_menu, segmented_menu) = hand_menu
                cv2.drawContours(frame_copy, [segmented_menu + (right, top)], -1, (255, 0, 0))
                finger_point = coordinate_menu(segmented_menu)
                #if finger_point[0] < int(width/4):
                count_menu(finger_point)
                #cv2.imshow("Menu threshold", thresholded_menu)
        #else:
            #cv2.destroyWindow("Menu threshold")
    if num == 1:
        hand_finger = None
        diff_finger = cv2.absdiff(bg.astype("uint8"), gray)
        thresholded_finger = cv2.threshold(diff_finger, 25, 255, cv2.THRESH_BINARY)[1]
        (cnts_finger, _) = cv2.findContours(thresholded_finger.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts_finger) == 0:
            cv2.putText(frame, 'No hand found', (200, 230), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
        else:
            segmented_finger = max(cnts_finger, key=cv2.contourArea)
            hand_finger = (thresholded_finger, segmented_finger)
        if hand_finger is not None:
                (thresholded_finger, segmented_finger) = hand_finger
                cv2.drawContours(frame_copy, [segmented_finger + (right, top)], -1, (255, 0, 0))
                fingers = count_finger(thresholded_finger, segmented_finger)
                outputtext = "Number of fingers =" + str(fingers)
                cv2.putText(frame, outputtext, (200, 230), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
                #cv2.imshow("Finger threshold", thresholded_finger)
        #else:
            #cv2.destroyWindow("Finger threshold")
        
#--------------------main-----------------------------------------------------        

bg_menu = None
bg_finger = None
cv2.namedWindow("preview")
webcam = cv2.VideoCapture(0)
num_frames_menu = 0
num_frames_finger = 0
calibrated = False
top, right, bottom, left = 0, 800, 600, 0
df = pd.DataFrame()
vol_ram = []
bright_ram = []
cursor_ram = []
ss_ram = []
cust_ram = []
while(True):
    '''
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use:', memoryUse)'''
    rval, frame = webcam.read()
    frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, width=800, height=600)
    frame_copy = frame.copy()
    (height, width) = frame.shape[:2]
    key = cv2.waitKey(20)
    cv2.line(img=frame, pt1=(int(width/4), 0), pt2=(int(width/4), height), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(0, int(height/5)), pt2=(int(width/4), int(height/5)), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(0, 2*int(height/5)), pt2=(int(width/4), 2*int(height/5)), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(0, 3*int(height/5)), pt2=(int(width/4), 3*int(height/5)), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(0, 4*int(height/5)), pt2=(int(width/4), 4*int(height/5)), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
    
    cv2.putText(frame, 'Volume', (10, int(height/5)-10), cv2.FONT_HERSHEY_DUPLEX , 0.75, (255, 255, 255), 1)
    cv2.putText(frame, 'Brightness', (10, int(height/5)*2-10), cv2.FONT_HERSHEY_DUPLEX , 0.75, (255, 255, 255), 1)
    cv2.putText(frame, 'Mouse Cursor', (10, int(height/5)*3-10), cv2.FONT_HERSHEY_DUPLEX , 0.75, (255, 255, 255), 1)
    cv2.putText(frame, 'Screenshot', (10, int(height/5)*4-10), cv2.FONT_HERSHEY_DUPLEX , 0.75, (255, 255, 255), 1)
    cv2.putText(frame, 'Custom Files', (10, int(height/5)*5-10), cv2.FONT_HERSHEY_DUPLEX  , 0.75,(255, 255, 255), 1)
    
    menu[0] = 0
    menu[1] = int(height/5)
    menu[2] = 2*int(height/5)
    menu[3] = 3*int(height/5)
    menu[4] = 4*int(height/5)
    menu[5] = 5*int(height/5)
    
    accumWeight = 0.5
    
    roi_menu = frame_copy[0:600, 0:int(width/4)]
    roi_finger = frame_copy[0:240, 200:600]
    
    cv2.rectangle(frame, (200, 0), (600, 240), (0, 255, 0), 1)    
    #cv2.rectangle(frame, (top, left), (right, bottom), (0,255,0), 5)
    if box_num == 1:
        cv2.putText(frame, "Selected: Volume", (200, 20), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
    elif box_num == 2:
        cv2.putText(frame, "Selected: Brightness", (200, 20), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
    elif box_num == 3:
        cv2.putText(frame, "Selected: Mouse Control", (200, 20), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
    elif box_num == 4:
        cv2.putText(frame, "Selected: Screenshot", (200, 20), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
    elif box_num == 5:
        cv2.putText(frame, "Selected: Custom Files", (200, 20), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
        
    hand = None
    gray_menu = cv2.cvtColor(roi_menu, cv2.COLOR_BGR2GRAY)
    gray_menu = cv2.GaussianBlur(gray_menu, (7, 7), 0)
    
    gray_finger = cv2.cvtColor(roi_finger, cv2.COLOR_BGR2GRAY)
    gray_finger = cv2.GaussianBlur(gray_finger, (7, 7), 0)
    #background formation-----------------------------------------------------
    if num_frames_menu == 0:
        bg_menu = gray_menu.copy().astype('float')
    if num_frames_menu < 30:
        cv2.accumulateWeighted(gray_menu, bg_menu, accumWeight)
        
    if num_frames_finger == 0:
        bg_finger = gray_finger.copy().astype('float')
    if num_frames_finger < 30:
        cv2.accumulateWeighted(gray_finger, bg_finger, accumWeight)
    #hand segmentation--------------------------------------------------------
    else:
        roi_function(gray_menu, bg_menu, 0)
    num_frames_menu += 1
    num_frames_finger += 1
    if box_num == 5:
        cv2.putText(frame, "File1", (200, 40), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
        cv2.putText(frame, "File2", (int(400/3)+200, 40), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
        cv2.putText(frame, "File3", (int(400*2/3)+200, 40), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 1)
        
        cv2.line(img=frame, pt1=(int(400/3)+200, 0), pt2=(int(400/3)+200, 240), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(int(400*2/3 + 200), 0), pt2=(int(400*2/3+200), 240), color=(0, 255, 0), thickness=1, lineType=8, shift=0)
    #cv2.rectangle(frame, (int(width/4), 0), (3*(int(width/4)), 2*(int(height/5))), 255, 5)
    cv2.imshow("preview", frame)
    '''
    if box_num == 1:
        print("Volram length = ", len(vol_ram))
        vol_ram.append(memoryUse)
    elif box_num == 2:
        print("bright length = ", len(bright_ram))
        bright_ram.append(memoryUse)
    elif box_num == 3:
        print("Cursor length = ", len(cursor_ram))
        cursor_ram.append(memoryUse)
    elif box_num == 4:
        print("SS length = ", len(ss_ram))
        ss_ram.append(memoryUse)
    elif box_num == 5:
        print("Custom length = ", len(cust_ram))
        cust_ram.append(memoryUse)
        
    if len(vol_ram) == 240:
        df['Volume'] = vol_ram
    if len(bright_ram) == 240:
        df['Brightness'] = bright_ram
    if len(cursor_ram) == 240:
        df['Mouse Cursor'] = cursor_ram
    if len(ss_ram) == 240:
        df['Screenshot'] = ss_ram
    if len(cust_ram) == 240:
        df['Custom Access'] = cust_ram
        '''
    if key == 27:
        break
webcam.release()
cv2.destroyWindow("preview")
