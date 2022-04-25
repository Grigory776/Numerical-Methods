# Построение интерполяционного многочлена Лагранжа
import numpy as np
import matplotlib.pyplot as plt

def f(x): # Изначальная функция f = sinx * sqrt(x) + 1
    return np.sin(x)*np.sqrt(x)+1


def basicFuncLagr(array_x,i): # Функция, возвращает базисную функцию iго номера
    def resFunc(x):
        ch = 1
        zn = 1
        for j in range(len(array_x)):
            if i!=j:
                ch *= (x - array_x[j])
                zn *= (array_x[i] - array_x[j])
        return ch/zn
    return resFunc

def funcLagr(array_x,array_y): # Возвращает функцию Лагранжа от двух массивов
    def resFunc(x):
        res = 0
        for i in range(len(array_x)):
            tmp = basicFuncLagr(array_x,i)
            res+=tmp(x)*array_y[i]
        return res
    return resFunc

x = np.arange(0,2*np.pi,1/639) # Диапозон от 0 до 2Pi (по оси X)
y = f(x)
h = np.pi/7 
x1 = [0.5*h,1.5*h,2.5*h,4.5*h,6.5*h] # Узлы
y1 = [f(x1[0]),f(x1[1]),f(x1[2]),f(x1[3]),f(x1[4])] # Значения в узлах
Lagr = funcLagr(x1,y1)

#Надстройки окна
plt.figure(figsize=(9, 9))
plt.title('Function')
plt.ylabel('Y')
plt.xlabel('X')
plt.grid(True)
plt.ylim((-5,5))

plt.plot(x,y,label = "f(x)")
for i in range(5):
    plt.plot(x,basicFuncLagr(x1,i)(x),label = "Базисная функция - " + str(i+1) )
plt.plot(x,Lagr(x),label="Ln(x)")
plt.scatter(x1,y1,label = "Узлы")
plt.legend(loc = 1)
plt.show()




            

