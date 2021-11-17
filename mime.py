from tkinter import *
import os
os.system('clear')
import cv2
from PIL import Image, ImageTk
import HandTrackingModule as htm

# Dimensions for video:
# If your webcam supports 1080p:
# wCam, hCam = 1980, 1080
# If your webcam supports 720p:
wCam, hCam = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detectionCon=0.8)
fingerTips = [4, 8, 12, 16, 20]

###############################
#            GUI              #
###############################
root = Tk()
root.title('Mime')
root.geometry(str(wCam) + 'x' + str(hCam))
root.bind('<Escape>', lambda e: root.quit())

lmain = Label(root)
lmain.pack()

def to_pil(img, label, w, h):
    img = cv2.resize(img, (w, h))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    pic = ImageTk.PhotoImage(image)
    label.configure(image=pic)
    label.image = pic
    label.place(x=0, y=0)


def translate(img):
    lmList = detector.findPos(img, False)
    #print(lmList)
    if len(lmList)!=0:
        fingers = []

        # Thumb
        if lmList[fingerTips[0]][1] > lmList[fingerTips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1,5):
            if lmList[fingerTips[id]][2] < lmList[fingerTips[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        phrase = ""
        if fingers == [0, 1, 1, 1, 1]:
            phrase = "Hello!"
        elif fingers == [1, 1, 1, 1, 1]:
            phrase = "Thank You!"
        elif fingers == [1, 0, 0, 0, 0]:
            phrase = "Goodbye!"
        elif fingers == [0, 0, 0, 0, 0]:
            phrase = "Yes"
        elif fingers == [1, 1, 1, 0, 0]:
            phrase = "No"

        if phrase in ['Hello!', 'Yes', 'No']:
            x1, y1 = 600,700
        else: 
            x1, y1 = 550,700
        
        cv2.putText(img, phrase, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (150,200,100), 2)


def app():
    _, img = cap.read()
    img = detector.findHands(img, False)
    x1,y1,x2,y2 = 0, 670,1280,700
    cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,0), 50)
    translate(img)
    to_pil(img, lmain, wCam, hCam)
    root.after(1, app)

app()
root.mainloop()
cv2.destroyAllWindows()
cap.release()
