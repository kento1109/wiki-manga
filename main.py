from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import MeCab

import extract

app = FastAPI()
mc = MeCab.Tagger ("-Owakati -d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd")

TARGET_POS = ["名詞", " 動詞",  "形容詞"]
STOP_WORDS = ["漫画"]

class Query(BaseModel):
    text: str

class Result(BaseModel):
    title: str
    matched_tokens: List

def extract_key_tokens(text):
    extracted_tokens = []
    node = mc.parseToNode(text)
    while node:
        pos = node.feature.split(",")[0]
        if pos in TARGET_POS and node.surface not in STOP_WORDS:
            extracted_tokens.append(node.surface)
        node = node.next
    return extracted_tokens

@app.post("/search/")
def search_items(query: Query):
    query_tokens = extract_key_tokens(query.text)
    result = extract.serach_by_query(query_tokens)
    return result