import os
import random
import sys
import pygame

from persistence import load_settings, save_settings
from persistence import load_leaderboard, add_score

from racer import RacerGame, WIDTH, HEIGHT
from ui import Button, draw_center_text

pygame.init()
pygame.mixer.init()

screen=pygame.display.set_mode(
(WIDTH,HEIGHT)
)

pygame.display.set_caption(
"ILLIT Sky Racer"
)

clock=pygame.time.Clock()

TITLE=pygame.font.SysFont(
"arial",
48,
bold=True
)

FONT=pygame.font.SysFont(
"arial",
28
)

SMALL=pygame.font.SysFont(
"arial",
22
)

SKY=(225,244,255)
BABY_BLUE=(175,223,255)
ICE=(210,240,255)
DEEP=(50,80,120)
WHITE=(255,255,255)


MUSIC_END=pygame.USEREVENT+1
pygame.mixer.music.set_endevent(
MUSIC_END
)

MUSIC=[
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/Cherish (My Love) (Instrumental) - ILLIT (128).mp3",
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/Billyeoon_Goyangi_Do_the_Dance_Instrumental_ILLIT_128.mp3",
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/NOT CUTE ANYMORE (Instrumental) - ILLIT (128).mp3"
]


def songs():
    return[
    s for s in MUSIC
    if os.path.exists(s)
]


def play_song():

    music=songs()

    if not music:
        return

    s=random.choice(music)

    pygame.mixer.music.load(s)
    pygame.mixer.music.set_volume(.55)
    pygame.mixer.music.play()


def music_state(settings):

    if settings["sound"]:
        if not pygame.mixer.music.get_busy():
            play_song()
    else:
        pygame.mixer.music.stop()


def ensure_assets():

    required=[
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/Enemyy.png",
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/coinn.png",
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/shield.png",
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/heal.png",
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/boost.png",
"/Users/gulmarzantaben/Desktop/TSIS/TSIS3/assets/oil.png"
]

    for f in required:
        if not os.path.exists(f):
            print("Missing:",f)
            pygame.quit()
            sys.exit()


def cute_bg():
    screen.fill(SKY)


def main():

    ensure_assets()

    settings=load_settings()
    leaderboard=load_leaderboard()

    music_state(settings)

    state="menu"
    username=""
    result=None

    difficulties=[
"easy",
"normal",
"hard"
]

    colors=[
"red",
"blue",
"green",
"yellow"
]

    while True:

        clock.tick(60)

        if state=="menu":

            play=Button(110,240,200,55,"Play")
            lb=Button(110,315,200,55,"Leaderboard")
            sett=Button(110,390,200,55,"Settings")
            quitb=Button(110,465,200,55,"Quit")

            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type==MUSIC_END:
                    if settings["sound"]:
                        play_song()

                if play.is_clicked(event):
                    state="name"

                elif lb.is_clicked(event):
                    leaderboard=load_leaderboard()
                    state="leaderboard"

                elif sett.is_clicked(event):
                    state="settings"

                elif quitb.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            cute_bg()

            draw_center_text(
screen,
"ILLIT SKY RACER",
TITLE,
DEEP,
120
)

            draw_center_text(
screen,
"blue dreamy arcade edition",
SMALL,
DEEP,
170
)

            play.draw(screen,FONT)
            lb.draw(screen,FONT)
            sett.draw(screen,FONT)
            quitb.draw(screen,FONT)

            pygame.display.flip()


        elif state=="name":

            start=Button(100,420,220,55,"Start Race")
            back=Button(100,490,220,55,"Back")

            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type==MUSIC_END:
                    if settings["sound"]:
                        play_song()

                if event.type==pygame.KEYDOWN:

                    if event.key==pygame.K_BACKSPACE:
                        username=username[:-1]

                    elif(
event.key==pygame.K_RETURN
and username.strip()
):
                        game=RacerGame(
screen,
settings,
username
)
                        result=game.run()

                        if result.get("quit"):
                            pygame.quit()
                            sys.exit()

                        add_score(result)
                        state="gameover"

                    elif(
event.unicode.isprintable()
and len(username)<15
):
                        username+=event.unicode

                if(
start.is_clicked(event)
and username.strip()
):
                    game=RacerGame(
screen,
settings,
username
)

                    result=game.run()
                    add_score(result)
                    state="gameover"

                if back.is_clicked(event):
                    state="menu"

            cute_bg()

            draw_center_text(
screen,
"Enter Username",
FONT,
DEEP,
220
)

            box=pygame.Rect(
85,280,
250,55
)

            pygame.draw.rect(
screen,
WHITE,
box,
border_radius=12
)

            pygame.draw.rect(
screen,
BABY_BLUE,
box,
4,
border_radius=12
)

            txt=FONT.render(
username+"|",
True,
DEEP
)

            screen.blit(
txt,
(110,295)
)

            start.draw(screen,FONT)
            back.draw(screen,FONT)

            pygame.display.flip()


        elif state=="settings":

            sound=Button(80,240,260,50,f"Sound {settings['sound']}")
            diff=Button(80,310,260,50,f"Difficulty {settings['difficulty']}")
            color=Button(80,380,260,50,f"Car {settings['car_color']}")
            back=Button(80,470,260,50,"Back")

            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if sound.is_clicked(event):
                    settings["sound"]=not settings["sound"]
                    save_settings(settings)
                    music_state(settings)

                elif diff.is_clicked(event):
                    i=difficulties.index(settings["difficulty"])
                    settings["difficulty"]=difficulties[(i+1)%3]
                    save_settings(settings)

                elif color.is_clicked(event):
                    i=colors.index(settings["car_color"])
                    settings["car_color"]=colors[(i+1)%4]
                    save_settings(settings)

                elif back.is_clicked(event):
                    state="menu"

            cute_bg()

            draw_center_text(
screen,
"SETTINGS",
TITLE,
DEEP,
150
)

            sound.draw(screen,FONT)
            diff.draw(screen,FONT)
            color.draw(screen,FONT)
            back.draw(screen,FONT)

            pygame.display.flip()


        elif state=="leaderboard":

            back=Button(125,590,170,50,"Back")

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if back.is_clicked(event):
                    state="menu"

            cute_bg()

            draw_center_text(
screen,
"TOP 10",
TITLE,
DEEP,
80
)

            y=150

            if not leaderboard:
                draw_center_text(
screen,
"No Scores Yet",
FONT,
DEEP,
250
)
            else:
                for i,row in enumerate(leaderboard[:10],1):
                    txt=f"{i}. {row['username']} {row['score']}"
                    t=SMALL.render(txt,True,DEEP)
                    screen.blit(t,(60,y))
                    y+=42

            back.draw(screen,FONT)
            pygame.display.flip()


        elif state=="gameover":

            retry=Button(90,500,240,55,"Retry")
            menu=Button(90,570,240,55,"Menu")

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if retry.is_clicked(event):
                    game=RacerGame(screen,settings,username)
                    result=game.run()
                    add_score(result)

                if menu.is_clicked(event):
                    state="menu"

            cute_bg()

            title="YOU WON <3" if result["status"]=="finished" else "GAME OVER"

            draw_center_text(
screen,
title,
TITLE,
DEEP,
130
)

            stats=[
f"Score {result['score']}",
f"Coins {result['coins']}",
f"Distance {result['distance']}"
]

            y=250
            for s in stats:
                draw_center_text(screen,s,FONT,DEEP,y)
                y+=55

            retry.draw(screen,FONT)
            menu.draw(screen,FONT)
            pygame.display.flip()


if __name__=="__main__":
    main()
