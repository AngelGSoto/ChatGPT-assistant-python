import numpy as np
from scipy.integrate import ode

# Define la función que describe el sistema de ecuaciones diferenciales
def three_body(t, y, G, m1, m2, m3):
    # Extrae los vectores de posición y velocidad de los cuerpos
    x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, x3, y3, z3, vx3, vy3, vz3 = y

    # Calcula las distancias entre los cuerpos
    r12 = np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
    r13 = np.sqrt((x1 - x3)**2 + (y1 - y3)**2 + (z1 - z3)**2)
    r23 = np.sqrt((x2 - x3)**2 + (y2 - y3)**2 + (z2 - z3)**2)

    # Calcula las aceleraciones de cada cuerpo
    ax1 = G * m2 * (x2 - x1) / r12**3 + G * m3 * (x3 - x1) / r13**3
    ay1 = G * m2 * (y2 - y1) / r12**3 + G * m3 * (y3 - y1) / r13**3
    az1 = G * m2 * (z2 - z1) / r12**3 + G * m3 * (z3 - z1) / r13**3

    ax2 = G * m1 * (x1 - x2) / r12**3 + G * m3 * (x3 - x2) / r23**3
    ay2 = G * m1 * (y1 - y2) / r12**3 + G * m3 * (y3 - y2) / r23**3
    az2 = G * m1 * (z1 - z2) / r12**3 + G * m3 * (z3 - z2) / r23**3

    ax3 = G * m1 * (x1 - x3) / r13**3 + G * m2 * (x2 - x3) / r23**3
    ay3 = G * m1 * (y1 - y3) / r13**3 + G * m2 * (y2 - y3) / r23**3
    az3 = G * m1 * (z1 - z3) / r13**3 + G * m2 * (z2 - z3) / r23**3

    # Retorna las derivadas de cada variable
    return [vx1, vy1, vz1, ax1, ay1, az1, vx2, vy2, vz2, ax2, ay2, az2, vx3, vy3, vz3, ax3, ay3, az3]

# Define las condiciones iniciales y los parámetros del sistema
y0 = [1, 0, 0, 0, 0.5, 0, -1, 0, 0, 0, -0.5, 0, 0, 0, 0, 0, 0]
t0 = 1
tmax = 20
dt = 0.01
G = 1
m1 = 1
m2 = 1
m3 = 1

# Crea el objeto que resuelve la ecuación diferencial
solver = ode(three_body)
solver.set_integrator('dopri5')
solver.set_initial_value(y0, t0)
solver.set_f_params(G, m1, m2, m3)

# Define las listas para almacenar las posiciones de los cuerpos
x1_list = []
y1_list = []
z1_list = []
x2_list = []
y2_list = []
z2_list = []
x3_list = []
y3_list = []
z3_list = []

# Resuelve la ecuación diferencial y almacena las posiciones de los cuerpos
while solver.successful() and solver.t < tmax:
    x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, x3, y3, z3, vx3, vy3, vz3 = solver.y
    x1_list.append(x1)
    y1_list.append(y1)
    z1_list.append(z1)
    x2_list.append(x2)
    y2_list.append(y2)
    z2_list.append(z2)
    x3_list.append(x3)
    y3_list.append(y3)
    z3_list.append(z3)
    solver.integrate(solver.t + dt)

# Grafica las trayectorias de los cuerpos
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x1_list, y1_list, z1_list)
ax.plot(x2_list, y2_list, z2_list)
ax.plot(x3_list, y3_list, z3_list)
plt.show()
