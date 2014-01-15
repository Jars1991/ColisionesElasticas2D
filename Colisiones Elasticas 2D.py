"""
Programa principal que simula las colisiones elasticas frontales y oblicuas en 2D,
donde el segundo cuerpo se encuentra en reposo.

Created by: Jassael Ruiz
Version: 1.0
"""

# librerias a usar
import sys
sys.path.append('..')
import simplegui as sg
from stopwatch import stopwatch
import math

# global variables
width = 600
height = 500
conv = 30 # 1m - 30 px
velocidad = 10 # m/s, 300px - 1s
div = 100
vi2 = 0
velx = (velocidad * conv) / div
vely = 0 
velx2 = 0
vely2 = 0
ball_radius = 20
ball2_radius = 20
ball2_pos = [width / 2, height / 2]
ball2_vel = [velx2, vely2]
ball1_pos = [ball_radius * 2, height / 2 - ball_radius]
ball1_vel = [velx, vely]
dist = 0.1
start = False
mover = False
collision = False
cy = ball1_pos[1]
cy2 = ball2_pos[1]
vfa = 0
vfr = 0
ang1 = 0
choque = [0, 0]
choque2 = [0, 0]
liner_pos = [0, ball2_pos[1]]
lineb_pos = [0, ball1_pos[1]]
ang1m = 0.0
ang2m = 0.0
masa_a = 5.0 # kg
masa_r = 5.0 # kg
e = 1.0
teta2 = 0
reloj = stopwatch()
reloj.crear_timer()
bounds = False
reloj_roja = stopwatch()
reloj_roja.crear_timer()
tiempo_colision = ""
font_face = 'Arial'
color1 = "#2672F4"
color2 = "#FB3E3E"
color3 = "#54340F"

def draw(c):
    # metodo que se encargar de dibujar la simulacion en la ventana
    
    global choque, choque2, tiempo_colision
    tipo = ""
    if(ang1 == 0):
        tipo = "Frontal"
    else:
        tipo = "Oblicua"
    c.draw_text("Tipo de Colision: "+tipo, [10, 30], 10, "black", font_face+' black')
    # tiempo
    ta = reloj.get_time()
    c.draw_text("Tiempo recorrido bola Azul:> "+ta+" s", [10, 50], 10, color1, font_face)
    c.draw_text("Momento del Choque:> "+tiempo_colision+" s", [10, 70], 10, color3, font_face)
    c.draw_text("Tiempo recorrido bola Roja:> "+reloj_roja.get_time()+" s", [10, 90], 10, color2, font_face)
    if(start):
        msj = "On"
    else:
        msj = "Off"
    c.draw_text("Estado de la simulacion: "+msj, [10, 110], 10, color3, font_face)
    # ball 2, red
    c.draw_circle(ball2_pos, ball2_radius, 2, color2, color2)
    c.draw_line([0, ball2_pos[1]], [width, ball2_pos[1]], 1, color2)
    c.draw_line(liner_pos, [width, liner_pos[1]], 1, "black")
    # ball 1, blue
    c.draw_circle(ball1_pos, ball_radius, 2, color1, color1)
    c.draw_line([0, ball1_pos[1]], [width, ball1_pos[1]], 1, color1)
    c.draw_line(lineb_pos, [width, lineb_pos[1]], 1, "black")
    cad = ""
    ds = dis()
    if(ds - ball_radius - ball2_radius - ball1_vel[0] <= 0):
        cad = "Choque: "+str(ds)

        if(collision == False):
            choque[0] = ball1_pos[0]
            choque[1] = ball1_pos[1]
            choque2[0] = ball2_pos[0]
            choque2[1] = ball2_pos[1]
            nueva_velocidad()
            tiempo_colision = ta
            reloj_roja.start_handler()
    else:
        cad = str(ds)
    if collision:
        # vertical lines
        # red bal
        c.draw_line([choque2[0], 0], [choque2[0], height], 1, color2)
        # blue ball
        c.draw_line([choque[0], 0], [choque[0], height], 1, color1)
        # collision path
        # blue ball
        c.draw_line(choque, ball1_pos, 1, "blue")
        # red ball
        c.draw_line(choque2, ball2_pos, 1, "red")
        
    R = dy() / ball_radius
    c.draw_text("\nAngulo(A):> "+str(ang1m)+", Angulo(R):> "+str(ang2m)+"\n"+"Vfa(m/s): "+str(vfa) + ", Vfr(m/s): "+str(vfr), [10, 480], 10, color3, font_face)
    c.draw_text("Dist(R):"+ str(R)+", D:> "+cad+"\nVi(A)(m/s): "+str(velocidad)+", Vi(R)(m/s): "+str(vi2)+"\nVax(px/s): "+\
                str(velx * div)+", Vay(px/s): "+str(vely * div)+"\nVrx(px/s): "+\
                str(velx2 * div)+", Vry(px/s): "+str(vely2 * div), [10, 440], 10, color3, font_face)
    c.draw_line(ball1_pos, ball2_pos, 1, "gray")

