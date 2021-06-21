from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

import MeCab
import extract

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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

@app.get("/search", response_class=HTMLResponse)
def search_items(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/result", response_class=HTMLResponse)
def show_items(request: Request, text: str = Form(...)):
    print("text", text)
    print("tagger", mc.parse(text))
    query_tokens = extract_key_tokens(text)
    print("query_tokens", query_tokens)
    results = extract.serach_by_query(query_tokens)
    print(type(results), results)
    return templates.TemplateResponse("result.html", {"request": request, "results": results})