#!/usr/bin/env python3
from ga import genetic_algorithm

# 個体の評価関数(one-max問題)
def eval_ind(ind):
    mask = 1
    count = 0
    while ind != 0:
        count += ind&mask
        ind>>=1
    return count

# 学習の終了条件
def break_condition(score):
    return score == 2**GENE_LENGTH-1

## 全画面推奨
#GENE_LENGTH = 256
#INDIVI_NUM  = 10
#MUTATE_PROB = 0.08
#GENERATIONS = 100000

GENE_LENGTH = 64
INDIVI_NUM  = 5
MUTATE_PROB = 0.08
GENERATIONS = 20000

genetic_algorithm(GENE_LENGTH, INDIVI_NUM, MUTATE_PROB, GENERATIONS, eval_ind, break_condition)
