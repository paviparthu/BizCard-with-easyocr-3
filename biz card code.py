#Imoprt libraries -------->

#Data frame library
import pandas as pd

#Scanning libraries

import easyocr # (Optical Character Recognition)
import numpy as np
import PIL
from PIL import Image, ImageDraw
import cv2
import os
import re


#Database libraries
#import sqlalchemy
#import mysql.connector

#from sqlalchemy import create_engine

#Dashboard library
#import streamlit as st

 # import image
import_image = PIL.Image.open('E:\PAVITHRA\biz card pro3\BizCard project details\1.png')
import_image


if import_image is not None:
    try:
        # Create the reader object with desired languages
        reader = easyocr.Reader(['en'], gpu=False)
    except ModuleNotFoundError:
        print("Error: easyocr module is not installed. Please install it.")

    try:
        # Read the image file as a PIL Image object
        if isinstance(import_image, str):
            image = Image.open(import_image)
        elif isinstance(import_image, Image.Image):
            image = import_image
        else:
            raise ValueError("Invalid image format. Please provide a file path or a PIL Image object.")

        # Convert the image to a numpy array
        image_array = np.array(image)

        # Perform OCR on the image
        text_read = reader.readtext(image_array)

        # Extract the text
        #result = [text[1] for text in text_read]
        result = []
        for text in text_read:
            result.append(text[1])

        # Convert the result to the desired format
        #formatted_result = "\n".join(result)
        #print(formatted_result)

    except Exception as e:
        print("Error: Failed to process the image. Please try again with a different image.")
        print(e)
else:
    print("Error: No image provided.")



def draw_boxes(import_image, text_read, color='yellow', width=2):
    draw = ImageDraw.Draw(import_image)
    for bound in text_read:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return import_image

result_image = draw_boxes(import_image, text_read)
result_image

def get_data(res):
    city = ""  # Initialize the city variable
    for ind, i in enumerate(res):
        # To get WEBSITE_URL
        if "www " in i.lower() or "www." in i.lower():
            data["Website"].append(i)
        elif "WWW" in i:
            data["Website"].append(res[ind-1] + "." + res[ind])

        # To get EMAIL ID
        elif "@" in i:
            data["Email"].append(i)

        # To get MOBILE NUMBER
        elif "-" in i:
            data["Mobile_number"].append(i)
            if len(data["Mobile_number"]) == 2:
                data["Mobile_number"] = " & ".join(data["Mobile_number"])

        # To get COMPANY NAME
        elif ind == len(res) - 1:
            data["Company_name"].append(i)

        # To get CARD HOLDER NAME
        elif ind == 0:
            data["Card_holder"].append(i)

        # To get DESIGNATION
        elif ind == 1:
            data["Designation"].append(i)

        # To get AREA
        if re.findall("^[0-9].+, [a-zA-Z]+", i):
            data["Area"].append(i.split(",")[0])
        elif re.findall("[0-9] [a-zA-Z]+", i):
            data["Area"].append(i)

        # To get CITY NAME
        match1 = re.findall(".+St , ([a-zA-Z]+).+", i)
        match2 = re.findall(".+St,, ([a-zA-Z]+).+", i)
        match3 = re.findall("^[E].*", i)
        if match1:
            city = match1[0]  # Assign the matched city value
        elif match2:
            city = match2[0]  # Assign the matched city value
        elif match3:
            city = match3[0]  # Assign the matched city value

        # To get STATE
        state_match = re.findall("[a-zA-Z]{9} +[0-9]", i)
        if state_match:
            data["State"].append(i[:9])
        elif re.findall("^[0-9].+, ([a-zA-Z]+);", i):
            data["State"].append(i.split()[-1])
        if len(data["State"]) == 2:
            data["State"].pop(0)

        # To get PINCODE
        if len(i) >= 6 and i.isdigit():
            data["Pin_code"].append(i)
        elif re.findall("[a-zA-Z]{9} +[0-9]", i):
            data["Pin_code"].append(i[10:])

    data["City"].append(city)  # Append the city value to the 'city' array


get_data(result)


data_df = pd.DataFrame(data)

data_df.T


