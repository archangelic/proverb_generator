#!/usr/bin/env python3
import shlex
import urllib.request

from configobj import ConfigObj
from imgurpython import ImgurClient
from subprocess import call

# conf conf conf conf
config = ConfigObj("config.conf")

client_id = conf['client_id']
client_secret = conf['client_secret']
client = ImgurClient(client_id, client_secret)

def create_image(quote, pic_name, width, height):
    width = str(width)
    height = str(height)
    # I haven't found a good module for image processing, so you gotta use some command line tool, bro.
    cmd = '''convert -background none -gravity center -font Helvetica \
-fill white -stroke black -strokewidth 2 -size %sx%s \
caption:"%s" \
%s +swap -gravity center -composite imgur.jpg''' % (width, height, quote, pic_name)
    call(shlex.split(cmd))

url = input("Image URL: ")
quote = input("Image Text: ")
print("By default, this thing uses 1920x1080 images with a safety of 200px.")
safe_override = input("Do you want to override? [y/N]: ")
if safe_override.lower() == "y":
    w = int(input("Width: "))
    h = int(input("Height: "))
    # FLY INTO THE SAFETY ZONE
    safety = (int(input("Safe Zone: "))*2)
else:
    w = 1920
    h = 1080
    # safety for a 200px border is 400px because math
    safety = 400

urllib.request.urlretrieve(url, "wallpaper.jpg")
create_image(quote, "wallpaper.jpg", w-safety, h-safety)

img = client.upload_from_path("imgur.jpg")
print("Image uploaded.")
print(img['link'])
print("Delete Link: ", "http://imgur.com/delete/" + img['deletehash'])
