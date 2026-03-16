with open("lyrics.txt","r") as f:
    start = f.readline()
    print(start)
    intro = f.readline()
    print(intro)
    lyric = f.read()
    print(lyric)
