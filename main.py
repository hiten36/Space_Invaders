import pygame
import os
import random
import math

# Initialising Pygame
pygame.init()
pygame.mixer.init()
# size
screenwidth=1200
screenheight=600
# configuring display
gamewindow=pygame.display.set_mode((screenwidth,screenheight))
# Images and backgrounds
bg1=pygame.image.load('sp.png')
bg1=pygame.transform.scale(bg1,(screenwidth,screenheight)).convert_alpha()
bg2=pygame.image.load('back.jpg')
bg2=pygame.transform.scale(bg2,(screenwidth,screenheight)).convert_alpha()
admin=pygame.image.load('3.jpg')
admin=pygame.transform.scale(admin,(250,250)).convert_alpha()
bullet=pygame.image.load('bullet.png')
bullet=pygame.transform.scale(bullet,(20,40)).convert_alpha()
monster=pygame.image.load('monster.png')
rocket=pygame.image.load('rocket.png')
rocket=pygame.transform.scale(rocket,(170,70)).convert_alpha()
# Font
font1=pygame.font.SysFont('font1.ttf',55)
font2=pygame.font.SysFont('font2.ttf',100)
# updating display
pygame.display.set_caption("Space Invaders")
pygame.display.update()
clock=pygame.time.Clock()
# Values
exit_game=False
game_over=False
bullet_state='ready'
monster_n=[]
# Player
def player(player_x,player_y):
    gamewindow.blit(rocket,(player_x,player_y))
# monster
def monster1(i,monster_x,monster_y):
    gamewindow.blit(monster_n[i],(monster_x,monster_y))
# bullet
def bullet1(bullet_x,bullet_y):
    global bullet_state
    bullet_state='fire'
    gamewindow.blit(bullet,(bullet_x+75,bullet_y+10))
# colloid
def iscolloid(monster_x,monster_y,bullet_x,bullet_y):
    offset=math.sqrt(((bullet_x-monster_x)*(bullet_x-monster_x))+((bullet_y-monster_y)*(bullet_y-monster_y)))
    if offset<50:
        return True
    else:
        False
# displaying text1
def sctext1(text,color,x,y):
    sc_font1=font1.render(text,True,color)
    gamewindow.blit(sc_font1,(x,y))
# displaying text2
def sctext2(text,color,x,y):
    sc_font2=font2.render(text,True,color)
    gamewindow.blit(sc_font2,(x,y))
# initial game window
def welcome():
    global exit_game
    while not exit_game:
        gamewindow.blit(bg1,(0,0))
        gamewindow.blit(admin,(870,20))
        sctext1("Press Spacebar to play",(0,0,255),120,220)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    gameloop()
        pygame.display.update()
        clock.tick(30)
# Music
pygame.mixer.music.load('song.mp3')
pygame.mixer.music.play(-1)
# Main Game
def gameloop():
    global exit_game
    global game_over
    global bullet_state
    game_over=False
    if(not os.path.exists("high.txt")):
        with open('high.txt','w') as f:
            f.write('0')
            f.close()
    with open('high.txt') as f:
        high_score=f.read()
        f.close()
    player_x=520
    player_y=530
    player_v=0
    monster_x=[]
    monster_y=[]
    monster_v=[]
    monster_v1=[]
    num_m=6
    for i in range(num_m):
        monster_n.append(pygame.transform.scale(monster,(110,50)).convert_alpha())
        monster_x.append(random.randint(20,1000))
        monster_y.append(30)
        monster_v.append(10)
        monster_v1.append(60)
    bullet_x=0
    bullet_y=530
    bullet_v=18
    score=0
    fps=30
    while not exit_game:
        gamewindow.blit(bg2,(0,0))
        if game_over:
            with open('high.txt','w') as f:
                f.write(str(high_score))
                f.close()
            sctext2("GAME OVER!",(255,0,0),370,100)
            sctext2(f'score: {score}',(255,0,0),450,200)
            sctext2('Press Enter to continue',(255,0,0),270,300)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        player_v=14
                    if event.key==pygame.K_LEFT:
                        player_v=-14
                    if event.key==pygame.K_SPACE:
                        if bullet_state is 'ready':
                            pygame.mixer.Sound('shoot.wav').play()
                            bullet_x=player_x
                            bullet1(bullet_x,bullet_y)
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                        player_v=0
            player_x+=player_v
            if player_x<-30:
                player_x=-30
            if player_x>1060:
                player_x=1060
            for i in range(num_m):
                if monster_y[i]>480:
                    for j in range(num_m):
                        monster_y[j]=2000
                    game_over=True
                monster_x[i]+=monster_v[i]
                if monster_x[i]>1060:
                    monster_v[i]=-10
                    monster_y[i]+=monster_v1[i]
                if monster_x[i]<-10:
                    monster_v[i]=10
                    monster_y[i]+=monster_v1[i]
                colloid=iscolloid(monster_x[i],monster_y[i],bullet_x,bullet_y)
                if colloid:
                    pygame.mixer.Sound('kill.wav').play()
                    score+=1
                    if score>int(high_score):
                        high_score=score
                    monster_x[i]=random.randint(20,1000)
                    monster_y[i]=30
                    bullet_y=530
                    bullet_state='ready'
                monster1(i,monster_x[i],monster_y[i])
            if bullet_y<0:
                bullet_y=530
                bullet_state='ready'
            if bullet_state=='fire':
                bullet1(bullet_x,bullet_y)
                bullet_y-=bullet_v
            sctext1(f'Score: {score}     High Score: {high_score}',(0,255,0),5,5)
            player(player_x,player_y)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    exit()
welcome()