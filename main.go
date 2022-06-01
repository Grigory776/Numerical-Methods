package main

import (
	"fmt"
	"math"
)

func f() float64{ // точное значение функции: integral(sin(x)dx) с нижним пределом 0, верхним pi
	return -(math.Cos(math.Pi) - math.Cos(0)) 
}

//формула трапеций. a,b - границы,
//n - количество точек
//f - интегрируемая функция
func trapezoidF(a,b float64, f func(float64)float64, n int)(res float64){  
	h := (b-a) / float64(n-1)
	for i:=0; i < n-1; i++{
		leftV := f(a + float64(i)*h)
		rightV := f(a + float64(i+1)*h)
		res += ((leftV+rightV)/2) * h
	}		
	return
}

//формула Симпсона
func simpsonF(a,b float64, f func(float64)float64, n int) (res float64){
	h := (b-a) / float64(n-1)
	for i:=0; i < n-1; i++{
		leftV := f(a + float64(i)*h)
		averageV := f(a + (float64(i) + 0.5)*h)
		rightV := f(a + float64(i+1)*h)
		res += (leftV + 4*averageV + rightV) * (h/6)
	}
	return
}

//формула Рунге
func rungeF(a,b float64, f func(float64)float64)float64{
	return (4*trapezoidF(a,b,f,21) - trapezoidF(a,b,f,11)) / 3
}

func main(){
	val := f()
	fmt.Printf("Точное значение интеграла:\n%v\n", val)

	val = trapezoidF(0, math.Pi, math.Sin, 11)
	fmt.Printf("Формула трапеции на 11 точках:\n%v\n", val)

	val = trapezoidF(0, math.Pi, math.Sin, 21)
	fmt.Printf("Формула трапеции на 21 точках:\n%v\n", val)

	val = simpsonF(0, math.Pi, math.Sin, 21)
	fmt.Printf("Формула Симсона на 21 точке:\n%v\n", val)

	val = rungeF(0, math.Pi, math.Sin)
	fmt.Printf("Формула Рунге:\n%v\n", val)

	bool_val := simpsonF(0,math.Pi,math.Sin,21) == rungeF(0,math.Pi,math.Sin)
	fmt.Printf("Формула Рунге равна формуле Симпсона на 21 точке?\n%v\n",bool_val)

}