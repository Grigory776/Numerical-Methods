import matplotlib.pyplot as plt
import numpy as np
 
# Структура, описывающая сплайн на каждом сегменте сетки
class SplineTuple:
    def __init__(self, a, b, c, d, x):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x = x

def f(x): # Изначальная функция f = sinx * sqrt(x) + 1
    return np.sin(x)*np.sqrt(x)+1
 
# Построение сплайна
# x - узлы сетки, должны быть упорядочены по возрастанию, кратные узлы запрещены
# y - значения функции в узлах сетки
# n - количество узлов сетки
def BuildSpline(x, y, n):
    # Инициализация массива сплайнов
    splines = [SplineTuple(0, 0, 0, 0, 0) for _ in range(0, n)]
    for i in range(0, n):
        splines[i].x = x[i]
        splines[i].a = y[i]
    
    splines[0].c = splines[n - 1].c = 0.0
    
    # Решение СЛАУ относительно коэффициентов сплайнов c[i] методом прогонки для трехдиагональных матриц
    # Вычисление прогоночных коэффициентов - прямой ход метода прогонки
    alpha = [0.0 for _ in range(0, n - 1)]
    beta  = [0.0 for _ in range(0, n - 1)]
 
    for i in range(1, n - 1):
        hi  = x[i] - x[i - 1]
        hi1 = x[i + 1] - x[i]
        A = hi
        C = 2.0 * (hi + hi1)
        B = hi1
        F = 6.0 * ((y[i + 1] - y[i]) / hi1 - (y[i] - y[i - 1]) / hi)
        z = (A * alpha[i - 1] + C)
        alpha[i] = -B / z
        beta[i] = (F - A * beta[i - 1]) / z
  
 
    # Нахождение решения - обратный ход метода прогонки
    for i in range(n - 2, 0, -1):
        splines[i].c = alpha[i] * splines[i + 1].c + beta[i]
    
    # По известным коэффициентам c[i] находим значения b[i] и d[i]
    for i in range(n - 1, 0, -1):
        hi = x[i] - x[i - 1]
        splines[i].d = (splines[i].c - splines[i - 1].c) / hi
        splines[i].b = hi * (2.0 * splines[i].c + splines[i - 1].c) / 6.0 + (y[i] - y[i - 1]) / hi
    return splines
 
 
# Вычисление значения интерполированной функции в произвольной точке
def Interpolate(splines, x):
    if not splines:
        return None # Если сплайны ещё не построены - возвращаем NaN
    
    n = len(splines)
    s = SplineTuple(0, 0, 0, 0, 0)
    
    if x <= splines[0].x: # Если x меньше точки сетки x[0] - пользуемся первым эл-тов массива
        s = splines[0]
    elif x >= splines[n - 1].x: # Если x больше точки сетки x[n - 1] - пользуемся последним эл-том массива
        s = splines[n - 1]
    else: # Иначе x лежит между граничными точками сетки - производим бинарный поиск нужного эл-та массива
        i = 0
        j = n - 1
        while i + 1 < j:
            k = i + (j - i) // 2
            if x <= splines[k].x:
                j = k
            else:
                i = k
        s = splines[j]
    
    dx = x - s.x
    # Вычисляем значение сплайна в заданной точке по схеме Горнера (в принципе, "умный" компилятор применил бы схему Горнера сам, но ведь не все так умны, как кажутся)
    return s.a + (s.b + (s.c / 2.0 + s.d * dx / 6.0) * dx) * dx
    
x = np.arange(0,2*np.pi,1/639) # Диапозон от 0 до 2Pi (по оси X)
y = f(x)
h = np.pi/7 
x1 = [0,0.5*h,1.5*h,2.5*h,4.5*h,6.5*h,np.pi] # Узлы
y1 = [f(x1[0]),f(x1[1]),f(x1[2]),f(x1[3]),f(x1[4]),f(x1[5]),f(x1[6])] # Значения в узлах

#Надстройки окна
plt.figure(figsize=(9, 9))


# Основная функция и все сплайны
plt.subplot(3,3,1)
plt.grid(True)
plt.xlim((0-0.1,np.pi+0.1))
plt.ylim((0,3))
plt.title(label = "Splines")
plt.plot(x,y,label = "f(x)")
plt.scatter(x1,y1,label = "Узлы")
splines = BuildSpline(x1, y1, len(x1))
value_splines = []
x2 = np.arange(0,np.pi,1/639) # Диапозон от 0 до Pi (по оси X)
for i in range(len(x2)):
    value_splines.append(Interpolate(splines,x2[i]))
plt.plot(x2,value_splines,label = "Splines")
#plt.legend(loc = 3)

#От 1 до 2 узла

for i in range(1,7):
    plt.subplot(3,3,i+1)
    plt.grid(True)
    plt.plot(x,y,label = "f(x)")
    plt.scatter(x1,y1,label = "Узлы")
    plt.xlim((x1[i-1]-0.1,x1[i]+0.1))
    if y1[i-1] - 0.1 < y1[i] + 0.1:
        plt.ylim((y1[i-1]-0.1,y1[i]+0.1))
    else:
        plt.ylim((y1[i],y1[i-1]))
    plt.plot(x2,value_splines,label = "Spline" + str(i))
   # plt.legend(loc = 2)
    
plt.show()
