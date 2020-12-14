import cv2
import numpy as np

# 画像ではなくまっさらな下地となる200x300の黒い画像を生成
# zerosの引数がheightが先になるので注意
height = 1920
width = 1080
img = np.zeros((height, width, 3), np.uint8)


# 線を引く（線を引く画像、座標、線の色、線の太さをパラメータに指定）
# 細めの赤線
img = cv2.line(img,(0,0),(width,height),(0,0, 255),1)
# 太めの青線
img = cv2.line(img,(width,0),(0,height),(255,0, 0),5)
cv2.imwrite("line.jpg", img)