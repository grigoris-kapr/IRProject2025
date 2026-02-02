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
        val isLoading: Boolean = false,
        val searchQuery: String = "",
        val documents: List<DocumentDto> = emptyList(),
        val members: List<String> = emptyList(),
        val parties: List<String> = emptyList(),
        val selectedMember: String = "",
        val selectedParty: String = "",
        val memberKeywords: Map<String, List<String>> = emptyMap(),
        val partyKeywords: Map<String, List<String>> = emptyMap(),
        val selectedMemberForChart: String = "",
        val chartData: Map<String, Double> = emptyMap()
    )

    val uiState = MutableStateFlow(State())
    private val scope = CoroutineScope(Dispatchers.Main)

    sealed interface Action {
        data object Initialize : Action
        data class UpdateSearchQuery(val newQuery: String) : Action
        data object GetResults : Action
        data class GetMemberKeywords(val member: String) : Action
        data class GetPartyKeywords(val party: String) : Action
        data class GetMemberChartData(val member: String) : Action
    }

    fun onAction(action: Action) {
        when (action) {
            is Action.Initialize -> {
                initialize()
            }

            is Action.UpdateSearchQuery -> {
                updateSearchQuery(action.newQuery)
            }

            is Action.GetResults -> {
                getResults(uiState.value.searchQuery)
            }

            is Action.GetMemberKeywords -> {
                getMemberKeywords(action.member)
            }

            is Action.GetPartyKeywords -> {
                getPartyKeywords(action.party)
            }

            is Action.GetMemberChartData -> {
                getMemberChartData(action.member)
            }
        }
    }

    private fun suspendedFun(
        block: suspend () -> Unit
    ) {
        scope.launch {
            uiState.update { it.copy(isLoading = true) }
            try {
                block()
            } finally {
                uiState.update { it.copy(isLoading = false) }
            }
        }
    }

    private fun initialize() {
        suspendedFun {
            val members = Api.getMembers()
            val parties = Api.getParties()
            uiState.update {
                it.copy(
                    members = members,
                    parties = parties
                )
            }
        }
    }

    fun updateSearchQuery(newQuery: String) {
        uiState.update { it.copy(searchQuery = newQuery) }
    }

    fun getResults(query: String) {
        suspendedFun {
            val documents = Api.getDocuments(query)
            uiState.update {
                it.copy(
                    documents = documents
                )
            }
        }
    }

    fun getMemberKeywords(member: String) {
        suspendedFun {
            uiState.update { it.copy(selectedMember = member) }
            val keywords = Api.getMemberKeywords(member).government_keywords
            uiState.update { it.copy(memberKeywords = keywords) }
        }
    }

    fun getPartyKeywords(party: String) {
        suspendedFun {
            uiState.update { it.copy(selectedParty = party) }
            val keywords = Api.getPartyKeywords(party).government_keywords
            uiState.update { it.copy(partyKeywords = keywords) }
        }
    }

    fun getMemberChartData(member: String) {
        suspendedFun {
            uiState.update { it.copy(selectedMemberForChart = member) }
            val errors = Api.getMemberErrors(member)
            uiState.update { it.copy(chartData = errors) }
        }
    }
}