# -*- coding: utf-8 -*-
"""
Created on Wed May  5 20:27:53 2020

@author: revukrishna2000
"""

import os, io
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'key.json'
client = vision.ImageAnnotatorClient()

parent_folder_path = r'C:\Users\revukrishna2000\Documents\Python Scripts\VisionAPIDemo\Images'
image_name = 'test5.jpg'
file_location = os.path.join(parent_folder_path, image_name)

img = Image.open(file_location)
img.thumbnail((600, 600))
buffer = io.BytesIO()
img.save(buffer, "PNG")

content = buffer.getvalue()
image = vision.types.Image(content=content)
response = client.document_text_detection(image=image)

text = response.full_text_annotation.text
print(text)

