package ir.website.dashboard.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.dropShadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.shadow.Shadow
import androidx.compose.ui.unit.dp
import ir.website.dashboard.data.DocumentDto

@Composable
fun DocumentSection(
    document: DocumentDto,
) {
    Card(
        modifier = Modifier
            .fillMaxWidth(),
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .padding(
                    horizontal = 24.dp,
                    vertical = 12.dp
                ).fillMaxWidth()
        ) {
            Text(
                text = document.text,
                modifier = Modifier
                    .weight(1f)
            )

            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(8.dp, Alignment.CenterVertically),
                modifier = Modifier
                    .width(200.dp)
            ) {
                document.keywords.forEach { keyWord ->
                    Text(
                        text = keyWord,
                        modifier = Modifier
                            .dropShadow(
                                shape = CircleShape,
                                shadow = Shadow(
                                    radius = 4.dp,
                                    color = Color.LightGray
                                )
                            ).background(
                                color = Color.White,
                                shape = CircleShape
                            ).padding(4.dp)
                    )
                }
            }
        }
    }
}