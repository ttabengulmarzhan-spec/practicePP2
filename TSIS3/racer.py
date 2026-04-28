import pygame
import random
from datetime import datetime

WIDTH=420
HEIGHT=700

ROAD_X=60
ROAD_W=300
LANES=3
LANE_W=ROAD_W//LANES


BG=(224,244,255)
ROAD=(242,247,255)
LANE=(255,255,255)
HUD=(30,60,110)

PLAYER_BLUE=(100,180,255)
PLAYER_LIGHT=(180,230,255)
WHEEL=(50,60,80)

DIFF={
"easy":{"speed":200,"finish":3000,"traffic_ms":1900,"obstacle_ms":2400},
"normal":{"speed":240,"finish":4200,"traffic_ms":1500,"obstacle_ms":1900},
"hard":{"speed":290,"finish":5200,"traffic_ms":1100,"obstacle_ms":1500}
}

CAR_COLORS = {
    "red": ((220, 80, 80), (255, 160, 160)),
    "blue": ((100, 180, 255), (180, 230, 255)),
    "green": ((80, 220, 140), (160, 255, 200)),
    "yellow": ((240, 220, 80), (255, 250, 160)),
}

def lane_x(l):
    return ROAD_X+l*LANE_W+LANE_W//2


def img(path,size):
    i=pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(i,size)