def vel_final():
    # Calcula la velocidad final que tendran las bolas despues del impacto
    
    global vfr, vfa, ang2m, teta2, bounds
    teta1 = angulo()
    
    if(teta1 != 0):
        teta2 = 90.0 - teta1
        ang2m = abs(teta1) - 90
        R = dy() / ball_radius
        if(R < 0):
            ang2m *= -1
    else:
        teta2 = 0
        ang2m = teta2
        bounds = True
        
    if(teta1 != 0):
        vfr = ((e + 1) * masa_a * velocidad * math.cos(math.radians(teta2)))/(masa_a + masa_r)
        vfa = (masa_r * vfr * math.sin(math.radians(teta2))) / (masa_a * math.sin(math.radians(teta1)))        
    else:
        # a 180 grados
        vfa = ((masa_a - masa_r)/(masa_a + masa_r))* velocidad
        vfr = ((2 * masa_a)/(masa_a + masa_r)) * velocidad
    if(vfa == 0):
        reloj.stop_handler()
    if(vfr == 0):
        reloj_roja.stop_handler()
        
def nueva_velocidad():
    # Establece las componentes X y Y de la velocidad de cada una de las bolas despues del impacto
    
    global ball1_vel, velx, collision, ball2_vel, vely, velx2, vely2, ang1m, teta2
    vel_final()
    teta1 = angulo()
    ang = -1 * teta1
    velx = vfa * math.cos(math.radians(ang))
    velx = (velx * conv) / div
    vely = vfa * math.sin(math.radians(ang))
    vely = (vely * conv) / div
    ball1_vel = [velx, vely]
    collision = True

    # nueva velocida de la bola 2
    velx2 = vfr * math.cos(math.radians(teta2))
    velx2 = (velx2 * conv) / div
    vely2= vfr * math.sin(math.radians(teta2))
    vely2 = (vely2 * conv) / div
    ball2_vel = [velx2, vely2]
    ang1m = ang1
    
def dy():
    # Retorna la distancia vertical que hay entre el centro de una bola y la otra
    
    y = ball2_pos[1] - ball1_pos[1]
    return y

def dis():
    # distancia entre las dos bolas, es la hipotenusa
    
    x = ball1_pos[0] - ball2_pos[0]
    y = ball1_pos[1] - ball2_pos[1]
    d = math.sqrt(x ** 2 + y ** 2)    
    return d

