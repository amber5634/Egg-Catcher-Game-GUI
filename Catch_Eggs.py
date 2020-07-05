# import the necessary libraries
from itertools import cycle
from random import randrange
from tkinter import *
from tkinter import  Canvas, messagebox

# Define the canvas weigth and height

canvas_width=800
canvas_height=600

# Defininig a window

win=Tk()
# Creating a Canvas
c= Canvas(win, width=canvas_width, height=canvas_height, background='OliveDrab2')

# Creating a rectangle at the bottom of the canvas where the eggs will be catched
c.create_rectangle(-10,canvas_height-100,canvas_width+10,canvas_height+10, fill='deep sky blue')

# creating an oval shape topmost left where score will be displayed
c.create_oval(-100,-100,150,150,fill='orange', width=0)

#creating your own color cycle where the color of the egg will be choosen
color_cycle=cycle(['red', 'blue', 'yellow', 'black', 'light pink', 'green', 'purple','violet'])

egg_width=45
egg_height=55

#Score for eggs with an increment of 1

egg_score=1

#Defining speed, interval, difficulty of the game module
egg_speed=400
egg_interval=5000
difficulty_factor=0.95

#defining dimensions and color for egg catcher
catcher_color='dark blue'
catcher_width=110
catcher_height=110
catcher_start_x=canvas_width/ 2 - catcher_width/ 2
catcher_start_y=canvas_height - catcher_height -30
catcher_end_x=catcher_start_x + catcher_width
catcher_end_y=catcher_start_y + catcher_width

catcher=c.create_arc(catcher_start_x,catcher_start_y,catcher_end_x,catcher_end_y, start=200,extent=150,style='arc', outline=catcher_color,width=10)

#Defining Score Section
score=0
#nw stands for north west where score will be shown
score_text=c.create_text(10,10,anchor='nw',font=('Vedante',20,'bold'),fill='white',text='Score :'+str(score))

#defining lives remaining with an initial value of 3
lives_remaining=3
lives_test=c.create_text(canvas_width-10,10,anchor='ne',font=('Vedante',20,'bold'),fill='red',text='Lives :'+str(lives_remaining))

#defining a function for egg
eggs=[] #empty list

#Creation of eggs
def create_eggs():
    x=randrange(10,740)
    y=40
    new_egg=c.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle),width=0)  #x and y is added to egg width and height to avoid half egg/incomplete eggs falling at the end
    eggs.append(new_egg)
    win.after(egg_interval,create_eggs)
#Motion for eggs
def move_eggs():
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2)=c.coords(egg)
        c.move(egg,0,10)
        if egg_y2>canvas_height:
            egg_dropped(egg)
    win.after(egg_speed,move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining==0:
        messagebox.showinfo('Game Over:','Final Score:'+str(score))
        win.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_test, text='Lives: '+ str(lives_remaining))

def catch_check():
    (catcher_x,catcher_y,catcher_x2,catcher_y2)=c.coords(catcher)
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2)=c.coords(egg)
        if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2 < 45:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    win.after(100,catch_check)

def increase_score(points):
    global score , egg_speed , egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text , text='Score :'+ str(score))

def move_left(event):
    (x1,y1,x2,y2)=c.coords(catcher)
    if x1 > 0 :
        c.move(catcher,-20,0)

def move_right(event):
    (x1,y1,x2,y2)=c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher,20,0)

c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)


c.pack()

win.mainloop()
