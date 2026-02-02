package ir.website.dashboard.data

import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

object Api {
    private val client = HttpClient {
        install(ContentNegotiation) {
            json(
                Json {
                    ignoreUnknownKeys = true
                }
            )
        }
        defaultRequest {
            url("http://localhost:8000")
        }
    }

    suspend fun getDocuments(query: String): List<DocumentDto> {
        return client.get("/search") {
            parameter("query", query)
        }.body()
    }

    suspend fun getMembers(): List<String> {
        return client.get("/members").body()
    }

    suspend fun getParties(): List<String> {
        return client.get("/parties").body()
    }

    suspend fun getMemberKeywords(member: String): MemberKeywordsDto {
        return client.get("/member/keywords") {
            parameter("member", member)
        }.body()
    }

    suspend fun getPartyKeywords(party: String): PartyKeywordsDto {
        return client.get("/party/keywords") {
            parameter("party", party)
        }.body()
    }

    suspend fun getMemberErrors(member: String): Map<String, Double> {
        return client.get("/member/errors") {
            parameter("member", member)
        }.body()
    }
}