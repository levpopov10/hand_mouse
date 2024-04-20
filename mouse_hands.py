from tkinter import *
from tkinter import ttk
import cv2
import pyautogui
import mediapipe as mp
from numpy import *

def start():
    cap=cv2.VideoCapture(0)

    hands=mp.solutions.hands.Hands(static_image_mode=False,
                            max_num_hands=2,
                            min_tracking_confidence=0.5, min_detection_confidence=0.5)

    screenWidth, screenHeight = pyautogui.size()
    mpDraw=mp.solutions.drawing_utils

    def l_click(id1, id2, landmarks):
        # Получаем координаты двух точек по их ID
        x1, y1 = landmarks.landmark[id1].x, landmarks.landmark[id1].y
        x2, y2 = landmarks.landmark[id2].x, landmarks.landmark[id2].y
        if y1>=y2 :
            return pyautogui.click()
        
    def r_click(id1, id2, landmarks):
        # Получаем координаты двух точек по их ID
        x1, y1 = landmarks.landmark[id1].x, landmarks.landmark[id1].y
        x2, y2 = landmarks.landmark[id2].x, landmarks.landmark[id2].y
        if y1>=y2 :
            return pyautogui.rightClick()

    def d_click(id1, id2, landmarks):
        # Получаем координаты двух точек по их ID
        x1, y1 = landmarks.landmark[id1].x, landmarks.landmark[id1].y
        x2, y2 = landmarks.landmark[id2].x, landmarks.landmark[id2].y
        if result.multi_handedness[hand_no].classification[0].label == 'Left':
            if x1<=x2 :
                pyautogui.doubleClick()
        elif result.multi_handedness[hand_no].classification[0].label == 'Right':
            if x1>=x2 :
                pyautogui.doubleClick()

    while True:
        _,img=cap.read()
        img = cv2.flip(img, 1)
        result=hands.process(img)
        if result.multi_hand_landmarks:
            for hand_no, hand_landmarks in enumerate(result.multi_hand_landmarks):

                for id, lm in enumerate(hand_landmarks.landmark):
                    h,w,_=img.shape
                    cx,cy=int(lm.x*w),int(lm.y*h)
                    cv2.circle(img,(cx,cy),3,(255,0,0))
                    if id==8:
                        cv2.circle(img,(cx,cy),5,(255,255,0),cv2.FILLED)
                        pyautogui.moveTo((cx*screenWidth/w), (cy*screenHeight/h))
                    if id==12:
                        cv2.circle(img,(cx,cy),5,(255,0,0))

                mpDraw.draw_landmarks(img,hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                l_click(12, 8, hand_landmarks)
                d_click(4, 8, hand_landmarks)
                r_click(16, 11, hand_landmarks)

        cv2.imshow("Hand",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

root = Tk()
root.title("HANDS")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Start program").grid(column=0, row=0)
ttk.Button(frm, text="start", command=start).grid(column=0, row=2)
ttk.Label(frm, text="Push 'q' and you will close program").grid(column=0, row=3)
ttk.Button(frm, text="exit", command=root.destroy).grid(column=0, row=4)
root.mainloop()


