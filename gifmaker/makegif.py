import time
import cv2
import numpy as np
from mss import mss
import mss.tools
import glob
from PIL import Image
import shutil
import os
import re

# filepaths
fp_in = "capture/*.png"
fp_out = "output/image1.gif"


def create_gif(duration=100):
    images = glob.glob(fp_in)
    n_images=len(images)
    images_int = [re.sub("[^0-9]", "",item) for item in images]
    images_sorted =sorted(images_int,key=int)
    images_png=["capture/" + item + ".png" for item in images_sorted]

    img, *imgs = [Image.open(f) for f in images_png]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=duration, loop=0)
    

    


def capture_images(nImages=150,delay=1/15,top=0,left=0,width=1000,height=1000):
    """ Capture and save screenshots"""
    try:
        os.mkdir("capture")
    except:
        pass
    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": int(width), "height": int(height)}
        #output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        sct.compression_level = 2
        #sct_img = sct.grab(monitor)

        for n in range(nImages):
            sct_img=sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=f'capture/{n}.png'.format(**monitor))
            print(n)
            time.sleep(delay)



def flush():
    """removes all temporary screenshots,
       run after gif is created"""
    shutil.rmtree("capture", ignore_errors=True)



def combined(nImages=150,delay=1/15,top=0,left=0,width=500,height=500,duration=100):
    capture_images(nImages,delay,top,left,width,height)
    create_gif(duration)
    flush()



if __name__ == '__main__':
    capture_images()
    create_gif()
    flush()


