with open("lyrics.txt","a") as f:
    f.write("But nothing better than songs by Kairat Nurtas.\n")

with open("lyrics.txt","r") as f:
    f.read()

import shutil

shutil.copy("lyrics.txt","copylyr.txt")

import os

if os.path.exists("copylyr.txt"):
    os.remove("copylyr.txt")
