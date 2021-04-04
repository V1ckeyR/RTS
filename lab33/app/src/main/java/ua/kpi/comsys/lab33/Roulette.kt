package ua.kpi.comsys.lab33

import kotlin.math.abs
import kotlin.random.Random


class Chromosome(private val range: IntRange,
                 private val coefficients: List<Int>,
                 private val y: Int) {
    var data = List(4) { range.random() }
    val fitness: Int by lazy {
        val result = data.mapIndexed { i, v -> coefficients[i] * v }.sum()
        abs(y - result)
    }
}

class Roulette(a: Int, b: Int, c: Int, d: Int, private val y: Int) {
    private val coefficients = listOf(a, b, c, d)
    private val range = 0..y / coefficients.maxOf { it }

    fun run(): List<Int>? {
        var chromosomes = initGeneration()
        for (g in 1..100) {
            chromosomes.forEach { if (it.fitness == 0) return it.data }
            if (chromosomes.all { it.data == chromosomes.first().data }) chromosomes = initGeneration()

            chromosomes = selection(chromosomes).map(this::crossing).flatten()
            chromosomes.forEach(this::mutation)
        }
        return null
    }

    private fun initGeneration() = List(4) { Chromosome(range, coefficients, y) }

    private fun generator(ch: List<Chromosome>): Chromosome {
        val roulette = ch.map { 1.0 / it.fitness }.sum()
        val chances = ch.map { 1.0 / it.fitness / roulette }
        val rand = Random.nextFloat()
        var a = 0.0
        for (i in chances.indices) {
            if (rand <= chances[i] + a) return ch[i]
            a += chances[i]
        }
        return ch.last()
    }

    private fun pair(ch: List<Chromosome>): List<Chromosome> {
        val ch1 = generator(ch)
        val ch2 = generator(ch.filterNot { it == ch1 })
        return listOf(ch1, ch2)
    }

    private fun selection(ch: List<Chromosome>) = List(2) { pair(ch) }

    private fun crossing(pair: List<Chromosome>): List<Chromosome> {
        val ch1 = pair[0].data
        val ch2 = pair[1].data
        val point = Random.nextInt(1, ch1.lastIndex + 1)

        val ch3 = Chromosome(range, coefficients, y)
        ch3.data = ch1.subList(0, point) + ch2.subList(point, ch2.lastIndex + 1)

        val ch4 = Chromosome(range, coefficients, y)
        ch4.data = ch2.subList(0, point) + ch1.subList(point, ch1.lastIndex + 1)

        return listOf(ch3, ch4)
    }

    private fun mutation(ch: Chromosome) {
        val mutationProbability = 0.1
        if (Random.nextFloat() <= mutationProbability) {
            val newData = ch.data.toMutableList()
            val index = Random.nextInt(newData.lastIndex + 1)

            val mutation = newData[index] + if (Random.nextBoolean()) 1 else -1
            if (mutation in range) {
                newData[index] = mutation
                ch.data = newData
            }
        }
    }
}