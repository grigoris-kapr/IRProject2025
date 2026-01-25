package ir.website.dashboard

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

@Composable
fun SearchSection(
    state: ViewModel.State,
    onAction: (ViewModel.Action) -> Unit
) {
    Column(
        verticalArrangement = Arrangement.spacedBy(8.dp, Alignment.Top),
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .padding(vertical = 16.dp)
    ) {
        Row(
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .fillMaxWidth(0.5f)
                .height(56.dp)
        ) {
            OutlinedTextField(
                value = state.searchQuery,
                shape = RoundedCornerShape(
                    topStart = 16.dp,
                    bottomStart = 16.dp,
                    topEnd = 0.dp,
                    bottomEnd = 0.dp
                ),
                onValueChange = { newValue ->
                    onAction(ViewModel.Action.UpdateSearchQuery(newValue))
                },
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

        state.results.forEach { result ->
            Text(text = result)
        }
    }
}