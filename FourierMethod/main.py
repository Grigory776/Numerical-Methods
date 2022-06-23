import math
import matplotlib.pyplot as plt 
import numpy as np 

l = np.pi /2

def u0(x):
    if x < l/3:
        return 3*x/l
    else:
        return 1

def w0(x):
    return u0(x) - x/l

def w0n(xi, n): #функция зависит от набора узлов xi
    sum = 0
    N = len(xi)
    i = 1
    while i <= N-1:
        sum+=w0(xi[i])*math.sin((math.pi * n * xi[i])/l)
        i+=1
    return (2/N)*sum

def u(x, xi, j):
    sum = 0
    N = len(xi)+1
    n = 1
    while n <= N-1:
        sum += w0n(xi, n) * math.exp(-(n*n*j*j)/100) * math.sin((math.pi*n*x)/l)
        n += 1
    return x/l + sum

#строим u0
x = np.arange(0, np.pi, 1 / 640)
y = []
for i in range (len(x)):
    y.append(u0(x[i]))
plt.plot(x,y,label = "u0(x)")

#строим u(x,t)|t=0
x = np.arange(0, np.pi, 1 / 640)
h = l/20
xi = []
for i in range (20):
    xi.append(i * h)
y = []

for j in range(20):
    for i in range (len(x)):
        y.append(u(x[i],xi,j))
    plt.plot(x,y)
    y = []



plt.ylim([0, 1.2]) 
plt.xlim([0, 1.6]) 
plt.grid(True) 
plt.legend(loc = 1)
plt.show()

