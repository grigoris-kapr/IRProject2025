from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.QueryHandler import QueryHandler

from pydantic import BaseModel

class Document(BaseModel):
    text: str
    keywords: list[str]

class Keywords(BaseModel):
    government_keywords: dict[str, list[str]]

qh = QueryHandler()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search", response_model=list[Document])
def read_root(query: str):
    query_results = qh.get_relevant_documents(query)
    return [Document(text=doc, keywords=keywords) for doc, keywords in query_results]

@app.get("/member/keywords", response_model=Keywords)
def get_keywords(member: str):
    return Keywords(government_keywords=qh.get_keywords_for_member(member))

@app.get("/party/keywords", response_model=Keywords)
def get_party_keywords(party: str):
    return Keywords(government_keywords=qh.get_keywords_for_party(party))
@app.get("/members", response_model=list[str])
def get_members():
    return qh.models.dataset['member_name'].unique().tolist()

@app.get("/parties", response_model=list[str])
def get_parties():
    return qh.models.dataset['political_party'].unique().tolist()

@app.get("/member/errors", response_model=dict[str, float])
def get_member_errors(member: str):
    return qh.get_member_errors(member)