from turtle import *
import os
from math import sqrt
from random import randint
import time

#Screen
window=Screen()
window.title("Space Invaders")
window.bgcolor("black")
window.bgpic("ScreenshotStarfield.png")
register_shape("invader.gif")
register_shape("player.gif")


#Player
player=Turtle()
player.speed(0)
player.penup()
player.color("blue")
player.setpos(0,-250)
player.shape("player.gif")
player.setheading(90)
playerspeed=15

#Ennemy
nb_ennemy=8
ennemies=[]
for i in range(nb_ennemy):
    ennemies.append(Turtle())

for ennemy in ennemies:
    ennemy.speed(0)
    ennemy.color("red")
    ennemy.shape("invader.gif")
    ennemy.penup()
    x_ennemy_spawn=randint(-200,200)
    y_ennemy_spawn=randint(100,250)
    ennemy.setpos(x_ennemy_spawn,y_ennemy_spawn)

ennemy_speed=6

#Bullet
bullet=Turtle()
bullet.hideturtle()
bullet.color("yellow")
bullet.penup()
bullet.speed(0)
bullet.shape("triangle")
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.setpos(player.xcor(),player.ycor())
bullet_state=0
bulletspeed=25

#X and Y size window
xwindow=window.screensize()[0]
ywindow=window.screensize()[1]

#Border
border=Turtle()
border.hideturtle()
border.color("white")
border.speed(0)
border.penup()
border.setpos(-xwindow,-ywindow)
border.pendown()
xw=xwindow*2
yw=ywindow*2
for carre in range(5):
    if carre==4:
        border.fd(50)
    else:
        if carre%2 !=0:
            border.fd(yw)
        else:
            if carre ==2:
                border.fd(xw+100)
            elif carre == 0:
                border.fd(xw+50)
        border.left(90)

#Move left and right
def move_left():
    x=player.xcor()-playerspeed
    if x < -xwindow:
        x=-xwindow
    player.setx(x)

def move_right():
    x=player.xcor()+playerspeed
    if x > xwindow:
        x=xwindow
    player.setx(x)

def start_repeat(func):
    func()

def stop_repeat():
    return

#Shot bullet
def shot():
    global bullet_state
    if bullet_state == 0:
        bullet_state=1
        x=player.xcor()
        y=player.ycor()+10
        bullet.setpos(x,y)
        bullet.showturtle()
    else: pass

#Check hit
def is_hit(t1,t2):
    distance=sqrt((t2.xcor()-t1.xcor())**2+(t2.ycor()-t1.ycor())**2)
    if distance < 15:
        return True
    return False

#Score
score=0
score_write=Turtle()
score_write.hideturtle()
score_write.speed(0)
score_write.color("white")
score_write.penup()
score_write.setpos(-xwindow-40,ywindow-30)
score_str="Score: {}".format(score)
score_write.write(score_str,False,align="left",font=("Arial",14,"italic"))

#Title
space_title=Turtle()
space_title.hideturtle()
space_title.speed(0)
space_title.color("blue")
space_title.penup()
space_title.setpos(0,ywindow+30)
space_str="SPACE INVADERS"
space_title.write(space_str,False,align="center",font=("Arial",24,"bold"))

#Check event on key
window.listen()
window.onkeypress(lambda: start_repeat(move_left), 'Left')
window.onkeyrelease(stop_repeat, 'Left')
window.onkeypress(lambda: start_repeat(move_right), 'Right')
window.onkeyrelease(stop_repeat, 'Left')
window.onkeypress(shot,"space")

#Game
if __name__=="__main__":
    while True:
        #Player pos
        x_player=player.xcor()
        y_player=player.ycor()
        #Move ennemy
        for ennemy in ennemies:
            x_ennemy=ennemy.xcor()
            x_ennemy+=ennemy_speed
            ennemy.setx(x_ennemy)
            if x_ennemy > xwindow:
                ennemy_speed*=-1
                for e in ennemies:
                    y_ennemy=e.ycor()
                    y_ennemy-=30
                    if y_ennemy <= y_player:
                        game_over=Turtle()
                        game_over.hideturtle()
                        game_over.color("white")
                        game_over.speed(0)
                        game_over.setpos(0,0)
                        game_over.write("GAME OVER",False, align="center",font=("Arial",28,"bold"))
                        time.sleep(3)
                        bye();exit()
                    e.sety(y_ennemy)

            if x_ennemy < -xwindow:
                ennemy_speed*=-1
                for e in ennemies:
                    y_ennemy=e.ycor()
                    y_ennemy-=30
                    e.sety(y_ennemy)

            #Check if the ennemy is hit
            if is_hit(bullet,ennemy):
                bullet.hideturtle()
                bullet_state=0
                ennemy.setpos(randint(-200,200),randint(100,250))
                score+=10
                score_str="Score: {}".format(score)
                score_write.clear()
                score_write.write(score_str,False,align="left",font=("Arial",14,"italic"))

            #Check if the player is hit
            if is_hit(player,ennemy):
                player.reset()
                ennemy.reset()
                print("Game Over");break;
        #Move bullet
        if bullet_state==0:
            x_bullet=player.xcor()
            y_bullet=player.ycor()
            bullet.setx(x_bullet)
            bullet.sety(y_bullet)
        else:
            y_bullet=bullet.ycor()
            y_bullet+=bulletspeed
            bullet.sety(y_bullet)

        if y_bullet > ywindow-50:
            bullet.hideturtle()
            bullet.setpos(x_player,y_player)
            bullet_state=0
