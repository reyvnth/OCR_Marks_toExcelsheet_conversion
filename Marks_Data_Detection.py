# -*- coding: utf-8 -*-
"""
Created on Thu May  7 09:27:15 2020

@author: revukrishna2000
"""

import os
from google.cloud import vision
from google.cloud.vision import types
from google.cloud.vision import enums
import xlsxwriter 
import cv2

img = cv2.imread('test4.jpeg')
img=cv2.resize(img,(600,600))

fromCenter = False
ROIs = cv2.selectROIs('Select the region with name first, then roll no. and then marks', img, fromCenter)

ROI_1 = img[ROIs[0][1]:ROIs[0][1]+ROIs[0][3], ROIs[0][0]:ROIs[0][0]+ROIs[0][2]]
ROI_2 = img[ROIs[1][1]:ROIs[1][1]+ROIs[1][3], ROIs[1][0]:ROIs[1][0]+ROIs[1][2]]
ROI_3 = img[ROIs[2][1]:ROIs[2][1]+ROIs[2][3], ROIs[2][0]:ROIs[2][0]+ROIs[2][2]]

cv2.imwrite('Name.png', ROI_1)
cv2.imwrite('Roll.png', ROI_2)
cv2.imwrite('Marks.png', ROI_3)

cv2.waitKey(0)
cv2.destroyAllWindows()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'key.json'
client = vision.ImageAnnotatorClient()
workbook = xlsxwriter.Workbook('Marks.xlsx')
worksheet= workbook.add_worksheet()
parent_folder_path = r'C:\Users\revukrishna2000\Documents\Python Scripts\VisionAPIDemo'
features = [
    types.Feature(type=enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
    ]
requests = []
row=0
col=0   
for filename in ['Name.png','Roll.png','Marks.png']:
    filepath=os.path.join(parent_folder_path,filename)
    with open(filepath, 'rb') as image_file:
        image = vision.types.Image(content= image_file.read())
        request = types.AnnotateImageRequest(
        image=image, features=features)
        requests.append(request)
        response = client.document_text_detection(image=image)
        text = response.full_text_annotation.text
        li=text.splitlines()
        for elem in li:
            worksheet.write(row, col, elem)
            row+=1
        col+=1    
        row=0
        print("Done")
        
workbook.close()
    