def keydown(k):
    # Key Listener
    
    global cy, cy2

    if(not mover):
        d = 0
        d = dy()
        if(d / ball_radius < 1.9):
            if(k == sg.KEY_MAP['up']):
                ball1_pos[1] -= dist * ball_radius
                lineb_pos[1] -= dist * ball_radius
        if(d / ball_radius > -1.9):
            if(k == sg.KEY_MAP['down']):
                ball1_pos[1] += dist * ball_radius
                lineb_pos[1] += dist * ball_radius
        if(k == sg.KEY_MAP['right']):
                ball1_pos[0] += ball1_vel[0]
        if(k == sg.KEY_MAP['left']):
                ball1_pos[0] -= ball1_vel[0]

        if(k == sg.KEY_MAP['up'] or k == sg.KEY_MAP['down'] or k == sg.KEY_MAP['right'] or k == sg.KEY_MAP['left']):
            cy = ball1_pos[1]
            cy2 = ball2_pos[1]

def play():
    # Inicia la simulacion
    
    global start, mover
    start = not start
    if start:
        mover = True
    if start:
        reloj.start_handler()
    else:
        reloj.stop_handler()
        reloj_roja.stop_handler()

def t():
    # Este timer se ejecuta 100 veces por segundo y se encarga de actualizar la posicion de las bolas
    
    global bounds
    if start:
        cx1 = ball1_pos[0]
        cy1 = ball1_pos[1]
        cx2 = ball2_pos[0]
        cy2 = ball2_pos[1]
        vx1 = abs(ball1_vel[0])
        vy1 = abs(ball1_vel[1])
        vx2 = abs(ball2_vel[0])
        vy2 = abs(ball2_vel[1])

        # arriba y derecha
        if(cy1 - vy1 >= ball_radius and cx1 + vx1 <= width - ball_radius - 1):
            if(cx1 - vx1 >= ball_radius and cy1 + vy1 <= height - ball_radius):
                ball1_pos[0] += ball1_vel[0]
                ball1_pos[1] += ball1_vel[1]
            else:
                reloj.stop_handler()
                bounds = True
        else:
            reloj.stop_handler()
            bounds = True 

        # arriba y derecha    
        if(cy2 - vy2 >= ball2_radius and cx2 + vx2 <= width - ball2_radius - 1):
            if(cx2 - vx2 >= ball2_radius and cy2 + vy2 <= height - ball2_radius):
                ball2_pos[0] += ball2_vel[0]
                ball2_pos[1] += ball2_vel[1]
            else:
                reloj_roja.stop_handler()
        else:
            reloj_roja.stop_handler()

def vel(va):
    # Lee la velocidad inicial de la bola azul
    
    global velx, velocidad
    if(not mover and float(va) >= 0):
        try:
            velocidad = float(va)
        except ValueError:
            label_a.set_text(velocidad)
        velx = (velocidad * conv) / div
        ball1_vel[0] = velx
    else:
        label_a.set_text(velocidad)

def vel2(vr):
    # Lee la velocidad inicial de la bola roja
    
    global vi2
    vi2 = 0.0
    label_b.set_text(vi2)    

def masa1(ma):
    # Lee la masa inicial de la bola Azul
    
    global masa_a
    if(not mover and ang1 == 0 and float(ma) >= 0):
        try:
            masa_a = float(ma)
        except ValueError:
            label_m1.set_text(masa_a)
    else:
        label_m1.set_text(masa_a)

def masa2(mr):
    # Lee la masa inicial de la bola Roja
    
    global masa_r
    if(not mover and ang1 == 0 and float(mr) >= 0):
        try:
            masa_r = float(mr)
        except ValueError:
            label_m2.set_text(masa_r)
    else:
        label_m2.set_text(masa_r)
    
def rest(cr):
    # Lee el coeficiente de restitucion
    
    global e
    e = 1.0
    label_e.set_text(e)

def frontal():
    # Simulacion de un choque frontal
    
    global ball1_pos, lineb_pos
    reinicio()
    ball1_pos = [ball_radius * 2, height / 2]
    lineb_pos = [0, ball1_pos[1]]

