# Построение интерполяционного многочлена Ньютона
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def f(x): # Изначальная функция f = sinx * sqrt(x) + 1
    return np.sin(x)*np.sqrt(x)+1

def DifferenceR (array_x,array_y,size):
    res = 0
    for i in range(size+1):
        ch = array_y[i]
        zn = 1
        for j in range(size+1):
            if i != j:
                zn *= (array_x[i] - array_x[j])
        res += (ch/zn)
    return res

def PolinomNew (array_x,array_y,size):
    def resFunc(x):
        res = 0
        for i in range (size + 1):
            slg = DifferenceR(array_x,array_y,i)
            for j in range (i):
                slg *= (x - array_x[j])
            res += slg
        return res
    return resFunc

x = np.arange(0,2*np.pi,1/639) # Диапозон от 0 до 2Pi (по оси X)
y = f(x)
h = np.pi/7 
x1 = [0.5*h,2.5*h,6.5*h,4.5*h,1.5*h] # Узлы
y1 = [f(x1[0]),f(x1[1]),f(x1[2]),f(x1[3]),f(x1[4])] # Значения в узлах

#Надстройки окна
plt.figure(figsize=(9, 9))

for i in range(5):
    plt.subplot(2, 3, i+1)
    plt.title("Разложение " + str(i+1) + "-го порядка")
    plt.plot(x,y,label = "f(x)")
    PolNew = PolinomNew(x1,y1,i)
    if i == 0:
        resPolNew = np.full(len(x),PolNew(x))
    else:
        resPolNew = PolNew(x)
    plt.plot(x,resPolNew,label="Ln(x)")
    plt.scatter(x1[:i+1],y1[:i+1],label = "Узлы")
    plt.legend(loc = 1)
    plt.grid(True)
    plt.ylim((-5,5))


plt.show()



        
