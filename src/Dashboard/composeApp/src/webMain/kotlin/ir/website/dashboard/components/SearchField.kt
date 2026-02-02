package ir.website.dashboard.components

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import ir.website.dashboard.ui.ViewModel

@Composable
fun SearchField(
    searchQuery: String,
    onAction: (ViewModel.Action) -> Unit
) {
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .width(500.dp)
            .height(56.dp)
    ) {
        OutlinedTextField(
            value = searchQuery,
            shape = RoundedCornerShape(
                topStart = 16.dp,
                bottomStart = 16.dp,
                topEnd = 0.dp,
                bottomEnd = 0.dp
            ),
            placeholder = { Text(text = "Search") },
            maxLines = 1,
            singleLine = true,
            onValueChange = { newValue ->
                onAction(ViewModel.Action.UpdateSearchQuery(newValue))
            },
            modifier = Modifier
                .weight(1f)
        )
        Button(
            onClick = { onAction(ViewModel.Action.GetResults) },
            shape = RoundedCornerShape(
                topStart = 0.dp,
                bottomStart = 0.dp,
                topEnd = 16.dp,
                bottomEnd = 16.dp
            ),
            modifier = Modifier.fillMaxHeight()
        ) {
            Icon(Icons.Default.Search, contentDescription = "Search")
        }
    }
}