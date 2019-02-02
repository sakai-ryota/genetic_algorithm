#!/usr/bin/env python3
from genetic_algorithm import genetic_algorithm

# 個体の評価関数(one-max問題)
def eval_ind(ind):
    mask = 1
    count = 0
    while ind != 0:
        count += ind&mask
        ind>>=1
    return count

# 学習の終了条件(one-max問題)
def break_condition(score):
    return score[0] == 2**GENE_LENGTH-1

# sqrt(2)を求めてみる
def prob_sqrt2(ind):
    ind /= 2**GENE_LENGTH
    ind += 1
    error = abs(2-ind**2)
    return 1/(10*error)

# 学習の終了条件(sqrt2)
def break_cond_sqrt2(elite):
    gene = elite[0]
    ans = gene/2**GENE_LENGTH + 1
    error = abs(2-ans**2)
    return error <= 1/GENE_LENGTH

# 学習経過の表示(sqrt2)
def print_sqrt2(i, elite):
    import math
    print(f'iter:{i+1:>7}    solve:{elite[0]/(2**GENE_LENGTH)+1:>10.7}    ans:{math.sqrt(2):>10.7}    score:{elite[1]:>10.7}')

## 全画面推奨(one-max問題)
#GENE_LENGTH = 256
#INDIVI_NUM  = 10
#MUTATE_PROB = 0.05
#GENERATIONS = 100000

## 簡易版(one-max問題)
#GENE_LENGTH = 64
#INDIVI_NUM  = 5
#MUTATE_PROB = 0.08
#GENERATIONS = 20000

# sqrt2
GENE_LENGTH = 2**20
INDIVI_NUM  = 20
MUTATE_PROB = 0.05
GENERATIONS = 1000

## one-max問題
#elite = genetic_algorithm(GENE_LENGTH, INDIVI_NUM, MUTATE_PROB, GENERATIONS, eval_ind, break_condition)

# sqrt2
elite = genetic_algorithm(GENE_LENGTH, INDIVI_NUM, MUTATE_PROB, GENERATIONS, prob_sqrt2, break_condition, print_sqrt2)