class RacerGame:

    def __init__(self,screen,settings,username):

        self.screen=screen
        self.settings=settings
        self.username=username
        

        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("arial",19)

        d=DIFF[settings["difficulty"]]

        self.base_speed=d["speed"]
        self.finish=d["finish"]
        self.traffic_interval=d["traffic_ms"]
        self.obs_interval=d["obstacle_ms"]

        self.distance=0
        self.score=0
        self.coins=0

        self.player_lane=1
        self.player_y=590

        self.running=True
        self.result_status="game_over"

        self.road_offset=0

        self.active_power=None
        self.power_until=0
        self.shield=False

        self.slow_until=0
        self.speed_mult=1

        self.player_w=56
        self.player_h=92

        self.car_color = settings["car_color"]

        self.enemy=img(
"/Users/gulmarzantaben/Desktop/practicePP2/TSIS3/assets/Enemyy.png",
(55,88)
)

        self.coin=img(
"/Users/gulmarzantaben/Desktop/practicePP2/TSIS3/assets/coinn.png",
(34,34)
)

        self.shield_img=img(
"/Users/gulmarzantaben/Desktop/practicePP2/TSIS3/assets/shield.png",
(36,36)
)

        self.heal_img=img(
"/Users/gulmarzantaben/Desktop/practicePP2/TSIS3/assets/heal.png",
(36,36)
)

        self.boost_img=img(
"/Users/gulmarzantaben/Desktop/practicePP2/TSIS3/assets/boost.png",
(36,36)
)

        self.oil_img=img(
"/Users/gulmarzantaben/Desktop/practicePP2/TSIS3/assets/oil.png",
(42,28)
)

        self.traffic=[]
        self.obstacles=[]
        self.coin_list=[]
        self.powerups=[]

        self.last_traffic=0
        self.last_obs=0
        self.last_coin=0
        self.last_power=0


    def player_rect(self):
        r=pygame.Rect(0,0,self.player_w,self.player_h)
        r.center=(lane_x(self.player_lane),self.player_y)
        return r


    def draw_player(self):

        car=self.player_rect()
        
        base, light = CAR_COLORS[self.car_color]

        pygame.draw.rect(
            self.screen,
            base,
            car,
            border_radius=18
        )

        top=pygame.Rect(
            car.x+10,
            car.y+14,
            car.w-20,
            26
        )

        pygame.draw.rect(
            self.screen,
            light,
            top,
            border_radius=10
        )

        for y in [car.y+18,car.y+60]:
            pygame.draw.circle(self.screen,WHEEL,(car.x+6,y),7)
            pygame.draw.circle(self.screen,WHEEL,(car.right-6,y),7)

        pygame.draw.circle(
            self.screen,
            (255,255,220),
            (car.centerx-10,car.y+10),
            4
        )

        pygame.draw.circle(
            self.screen,
            (255,255,220),
            (car.centerx+10,car.y+10),
            4
        )

        if self.shield:
            pygame.draw.circle(
                self.screen,
                (150,220,255),
                car.center,
                44,
                4
            )


    def current_speed(self):
        now=pygame.time.get_ticks()
        mult=self.speed_mult
        if now<self.slow_until:
            mult*=0.7
        return self.base_speed*mult


    def activate(self,t):

        if self.active_power:
            return

        now=pygame.time.get_ticks()

        if t=="nitro":
            self.active_power="nitro"
            self.power_until=now+4000
            self.speed_mult=1.6

        if t=="shield":
            self.active_power="shield"
            self.shield=True

        if t=="repair":
            self.active_power="repair"
            self.coins+=5


    def clear_power(self):
        self.active_power=None
        self.shield=False
        self.speed_mult=1


    def safe_lane(self):
        lanes=[0,1,2]
        lanes.remove(self.player_lane)
        return random.choice(lanes)


    def spawn_traffic(self):
        if len(self.traffic)>=2:
            return
        r=self.enemy.get_rect()
        lane=self.safe_lane()
        r.centerx=lane_x(lane)
        r.y=-100
        self.traffic.append(r)


    def spawn_obstacle(self):
        if len(self.obstacles)>=2:
            return

        lane=self.safe_lane()
        r=self.oil_img.get_rect()
        r.centerx=lane_x(lane)
        r.y=-60

        kind=random.choice(["oil","bump"])

        self.obstacles.append({
            "rect":r,
            "type":kind
        })


    def spawn_coin(self):
        r=self.coin.get_rect()
        r.centerx=lane_x(random.randint(0,2))
        r.y=-40
        self.coin_list.append(r)


    def spawn_power(self):

        kind=random.choice([
"nitro","shield","repair"
])

        r=pygame.Rect(0,0,36,36)
        r.centerx=lane_x(random.randint(0,2))
        r.y=-40

        self.powerups.append(
        {
"type":kind,
"rect":r,
"born":pygame.time.get_ticks()
}
)


    def update(self,dt):

        now=pygame.time.get_ticks()

        if self.active_power=="nitro" and now>self.power_until:
            self.clear_power()

        keys=pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.player_lane=max(0,self.player_lane-1)

        if keys[pygame.K_RIGHT]:
            self.player_lane=min(2,self.player_lane+1)

        if now-self.last_traffic>self.traffic_interval:
            self.spawn_traffic()
            self.last_traffic=now

        if now-self.last_obs>self.obs_interval:
            self.spawn_obstacle()
            self.last_obs=now

        if now-self.last_coin>900:
            self.spawn_coin()
            self.last_coin=now

        if now-self.last_power>6500:
            self.spawn_power()
            self.last_power=now

        speed=self.current_speed()

        self.distance+=speed*dt/17

        self.road_offset=(
self.road_offset+
speed*dt*.45
)%60

        p=self.player_rect()

        for t in self.traffic:
            t.y+=speed*dt

        for o in self.obstacles:
            o["rect"].y+=speed*dt

        for c in self.coin_list:
            c.y+=speed*dt

        for pwr in self.powerups:
            pwr["rect"].y+=speed*dt

        self.traffic=[t for t in self.traffic if t.y<HEIGHT]
        self.obstacles=[o for o in self.obstacles if o["rect"].y<HEIGHT]

        for c in list(self.coin_list):
            if p.colliderect(c):
                self.coins+=random.choice([1,2,3])
                self.coin_list.remove(c)

        for pwr in list(self.powerups):
            if p.colliderect(pwr["rect"]):
                self.activate(pwr["type"])
                self.powerups.remove(pwr)

        for t in self.traffic:
            if p.colliderect(t):
                if self.shield:
                    self.clear_power()
                    t.y=900
                else:
                    self.running=False

        for o in list(self.obstacles):
            if p.colliderect(o["rect"]):

                if o["type"]=="oil":
                    self.player_lane=max(
0,
min(
2,
self.player_lane+random.choice([-1,1])
)
)
                else:
                    self.slow_until=now+1200

                self.obstacles.remove(o)

        self.score=int(self.coins*15+self.distance)

        if self.distance>=self.finish:
            self.running=False
            self.result_status="finished"


    def draw(self):

        self.screen.fill(BG)

        pygame.draw.rect(
self.screen,
ROAD,
(ROAD_X,0,ROAD_W,HEIGHT)
)

        for i in range(1,3):
            x=ROAD_X+i*LANE_W
            y=-60+int(self.road_offset)

            while y<HEIGHT:
                pygame.draw.line(
self.screen,
LANE,
(x,y),
(x,y+35),
5
)
                y+=60

        for c in self.coin_list:
            self.screen.blit(self.coin,c)

        for o in self.obstacles:
            self.screen.blit(self.oil_img,o["rect"])

        for t in self.traffic:
            self.screen.blit(self.enemy,t)

        for pwr in self.powerups:

            if pwr["type"]=="nitro":
                self.screen.blit(self.boost_img,pwr["rect"])
            elif pwr["type"]=="shield":
                self.screen.blit(self.shield_img,pwr["rect"])
            else:
                self.screen.blit(self.heal_img,pwr["rect"])

        # DRAWN PLAYER
        self.draw_player()

        power="None"

        if self.active_power=="nitro":
            left=max(
0,
(self.power_until-pygame.time.get_ticks())/1000
)
            power=f"Nitro {left:.1f}s"

        elif self.active_power=="shield":
            power="Shield"

        elif self.active_power=="repair":
            power="Repair"

        hud=[
f"{self.username}",
f"Coins {self.coins}",
f"Score {self.score}",
f"Dist {int(self.distance)}",
f"Power {power}"
]

        for i,h in enumerate(hud):
            self.screen.blit(
                self.font.render(h,True,HUD),
                (12,12+i*24)
            )

        pygame.display.flip()


    def run(self):

        while self.running:

            dt=self.clock.tick(60)/1000

            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    return {"quit":True}

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        self.running=False

            self.update(dt)
            self.draw()

        return {
"quit":False,
"status":self.result_status,
"username":self.username,
"score":self.score,
"coins":self.coins,
"distance":int(self.distance),
"date":datetime.now().strftime(
"%Y-%m-%d %H:%M:%S"
)
}

