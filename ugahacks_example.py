import os
from PIL import Image as pimg
import cv2

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/will/Downloads/ugahacks.json"

def localize_objects(path, output):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    im = pimg.open(path)
    width, height = im.size
    arrX = []
    arrY = []
    tlx = 0
    tly = 0
    brx = 0
    bry = 0
    i = 0

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations
    
    for object_ in objects:
        
        for vertex in object_.bounding_poly.normalized_vertices:
            # Converts back to non-normalized vertices
            arrX.append(vertex.x * width)
            arrY.append(vertex.y * height)
            
            if i == 0:
                tlx = vertex.x * width
                tly = vertex.y * height
            if i == 1:
                brx = vertex.x * width
                bry = vertex.y * height
            i = i + 1

    print(objects[0].name)
    print(tlx, tly, brx, bry)
    crop = (brx, bry, tlx, bry)
    crop_img = im.crop(crop)
    crop_img.show()

        #print(arrX)
        #print(arrY)



    # Prints info about objects found in image. Useful for debugging. TL, TR, BR, BL
    # print('Number of objects found: {}'.format(len(objects)))
    # for object_ in objects:
    #     print('\n{} (confidence: {})'.format(object_.name, object_.score))
    #     print('Normalized bounding polygon vertices: ')
    #     for vertex in object_.bounding_poly.normalized_vertices:
    #         print(' - ({}, {})'.format(vertex.x, vertex.y))
    


localize_objects("/home/will/Downloads/jakey.jpg", "/home/will/Downloads/jakey2.jpg")