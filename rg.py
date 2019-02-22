#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from genetic_algorithm import genetic_algorithm

def runge_kutta(func):
    def _inner(x, u):
        k1 = func(x        , u)
        k2 = func(x+k1*dt/2, u)
        k3 = func(x+k2*dt/2, u)
        k4 = func(x+k3*dt  , u)
        return x + (k1 + 2*k2 + 2*k3 + k4) * dt / 6
    return _inner

@runge_kutta
def nominal_model(x, u):
    return 10*(u-x)/4

@runge_kutta
def plant(x, u):
    dx = x[1,0]
    ddx = u/m
    return np.array([[dx, ddx]]).T

# シミュレーション条件
rd  = 1.0
m   = 1.0
kp  = 3.0
ki  = 1.0
kd  = 3.0
dt  = 0.01
EOS = 10

# 規範モデル出力と真の目標値を用いた場合の出力の計算(xnom: 規範モデル, xsim: 真の目標値)
xnom = 0.0
xsim = np.array([[0.0, 0.0]]).T

Xnom = [xnom]
Xsim = [xsim[0,0]]
SUM  = 0.0
lx   = xsim[0,0]
for i in range(1, int(EOS/dt)):
    e     = rd - xsim[0,0]
    SUM  += e*dt
    u     = kp*e + ki*SUM - kd*(xsim[0,0] - lx)/dt
    lx    = xsim[0,0]
    xsim  = plant(xsim, u)

    xnom = nominal_model(xnom, rd)

    Xnom.append(xnom)
    Xsim.append(xsim[0,0])

# GAの問題設定
def prob_rg(ind):
    X, _ = sim_ind(ind)
    return evaluate_ind(X, Xnom)

def sim_ind(ind):
    x   = np.array([[0.0, 0.0]]).T
    X   = [x[0,0]]
    T   = [0.0]
    SUM = 0.0
    lx  = x[0,0]
    mask = 2**3-1
    ref = rd*(ind&mask)/255
    ind >>=3
    for i in range(1, int(EOS/dt)):
        e    = ref - x[0,0]
        SUM += e*dt
        u    = kp*e + ki*SUM - kd*(x[0,0] - lx)/dt
        lx   = x[0,0]
        x    = plant(x, u)
        ref += rd*(ind&mask)/255
        ind >>=3
        X.append(x[0,0])
        T.append(i*dt)
    return X, T

# 評価関数
def evaluate_ind(x, xnom):
    x = np.array(x)
    xnom = np.array(xnom)
    mae = np.abs(x - xnom).mean()
    return 1/mae

# 学習過程の表示関数
def print_rg(i, elite):
    print(f'iter:{i+1:>7}   score:{elite[1]:>10.7}', end='\r')

# 学習結果の確認グラフ作成
def plot_ind(ind):
    X, T = sim_ind(ind)
    plt.plot(T, Xsim, label='simple')
    plt.plot(T, Xnom, label='nominal')
    plt.plot(T, X, label='rg')
    plt.legend()
    plt.show()

if __name__=='__main__':
    GENE_LENGTH = 8*int(EOS/dt)
    INDIVI_NUM  = 100
    MUTATE_PROB = 0.1
    GENERATIONS = 10000

    individuals, highscore_list = genetic_algorithm(GENE_LENGTH, INDIVI_NUM, MUTATE_PROB, prob_rg, generations=GENERATIONS, print_func=print_rg)

    elite = individuals[-1][0]

    plot_ind(elite)
