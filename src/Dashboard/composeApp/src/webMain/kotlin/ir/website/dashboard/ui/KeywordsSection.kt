package ir.website.dashboard.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.VerticalDivider
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp.Companion.Hairline
import androidx.compose.ui.unit.dp
import ir.website.dashboard.components.Dropdown
import ir.website.dashboard.components.KeywordsList

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun KeywordsSection(
    state: ViewModel.State,
    onAction: (ViewModel.Action) -> Unit
) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .height(IntrinsicSize.Min)
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .weight(1f)
        ) {
            Dropdown(
                label = "Select Member",
                value = state.selectedMember,
                options = state.members,
                onOptionSelected = {
                    onAction(ViewModel.Action.GetMemberKeywords(it))
                }
            )
            Spacer(
                modifier = Modifier
                    .height(16.dp)
            )
            KeywordsList(
                keywords = state.memberKeywords
            )
        }

        VerticalDivider(
            thickness = Hairline,
            color = Color.Black,
            modifier = Modifier
                .fillMaxHeight()
        )

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .weight(1f)
        ) {
            Dropdown(
                label = "Select Party",
                value = state.selectedParty,
                options = state.parties,
                onOptionSelected = {
                    onAction(ViewModel.Action.GetPartyKeywords(it))
                }
            )
            Spacer(
                modifier = Modifier
                    .height(16.dp)
            )
            KeywordsList(
                keywords = state.partyKeywords
            )
        }
    }
}
