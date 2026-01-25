package ir.website.dashboard

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.update

class ViewModel {
    data class State(
        val searchQuery: String = "",
        val results: List<String> = emptyList()
    )


    val uiState = MutableStateFlow(State())

    sealed interface Action {
        data class UpdateSearchQuery(val newQuery: String) : Action
        data object GetResults : Action
    }

    fun onAction(action: Action) {
        when (action) {
            is Action.UpdateSearchQuery -> {
                updateSearchQuery(action.newQuery)
            }

            is Action.GetResults -> {
                getResults()
            }
        }
    }

    fun updateSearchQuery(newQuery: String) {
        uiState.update { it.copy(searchQuery = newQuery) }
    }

    fun getResults() {
        uiState.update {
            it.copy(
                results = listOf(
                    "Result 1 for ${uiState.value.searchQuery}",
                    "Result 2 for ${uiState.value.searchQuery}"
                )
            )
        }
    }
}