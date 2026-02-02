package ir.website.dashboard.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp

@Composable
fun KeywordsList(
    keywords: Map<String, List<String>>,
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(30.dp, Alignment.Top)
    ) {
        keywords.entries.forEachIndexed { index, (title, keywords) ->
            KeywordsItem(
                title = title,
                keywords = keywords,
            )
        }
    }
}

@Composable
fun KeywordsItem(
    title: String,
    keywords: List<String>,
) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterHorizontally),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            textAlign = TextAlign.End,
            text = title,
            modifier = Modifier
                .weight(1f)
        )
        Box(
            modifier = Modifier
                .size(40.dp)
                .background(Color.Red, shape = CircleShape)
        )
        Text(
            textAlign = TextAlign.Start,
            text = keywords.joinToString(", "),
            modifier = Modifier
                .weight(1f)
        )
    }
}