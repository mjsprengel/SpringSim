try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import time
import math

animation = Tk()

canvas = Canvas(animation, width = 1000, height = 600, bg = "black")
canvas.pack()

r = [500,300]
v = [0,0]
a = [0,0]

s1 = [400,400]
s2 = [600,200]
length1 = 100
length2 = 100

k1 = .2
d1 = .02
k2 = .2
d2 = .02
m = 1
g=5

dt = 1/5000.0
refresh = 0

pressed = False
pressedA = False
pressedB = False
def pressed(event):
    global k1,d1,k2,d2,pressed,pressedA,pressedB
    xm, ym = event.x, event.y
    if (xm < r[0]+25) and (xm > r[0]-25) and (ym < r[1]+25) and (ym > r[1]-25):
        k1,d1,k2,d2 = 0,0,0,0
        v[0],v[1] = 0,0
        a[0],a[1] = 0,0
        pressed = True
    elif (xm < s2[0]+10) and (xm > s2[0]-10) and (ym < s2[1]+10) and (ym>s2[1]-10):
        pressedA = True
    elif xm < (s1[0]+10) and xm > (s1[0]-10) and ym < (s1[1]+10) and (ym>s1[1]-10):
        pressedB = True
        
def release(event):
    global k1,d1,k2,d2,pressed,pressedA,pressedB
    k1,d1,k2,d2 = .4,.02,.4,.02
    pressed = False
    pressedA = False
    pressedB = False
    
def drag(event):
    global a,v,r,s2,s1,g
    g = 0
    xm, ym = event.x, event.y
    if pressed == True:
        a[0],a[1] = 0,0
        v[0],v[1] = 0,0
        r[0],r[1] = xm,ym
    elif pressedA:
        s2 = [xm,ym]
    elif pressedB:
        s1 = [xm,ym]

canvas.bind("<Button-1>",pressed)
canvas.bind("<B1-Motion>",drag)
canvas.bind("<ButtonRelease-1>",release)


def global_reset():
    global r,v,a
    r = [500,300]
    v = [0,0]
    a = [0,0]

def calculate_motion():
    global a,v,r
    rMag1 = math.sqrt((r[0]-s1[0])**2 + (r[1]-s1[1])**2)
    rMag2 = math.sqrt((r[0]-s2[0])**2 + (r[1]-s2[1])**2)
    rHat1 = [(r[0]-s1[0])/rMag1, (r[1]-s1[1])/rMag1]
    rHat2 = [(r[0]-s2[0])/rMag2, (r[1]-s2[1])/rMag2]
    eq1 = [s1[0] + length1*rHat1[0], s1[1] + length1*rHat1[1]]
    eq2 = [s2[0] + length2*rHat2[0], s2[1] + length2*rHat2[1]]
    x1 = [r[0]-eq1[0], r[1]-eq1[1]]
    x2 = [r[0]-eq2[0], r[1]-eq2[1]]
    a = [((-k1*x1[0]-d1*v[0])/m)+((-k2*x2[0]-d2*v[0])/m), ((-k1*x1[1]-d1*v[1])/m)+((-k2*x2[1]-d2*v[1])/m)]
    v = [v[0] + a[0]*dt, v[1] + a[1]*dt]
    r = [r[0] + v[0]*dt, r[1] + v[1]*dt]

def speedtest():
    global r,v,a,x,refresh,dt
    i=0
    t1 = time.time()
    while True:
        i+=1
        calculate_motion()
        if i%40000 == 0:
            t2 = time.time()
            iters_per_second = int(40000/(t2-t1))
            refresh = int(iters_per_second/120)
            dt = 1.0/(refresh*10)
            global_reset()
            print(iters_per_second, "position calculations per second")
            print(refresh, "calculation cycles per screen update")
            print(iters_per_second/refresh, "fps")
            break

def update_screen():
    canvas.delete("mass","spring1","spring2","s2","s1")
    canvas.create_oval(r[0]-15, r[1]-15, r[0]+15, r[1]+15, fill="blue",tags="mass")
    canvas.create_line(s1[0],s1[1],r[0],r[1],fill="white",tags="spring1")
    canvas.create_line(s2[0],s2[1],r[0],r[1],fill="white",tags="spring2")
    canvas.create_oval(s2[0]-10, s2[1]-10, s2[0]+10, s2[1]+10, fill="red",tags="s2")
    canvas.create_oval(s1[0]-10, s1[1]-10, s1[0]+10, s1[1]+10, fill="red",tags="s1")
    animation.update()

speedtest()

i = 0
while True:
    i+=1
    calculate_motion()
    if i%refresh == 0:
        update_screen()
        i=0
