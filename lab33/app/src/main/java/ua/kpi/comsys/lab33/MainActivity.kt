package ua.kpi.comsys.lab33

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import ua.kpi.comsys.lab33.databinding.ActivityMainBinding
import kotlin.system.measureTimeMillis

class MainActivity : AppCompatActivity() {
    lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        with(binding) {
            calculate.setOnClickListener {
                val argA = if (a.text.isNullOrBlank()) 0 else a.text.toString().toInt()
                val argB = if (b.text.isNullOrBlank()) 0 else b.text.toString().toInt()
                val argC = if (c.text.isNullOrBlank()) 0 else c.text.toString().toInt()
                val argD = if (d.text.isNullOrBlank()) 0 else d.text.toString().toInt()
                val argY = if (y.text.isNullOrBlank()) 0 else y.text.toString().toInt()

                val res: Pair<List<Int>, Int>?
                val time = measureTimeMillis {
                    res = try {
                        Roulette(argA, argB, argC, argD, argY).run()
                    } catch (e:Exception) {
                        null
                    }
                }

                val resultText = (res?.first ?: "Not found :(").toString()
                val iterationsText = (res?.second ?: "> 100").toString()
                val timeMsText = "$time ms"

                result.text = resultText
                iterations.text = iterationsText
                timeMs.text = timeMsText
            }
        }
    }
}
