from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
from math import sqrt

Block_colors = [[254, 220, 189],
                [255, 255, 255],
                [243, 152, 0],
                [255, 0, 255],
                [175, 223, 228],
                [255, 212, 0],
                [144, 238, 144],
                [247, 171, 166],
                [128, 128, 128],
                [211, 211, 211],
                [0,160,233],
                [167, 87, 168],
                [0, 103, 192],
                [153, 76, 0],
                [0, 177, 107],
                [239, 65, 35],
                [0,0,0]
                ]

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in Block_colors:
        cr,cg,cb = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

image_name = input('Please enter a file name.')
max_size = int(input('Please enter the maximum number of squares.'))

beautiful_view = Image.open(image_name)
im = cv2.imread(image_name)

h, w, c = im.shape
vertical = math.floor(w/h*max_size)
side = math.floor(h/w*max_size)

if w==h:  
  vertical = max_size
  side = max_size
elif w<h:
  side = max_size
else:
  vertical = max_size

beautiful_pixel = beautiful_view.resize((vertical,side))
plt.imshow(beautiful_pixel)

List_block = []
List_x = []
List_y = []

for vertical_number in range(vertical):
  for side_number in range(side):
    r,g,b = beautiful_pixel.getpixel((vertical_number,side_number))
    List_block.append(str(Block_colors.index(closest_color((r,g,b)))+666))
    List_x.append(str(vertical_number))
    List_y.append(str(side - side_number))

number = len(List_block) + 1

script = """
block = {' + ','.join(List_block) + '}
x = {' + ','.join(List_x) + '}
y = {' + ','.join(List_y) + '}
local function Block_Add(event)
 a = 1
 while( a <= " + str(number) + " ) do
   Block:replaceBlock(block[a],event.x + x[a],event.y + y[a],event.z, FACE_DIRECTION.DIR_POS_Y)
   a = a +1
 end
end
ScriptSupportEvent:registerEvent([=[Player.ClickBlock]=],Block_Add)
"""

print(script)
