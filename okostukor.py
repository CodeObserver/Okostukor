#okostükör

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
    
    
    
time.sleep(5)
# egy végtelen ciklus ami addig megy ameddig észre nem vesz valami mozgást (azaz hogyy megváltozott az eredeti kép, akkor egyből továbbmegy)
vid = cv2.VideoCapture(0)
ret, frame = vid.read()
# egy képkocka beolvasása, ez lesz az amihez majd hasonlítjuk a videóból származó képkockát, hogy megtudjuk hogy van e valami mozgás(nagy változás a képen)
cv2.imwrite('elso.jpeg', frame)
# itt az elso változóban megkapjuk az első képünkhöz tartozó pixelszámot,amely még az árnyalat változásokat is figyelembe veszi
elsoo = os.path.getsize('elso.jpeg')
a = 0
# 5 másodperc várás mielőtt elindítjuk a ciklust
while a != 1:
    ret, frame = vid.read()
    # második jpeg kép létrehozása
    cv2.imwrite('masodik.jpeg', frame)
    # ennek a második képnek megnézzök a pixelszámát ugyanúgy mint az elsőnek
    masodik = os.path.getsize('masodik.jpeg')
    print("elso:", elsoo, " masodik:", masodik)
    # hogyha 13000 pixel különbség van a két kép között akkor az nagy eséllyel jelenti azt hogy nagy változás történt azaz mozgás történt
    if ((elsoo - masodik) > 13000 or (elsoo - masodik) < -13000):
        a = 1
        break
vid.release()
cv2.destroyAllWindows()
    
    
    

