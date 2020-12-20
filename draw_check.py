import cv2
import numpy as np
import time
import numpy
a_temp=int(0)

height = 1080
width = 1920
img = np.zeros((height, width, 3), np.uint8)

print("OpenCV: " + cv2.__version__)
print("NumPy: " + numpy.__version__)


cv2.putText(img, "1", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), thickness=2)
cv2.putText(img, "2", (10,height-30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
cv2.putText(img, "3", (width-30,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
cv2.putText(img, "4", (width-30,height-30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), thickness=2)

cv2.namedWindow("dsp", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("dsp", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("dsp", img)
print("show")

while 1:
    a_temp +=1
    img = np.zeros((height, width, 3), np.uint8)
    cv2.putText(img, "1", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), thickness=2)
    cv2.putText(img, "2", (10,height-30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
    cv2.putText(img, "3", (width-30,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), thickness=2)
    cv2.putText(img, "4", (width-30,height-30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), thickness=2)
    cv2.putText(img, str(int(a_temp))  , (int(width/2),int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
    cv2.imshow("dsp", img)
    k=cv2.waitKey(100)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
