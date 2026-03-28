import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import math

layers = 30+1

hex_length = 0

for i in range(layers):
    for j in range(i*6):
        hex_length = hex_length + 1

hexes = np.ones([1,hex_length])

rnd.seed()

for i in range(1,hex_length):
    rnd_int = rnd.randrange(6)
    
    if rnd_int > 2:
        hexes[0,i] = 0
        

fig, ax = plt.subplots()
good_hex = np.zeros([1,4])

index = 0
for i in range(layers):
    for j in range(i*6):
        if hexes[0,index] == 1:
            radius = i
            angle = j * 2 * math.pi / (i * 6)
            
            x = i * np.cos(angle)
            y = i * np.sin(angle)
            
            hex = np.zeros([1,4])
            hex[0,0] = x
            hex[0,1] = y
            hex[0,2] = i
            hex[0,3] = j
            good_hex = np.append(good_hex,hex,axis = 0)
            
            #ax.annotate(str(10-i) + "," + str(j+1),(x,y))
        index = index + 1

edges = []

for i in range(np.size(good_hex,axis = 0)):
    h1 = good_hex[i,:]
    for j in range(i+1, np.size(good_hex,axis = 0)):
        h2 = good_hex[j,:]
        i1 = h1[2]
        i2 = h2[2]
        j1 = h1[3]
        j2 = h2[3]
        plot = False
        if i2 == i1:
            if j2 - j1 == 1:
                plot = True
            elif j2 - j1 == i2 * 6-1:
                plot = True
        elif i2 - i1 == 1:
            s2 = int(j2 / i2)
            s1 = s2
            if i1 != 0:
                s1 = int(j1 / i1)
            
            if j2 - j1 == s2:
                plot = True
            elif j2 - j1 == i2 * 6 - 1:
                plot = True
            elif s1 == s2:
                if j2 % i2 - j1 % i1 == 1:
                    plot = True
        elif i2 - i1 > 1:
            break
        if plot == True:
            ax.plot([h1[0],h2[0]],[h1[1],h2[1]])
            edges.append([h1[2:3],h2[2:3]])
                    
ax.scatter(good_hex[:,0],good_hex[:,1])
plt.show()

        