#import cv2
import os
#import mediapipe as mp
import numpy as np
import unidecode


from flask import url_for , current_app

#mp_drawing = mp.solutions.drawing_utils
#mp_selfie_segmentation = mp.solutions.selfie_segmentation

""" def remove_background(filename):
    BG_COLOR = (255, 255, 255)
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=0) as selfie_segmentation:
        filename = os.path.join('images',filename)
        path = current_app.root_path + url_for('static', filename = filename)
        image = cv2.imread(path)
        image_height, image_width, _ = image.shape
        results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        output_image = np.where(condition, image, bg_image)
        cv2.imwrite(path, output_image)
    return True """

def save_file(file, filename):
    if not (file and filename):
        return False
    filename = os.path.join('images',filename)
    path = current_app.root_path + url_for('static', filename = filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    """ file_exists = os.path.exists(path)
    if not file_exists:
        img_file = open(path,'wb')
        img_file.close() """
    file.save(path)
    return True

def file_handler(file):
    if file.filename != '':
        image_name = file.filename.replace(" ", "").lower()
        image_name = unidecode.unidecode(image_name)
        return file , image_name
    return None, None

""" def resize(filename, width, height):
    filename = os.path.join('images',filename)
    path = current_app.root_path + url_for('static', filename = filename)
    image = cv2.imread(path)
    image = cv2.resize(image, (width, height))
    cv2.imwrite(path, image)
    return True """