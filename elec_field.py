import numpy as np
import matplotlib.pyplot as plt

path = "" #### path of your folder

n = 0
N_max = 195
dt=0.004

Xm = [-5,0]
Ym = [0,0]
VXm = [0,0]
VYm = [30,0]
M  = [1,1000]
Q = [-1000,1000]

lenght = 10
pixel = 300
e0 = 1
k=1/(4*np.pi*e0)

nb_particules = len(M)

x = np.linspace(-lenght, lenght, pixel)
y = np.linspace(-lenght, lenght, pixel)
Y, X = np.meshgrid(x, y)

max_magnitude_vector = 1.5
arrow_spacing = 5
arrow_scale = 3
U, V = np.meshgrid(y[::arrow_spacing], x[::arrow_spacing])

field_E = np.gradient(np.zeros((pixel,pixel)))
field_E_trace = np.gradient(np.zeros((pixel,pixel)))
list_field=[field_E]*nb_particules

def field_Elec(q, xq, yq):
    e = 1e-10
    return np.gradient(-k * q / (np.sqrt((X-xq)**2 + (Y-yq)**2) + e))


while n<N_max:

    Xn = Xm.copy()
    Yn = Ym.copy()
    field_E_calc = np.gradient(np.zeros((pixel,pixel)))

    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(111)

    for i in range(nb_particules):

        xi=int(pixel*(1+(Xn[i]/lenght))/2)
        yi=int(pixel*(1+(Yn[i]/lenght))/2)
        q=Q[i]
    
        c0=field_E[0]-list_field[i][0]
        c1=field_E[1]-list_field[i][1]

        AX = q*c0[xi,yi]/M[i]
        AY = q*c1[xi,yi]/M[i]

        VXm[i] += AX*dt/2
        VYm[i] += AY*dt/2

        Xm[i] += VXm[i]*dt + AX*(dt**2)/2
        Ym[i] += VYm[i]*dt + AY*(dt**2)/2

        VXm[i] += AX*dt/2
        VYm[i] += AY*dt/2

        field=field_Elec(q,Xm[i],Ym[i])
        list_field.append(field)
        field_E_calc[0] += field[0]
        field_E_calc[1] += field[1]

    list_field=list_field[nb_particules:]

    field_E=field_E_calc
    
    magnitude = np.sqrt(field_E[0]**2 + field_E[1]**2)
    exceeds_max = magnitude > max_magnitude_vector
    scaling_factor = max_magnitude_vector / magnitude
    scaling_factor[~exceeds_max] = 1  

    field_E_trace[0] = field_E[0]*scaling_factor
    field_E_trace[1] = field_E[1]*scaling_factor

    EV = field_E_trace[1].T[::arrow_spacing, ::arrow_spacing]
    EU = field_E_trace[0].T[::arrow_spacing, ::arrow_spacing]
    ax.quiver(U, V, EU, EV, scale=arrow_scale, color='red', scale_units='xy', angles='xy')
    
    ax.set_aspect("equal", "box")
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(path+'/'+("0"*(4-len(str(n))))+str(n)+".png")
    n += 1
    plt.close('all')
    print(str(n)+'/'+str(N_max))



import os
from moviepy.editor import ImageSequenceClip

print(os.getcwd())
image_folder = path

os.chdir(image_folder)
 
images = [img for img in os.listdir(image_folder)
        if  img.endswith(".jpg") or
            img.endswith(".jpeg") or
            img.endswith("png")]
     
print(images) 
  
clip = ImageSequenceClip(images, fps = 40)

clip.ipython_display(width = 360)