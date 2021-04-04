package ua.kpi.comsys.rts

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.EditText
import android.widget.TextView
import androidx.core.widget.addTextChangedListener
import kotlin.math.ceil
import kotlin.math.pow
import kotlin.math.sqrt

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val number = findViewById<EditText>(R.id.number)
        val result = findViewById<TextView>(R.id.result)

        number.addTextChangedListener {
            if (it.toString().isNotEmpty()) result.text = ferma(it.toString().toFloat())
        }
    }

    fun ferma(number: Float) : String {
        var p = ceil(sqrt(number))
        var q = sqrt(p.pow(2) - number)
        while ( q < number) {
            if (q % 1 == 0f) return """ = ${(p + q).toInt()} * ${(p - q).toInt()}"""
            p++
            q = sqrt(p.pow(2) - number)
        }
        return "  Solution not founded! :("
    }
}