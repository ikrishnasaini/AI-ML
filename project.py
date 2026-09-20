# Hand Gesture Control using MediaPipe and PyAutoGUI
# This script uses MediaPipe to detect hand gestures and PyAutoGUI to control the mouse and keyboard based on those gestures.

import mediapipe as mp
import cv2
import time
import math
import pyautogui

# Configure PyAutoGUI
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1 , min_detection_confidence = 0.7) 


# Start video capture
cap = cv2.VideoCapture(0)


#gesture time control
click_strat_time = 0
click_time =[]
click_cooldown = 0.5
scroll_mode = False
freeze_cursor = False
screenshot_cooldown = 2
last_screenshot_time = 0
alpha = 0.3
click_threshold = 0.06


#Get screen size
screen_width , screen_height = pyautogui.size()
print("\n Hand Gesture Control")
prev_screen_x ,prev_screen_y = 0,0


#Check if webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
while True:
    ret,frame = cap.read()    
    if not ret:
        print("Error: Could not read frame.")
        break
    frame = cv2.flip(frame,1)
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        #get finger tips
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]

        fingers = [
            1 if hand_landmarks.landmark[tip].y<hand_landmarks.landmark[tip-2].y else 0
            for tip in [8,12,16,20]
        ]
        #distace between thumb and index finger
        distance = math.hypot(thumb_tip.x - index_tip.x , thumb_tip.y - index_tip.y)
        if distance < click_threshold:
            if not freeze_cursor:
                freeze_cursor = True
                click_time.append(time.time())

                #double click
                if len(click_time) >= 2 and click_time[-1] - click_time[-2]< 0.4:
                    pyautogui.doubleClick()
                    cv2.putText(frame,"Double click",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2 )
                    click_time = []
                else:
                    pyautogui.click()
                    cv2.putText(frame,"Single click",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2 )
        else:
                freeze_cursor = False
    
        # Move cursor
        if not freeze_cursor:
            screen_x = int(index_tip.x * screen_width)
            screen_y = int(index_tip.y * screen_height)
            x = int(prev_screen_x + alpha * (screen_x - prev_screen_x))
            y = int(prev_screen_y + alpha * (screen_y - prev_screen_y))
            pyautogui.moveTo(x, y)
            prev_screen_x, prev_screen_y = x, y
    

        #Scroll mode
        if sum(fingers) == 4:
            scroll_mode = True
        else:
            scroll_mode =False

        # Scroll mode (all four fingers open)
        if sum(fingers) == 4:
            scroll_mode = True
        else:
            scroll_mode = False
        
        if scroll_mode:
            if index_tip.y < 0.4:
                pyautogui.scroll(60)
                cv2.putText(frame, " Scroll Up", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            elif index_tip.y > 0.4:
                pyautogui.scroll(-60)
                cv2.putText(frame, " Scroll Down", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Screenshot (index + middle open, ring + pinky closed)
        if fingers == [1, 1, 1, 0]:
            current_time = time.time()
            if current_time - last_screenshot_time > screenshot_cooldown:
                pyautogui.screenshot(f'screenshot_{current_time}.png')
                cv2.putText(frame, "Screenshot", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                last_screenshot_time = current_time

         # Page Back (middle + ring + pinky open)
        if fingers == [0, 1, 1, 1]:
            cv2.putText(frame, "Page Back", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            pyautogui.hotkey('alt', 'left')
            time.sleep(0.5)
        
    
        # Play/Pause (three fingers)
        if fingers == [1,0,0,1]:
            pyautogui.press("space")
            cv2.putText(frame, "Play/Pause", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            time.sleep(0.4)
        
       # Volume Control
        if fingers == [1, 0, 1, 1]:
            pyautogui.press("volumeup")
            cv2.putText(frame, "Volume Up", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        if fingers == [1, 1, 0, 1]:
            pyautogui.press("volumedown")
            cv2.putText(frame, "Volume Down", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)


    # Display the resulting frame
    cv2.imshow('Webcam',frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
    