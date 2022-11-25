# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import matplotlib.image as mpimg
 
import cv2, time
import numpy as np

from ast import Pass
from math import comb
from turtle import color
from PIL import Image
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# import cv2
import extcolors

from colormap import rgb2hex

img_url = 'color\SABANCI.jpg'
output_width = 900                   #set the output size
img = Image.open(img_url)
wpercent = (output_width/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((output_width,hsize), Image.ANTIALIAS)

#save
# resize_name = 'resize_' + input_name  #the resized image name
# img.save(resize_name)                 #output location can be specified before resize_name

#read

def removeOccurence(colorList):
    newList = []
    for colorIndex in colorList[0]:
        newList.append(colorIndex[0])
    return newList


def difference(c1, c2):
    return (abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])) / 3

def newColor(c1, c2):
    c1Value = c1[0] + c1[1] + c1[2]
    c2Value = c2[0] + c2[1] + c2[2]

    if c1Value >= c2Value:
        return c1

    else:
        return c2

    # red = round((c1[0] + c2[0]) / 2)
    # green = round((c1[1] + c2[2]) / 2)
    # blue = round((c1[2] + c2[2]) / 2)
    # return (red,green,blue)

def combineColors(colorList, tolerance, colorAmount, tryAmount, tryLimit):
    changedColors = []
    tryAmount += 1

    for c1 in colorList:
        for i in range(1, len(colorList)):
            #Değerleri Sadeleştirme 
            c2 = colorList[i]
            # print(c1, " - ", c2)
            if c1 == c2:
                continue
            
            result = difference(c1, c2)

            if result < tolerance:
                combinedColor = newColor(c1, c2)


                colorList.remove(c1)
                colorList.remove(c2)
                colorList.append(combinedColor)
                changedColors.append((c1,c2,combinedColor))
                break
    print(tryAmount, " - ", tryLimit)

    if tryAmount == tryLimit:
        return colorList

    if len(colorList) > colorAmount:
        combineColors(colorList, tolerance, colorAmount, tryAmount, tryLimit)

    return[colorList]

colors_x = extcolors.extract_from_path(img_url, tolerance = 12, limit = 12)
# print(colors_x[0][0][1]) output in RGB

# print(colors_x[0])
# for i in range(len(colors_x[0])):
#     color = colors_x[0][i][0]

#     print(color)

# print(removeOccurence(colors_x))

tolerance = 30
colorAmount = 5
print(combineColors(removeOccurence(colors_x), tolerance, colorAmount,tryLimit=abs((len(colors_x) - colorAmount)), tryAmount=0))

colors = combineColors(removeOccurence(colors_x), tolerance, colorAmount,tryLimit=abs((len(colors_x) - colorAmount)), tryAmount=0)
img = np.zeros((300,650,3), np.uint8)
window_name = 'Trackbar Color Palette'
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
print(colors[0])
while(True):

    for i in colors:
        for j in range(len(colors)):

            cv2.imshow(window_name,img)
            key = cv2.waitKey(1) & 0xFF

            print(i, i[j][2], "-", i[j][1], "-", i[j][0])

            # img[:] = [i[j][2], i[j][1], i[j][0]]
            time.sleep(1)
            if key == ord('q'):
                break
cv2.destroyAllWindows()





