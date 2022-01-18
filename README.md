

  ```
  import face_recognition
  import cv2
  import smtplib
  import json
  import PIL.Image
  from PIL import ImageChops
  from newsapi import NewsApiClient
  import requests
  import tkinter as tk
  import os
  from tkinter import *
  from email.mime.multipart import MIMEMultipart
  from email.mime.image import MIMEImage
  from email.mime.text import MIMEText
  import time
  import sqlite3
  
  
#sqlitehoz ciklusok

# sqlite adatbázis létrehozása függvény:
def create_database():
    # Image adatbázis létrehozása
    image_database = sqlite3.connect("Image_data.db")
    data = image_database.cursor()

    a = data.execute("CREATE TABLE IF NOT EXISTS Image(Image BLOB)")
    print(a)
    image_database.commit()
    image_database.close()


# adott kép byte formára alakítása, majd annak a beolvasása a photo_image változóba és ezt a változót adja vissza a függvény
def conver_image_into_binary(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
    return photo_image


# ez egy eljárás, amely bekér egy képhez tartozó Path-t és ezt az adott képet elhelyezi az Image_data adatbázisban Blob-ként
def insert_image(image):
    image_database = sqlite3.connect("Image_data.db")
    data = image_database.cursor()

    insert_photo = conver_image_into_binary(image)
    data.execute("INSERT INTO Image Values(:image)",
                 {'image': insert_photo})

    image_database.commit()
    image_database.close()