def angulo():
    # Calcula el angulo de salida despues del choque de la bola azul
    global ang1
    hipotenusa = ball_radius + ball2_radius
    ady = dy()
    if(ady == 0):
        ang1 = 0
        return ang1
    opuesto = math.sqrt((hipotenusa ** 2) - (ady ** 2))
    div = opuesto / ady
    ang1 = math.degrees(math.atan(div))
    return ang1

def inicio_bola():
    # Repite el choque anterior
    
    global start, ang1m, ang2m, vfa, vfr, masa_a, masa_r, mover, tiempo_colision, bounds, ball1_pos, ball1_vel, collision, ball2_pos, ball2_vel, liner_pos, lineb_pos, ang1m, velx, vely, velx2, vely2
    ball1_pos = [ball_radius * 2, cy]
    velx = (velocidad * conv) / div
    vely = 0
    ball1_vel = [velx, vely]
    velx2 = 0
    vely2 = 0
    ball2_vel = [velx2, vely2]
    ball2_pos = [width / 2, height / 2]
    collision = False
    liner_pos = [0, ball2_pos[1]]
    lineb_pos = [0, ball1_pos[1]]
    reloj.reset_handler()
    reloj.stop_handler()
    bounds = False
    tiempo_colision = ""
    reloj_roja.reset_handler()
    reloj_roja.stop_handler()
    mover = False
    start = False
    masa_a = 5.0
    masa_r = 5.0
    label_m1.set_text(masa_a)
    label_m2.set_text(masa_r)
    vfa = 0
    vfr = 0
    ang1m = 0
    ang2m = 0

def reinicio():
    # Restablece los valores iniciales
    
    global start, ang1m, ang2m, vfa, vfr, masa_a, masa_r, mover, tiempo_colision, bounds, ball2_pos, ball1_pos, velx, vely, ball1_vel, collision, cy, vely2, velx2, ball2_vel, liner_pos, lineb_pos, ang1m
    ball2_pos = [width / 2, height / 2]
    ball1_pos = [ball_radius * 2, height / 2 - ball_radius]
    vely = 0
    velx = (velocidad * conv) / div
    ball1_vel = [velx, vely]
    velx2 = 0
    vely2 = 0
    ball2_vel = [velx2, vely2]
    collision = False
    liner_pos = [0, ball2_pos[1]]
    lineb_pos = [0, ball1_pos[1]]
    reloj.reset_handler()
    reloj.stop_handler()
    bounds = False
    tiempo_colision = ""
    reloj_roja.reset_handler()
    reloj_roja.stop_handler()
    label_a.set_text(velocidad)
    mover = False
    label_b.set_text(vi2)
    masa_a = 5.0
    masa_r = 5.0
    label_m1.set_text(masa_a)
    label_m2.set_text(masa_r)
    vfa = 0
    vfr = 0
    ang1m = 0
    ang2m = 0
    start = False

# init frame
f = sg.create_frame("Simulador de colisiones elasticas en 2D", width, height)
f.set_canvas_background("white")
f.set_draw_handler(draw)
f.set_keydown_handler(keydown)
f.add_button("Play / Pausa", play, 50)
f.add_button("Reinicio", reinicio, 50)
f.add_button("Choque anterior", inicio_bola, 50)
f.add_button("Choque frontal", frontal, 50)
label_a = f.add_input("Velocidad inicial A(m/s):", vel, 50)
label_a.set_text(velocidad)
label_b = f.add_input("Velocidad inicial R(m/s):", vel2, 50)
label_b.set_text(0.0)
label_m1 = f.add_input("Masa A(Kg):", masa1, 50)
label_m1.set_text(masa_a)
label_m2 = f.add_input("Masa R(Kg):", masa2, 50)
label_m2.set_text(masa_r)
label_e = f.add_input("Coeficiente de Restitucion:", rest, 50)
label_e.set_text(e)
timer = sg.create_timer(10, t) #100 veces por segundo
timer.start()
ang1m = ang1
# starting frame
f.start()
