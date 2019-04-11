using MathNet.Numerics.Random;
using System;
using System.Linq;

namespace GeneticAlgorithm.OneMax
{
    public class Individual
    {
        /// <summary>
        /// 遺伝子の数
        /// </summary>
        private static readonly int gene_count = 100;
        /// <summary>
        /// 個体が突然変異する確率
        /// </summary>
        private static readonly double ind_mutate_pb = 40;
        /// <summary>
        /// 突然変異した個体において、各遺伝子が突然変異する確率
        /// </summary>
        private static readonly double gene_mutate_pb = 5;

        /// <summary>
        /// この個体の遺伝子
        /// </summary>
        private byte[] genes;

        /// <summary>
        /// この個体の適応度
        /// </summary>
        public int Fitness => genes.Sum(x => x);

        /// <summary>
        /// OneMax 問題用の個体を生成します。
        /// </summary>
        public Individual()
        {
            genes = MersenneTwister.Doubles(100, RandomSeed.Guid())
                .Select(dVal => (byte)Math.Round(dVal, MidpointRounding.AwayFromZero))
                .ToArray();
        }

        /// <summary>
        /// この個体の遺伝子を一定確率の下で突然変異させます。
        /// </summary>
        public void TryMutate()
        {
            var mt = new MersenneTwister(RandomSeed.Guid());
            var percentage = mt.Next(0, 99);
            if (percentage >= ind_mutate_pb) return;

            genes = genes.Select(gene =>
                {
                    var percent = mt.Next(0, 99);
                    if (percent >= gene_mutate_pb) return gene;
                    return gene == 0 ? (byte)1 : (byte)0;
                })
                .ToArray();
        }
    }
}
