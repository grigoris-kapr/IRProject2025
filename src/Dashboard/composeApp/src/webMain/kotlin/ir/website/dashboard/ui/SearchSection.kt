package ir.website.dashboard.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import ir.website.dashboard.components.DocumentSection
import ir.website.dashboard.components.SearchField

@Composable
fun SearchSection(
    state: ViewModel.State,
    onAction: (ViewModel.Action) -> Unit
) {
    Column(
        verticalArrangement = Arrangement.spacedBy(8.dp, Alignment.Top),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        SearchField(
            searchQuery = state.searchQuery,
            onAction = onAction
        )

        Column(
            verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.Top),
            modifier = Modifier
                .padding(horizontal = 16.dp)
                .width(1000.dp)
        ) {
            state.documents.forEach { result ->
                DocumentSection(result)
            }
        }
    }
}