package ir.website.dashboard.ui

import ir.website.dashboard.data.Api
import ir.website.dashboard.data.DocumentDto
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class ViewModel {
    data class State(
        val searchQuery: String = "",
        val documents: List<DocumentDto> = emptyList()
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

        val scope = CoroutineScope(Dispatchers.Default)
        scope.launch {
            val documents = Api.getDocuments()
            uiState.update {
                it.copy(
                    documents = documents
                )
            }
        }
    }
}