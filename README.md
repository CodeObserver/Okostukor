

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

# eltávolítjuk az első és a második képet is a mappából mert már nincs rájuk szükségünk, valamint így nem marad nyoma ezeknek az adatoknak
os.remove(r'Ide megadjuk annak a file-nak az útvonalát amely abban a mappában van ahol ez a program és a végére odatesszük hogy \elso.jpeg')
os.remove(r'ugyanazt az útvonalat adjuk meg itt mint az előzőnél, csak itt nem \elso.jpeg-t teszünk a végére, hanem azt hogy \masodik.jpeg')

szamr = 0
# Itt a try-on belül megnézzük hogy kitudunk e kérni adatokat az Image_data.db-ből , hogyha nem akkor a try- miatt átlép az except blokkba,ha viszont sikerül, akkor pedig eltároljuk az a változóban azt a képet byte- formában amire szükségünk van

try:
    conn = sqlite3.connect("Image_data.db")
    results = conn.execute("SELECT * FROM Image")
    elso = 0
    for asd in results:
        if elso == 0:
            a = asd
        szamr += 1
        elso += 1
# Ide akkor tér át a program, hogyha még nem volt sosem létrehozva Image_data.db adatbázis
except:
    # a mappánkban ebben az esetben kell lennie egy képnek arról a személyről aki majd fel tudja oldani az okostükröt és az ahhoz tartozó PATH-t kell megadni a pathtoimage változóba
    pathtoimage = r'megadjuk ide azt az útvonalat, ahol az a kép van akit majd feltud ismerni a tükör'
    create_database()
    # az insert image eljárás segítségével feltöltjük az arról a személyről szóló képet az adatbázisba, aki majd feltudja oldani az okostükröt
    insert_image(pathtoimage)
    # ezt követően,mivel az adatbázisunkban bennevan a kép az előbb említett személyről ezért kitöröljük a mappából ezt a képet
    os.remove(pathtoimage)

