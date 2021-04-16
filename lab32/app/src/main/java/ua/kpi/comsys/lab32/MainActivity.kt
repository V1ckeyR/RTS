package ua.kpi.comsys.lab32

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import kotlinx.coroutines.*
import ua.kpi.comsys.lab32.databinding.ActivityMainBinding
import kotlin.system.measureTimeMillis

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val ls = arrayOf("0.001", "0.01", "0.05", "0.1", "0.2", "0.3")
        val td = arrayOf("0.5c", "1c", "2c", "5c")
        val mi = arrayOf("100", "200", "500", "1000")

        with(binding.learningSpeed) {
            minValue = 0
            maxValue = ls.size - 1
            displayedValues = ls
        }

        with(binding.timeDeadline) {
            minValue = 0
            maxValue = td.size - 1
            displayedValues = td
        }

        with(binding.maxIterations) {
            minValue = 0
            maxValue = mi.size - 1
            displayedValues = mi
        }

        with(binding) {
            btn.setOnClickListener {
                val timer = td[timeDeadline.value]
                var clock: Job? = null

                val train = GlobalScope.launch {
                    val result: Array<String>
                    val time = measureTimeMillis {
                        result = perceptron(
                                ls[learningSpeed.value].toFloat(),
                                mi[maxIterations.value].toInt()
                        )
                    }

                    clock?.cancelAndJoin()
                    withContext(Dispatchers.Main) {
                        iterations.text = result[0]
                        w1.text = result[1]
                        w2.text = result[2]
                        timeResult.text = ("$time ms")
                    }
                }

                clock = GlobalScope.launch {
                    delay((timer.subSequence(0, timer.lastIndex).toString().toFloat() * 1000).toLong())
                    train.cancelAndJoin()

                    withContext(Dispatchers.Main) {
                        iterations.text = "N/A"
                        w1.text = "Not found"
                        w2.text = "Not found"
                        timeResult.text = timer
                    }
                }
            }
        }
    }

    private fun perceptron(ls: Float, mi: Int): Array<String> {
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
}