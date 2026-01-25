package ir.website.dashboard.data

import kotlinx.serialization.Serializable

@Serializable
data class DocumentDto(
    val text: String,
    val keywords: List<String>
)