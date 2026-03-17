import shutil
import os

with open("/Users/gulmarzantaben/tasks/Practice6/file_handling/lyrics.txt", "a") as f:
    f.write("\nBut nothing better than songs by Kairat Nurtas.\n")

with open("/Users/gulmarzantaben/tasks/Practice6/file_handling/lyrics.txt", "r") as f:
    content = f.read()
    print(content)

shutil.copy("/Users/gulmarzantaben/tasks/Practice6/file_handling/lyrics.txt", "/Users/gulmarzantaben/tasks/Practice6/file_handling/copylyr.txt")

if os.path.exists("/Users/gulmarzantaben/tasks/Practice6/file_handling/copylyr.txt"):
    os.remove("/Users/gulmarzantaben/tasks/Practice6/file_handling/copylyr.txt")
