# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import matplotlib.image as mpimg

from PIL import Image
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# import cv2
import extcolors

from colormap import rgb2hex

input_name = 'SABANCI.jpg'
output_width = 900                   #set the output size
img = Image.open(input_name)
wpercent = (output_width/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((output_width,hsize), Image.ANTIALIAS)

#save
# resize_name = 'resize_' + input_name  #the resized image name
# img.save(resize_name)                 #output location can be specified before resize_name

#read

img_url = input_name



colors_x = extcolors.extract_from_path(img_url, tolerance = 12, limit = 12)

# print(colors_x[0][0][1]) output in RGB

for i in range(len(colors_x[0])):
    color = colors_x[0][i][0]
    occurrence = colors_x[0][i][1]
    print("-"*25)
    
    print(color,occurrence)

