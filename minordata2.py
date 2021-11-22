Python 3.10.0 (tags/v3.10.0:b494f59, Oct  4 2021, 19:00:18) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import cv2 as cv
import os
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("data/train"):
    os.makedirs("data/train")
if not os.path.exists("data/test"):
    os.makedirs("data/test")
Labels=["Play","Pause","Volume Up","Volume Down","Forward","Reverse","Next","Previous"]
for s in Labels:
    if not os.path.exists("data/train/"+s):
        os.makedirs("data/train/"+s)
    if not os.path.exists("data/test/"+s):
        os.makedirs("data/test/"+s)

mode="test"
minValue=70
directory="data/"+mode+"/"
cam=cv.VideoCapture(0)
interrupt=-1
if not cam.isOpened():
    print("Error!Camera is not opened.")
    exit()
interrupt=-1
while True:
    ret,frame = cam.read()
    frame = cv.flip(frame, 1)
    count={"Play":len(os.listdir(directory+"Play")),
       "Pause":len(os.listdir(directory+"Pause")),
       "Volume Up":len(os.listdir(directory+"Volume Up")),
       "Volume Down":len(os.listdir(directory+"Volume Down")),
       "Forward":len(os.listdir(directory+"Forward")),
       "Reverse":len(os.listdir(directory+"Reverse")),
       "Next":len(os.listdir(directory+"Next")),
       "Previous":len(os.listdir(directory+"Previous"))
      }

    c=70
    for s in Labels:
        cv.putText(frame, s+str(count[s]), (10,c), cv.FONT_HERSHEY_PLAIN, 1.25, (55,0,255), 2)
        c=c+20
    x1 = int(0.5*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])
    cv.rectangle(frame, (220-1, 9), (720+1, 519), (255,0,0) ,1)
    roi = frame[10:510, 220:720]
    cv.imshow("Frame", frame)
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),2)
    th3 = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,11,2)
    ret, test_image = cv.threshold(th3, minValue, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    test_image = cv.resize(test_image, (300,300))
    cv.imshow("test", test_image)
    interrupt = cv.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
    if interrupt & 0xFF == ord('1'):
        cv.imwrite(directory+'Play/'+str(count['Play'])+'.jpg', roi)
    if interrupt & 0xFF == ord('2'):
        cv.imwrite(directory+'Pause/'+str(count['Pause'])+'.jpg', roi)
    if interrupt & 0xFF == ord('3'):
        cv.imwrite(directory+'Volume Up/'+str(count['Volume Up'])+'.jpg', roi)
    if interrupt & 0xFF == ord('4'):
        cv.imwrite(directory+'Volume Down/'+str(count['Volume Down'])+'.jpg', roi)
    if interrupt & 0xFF == ord('5'):
        cv.imwrite(directory+'Forward/'+str(count['Forward'])+'.jpg', roi)
    if interrupt & 0xFF == ord('6'):
        cv.imwrite(directory+'Reverse/'+str(count['Reverse'])+'.jpg', roi)
    if interrupt & 0xFF == ord('7'):
        cv.imwrite(directory+'Next/'+str(count['Next'])+'.jpg', roi)
    if interrupt & 0xFF == ord('8'):
        cv.imwrite(directory+'Previous/'+str(count['Previous'])+'.jpg', roi)
cam.release()
cv.destroyAllWindows()
