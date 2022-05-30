from PIL import Image, ImageDraw
import cv2
import os
#
images = []
width = 1920
heigth = 1080
color1 = (0, 0, 0)
color2 = (159, 163, 163)
radius = 45

# for i in range(1, 3, 1):
#     im = Image.new('RGB', (width, heigth), color2)
#     draw = ImageDraw.Draw(im)
#     draw.ellipse((width - width/i, heigth/2, radius, radius), fill=color1)
#     images.append(im)
#
# images[0].save('video.gif', save_all=True, append_images=images[1:], optimize=False, duration=20/3, loop=3)
im = Image.new('RGB', (width, heigth), color2)
draw = ImageDraw.Draw(im)
# draw.ellipse((width - width/3 - radius, heigth/2 - radius, width - width/3 + radius, heigth/2 + radius), fill=color1)
draw.ellipse((width/4 - radius, heigth/30, width/4 + radius, heigth/30 + 2*radius), fill=color1)
draw.ellipse((width/2 - radius, heigth/30, width/2 + radius, heigth/30 + 2*radius), fill=color1)
draw.ellipse((width - width/4 - radius, heigth/30, width-width/4+radius, heigth/30 + 2*radius), fill=color1)
im.save('img.jpg', quality=100)

# frames = []
# for i in range(1, 3, 1):
#     frame = Image.open(f'{i}.jpg')
#     frames.append(frame)
#
# frames[0].save('video.gif', save_all=True, optimize='True', duration=20/3, loop=3)
# im0 = Image.open('images/0.jpg')
# im1 = Image.open('images/1.jpg')
# im2 = Image.open('images/2.jpg')
# im3 = Image.open('images/3.jpg')
# im0.save('video2.gif', save_all=True, append_images=[im1, im2, im3], duration=[3000, 6000, 6000, 6000], loop=3)


