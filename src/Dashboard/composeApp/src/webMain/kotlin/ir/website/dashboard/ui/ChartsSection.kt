package ir.website.dashboard.ui

import androidx.compose.animation.core.snap
import androidx.compose.foundation.layout.*
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import ir.ehsannarmani.compose_charts.ColumnChart
import ir.ehsannarmani.compose_charts.extensions.format
import ir.ehsannarmani.compose_charts.models.BarProperties
import ir.ehsannarmani.compose_charts.models.Bars
import ir.ehsannarmani.compose_charts.models.HorizontalIndicatorProperties
import ir.ehsannarmani.compose_charts.models.LabelProperties
import ir.website.dashboard.components.Dropdown

@Composable
fun ChartsSection(
    state: ViewModel.State,
    onAction: (ViewModel.Action) -> Unit
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .fillMaxSize()
            .height(1000.dp)
    ) {
        Text(
            text = "Average member's difference from its party in various elections",
            style = TextStyle(
                color = Color.Black,
                fontSize = 50.sp
            )
        )
        Dropdown(
            label = "Select member",
            value = state.selectedMemberForChart,
            options = state.members,
            onOptionSelected = {
                onAction(ViewModel.Action.GetMemberChartData(it))
            }
        )
        if (state.chartData.isNotEmpty()) {
            ColumnChart(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(300.dp)
                    .padding(horizontal = 100.dp),
                data =
                    state.chartData.map {
                        Bars(
                            label = it.key,
                            values = listOf(
                                Bars.Data(value = it.value, color = SolidColor(Color.Red)),
                            )
                        )
                    },
                animationSpec = snap(),
                barProperties = BarProperties(
                    cornerRadius = Bars.Data.Radius.Rectangle(topRight = 6.dp, topLeft = 6.dp),
                    spacing = 3.dp,
                    thickness = 20.dp
                ),
                labelProperties = LabelProperties(
                    enabled = true,
                    rotation = LabelProperties.Rotation(
                        mode = LabelProperties.Rotation.Mode.Force
                    )
                ),
                indicatorProperties = HorizontalIndicatorProperties(
                    enabled = true,
                    contentBuilder = { value -> value.format(3) })
            )
        }
    }
}
