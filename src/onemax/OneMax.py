# -*- coding: utf-8 -*-

import random
import datetime

from deap import base
from deap import creator
from deap import tools

# 最大化適応度クラスを定義
creator.create("FitnessMax", base.Fitness, weights = (1.0,))
# リストクラスに適応度クラスを追加して Individual クラスとして定義
creator.create("Individual", list, fitness = creator.FitnessMax)

toolbox = base.Toolbox()
# randint にデフォルト引数として最小値 0、最大値 1 を与える attr_bool 関数を作成
toolbox.register("attr_bool", random.randint, 0, 1)
# 第二引数の値を第三引数回第一引数のコンテナに突っ込む関数 initRepeat を使って
# 100 要素のランダムな 0, 1 値を持つ Individual クラスを作る関数を作成
toolbox.register("create_individual", tools.initRepeat,
    creator.Individual, toolbox.attr_bool, 100)
# ↑の Individual インスタンスを一世代分作る関数を作成
# 第三引数（値生成回数）は mainで与える
toolbox.register("create_population", tools.initRepeat, list, toolbox.create_individual)

# 目的関数：適応度の算出に使う関数
def evalOneMax(individual):
    return sum(individual), # , は付けないとダメらしい <- tuple で受け取りたい模様

# 目的関数を登録 <- しないとダメなの？
toolbox.register("evaluate", evalOneMax)

# 黄砂関数：単なる２点交叉
toolbox.register("mate", tools.cxTwoPoint)

# 突然変異関数：Individual のブール値を 5 % の確率で変化させる
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.05)

# 選択関数：世代の中からランダムに数個体取り出して最も適応度の良いものを選ぶトーナメント選択
# 取り出す個体数を 3 で固定
# デフォルトで fitness なる名前を持つプロパティが使われる
toolbox.register("select", tools.selTournament, tournsize = 3)

# メイン関数
def main():
    random.seed(64)
    start = datetime.datetime.now()
    # 最初世代の個体
    pop = toolbox.create_population(n = 300)

    # 交叉確率
    cross_probability = 0.5
    # 個体が突然変異関数にかけられる確率
    mutation_probability = 0.2

    print("Start Evolution!")

    # 最初世代の全個体を目的関数で評価して格納
    # python はこれ one_liner で書けへんのか...
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # 適応度だけ抽出
    # これ fitnesses じゃだめなん...？ -> evaluate が tuple 返してくるから、ってことですね...。
    fits = [ind.fitness.values[0] for ind in pop]

    # 世代数
    g = 0

    means = []
    mins = []
    maxs = []

    # 最初分の統計量を計算して表示
    length = len(pop)
    mean = sum(fits) / length
    sum2 = sum(x*x for x in fits)
    std = abs(sum2 / length - mean**2)**0.5

    print("  Min %s" % min(fits))
    print("  Max %s" % max(fits))
    print("  Avg %s" % mean)
    print("  Std %s" % std)

    means.append(mean)
    mins.append(min(fits))
    maxs.append(max(fits))

    # 世代更新開始
    # 適応度が 100 を超える（まあそれが答えだからね...）やつが現れるか、
    # 1000 世代繰り返した時点で終了
    while max(fits) < 100 and g < 1000:
        # 世代数更新
        g = g + 1
        print("-- Generation %i --" % g)

        # 選択関数を使って世代の個体数分トーナメント選抜
        offspring = toolbox.select(pop, len(pop))
        # deep copy して参照を切る
        offspring = list(map(toolbox.clone, offspring))

        # 偶数インデックスの選抜個体と奇数インデックスの選抜個体とで交叉を試みる
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # 交叉確率の下で交叉させる
            if random.random() < cross_probability:
                toolbox.mate(child1, child2)

                # 交叉したので適応度を消しておく
                del child1.fitness.values
                del child2.fitness.values

        # 全選抜個体に対して突然変異を試みる
        for mutant in offspring:

            # 個体突然変異確率の下で突然変異させる
            if random.random() < mutation_probability:
                toolbox.mutate(mutant)
                # 突然変異したので適応度を消しておく
                del mutant.fitness.values

        # 消した適応度を再計算する
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # 世代を次世代と丸ごと入れ替える
        pop[:] = offspring

        # 適応度リストを次世代のものに更新
        fits = [ind.fitness.values[0] for ind in pop]

        # 統計量を計算して表示
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        means.append(mean)
        mins.append(min(fits))
        maxs.append(max(fits))

    print("-- End of (successful) evolution --")

    # fitness プロパティが最も良い 1 個体を選出
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    end = datetime.datetime.now()
    print(end - start)

    print(maxs)
    print(means)
    print(mins)

if __name__ == "__main__":
    main()
