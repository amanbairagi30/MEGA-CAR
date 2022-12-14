import serial
import time
import cv2 
import mediapipe as mp
import time
from time import sleep

megaBoard = serial.Serial('COM5', 9600)

def forward():
    megaBoard.write(b'F')
def Backward():
    megaBoard.write(b'B')
def Stop():
    megaBoard.write(b'Q')
def Left():
    megaBoard.write(b'L')
def Right():
    megaBoard.write(b'R')
    
     
def count_fingers(lst):
    cnt = 0

    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2
    # print(thresh)

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt += 1

    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 6:
        cnt += 1


    return cnt 

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)


# start_init = False 

# prev = -1

while True:
    # end_time = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        hand_keyPoints = res.multi_hand_landmarks[0]
        cnt = count_fingers(hand_keyPoints) 
        
        if cnt==5:
            forward()
        elif cnt==4:
            Backward()
        elif cnt==1:
            Left()
        elif cnt==2:
            Right()
        elif cnt==0:
            Stop()
            
#END......................................................                
        drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)
    cv2.imshow("window", frm)
    
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break

# FINGURES COUNT...................................................................................


     