#!/usr/bin/env python3
import random
import matplotlib.pyplot as plt

def genetic_algorithm(gene_length, individual_num, mutate_prob,
        generations, eval_func, break_func=None, print_func=None):
    """
    genetic_algorithm(gene_length, individual_num, mutate_prob, generations, eval_func, break_func=None)

    args:
        gene_length:        gene's length.
        individual_num:     number of individuals.
        mutate_prob:        probability of mutation.
        generations:        number of generations.
        eval_func:          function of evaluation of individual.
        break_func:         (optional) main loop break condition.
        print_func:         (optional) score print function.
    """
    # 一点交叉を行なう関数
    def one_point_cross_over(a, b):
        # 交叉を行なう位置をランダムに決定
        mid = random.randint(1, gene_length)
        # 下位ビットマスク
        lmask = 2**mid-1
        # 上位ビットマスク
        gmask = (2**gene_length-1)-lmask
        # 交叉
        c = a
        a = (a&gmask)|(b&lmask)
        b = (b&gmask)|(c&lmask)
        return (a, b, mid)

    # （なんちゃって）一様交叉を行う関数
    def uniform_cross_over(a, b):
        mask = random.randint(0, 2**8-1)
        rmask = ~mask&(2**8-1)
        # 交叉
        c = a
        a = (a&mask) | (b&rmask)
        b = (b&mask) | (c&rmask)
        return (a, b, mask)

    # 突然変異を行なう関数
    def mutate(a):
        # マスクの作成
        mask = random.randint(0, 2**gene_length-1)
        # 乱数によって突然変異を制御
        if random.random() <= mutate_prob:
            # 排他的論理和によってデータを書き換える
            return (a ^ mask, mask)
        else:
            # 乱数が閾値を超えたら突然変異を行わない
            return (a, mask)

    # デフォルトの学習経過表示関数
    def default_print_func(i, elite):
        print(f'{i:<7}{elite[0]:0{gene_length}b}{elite[1]:>5}/{gene_length}')

    # 各世代の最高スコアを格納するためのリスト
    score_list = []
    # 現世代のリスト(初期化)
    population = [random.randint(0, 2**gene_length-1) for _ in range(individual_num)]
    for i in range(generations):
        # 次世代を格納するためのリスト
        pop_next     = []
        # 各個体を評価
        eval_list    = sorted([(ind, eval_func(ind)) for ind in population], key=lambda x: x[1])
        # 適合度の計算
        fitness_list = [score[1]/sum([s[1] for s in eval_list]) for score in eval_list]
        # エリート個体を次世代リストへ格納
        pop_next.append(eval_list[-1][0])
        # 現世代の最高スコアを格納
        score_list.append(eval_list[-1][1])
        # 学習経過を表示
        if print_func == None:
            default_print_func(i, eval_list[-1])
        else:
            print_func(i, eval_list[-1])
        for i in range(len(population)-1):
            # ２個体を選択
            a, b = random.choices(population, weights=fitness_list, k=2)
            # 重複していれば選び直し
            while a == b:
                a, b = random.choices(population, weights=fitness_list, k=2)
            # 交叉（一点と一様の入れ替えは適当）
            if random.randint(0,100)<95:
                # 一点交叉
                a, b, _ = one_point_cross_over(a, b)
            else:
                # 一様交叉
                a, b, _ = uniform_cross_over(a, b)
            # 突然変位
            a, _ = mutate(a)
            # 次世代リストへの格納
            pop_next.append(a)
        # 次世代リストで現世代を上書き
        population = pop_next.copy()
        # one-max問題が解けたら終了
        if break_func != None:
            if break_func(eval_list[-1]):
                break

    # 最高スコアの推移をプロット
    plt.plot(score_list)
    plt.tight_layout()

    plt.show()

    return eval_list[-1]
