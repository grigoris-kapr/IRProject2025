package ir.website.dashboard.data

import kotlinx.serialization.Serializable

@Serializable
data class DocumentDto(
    val text: String,
    val keywords: List<String>
)

@Serializable
data class PartyKeywordsDto(
    val government_keywords: Map<String, List<String>>,
)

@Serializable
data class MemberKeywordsDto(
    val government_keywords: Map<String, List<String>>,
)

@Serializable
data class MemberErrorsDto(
    val errors: List<String>,
)