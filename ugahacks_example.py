import os
from PIL import Image as pimg
import cv2
import time
import database

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/will/Downloads/ugahacks.json"

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
    
    for x in range(len(objects)):
        print(objects[x].name)
        print(tlx[x], tly[x], brx[x], bry[x])
        crop = (tlx[x], tly[x], brx[x], bry[x])
        crop_img = im.crop(crop)
        crop_img = crop_img.rotate(-90)
        #crop_img.show()
        name = ("/home/will/Desktop/UGAHacks/cropImgs_" + str(x) + ".jpg")
        crop_img.save(name, "JPEG")
        database.name.append(objects[x].name)


    # Prints info about objects found in image. Useful for debugging. TL, TR, BR, BL
    # print('Number of objects found: {}'.format(len(objects)))
    # for object_ in objects:
    #     print('\n{} (confidence: {})'.format(object_.name, object_.score))
    #     print('Normalized bounding polygon vertices: ')
    #     for vertex in object_.bounding_poly.normalized_vertices:
    #         print(' - ({}, {})'.format(vertex.x, vertex.y))
    


localize_objects("/home/will/Downloads/jakey.jpg")