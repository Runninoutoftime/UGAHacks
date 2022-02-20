import os
from PIL import Image as pimg
import cv2
import time
import getcolor
import colorfinder
import subprocess
import backgroundremover
from google_images_search import GoogleImagesSearch

from matplotlib.pyplot import gray
import database
import glob
import shutil as sh
from colorthief import ColorThief
import webcolors
from google.cloud import storage, vision
import requests
import numpy as np


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/will/Downloads/ugahacks.json"
mainloop = 0
gis = GoogleImagesSearch("AIzaSyBAjAcE1EJIKgIEZlYRpRfDBkbnU138DYg", "17188311404214169")

# Creates a list of localized objects in an image.
# Finds bounding boxes around them, then saves them to database along with ID
def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    im = pimg.open(path)
    width, height = im.size
    tlx = []
    tly = []
    brx = []
    bry = []
    i = 0

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations
    
    for object_ in objects:
        i = 0

        for vertex in object_.bounding_poly.normalized_vertices:

            # Converts back to non-normalized vertices
            if i == 0:
                tlx.append(vertex.x * width)
                tly.append(vertex.y * height)
            if i == 2:
                brx.append(vertex.x * width)
                bry.append(vertex.y * height)

            i = i + 1
    
    i = 0
    for x in range(len(objects)):
        allowed = ["Top", "Shoe", "Pants", "Footwear", "Dress", "Outerwear", "Jeans", "Jacket"]
        shoesFound = False


        if objects[x].name in allowed:
            if objects[x].name == "Shoe" or "Footwear":
                shoesFound = True
            if shoesFound == True:
                allowed.remove("Shoe")
                allowed.remove("Footwear")
            crop = (tlx[x], tly[x], brx[x], bry[x])
            crop_img = im.crop(crop)
            #crop_img = crop_img.rotate(-90)
            #crop_img.show()
            name = ("/home/will/Desktop/UGAHacks/cropImgs/img_" + str(i) + ".jpg")
            crop_img.save(name, "JPEG")
            database.name.append(objects[x].name)
            i = i + 1
    
# Finds dominant color among an image
def find_colors():
    
    for x in range(len(database.name)):
        cf = ColorThief("/home/will/Desktop/UGAHacks/pngImgs/img_" + str(x) + ".png")
        dc = cf.get_color(quality=1)
        print(dc)
        database.color.append(dc)
        #print(webcolors.rgb_to_hex(dc))
        #colors = getcolor.get_colors("/home/will/Desktop/UGAHacks/pngImgs/img_" + str(x) + ".png", numcolors=3, resize=150)
        #colors = colorfinder.colorz("/home/will/Desktop/UGAHacks/pngImgs/img_" + str(x) + ".png")
        #print("Name: " + database.name[x] + " Color: " + str(list(colors)))



# Removes background on images and stores them as JPG after converting from PNG
def remove_background():

    for x in range(len(database.name)):
        file = "/home/will/Desktop/UGAHacks/cropImgs/img_" + str(x) + ".jpg"
        output_file = "/home/will/Desktop/UGAHacks/pngImgs/img_" + str(x) + ".png"
#        final_file = "/home/will/Desktop/UGAHacks/jpgImgs/img_" + str(x) + ".jpg"
        subprocess.call(["backgroundremover", "-i", file, "-o", output_file])
#        im = pimg.open(output_file)
#        im.save(final_file)

def gatherStyle():
    sh.rmtree("/home/will/Desktop/UGAHacks/googleStyle")
    os.makedirs("/home/will/Desktop/UGAHacks/googleStyle")
    query = database.age_group + " " + database.skin_tone + " " + database.gender + " " + database.formality + " " + database.season + ""
    params = {
        'q': query,
        'num': 1,
        "fileType": "jpg",
        "imgColorType": "color",
        #"imgSize": "HUGE"
    }
    
    print(query)
    gis.search(search_params=params, path_to_dir="/home/will/Desktop/UGAHacks/googleStyle")
    
    return "/home/will/Desktop/UGAHacks/googleStyle"
    

# Main loop
# Analyzes image, segments clothing, removes background, and analyzes the colors of the clothing
def process(path):

    sh.rmtree("/home/will/Desktop/UGAHacks/cropImgs/")
    sh.rmtree("/home/will/Desktop/UGAHacks/pngImgs/")
    os.makedirs("/home/will/Desktop/UGAHacks/cropImgs")
    os.makedirs("/home/will/Desktop/UGAHacks/pngImgs")

    localize_objects(path)
    print(database.name)

    remove_background()
    
    find_colors() #List of all rgb dominant colors for each item in outfit

    print(str(database.color))

    txt = open("colorTxt.txt", "w")
    for t in database.color:
        txt.write(' '.join(str(s) for s in t) + "\n")
    txt.close()

    names = open("namesTxt.txt", "w")
    for t in database.name:
        names.write(''.join(str(s) for s in t) + "\n")
    names.close()



#def startup():




#path = "/home/will/Downloads/will2.jpg"

dir = gatherStyle()
pathList = os.listdir(dir)
path = ' '.join(pathList)
path = "/home/will/Desktop/UGAHacks/googleStyle/" + path
#path = str(os.listdir(dir))[1, os.listdir(dir).length - 1, 1]

path = "/home/will/Desktop/UGAHacks/person.jpg"
print(path)
process(path)
