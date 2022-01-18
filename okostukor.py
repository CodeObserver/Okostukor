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

   
# ide ebbe az elágazásba akkor lépünk csak bele, hogyha még sosem hoztuk létre az adatbázist a program lefuttatása előtt, mert akkor ugyanúgy az a változóban eltároljuk az első képet byte formátumban
if szamr == 0:
    conn = sqlite3.connect("Image_data.db")
    results = conn.execute("SELECT * FROM Image")
    elso = 0
    for asd in results:
        if elso == 0:
            a = asd
        elso += 1
# A fent említett személyről szóló kép bíte formáját kiolvastuk az a változóba, azonban ezt egyből még nem tudjuk felhasználni, mert szintaktikai probléma miatt, elöszőr lista formában kell beletenni egy másik változóba
conn.close()
# a 'b' változóba beletesszük a képet elöszőr számokká alakított formában ez egy lista amely számokat tartalmaz
b = list(a[0])
# a 'bytes' segítségével átkonvertáljuk ezt a listát byte formátumra
c = bytes(b)
# itt megadjuk azt az elérési utat ahova akarjuk tenni ideiglenesen arról a személyről való képet, aki majd feltudja oldani a tükröt
path = r'Ide kell megadni az elérési útvonalat a mappához, majd pedig megadjuk a kép nevét így a végére \kepneve.jpg'
fp = open(path, 'wb')
# ezzel pedig létrehozzuk a képet byte formában
fp.write(c)
fp.close()
# Annak az embernek képét olvassuk be aki felfogja tudni oldani a tükröt
image_of_me = face_recognition.load_image_file('ide adjuk meg annak a képnek a nevét és formátumát amit a 127. sorban adtunk meg pl kepneve.jpg')
# a ropter_face_encoding változóban eltároljuk az adott személy arcának aspektusait, amit majd a mesterséges intelligencia figyelni fog feloldáskor
ropter_face_encoding = face_recognition.face_encodings(image_of_me)[0]
# kitöröljük a mappából a személyről szóló képet, mert már nincs rá szükség
os.remove(path)
# a newsapi module-nak megadjuk a saját api key -ünket, amit ingyenesen tudunk kérni az oldalon
newsapi = NewsApiClient(api_key='ide kell megadni')
# ezzel megtudjuk adni, hogy milyen nyelvű híreket szolgáltasson nekünk ez az API, ha ezt így hagyjuk, akkor magyar híreket fogunk kapni
top_headlines = newsapi.get_top_headlines(country='hu')
a = sources = newsapi.get_sources(country='hu')
# ezzel az url-l magyar nyelvű híreket fogunk megkapni, az apikey= után kell megadni a saját api key-ünket
resp = 'https://newsapi.org/v2/top-headlines?country=hu&apiKey=ide adjuk meg az api keyünket'
# ezzel tulajdonképpen megszerezzük az előbb említett url-ről származó egész html-váz adatokat
r = requests.get(resp)
asdd = r.json()
# csak az articles-t szedjük ki az io változóba
io = asdd['articles']
# titlee változóba regular expressions segítségével megszerezzük az cikkekből származó fejléceket/címeket
titlee = re.findall(r'title\': \'(.*?)\'', str(asdd))
jo = []
hanyadik = 0
# idő (weather) api-hoz tartozó key-t kell megadnunk az api_key változóba
api_key = "ide"
# itt található egy alap url,amit később felhasználunk egy összetettebb url létrehozásához
base_url = "http://api.openweathermap.org/data/2.5/weather?"
# itt a city_name változóba megtudjuk adni, hogy melyik városról szeretnénk adatokat kapni időt illetőleg
city_name = "győr"
# itt hozzuk létre az összetettebb url-t
complete_url = base_url + "appid=" + api_key + "&lang=hu" + "&units=metric" + "&q=" + city_name
# Ugyanúgy mint az előzőnél itt is megkapjuk a html-vázat
response = requests.get(complete_url)
x = response.json()
# hogyha nem kapunk hibaüzenetet,akkor megtudjuk szerezni a különböző változókba az adatokat
if x["cod"] != "404":
    # az y változóban benne van minden adat amire szükségünk van ebből válogatjuk ki egyesével majd később
    y = x["main"]
    # ezzel megkapjuk a hőmérsékletet
    current_temperature = y["temp"]
    # a páratartalomhoz megfelelő adatot itt megkapjuk a current_humidity változóba
    current_humidity = y["humidity"]
    # itt egy rövid időjáráshoz tartozó leírást kapunk meg
    weather_description = z[0]["description"]
    # print following values
    temp = str(current_temperature)
    humidity = str(current_humidity)
    desc = str(weather_description)
    if len(temp) > 4:
        temp = (str(temp[0] + temp[1] + temp[2] + temp[3]))
else:
    print(" City Not Found ")

    

