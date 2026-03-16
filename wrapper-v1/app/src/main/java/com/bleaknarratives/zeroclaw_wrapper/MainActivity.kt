package com.bleaknarratives.zeroclaw_wrapper

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import com.bleaknarratives.zeroclaw_wrapper.ui.theme.ZeroclawWrapperTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ZeroclawWrapperTheme {
                Surface(color = MaterialTheme.colors.background) {
                    Dashboard()
                }
            }
        }
        startEventStreaming() // Start the socket connection for real-time events
    }

    private fun startEventStreaming() {
        // Implement TCP socket connection and event streaming logic here
    }
}

@Composable
fun Dashboard() {
    // Implement your dashboard UI here, including the status widget and TTS output
}

@Preview(showSystemUi = true, device = Devices.PIXEL_4)
@Composable
fun PreviewDashboard() {
    Dashboard()
}