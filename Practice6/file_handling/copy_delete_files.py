with open("/Users/gulmarzantaben/tasks/Practice6/file_handling/lyrics.txt", "a") as f:
    f.write("But nothing better than songs by Kairat Nurtas.\n")

with open("/Users/gulmarzantaben/tasks/Practice6/file_handling/lyrics.txt", "r") as f:
    content = f.read()
    print(content)

import shutil

shutil.copy("lyrics.txt","copylyr.txt")

import os

if os.path.exists("copylyr.txt"):
    os.remove("copylyr.txt")
