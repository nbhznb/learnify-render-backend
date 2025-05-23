"""
Methods related to processing the complete image as a whole
"""
import cv2
import numpy as np

"""
Takes cv2 image object. Returns the cropped image object.
"""
def cropImage(img):
    # Invert colors so that OpenCV can find bounding rectangle
    img = invertColors(img)
    # Find bounding rectangles
    x, y, w, h = cv2.boundingRect(img)

    # Crop image
    crop_img = img[y:y+h, x:x+w]

    # Invert colors to restore the original image
    crop_img = invertColors(crop_img)

    return crop_img

"""
Turns black over white to white over black and vice-versa
"""
def invertColors(img):
    img = cv2.bitwise_not(img)
    return img

"""
Returns true if img is a square image
"""
def isSquare(img):
    return img.shape[0] == img.shape[1]

"""
Splits given square image into a quadrant and the rest of the image
returns quad, rest_of_the_image
"""
def splitQuad(img, quad_number=0):
    # 0,1,2,3 => first_quad, second_quad, third_quad, fourth_quad
    quad_number = quad_number % 4
    height, width = img.shape  # Corrected order: height comes first, then width
    tmp_img = np.copy(img)

    if quad_number == 0:
        tmp_img[0:height//2, width//2:width] = 255  # Use integer division
        return img[0:height//2, width//2:width], tmp_img
    elif quad_number == 1:
        tmp_img[0:height//2, 0:width//2] = 255  # Use integer division
        return img[0:height//2, 0:width//2], tmp_img
    elif quad_number == 2:
        tmp_img[height//2:height, 0:width//2] = 255  # Use integer division
        return img[height//2:height, 0:width//2], tmp_img
    else:
        tmp_img[height//2:height, width//2:width] = 255  # Use integer division
        return img[height//2:height, width//2:width], tmp_img

def apply(polys, func_names, params):
    assert len(polys) == len(func_names) and len(func_names) == len(params)
    for i in range(len(polys)):
        if func_names[i] == 'flip':
            # apply something on the object
            polys[i].flip(how=params[i]['how'])
        elif func_names[i] == 'rotate':
            polys[i].rotate(theta=params[i]['theta'])
        elif func_names[i] == 'add_vertex':
            polys[i].add_vertex()
        elif func_names[i] == 'delete_vertex':
            polys[i].delete_vertex()
        elif func_names[i] == 'clone_circumcircle':
            polys[i].clone_circumcircle(otherpoly=params[i]['otherpoly'])
        elif func_names[i] == 'setHatch':
            polys[i].setHatch(hatch=params[i]['hatch'])
        elif func_names[i] == 'swap_polygons':
            polys[i].swap_polygons(otherpoly=params[i]['otherpoly'])
