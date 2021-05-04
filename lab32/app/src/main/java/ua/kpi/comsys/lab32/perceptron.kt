package ua.kpi.comsys.lab32

import kotlin.math.pow

fun perceptron(ls: Float, mi: Int): Array<String> {
    val p = 4
    var delta: Float
    val points = arrayOf(0 to 6, 1 to 5, 3 to 3, 2 to 4)
    val more = points.filter { it.second > p }
    val less = points.filter { it.second <= p }

    var w1 = 0f
    var w2 = 0f

    fun y(x1: Int, x2: Int) = x1 * w1 + x2 * w2
    fun next(w: Float, delta: Float, x: Int) = w + delta * x * ls

    for (i in 0..mi) {
        val point = points[i % points.size]
        delta = p - y(point.first, point.second)

        if (more.all { y(it.first, it.second) > p } && less.all { y(it.first, it.second) < p })
            return arrayOf(i.toString(), w1.toString(), w2.toString())

        w1 = next(w1, delta, point.first)
        w2 = next(w2, delta, point.second)
    }
    return arrayOf(mi.toString(), "Not found", "Not found")
}

fun main() {
    // одну і ту ж задачу вирішіть різними "сігмами" (наприклад від 0.1 до 0.9) та
    // зробіть відповідний  висновок яка сігма була найкращою для вирішення поставленої задачі
    println("sigma -> iteration, results")
    for (i in 3 downTo 1) {
        for (j in 1..9) {
            val sigma = "%.${i}f".format(0.1f.pow(i) * j).toFloat()
            println("$sigma -> ${perceptron(sigma, 1000).contentToString()}")
        }
    }
    // найкращою для вирішення поставленої задачі є сігма 0.04
}