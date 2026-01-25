from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

class Document(BaseModel):
    text: str
    keywords: list[str]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=list[Document])
def read_root():
    return [
        Document(text="Sample document 1", keywords=["sample", "document", "one"]),
        Document(text="Sample document 2", keywords=["sample", "document", "two"]),
		Document(text="Sample document 3", keywords=["sample", "document", "three"]),
        Document(text="Sample document 4", keywords=["sample", "document", "four"]),
	]